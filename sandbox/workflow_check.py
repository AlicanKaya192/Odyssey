"""İş akışı (GitHub Actions YAML) dosyasının durağan denetimi.

Program çevrimdışı; iş akışı gerçekten çalıştırılmıyor. Dosya PyYAML ile
okunup yapısına bakılıyor: önce GitHub'ın dosyayı reddedeceği hatalar
(iş yok, `runs-on` yok, sürümsüz `uses`, olmayan işe `needs`...), sonra
alıştırmanın istediği şartlar (tetikleyici, iş, adım sırası, matris,
izinler, gizli değer).

Sonuç `docker_runner` biçiminde: `{"passed", "reason", "values"}`; grader
metni `check.workflow.<reason>`'dan, yoksa `check.docker.<reason>`'dan alıyor
(`no_file`, `yaml_error` ortak).
"""

from __future__ import annotations

import re
from pathlib import Path

from docker_runner import _fail, _load_yaml, _ok

DEFAULT_FILE = ".github/workflows/ci.yml"
SECRET_REF = r"\$\{\{\s*secrets\.%s\s*\}\}"


def run(job: dict) -> dict:
    """`workflow` dilindeki alıştırma: çalışan kod yok, yalnızca kontroller."""
    workspace = Path(job.get("workspace") or Path(job["code_path"]).parent).resolve()
    out_checks = []
    for check in job.get("checks", []):
        kind = check.get("type", "")
        outcome = check_workflow(check, workspace) if kind == "workflow" else _fail("bad_type", type=kind)
        out_checks.append({
            "type": kind,
            "passed": outcome["passed"],
            "detail": {"reason": outcome["reason"], "values": outcome["values"]},
            "hint": check.get("hint", {}),
        })
    return {"status": "ok", "stdout": "", "stderr": "", "truncated": False, "error": None, "checks": out_checks}


def check_workflow(check: dict, workspace: Path) -> dict:
    name = str(check.get("file") or DEFAULT_FILE)
    path = workspace / name
    if not path.is_file():
        return _fail("no_file", file=name)
    data, error = _load_yaml(path)
    if error:
        return error

    problem = _structure_problem(data)
    if problem:
        return problem

    for test in (_check_triggers, _check_job, _check_keys, _check_permissions, _check_text):
        problem = test(check, data, path)
        if problem:
            return problem
    return _ok()


# --- GitHub'ın reddedeceği yapı hataları -----------------------------------


def _structure_problem(data) -> dict | None:
    if not isinstance(data, dict) or not isinstance(data.get("jobs"), dict) or not data["jobs"]:
        return _fail("no_jobs")
    if not _triggers(data):
        return _fail("no_trigger")
    jobs = data["jobs"]
    for job_id, job in jobs.items():
        if not isinstance(job, dict) or not job.get("runs-on"):
            return _fail("no_runs_on", job=job_id)
        for wanted in _as_list(job.get("needs")):
            if wanted not in jobs:
                return _fail("needs_unknown", job=job_id, name=wanted)
        steps = job.get("steps")
        if not isinstance(steps, list) or not steps:
            return _fail("no_steps", job=job_id)
        for number, step in enumerate(steps, start=1):
            problem = _step_problem(job_id, number, step)
            if problem:
                return problem
    stuck = _needs_cycle(jobs)
    if stuck:
        return _fail("needs_cycle", jobs=", ".join(stuck))
    return None


def _needs_cycle(jobs: dict) -> list[str]:
    """Başlayamayan işler: `needs` okları bir döngü kuruyorsa hiçbiri başlayamaz."""
    done: set[str] = set()
    waiting = {job_id: set(_as_list(job.get("needs"))) for job_id, job in jobs.items()}
    while True:
        ready = [job_id for job_id, needs in waiting.items() if job_id not in done and needs <= done]
        if not ready:
            return [job_id for job_id in waiting if job_id not in done]
        done.update(ready)


def _step_problem(job_id: str, number: int, step) -> dict | None:
    if not isinstance(step, dict):
        return _fail("step_empty", job=job_id, number=number)
    has_uses, has_run = bool(step.get("uses")), bool(step.get("run"))
    if has_uses and has_run:
        return _fail("step_both", job=job_id, number=number)
    if not has_uses and not has_run:
        return _fail("step_empty", job=job_id, number=number)
    if has_uses and "@" not in str(step["uses"]) and not str(step["uses"]).startswith(("./", "docker://")):
        return _fail("uses_no_ref", job=job_id, action=str(step["uses"]))
    return None


# --- Alıştırmanın şartları ----------------------------------------------------


def _check_triggers(check: dict, data: dict, _path: Path) -> dict | None:
    triggers = _triggers(data)
    for wanted in check.get("on", []):
        if wanted not in triggers:
            return _fail("trigger_missing", name=wanted)
    for event, branches in (check.get("branches") or {}).items():
        config = triggers.get(event)
        found = _as_list(config.get("branches")) if isinstance(config, dict) else []
        for branch in branches:
            if branch not in found:
                return _fail("branch_missing", event=event, branch=branch)
    for event, filters in (check.get("filters") or {}).items():
        config = triggers.get(event)
        for key, values in filters.items():
            found = _as_list(config.get(key)) if isinstance(config, dict) else []
            for value in values:
                if value not in found:
                    return _fail("filter_missing", event=event, key=key, value=value)
    if "cron" in check:
        crons = [str(item.get("cron", "")) for item in _as_list(triggers.get("schedule"))
                 if isinstance(item, dict)]
        if not any(re.search(check["cron"], cron) for cron in crons):
            return _fail("cron_missing", expected=check.get("show_cron", check["cron"]))
    return None


def _check_job(check: dict, data: dict, _path: Path) -> dict | None:
    job_id = check.get("job")
    if not job_id:
        return None
    job = data["jobs"].get(job_id)
    if job is None:
        return _fail("no_job", job=job_id)

    if "runs_on" in check:
        runs_on = " ".join(str(item) for item in _as_list(job.get("runs-on")))
        if not re.search(check["runs_on"], runs_on):
            return _fail("runs_on_wrong", job=job_id, expected=check.get("show_runs_on", check["runs_on"]),
                         actual=runs_on)
    needs = _as_list(job.get("needs"))
    for wanted in check.get("needs", []):
        if wanted not in needs:
            return _fail("needs_missing", job=job_id, name=wanted)
    if "if" in check and not re.search(check["if"], str(job.get("if", "") or "")):
        return _fail("if_missing", job=job_id, expected=check.get("show_if", check["if"]))
    env = job.get("env") if isinstance(job.get("env"), dict) else {}
    for key, pattern in (check.get("env") or {}).items():
        if key not in env or not re.search(pattern, str(env[key])):
            return _fail("env_missing", job=job_id, name=key)
    problem = _check_matrix(check, job_id, job)
    if problem:
        return problem
    return _check_steps(check, job_id, job["steps"])


def _check_matrix(check: dict, job_id: str, job: dict) -> dict | None:
    strategy = job.get("strategy")
    matrix = strategy.get("matrix") if isinstance(strategy, dict) else None
    matrix = matrix if isinstance(matrix, dict) else {}
    for key, values in (check.get("matrix") or {}).items():
        found = {str(item) for item in _as_list(matrix.get(key))}
        for value in values:
            if str(value) not in found:
                return _fail("matrix_missing", job=job_id, key=key, value=str(value))
    for part in ("include", "exclude"):
        given = [_as_text(item) for item in _as_list(matrix.get(part)) if isinstance(item, dict)]
        for wanted in check.get("matrix_" + part, []):
            want = _as_text(wanted)
            if not any(all(entry.get(key) == value for key, value in want.items()) for entry in given):
                shown = ", ".join(f"{key}: {value}" for key, value in want.items())
                return _fail("matrix_entry_missing", job=job_id, part=part, entry=shown)
    return None


def _check_steps(check: dict, job_id: str, steps: list) -> dict | None:
    """İstenen adımlar bu sırayla bulunmalı (aralarında başka adım olabilir)."""
    wanted = check.get("steps") or []
    position = 0
    for spec in wanted:
        found = next((index for index in range(position, len(steps)) if _step_matches(steps[index], spec)), None)
        if found is None:
            anywhere = any(_step_matches(step, spec) for step in steps[:position])
            reason = "step_order" if anywhere else "step_missing"
            return _fail(reason, job=job_id, step=_show_step(spec))
        position = found + 1
    return None


def _step_matches(step: dict, spec: dict) -> bool:
    for field in ("uses", "run", "name", "if"):
        if field in spec and not re.search(spec[field], str(step.get(field, "") or "")):
            return False
    for field in ("with", "env"):
        given = step.get(field) if isinstance(step.get(field), dict) else {}
        for key, pattern in (spec.get(field) or {}).items():
            if key not in given or not re.search(pattern, str(given[key])):
                return False
    return True


def _show_step(spec: dict) -> str:
    if spec.get("show"):
        return str(spec["show"])
    for field in ("uses", "run", "name"):
        if field in spec:
            return f"{field}: {spec[field].replace(chr(92), '')}"
    return ""


def _check_keys(check: dict, data: dict, _path: Path) -> dict | None:
    """`keys`: noktalı yol → değerin metninde aranan desen (`jobs.test.strategy.fail-fast`)."""
    shows = check.get("show_keys") or {}
    for path, pattern in (check.get("keys") or {}).items():
        value = _lookup(data, path)
        if value is _MISSING or not re.search(pattern, str(value)):
            return _fail("key_missing", path=path, expected=shows.get(path, pattern))
    return None


def _check_permissions(check: dict, data: dict, _path: Path) -> dict | None:
    wanted = check.get("permissions")
    if not wanted:
        return None
    job = data["jobs"].get(check.get("job") or "") or {}
    permissions = job.get("permissions") if "permissions" in job else data.get("permissions")
    permissions = permissions if isinstance(permissions, dict) else {}
    for scope, level in wanted.items():
        actual = str(permissions.get(scope, "") or "")
        if actual != str(level):
            return _fail("permission_wrong", scope=scope, expected=str(level), actual=actual or "-")
    return None


def _check_text(check: dict, _data: dict, path: Path) -> dict | None:
    """Gizli değer `${{ secrets.AD }}` ile kullanılmalı; açık yazılmış değer olmamalı."""
    text = path.read_text(encoding="utf-8", errors="replace")
    for secret in check.get("secrets", []):
        if not re.search(SECRET_REF % re.escape(secret), text):
            return _fail("secret_missing", name=secret)
    for rule in check.get("forbid", []):
        if re.search(rule["pattern"], text):
            return _fail("forbidden", text=rule.get("show", rule["pattern"]))
    return None


# --- Yardımcılar ------------------------------------------------------------------


def _triggers(data: dict) -> dict:
    """`on` her üç biçimde de olay adı → ayar sözlüğüne iner.

    YAML 1.1 `on` kelimesini `True` diye okuyor (PyYAML öyle); ikisine de bakılır.
    """
    raw = data.get("on", data.get(True))
    if isinstance(raw, str):
        return {raw: None}
    if isinstance(raw, list):
        return {str(item): None for item in raw}
    if isinstance(raw, dict):
        return {str(key): value for key, value in raw.items()}
    return {}


_MISSING = object()


def _lookup(data: dict, path: str):
    """Noktalı yolu ağaçta izler; `on` anahtarı YAML 1.1'de `True` okunduğu için ikisine de bakılır."""
    node = data
    for part in path.split("."):
        if not isinstance(node, dict):
            return _MISSING
        if part in node:
            node = node[part]
        elif part == "on" and True in node:
            node = node[True]
        else:
            return _MISSING
    return node


def _as_text(entry: dict) -> dict:
    """Matris girdisinin değerleri metin olarak (`3.14` ile `"3.14"`, `true` ile `True` aynı)."""
    return {str(key): str(value) for key, value in entry.items()}


def _as_list(value) -> list:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]
