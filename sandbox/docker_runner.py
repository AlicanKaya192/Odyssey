"""Docker alıştırmalarını denetler.

`harness.py` gibi bu dosya da **tek başına ayakta durur**: uygulamanın
hiçbir modülünü import etmez, çünkü ayrı bir süreçte çalışıyor.

İki tür kontrol var:

- **Durağan** (Docker gerekmez): `dockerfile` (talimatlar, sıra, sabit
  etiket, exec biçimi, kök olmayan kullanıcı), `compose` (servis, port,
  ortam değişkeni, volume, bağımlılık) ve `command` (kişinin `commands.sh`
  dosyasına yazdığı `docker ...` komutu ayrıştırılıyor; **komut
  çalıştırılmıyor**).
- **Gerçek** (Docker açık olmalı): `container` imajı kişinin Dockerfile'ından
  gerçekten kuruyor, konteyneri çalıştırıp çıktısına, çıkış koduna, HTTP
  yanıtına, imajın boyutuna ve ayarlarına bakıyor; `compose_up` compose
  dosyasını gerçekten ayağa kaldırıyor.

Durağan bir kontrol düştüyse gerçek kontroller çalıştırılmıyor: önce
yazılan düzelsin, kurulum beklemesi boşa gitmesin.

Her şey `odyssey` etiketli: imajlar `odyssey-ex-<özet>`, konteynerler
`odyssey-run-<çalıştırma>`; iş bitince konteynerler ve compose projesi
siliniyor. Kişinin kendi konteynerlerine dokunulmuyor.

Kullanım (harness üzerinden):
    sonuc = run(job)   # job içinde language == "docker"
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Çıktı sınırı (harness ile aynı).
MAX_OUTPUT_CHARS = 100_000

# Docker'ın çalışıp çalışmadığını sorarken beklenen süre. Docker Desktop
# kapalıysa `docker info` hemen dönüyor; açılıyorsa uzun bekleme anlamsız.
INFO_TIMEOUT_SEC = 10

# HTTP kontrolünde sunucunun ayağa kalkması için beklenen en fazla süre.
HTTP_WAIT_SEC = 20

# Çalıştırma sonunda temizlik için ayrılan pay: genel süre dolmadan önce
# konteynerleri silebilmek için gerçek kontroller bu kadar erken bitiyor.
CLEANUP_RESERVE_SEC = 8

# Derleme günlüğünden terminale aktarılan en fazla satır (hata durumunda).
BUILD_TAIL_LINES = 25

# Tanınan Dockerfile talimatları. Bilinmeyen bir kelime (`FORM`, `COPPY`)
# Docker'da derlemeyi durdurur; burada daha anlaşılır söyleniyor.
INSTRUCTIONS = {
    "FROM", "RUN", "CMD", "LABEL", "MAINTAINER", "EXPOSE", "ENV", "ADD", "COPY",
    "ENTRYPOINT", "VOLUME", "USER", "WORKDIR", "ARG", "ONBUILD", "STOPSIGNAL",
    "HEALTHCHECK", "SHELL",
}

STATIC_TYPES = {"dockerfile", "compose", "command"}
REAL_TYPES = {"container", "compose_up"}

# Çalışma klasöründe kişinin dosyası olmayanlar: derleme bağlamına girmez.
WORKSPACE_ONLY = {"job.json", "result.json", "seed.sql"}

CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


def clip(text: str, limit: int = MAX_OUTPUT_CHARS) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    return text[:limit], True


def _fail(reason: str, **values) -> dict:
    """Düşen kontrolün ayrıntısı: grader `check.<tür>.<reason>` metnini seçiyor."""
    return {"passed": False, "reason": reason, "values": values}


def _ok(**values) -> dict:
    return {"passed": True, "reason": "", "values": values}


# --- Dockerfile ------------------------------------------------------------


class Instruction:
    """Dockerfile'ın tek bir talimatı (devam satırları birleşmiş)."""

    __slots__ = ("line", "name", "args", "stage")

    def __init__(self, line: int, name: str, args: str, stage: int) -> None:
        self.line = line
        self.name = name
        self.args = args
        self.stage = stage

    @property
    def flat(self) -> str:
        """Boşlukları teke indirilmiş argümanlar (kalıp araması için)."""
        return " ".join(self.args.split())


def parse_dockerfile(text: str) -> list[Instruction]:
    """Talimatları satır numaralarıyla döndürür.

    `\\` ile biten satır bir sonrakiyle birleşiyor; devam satırları
    arasındaki yorumlar atlanıyor (Docker da öyle yapıyor). `escape`
    yönergesi (dosyanın başında `# escape=`` `) tanınıyor.
    """
    lines = text.splitlines()
    escape = "\\"
    for raw in lines[:5]:
        match = re.match(r"^\s*#\s*escape\s*=\s*(\S)\s*$", raw, re.IGNORECASE)
        if match:
            escape = match.group(1)
            break
        if raw.strip() and not raw.strip().startswith("#"):
            break

    out: list[Instruction] = []
    stage = -1
    index = 0
    while index < len(lines):
        raw = lines[index]
        start = index + 1
        stripped = raw.strip()
        index += 1
        if not stripped or stripped.startswith("#"):
            continue
        buffer = raw.rstrip()
        while buffer.endswith(escape) and index < len(lines):
            buffer = buffer[: -len(escape)].rstrip()
            nxt = lines[index].strip()
            index += 1
            if not nxt or nxt.startswith("#"):
                # Devam ortasındaki yorum ve boş satır atlanıyor; satır
                # sürmeye devam ediyor.
                buffer += escape
                continue
            buffer = buffer + " " + nxt
        if buffer.endswith(escape):
            buffer = buffer[: -len(escape)]
        parts = buffer.strip().split(None, 1)
        name = parts[0].upper()
        args = parts[1].strip() if len(parts) > 1 else ""
        if name == "FROM":
            stage += 1
        out.append(Instruction(start, name, args, max(stage, 0)))
    return out


def _exec_form(args: str) -> bool:
    """`["python", "app.py"]` biçimi mi (JSON dizi)."""
    if not args.startswith("["):
        return False
    try:
        value = json.loads(args)
    except ValueError:
        return False
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _from_parts(args: str) -> tuple[str, str]:
    """`FROM` satırından imaj ve (varsa) aşama adı."""
    words = [word for word in args.split() if not word.startswith("--")]
    image = words[0] if words else ""
    alias = words[2] if len(words) >= 3 and words[1].lower() == "as" else ""
    return image, alias


def _pinned(image: str) -> bool:
    """Etiket ya da özet yazılmış mı (`latest` sayılmıyor)."""
    if "@" in image:
        return True
    last = image.rsplit("/", 1)[-1]
    if ":" not in last:
        return False
    return last.split(":", 1)[1].lower() != "latest"


def _matches(instruction: Instruction, spec: dict) -> bool:
    if instruction.name != str(spec.get("instruction", "")).upper():
        return False
    pattern = spec.get("value")
    return not pattern or re.search(pattern, instruction.flat) is not None


def _show(spec: dict) -> str:
    """Mesajda gösterilecek talimat: yazarın verdiği `show` ya da talimat adı."""
    return str(spec.get("show") or spec.get("instruction", "")).strip()


def _in_stage(instructions: list[Instruction], spec: dict) -> list[Instruction]:
    """`stage: "last"` verilmişse yalnızca son aşamanın talimatları."""
    if spec.get("stage") == "last" and instructions:
        last = max(item.stage for item in instructions)
        return [item for item in instructions if item.stage == last]
    return instructions


def check_dockerfile(check: dict, workspace: Path) -> dict:
    name = str(check.get("file") or "Dockerfile")
    path = workspace / name
    if not path.is_file():
        return _fail("no_file", file=name)
    instructions = parse_dockerfile(path.read_text(encoding="utf-8", errors="replace"))
    if not instructions:
        return _fail("empty", file=name)

    # Her kural önce dosyanın Docker'ın okuyabileceği bir dosya olduğuna
    # bakıyor: yazım hatası varsa asıl söylenmesi gereken o.
    for item in instructions:
        if item.name not in INSTRUCTIONS:
            return _fail("unknown", file=name, line=item.line, word=item.name)
    if instructions[0].name not in ("FROM", "ARG"):
        return _fail("from_first", file=name, line=instructions[0].line)

    rule = check.get("rule", "has")
    scope = _in_stage(instructions, check)

    if rule == "has":
        found = [item for item in scope if _matches(item, check)]
        if not found:
            return _fail("missing", file=name, what=_show(check))
        return _ok()

    if rule == "forbid":
        for item in scope:
            if _matches(item, check):
                return _fail("forbidden", file=name, what=_show(check), line=item.line)
        return _ok()

    if rule == "order":
        position = -1
        previous = ""
        for spec in check.get("steps", []):
            spec = dict(spec, stage=check.get("stage"))
            hits = [i for i, item in enumerate(scope) if _matches(item, spec)]
            if not hits:
                return _fail("missing", file=name, what=_show(spec))
            after = [i for i in hits if i > position]
            if not after:
                return _fail("order", file=name, first=previous, second=_show(spec))
            position = after[0]
            previous = _show(spec)
        return _ok()

    if rule == "pinned":
        aliases: set[str] = set()
        for item in instructions:
            if item.name != "FROM":
                continue
            image, alias = _from_parts(item.args)
            if image.lower() != "scratch" and image not in aliases and not _pinned(image):
                return _fail("unpinned", file=name, image=image, line=item.line)
            if alias:
                aliases.add(alias)
        return _ok()

    if rule == "exec_form":
        wanted = str(check.get("instruction", "CMD")).upper()
        found = [item for item in scope if item.name == wanted]
        if not found:
            return _fail("missing", file=name, what=wanted)
        last = found[-1]
        if not _exec_form(last.args):
            return _fail("shell_form", file=name, instruction=wanted, line=last.line)
        # `args` listesi verilmişse JSON dizisi birebir karşılaştırılıyor:
        # `["python","app.py"]` ile `["python", "app.py"]` aynı.
        if "args" in check and json.loads(last.args) != list(check["args"]):
            return _fail("missing", file=name, what=_show(check))
        if check.get("value") and not re.search(check["value"], last.flat):
            return _fail("missing", file=name, what=_show(check))
        return _ok()

    if rule == "non_root":
        last_stage = max(item.stage for item in instructions)
        users = [item for item in instructions if item.stage == last_stage and item.name == "USER"]
        if not users:
            return _fail("no_user", file=name)
        user = users[-1].args.split(":", 1)[0].strip()
        if user in ("root", "0"):
            return _fail("root_user", file=name, line=users[-1].line)
        return _ok()

    if rule == "stages":
        count = sum(1 for item in instructions if item.name == "FROM")
        if count < int(check.get("min", 2)):
            return _fail("stages", file=name, count=count, min=int(check.get("min", 2)))
        return _ok()

    if rule == "count":
        wanted = str(check.get("instruction", "")).upper()
        count = sum(1 for item in scope if _matches(item, check))
        if "max" in check and count > int(check["max"]):
            return _fail("too_many", file=name, what=_show(check) or wanted, count=count, max=check["max"])
        if "min" in check and count < int(check["min"]):
            return _fail("too_few", file=name, what=_show(check) or wanted, count=count, min=check["min"])
        return _ok()

    return _fail("bad_rule", rule=str(rule))


# --- compose.yaml ----------------------------------------------------------


def _load_yaml(path: Path) -> tuple[object, dict | None]:
    """Dosyayı okur; hata varsa (None, ayrıntı)."""
    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        return None, _fail("no_yaml")
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8", errors="replace")), None
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = mark.line + 1 if mark is not None else 0
        problem = str(getattr(exc, "problem", "") or exc).strip()
        return None, _fail("yaml_error", file=path.name, line=line, problem=problem)


def _port_pairs(entries) -> set[str]:
    """Portları `host:container` biçimine indirir (`8080:80`, `:80`)."""
    pairs: set[str] = set()
    for entry in entries or []:
        if isinstance(entry, dict):
            host = str(entry.get("published", "") or "")
            target = str(entry.get("target", "") or "")
        else:
            text = str(entry).split("/", 1)[0]
            parts = text.split(":")
            target = parts[-1]
            host = parts[-2] if len(parts) >= 2 else ""
        pairs.add(f"{host}:{target}")
    return pairs


def _port_busy(port: int) -> bool:
    """Bilgisayarda bu portu dinleyen bir şey var mı (Docker'ın açtıkları dahil).

    Windows'ta sıradan `bind` başka sürecin dinlediği portu boş sanabiliyor:
    Docker Desktop'ın açtığı `0.0.0.0:8095` IPv4'te bağlanmaya izin verdi
    (ölçüldü). Bu yüzden tek başına sahiplik (`SO_EXCLUSIVEADDRUSE`) isteniyor
    ve ayrıca porta bağlanmak deneniyor; dinleyen varsa bağlantı kabul ediliyor.
    """
    for host in ("127.0.0.1", "::1"):
        family = socket.AF_INET6 if ":" in host else socket.AF_INET
        try:
            with socket.socket(family, socket.SOCK_STREAM) as probe:
                probe.settimeout(0.3)
                if probe.connect_ex((host, port)) == 0:
                    return True
        except OSError:
            pass
    exclusive = getattr(socket, "SO_EXCLUSIVEADDRUSE", None)
    for family, host in ((socket.AF_INET, "0.0.0.0"), (socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::")):
        try:
            with socket.socket(family, socket.SOCK_STREAM) as probe:
                if exclusive is not None:
                    probe.setsockopt(socket.SOL_SOCKET, exclusive, 1)
                probe.bind((host, port))
        except OSError as exc:
            # IPv6 kapalı makinede adres ailesi hatası doluluk sayılmıyor.
            if family == socket.AF_INET6 and getattr(exc, "winerror", None) in (10047, 10049):
                continue
            if family == socket.AF_INET6 and exc.errno in (97, 99):
                continue
            return True
    return False


def _free_port_near(port: int, taken: set[int]) -> int:
    for candidate in range(port + 1, min(port + 200, 65535)):
        if candidate not in taken and not _port_busy(candidate):
            return candidate
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("0.0.0.0", 0))
        return probe.getsockname()[1]


def _move_busy_ports(data: dict) -> list[tuple[str, int, int]]:
    """Compose verisinde dolu ana makine portlarını boş olanlarla değiştirir.

    `8095:8000`, `127.0.0.1:8095:8000`, `8095:8000/tcp` ve uzun yazım
    (`published`) tanınıyor; aralıklar ve yalnızca konteyner portu olanlar
    olduğu gibi bırakılıyor. Döndürdüğü liste: (servis, eski, yeni).
    """
    moved: list[tuple[str, int, int]] = []
    taken: set[int] = set()
    for service_name, service in (data.get("services") or {}).items():
        if not isinstance(service, dict) or not isinstance(service.get("ports"), list):
            continue
        entries = service["ports"]
        for index, entry in enumerate(entries):
            if isinstance(entry, dict):
                published = str(entry.get("published", "") or "")
                if not published.isdigit():
                    continue
                port = int(published)
            else:
                text = str(entry)
                main, slash, proto = text.partition("/")
                parts = main.split(":")
                if len(parts) < 2 or not parts[-2].isdigit():
                    continue
                port = int(parts[-2])
            if _port_busy(port):
                new = _free_port_near(port, taken)
                if isinstance(entry, dict):
                    entry["published"] = str(new) if isinstance(entry.get("published"), str) else new
                else:
                    parts[-2] = str(new)
                    entries[index] = ":".join(parts) + (slash + proto if slash else "")
                moved.append((str(service_name), port, new))
                port = new
            taken.add(port)
    return moved


def _dump_yaml(path: Path, data: dict) -> None:
    import yaml  # noqa: PLC0415

    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def _environment(value) -> dict[str, str | None]:
    if isinstance(value, dict):
        return {str(k): None if v is None else str(v) for k, v in value.items()}
    env: dict[str, str | None] = {}
    for item in value or []:
        text = str(item)
        key, sep, val = text.partition("=")
        env[key] = val if sep else None
    return env


def _volume_pairs(entries) -> list[tuple[str, str, str]]:
    """Volume girdilerini (kaynak, hedef, kip) üçlüsüne indirir."""
    out = []
    for entry in entries or []:
        if isinstance(entry, dict):
            out.append((str(entry.get("source", "") or ""), str(entry.get("target", "") or ""),
                        "ro" if entry.get("read_only") else ""))
            continue
        parts = str(entry).split(":")
        # Windows sürücü harfi (`C:\x:/data`) burada beklenmiyor; içerik
        # göreli yol ve adlandırılmış volume kullanıyor.
        if len(parts) == 1:
            out.append(("", parts[0], ""))
        elif len(parts) == 2:
            out.append((parts[0], parts[1], ""))
        else:
            out.append((parts[0], parts[1], parts[2]))
    return out


def _norm_path(text: str) -> str:
    text = text.strip()
    if text.startswith("./"):
        text = text[2:]
    return text.rstrip("/") or text


def check_compose(check: dict, workspace: Path) -> dict:
    name = str(check.get("file") or "compose.yaml")
    path = workspace / name
    if not path.is_file():
        return _fail("no_file", file=name)
    data, error = _load_yaml(path)
    if error:
        return error
    if not isinstance(data, dict) or not isinstance(data.get("services"), dict) or not data["services"]:
        return _fail("no_services", file=name)

    for volume in check.get("top_volumes", []):
        if not isinstance(data.get("volumes"), dict) or volume not in data["volumes"]:
            return _fail("top_volume_missing", file=name, name=volume)

    service_name = check.get("service")
    if not service_name:
        return _ok()
    service = data["services"].get(service_name)
    if not isinstance(service, dict):
        return _fail("no_service", file=name, service=service_name)

    if "image" in check:
        image = str(service.get("image", "") or "")
        if not image:
            return _fail("image_missing", service=service_name)
        if not re.search(check["image"], image):
            return _fail("image_wrong", service=service_name, expected=check.get("show_image", check["image"]),
                         actual=image)

    if check.get("build") and not service.get("build"):
        return _fail("no_build", service=service_name)

    if check.get("no_ports") and service.get("ports"):
        return _fail("ports_present", service=service_name)

    if check.get("ports"):
        found = _port_pairs(service.get("ports"))
        for wanted in check["ports"]:
            if str(wanted) not in found:
                return _fail("port_missing", service=service_name, port=str(wanted))

    if check.get("environment"):
        env = _environment(service.get("environment"))
        for key, value in check["environment"].items():
            if key not in env:
                return _fail("env_missing", service=service_name, name=key)
            if value is not None and env[key] != str(value):
                return _fail("env_wrong", service=service_name, name=key, expected=str(value),
                             actual=str(env[key]))

    if check.get("env_file") and not service.get("env_file"):
        return _fail("no_env_file", service=service_name)

    if check.get("volumes"):
        found = {(_norm_path(src), _norm_path(dst)) for src, dst, _ in _volume_pairs(service.get("volumes"))}
        for wanted in check["volumes"]:
            src, _, dst = str(wanted).partition(":")
            if (_norm_path(src), _norm_path(dst.split(":")[0])) not in found:
                return _fail("volume_missing", service=service_name, volume=str(wanted))

    if check.get("depends_on"):
        depends = service.get("depends_on") or []
        names = set(depends) if isinstance(depends, (list, dict)) else set()
        for wanted in check["depends_on"]:
            if wanted not in names:
                return _fail("depends_missing", service=service_name, name=wanted)
        condition = check.get("depends_condition")
        if condition:
            for wanted in check["depends_on"]:
                spec = depends.get(wanted) if isinstance(depends, dict) else None
                if not isinstance(spec, dict) or spec.get("condition") != condition:
                    return _fail("depends_condition", service=service_name, name=wanted, condition=condition)

    if "command" in check:
        command = service.get("command")
        text = " ".join(command) if isinstance(command, list) else str(command or "")
        if not re.search(check["command"], text):
            return _fail("command_wrong", service=service_name, expected=check.get("show_command", check["command"]),
                         actual=text)

    if "restart" in check and str(service.get("restart", "")) != check["restart"]:
        return _fail("restart_wrong", service=service_name, expected=check["restart"],
                     actual=str(service.get("restart", "")))

    if check.get("healthcheck") and not isinstance(service.get("healthcheck"), dict):
        return _fail("no_healthcheck", service=service_name)

    return _ok()


def compose_guard(data: dict) -> dict | None:
    """Ayağa kaldırmadan önce bilgisayara dokunan ayarları reddeder.

    Alıştırma konteyneri kişinin kendi bilgisayarında çalışıyor; tam yetki,
    ana makinenin ağı ya da çalışma klasörünün dışına bağlama gerekmiyor.
    """
    for name, service in (data.get("services") or {}).items():
        if not isinstance(service, dict):
            continue
        if service.get("privileged"):
            return _fail("unsafe", service=name, setting="privileged")
        for key in ("network_mode", "pid", "ipc"):
            if str(service.get(key, "")) == "host":
                return _fail("unsafe", service=name, setting=f"{key}: host")
        for src, _dst, _mode in _volume_pairs(service.get("volumes")):
            if src.startswith(("/", "~", "\\")) or ":" in src[1:3] or ".." in src.replace("\\", "/").split("/"):
                return _fail("unsafe", service=name, setting=f"volumes: {src}")
    return None


# --- commands.sh -----------------------------------------------------------

# Değer alan bayraklar ve kısa adların uzun karşılıkları, alt komuta göre.
# Aynı kısa ad iki yerde farklı şey: `run -t` terminal, `build -t` etiket.
_RUN = {
    "short": {"p": "--publish", "e": "--env", "v": "--volume", "d": "--detach", "i": "--interactive",
              "t": "--tty", "w": "--workdir", "u": "--user", "l": "--label", "m": "--memory",
              "P": "--publish-all", "h": "--hostname"},
    "values": {"--publish", "--env", "--volume", "--name", "--workdir", "--user", "--env-file",
               "--restart", "--entrypoint", "--memory", "--cpus", "--label", "--network", "--mount",
               "--platform", "--hostname", "--cap-add", "--cap-drop", "--add-host", "--expose",
               "--health-cmd", "--health-interval", "--pull", "--stop-timeout"},
}
FLAG_TABLES = {
    "run": _RUN,
    "create": _RUN,
    "build": {"short": {"t": "--tag", "f": "--file", "q": "--quiet"},
              "values": {"--tag", "--file", "--build-arg", "--target", "--platform", "--label",
                         "--network", "--progress", "--cache-from"}},
    "exec": {"short": {"e": "--env", "i": "--interactive", "t": "--tty", "d": "--detach",
                       "u": "--user", "w": "--workdir"},
             "values": {"--env", "--user", "--workdir"}},
    "logs": {"short": {"f": "--follow", "n": "--tail", "t": "--timestamps"},
             "values": {"--tail", "--since", "--until"}},
    "ps": {"short": {"a": "--all", "q": "--quiet", "f": "--filter", "n": "--last", "s": "--size"},
           "values": {"--filter", "--format", "--last"}},
    "images": {"short": {"a": "--all", "q": "--quiet", "f": "--filter"}, "values": {"--filter", "--format"}},
    "rm": {"short": {"f": "--force", "v": "--volumes"}, "values": set()},
    "rmi": {"short": {"f": "--force"}, "values": set()},
    "stop": {"short": {"t": "--time", "s": "--signal"}, "values": {"--time", "--signal"}},
    "inspect": {"short": {"f": "--format"}, "values": {"--format", "--type"}},
    "pull": {"short": {"q": "--quiet", "a": "--all-tags"}, "values": {"--platform"}},
    "cp": {"short": {"a": "--archive", "L": "--follow-link", "q": "--quiet"}, "values": set()},
    "network create": {"short": {"d": "--driver"}, "values": {"--driver", "--subnet", "--label"}},
    "volume create": {"short": {"d": "--driver"}, "values": {"--driver", "--label"}},
    "compose": {"short": {"f": "--file", "p": "--project-name"},
                "values": {"--file", "--project-name", "--env-file", "--profile"}},
    "compose up": {"short": {"d": "--detach"}, "values": {"--scale", "--wait-timeout"}},
    "compose down": {"short": {"v": "--volumes"}, "values": {"--rmi", "--timeout"}},
    "compose logs": {"short": {"f": "--follow", "n": "--tail", "t": "--timestamps"}, "values": {"--tail"}},
    "compose exec": {"short": {"e": "--env", "u": "--user", "w": "--workdir", "T": "--no-TTY", "d": "--detach"},
                     "values": {"--env", "--user", "--workdir"}},
    "compose run": {"short": {"e": "--env", "p": "--publish", "d": "--detach", "v": "--volume"},
                    "values": {"--env", "--publish", "--name", "--volume", "--entrypoint"}},
    "compose ps": {"short": {"a": "--all", "q": "--quiet"}, "values": {"--format", "--status"}},
}
# `docker image ls` ile `docker images` aynı; gruplar iki kelimelik alt komut.
GROUPS = {"image", "container", "network", "volume", "compose", "system", "builder", "buildx", "context"}
ALIASES = {"image ls": "images", "image list": "images", "container ls": "ps", "container list": "ps",
           "container run": "run", "container rm": "rm", "image rm": "rmi", "container stop": "stop",
           "container logs": "logs", "container exec": "exec", "image build": "build", "buildx build": "build",
           "image pull": "pull", "image inspect": "inspect", "container inspect": "inspect",
           "image history": "history", "image tag": "tag", "image push": "push",
           "container start": "start", "container restart": "restart", "container prune": "container prune",
           "container cp": "cp"}


def _command_lines(text: str) -> list[tuple[int, str]]:
    """Komut satırları: `\\` (bash) ve `` ` `` (PowerShell) devamları birleşiyor."""
    out: list[tuple[int, str]] = []
    buffer = ""
    start = 0
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()
        if not buffer:
            start = number
            if not line.strip() or line.strip().startswith("#"):
                continue
        if line.endswith(("\\", "`")):
            buffer += line[:-1] + " "
            continue
        buffer += line
        out.append((start, buffer.strip()))
        buffer = ""
    if buffer.strip():
        out.append((start, buffer.strip()))
    return out


def parse_docker_command(text: str) -> dict | None:
    """`docker ...` satırını alt komut, bayraklar ve konum argümanlarına ayırır.

    Bayraklar uzun adlarıyla saklanıyor (`-p` → `--publish`); birleşik kısa
    bayraklar (`-it`, `-dp 8080:80`) ve `--ad=değer` biçimi tanınıyor.
    Docker değilse ya da ayrıştırılamıyorsa None.
    """
    try:
        tokens = shlex.split(text, comments=True, posix=True)
    except ValueError:
        return None
    if not tokens or Path(tokens[0]).name.lower() not in ("docker", "docker.exe"):
        return None

    rest = tokens[1:]
    words: list[str] = []
    flags: dict[str, list] = {}
    positionals: list[str] = []

    def table_for() -> dict:
        key = ALIASES.get(" ".join(words), " ".join(words))
        return FLAG_TABLES.get(key, {"short": {}, "values": set()})

    def add(flag: str, value) -> None:
        flags.setdefault(flag, []).append(value)

    index = 0
    while index < len(rest):
        token = rest[index]
        index += 1
        table = table_for()
        if token.startswith("--") and len(token) > 2:
            name, sep, value = token.partition("=")
            if sep:
                add(name, value)
            elif name in table["values"] and index < len(rest):
                add(name, rest[index])
                index += 1
            else:
                add(name, True)
            continue
        if token.startswith("-") and len(token) > 1 and not positionals:
            letters = token[1:]
            position = 0
            while position < len(letters):
                letter = letters[position]
                name = table["short"].get(letter, "-" + letter)
                position += 1
                if name in table["values"]:
                    value = letters[position:]
                    if not value and index < len(rest):
                        value = rest[index]
                        index += 1
                    add(name, value)
                    break
                add(name, True)
            continue
        if token.startswith("-") and len(token) > 1:
            # Konum argümanından sonraki bayrak (`docker run imaj -c x`)
            # konteynerin komutuna ait; olduğu gibi kalıyor.
            positionals.append(token)
            continue
        # Alt komut kelimeleri: `compose up`, `image ls`, `network create`.
        if not positionals and (not words or (len(words) == 1 and words[0] in GROUPS)):
            words.append(token)
            continue
        positionals.append(token)

    command = ALIASES.get(" ".join(words), " ".join(words))
    return {"command": command, "flags": flags, "args": positionals}


def _flag_values(parsed: dict, flag: str) -> list:
    return parsed["flags"].get(flag, [])


def _command_problems(parsed: dict, check: dict) -> list[dict]:
    """Bir komut satırının beklentiden sapmaları (ilki mesaja gidiyor)."""
    problems = []
    command = check.get("command", "")
    for flag, wanted in (check.get("flags") or {}).items():
        values = _flag_values(parsed, flag)
        if not values:
            problems.append(_fail("flag_missing", command=command, flag=flag))
            continue
        if wanted is True:
            continue
        wanted_list = wanted if isinstance(wanted, list) else [wanted]
        for item in wanted_list:
            if str(item) not in [str(value) for value in values]:
                problems.append(_fail("flag_wrong", command=command, flag=flag, expected=str(item),
                                      actual=", ".join(str(value) for value in values if value is not True)))
                break
    for position, wanted in enumerate(check.get("args") or []):
        actual = parsed["args"][position] if position < len(parsed["args"]) else ""
        if actual != str(wanted):
            problems.append(_fail("arg_wrong", command=command, expected=str(wanted), actual=actual or "—"))
            break
    for flag in check.get("forbid_flags") or []:
        if _flag_values(parsed, flag):
            problems.append(_fail("flag_forbidden", command=command, flag=flag))
    return problems


def check_command(check: dict, workspace: Path) -> dict:
    name = str(check.get("file") or "commands.sh")
    path = workspace / name
    if not path.is_file():
        return _fail("no_file", file=name)
    command = str(check.get("command", ""))
    candidates = []
    for line, text in _command_lines(path.read_text(encoding="utf-8", errors="replace")):
        parsed = parse_docker_command(text)
        if parsed is None:
            # `curl localhost:8080` gibi Docker dışı satırlar serbest.
            continue
        if parsed["command"] == command:
            candidates.append(_command_problems(parsed, check))
    if not candidates:
        return _fail("no_command", file=name, command=command, show=check.get("show", "docker " + command))
    best = min(candidates, key=len)
    if best:
        return best[0]
    return _ok()


# --- Docker'ın kendisi -----------------------------------------------------


def docker_path() -> str:
    """`docker` komutunun yolu; bulunamazsa boş."""
    found = shutil.which("docker")
    if found:
        return found
    candidates = []
    for base in (os.environ.get("ProgramFiles", ""), os.environ.get("LOCALAPPDATA", "")):
        if base:
            candidates.append(Path(base) / "Docker" / "Docker" / "resources" / "bin" / "docker.exe")
            candidates.append(Path(base) / "Programs" / "DockerDesktop" / "resources" / "bin" / "docker.exe")
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return ""


class Docker:
    """`docker` komutunu süre sınırıyla çağıran küçük yardımcı."""

    def __init__(self, exe: str, deadline: float) -> None:
        self.exe = exe
        self.deadline = deadline

    def remaining(self) -> float:
        return self.deadline - time.monotonic()

    def call(self, args: list[str], timeout: float | None = None, cwd: Path | None = None,
             cleanup: bool = False) -> subprocess.CompletedProcess:
        # Temizlik genel süreye bağlı değil: süre dolduğu için çağrılıyor.
        if cleanup:
            limit = float(timeout or 30)
        else:
            limit = self.remaining() if timeout is None else min(timeout, self.remaining())
        if limit <= 0:
            raise subprocess.TimeoutExpired([self.exe, *args], 0)
        return subprocess.run(
            [self.exe, *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=limit, creationflags=CREATE_NO_WINDOW, stdin=subprocess.DEVNULL,
        )


def docker_state(exe: str) -> tuple[str, str]:
    """("ok", sürüm) / ("missing", "") / ("stopped", ayrıntı)."""
    if not exe:
        return "missing", ""
    try:
        done = subprocess.run(
            [exe, "info", "--format", "{{.ServerVersion}}"], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=INFO_TIMEOUT_SEC,
            creationflags=CREATE_NO_WINDOW, stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "stopped", str(exc)
    version = done.stdout.strip()
    if done.returncode != 0 or not version:
        return "stopped", (done.stderr or done.stdout).strip()[:300]
    return "ok", version


def image_tag(key: str) -> str:
    return "odyssey-ex-" + hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]


def _build_steps(log: str) -> list[str]:
    """`--progress=plain` günlüğünden adımlar: `[2/4] COPY app.py .  CACHED`.

    Ham günlük yüzlerce satır; terminalde yalnızca hangi adımın önbellekten
    geldiği, hangisinin yeniden çalıştığı gösteriliyor (katman dersinin
    gördürmek istediği şey bu).
    """
    titles: dict[str, str] = {}
    states: dict[str, str] = {}
    order: list[str] = []
    for line in log.splitlines():
        match = re.match(r"^#(\d+) \[(?:[\w.-]+ )?\s*(\d+/\d+)\] (.+)$", line)
        if match:
            step = match.group(1)
            if step not in titles:
                order.append(step)
                # `FROM docker.io/library/python:3.13-slim@sha256:...` →
                # Dockerfile'da yazıldığı gibi `FROM python:3.13-slim`.
                title = re.sub(r"docker\.io/library/|@sha256:[0-9a-f]+", "", match.group(3).strip())
                titles[step] = f"[{match.group(2)}] {title}"
            continue
        match = re.match(r"^#(\d+) (CACHED|DONE [\d.]+s|ERROR.*)$", line)
        if match and match.group(1) in titles:
            states[match.group(1)] = match.group(2)
    # Günlükte adımlar paralel kurulduğu için karışık geliyor; Dockerfile
    # sırasına (`[2/6]`) diziliyor.
    order.sort(key=lambda step: int(re.match(r"\[(\d+)", titles[step]).group(1)))
    lines = []
    for step in order:
        title = titles[step]
        if len(title) > 60:
            title = title[:57] + "..."
        lines.append(f"  {title:<60} {states.get(step, '')}".rstrip())
    return lines


def _build_context(workspace: Path) -> Path:
    """Derleme bağlamı: kişinin dosyaları (denetleyicinin iş dosyaları hariç)."""
    context = workspace / ".odyssey-build"
    if context.exists():
        shutil.rmtree(context, ignore_errors=True)
    context.mkdir()
    for item in workspace.iterdir():
        if item.name in WORKSPACE_ONLY or item.name == context.name:
            continue
        if item.is_dir():
            shutil.copytree(item, context / item.name)
        else:
            shutil.copy2(item, context / item.name)
    return context


def _http_get(url: str, timeout: float) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "odyssey-check"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(request, timeout=timeout) as response:
            return response.status, response.read(200_000).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(200_000).decode("utf-8", errors="replace")


def _compare_http(expect: dict, status: int, body: str) -> dict | None:
    if "status" in expect and status != int(expect["status"]):
        return _fail("http_status", path=expect.get("path", "/"), expected=expect["status"], actual=status)
    if "contains" in expect and str(expect["contains"]) not in body:
        return _fail("http_body", path=expect.get("path", "/"), expected=str(expect["contains"]),
                     actual=body.strip()[:200])
    if "json" in expect:
        try:
            value = json.loads(body)
        except ValueError:
            return _fail("http_not_json", path=expect.get("path", "/"), actual=body.strip()[:200])
        if value != expect["json"]:
            return _fail("http_json", path=expect.get("path", "/"),
                         expected=json.dumps(expect["json"], ensure_ascii=False),
                         actual=json.dumps(value, ensure_ascii=False)[:300])
    return None


def _one_line(body: str, limit: int = 100) -> str:
    """Yanıt gövdesi terminalde tek satır (HTML sayfası yüzlerce satır olabiliyor)."""
    text = " ".join(body.split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _lines(text: str) -> list[str]:
    return [line.rstrip() for line in text.strip().splitlines()]


class RealChecks:
    """Gerçek kontroller: imaj bir kez kuruluyor, kontroller paylaşıyor."""

    def __init__(self, docker: Docker, workspace: Path, run_id: str, key: str, transcript: list[str]) -> None:
        self.docker = docker
        self.workspace = workspace
        self.run_id = run_id
        self.key = key
        self.transcript = transcript
        self.builds: dict[str, tuple[str, dict | None]] = {}
        self.containers: list[str] = []
        self.projects: list[tuple[str, str]] = []
        self.counter = 0
        # Alıştırmanın adlandırdığı volume → bu çalıştırmaya özel gerçek ad.
        self.volumes: dict[str, str] = {}

    def labels(self) -> list[str]:
        return ["--label", "odyssey=1", "--label", f"odyssey.run={self.run_id}"]

    # --- imaj

    def build(self, spec: dict) -> tuple[str, dict | None]:
        """İmajı kurar; (etiket, hata ayrıntısı ya da None)."""
        cache_key = json.dumps(spec, sort_keys=True)
        if cache_key in self.builds:
            return self.builds[cache_key]
        dockerfile = str(spec.get("file") or "Dockerfile")
        if not (self.workspace / dockerfile).is_file():
            result = ("", _fail("no_file", file=dockerfile))
            self.builds[cache_key] = result
            return result
        tag = image_tag(self.key + "|" + cache_key)
        context = _build_context(self.workspace)
        args = ["build", "--progress=plain", "-t", tag, "-f", dockerfile, *self.labels()]
        if spec.get("target"):
            args += ["--target", str(spec["target"])]
        for name, value in (spec.get("args") or {}).items():
            args += ["--build-arg", f"{name}={value}"]
        args.append(".")
        shown = "docker build" + (f" -f {dockerfile}" if dockerfile != "Dockerfile" else "")
        if spec.get("target"):
            shown += f" --target {spec['target']}"
        self.transcript.append(f"❯ {shown} -t {spec.get('show_tag', 'app')} .")
        started = time.monotonic()
        try:
            done = self.docker.call(args, cwd=context)
        except subprocess.TimeoutExpired:
            result = ("", _fail("build_timeout"))
            self.builds[cache_key] = result
            return result
        log = (done.stdout or "") + (done.stderr or "")
        steps = _build_steps(log)
        if done.returncode != 0:
            self.transcript.extend(steps)
            tail = [line for line in log.strip().splitlines() if line.strip()][-BUILD_TAIL_LINES:]
            self.transcript.extend("  " + line for line in tail)
            result = ("", _fail("build_failed", log=_build_error(log)))
        else:
            self.transcript.extend(steps)
            self.transcript.append(f"  => {time.monotonic() - started:.1f}s")
            result = (tag, None)
            # Aynı etiket yeniden kurulunca eskisi adsız (dangling) kalıyor;
            # yalnızca Odyssey'nin etiketli artıkları siliniyor.
            try:
                self.docker.call(["image", "prune", "-f", "--filter", "label=odyssey=1"], timeout=30)
            except subprocess.TimeoutExpired:
                pass
        self.builds[cache_key] = result
        return result

    def inspect(self, tag: str) -> dict:
        done = self.docker.call(["image", "inspect", tag, "--format", "{{json .}}"], timeout=20)
        try:
            return json.loads(done.stdout)
        except ValueError:
            return {}

    # --- konteyner

    def name(self) -> str:
        self.counter += 1
        name = f"odyssey-run-{self.run_id}-{self.counter}"
        self.containers.append(name)
        return name

    def volume(self, name: str) -> str:
        """Alıştırmadaki `notes` volume'u → `odyssey-<çalıştırma>-notes` (etiketli).

        Aynı çalıştırmadaki kontroller aynı volume'u paylaşıyor: biri yazıyor,
        sonraki (yeni bir konteyner) okuyor. Çalıştırma sonunda siliniyor.
        """
        if name not in self.volumes:
            real = f"odyssey-{self.run_id}-{re.sub(r'[^a-zA-Z0-9_.-]', '-', name)}"
            self.docker.call(["volume", "create", *self.labels(), real], timeout=30)
            self.volumes[name] = real
        return self.volumes[name]

    def run_args(self, run: dict) -> list[str]:
        args: list[str] = []
        for key, value in (run.get("env") or {}).items():
            args += ["-e", f"{key}={value}"]
        if run.get("user"):
            args += ["--user", str(run["user"])]
        for spec in run.get("volumes") or []:
            name, _, target = str(spec).partition(":")
            args += ["-v", f"{self.volume(name)}:{target}"]
        return args

    def container(self, check: dict) -> dict:
        image = check.get("image")
        if image:
            tag = str(image)
        else:
            tag, error = self.build(check.get("build") or {})
            if error:
                return error
        expect = check.get("expect") or {}
        run = check.get("run") or {}

        info = {}
        if any(key in expect for key in ("max_size_mb", "user", "workdir", "env", "exposed", "layers_max")):
            info = self.inspect(tag)
            config = info.get("Config") or {}
            if "max_size_mb" in expect:
                size = round(int(info.get("Size", 0)) / 1_000_000)
                if size > float(expect["max_size_mb"]):
                    return _fail("too_big", size=size, max=expect["max_size_mb"])
            if "user" in expect and str(config.get("User", "")) != str(expect["user"]):
                return _fail("user_wrong", expected=expect["user"], actual=config.get("User") or "root")
            if "workdir" in expect and str(config.get("WorkingDir", "")) != str(expect["workdir"]):
                return _fail("workdir_wrong", expected=expect["workdir"], actual=config.get("WorkingDir") or "/")
            if "env" in expect:
                env = dict(item.partition("=")[::2] for item in config.get("Env") or [])
                for key, value in expect["env"].items():
                    if key not in env:
                        return _fail("env_missing", name=key)
                    if value is not None and env[key] != str(value):
                        return _fail("env_wrong", name=key, expected=str(value), actual=env[key])
            if "exposed" in expect:
                exposed = config.get("ExposedPorts") or {}
                for port in expect["exposed"]:
                    if f"{port}/tcp" not in exposed:
                        return _fail("not_exposed", port=port)
            if "layers_max" in expect:
                layers = len((info.get("RootFS") or {}).get("Layers") or [])
                if layers > int(expect["layers_max"]):
                    return _fail("too_many_layers", count=layers, max=expect["layers_max"])

        for path in expect.get("file_exists", []):
            if not self.test_path(tag, path):
                return _fail("file_missing", path=path)
        for path in expect.get("file_missing", []):
            if self.test_path(tag, path):
                return _fail("file_present", path=path)

        if "http" in expect:
            return self.http(tag, run, expect)
        if any(key in expect for key in ("logs", "logs_contains", "exit_code")):
            return self.foreground(tag, run, expect)
        return _ok()

    def test_path(self, tag: str, path: str) -> bool:
        name = self.name()
        done = self.docker.call(["run", "--rm", "--name", name, *self.labels(), "--entrypoint", "test",
                                 tag, "-e", path], timeout=30)
        return done.returncode == 0

    def foreground(self, tag: str, run: dict, expect: dict) -> dict:
        name = self.name()
        cmd = [str(item) for item in run.get("cmd") or []]
        shown = " ".join(["docker run --rm", *self._shown_env(run), "app", *cmd])
        self.transcript.append(f"❯ {shown}")
        try:
            done = self.docker.call(["run", "--rm", "--name", name, *self.labels(), *self.run_args(run), tag, *cmd],
                                    timeout=float(run.get("timeout", 30)))
        except subprocess.TimeoutExpired:
            return _fail("run_timeout", seconds=run.get("timeout", 30))
        output = (done.stdout or "") + (done.stderr or "")
        if output.strip():
            self.transcript.extend("  " + line for line in output.rstrip().splitlines()[:200])
        if done.returncode in (125, 126, 127) and "exit_code" not in expect:
            return _fail("run_failed", code=done.returncode, error=(done.stderr or "").strip()[-300:])
        if "exit_code" in expect and done.returncode != int(expect["exit_code"]):
            return _fail("exit_code", expected=expect["exit_code"], actual=done.returncode)
        if "logs" in expect and _lines(done.stdout) != _lines(str(expect["logs"])):
            return _fail("logs", expected=str(expect["logs"]).strip(), actual=(done.stdout or "").strip())
        for text in expect.get("logs_contains", []):
            if text not in output:
                return _fail("logs_missing", text=text, actual=output.strip()[-400:])
        return _ok()

    def _shown_env(self, run: dict) -> list[str]:
        shown = [f"-e {key}={value}" for key, value in (run.get("env") or {}).items()]
        return shown + [f"-v {spec}" for spec in run.get("volumes") or []]

    def http(self, tag: str, run: dict, expect: dict) -> dict:
        port = int(run.get("port") or expect["http"].get("port") or 80)
        name = self.name()
        cmd = [str(item) for item in run.get("cmd") or []]
        self.transcript.append("❯ " + " ".join(["docker run -d", f"-p 8080:{port}", *self._shown_env(run), "app", *cmd]))
        done = self.docker.call(["run", "-d", "--name", name, *self.labels(), "-p", f"127.0.0.1::{port}",
                                 *self.run_args(run), tag, *cmd], timeout=60)
        if done.returncode != 0:
            return _fail("run_failed", code=done.returncode, error=(done.stderr or "").strip()[-300:])
        mapped = self.docker.call(["port", name, f"{port}/tcp"], timeout=15).stdout.strip().splitlines()
        address = next((line for line in mapped if line.startswith("127.0.0.1:")), "")
        if not address:
            return _fail("no_port", port=port)
        checks = expect["http"] if isinstance(expect["http"], list) else [expect["http"]]
        wait_until = time.monotonic() + min(float(run.get("wait", HTTP_WAIT_SEC)), self.docker.remaining())
        result = None
        for spec in checks:
            path = str(spec.get("path", "/"))
            url = f"http://{address}{path}"
            last_error = ""
            while True:
                try:
                    status, body = _http_get(url, timeout=5)
                    self.transcript.append(f"❯ curl localhost:8080{path}")
                    self.transcript.append(f"  {status} {_one_line(body)}")
                    result = _compare_http(dict(spec, path=path), status, body)
                    break
                except (OSError, urllib.error.URLError) as exc:
                    last_error = str(exc)
                    if time.monotonic() > wait_until or not self._running(name):
                        logs = self._logs(name)
                        if logs:
                            self.transcript.extend("  " + line for line in logs.splitlines()[-20:])
                        return _fail("http_unreachable", path=path, port=port,
                                     exited=not self._running(name), error=last_error[:200])
                    time.sleep(0.5)
            if result is not None:
                return result
        return _ok()

    def _running(self, name: str) -> bool:
        done = self.docker.call(["inspect", "-f", "{{.State.Running}}", name], timeout=15)
        return done.stdout.strip() == "true"

    def _logs(self, name: str) -> str:
        done = self.docker.call(["logs", name], timeout=15)
        return ((done.stdout or "") + (done.stderr or "")).strip()

    # --- compose

    def compose_up(self, check: dict) -> dict:
        file = str(check.get("file") or "compose.yaml")
        path = self.workspace / file
        if not path.is_file():
            return _fail("no_file", file=file)
        data, error = _load_yaml(path)
        if error:
            return error
        if not isinstance(data, dict) or not isinstance(data.get("services"), dict):
            return _fail("no_services", file=file)
        unsafe = compose_guard(data)
        if unsafe:
            return unsafe
        context = _build_context(self.workspace)
        project = f"odyssey-{self.run_id}"
        self.projects.append((project, str(context / file)))
        base = ["compose", "-p", project, "-f", file]
        self.transcript.append("❯ docker compose up -d --build")
        # Bilgisayarda dolu olan port yalnızca çalıştırma kopyasında boş bir
        # porta taşınıyor; kontroller servise ağın içinden ulaştığı için
        # sonucu değiştirmiyor, kişinin dosyası olduğu gibi kalıyor.
        moved = _move_busy_ports(data)
        if moved:
            _dump_yaml(context / file, data)
            for service, old, new in moved:
                self.transcript.append(f"  ⚠ {service}: {old} in use → {new}")
        try:
            done = self.docker.call([*base, "up", "-d", "--build", "--quiet-pull"], cwd=context,
                                    timeout=max(30.0, self.docker.remaining() - CLEANUP_RESERVE_SEC))
        except subprocess.TimeoutExpired:
            return _fail("build_timeout")
        output = ((done.stdout or "") + (done.stderr or "")).strip()
        if done.returncode != 0:
            self.transcript.extend("  " + line for line in output.splitlines()[-BUILD_TAIL_LINES:])
            return _fail("compose_failed", log=_build_error(output))

        wait_until = time.monotonic() + min(float(check.get("wait", 40)), self.docker.remaining() - CLEANUP_RESERVE_SEC)
        running = [str(name) for name in check.get("running", [])]
        # `healthy`: servisin sağlık denetimi olmalı ve geçmeli (yalnızca
        # çalışıyor olması yetmiyor).
        healthy = [str(name) for name in check.get("healthy", [])]
        while True:
            states = self._compose_states(base, context)
            missing = [name for name in running if states.get(name) != "running"]
            healthy_wait = [name for name in running if states.get(name + ":health") == "starting"]
            for name in healthy:
                health = states.get(name + ":health", "")
                if not health and states.get(name) == "running":
                    return _fail("no_healthcheck", service=name)
                if health == "unhealthy":
                    return _fail("unhealthy", service=name)
                if health != "healthy" and name not in healthy_wait:
                    healthy_wait.append(name)
            if not missing and not healthy_wait:
                break
            if time.monotonic() > wait_until:
                name = missing[0] if missing else healthy_wait[0]
                logs = self.docker.call([*base, "logs", "--no-color", "--tail", "20", name], cwd=context, timeout=20)
                self.transcript.extend("  " + line for line in (logs.stdout or "").splitlines()[-20:])
                return _fail("service_down", service=name, state=states.get(name, "—"))
            time.sleep(1)
        for name in running:
            self.transcript.append(f"  ✔ {name}  running" + ("  (healthy)" if name in healthy else ""))

        for spec in check.get("http", []) if isinstance(check.get("http"), list) else (
                [check["http"]] if check.get("http") else []):
            result = self._probe(base, context, project, spec, wait_until)
            if result is not None:
                return result

        # Servis yazacağını hemen yazmayabilir (bağımlı olduğu servisi
        # birkaç kez deniyor olabilir); süre içinde yazana kadar bekleniyor.
        for service, text in (check.get("logs_contains") or {}).items():
            while True:
                logs = self.docker.call([*base, "logs", "--no-color", service], cwd=context, timeout=20)
                output = (logs.stdout or "") + (logs.stderr or "")
                if text in output:
                    break
                if time.monotonic() > wait_until:
                    self.transcript.extend("  " + line for line in output.strip().splitlines()[-12:])
                    return _fail("logs_missing", text=text, actual=output.strip()[-400:])
                time.sleep(1)
            self.transcript.append(f"  {service}: {text}")
        return _ok()

    def _compose_states(self, base: list[str], context: Path) -> dict[str, str]:
        done = self.docker.call([*base, "ps", "-a", "--format", "json"], cwd=context, timeout=20)
        states: dict[str, str] = {}
        text = (done.stdout or "").strip()
        items = []
        if text.startswith("["):
            try:
                items = json.loads(text)
            except ValueError:
                items = []
        else:
            for line in text.splitlines():
                try:
                    items.append(json.loads(line))
                except ValueError:
                    continue
        for item in items:
            service = str(item.get("Service", ""))
            states[service] = str(item.get("State", ""))
            if item.get("Health"):
                states[service + ":health"] = str(item["Health"])
        return states

    def _probe(self, base: list[str], context: Path, project: str, spec: dict, wait_until: float) -> dict | None:
        """Servise compose ağının içinden istek atar (ana makinenin portu gerekmiyor)."""
        service = str(spec.get("service", "web"))
        port = int(spec.get("port", 80))
        path = str(spec.get("path", "/"))
        ids = self.docker.call([*base, "ps", "-q", service], cwd=context, timeout=20).stdout.split()
        if not ids:
            return _fail("service_down", service=service, state="—")
        nets = self.docker.call(["inspect", "-f", "{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}",
                                 ids[0]], timeout=15).stdout.split()
        if not nets:
            return _fail("http_unreachable", path=path, port=port, exited=False, error="no network")
        url = f"http://{service}:{port}{path}"
        self.transcript.append(f"❯ curl {service}:{port}{path}")
        while True:
            name = self.name()
            done = self.docker.call(["run", "--rm", "--name", name, *self.labels(), "--network", nets[0],
                                     "alpine:3.22", "wget", "-q", "-S", "-O", "-", "-T", "5", url], timeout=30)
            match = re.search(r"HTTP/[\d.]+ (\d{3})", done.stderr or "")
            if match:
                status = int(match.group(1))
                body = done.stdout or ""
                self.transcript.append(f"  {status} {_one_line(body)}")
                return _compare_http(dict(spec, path=path), status, body)
            if time.monotonic() > wait_until:
                return _fail("http_unreachable", path=path, port=port, exited=False,
                             error=(done.stderr or "").strip()[-200:])
            time.sleep(1)

    # --- temizlik

    def cleanup(self) -> None:
        for project, file in self.projects:
            try:
                self.docker.call(["compose", "-p", project, "-f", file, "down", "-v", "--remove-orphans",
                                  "--rmi", "local"], timeout=60, cwd=Path(file).parent,
                                 cleanup=True)
            except (subprocess.TimeoutExpired, OSError):
                pass
        try:
            ids = self.docker.call(["ps", "-aq", "--filter", f"label=odyssey.run={self.run_id}"], timeout=20,
                                   cleanup=True).stdout.split()
            if ids:
                self.docker.call(["rm", "-f", "-v", *ids], timeout=30, cleanup=True)
            if self.volumes:
                self.docker.call(["volume", "rm", "-f", *self.volumes.values()], timeout=30, cleanup=True)
        except (subprocess.TimeoutExpired, OSError):
            pass


def _build_error(log: str) -> str:
    """Derleme günlüğünden kişiye gösterilecek hata satırı."""
    for line in reversed(log.splitlines()):
        text = line.strip()
        if text.startswith(("ERROR", "#")) and "ERROR" in text:
            return re.sub(r"^#\d+\s*", "", text)[:300]
    lines = [line.strip() for line in log.splitlines() if line.strip()]
    return lines[-1][:300] if lines else ""


# --- giriş ---------------------------------------------------------------

STATIC = {"dockerfile": check_dockerfile, "compose": check_compose, "command": check_command}


def run(job: dict) -> dict:
    # Giriş dosyası alt klasörde olabilir (`web/client.py`); klasörü çalıştırıcı veriyor.
    workspace = Path(job.get("workspace") or Path(job["code_path"]).parent).resolve()
    checks = job.get("checks", [])
    run_id = str(job.get("run_id") or workspace.name)[:16]
    key = str(job.get("exercise_key") or run_id)
    budget = float(job.get("timeout_sec") or 120)
    deadline = time.monotonic() + max(10.0, budget - CLEANUP_RESERVE_SEC)

    results: list[dict] = [None] * len(checks)  # type: ignore[list-item]
    transcript: list[str] = []
    static_failed = False
    for index, check in enumerate(checks):
        kind = check.get("type", "")
        if kind in STATIC:
            outcome = STATIC[kind](check, workspace)
            static_failed = static_failed or not outcome["passed"]
            results[index] = outcome

    state, version = "", ""
    real = [index for index, check in enumerate(checks) if check.get("type") in REAL_TYPES]
    if real:
        if static_failed:
            for index in real:
                results[index] = _fail("skipped")
        else:
            exe = docker_path()
            state, version = docker_state(exe)
            if state != "ok":
                for index in real:
                    results[index] = _fail("docker_" + state)
            else:
                runner = RealChecks(Docker(exe, deadline), workspace, run_id, key, transcript)
                try:
                    for index in real:
                        check = checks[index]
                        try:
                            if check["type"] == "container":
                                results[index] = runner.container(check)
                            else:
                                results[index] = runner.compose_up(check)
                        except subprocess.TimeoutExpired:
                            results[index] = _fail("timeout")
                finally:
                    runner.cleanup()

    out_checks = []
    for check, outcome in zip(checks, results):
        if outcome is None:
            outcome = _fail("bad_type", type=check.get("type", ""))
        out_checks.append({
            "type": check.get("type", ""),
            "passed": outcome["passed"],
            "detail": {"reason": outcome["reason"], "values": outcome["values"]},
            "hint": check.get("hint", {}),
        })

    stdout, truncated = clip("\n".join(transcript))
    return {
        "status": "ok",
        "stdout": stdout,
        "stderr": "",
        "truncated": truncated,
        "error": None,
        "checks": out_checks,
        "docker": {"state": state, "version": version},
    }
