"""Git benzeticisi: Git patikasının terminal alıştırmaları için.

Kişinin bilgisayarında git kurulu olmak zorunda değil. Burada küçük bir
dosya sistemi, depolar ve uzak depolar bellekte tutuluyor; komutlar
(`git status`, `git commit -m ...`, `echo "x" > a.txt`) yorumlanıp gerçek
git 2.55'in çıktılarına benzetilmiş metin üretiliyor (çıktılar bu makinede
gerçek git ile ölçüldü, `Plan/araclar/git_sim_testi.py` karşılaştırıyor).

Nesne kimlikleri gerçek git'inkiyle aynı biçimde hesaplanıyor (blob, tree,
commit SHA-1); aynı yazar ve tarihle gerçek git de aynı kimliği verir.

Kişinin kodu çalışmıyor; yalnızca komut satırı ayrıştırılıyor. Benzetici
uygulamanın kendi sürecinde, anında çalışıyor.
"""

from __future__ import annotations

import difflib
import fnmatch
import hashlib
import posixpath
import re
import shlex
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

HOME = "/home/ada"
TZ = timezone(timedelta(hours=3))
START = int(datetime(2026, 10, 7, 10, 0, 0, tzinfo=TZ).timestamp())
GIT_VERSION = "git version 2.55.0"
# "Bunu mu demek istedin?" önerisi için git'in komut listesi.
GIT_COMMANDS = ["add", "am", "archive", "bisect", "blame", "branch", "bundle", "checkout", "cherry-pick", "clean",
                "clone", "commit", "config", "describe", "diff", "fetch", "format-patch", "gc", "grep", "init", "log",
                "maintenance", "merge", "mv", "notes", "pull", "push", "range-diff", "rebase", "reflog", "remote",
                "reset", "restore", "revert", "rm", "shortlog", "show", "sparse-checkout", "stash", "status",
                "submodule", "switch", "tag", "worktree"]
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

# Benzeticiye özgü (gerçek git'te olmayan) mesajlar: kişinin dilinde.
SIM_TEXT = {
    "tr": {
        "no_editor": "odyssey: Bu terminalde metin düzenleyici açılmıyor. Mesajı -m ile yaz: git commit -m \"mesaj\"",
        "no_editor_file": "odyssey: Bu terminalde düzenleyici yok. Dosyayı echo ile yaz: echo \"metin\" > {name}",
        "unsupported": "odyssey: '{what}' bu benzeticide yok.",
        "interactive": "odyssey: Etkileşimli komutlar (-i, -p) bu terminalde çalışmıyor.",
        "no_pipe": "odyssey: '{op}' bu terminalde yok; komutları tek tek ya da && ile yaz.",
        "no_editor_config": "odyssey: Bu terminalde düzenleyici açılmıyor. Ayarı komutla yaz: git config --global user.name \"Adın\"",
    },
    "en": {
        "no_editor": "odyssey: No text editor opens in this terminal. Write the message with -m: git commit -m \"message\"",
        "no_editor_file": "odyssey: There is no editor in this terminal. Write the file with echo: echo \"text\" > {name}",
        "unsupported": "odyssey: '{what}' is not available in this simulator.",
        "interactive": "odyssey: Interactive commands (-i, -p) do not work in this terminal.",
        "no_pipe": "odyssey: '{op}' is not available in this terminal; write the commands one by one or with &&.",
        "no_editor_config": "odyssey: No editor opens in this terminal. Set the value with a command: git config --global user.name \"Your Name\"",
    },
}


class GitError(Exception):
    """Komutun hatası: metin çıktıya, çıkış kodu 1 (ya da verilen)."""

    def __init__(self, text: str, code: int = 128) -> None:
        super().__init__(text)
        self.text = text
        self.code = code


@dataclass
class Commit:
    tree: str
    parents: list[str]
    author: str
    email: str
    time: int
    message: str


@dataclass
class Repo:
    root: str
    bare: bool = False
    blobs: dict = field(default_factory=dict)       # sha → metin
    trees: dict = field(default_factory=dict)       # sha → {ad: (mod, sha)}
    commits: dict = field(default_factory=dict)     # sha → Commit
    tag_objects: dict = field(default_factory=dict)  # sha → (hedef, ad, mesaj, kişi, zaman)
    refs: dict = field(default_factory=dict)        # "refs/heads/main" → sha
    head: str = "refs/heads/main"                   # dal ref'i ya da kopuk sha
    index: dict = field(default_factory=dict)       # yol → blob sha
    conflicts: dict = field(default_factory=dict)   # yol → (taban, bizim, onların)
    state: dict | None = None                       # merge / rebase / cherry-pick
    config: dict = field(default_factory=dict)
    remotes: dict = field(default_factory=dict)     # ad → url
    upstream: dict = field(default_factory=dict)    # dal → (uzak, dal)
    stash: list = field(default_factory=list)
    reflog: list = field(default_factory=list)      # (sha, mesaj), en yeni başta

    # --- HEAD ------------------------------------------------------------

    @property
    def detached(self) -> bool:
        return not self.head.startswith("refs/")

    @property
    def branch(self) -> str:
        return "" if self.detached else self.head[len("refs/heads/"):]

    def head_sha(self) -> str | None:
        return self.head if self.detached else self.refs.get(self.head)

    def set_head_sha(self, sha: str) -> None:
        if self.detached:
            self.head = sha
        else:
            self.refs[self.head] = sha

    def branches(self) -> list[str]:
        return sorted(r[len("refs/heads/"):] for r in self.refs if r.startswith("refs/heads/"))


# --- nesne biçimi (gerçek git'le aynı) ---------------------------------------


def _sha(kind: str, data: bytes) -> str:
    return hashlib.sha1(f"{kind} {len(data)}\0".encode() + data).hexdigest()


def blob_sha(text: str) -> str:
    return _sha("blob", text.encode("utf-8"))


def _tree_bytes(entries: dict) -> bytes:
    def key(name):
        mode, _ = entries[name]
        return name + "/" if mode == "40000" else name

    out = b""
    for name in sorted(entries, key=key):
        mode, sha = entries[name]
        out += f"{mode} {name}\0".encode() + bytes.fromhex(sha)
    return out


def _person(name: str, email: str, when: int) -> str:
    return f"{name} <{email}> {when} +0300"


def commit_bytes(c: Commit) -> bytes:
    lines = [f"tree {c.tree}"] + [f"parent {p}" for p in c.parents]
    kisi = _person(c.author, c.email, c.time)
    lines += [f"author {kisi}", f"committer {kisi}", "", c.message]
    return ("\n".join(lines) + "\n").encode("utf-8")


def git_date(when: int) -> str:
    dt = datetime.fromtimestamp(when, TZ)
    return f"{dt:%a %b} {dt.day} {dt:%H:%M:%S %Y} +0300"


def short(sha: str) -> str:
    return sha[:7]


# --- satır çıktısı ---------------------------------------------------------
# Her satır (metin, renk); renk Git Bash'teki gibi: yeşil hazırlanmış,
# kırmızı hazırlanmamış, sarı commit kimliği, mavi dal adları.


class Out:
    def __init__(self) -> None:
        self.lines: list[tuple[str, str]] = []

    def __call__(self, text: str = "", color: str = "") -> None:
        for line in str(text).split("\n"):
            self.lines.append((line, color))

    def extend(self, other: "Out") -> None:
        self.lines.extend(other.lines)

    def text(self) -> str:
        return "\n".join(t for t, _ in self.lines)


def _lines(text: str) -> list[str]:
    return text.splitlines(keepends=True)


def count_changes(old: str, new: str) -> tuple[int, int]:
    """(eklenen, silinen) satır sayısı."""
    ins = dels = 0
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, _lines(old), _lines(new)).get_opcodes():
        if tag in ("replace", "delete"):
            dels += i2 - i1
        if tag in ("replace", "insert"):
            ins += j2 - j1
    return ins, dels


def unified(old: str, new: str, a: str, b: str) -> list[str]:
    """`git diff` gövdesi (başlık satırları hariç `@@` ve satırlar)."""
    out = []
    for line in difflib.unified_diff(_lines(old), _lines(new), a, b, n=3):
        if line.startswith(("---", "+++")):
            continue
        text = line.rstrip("\n")
        out.append(text)
        if not line.endswith("\n"):
            out.append("\\ No newline at end of file")
    return out


def merge_text(base: str, ours: str, theirs: str, their_name: str) -> tuple[str, bool]:
    """Üç yollu satır birleştirme; çakışan parçalar git'in işaretleriyle."""
    b = _lines(base)

    def regions(other):
        sm = difflib.SequenceMatcher(None, b, _lines(other))
        return [(i1, i2, _lines(other)[j1:j2]) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]

    ro, rt = regions(ours), regions(theirs)
    events = sorted([(s, e, r, "o") for s, e, r in ro] + [(s, e, r, "t") for s, e, r in rt],
                    key=lambda x: (x[0], x[1]))
    out: list[str] = []
    pos = 0
    conflict = False
    i = 0
    while i < len(events):
        start, end, _, _ = events[i]
        group = [events[i]]
        j = i + 1
        # Git bitişik satırlardaki değişiklikleri de çakışma sayıyor.
        while j < len(events) and events[j][0] <= end:
            group.append(events[j])
            end = max(end, events[j][1])
            j += 1
        out.extend(b[pos:start])
        sides = {k for *_, k in group}

        def apply(side):
            res, p = [], start
            for s, e, r, k in group:
                if k != side:
                    continue
                res.extend(b[p:s])
                res.extend(r)
                p = e
            res.extend(b[p:end])
            return res

        if sides == {"o"}:
            out.extend(apply("o"))
        elif sides == {"t"}:
            out.extend(apply("t"))
        else:
            o, t = apply("o"), apply("t")
            if o == t:
                out.extend(o)
            else:
                conflict = True
                fix = lambda lines: [ln if ln.endswith("\n") else ln + "\n" for ln in lines]  # noqa: E731
                out.append("<<<<<<< HEAD\n")
                out.extend(fix(o))
                out.append("=======\n")
                out.extend(fix(t))
                out.append(f">>>>>>> {their_name}\n")
        pos = end
        i = j
    out.extend(b[pos:])
    return "".join(out), conflict


# --- dünya: dosya sistemi + depolar ------------------------------------------


class World:
    """Bir alıştırmanın bütün durumu: dosyalar, depolar, uzak depolar, saat."""

    def __init__(self, lang: str = "tr", *, configured: bool = True, fixed_time: bool = False) -> None:
        self.lang = lang if lang in SIM_TEXT else "en"
        self.files: dict[str, str] = {}
        self.dirs: set[str] = {"/", "/home", HOME}
        self.cwd = HOME
        self.repos: dict[str, Repo] = {}
        self.remote_repos: dict[str, Repo] = {}
        # Ayarlanmış kullanıcının ~/.gitconfig'i (bölüm 01'de anlatılan üç satır).
        # Ayarsız dünyada da yeni depo `main` ile açılıyor (sistem düzeyi; listelenmiyor).
        self.global_config: dict[str, str] = {}
        if configured:
            self.global_config.update({"user.name": "Ada Lovelace", "user.email": "ada@example.com",
                                       "init.defaultbranch": "main"})
        self.system_config: dict[str, str] = {"init.defaultbranch": "main"}
        self._time = START
        self._fixed_time = fixed_time
        self.history: list[str] = []

    # --- yardımcılar ---------------------------------------------------------

    def t(self, key: str, **kw) -> str:
        return SIM_TEXT[self.lang][key].format(**kw)

    def tick(self) -> int:
        when = self._time
        if not self._fixed_time:
            self._time += 60
        return when

    def abspath(self, path: str) -> str:
        if path.startswith("~"):
            path = HOME + path[1:]
        if not path.startswith("/"):
            path = posixpath.join(self.cwd, path)
        norm = posixpath.normpath(path)
        return "/" if norm in ("", ".") else norm

    def display(self, path: str) -> str:
        return "~" + path[len(HOME):] if path == HOME or path.startswith(HOME + "/") else path

    def repo_at(self, path: str | None = None) -> Repo | None:
        p = self.abspath(path or self.cwd)
        while True:
            if p in self.repos:
                return self.repos[p]
            if p == "/":
                return None
            p = posixpath.dirname(p)

    def need_repo(self) -> Repo:
        repo = self.repo_at()
        if repo is None:
            raise GitError("fatal: not a git repository (or any of the parent directories): .git")
        return repo

    def config_get(self, repo: Repo | None, key: str) -> str | None:
        key = key.lower()
        if repo is not None and key in repo.config:
            return repo.config[key]
        return self.global_config.get(key, self.system_config.get(key))

    def prompt(self) -> str:
        repo = self.repo_at()
        yer = self.display(self.cwd)
        if repo is None:
            return f"{yer} $"
        if repo.state and repo.state.get("kind") == "merge":
            tail = f"{repo.branch}|MERGING"
        elif repo.state and repo.state.get("kind") == "rebase":
            tail = f"{repo.state['branch']}|REBASE"
        elif repo.state and repo.state.get("kind") == "cherry-pick":
            tail = f"{repo.branch}|CHERRY-PICKING"
        elif repo.detached:
            tail = short(repo.head) + "..."
        else:
            tail = repo.branch
        return f"{yer} ({tail}) $"

    # --- çalışma ağacı ------------------------------------------------------

    def worktree(self, repo: Repo) -> dict[str, str]:
        """Deponun çalışma ağacındaki dosyalar: göreli yol → içerik (.git hariç)."""
        root = repo.root.rstrip("/") + "/"
        out = {}
        for path, text in self.files.items():
            if path.startswith(root):
                rel = path[len(root):]
                if rel.split("/")[0] == ".git":
                    continue
                if self._inner_repo(repo, path):
                    continue
                out[rel] = text
        return out

    def _inner_repo(self, repo: Repo, path: str) -> bool:
        for root in self.repos:
            if root != repo.root and root.startswith(repo.root.rstrip("/") + "/") and path.startswith(root + "/"):
                return True
        return False

    def write_file(self, path: str, text: str) -> None:
        self.files[path] = text
        d = posixpath.dirname(path)
        while d not in self.dirs:
            self.dirs.add(d)
            d = posixpath.dirname(d)

    def set_worktree_file(self, repo: Repo, rel: str, text: str | None) -> None:
        path = posixpath.join(repo.root, rel)
        if text is None:
            self.files.pop(path, None)
        else:
            self.write_file(path, text)

    # --- ağaçlar --------------------------------------------------------

    def write_tree(self, repo: Repo, flat: dict[str, str]) -> str:
        """Yol → blob sha sözlüğünden ağaç nesneleri kurar; kök ağacın sha'sı."""
        nested: dict = {}
        for path, sha in flat.items():
            parts = path.split("/")
            node = nested
            for part in parts[:-1]:
                node = node.setdefault(part + "/", {})
            node[parts[-1]] = sha

        def build(node) -> str:
            entries = {}
            for name, value in node.items():
                if name.endswith("/"):
                    entries[name[:-1]] = ("40000", build(value))
                else:
                    entries[name] = ("100644", value)
            sha = _sha("tree", _tree_bytes(entries))
            repo.trees[sha] = entries
            return sha

        return build(nested)

    def read_tree(self, repo: Repo, tree_sha: str, prefix: str = "") -> dict[str, str]:
        out = {}
        for name, (mode, sha) in repo.trees.get(tree_sha, {}).items():
            path = prefix + name
            if mode == "40000":
                out.update(self.read_tree(repo, sha, path + "/"))
            else:
                out[path] = sha
        return out

    def commit_files(self, repo: Repo, sha: str | None) -> dict[str, str]:
        """Commit'teki dosyalar: yol → blob sha (commit yoksa boş)."""
        if not sha:
            return {}
        return self.read_tree(repo, repo.commits[sha].tree)

    def add_blob(self, repo: Repo, text: str) -> str:
        sha = blob_sha(text)
        repo.blobs[sha] = text
        return sha

    def make_commit(self, repo: Repo, flat: dict[str, str], parents: list[str], message: str,
                    author: tuple[str, str] | None = None) -> str:
        tree = self.write_tree(repo, flat)
        name, email = author or (self.config_get(repo, "user.name"), self.config_get(repo, "user.email"))
        c = Commit(tree, parents, name, email, self.tick(), message.rstrip("\n"))
        sha = _sha("commit", commit_bytes(c))
        repo.commits[sha] = c
        return sha

    # --- yok sayma ----------------------------------------------------------

    def ignore_rule(self, repo: Repo, rel: str, is_dir: bool = False):
        """Son eşleşen .gitignore kuralı: (satır no, kural, yok sayılıyor mu) ya da None.

        Dosyanın kendisi ya da üst klasörlerinden biri kurala uyabilir; üst klasör
        yok sayılıyorsa içindeki dosya da yok sayılır (git'te olduğu gibi)."""
        rules = self.files.get(posixpath.join(repo.root, ".gitignore"))
        if not rules:
            return None
        parts = rel.split("/")
        # Önce üst klasörler: biri yok sayılıyorsa içerideki hiçbir kural onu geri alamaz.
        for k in range(1, len(parts)):
            hit = self._rule_for(rules, "/".join(parts[:k]), True)
            if hit and hit[2]:
                return hit
        return self._rule_for(rules, rel, is_dir)

    @staticmethod
    def _rule_for(rules: str, rel: str, is_dir: bool):
        parts = rel.split("/")
        found = None
        for lineno, raw in enumerate(rules.splitlines(), start=1):
            pat = raw.strip()
            if not pat or pat.startswith("#"):
                continue
            neg = pat.startswith("!")
            body = pat[1:] if neg else pat
            dir_only = body.endswith("/")
            body = body.rstrip("/")
            if dir_only and not is_dir:
                continue
            if body.startswith("**/"):
                tail = body[3:]
                hit = any(fnmatch.fnmatch("/".join(parts[i:]), tail) for i in range(len(parts)))
            elif body.startswith("/") or "/" in body:
                hit = fnmatch.fnmatch(rel, body.lstrip("/"))
            else:
                hit = fnmatch.fnmatch(parts[-1], body)
            if hit:
                found = (lineno, pat, not neg)
        return found

    def ignored(self, repo: Repo, rel: str, is_dir: bool = False) -> bool:
        rule = self.ignore_rule(repo, rel, is_dir)
        return bool(rule and rule[2])

    def ignored_display(self, repo: Repo) -> list[str]:
        """`git status --ignored` satırları: yok sayılan klasör tek satır (`build/`)."""
        work = self.worktree(repo)
        shown = set()
        for rel in sorted(work):
            if rel in repo.index or not self.ignored(repo, rel):
                continue
            parts = rel.split("/")
            top = rel
            for k in range(1, len(parts)):
                d = "/".join(parts[:k])
                if self.ignored(repo, d, True):
                    top = d + "/"
                    break
            shown.add(top)
        return sorted(shown)

    # --- durum ----------------------------------------------------------

    def changes(self, repo: Repo) -> dict:
        """staged / unstaged / untracked listeleri (git status'un verisi)."""
        head = self.commit_files(repo, repo.head_sha())
        work = self.worktree(repo)
        staged, unstaged, untracked = [], [], []
        for path in sorted(set(head) | set(repo.index)):
            if path in repo.conflicts:
                continue
            if path not in head:
                staged.append(("new file", path))
            elif path not in repo.index:
                staged.append(("deleted", path))
            elif head[path] != repo.index[path]:
                staged.append(("modified", path))
        # Yeniden adlandırma: silinen + yeni eklenen aynı içerik.
        deleted = {head[p]: p for kind, p in staged if kind == "deleted"}
        renamed = []
        for kind, p in staged:
            if kind == "new file" and repo.index[p] in deleted:
                renamed.append((deleted.pop(repo.index[p]), p))
        if renamed:
            gone = {a for a, _ in renamed} | {b for _, b in renamed}
            staged = [s for s in staged if s[1] not in gone] + [("renamed", f"{a} -> {b}") for a, b in renamed]
            staged.sort(key=lambda s: s[1])
        for path in sorted(repo.index):
            if path in repo.conflicts:
                continue
            if path not in work:
                unstaged.append(("deleted", path))
            elif blob_sha(work[path]) != repo.index[path]:
                unstaged.append(("modified", path))
        tracked = set(repo.index) | set(repo.conflicts)
        for path in sorted(work):
            if path not in tracked and not self.ignored(repo, path):
                untracked.append(path)
        return {"staged": staged, "unstaged": unstaged, "untracked": untracked,
                "conflicts": sorted(repo.conflicts)}

    def untracked_display(self, repo: Repo, paths: list[str]) -> list[str]:
        """İzlenmeyen klasörün tamamı izlenmiyorsa `klasor/` diye tek satır."""
        tracked = set(repo.index) | set(repo.conflicts)
        shown: list[str] = []
        for path in paths:
            parts = path.split("/")
            if len(parts) > 1:
                top = parts[0] + "/"
                if not any(t.startswith(top) for t in tracked):
                    if top not in shown:
                        shown.append(top)
                    continue
            shown.append(path)
        return shown

    # --- komut satırı -------------------------------------------------------

    def run(self, line: str) -> tuple[Out, int]:
        """Bir satırı çalıştırır: (çıktı, çıkış kodu). `&&` zinciri destekli."""
        out = Out()
        line = line.strip()
        if not line or line.startswith("#"):
            return out, 0
        self.history.append(line)
        try:
            # `>`, `>>` ve `&&` bash'teki gibi boşluksuz da ayrılıyor (`echo hi>a.txt`).
            lexer = shlex.shlex(line, posix=True, punctuation_chars=True)
            lexer.whitespace_split = True
            tokens = list(lexer)
        except ValueError:
            out("bash: syntax error: unexpected end of file (a quote is not closed)", "red")
            return out, 2
        for tok in tokens:
            if tok in ("|", "||", ";", "&", "<", ";;", "|&", "&>", "<<"):
                out(self.t("no_pipe", op=tok), "yellow")
                return out, 2
        parts, cur = [], []
        for tok in tokens:
            if tok == "&&":
                parts.append(cur)
                cur = []
            else:
                cur.append(tok)
        parts.append(cur)
        code = 0
        for argv in parts:
            if not argv:
                continue
            try:
                code = self._run_argv(argv, out)
            except GitError as exc:
                out(exc.text, "red" if exc.text.startswith(("fatal", "error")) else "")
                code = exc.code
            if code != 0:
                break
        return out, code

    def _run_argv(self, argv: list[str], out: Out) -> int:
        cmd, args = argv[0], argv[1:]
        if cmd == "git":
            return self.git(args, out)
        handler = getattr(self, "sh_" + cmd.replace("-", "_"), None)
        if handler is None:
            if cmd in ("nano", "vim", "vi", "code", "notepad", "emacs"):
                out(self.t("no_editor_file", name=args[0] if args else "file.txt"), "yellow")
                return 1
            out(f"bash: {cmd}: command not found", "red")
            return 127
        return handler(args, out)

    # --- kabuk ----------------------------------------------------------

    def sh_pwd(self, args, out):
        out(self.cwd)
        return 0

    def sh_clear(self, args, out):
        return 0

    def sh_cd(self, args, out):
        target = self.abspath(args[0]) if args else HOME
        if target not in self.dirs:
            out(f"bash: cd: {args[0]}: No such file or directory", "red")
            return 1
        self.cwd = target
        return 0

    def _children(self, d: str) -> list[str]:
        pref = d.rstrip("/") + "/"
        names = set()
        for p in list(self.files) + list(self.dirs):
            if p.startswith(pref) and p != d:
                names.add(p[len(pref):].split("/")[0])
        return sorted(names)

    def sh_ls(self, args, out):
        show_all = any(a.startswith("-") and "a" in a for a in args)
        targets = [a for a in args if not a.startswith("-")] or ["."]
        for t in targets:
            p = self.abspath(t)
            if p in self.files:
                out(t)
                continue
            if p not in self.dirs:
                out(f"ls: cannot access '{t}': No such file or directory", "red")
                return 2
            names = self._children(p)
            if p in self.repos and show_all:
                names = sorted(set(names) | {".git"})
            if not show_all:
                names = [n for n in names if not n.startswith(".")]
            else:
                names = [".", ".."] + names
            shown = [n + "/" if posixpath.join(p, n) in self.dirs or n == ".git" else n for n in names]
            if shown:
                out("  ".join(shown))
        return 0

    def sh_mkdir(self, args, out):
        for a in [x for x in args if not x.startswith("-")]:
            p = self.abspath(a)
            if p in self.dirs and "-p" not in args:
                out(f"mkdir: cannot create directory '{a}': File exists", "red")
                return 1
            d = p
            while d not in self.dirs:
                self.dirs.add(d)
                d = posixpath.dirname(d)
        return 0

    def sh_touch(self, args, out):
        for a in args:
            p = self.abspath(a)
            if posixpath.dirname(p) not in self.dirs:
                out(f"touch: cannot touch '{a}': No such file or directory", "red")
                return 1
            self.files.setdefault(p, "")
        return 0

    def sh_cat(self, args, out):
        for a in args:
            p = self.abspath(a)
            if p in self.dirs:
                out(f"cat: {a}: Is a directory", "red")
                return 1
            if p not in self.files:
                out(f"cat: {a}: No such file or directory", "red")
                return 1
            text = self.files[p]
            out(text[:-1] if text.endswith("\n") else text)
        return 0

    def _redirect(self, args):
        """`echo x > a.txt` / `>> a.txt`: (argümanlar, dosya, ekle mi)."""
        for i, tok in enumerate(args):
            if tok in (">", ">>") and i + 1 < len(args):
                return args[:i] + args[i + 2:], args[i + 1], tok == ">>"
            if tok.startswith(">>") and len(tok) > 2:
                return args[:i] + args[i + 1:], tok[2:], True
            if tok.startswith(">") and len(tok) > 1:
                return args[:i] + args[i + 1:], tok[1:], False
        return args, None, False

    def _emit(self, text: str, target, append: bool, out: Out) -> int:
        if target is None:
            out(text[:-1] if text.endswith("\n") else text)
            return 0
        p = self.abspath(target)
        if posixpath.dirname(p) not in self.dirs:
            out(f"bash: {target}: No such file or directory", "red")
            return 1
        if p in self.dirs:
            out(f"bash: {target}: Is a directory", "red")
            return 1
        self.write_file(p, (self.files.get(p, "") if append else "") + text)
        return 0

    def sh_echo(self, args, out):
        args, target, append = self._redirect(args)
        newline = True
        if args and args[0] == "-n":
            newline = False
            args = args[1:]
        return self._emit(" ".join(args) + ("\n" if newline else ""), target, append, out)

    def sh_printf(self, args, out):
        args, target, append = self._redirect(args)
        if not args:
            return 0
        text = args[0].replace("\\n", "\n").replace("\\t", "\t")
        if len(args) > 1:
            try:
                text = text.replace("%s", "{}").format(*args[1:])
            except (IndexError, ValueError):
                pass
        return self._emit(text, target, append, out)

    def sh_rm(self, args, out):
        recursive = any(a.startswith("-") and "r" in a for a in args)
        for a in [x for x in args if not x.startswith("-")]:
            p = self.abspath(a)
            if p in self.files:
                del self.files[p]
            elif p in self.dirs:
                if not recursive:
                    out(f"rm: cannot remove '{a}': Is a directory", "red")
                    return 1
                for f in [f for f in self.files if f.startswith(p + "/")]:
                    del self.files[f]
                for d in [d for d in self.dirs if d == p or d.startswith(p + "/")]:
                    self.dirs.discard(d)
                for r in [r for r in self.repos if r == p or r.startswith(p + "/")]:
                    del self.repos[r]
            else:
                out(f"rm: cannot remove '{a}': No such file or directory", "red")
                return 1
        return 0

    def sh_mv(self, args, out):
        if len(args) != 2:
            out("mv: missing file operand", "red")
            return 1
        src, dst = self.abspath(args[0]), self.abspath(args[1])
        if src not in self.files:
            out(f"mv: cannot stat '{args[0]}': No such file or directory", "red")
            return 1
        if dst in self.dirs:
            dst = posixpath.join(dst, posixpath.basename(src))
        self.write_file(dst, self.files.pop(src))
        return 0

    # --- git: dağıtıcı ------------------------------------------------------

    def git(self, args: list[str], out: Out) -> int:
        if not args or args[0] in ("--help", "help"):
            out("usage: git [--version] [--help] <command> [<args>]")
            return 0 if args else 1
        if args[0] in ("--version", "version"):
            out(GIT_VERSION)
            return 0
        sub, rest = args[0], args[1:]
        handler = getattr(self, "git_" + sub.replace("-", "_"), None)
        alias = self.config_get(self.repo_at(), f"alias.{sub.lower()}") if handler is None else None
        if alias and not getattr(self, "_in_alias", False):
            # Kısaltma (git config alias.lg "log --oneline"): yazılanı açıp yeniden çalıştır.
            self._in_alias = True
            try:
                return self.git(shlex.split(alias) + rest, out)
            finally:
                self._in_alias = False
        if handler is None:
            out(f"git: '{sub}' is not a git command. See 'git --help'.", "red")
            # git yalnızca en iyi puanlıları yazıyor (eşitse birden çok).
            scores = {c: difflib.SequenceMatcher(None, sub, c).ratio() for c in GIT_COMMANDS}
            top = max(scores.values())
            close = [c for c in GIT_COMMANDS if top >= 0.6 and abs(scores[c] - top) < 1e-9]
            if close:
                out("")
                out("The most similar command is" if len(close) == 1 else "The most similar commands are")
                for c in close:
                    out(f"\t{c}")
            return 1
        if any(a in ("-i", "--interactive", "-p", "--patch") for a in rest) and sub in (
                "add", "rebase", "checkout", "restore", "reset", "stash") and rest[:1] != ["show"]:
            out(self.t("interactive"), "yellow")
            return 1
        return handler(rest, out) or 0

    # --- init / config ------------------------------------------------------

    def git_init(self, args, out):
        bare = "--bare" in args
        names = [a for a in args if not a.startswith("-")]
        branch = self.config_get(None, "init.defaultbranch") or "master"
        for i, a in enumerate(args):
            if a in ("-b", "--initial-branch") and i + 1 < len(args):
                branch = args[i + 1]
                names = [n for n in names if n != branch]
        root = self.abspath(names[0]) if names else self.cwd
        d = root
        while d not in self.dirs:
            self.dirs.add(d)
            d = posixpath.dirname(d)
        quiet = "-q" in args or "--quiet" in args
        if root in self.repos:
            if not quiet:
                out(f"Reinitialized existing Git repository in {root}/.git/")
            return 0
        self.repos[root] = Repo(root=root, bare=bare, head=f"refs/heads/{branch}")
        if not quiet:
            out(f"Initialized empty Git repository in {root}/" + ("" if bare else ".git/"))
        return 0

    def local_config(self, repo: Repo) -> list[tuple[str, str]]:
        """`.git/config`'in satırları: init'in yazdıkları (Git Bash'teki gibi),
        kişinin ayarları, uzak depolar ve izlenen dallar."""
        items = {"core.repositoryformatversion": "0", "core.filemode": "false",
                 "core.bare": "true" if repo.bare else "false"}
        if not repo.bare:
            items["core.logallrefupdates"] = "true"
        items.update({"core.symlinks": "false", "core.ignorecase": "true"})
        for k, v in repo.config.items():
            # remote.<ad>.head benzeticinin iç kaydı (gerçekte refs/remotes/<ad>/HEAD).
            if not re.fullmatch(r"remote\.[^.]+\.head", k):
                items[k] = v
        for name, url in repo.remotes.items():
            items[f"remote.{name}.url"] = url
            items[f"remote.{name}.fetch"] = f"+refs/heads/*:refs/remotes/{name}/*"
        for b, (remote, rb) in repo.upstream.items():
            items[f"branch.{b}.remote"] = remote
            items[f"branch.{b}.merge"] = f"refs/heads/{rb}"
        return list(items.items())

    @staticmethod
    def _config_key(key: str) -> str:
        """Bölüm ve anahtar küçük harfe, alt bölüm olduğu gibi (git'in yaptığı)."""
        parts = key.split(".")
        if len(parts) < 2:
            raise GitError(f"error: key does not contain a section: {key}", 2)
        parts[0], parts[-1] = parts[0].lower(), parts[-1].lower()
        return ".".join(parts)

    def git_config(self, args, out):
        glob = "--global" in args
        local = "--local" in args
        origin = "--show-origin" in args
        rest = [a for a in args if a not in ("--global", "--local", "--show-origin", "--get")]
        repo = self.repo_at()
        if local and repo is None:
            raise GitError("fatal: --local can only be used inside a git repository")
        if rest and rest[0] in ("-e", "--edit"):
            out(self.t("no_editor_config"), "yellow")
            return 1
        if rest and rest[0] in ("--list", "-l"):
            rows = []
            if not local:
                rows += [(f"{HOME}/.gitconfig", k, v) for k, v in self.global_config.items()]
            if repo is not None and not glob:
                rows += [(".git/config", k, v) for k, v in self.local_config(repo)]
            if glob and not self.global_config:
                raise GitError(f"fatal: unable to read config file '{HOME}/.gitconfig': No such file or directory")
            for src, k, v in rows:
                out((f"file:{src}\t" if origin else "") + f"{k}={v}")
            return 0
        if rest and rest[0] == "--unset" and len(rest) > 1:
            if not glob and repo is None:
                raise GitError("fatal: not in a git directory")
            store = self.global_config if glob else repo.config
            key = self._config_key(rest[1])
            if key not in store:
                return 5
            store.pop(key)
            return 0
        if len(rest) == 1:
            key = self._config_key(rest[0])
            if glob:
                value = self.global_config.get(key)
            elif local:
                value = dict(self.local_config(repo)).get(key)
            else:
                value = dict(self.local_config(repo)).get(key) if repo is not None else None
                if value is None:
                    value = self.global_config.get(key, self.system_config.get(key))
            if value is None:
                return 1
            out(value)
            return 0
        if len(rest) >= 2:
            if not glob and repo is None:
                raise GitError("fatal: not in a git directory")
            store = self.global_config if glob else repo.config
            store[self._config_key(rest[0])] = rest[1]
            return 0
        out("usage: git config [<options>]", "red")
        return 129

    # --- status ---------------------------------------------------------

    def tracking(self, repo: Repo) -> list[str]:
        if repo.detached or repo.branch not in repo.upstream:
            return []
        remote, rbranch = repo.upstream[repo.branch]
        ref = f"refs/remotes/{remote}/{rbranch}"
        name = f"{remote}/{rbranch}"
        if ref not in repo.refs:
            return [f"Your branch is based on '{name}', but the upstream is gone.",
                    '  (use "git branch --unset-upstream" to fixup)']
        ahead = len(self.reachable(repo, repo.head_sha()) - self.reachable(repo, repo.refs[ref]))
        behind = len(self.reachable(repo, repo.refs[ref]) - self.reachable(repo, repo.head_sha()))
        s = lambda n: "" if n == 1 else "s"  # noqa: E731
        if ahead and behind:
            return [f"Your branch and '{name}' have diverged,",
                    f"and have {ahead} and {behind} different commits each, respectively.",
                    '  (use "git pull" if you want to integrate the remote branch with yours)']
        if ahead:
            return [f"Your branch is ahead of '{name}' by {ahead} commit{s(ahead)}.",
                    '  (use "git push" to publish your local commits)']
        if behind:
            return [f"Your branch is behind '{name}' by {behind} commit{s(behind)}, and can be fast-forwarded.",
                    '  (use "git pull" to update your local branch)']
        return [f"Your branch is up to date with '{name}'."]

    def status_long(self, repo: Repo, out: Out, ignored: bool = False) -> dict:
        ch = self.changes(repo)
        rebasing = (repo.state or {}).get("kind") == "rebase"
        if rebasing:
            pass
        elif repo.detached:
            base = getattr(repo, "detached_at", None) or repo.head
            word = "at" if base == repo.head else "from"
            out(f"HEAD detached {word} {short(base)}", "red")
        else:
            out(f"On branch {repo.branch}")
        track = self.tracking(repo)
        for line in track:
            out(line)
        no_commits = repo.head_sha() is None
        if no_commits:
            out("")
            out("No commits yet")
        sep = bool(track) or no_commits
        sections = []
        st = repo.state or {}
        if st.get("kind") == "merge":
            if ch["conflicts"]:
                sections.append(["You have unmerged paths.", '  (fix conflicts and run "git commit")',
                                 '  (use "git merge --abort" to abort the merge)'])
            else:
                sections.append(["All conflicts fixed but you are still merging.",
                                 '  (use "git commit" to conclude merge)'])
        elif st.get("kind") == "rebase":
            def pick(sha):
                return f"   pick {short(sha)} # {repo.commits[sha].message.splitlines()[0]}"
            # todo[0] durulan (çakışan) commit; kalanlar ondan sonrakiler.
            done, todo = st.get("done", []), st["todo"][1:]
            info = [f"interactive rebase in progress; onto {short(st['onto'])}"]
            if done:
                n = len(done)
                info.append(f"Last command{'s' if n > 1 else ''} done ({n} command{'s' if n > 1 else ''} done):")
                info += [pick(x) for x in done[-2:]]
                if n > 2:
                    info.append("  (see more in file .git/rebase-merge/done)")
            if todo:
                k = len(todo)
                info.append(f"Next command{'s' if k > 1 else ''} to do ({k} remaining command{'s' if k > 1 else ''}):")
                info += [pick(x) for x in todo[:2]]
                info.append('  (use "git rebase --edit-todo" to view and edit)')
            else:
                info.append("No commands remaining.")
            sections.append(info + [
                             f"You are currently rebasing branch '{st['branch']}' on '{short(st['onto'])}'.",
                             '  (fix conflicts and then run "git rebase --continue")',
                             '  (use "git rebase --skip" to skip this patch)',
                             '  (use "git rebase --abort" to check out the original branch)'])
        elif st.get("kind") == "cherry-pick":
            sections.append([f"You are currently cherry-picking commit {short(st['commit'])}.",
                             '  (fix conflicts and run "git cherry-pick --continue")',
                             '  (use "git cherry-pick --skip" to skip this patch)',
                             '  (use "git cherry-pick --abort" to cancel the cherry-pick operation)'])
        first = True
        for block in sections:
            if sep or not first:
                out("")
            for line in block:
                out(line)
            first = False
            sep = True
        blocks = []
        if ch["staged"]:
            hint = ('  (use "git rm --cached <file>..." to unstage)' if no_commits
                    else '  (use "git restore --staged <file>..." to unstage)')
            blocks.append(("Changes to be committed:", [] if st.get("kind") == "merge" else [hint],
                           ch["staged"], "green"))
        if ch["conflicts"]:
            blocks.append(("Unmerged paths:", (['  (use "git restore --staged <file>..." to unstage)'] if rebasing
                                               else []) + ['  (use "git add <file>..." to mark resolution)'],
                           [("both modified", p) for p in ch["conflicts"]], "red"))
        if ch["unstaged"]:
            has_del = any(k == "deleted" for k, _ in ch["unstaged"])
            blocks.append(("Changes not staged for commit:",
                           ['  (use "git add/rm <file>..." to update what will be committed)' if has_del
                            else '  (use "git add <file>..." to update what will be committed)',
                            '  (use "git restore <file>..." to discard changes in working directory)'],
                           ch["unstaged"], "red"))
        if ch["untracked"]:
            blocks.append(("Untracked files:", ['  (use "git add <file>..." to include in what will be committed)'],
                           [("", p) for p in self.untracked_display(repo, ch["untracked"])], "red"))
        if ignored:
            shown = self.ignored_display(repo)
            if shown:
                blocks.append(("Ignored files:", ['  (use "git add -f <file>..." to include in what will be committed)'],
                               [("", p) for p in shown], "red"))
        for title, hints, items, color in blocks:
            if sep:
                out("")
            out(title)
            for h in hints:
                out(h)
            for kind, path in items:
                label = kind + ":"
                width = 12 if len(label) < 12 else len(label) + 3
                out(f"\t{label:<{width}}{path}" if kind else f"\t{path}", color)
            sep = True
        if blocks:
            out("")
        if ch["staged"]:
            pass
        elif ch["unstaged"] or ch["conflicts"]:
            out('no changes added to commit (use "git add" and/or "git commit -a")')
        elif ch["untracked"]:
            out('nothing added to commit but untracked files present (use "git add" to track)')
        elif no_commits:
            if sep and not blocks:
                out("")
            out('nothing to commit (create/copy files and use "git add" to track)')
        else:
            if sep and not blocks:
                out("")
            out("nothing to commit, working tree clean")
        if out.lines and out.lines[-1][0] == "":
            out.lines.pop()
        return ch

    def git_status(self, args, out):
        repo = self.need_repo()
        if "-s" in args or "--short" in args:
            ch = self.changes(repo)
            codes: dict[str, list[str]] = {}
            for kind, path in ch["staged"]:
                if kind == "renamed":
                    codes[path] = ["R", " "]
                else:
                    codes.setdefault(path, [" ", " "])[0] = {"new file": "A", "deleted": "D", "modified": "M"}[kind]
            for kind, path in ch["unstaged"]:
                codes.setdefault(path, [" ", " "])[1] = {"deleted": "D", "modified": "M"}[kind]
            for path in ch["conflicts"]:
                codes[path] = ["U", "U"]
            for path in sorted(codes):
                x, y = codes[path]
                out(f"{x}{y} {path}", "")
            for path in self.untracked_display(repo, ch["untracked"]):
                out(f"?? {path}", "red")
            if "--ignored" in args:
                for path in self.ignored_display(repo):
                    out(f"!! {path}", "red")
            return 0
        self.status_long(repo, out, ignored="--ignored" in args)
        return 0

    # --- add / rm / mv ----------------------------------------------------

    def _match(self, repo: Repo, spec: str, candidates) -> list[str]:
        rel = posixpath.relpath(self.abspath(spec), repo.root)
        if rel == ".":
            return sorted(candidates)
        hits = [c for c in candidates if c == rel or c.startswith(rel + "/") or fnmatch.fnmatch(c, rel)]
        return sorted(hits)

    def git_add(self, args, out):
        repo = self.need_repo()
        allf = any(a in ("-A", "--all") for a in args)
        update = "-u" in args
        specs = [a for a in args if not a.startswith("-")]
        if not specs and not allf and not update:
            out("Nothing specified, nothing added.", "")
            out("hint: Maybe you wanted to say 'git add .'?", "yellow")
            return 0
        work = self.worktree(repo)
        if allf and not specs:
            specs = [posixpath.relpath(repo.root, self.cwd) if self.cwd != repo.root else "."]
            specs = ["."] if self.cwd == repo.root else [repo.root]
        candidates = set(work) | set(repo.index) | set(repo.conflicts)
        chosen: set[str] = set()
        for spec in specs:
            hits = self._match(repo, spec, candidates)
            if not hits:
                raise GitError(f"fatal: pathspec '{spec}' did not match any files")
            chosen.update(hits)
        ignored_hits = []
        force = "-f" in args or "--force" in args
        for path in sorted(chosen):
            if path in work:
                if not force and path not in repo.index and path not in repo.conflicts and self.ignored(repo, path):
                    if any(self.abspath(s) == posixpath.join(repo.root, path) for s in specs):
                        ignored_hits.append(path)
                    continue
                if update and path not in repo.index and path not in repo.conflicts:
                    continue
                repo.index[path] = self.add_blob(repo, work[path])
            else:
                repo.index.pop(path, None)
            repo.conflicts.pop(path, None)
        if ignored_hits:
            out("The following paths are ignored by one of your .gitignore files:", "")
            for p in ignored_hits:
                out(p)
            out("hint: Use -f if you really want to add them.", "yellow")
            out('hint: Disable this message with "git config set advice.addIgnoredFile false"', "yellow")
            return 1
        return 0

    def git_check_ignore(self, args, out):
        """Bir dosya neden yok sayılıyor: `-v` kuralı ve satırını da yazar."""
        repo = self.need_repo()
        verbose = "-v" in args or "--verbose" in args
        names = [a for a in args if not a.startswith("-")]
        if not names:
            raise GitError("fatal: no path specified", 128)
        found = False
        for name in names:
            rel = posixpath.relpath(self.abspath(name), repo.root)
            if rel in repo.index:
                continue
            rule = self.ignore_rule(repo, rel, rel + "/" in {d + "/" for d in self._repo_dirs(repo)})
            if rule and rule[2]:
                found = True
                out(f".gitignore:{rule[0]}:{rule[1]}\t{name}" if verbose else name)
        return 0 if found else 1

    def _repo_dirs(self, repo: Repo) -> set[str]:
        root = repo.root.rstrip("/") + "/"
        return {d[len(root):] for d in self.dirs if d.startswith(root)}

    def git_rm(self, args, out):
        repo = self.need_repo()
        cached = "--cached" in args
        recursive = "-r" in args
        specs = [a for a in args if not a.startswith("-")]
        for spec in specs:
            hits = self._match(repo, spec, repo.index)
            if not hits:
                raise GitError(f"fatal: pathspec '{spec}' did not match any files")
            if len(hits) > 1 or hits[0] != posixpath.relpath(self.abspath(spec), repo.root):
                if not recursive:
                    raise GitError(f"fatal: not removing '{spec}' recursively without -r")
            for path in hits:
                repo.index.pop(path, None)
                if not cached:
                    self.set_worktree_file(repo, path, None)
                out(f"rm '{path}'")
        return 0

    def git_mv(self, args, out):
        repo = self.need_repo()
        specs = [a for a in args if not a.startswith("-")]
        if len(specs) != 2:
            raise GitError("usage: git mv [<options>] <source>... <destination>", 129)
        src = posixpath.relpath(self.abspath(specs[0]), repo.root)
        dst = posixpath.relpath(self.abspath(specs[1]), repo.root)
        if src not in repo.index:
            raise GitError(f"fatal: not under version control, source={src}, destination={dst}")
        if posixpath.join(repo.root, dst) in self.dirs:
            dst = posixpath.join(dst, posixpath.basename(src))
        text = self.files.pop(posixpath.join(repo.root, src), None)
        if text is not None:
            self.write_file(posixpath.join(repo.root, dst), text)
        repo.index[dst] = repo.index.pop(src)
        return 0

    # --- revizyonlar -----------------------------------------------------

    def reachable(self, repo: Repo, sha: str | None) -> set[str]:
        seen: set[str] = set()
        stack = [sha] if sha else []
        while stack:
            s = stack.pop()
            if s in seen or s not in repo.commits:
                continue
            seen.add(s)
            stack.extend(repo.commits[s].parents)
        return seen

    def merge_base(self, repo: Repo, a: str, b: str) -> str | None:
        common = self.reachable(repo, a) & self.reachable(repo, b)
        if not common:
            return None
        # En yeni ortak ata: ötekilerin atası olmayan.
        for s in sorted(common, key=lambda x: repo.commits[x].time * 0 + self._seq(repo, x), reverse=True):
            return s
        return None

    def _seq(self, repo: Repo, sha: str) -> int:
        return list(repo.commits).index(sha)

    def peel(self, repo: Repo, sha: str) -> str:
        while sha in repo.tag_objects:
            sha = repo.tag_objects[sha][0]
        return sha

    def resolve(self, repo: Repo, rev: str) -> str:
        base, ops = rev, ""
        for i, ch in enumerate(rev):
            if ch in "~^":
                base, ops = rev[:i], rev[i:]
                break
        if base.startswith(("HEAD@{", "@{")) and base.endswith("}") and base[base.index("{") + 1:-1].isdigit():
            n = int(base[base.index("{") + 1:-1])
            sha = repo.reflog[n][0] if n < len(repo.reflog) else None
            if sha is None:
                raise GitError(f"fatal: log for 'HEAD' only has {len(repo.reflog)} entries")
        elif base in ("HEAD", "@", ""):
            sha = repo.head_sha()
        elif f"refs/heads/{base}" in repo.refs:
            sha = repo.refs[f"refs/heads/{base}"]
        elif f"refs/tags/{base}" in repo.refs:
            sha = self.peel(repo, repo.refs[f"refs/tags/{base}"])
        elif f"refs/remotes/{base}" in repo.refs:
            sha = repo.refs[f"refs/remotes/{base}"]
        elif base.startswith("stash@{") and base.endswith("}"):
            n = int(base[7:-1])
            sha = repo.stash[n]["sha"] if n < len(repo.stash) else None
        else:
            hits = [s for s in repo.commits if s.startswith(base.lower())] if len(base) >= 4 else []
            sha = hits[0] if len(hits) == 1 else None
        if sha is None:
            raise GitError(f"fatal: ambiguous argument '{rev}': unknown revision or path not in the working tree.\n"
                           "Use '--' to separate paths from revisions, like this:\n"
                           "'git <command> [<revision>...] -- [<file>...]'")
        i = 0
        while i < len(ops):
            op = ops[i]
            j = i + 1
            while j < len(ops) and ops[j].isdigit():
                j += 1
            n = int(ops[i + 1:j]) if j > i + 1 else 1
            for _ in range(n if op == "~" else 1):
                parents = repo.commits[sha].parents
                idx = 0 if op == "~" else n - 1
                if idx >= len(parents):
                    raise GitError(f"fatal: ambiguous argument '{rev}': unknown revision or path not in the working tree.")
                sha = parents[idx]
            i = j
        return sha

    def decorations(self, repo: Repo, sha: str) -> str:
        head = []
        if repo.head_sha() == sha:
            head.append(("HEAD -> " + repo.branch) if not repo.detached else "HEAD")
        items = []
        for ref in repo.refs:
            if repo.refs[ref] != sha and self.peel(repo, repo.refs[ref]) != sha:
                continue
            if ref.startswith("refs/heads/"):
                name = ref[11:]
                if name != repo.branch or repo.detached:
                    items.append((ref, name))
            elif ref.startswith("refs/remotes/"):
                items.append((ref, ref[13:]))
                remote, _, rb = ref[13:].partition("/")
                if repo.config.get(f"remote.{remote}.head") == rb:
                    items.append((f"refs/remotes/{remote}/HEAD", f"{remote}/HEAD"))
            elif ref.startswith("refs/tags/"):
                items.append((ref, "tag: " + ref[10:]))
        parts = head + [label for _, label in sorted(items, reverse=True)]
        return f" ({', '.join(parts)})" if parts else ""

    # --- istatistik ------------------------------------------------------

    def stat_lines(self, repo: Repo, old: dict, new: dict, out: Out, *, table: bool = False,
                   summary: bool = True) -> None:
        paths = sorted(set(old) | set(new))
        deleted = {old[p]: p for p in paths if p in old and p not in new}
        renames = {}
        for p in paths:
            if p in new and p not in old and new[p] in deleted:
                renames[deleted.pop(new[p])] = p
        rows, ins_total, del_total, modes = [], 0, 0, []
        for p in paths:
            if p in renames.values():
                continue
            a = repo.blobs.get(old[p], "") if p in old else ""
            b = repo.blobs.get(new[p], "") if p in new else ""
            if p in renames:
                rows.append((f"{p} => {renames[p]}", 0, 0))
                modes.append(f" rename {p} => {renames[p]} (100%)")
                continue
            if p in old and p in new and old[p] == new[p]:
                continue
            i, d = count_changes(a, b)
            ins_total += i
            del_total += d
            rows.append((p, i, d))
            if p not in old:
                modes.append(f" create mode 100644 {p}")
            elif p not in new:
                modes.append(f" delete mode 100644 {p}")
        if not rows:
            return
        if table:
            width = max(len(r[0]) for r in rows)
            for name, i, d in rows:
                n = i + d
                out(f" {name:<{width}} | {n} {'+' * i}{'-' * d}".rstrip())
        files = len(rows)
        parts = [f" {files} file{'s' if files != 1 else ''} changed"]
        if ins_total or not del_total:
            parts.append(f" {ins_total} insertion{'s' if ins_total != 1 else ''}(+)")
        if del_total or not ins_total:
            parts.append(f" {del_total} deletion{'s' if del_total != 1 else ''}(-)")
        out(",".join(parts))
        if summary:
            for m in modes:
                out(m)

    # --- commit ---------------------------------------------------------

    def _need_identity(self, repo: Repo) -> None:
        if not self.config_get(repo, "user.name") or not self.config_get(repo, "user.email"):
            raise GitError("Author identity unknown\n\n*** Please tell me who you are.\n\nRun\n\n"
                           '  git config --global user.email "you@example.com"\n'
                           '  git config --global user.name "Your Name"\n\n'
                           "to set your account's default identity.\n"
                           "Omit --global to set the identity only in this repository.\n\n"
                           "fatal: unable to auto-detect email address (got 'ada@odyssey.(none)')")

    def _messages(self, args) -> tuple[list[str], list[str]]:
        msgs, rest, i = [], [], 0
        while i < len(args):
            a = args[i]
            if a in ("-m", "--message") and i + 1 < len(args):
                msgs.append(args[i + 1])
                i += 2
                continue
            if a.startswith("-m") and len(a) > 2 and not a.startswith("--"):
                msgs.append(a[2:])
            elif a == "-am" and i + 1 < len(args):
                rest.append("-a")
                msgs.append(args[i + 1])
                i += 2
                continue
            else:
                rest.append(a)
            i += 1
        return msgs, rest

    def git_commit(self, args, out):
        repo = self.need_repo()
        msgs, rest = self._messages(args)
        amend = "--amend" in rest
        if "-a" in rest or "--all" in rest:
            work = self.worktree(repo)
            for path in list(repo.index):
                if path in work:
                    repo.index[path] = self.add_blob(repo, work[path])
                else:
                    del repo.index[path]
        if repo.conflicts:
            raise GitError("error: Committing is not possible because you have unmerged files.\n"
                           "hint: Fix them up in the work tree, and then use 'git add/rm <file>'\n"
                           "hint: as appropriate to mark resolution and make a commit.\n"
                           "fatal: Exiting because of an unresolved conflict.\n"
                           + "\n".join(f"U\t{c}" for c in sorted(repo.conflicts)))
        self._need_identity(repo)
        head = repo.head_sha()
        st = repo.state or {}
        if amend and head is None:
            raise GitError("fatal: You have nothing to amend.")
        message = "\n\n".join(msgs)
        if not message:
            if st.get("kind") == "merge":
                message = st["msg"]
                if "--no-edit" in rest and st.get("conflicted"):
                    message += "\n\n# Conflicts:\n" + "\n".join(f"#\t{c}" for c in st["conflicted"])
            elif amend and "--no-edit" in rest:
                message = repo.commits[head].message
            else:
                out(self.t("no_editor"), "yellow")
                return 1
        parents = repo.commits[head].parents[:] if amend else ([head] if head else [])
        if st.get("kind") == "merge":
            parents = [head, st["other"]]
        head_files = self.commit_files(repo, head)
        if (not amend and st.get("kind") != "merge" and repo.index == head_files
                and "--allow-empty" not in rest):
            self.status_long(repo, out)
            return 1
        sha = self.make_commit(repo, dict(repo.index), parents, message)
        repo.set_head_sha(sha)
        first = message.split("\n")[0]
        if st.get("kind") == "merge":
            kind = "commit (merge)"
        elif amend:
            kind = "commit (amend)"
        elif not parents:
            kind = "commit (initial)"
        else:
            kind = "commit"
        repo.reflog.insert(0, (sha, f"{kind}: {first}"))
        where = "detached HEAD" if repo.detached else repo.branch
        root = " (root-commit)" if not parents else ""
        out(f"[{where}{root} {short(sha)}] {first}")
        if st.get("kind") == "merge":
            repo.state = None
            return 0
        if amend:
            out(f" Date: {git_date(repo.commits[sha].time)}")
        old = self.commit_files(repo, parents[0]) if parents else {}
        before = len(out.lines)
        self.stat_lines(repo, old, repo.index, out)
        if len(out.lines) == before and "--allow-empty" not in rest:
            out(" 0 files changed")
        return 0

    # --- log / show -------------------------------------------------------

    def _ordered(self, repo: Repo, starts: list[str], limit: int | None) -> list[str]:
        seen = set()
        for s in starts:
            seen |= self.reachable(repo, s)
        order = sorted(seen, key=lambda x: self._seq(repo, x), reverse=True)
        return order[:limit] if limit else order

    def _topo(self, repo: Repo, starts: list[str], limit: int | None) -> list[str]:
        """--graph'ın sırası (git'in --topo-order'ı): çocuk ebeveynden önce, birleştirilen
        dalın commit'leri ana çizgiden önce (yığından son giren önce çıkar)."""
        seen = set()
        for s_ in starts:
            seen |= self.reachable(repo, s_)
        indeg = {c: 0 for c in seen}
        for c in seen:
            for par in repo.commits[c].parents:
                if par in indeg:
                    indeg[par] += 1
        tips = sorted({c for c in seen if indeg[c] == 0}, key=lambda x: self._seq(repo, x))
        stack, order = list(tips), []
        while stack:
            c = stack.pop()
            order.append(c)
            for par in repo.commits[c].parents:
                if par in indeg:
                    indeg[par] -= 1
                    if indeg[par] == 0:
                        stack.append(par)
        return order[:limit] if limit else order

    def _graph(self, repo: Repo, order: list[str]):
        """(önek, sha) satırları; sha None ise yalnızca çizgi."""
        cols: list[str] = []
        rows = []
        for sha in order:
            if sha not in cols:
                cols.append(sha)
            col = cols.index(sha)
            parents = repo.commits[sha].parents
            cells = ["*" if i == col else "|" for i in range(len(cols))]
            prefix = " ".join(cells)
            if len(parents) > 1:
                prefix += "  "
            rows.append((prefix, sha))
            if not parents:
                cols.pop(col)
            elif len(parents) == 1:
                p = parents[0]
                if p in cols and cols.index(p) != col:
                    keep = cols.index(p)
                    cols.pop(col)
                    left = ["|"] * len(cols)
                    rows.append((" ".join(left[:keep + 1]) + "/  " if col > keep else "|/  ", None))
                else:
                    cols[col] = p
            else:
                cols[col] = parents[0]
                extra = [p for p in parents[1:] if p not in cols]
                for k, p in enumerate(extra):
                    cols.insert(col + 1 + k, p)
                rows.append((" ".join(["|"] * (col + 1)) + "\\  ", None))
        return rows

    def _log_entry(self, repo: Repo, sha: str, out: Out, prefix: str = "", oneline: bool = False) -> None:
        c = repo.commits[sha]
        deco = self.decorations(repo, sha)
        if oneline:
            out.lines.append((f"{prefix}{short(sha)}{deco} {c.message.split(chr(10))[0]}", "yellow"))
            return
        out.lines.append((f"{prefix}commit {sha}{deco}", "yellow"))
        pad = prefix.replace("*", "|") if prefix else ""
        if len(c.parents) > 1:
            out(f"{pad}Merge: {' '.join(short(p) for p in c.parents)}")
        out(f"{pad}Author: {c.author} <{c.email}>")
        out(f"{pad}Date:   {git_date(c.time)}")
        out(pad.rstrip() if pad else "")
        for line in c.message.split("\n"):
            out(f"{pad}    {line}")

    def _touches(self, repo: Repo, sha: str, paths: list[str]) -> bool:
        """Commit (ilk ebeveynine göre) bu yollardan birini değiştirdi mi."""
        c = repo.commits[sha]
        new = self.commit_files(repo, sha)
        old = self.commit_files(repo, c.parents[0]) if c.parents else {}
        return any(new.get(p) != old.get(p) for p in set(new) | set(old)
                   if any(p == x or p.startswith(x.rstrip("/") + "/") for x in paths))

    def _format(self, repo: Repo, sha: str, fmt: str) -> str:
        """--format yer tutucuları (%h %H %an %ae %ad %s %b %d %n %%)."""
        c = repo.commits[sha]
        subject, _, body = c.message.partition("\n")
        values = {"h": short(sha), "H": sha, "an": c.author, "ae": c.email, "ad": git_date(c.time),
                  "cn": c.author, "ce": c.email, "s": subject, "b": body.strip("\n"),
                  "d": self.decorations(repo, sha), "n": "\n", "%": "%"}
        return re.sub(r"%(an|ae|ad|cn|ce|[hHsbdn%])", lambda m: values[m.group(1)], fmt)

    def git_log(self, args, out):
        repo = self.need_repo()
        paths = []
        if "--" in args:
            k = args.index("--")
            paths = [posixpath.relpath(self.abspath(p), repo.root) for p in args[k + 1:]]
            args = args[:k]
        oneline = "--oneline" in args
        graph = "--graph" in args
        patch = any(a in ("-p", "-u", "--patch") for a in args)
        stat = "--stat" in args
        names = "--name-only" in args
        flags = re.I if ("-i" in args or "--regexp-ignore-case" in args) else 0
        limit, revs, fmt, author, grep = None, [], None, None, None
        exclude = []
        i = 0
        while i < len(args):
            a = args[i]
            nxt = args[i + 1] if i + 1 < len(args) else None
            if a in ("-n", "--max-count", "--author", "--grep") and nxt is not None:
                if a in ("-n", "--max-count"):
                    limit = int(nxt)
                elif a == "--author":
                    author = nxt
                else:
                    grep = nxt
                i += 2
                continue
            if a.startswith("-") and a[1:].isdigit():
                limit = int(a[1:])
            elif a.startswith("--max-count="):
                limit = int(a.split("=", 1)[1])
            elif a.startswith("--author="):
                author = a.split("=", 1)[1]
            elif a.startswith("--grep="):
                grep = a.split("=", 1)[1]
            elif a.startswith(("--format=", "--pretty=")):
                value = a.split("=", 1)[1]
                if value == "oneline":
                    oneline = True
                elif value.startswith(("format:", "tformat:")):
                    fmt = value.split(":", 1)[1]
                elif value not in ("short", "medium", "full"):
                    fmt = value
            elif not a.startswith("-") and ".." in a:
                # A..B: B'de olup A'da olmayan commit'ler (B yoksa HEAD).
                left, _, right = a.partition("..")
                exclude.append(self.resolve(repo, left or "HEAD"))
                revs.append(right or "HEAD")
            elif not a.startswith("-"):
                try:
                    self.resolve(repo, a)
                    revs.append(a)
                except GitError:
                    rel = posixpath.relpath(self.abspath(a), repo.root)
                    if rel in self.worktree(repo) or rel in repo.index:
                        paths.append(rel)
                    else:
                        raise
            i += 1
        if repo.head_sha() is None and not revs and "--all" not in args:
            raise GitError(f"fatal: your current branch '{repo.branch}' does not have any commits yet")
        starts = [self.resolve(repo, r) for r in revs] or [repo.head_sha()]
        if "--all" in args:
            starts += [self.peel(repo, s) for r, s in repo.refs.items() if not r.startswith("refs/tags/")]
        filtered = bool(paths or author or grep or exclude)
        order = self._ordered(repo, [s for s in starts if s], None if filtered else limit)
        hidden = set()
        for x in exclude:
            hidden |= self.reachable(repo, x)
        if hidden:
            order = [sha for sha in order if sha not in hidden]
        if paths:
            order = [sha for sha in order if self._touches(repo, sha, paths)]
        if author:
            order = [sha for sha in order if re.search(author, f"{repo.commits[sha].author} <{repo.commits[sha].email}>",
                                                         flags)]
        if grep:
            order = [sha for sha in order if re.search(grep, repo.commits[sha].message, flags)]
        if filtered and limit:
            order = order[:limit]
        if "--reverse" in args:
            order.reverse()
        if graph and not (paths or author or grep):
            topo = [x for x in self._topo(repo, [s for s in starts if s], None) if x not in hidden]
            rows = self._graph(repo, topo[:limit] if limit else topo)
            first = True
            for prefix, sha in rows:
                if sha is None:
                    out(prefix)
                    continue
                if not oneline and not first:
                    out(prefix.replace("*", "|").rstrip() or "|")
                self._log_entry(repo, sha, out, prefix + " ", oneline)
                first = False
            return 0
        for n, sha in enumerate(order):
            if fmt is not None:
                out(self._format(repo, sha, fmt))
                continue
            if n and not oneline:
                out("")
            self._log_entry(repo, sha, out, oneline=oneline)
            c = repo.commits[sha]
            if (patch or stat or names) and len(c.parents) < 2:
                old = self.commit_files(repo, c.parents[0]) if c.parents else {}
                new = self.commit_files(repo, sha)
                if not oneline:
                    out("")
                if stat:
                    self.stat_lines(repo, old, new, out, table=True, summary=False)
                elif names:
                    for p in sorted(set(old) | set(new)):
                        if old.get(p) != new.get(p):
                            out(p)
                else:
                    self._diff_out(repo, old, new, out)
        return 0

    def git_show(self, args, out):
        repo = self.need_repo()
        revs = [a for a in args if not a.startswith("-")] or ["HEAD"]
        rev = revs[0]
        if ":" in rev and not rev.startswith("stash@{"):
            base, _, path = rev.partition(":")
            files = self.commit_files(repo, self.resolve(repo, base or "HEAD"))
            if path not in files:
                raise GitError(f"fatal: path '{path}' does not exist in '{base or 'HEAD'}'")
            out(repo.blobs.get(files[path], "").rstrip("\n"))
            return 0
        tag_ref = f"refs/tags/{rev}"
        if tag_ref in repo.refs and repo.refs[tag_ref] in repo.tag_objects:
            target, name, msg, who, when = repo.tag_objects[repo.refs[tag_ref]]
            out(f"tag {name}", "yellow")
            out(f"Tagger: {who}")
            out(f"Date:   {git_date(when)}")
            out("")
            out(msg)
            out("")
        sha = self.resolve(repo, rev)
        self._log_entry(repo, sha, out, oneline="--oneline" in args)
        c = repo.commits[sha]
        if len(c.parents) > 1:
            return 0
        old = self.commit_files(repo, c.parents[0]) if c.parents else {}
        new = self.commit_files(repo, sha)
        if "--stat" in args:
            out("")
            self.stat_lines(repo, old, new, out, table=True, summary=False)
            return 0
        if "--name-only" in args:
            out("")
            for p in sorted(set(old) | set(new)):
                if old.get(p) != new.get(p):
                    out(p)
            return 0
        if "--oneline" not in args:
            out("")
        self._diff_out(repo, old, new, out)
        return 0

    def git_clean(self, args, out):
        """İzlenmeyen dosyaları siler: -n (yalnızca göster), -f (sil), -d (klasörler), -x (yok sayılanlar da)."""
        repo = self.need_repo()
        flags = set()
        for a in args:
            if a.startswith("--"):
                flags.add({"--dry-run": "n", "--force": "f"}.get(a, a))
            elif a.startswith("-"):
                flags.update(a[1:])
        if "i" in flags:
            out(self.t("interactive"), "yellow")
            return 1
        if "n" not in flags and "f" not in flags:
            raise GitError("fatal: clean.requireForce is true and -f not given: refusing to clean")
        work = self.worktree(repo)
        tracked = set(repo.index)
        tracked_dirs = {posixpath.dirname(p) for p in tracked}
        tracked_dirs |= {d for p in tracked for d in self._parents(p)}
        targets = []
        dirs_seen = set()
        for rel in sorted(work):
            if rel in tracked:
                continue
            ignored = self.ignored(repo, rel)
            if ignored and "x" not in flags:
                continue
            parts = rel.split("/")
            top = None
            for k in range(1, len(parts)):
                d = "/".join(parts[:k])
                if d not in tracked_dirs:
                    top = d
                    break
            if top is None:
                targets.append((rel, [rel]))
            elif "d" in flags and top not in dirs_seen:
                dirs_seen.add(top)
                members = [r for r in work if r.startswith(top + "/") and r not in tracked]
                targets.append((top + "/", members))
        targets.sort()
        for name, members in targets:
            if "n" in flags:
                out(f"Would remove {name}")
                continue
            out(f"Removing {name}")
            for rel in members:
                self.files.pop(posixpath.join(repo.root, rel), None)
            if name.endswith("/"):
                base = posixpath.join(repo.root, name.rstrip("/"))
                self.dirs = {d for d in self.dirs if d != base and not d.startswith(base + "/")}
        return 0

    @staticmethod
    def _parents(rel: str) -> list[str]:
        parts = rel.split("/")
        return ["/".join(parts[:k]) for k in range(1, len(parts))]

    def git_blame(self, args, out):
        """Her satırı onu getiren commit'le: ilk ebeveyn zincirinde geriye doğru izleniyor."""
        repo = self.need_repo()
        names = [a for a in args if not a.startswith("-")]
        if not names:
            out("usage: git blame [<options>] [<rev-opts>] [<rev>] [--] <file>", "red")
            return 129
        path = posixpath.relpath(self.abspath(names[-1]), repo.root)
        head = repo.head_sha()
        head_files = self.commit_files(repo, head)
        if path not in head_files:
            raise GitError(f"fatal: no such path '{path}' in HEAD")
        work = self.worktree(repo).get(path)
        cur = (work if work is not None else repo.blobs.get(head_files[path], "")).splitlines()
        owner: list[str | None] = [None] * len(cur)

        def trace(sha, text_lines, idx_map):
            """idx_map: bu metnin satırı -> güncel satır numarası."""
            while True:
                c = repo.commits[sha]
                parent = c.parents[0] if c.parents else None
                pf = self.commit_files(repo, parent) if parent else {}
                ptext = repo.blobs.get(pf[path], "").splitlines() if path in pf else []
                matched = {}
                for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ptext, text_lines,
                                                                   autojunk=False).get_opcodes():
                    if tag == "equal":
                        for k in range(i2 - i1):
                            matched[j1 + k] = i1 + k
                new_map = {}
                for j, cur_i in idx_map.items():
                    if j in matched:
                        new_map[matched[j]] = cur_i
                    else:
                        owner[cur_i] = sha
                if not new_map or parent is None:
                    for cur_i in new_map.values():
                        owner[cur_i] = sha
                    return
                sha, text_lines, idx_map = parent, ptext, new_map

        head_text = repo.blobs.get(head_files[path], "").splitlines()
        start = {}
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, head_text, cur, autojunk=False).get_opcodes():
            if tag == "equal":
                for k in range(i2 - i1):
                    start[i1 + k] = j1 + k
        trace(head, head_text, start)
        who = {}
        for sha in set(o for o in owner if o):
            c = repo.commits[sha]
            dt = datetime.fromtimestamp(c.time, TZ)
            who[sha] = (c.author, f"{dt:%Y-%m-%d %H:%M:%S} +0300")
        now = datetime.fromtimestamp(self._time, TZ)
        width = max([len(w[0]) for w in who.values()] + ([len("Not Committed Yet")] if None in owner else []))
        num = len(str(len(cur)))
        for n, (sha, text) in enumerate(zip(owner, cur), start=1):
            if sha is None:
                ident, (name, when) = "00000000", ("Not Committed Yet", f"{now:%Y-%m-%d %H:%M:%S} +0300")
            else:
                boundary = not repo.commits[sha].parents
                ident = ("^" + sha[:7]) if boundary else sha[:8]
                name, when = who[sha]
            out(f"{ident} ({name:<{width}} {when} {n:>{num}}) {text}")
        return 0

    # --- diff -----------------------------------------------------------

    def _diff_out(self, repo: Repo, old: dict, new: dict, out: Out, *, old_text=None, new_text=None,
                  paths: list[str] | None = None) -> None:
        old_text = old_text or (lambda p: repo.blobs.get(old[p], ""))
        new_text = new_text or (lambda p: repo.blobs.get(new[p], ""))
        for p in sorted(set(old) | set(new)):
            if paths and not any(p == x or p.startswith(x.rstrip("/") + "/") for x in paths):
                continue
            if p in old and p in new and old[p] == new[p]:
                continue
            a = old_text(p) if p in old else ""
            b = new_text(p) if p in new else ""
            out.lines.append((f"diff --git a/{p} b/{p}", "bold"))
            if p not in old:
                out.lines.append(("new file mode 100644", "bold"))
                out.lines.append((f"index 0000000..{short(new[p])}", "bold"))
            elif p not in new:
                out.lines.append(("deleted file mode 100644", "bold"))
                out.lines.append((f"index {short(old[p])}..0000000", "bold"))
            else:
                out.lines.append((f"index {short(old[p])}..{short(new[p])} 100644", "bold"))
            out.lines.append(("--- " + (f"a/{p}" if p in old else "/dev/null"), "bold"))
            out.lines.append(("+++ " + (f"b/{p}" if p in new else "/dev/null"), "bold"))
            for line in unified(a, b, p, p):
                color = "cyan" if line.startswith("@@") else "green" if line.startswith("+") else (
                    "red" if line.startswith("-") else "")
                out.lines.append((line, color))

    def git_diff(self, args, out):
        repo = self.need_repo()
        paths = []
        if "--" in args:
            k = args.index("--")
            paths = [posixpath.relpath(self.abspath(p), repo.root) for p in args[k + 1:]]
            args = args[:k]
        staged = "--staged" in args or "--cached" in args
        revs = [a for a in args if not a.startswith("-")]
        work = self.worktree(repo)
        work_sha = {p: blob_sha(t) for p, t in work.items() if p in repo.index or p in repo.conflicts}
        rels = []
        for r in revs:
            if posixpath.relpath(self.abspath(r), repo.root) in set(work) | set(repo.index):
                paths.append(posixpath.relpath(self.abspath(r), repo.root))
            else:
                rels.append(r)
        if staged:
            old = self.commit_files(repo, self.resolve(repo, rels[0]) if rels else repo.head_sha())
            new, nt = dict(repo.index), None
        elif len(rels) >= 2:
            old = self.commit_files(repo, self.resolve(repo, rels[0]))
            new, nt = self.commit_files(repo, self.resolve(repo, rels[1])), None
        elif len(rels) == 1:
            old = self.commit_files(repo, self.resolve(repo, rels[0]))
            new = {p: blob_sha(work[p]) for p in work if p in old or p in repo.index}
            nt = lambda p: work[p]  # noqa: E731
        else:
            old = dict(repo.index)
            new = work_sha
            nt = lambda p: work[p]  # noqa: E731
        if "--stat" in args:
            tmp = Repo(root=repo.root, blobs=dict(repo.blobs))
            for p, t in work.items():
                tmp.blobs[blob_sha(t)] = t
            self.stat_lines(tmp, old, new, out, table=True, summary=False)
            return 0
        if "--name-only" in args:
            for p in sorted(set(old) | set(new)):
                if old.get(p) != new.get(p):
                    out(p)
            return 0
        self._diff_out(repo, old, new, out, new_text=nt, paths=paths or None)
        return 0

    # --- çalışma ağacını bir commit'e taşımak ------------------------------

    def _local_changes(self, repo: Repo) -> set[str]:
        """Hazırlanmış ya da hazırlanmamış değişikliği olan izlenen dosyalar."""
        head = self.commit_files(repo, repo.head_sha())
        work = self.worktree(repo)
        changed = {p for p in set(head) | set(repo.index) if head.get(p) != repo.index.get(p)}
        changed |= {p for p in repo.index if p not in work or blob_sha(work[p]) != repo.index[p]}
        return changed

    def _move_to(self, repo: Repo, target: str | None, action: str) -> None:
        """HEAD'in ağacından hedefin ağacına geç; yerel değişiklikler taşınır."""
        old = self.commit_files(repo, repo.head_sha())
        new = self.commit_files(repo, target)
        local = self._local_changes(repo)
        clash = sorted(p for p in local if old.get(p) != new.get(p))
        if clash:
            noun = "checkout" if action == "checkout" else action
            verb = "switch branches" if action == "checkout" else action
            raise GitError(f"error: Your local changes to the following files would be overwritten by {noun}:\n"
                           + "".join(f"\t{p}\n" for p in clash)
                           + f"Please commit your changes or stash them before you {verb}.\nAborting", 1)
        work = self.worktree(repo)
        untracked_hit = sorted(p for p in new if p not in old and p in work and p not in repo.index
                               and work[p] != repo.blobs.get(new[p]))
        if untracked_hit:
            raise GitError(f"error: The following untracked working tree files would be overwritten by {action}:\n"
                           + "".join(f"\t{p}\n" for p in untracked_hit)
                           + f"Please move or remove them before you {action}.\nAborting", 1)
        index = dict(new)
        for p in local:
            if p in repo.index:
                index[p] = repo.index[p]
            else:
                index.pop(p, None)
        for p in old:
            if p not in new and p not in local:
                self.set_worktree_file(repo, p, None)
        for p, sha in new.items():
            if p not in local:
                self.set_worktree_file(repo, p, repo.blobs[sha])
        repo.index = index

    def _hard_to(self, repo: Repo, target: str | None) -> None:
        old = self.commit_files(repo, repo.head_sha())
        new = self.commit_files(repo, target)
        for p in set(old) | set(repo.index):
            if p not in new:
                self.set_worktree_file(repo, p, None)
        for p, sha in new.items():
            self.set_worktree_file(repo, p, repo.blobs[sha])
        repo.index = dict(new)
        repo.conflicts = {}

    # --- restore / reset / revert ----------------------------------------

    def git_restore(self, args, out):
        repo = self.need_repo()
        staged = "--staged" in args or "-S" in args
        worktree = "--worktree" in args or "-W" in args or not staged
        source = None
        specs = []
        for a in args:
            if a.startswith("--source="):
                source = a.split("=", 1)[1]
            elif not a.startswith("-"):
                specs.append(a)
        if not specs:
            raise GitError("fatal: you must specify path(s) to restore")
        if "--ours" in args or "--theirs" in args:
            return self._take_side(repo, specs, "--theirs" in args, out, quiet=True)
        head = self.commit_files(repo, repo.head_sha())
        src = self.commit_files(repo, self.resolve(repo, source)) if source else None
        work = self.worktree(repo)
        for spec in specs:
            pool = set(head) | set(repo.index) | set(work) | set(src or {})
            hits = self._match(repo, spec, pool)
            if not hits:
                raise GitError(f"error: pathspec '{spec}' did not match any file(s) known to git", 1)
            for p in hits:
                if staged:
                    base = src if src is not None else head
                    if p in base:
                        repo.index[p] = base[p]
                    else:
                        repo.index.pop(p, None)
                if worktree:
                    base = src if src is not None else (repo.index if not staged else head)
                    if p in base:
                        self.set_worktree_file(repo, p, repo.blobs[base[p]])
                    elif p in repo.index or p in head:
                        self.set_worktree_file(repo, p, None)
        return 0

    def git_reset(self, args, out):
        repo = self.need_repo()
        mode = "--mixed"
        for m in ("--soft", "--mixed", "--hard"):
            if m in args:
                mode = m
        rest = [a for a in args if not a.startswith("-")]
        head = repo.head_sha()
        # Dosya verildiyse: yalnızca hazırlık alanından çıkar (reflog'a yazılmaz).
        # `git reset HEAD a.txt` da böyle: ilk ad sürüm, gerisi dosya.
        paths = rest if rest and rest[0] != "HEAD" and not self._is_rev(repo, rest[0]) else rest[1:]
        if paths:
            if mode in ("--soft", "--hard"):
                raise GitError(f"fatal: Cannot do {mode[2:]} reset with paths.")
            src = head if paths is rest else self.resolve(repo, rest[0])
            files = self.commit_files(repo, src)
            for spec in paths:
                for p in self._match(repo, spec, set(files) | set(repo.index)):
                    if p in files:
                        repo.index[p] = files[p]
                    else:
                        repo.index.pop(p, None)
            self._unstaged_after(repo, out)
            return 0
        target = self.resolve(repo, rest[0]) if rest else head
        if mode == "--hard":
            self._hard_to(repo, target)
        elif mode == "--mixed":
            repo.index = self.commit_files(repo, target)
        repo.set_head_sha(target)
        repo.state = None
        # Gerçek git yerinde duran reset'i de yazıyor ("reset: moving to HEAD").
        repo.reflog.insert(0, (target, f"reset: moving to {rest[0] if rest else 'HEAD'}"))
        if mode == "--hard":
            out(f"HEAD is now at {short(target)} {repo.commits[target].message.splitlines()[0]}")
        elif mode == "--mixed":
            self._unstaged_after(repo, out)
        return 0

    def _is_rev(self, repo: Repo, rev: str) -> bool:
        try:
            self.resolve(repo, rev)
            return True
        except GitError:
            return False

    def _unstaged_after(self, repo: Repo, out: Out) -> None:
        ch = self.changes(repo)
        if ch["unstaged"]:
            out("Unstaged changes after reset:")
            for kind, p in ch["unstaged"]:
                out(f"{'D' if kind == 'deleted' else 'M'}\t{p}")

    def git_revert(self, args, out):
        repo = self.need_repo()
        self._need_identity(repo)
        revs = [a for a in args if not a.startswith("-")]
        if not revs:
            raise GitError("usage: git revert [<options>] <commit-ish>...", 129)
        sha = self.resolve(repo, revs[0])
        c = repo.commits[sha]
        if not c.parents:
            raise GitError("error: cannot revert a root commit")
        if self._local_changes(repo):
            raise GitError("error: your local changes would be overwritten by revert.\n"
                           "hint: commit your changes or stash them to proceed.\nfatal: revert failed")
        base = self.commit_files(repo, sha)
        theirs = self.commit_files(repo, c.parents[0])
        merged, conflicts = self._three_way(repo, base, self.commit_files(repo, repo.head_sha()), theirs,
                                            f"parent of {short(sha)} ({c.message.splitlines()[0]})")
        if conflicts:
            raise GitError(f"error: could not revert {short(sha)}... {c.message.splitlines()[0]}", 1)
        msg = f'Revert "{c.message.splitlines()[0]}"\n\nThis reverts commit {sha}.'
        head = repo.head_sha()
        new = self.make_commit(repo, merged, [head], msg)
        self._hard_to(repo, new)
        repo.set_head_sha(new)
        repo.reflog.insert(0, (new, f'revert: Revert "{c.message.splitlines()[0]}"'))
        out(f"[{repo.branch or 'detached HEAD'} {short(new)}] Revert \"{c.message.splitlines()[0]}\"")
        self.stat_lines(repo, self.commit_files(repo, head), merged, out)
        return 0

    # --- dallar -----------------------------------------------------------

    def git_branch(self, args, out):
        repo = self.need_repo()
        flags = [a for a in args if a.startswith("-")]
        names = [a for a in args if not a.startswith("-")]
        listing = {"-a", "--all", "-r", "--remotes", "-v", "-vv", "--verbose", "--list", "--merged", "--no-merged"}
        if not names or flags and set(flags) <= listing:
            if not names or "--list" in flags:
                show_local = "-r" not in flags and "--remotes" not in flags
                verbose = 2 if "-vv" in flags else (1 if ("-v" in flags or "--verbose" in flags) else 0)
                branches = repo.branches()
                here = self.reachable(repo, repo.head_sha()) if repo.head_sha() else set()
                if "--merged" in flags:
                    branches = [b for b in branches if repo.refs[f"refs/heads/{b}"] in here]
                if "--no-merged" in flags:
                    branches = [b for b in branches if repo.refs[f"refs/heads/{b}"] not in here]
                width = max((len(b) for b in branches), default=0)
                if show_local:
                    for b in branches:
                        current = b == repo.branch and not repo.detached
                        text = b
                        if verbose:
                            tip = repo.refs[f"refs/heads/{b}"]
                            up = ""
                            if verbose == 2 and b in repo.upstream:
                                r, rb = repo.upstream[b]
                                rref = repo.refs.get(f"refs/remotes/{r}/{rb}")
                                info = []
                                if rref:
                                    ahead = len(self.reachable(repo, tip) - self.reachable(repo, rref))
                                    behind = len(self.reachable(repo, rref) - self.reachable(repo, tip))
                                    if ahead:
                                        info.append(f"ahead {ahead}")
                                    if behind:
                                        info.append(f"behind {behind}")
                                up = f"[{r}/{rb}{': ' + ', '.join(info) if info else ''}] "
                            text = f"{b:<{width}} {short(tip)} {up}{repo.commits[tip].message.splitlines()[0]}"
                        if current:
                            out(f"* {text}", "green")
                        else:
                            out(f"  {text}")
                    if repo.detached:
                        out.lines.insert(0, (f"* (HEAD detached at {short(repo.head)})", "green"))
                if any(f in flags for f in ("-a", "--all", "-r", "--remotes")):
                    pre = "remotes/" if show_local else ""
                    rows = {r[13:]: f"  {pre}{r[13:]}" for r in repo.refs if r.startswith("refs/remotes/")}
                    for name in repo.remotes:
                        head = repo.config.get(f"remote.{name}.head")
                        if head and f"refs/remotes/{name}/{head}" in repo.refs:
                            rows[f"{name}/HEAD"] = f"  {pre}{name}/HEAD -> {name}/{head}"
                    for key in sorted(rows):
                        out(rows[key], "red")
                return 0
        if any(f in flags for f in ("-d", "-D", "--delete")):
            force = "-D" in flags
            for name in names:
                ref = f"refs/heads/{name}"
                if ref not in repo.refs:
                    raise GitError(f"error: branch '{name}' not found", 1)
                if name == repo.branch and not repo.detached:
                    raise GitError(f"error: cannot delete branch '{name}' used by worktree at '{repo.root}'", 1)
                tip = repo.refs[ref]
                if not force and tip not in self.reachable(repo, repo.head_sha()):
                    raise GitError(f"error: the branch '{name}' is not fully merged\n"
                                   f"hint: If you are sure you want to delete it, run 'git branch -D {name}'\n"
                                   'hint: Disable this message with "git config set advice.forceDeleteBranch false"', 1)
                del repo.refs[ref]
                repo.upstream.pop(name, None)
                out(f"Deleted branch {name} (was {short(tip)}).")
            return 0
        if any(f in flags for f in ("-m", "-M", "--move")):
            old, new = (names if len(names) == 2 else [repo.branch, names[0]])
            if f"refs/heads/{old}" not in repo.refs and old != repo.branch:
                raise GitError(f"error: refname refs/heads/{old} not found\nfatal: Branch rename failed")
            if f"refs/heads/{new}" in repo.refs and "-M" not in flags:
                raise GitError(f"fatal: a branch named '{new}' already exists")
            sha = repo.refs.pop(f"refs/heads/{old}", None)
            if sha:
                repo.refs[f"refs/heads/{new}"] = sha
            if old == repo.branch:
                repo.head = f"refs/heads/{new}"
            if old in repo.upstream:
                repo.upstream[new] = repo.upstream.pop(old)
            return 0
        name = names[0]
        if f"refs/heads/{name}" in repo.refs:
            raise GitError(f"fatal: a branch named '{name}' already exists")
        if repo.head_sha() is None and len(names) == 1:
            raise GitError(f"fatal: not a valid object name: '{repo.branch}'")
        start = self.resolve(repo, names[1]) if len(names) > 1 else repo.head_sha()
        self._check_branch_name(repo, name)
        repo.refs[f"refs/heads/{name}"] = start
        return 0

    @staticmethod
    def _check_branch_name(repo: Repo, name: str) -> None:
        """`feature` varken `feature/login` (ya da tersi) açılamaz: git dalları klasör gibi saklıyor."""
        new = f"refs/heads/{name}"
        for ref in repo.refs:
            if ref.startswith("refs/heads/") and (new.startswith(ref + "/") or ref.startswith(new + "/")):
                raise GitError(f"fatal: cannot lock ref '{new}': '{ref}' exists; cannot create '{new}'")

    def _switch_to_branch(self, repo: Repo, name: str, out: Out, new: bool = False, start: str | None = None) -> None:
        if new:
            self._check_branch_name(repo, name)
        # Kopuk HEAD'den çıkarken reflog'a tam kimlik yazılıyor (git'teki gibi).
        prev = (repo.head_sha() if repo.detached else repo.branch) or short(repo.head_sha() or "")
        target = start if new else repo.refs[f"refs/heads/{name}"]
        if repo.head_sha() is not None or target is not None:
            self._move_to(repo, target, "checkout")
        was_detached = repo.detached
        old_sha = repo.head_sha()
        if new and target is not None:
            repo.refs[f"refs/heads/{name}"] = target
        repo.head = f"refs/heads/{name}"
        self._prev = prev
        if target:
            repo.reflog.insert(0, (target, f"checkout: moving from {prev} to {name}"))
        self._local_change_lines(repo, out)
        orphans = self._orphans(repo, old_sha) if was_detached and old_sha else []
        if orphans:
            n = len(orphans)
            out(f"Warning: you are leaving {n} commit{'s' if n > 1 else ''} behind, not connected to\n"
                "any of your branches:\n", "yellow")
            for sha in orphans[:4]:
                out(f"  {short(sha)} {repo.commits[sha].message.splitlines()[0]}")
            if n > 4:
                out(f" ... and {n - 4} more.")
            out("\nIf you want to keep it by creating a new branch, this may be a good time\n"
                f"to do so with:\n\n git branch <new-branch-name> {short(old_sha)}\n", "yellow")
        elif was_detached and old_sha and old_sha != target:
            out(f"Previous HEAD position was {short(old_sha)} {repo.commits[old_sha].message.splitlines()[0]}")
        out(f"Switched to a new branch '{name}'" if new else f"Switched to branch '{name}'")
        for line in self.tracking(repo):
            out(line)

    def _orphans(self, repo: Repo, sha: str) -> list[str]:
        """sha'dan ulaşılan ama hiçbir dal / etiket / uzak daldan ulaşılamayan commit'ler (yeniden eskiye)."""
        kept = set()
        for ref, target in repo.refs.items():
            kept |= self.reachable(repo, self.peel(repo, target))
        lost = self.reachable(repo, sha) - kept
        return sorted(lost, key=lambda x: self._seq(repo, x), reverse=True)

    def _local_change_lines(self, repo: Repo, out: Out) -> None:
        """Dal değişirken yanında taşınan değişiklikler: git'teki `M\tdosya` satırları."""
        head = self.commit_files(repo, repo.head_sha())
        work = self.worktree(repo)
        for p in sorted(set(head) | set(repo.index)):
            if p not in head:
                out(f"A\t{p}")
            elif p not in repo.index or p not in work:
                out(f"D\t{p}")
            elif repo.index[p] != head[p] or blob_sha(work[p]) != repo.index[p]:
                out(f"M\t{p}")

    def _detach(self, repo: Repo, sha: str, label: str, out: Out, *, advice: bool = True) -> None:
        prev = repo.branch or short(repo.head_sha() or "")
        self._move_to(repo, sha, "checkout")
        old = repo.head_sha()
        repo.head = sha
        repo.detached_at = sha
        self._prev = prev
        repo.reflog.insert(0, (sha, f"checkout: moving from {prev} to {label}"))
        if advice:
            out(f"Note: switching to '{label}'.\n\n"
                "You are in 'detached HEAD' state. You can look around, make experimental\n"
                "changes and commit them, and you can discard any commits you make in this\n"
                "state without impacting any branches by switching back to a branch.\n\n"
                "If you want to create a new branch to retain commits you create, you may\n"
                "do so (now or later) by using -c with the switch command. Example:\n\n"
                "  git switch -c <new-branch-name>\n\n"
                "Or undo this operation with:\n\n"
                "  git switch -\n\n"
                "Turn off this advice by setting config variable advice.detachedHead to false\n")
        elif old and old != sha:
            out(f"Previous HEAD position was {short(old)} {repo.commits[old].message.splitlines()[0]}")
        out(f"HEAD is now at {short(sha)} {repo.commits[sha].message.splitlines()[0]}")

    def _dwim_remote(self, repo: Repo, name: str) -> str | None:
        hits = [r for r in repo.refs if r.startswith("refs/remotes/") and r.endswith("/" + name)]
        return hits[0] if len(hits) == 1 else None

    def git_switch(self, args, out):
        repo = self.need_repo()
        if repo.state:
            raise GitError("fatal: cannot switch branch while merging\n"
                           "Consider \"git merge --quit\" or \"git worktree add\".")
        names = [a for a in args if not a.startswith("-")]
        if "-c" in args or "--create" in args or "-C" in args:
            if not names:
                raise GitError("fatal: missing branch name; try -c")
            name = names[0]
            if f"refs/heads/{name}" in repo.refs and "-C" not in args:
                raise GitError(f"fatal: a branch named '{name}' already exists")
            start = self.resolve(repo, names[1]) if len(names) > 1 else repo.head_sha()
            self._switch_to_branch(repo, name, out, new=True, start=start)
            return 0
        if "--detach" in args:
            rev = names[0] if names else "HEAD"
            self._detach(repo, self.resolve(repo, rev), rev, out, advice=False)
            return 0
        if args == ["-"]:
            prev = getattr(self, "_prev", None)
            if not prev:
                raise GitError("fatal: invalid reference: @{-1}")
            if f"refs/heads/{prev}" in repo.refs:
                self._switch_to_branch(repo, prev, out)
            else:
                self._detach(repo, self.resolve(repo, prev), prev, out, advice=False)
            return 0
        if not names:
            raise GitError("fatal: missing branch or commit argument")
        name = names[0]
        if name == repo.branch and not repo.detached:
            out(f"Already on '{name}'")
            for line in self.tracking(repo):
                out(line)
            return 0
        if f"refs/heads/{name}" in repo.refs:
            self._switch_to_branch(repo, name, out)
            return 0
        remote = self._dwim_remote(repo, name)
        if remote:
            rname = remote[13:].split("/")[0]
            repo.upstream[name] = (rname, name)
            out(f"branch '{name}' set up to track '{rname}/{name}'.")
            self._switch_to_branch(repo, name, out, new=True, start=repo.refs[remote])
            return 0
        if self._is_rev(repo, name):
            raise GitError(f"fatal: a branch is expected, got commit '{name}'\n"
                           "hint: If you want to detach HEAD at the commit, try again with the --detach option.")
        raise GitError(f"fatal: invalid reference: {name}")

    def git_checkout(self, args, out):
        repo = self.need_repo()
        if "--ours" in args or "--theirs" in args:
            return self._take_side(repo, [a for a in args if not a.startswith("-")], "--theirs" in args, out,
                                   quiet=False)
        if "--" in args:
            k = args.index("--")
            revs = [a for a in args[:k] if not a.startswith("-")]
            return self._checkout_files(repo, args[k + 1:], out, rev=revs[0] if revs else None)
        names = [a for a in args if not a.startswith("-")]
        if "-b" in args or "-B" in args:
            if not names:
                raise GitError("error: switch `b' requires a value", 129)
            name = names[0]
            if f"refs/heads/{name}" in repo.refs and "-B" not in args:
                raise GitError(f"fatal: a branch named '{name}' already exists")
            start = self.resolve(repo, names[1]) if len(names) > 1 else repo.head_sha()
            self._switch_to_branch(repo, name, out, new=True, start=start)
            return 0
        if not names:
            if args == ["-"]:
                return self.git_switch(["-"], out)
            return 0
        name = names[0]
        if f"refs/heads/{name}" in repo.refs:
            if name == repo.branch and not repo.detached:
                out(f"Already on '{name}'")
                return 0
            self._switch_to_branch(repo, name, out)
            return 0
        remote = self._dwim_remote(repo, name)
        if remote:
            rname = remote[13:].split("/")[0]
            repo.upstream[name] = (rname, name)
            out(f"branch '{name}' set up to track '{rname}/{name}'.")
            self._switch_to_branch(repo, name, out, new=True, start=repo.refs[remote])
            return 0
        if self._is_rev(repo, name):
            self._detach(repo, self.resolve(repo, name), name, out)
            return 0
        return self._checkout_files(repo, names, out)

    def _take_side(self, repo: Repo, specs: list[str], theirs: bool, out: Out, quiet: bool) -> int:
        """Çakışan dosyayı bir tarafın hâline getirir; dosya `git add`'e kadar çakışmalı kalır."""
        n = 0
        for spec in specs:
            hits = [p for p in self._match(repo, spec, set(repo.conflicts) | set(repo.index))]
            if not hits:
                raise GitError(f"error: pathspec '{spec}' did not match any file(s) known to git", 1)
            for p in hits:
                if p not in repo.conflicts:
                    raise GitError(f"error: path '{p}' does not have {'their' if theirs else 'our'} version", 1)
                blob = repo.conflicts[p][2 if theirs else 1]
                self.set_worktree_file(repo, p, repo.blobs.get(blob, "") if blob else None)
                n += 1
        if not quiet:
            out(f"Updated {n} path{'s' if n != 1 else ''} from the index")
        return 0

    def _checkout_files(self, repo: Repo, specs: list[str], out: Out, rev: str | None = None) -> int:
        if rev is not None:
            # checkout <commit> -- dosya: dosya o commit'teki hâline, hem hazırlık alanına hem klasöre.
            files = self.commit_files(repo, self.resolve(repo, rev))
            for spec in specs:
                hits = self._match(repo, spec, files)
                if not hits:
                    raise GitError(f"error: pathspec '{spec}' did not match any file(s) known to git", 1)
                for p in hits:
                    repo.index[p] = files[p]
                    self.set_worktree_file(repo, p, repo.blobs[files[p]])
            return 0
        n = 0
        for spec in specs:
            hits = self._match(repo, spec, repo.index)
            if not hits:
                raise GitError(f"error: pathspec '{spec}' did not match any file(s) known to git", 1)
            for p in hits:
                self.set_worktree_file(repo, p, repo.blobs[repo.index[p]])
                n += 1
        out(f"Updated {n} path{'s' if n != 1 else ''} from the index")
        return 0

    # --- birleştirme -------------------------------------------------------

    def _three_way(self, repo: Repo, base: dict, ours: dict, theirs: dict, their_name: str):
        """(birleşmiş yol → blob, çakışmalar {yol: (taban, bizim, onların)}). Notlar `self._merge_notes`."""
        merged, conflicts = {}, {}
        self._merge_notes = []
        for p in sorted(set(base) | set(ours) | set(theirs)):
            b, o, t = base.get(p), ours.get(p), theirs.get(p)
            if o == t:
                if o is not None:
                    merged[p] = o
            elif b == o:
                if t is not None:
                    merged[p] = t
            elif b == t:
                if o is not None:
                    merged[p] = o
            elif o is None or t is None:
                merged[p] = o or t
            else:
                text, conflict = merge_text(repo.blobs.get(b, "") if b else "", repo.blobs[o], repo.blobs[t],
                                            their_name)
                self._merge_notes.append(f"Auto-merging {p}")
                if conflict:
                    self._merge_notes.append(f"CONFLICT (content): Merge conflict in {p}")
                    conflicts[p] = (b, o, t, text)
                else:
                    merged[p] = self.add_blob(repo, text)
        return merged, conflicts

    def _merge_into_head(self, repo: Repo, other: str, label: str, out: Out, *, message: str | None = None,
                         no_ff: bool = False, reflog_label: str | None = None) -> int:
        head = repo.head_sha()
        if other in self.reachable(repo, head):
            out("Already up to date.")
            return 0
        if head is None or (head in self.reachable(repo, other) and not no_ff):
            self._move_to(repo, other, "merge")
            old = self.commit_files(repo, head)
            repo.set_head_sha(other)
            if head:
                out(f"Updating {short(head)}..{short(other)}")
            out("Fast-forward")
            self.stat_lines(repo, old, self.commit_files(repo, other), out, table=True)
            repo.reflog.insert(0, (other, f"{reflog_label or 'merge ' + label}: Fast-forward"))
            return 0
        base = self.merge_base(repo, head, other)
        ours = self.commit_files(repo, head)
        theirs = self.commit_files(repo, other)
        merged, conflicts = self._three_way(repo, self.commit_files(repo, base), ours, theirs, label)
        local = self._local_changes(repo)
        clash = sorted(p for p in local if merged.get(p) != ours.get(p) or p in conflicts)
        if clash:
            raise GitError("error: Your local changes to the following files would be overwritten by merge:\n"
                           + "".join(f"\t{p}\n" for p in clash)
                           + "Please commit your changes or stash them before you merge.\nAborting", 1)
        msg = message or (f"Merge remote-tracking branch '{label}'" if label.count("/") else f"Merge branch '{label}'")
        for note in self._merge_notes:
            out(note, "red" if note.startswith("CONFLICT") else "")
        if conflicts:
            snapshot = {"index": dict(repo.index), "work": self.worktree(repo)}
            for p, sha in merged.items():
                self.set_worktree_file(repo, p, repo.blobs[sha])
            for p in ours:
                if p not in merged and p not in conflicts:
                    self.set_worktree_file(repo, p, None)
            repo.index = {p: s for p, s in merged.items()}
            repo.conflicts = {p: v[:3] for p, v in conflicts.items()}
            for p, v in conflicts.items():
                self.set_worktree_file(repo, p, v[3])
            repo.state = {"kind": "merge", "other": other, "msg": msg, "snapshot": snapshot,
                          "conflicted": sorted(conflicts)}
            out("Automatic merge failed; fix conflicts and then commit the result.")
            return 1
        self._need_identity(repo)
        new = self.make_commit(repo, merged, [head, other], msg)
        self._hard_to(repo, new)
        repo.set_head_sha(new)
        repo.reflog.insert(0, (new, f"{reflog_label or 'merge ' + label}: Merge made by the 'ort' strategy."))
        out("Merge made by the 'ort' strategy.")
        self.stat_lines(repo, ours, merged, out, table=True)
        return 0

    def git_merge(self, args, out):
        repo = self.need_repo()
        if "--abort" in args:
            st = repo.state or {}
            if st.get("kind") != "merge":
                raise GitError("fatal: There is no merge to abort (MERGE_HEAD missing).")
            snap = st["snapshot"]
            for p in list(self.worktree(repo)):
                if p in repo.index or p in repo.conflicts or p in snap["work"]:
                    self.set_worktree_file(repo, p, None)
            for p, text in snap["work"].items():
                self.set_worktree_file(repo, p, text)
            repo.index = snap["index"]
            repo.conflicts = {}
            repo.state = None
            return 0
        if "--continue" in args:
            if (repo.state or {}).get("kind") != "merge":
                raise GitError("fatal: There is no merge in progress (MERGE_HEAD missing).")
            return self.git_commit([], out)
        if repo.state:
            raise GitError("fatal: You have not concluded your merge (MERGE_HEAD exists).\n"
                           "Please, commit your changes before you merge.")
        msgs, rest = self._messages(args)
        names = [a for a in rest if not a.startswith("-")]
        if not names:
            raise GitError("fatal: No remote for the current branch.")
        if "--squash" in rest:
            out(self.t("unsupported", what="git merge --squash"), "yellow")
            return 1
        try:
            other = self.resolve(repo, names[0])
        except GitError:
            raise GitError(f"merge: {names[0]} - not something we can merge", 1) from None
        return self._merge_into_head(repo, other, names[0], out, message="\n\n".join(msgs) or None,
                                     no_ff="--no-ff" in rest)

    # --- etiket / stash / reflog -------------------------------------------

    def git_tag(self, args, out):
        repo = self.need_repo()
        msgs, rest = self._messages(args)
        names = [a for a in rest if not a.startswith("-")]
        if "-d" in rest or "--delete" in rest:
            for n in names:
                ref = f"refs/tags/{n}"
                if ref not in repo.refs:
                    raise GitError(f"error: tag '{n}' not found.", 1)
                out(f"Deleted tag '{n}' (was {short(repo.refs.pop(ref))})")
            return 0
        if not names or "-l" in rest or "--list" in rest or "-n" in rest:
            pattern = names[0] if names and ("-l" in rest or "--list" in rest) else "*"
            for r in sorted(repo.refs):
                if r.startswith("refs/tags/") and fnmatch.fnmatch(r[10:], pattern):
                    if "-n" in rest:
                        obj = repo.refs[r]
                        note = (repo.tag_objects[obj][2] if obj in repo.tag_objects
                                else repo.commits[obj].message).splitlines()[0]
                        out(f"{r[10:]:<15} {note}")
                    else:
                        out(r[10:])
            return 0
        name = names[0]
        if f"refs/tags/{name}" in repo.refs:
            raise GitError(f"fatal: tag '{name}' already exists")
        target = self.resolve(repo, names[1]) if len(names) > 1 else repo.head_sha()
        if target is None:
            raise GitError("fatal: Failed to resolve 'HEAD' as a valid ref.")
        if "-a" in rest or msgs:
            if not msgs:
                out(self.t("no_editor").replace("git commit", f"git tag -a {name}"), "yellow")
                return 1
            who = f"{self.config_get(repo, 'user.name')} <{self.config_get(repo, 'user.email')}>"
            when = self.tick()
            body = f"object {target}\ntype commit\ntag {name}\ntagger {who} {when} +0300\n\n{msgs[0]}\n"
            sha = _sha("tag", body.encode())
            repo.tag_objects[sha] = (target, name, msgs[0], who, when)
            repo.refs[f"refs/tags/{name}"] = sha
        else:
            repo.refs[f"refs/tags/{name}"] = target
        return 0

    def git_describe(self, args, out):
        """En yakın etiketten uzaklık: `v1.1` ya da `v1.1-1-g817f03c` (--tags hafif etiketleri de sayar)."""
        repo = self.need_repo()
        names = [a for a in args if not a.startswith("-")]
        head = self.resolve(repo, names[0]) if names else repo.head_sha()
        if head is None:
            raise GitError("fatal: No names found, cannot describe anything.")
        here = self.reachable(repo, head)
        best = None
        any_light = False
        for ref, obj in sorted(repo.refs.items()):
            if not ref.startswith("refs/tags/"):
                continue
            annotated = obj in repo.tag_objects
            if not annotated and "--tags" not in args:
                any_light = True
                continue
            target = self.peel(repo, obj)
            if target not in here:
                continue
            n = len(here - self.reachable(repo, target))
            if best is None or n < best[0]:
                best = (n, ref[10:])
        if best is None:
            if any_light:
                raise GitError(f"fatal: No annotated tags can describe '{head}'.\n"
                               "However, there were unannotated tags: try --tags.")
            raise GitError("fatal: No names found, cannot describe anything.")
        n, name = best
        out(name if n == 0 else f"{name}-{n}-g{short(head)}")
        return 0

    def _stash_label(self, repo: Repo) -> str:
        head = repo.head_sha()
        return f"{repo.branch or '(no branch)'}: {short(head)} {repo.commits[head].message.splitlines()[0]}"

    def git_stash(self, args, out):
        repo = self.need_repo()
        sub = args[0] if args and not args[0].startswith("-") else "push"
        rest = args[1:] if args and not args[0].startswith("-") else args
        if sub in ("push", "save"):
            if repo.head_sha() is None:
                raise GitError("You do not have the initial commit yet", 1)
            msgs, rest = self._messages(rest)
            local = self._local_changes(repo)
            untracked = self.changes(repo)["untracked"] if ("-u" in rest or "--include-untracked" in rest) else []
            if not local and not untracked:
                out("No local changes to save")
                return 0
            work = self.worktree(repo)
            label = (f"On {repo.branch}: {msgs[0]}" if msgs else f"WIP on {self._stash_label(repo)}")
            entry = {"base": repo.head_sha(), "index": dict(repo.index),
                     "work": {p: work.get(p) for p in local}, "untracked": {p: work[p] for p in untracked},
                     "label": label}
            flat = {p: s for p, s in repo.index.items()}
            for p, text in entry["work"].items():
                if text is None:
                    flat.pop(p, None)
                else:
                    flat[p] = self.add_blob(repo, text)
            entry["sha"] = self.make_commit(repo, flat, [repo.head_sha()], label)
            repo.stash.insert(0, entry)
            for p in untracked:
                self.set_worktree_file(repo, p, None)
            self._hard_to(repo, repo.head_sha())
            # stash içeride `reset --hard` çalıştırıyor; reflog'da görünüyor.
            repo.reflog.insert(0, (repo.head_sha(), "reset: moving to HEAD"))
            out(f"Saved working directory and index state {label}")
            return 0
        if sub == "list":
            for i, e in enumerate(repo.stash):
                out(f"stash@{{{i}}}: {e['label']}")
            return 0
        if sub in ("pop", "apply", "drop", "show"):
            n = 0
            names = [a for a in rest if not a.startswith("-")]
            if names:
                ref = names[0]
                n = int(ref[7:-1]) if ref.startswith("stash@{") else int(ref)
            if n >= len(repo.stash):
                raise GitError("error: No stash entries found." if not repo.stash
                               else f"error: stash@{{{n}}} is not a valid reference", 1)
            e = repo.stash[n]
            if sub == "show":
                old = self.commit_files(repo, e["base"])
                if "-p" in rest or "--patch" in rest:
                    self._diff_out(repo, old, self.commit_files(repo, e["sha"]), out)
                else:
                    self.stat_lines(repo, old, self.commit_files(repo, e["sha"]), out, table=True, summary=False)
                return 0
            if sub in ("pop", "apply"):
                local = self._local_changes(repo)
                clash = sorted(p for p in e["work"] if p in local)
                if clash:
                    raise GitError("error: Your local changes to the following files would be overwritten by merge:\n"
                                   + "".join(f"\t{p}\n" for p in clash)
                                   + "Please commit your changes or stash them before you merge.\nAborting", 1)
                if not e["work"] and e["untracked"]:
                    # Yalnızca izlenmeyen dosyalar saklanmışsa izlenen tarafta birleştirilecek bir şey yok.
                    out("Already up to date.")
                for p, text in list(e["work"].items()) + list(e["untracked"].items()):
                    self.set_worktree_file(repo, p, text)
                    if text is not None and p not in repo.index and p in e["index"]:
                        repo.index[p] = self.add_blob(repo, text)
                    if text is None:
                        repo.index.pop(p, None) if p not in e["index"] else None
                self.status_long(repo, out)
            if sub in ("pop", "drop"):
                repo.stash.pop(n)
                ref = f"refs/stash@{{{n}}}" if sub == "pop" and not names else f"stash@{{{n}}}"
                out(f"Dropped {ref} ({e['sha']})")
            return 0
        if sub == "clear":
            repo.stash = []
            return 0
        out(self.t("unsupported", what=f"git stash {sub}"), "yellow")
        return 1

    def git_reflog(self, args, out):
        repo = self.need_repo()
        limit = None
        for a in args:
            if a.startswith("-") and a[1:].isdigit():
                limit = int(a[1:])
        for i, (sha, msg) in enumerate(repo.reflog[:limit]):
            out.lines.append((f"{short(sha)}{self.decorations(repo, sha)} HEAD@{{{i}}}: {msg}", "yellow"))
        return 0

    # --- uzak depolar --------------------------------------------------------

    def add_remote_repo(self, url: str, branch: str = "main") -> Repo:
        """Benzeticide bir uzak depo (GitHub'daki depo gibi): çıplak, boş."""
        repo = Repo(root=url, bare=True, head=f"refs/heads/{branch}")
        self.remote_repos[url] = repo
        return repo

    def _copy_objects(self, src: Repo, dst: Repo) -> None:
        for name in ("blobs", "trees", "tag_objects"):
            getattr(dst, name).update(getattr(src, name))
        for sha, c in src.commits.items():
            if sha not in dst.commits:
                dst.commits[sha] = c

    def remote_commit(self, url: str, files: dict[str, str | None], message: str, branch: str = "main",
                      author: tuple[str, str] = ("Grace Hopper", "grace@example.com")) -> str:
        """Başka biri uzak depoya commit atmış gibi (alıştırma kurulumu)."""
        r = self.remote_repos[url]
        ref = f"refs/heads/{branch}"
        parent = r.refs.get(ref)
        flat = self.commit_files(r, parent)
        for p, text in files.items():
            if text is None:
                flat.pop(p, None)
            else:
                flat[p] = self.add_blob(r, text)
        sha = self.make_commit(r, flat, [parent] if parent else [], message, author=author)
        r.refs[ref] = sha
        return sha

    def lookup_remote(self, url: str, base: str | None = None) -> Repo | None:
        """Uzak depo: benzeticideki adres (GitHub gibi) ya da bu makinedeki çıplak depo."""
        if url in self.remote_repos:
            return self.remote_repos[url]
        path = posixpath.normpath(posixpath.join(base or self.cwd, url)) if not url.startswith("/") else url
        repo = self.repos.get(path)
        return repo if repo is not None and repo.bare else None

    def _remote_of(self, repo: Repo, name: str) -> Repo:
        url = repo.remotes.get(name)
        found = self.lookup_remote(url, repo.root) if url else None
        if found is not None:
            return found
        if url and "://" in url and url not in self.remote_repos:
            # GitHub'da açılmamış (ya da yanlış yazılmış) depo.
            raise GitError(f"remote: Repository not found.\nfatal: repository '{url.rstrip('/')}/' not found")
        if url is None or url not in self.remote_repos:
            raise GitError(f"fatal: '{name}' does not appear to be a git repository\n"
                           "fatal: Could not read from remote repository.\n\n"
                           "Please make sure you have the correct access rights\nand the repository exists.")
        return self.remote_repos[url]

    def git_remote(self, args, out):
        repo = self.need_repo()
        if not args:
            for n in sorted(repo.remotes):
                out(n)
            return 0
        if args[0] in ("-v", "--verbose"):
            for n in sorted(repo.remotes):
                out(f"{n}\t{repo.remotes[n]} (fetch)")
                out(f"{n}\t{repo.remotes[n]} (push)")
            return 0
        if args[0] == "add" and len(args) >= 3:
            if args[1] in repo.remotes:
                raise GitError(f"error: remote {args[1]} already exists.", 3)
            # Adres yalnızca kaydedilir; depo GitHub'da yoksa ilk push / fetch'te anlaşılır.
            repo.remotes[args[1]] = args[2]
            return 0
        if args[0] in ("remove", "rm") and len(args) >= 2:
            if args[1] not in repo.remotes:
                raise GitError(f"error: No such remote: '{args[1]}'", 2)
            del repo.remotes[args[1]]
            for r in [r for r in repo.refs if r.startswith(f"refs/remotes/{args[1]}/")]:
                del repo.refs[r]
            return 0
        if args[0] == "set-url" and len(args) >= 3:
            repo.remotes[args[1]] = args[2]
            return 0
        out(self.t("unsupported", what="git remote " + " ".join(args)), "yellow")
        return 1

    def git_clone(self, args, out):
        names = [a for a in args if not a.startswith("-")]
        if not names:
            raise GitError("fatal: You must specify a repository to clone.", 129)
        url = names[0]
        src = self.lookup_remote(url)
        if src is None:
            if "://" in url:
                dirname = names[1] if len(names) > 1 else posixpath.basename(url.rstrip("/")).removesuffix(".git")
                out(f"Cloning into '{dirname}'...")
                raise GitError(f"remote: Repository not found.\nfatal: repository '{url.rstrip('/')}/' not found")
            raise GitError(f"fatal: repository '{url}' does not exist")
        if url not in self.remote_repos:
            url = posixpath.normpath(posixpath.join(self.cwd, url))
        dirname = names[1] if len(names) > 1 else posixpath.basename(url.rstrip("/")).removesuffix(".git")
        root = self.abspath(dirname)
        if root in self.dirs and self._children(root):
            raise GitError(f"fatal: destination path '{dirname}' already exists and is not an empty directory.")
        out(f"Cloning into '{dirname}'...")
        self.dirs.add(root)
        repo = Repo(root=root, head=src.head)
        self.repos[root] = repo
        self._copy_objects(src, repo)
        repo.remotes["origin"] = url
        repo.config["remote.origin.head"] = src.head[11:]
        for ref, sha in src.refs.items():
            if ref.startswith("refs/heads/"):
                repo.refs[f"refs/remotes/origin/{ref[11:]}"] = sha
            elif ref.startswith("refs/tags/"):
                repo.refs[ref] = sha
        branch = src.head[11:]
        if f"refs/heads/{branch}" in src.refs:
            sha = src.refs[f"refs/heads/{branch}"]
            repo.refs[f"refs/heads/{branch}"] = sha
            repo.upstream[branch] = ("origin", branch)
            for p, b in self.commit_files(repo, sha).items():
                self.set_worktree_file(repo, p, repo.blobs[b])
            repo.index = self.commit_files(repo, sha)
            repo.reflog.insert(0, (sha, f"clone: from {url}"))
        else:
            out("warning: You appear to have cloned an empty repository.")
        if url not in self.remote_repos:
            out("done.")
        return 0

    def _fetch(self, repo: Repo, remote: str, out: Out, prune: bool = False) -> bool:
        r = self._remote_of(repo, remote)
        self._copy_objects(r, repo)
        pruned = []
        if prune:
            # GitHub'da silinmiş dalların izleme dalları (origin/x) da silinir.
            for ref in sorted(repo.refs):
                pre = f"refs/remotes/{remote}/"
                if ref.startswith(pre) and f"refs/heads/{ref[len(pre):]}" not in r.refs:
                    del repo.refs[ref]
                    pruned.append(f" - [deleted]         {'(none)':<10} -> {remote}/{ref[len(pre):]}")
        # git 2.48'den beri fetch uzak deponun HEAD'ini de izliyor (origin/HEAD).
        if r.head.startswith("refs/heads/") and r.head in r.refs:
            repo.config[f"remote.{remote}.head"] = r.head[11:]
        lines = []
        for ref, sha in sorted(r.refs.items()):
            if not ref.startswith("refs/heads/"):
                if ref.startswith("refs/tags/") and ref not in repo.refs:
                    repo.refs[ref] = sha
                    lines.append(f" * [new tag]         {ref[10:]:<10} -> {ref[10:]}")
                continue
            name = ref[11:]
            local = f"refs/remotes/{remote}/{name}"
            old = repo.refs.get(local)
            if old == sha:
                continue
            if old is None:
                lines.append(f" * [new branch]      {name:<10} -> {remote}/{name}")
            else:
                lines.append(f"   {short(old)}..{short(sha)}  {name:<10} -> {remote}/{name}")
            repo.refs[local] = sha
        lines = pruned + lines
        if lines:
            out(f"From {repo.remotes[remote].removesuffix('.git')}")
            for line in lines:
                out(line)
        return bool(lines)

    def git_fetch(self, args, out):
        repo = self.need_repo()
        names = [a for a in args if not a.startswith("-")]
        remote = names[0] if names else "origin"
        if not repo.remotes:
            raise GitError("fatal: No remote repository specified.  Please, specify either a URL or a\n"
                           "remote name from which new revisions should be fetched.")
        self._fetch(repo, remote, out, prune="--prune" in args or "-p" in args
                    or self.config_get(repo, "fetch.prune") == "true")
        return 0

    def git_push(self, args, out):
        repo = self.need_repo()
        set_up = "-u" in args or "--set-upstream" in args
        tags = "--tags" in args
        force = "-f" in args or "--force" in args
        names = [a for a in args if not a.startswith("-")]
        if not repo.remotes:
            raise GitError("fatal: No configured push destination.\n"
                           "Either specify the URL from the command-line or configure a remote repository using\n\n"
                           "    git remote add <name> <url>\n\n"
                           "and then push using the remote name\n\n    git push <name>\n\n"
                           "To push to multiple remotes at once, configure a remote group using\n\n"
                           "    git config remotes.<groupname> \"<remote1> <remote2>\"\n\n"
                           "and then push using the group name\n\n    git push <groupname>\n")
        if not names:
            if repo.detached:
                raise GitError("fatal: You are not currently on a branch.")
            if repo.branch not in repo.upstream and self.config_get(repo, "push.autosetupremote") == "true" \
                    and "origin" in repo.remotes:
                # push.autoSetupRemote: ilk push'ta -u origin <dal> kendiliğinden.
                return self.git_push(["-u", "origin", repo.branch], out)
            if repo.branch not in repo.upstream:
                raise GitError(f"fatal: The current branch {repo.branch} has no upstream branch.\n"
                               "To push the current branch and set the remote as upstream, use\n\n"
                               f"    git push --set-upstream origin {repo.branch}\n\n"
                               "To have this happen automatically for branches without a tracking\n"
                               "upstream, see 'push.autoSetupRemote' in 'git help config'.\n")
            remote, rbranch = repo.upstream[repo.branch]
            refs = [(repo.branch, rbranch)]
        else:
            remote = names[0]
            specs = names[1:] or ([] if tags else [repo.branch])
            refs = []
            for s in specs:
                a, _, b = s.partition(":")
                refs.append((a, b or a))
        r = self._remote_of(repo, remote)
        lines, rejected, notes = [], [], []
        # Uzak dalı silmek: git push origin --delete dal  (ya da  git push origin :dal)
        deletes = [b for _, b in refs if "--delete" in args or "-d" in args] or \
            [b for a, b in refs if a == "" and b]
        if deletes:
            done = []
            for b in deletes:
                if r.head == f"refs/heads/{b}":
                    raise GitError(
                        "remote: error: By default, deleting the current branch is denied, because the next\n"
                        "remote: 'git clone' won't result in any file checked out, causing confusion.\n"
                        "remote:\n"
                        "remote: You can set 'receive.denyDeleteCurrent' configuration variable to\n"
                        "remote: 'warn' or 'ignore' in the remote repository to allow deleting the\n"
                        "remote: current branch, with or without a warning message.\n"
                        "remote:\n"
                        "remote: To squelch this message, you can set it to 'refuse'.\n"
                        f"remote: error: refusing to delete the current branch: refs/heads/{b}\n"
                        f"To {repo.remotes[remote]}\n"
                        f" ! [remote rejected] {b} (deletion of the current branch prohibited)\n"
                        f"error: failed to push some refs to '{repo.remotes[remote]}'", 1)
                if f"refs/heads/{b}" not in r.refs:
                    raise GitError(f"error: unable to delete '{b}': remote ref does not exist\n"
                                   f"error: failed to push some refs to '{repo.remotes[remote]}'", 1)
                del r.refs[f"refs/heads/{b}"]
                repo.refs.pop(f"refs/remotes/{remote}/{b}", None)
                done.append(f" - [deleted]         {b}")
            out(f"To {repo.remotes[remote]}")
            for line in done:
                out(line)
            return 0
        for local, rb in refs:
            if f"refs/tags/{local}" in repo.refs and f"refs/heads/{local}" not in repo.refs:
                if f"refs/tags/{local}" not in r.refs:
                    r.refs[f"refs/tags/{local}"] = repo.refs[f"refs/tags/{local}"]
                    self._copy_objects(repo, r)
                    lines.append(f" * [new tag]         {local} -> {local}")
                continue
            if f"refs/heads/{local}" not in repo.refs:
                raise GitError(f"error: src refspec {local} does not match any\n"
                               f"error: failed to push some refs to '{repo.remotes[remote]}'", 1)
            sha = repo.refs[f"refs/heads/{local}"]
            old = r.refs.get(f"refs/heads/{rb}")
            if old == sha:
                continue
            if old and old not in self.reachable(repo, sha) and not force:
                rejected.append((local, rb, "fetch first" if old not in repo.commits else "non-fast-forward"))
                continue
            self._copy_objects(repo, r)
            r.refs[f"refs/heads/{rb}"] = sha
            repo.refs[f"refs/remotes/{remote}/{rb}"] = sha
            if old is None:
                lines.append(f" * [new branch]      {local} -> {rb}")
                url = repo.remotes[remote]
                if "github.com/" in url and r.head != f"refs/heads/{rb}":
                    # GitHub yeni dal gelince pull request bağlantısını yazar.
                    page = url.removesuffix(".git")
                    notes.extend(["remote: ", f"remote: Create a pull request for '{rb}' on GitHub by visiting:",
                                  f"remote:      {page}/pull/new/{rb}", "remote: "])
            elif force and old not in self.reachable(repo, sha):
                lines.append(f" + {short(old)}...{short(sha)} {local} -> {rb} (forced update)")
            else:
                lines.append(f"   {short(old)}..{short(sha)}  {local} -> {rb}")
            if set_up:
                repo.upstream[local] = (remote, rb)
        if tags:
            for ref, sha in sorted(repo.refs.items()):
                if ref.startswith("refs/tags/") and ref not in r.refs:
                    r.refs[ref] = sha
                    self._copy_objects(repo, r)
                    lines.append(f" * [new tag]         {ref[10:]} -> {ref[10:]}")
        if not lines and not rejected:
            out("Everything up-to-date")
            return 0
        for note in notes:
            out(note)
        out(f"To {repo.remotes[remote]}")
        for line in lines:
            out(line)
        for local, rb, why in rejected:
            out(f" ! [rejected]        {local} -> {rb} ({why})", "red")
        if set_up:
            for local, rb in refs:
                if (local, rb) not in [(a, b) for a, b, _ in rejected] and f"refs/heads/{local}" in repo.refs:
                    out(f"branch '{local}' set up to track '{remote}/{rb}'.")
        if rejected:
            out(f"error: failed to push some refs to '{repo.remotes[remote]}'", "red")
            if rejected[0][2] == "fetch first":
                out("hint: Updates were rejected because the remote contains work that you do not\n"
                    "hint: have locally. This is usually caused by another repository pushing to\n"
                    "hint: the same ref. If you want to integrate the remote changes, use\n"
                    "hint: 'git pull' before pushing again.\n"
                    "hint: See the 'Note about fast-forwards' in 'git push --help' for details.", "yellow")
            else:
                out("hint: Updates were rejected because the tip of your current branch is behind\n"
                    "hint: its remote counterpart. If you want to integrate the remote changes,\n"
                    "hint: use 'git pull' before pushing again.\n"
                    "hint: See the 'Note about fast-forwards' in 'git push --help' for details.", "yellow")
            return 1
        return 0

    def git_pull(self, args, out):
        repo = self.need_repo()
        if repo.detached or repo.branch not in repo.upstream:
            names = [a for a in args if not a.startswith("-")]
            if len(names) < 2:
                raise GitError("There is no tracking information for the current branch.\n"
                               "Please specify which branch you want to merge with.\n"
                               "See git-pull(1) for details.\n\n    git pull <remote> <branch>\n\n"
                               "If you wish to set tracking information for this branch you can do so with:\n\n"
                               f"    git branch --set-upstream-to=origin/<branch> {repo.branch}\n", 1)
            remote, rbranch = names[0], names[1]
        else:
            remote, rbranch = repo.upstream[repo.branch]
        self._fetch(repo, remote, out)
        ref = f"refs/remotes/{remote}/{rbranch}"
        if ref not in repo.refs:
            raise GitError(f"fatal: couldn't find remote ref {rbranch}", 1)
        other = repo.refs[ref]
        head = repo.head_sha()
        if other in self.reachable(repo, head):
            out("Already up to date.")
            return 0
        rebase = "--rebase" in args or self.config_get(repo, "pull.rebase") == "true"
        merge_ok = "--no-rebase" in args or self.config_get(repo, "pull.rebase") == "false" \
            or "--ff-only" in args or self.config_get(repo, "pull.ff") == "only"
        ff = head is None or head in self.reachable(repo, other)
        if not ff and not rebase and not merge_ok:
            out("hint: You have divergent branches and need to specify how to reconcile them.\n"
                "hint: You can do so by running one of the following commands sometime before\n"
                "hint: your next pull:\n"
                "hint:\n"
                "hint:   git config pull.rebase false  # merge\n"
                "hint:   git config pull.rebase true   # rebase\n"
                "hint:   git config pull.ff only       # fast-forward only\n"
                "hint:\n"
                "hint: You can replace \"git config\" with \"git config --global\" to set a default\n"
                "hint: preference for all repositories. You can also pass --rebase, --no-rebase,\n"
                "hint: or --ff-only on the command line to override the configured default per\n"
                "hint: invocation.", "yellow")
            raise GitError("fatal: Need to specify how to reconcile divergent branches.")
        if not ff and ("--ff-only" in args or self.config_get(repo, "pull.ff") == "only"):
            raise GitError("fatal: Not possible to fast-forward, aborting.")
        if rebase and not ff:
            return self._rebase(repo, other, f"{remote}/{rbranch}", out)
        url = repo.remotes[remote]
        return self._merge_into_head(repo, other, f"{remote}/{rbranch}", out,
                                     message=f"Merge branch '{rbranch}' of {url.removesuffix('.git')}",
                                     reflog_label="pull")

    # --- rebase / cherry-pick ----------------------------------------------

    def _apply_commit(self, repo: Repo, sha: str, label: str):
        """Commit'in değişikliğini HEAD'in üstüne uygula: (birleşmiş, çakışmalar)."""
        c = repo.commits[sha]
        base = self.commit_files(repo, c.parents[0]) if c.parents else {}
        return self._three_way(repo, base, self.commit_files(repo, repo.head_sha()),
                               self.commit_files(repo, sha), f"{short(sha)} ({c.message.splitlines()[0]})")

    def _rebase(self, repo: Repo, onto: str, label: str, out: Out) -> int:
        head = repo.head_sha()
        base = self.merge_base(repo, head, onto)
        mine = [s for s in self._ordered(repo, [head], None) if s not in self.reachable(repo, onto)]
        mine = [s for s in reversed(mine) if len(repo.commits[s].parents) == 1]
        if not mine or base == onto and head in self.reachable(repo, onto):
            out(f"Current branch {repo.branch} is up to date.")
            return 0
        if self._local_changes(repo):
            raise GitError("error: cannot rebase: You have unstaged changes.\n"
                           "error: Please commit or stash them.")
        branch = repo.branch
        repo.state = {"kind": "rebase", "branch": branch, "onto": onto, "todo": mine, "orig": head, "done": []}
        self._hard_to(repo, onto)
        repo.head = onto
        return self._rebase_continue(repo, out)

    def _rebase_continue(self, repo: Repo, out: Out) -> int:
        st = repo.state
        while st["todo"]:
            sha = st["todo"][0]
            c = repo.commits[sha]
            merged, conflicts = self._apply_commit(repo, sha, "")
            st.setdefault("done", []).append(sha)
            if conflicts:
                for note in self._merge_notes:
                    out(note, "red" if note.startswith("CONFLICT") else "")
                for p, v in conflicts.items():
                    self.set_worktree_file(repo, p, v[3])
                for p, b in merged.items():
                    self.set_worktree_file(repo, p, repo.blobs[b])
                repo.index = dict(merged)
                repo.conflicts = {p: v[:3] for p, v in conflicts.items()}
                first = c.message.splitlines()[0]
                out(f"error: could not apply {short(sha)}... {first}", "red")
                out("hint: Resolve all conflicts manually, mark them as resolved with\n"
                    "hint: \"git add/rm <conflicted_files>\", then run \"git rebase --continue\".\n"
                    "hint: You can instead skip this commit: run \"git rebase --skip\".\n"
                    "hint: To abort and get back to the state before \"git rebase\", run \"git rebase --abort\".\n"
                    "hint: Disable this message with \"git config set advice.mergeConflict false\"",
                    "yellow")
                out(f"Could not apply {short(sha)}... # {first}")
                return 1
            new = self.make_commit(repo, merged, [repo.head_sha()], c.message, author=(c.author, c.email))
            self._hard_to(repo, new)
            repo.head = new
            repo.reflog.insert(0, (new, f"rebase (pick): {c.message.splitlines()[0]}"))
            st["todo"].pop(0)
        final = repo.head
        repo.refs[f"refs/heads/{st['branch']}"] = final
        repo.head = f"refs/heads/{st['branch']}"
        repo.state = None
        repo.reflog.insert(0, (final, f"rebase (finish): returning to refs/heads/{st['branch']}"))
        out(f"Successfully rebased and updated refs/heads/{st['branch']}.")
        return 0

    def git_rebase(self, args, out):
        repo = self.need_repo()
        st = repo.state or {}
        if "--abort" in args:
            if st.get("kind") != "rebase":
                raise GitError("fatal: no rebase in progress")
            self._hard_to(repo, st["orig"])
            repo.head = f"refs/heads/{st['branch']}"
            repo.refs[repo.head] = st["orig"]
            repo.state = None
            return 0
        if "--continue" in args or "--skip" in args:
            if st.get("kind") != "rebase":
                raise GitError("fatal: no rebase in progress")
            if "--skip" in args:
                st["todo"].pop(0)
                self._hard_to(repo, repo.head)
                return self._rebase_continue(repo, out)
            if repo.conflicts:
                raise GitError("error: Committing is not possible because you have unmerged files.\n"
                               "hint: Fix them up in the work tree, and then use 'git add/rm <file>'\n"
                               "hint: as appropriate to mark resolution and make a commit.", 1)
            sha = st["todo"].pop(0)
            c = repo.commits[sha]
            old = self.commit_files(repo, repo.head)
            new = self.make_commit(repo, dict(repo.index), [repo.head], c.message, author=(c.author, c.email))
            self._hard_to(repo, new)
            repo.head = new
            out(f"[detached HEAD {short(new)}] {c.message.splitlines()[0]}")
            self.stat_lines(repo, old, self.commit_files(repo, new), out)
            return self._rebase_continue(repo, out)
        names = [a for a in args if not a.startswith("-")]
        if not names:
            if repo.branch in repo.upstream:
                r, b = repo.upstream[repo.branch]
                names = [f"{r}/{b}"]
            else:
                raise GitError("There is no tracking information for the current branch.\n"
                               "Please specify which branch you want to rebase against.\n"
                               "See git-rebase(1) for details.\n\n"
                               "    git rebase '<branch>'\n\n"
                               "If you wish to set tracking information for this branch you can do so with:\n\n"
                               f"    git branch --set-upstream-to=<remote>/<branch> {repo.branch}\n", 1)
        return self._rebase(repo, self.resolve(repo, names[0]), names[0], out)

    def git_cherry_pick(self, args, out):
        repo = self.need_repo()
        st = repo.state or {}
        if "--abort" in args:
            if st.get("kind") != "cherry-pick":
                raise GitError("error: no cherry-pick or revert in progress\nfatal: cherry-pick failed")
            self._hard_to(repo, repo.head_sha())
            repo.state = None
            return 0
        if "--continue" in args:
            if st.get("kind") != "cherry-pick":
                raise GitError("error: no cherry-pick or revert in progress\nfatal: cherry-pick failed")
            if repo.conflicts:
                raise GitError("error: Committing is not possible because you have unmerged files.", 1)
            c = repo.commits[st["commit"]]
            new = self.make_commit(repo, dict(repo.index), [repo.head_sha()], c.message, author=(c.author, c.email))
            repo.set_head_sha(new)
            repo.state = None
            out(f"[{repo.branch} {short(new)}] {c.message.splitlines()[0]}")
            return 0
        names = [a for a in args if not a.startswith("-")]
        if not names:
            raise GitError("usage: git cherry-pick [<options>] <commit-ish>...", 129)
        self._need_identity(repo)
        sha = self.resolve(repo, names[0])
        c = repo.commits[sha]
        merged, conflicts = self._apply_commit(repo, sha, "")
        if conflicts:
            for note in self._merge_notes:
                out(note, "red" if note.startswith("CONFLICT") else "")
            for p, v in conflicts.items():
                self.set_worktree_file(repo, p, v[3])
            repo.index = dict(merged)
            repo.conflicts = {p: v[:3] for p, v in conflicts.items()}
            repo.state = {"kind": "cherry-pick", "commit": sha}
            out(f"error: could not apply {short(sha)}... {c.message.splitlines()[0]}", "red")
            out("hint: After resolving the conflicts, mark them with\n"
                "hint: \"git add/rm <pathspec>\", then run\n"
                "hint: \"git cherry-pick --continue\".\n"
                "hint: You can instead skip this commit with \"git cherry-pick --skip\".\n"
                "hint: To abort and get back to the state before \"git cherry-pick\",\n"
                "hint: run \"git cherry-pick --abort\".", "yellow")
            return 1
        old = self.commit_files(repo, repo.head_sha())
        new = self.make_commit(repo, merged, [repo.head_sha()], c.message, author=(c.author, c.email))
        self._hard_to(repo, new)
        repo.set_head_sha(new)
        first = c.message.splitlines()[0]
        repo.reflog.insert(0, (new, f"cherry-pick: {first}"))
        out(f"[{repo.branch or 'detached HEAD'} {short(new)}] {first}")
        out(f" Date: {git_date(c.time)}")
        self.stat_lines(repo, old, merged, out)
        return 0

    # --- alıştırma: kurulum ve hedef denetimi --------------------------------

    def setup(self, steps: list) -> None:
        """Başlangıç durumu: komut satırları ya da özel adımlar (sessiz)."""
        for step in steps:
            if isinstance(step, str):
                self.run(step)
            elif step.get("fork"):
                # GitHub'daki "Fork": başkasının deposunun bütün geçmişiyle kendi hesabındaki kopyası.
                src = self.remote_repos[step["fork"]]
                copy = Repo(root=step["remote"], bare=True, head=src.head)
                self._copy_objects(src, copy)
                copy.refs = {r: v for r, v in src.refs.items() if r.startswith(("refs/heads/", "refs/tags/"))}
                self.remote_repos[step["remote"]] = copy
            elif step.get("remote"):
                if step["remote"] not in self.remote_repos:
                    self.add_remote_repo(step["remote"], step.get("branch", "main"))
                if step.get("files") is not None:
                    self.remote_commit(step["remote"], step["files"], step.get("message", "Update"),
                                       step.get("branch", "main"),
                                       tuple(step.get("author", ("Grace Hopper", "grace@example.com"))))
        self.history = []
