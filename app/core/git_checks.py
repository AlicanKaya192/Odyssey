"""Git terminal alıştırmalarının hedef denetimi.

Alıştırma (`exercise.json` → `checks`) deponun varılması gereken hâlini
tarif ediyor; her komuttan sonra benzeticinin (`git_sim.World`) durumuna
bakılıyor. Sonuç Docker ve FastAPI kontrolleri gibi `{"reason", "values"}`;
arayüz metni `check.git.<sebep>`.

`git_state` alanları (hepsi isteğe bağlı; `repo` ev klasörüne göre yol,
varsayılan ilk depo):
`exists`, `branch`, `branches`, `no_branches`, `no_remote_branches`, `commits`, `min_commits`,
`clean`, `staged`, `unstaged`, `untracked`, `tracked`, `not_tracked`,
`files`, `missing_files`, `head_files`, `last_message`, `messages`,
`merged`, `merge_commit`, `linear`, `no_conflicts`, `in_progress`, `tags`,
`annotated`, `tag_at`, `remote_tags`, `stash`, `config`, `remotes`, `upstream`, `pushed`, `tips`,
`remote_commits`, `ignored`, `detached`, `same_as`.

`git_command` kontrolü: komut geçmişinde düzenli ifadeye uyan bir satır var mı
(`git switch -c` ile mi yaptı).
"""

from __future__ import annotations

import posixpath
import re

from .git_sim import HOME, World, blob_sha


def build_world(exercise, lang: str) -> World:
    """Alıştırmanın başlangıç dünyası: kurulum adımları sessiz, sonra başlangıç klasörü.

    `"configured": false` olan alıştırmada kullanıcı adı ve e-posta ayarlı değil
    (Kurulum bölümü onları ayarlatıyor)."""
    world = World(lang, configured=bool(exercise.raw.get("configured", True)))
    world.setup(exercise.setup)
    if exercise.start_dir:
        world.run(f"cd {HOME}/{exercise.start_dir}")
        world.history = []
    return world


def hint_commands(text: str) -> list[str]:
    """Son ipucundaki ```bash bloğunun komutları (boş ve # satırları hariç)."""
    match = re.search(r"```(?:bash|shell|sh)\n(.*?)```", text, re.S)
    if not match:
        return []
    return [line for line in match.group(1).splitlines() if line.strip() and not line.lstrip().startswith("#")]


def _fail(reason: str, **values) -> dict:
    return {"passed": False, "detail": {"reason": reason, "values": values}}


def _ok() -> dict:
    return {"passed": True, "detail": {"reason": "", "values": {}}}


def _same(a: str | None, b: str) -> bool:
    return a is not None and a.rstrip("\n") == str(b).rstrip("\n")


def _repo(world: World, spec: dict):
    if spec.get("repo"):
        root = posixpath.normpath(posixpath.join(HOME, spec["repo"]))
        return world.repos.get(root), spec["repo"]
    if not world.repos:
        return None, ""
    root = sorted(world.repos)[0]
    return world.repos[root], posixpath.relpath(root, HOME)


def check_state(world: World, spec: dict) -> dict:
    repo, name = _repo(world, spec)
    if repo is None:
        return _fail("no_repo", repo=name or spec.get("repo", ""))
    if spec.get("exists") is False:
        return _fail("repo_exists", repo=name)
    ch = world.changes(repo) if not repo.bare else {"staged": [], "unstaged": [], "untracked": [], "conflicts": []}
    head = repo.head_sha()
    head_files = world.commit_files(repo, head)
    work = world.worktree(repo) if not repo.bare else {}

    if "branch" in spec and (repo.detached or repo.branch != spec["branch"]):
        return _fail("branch", expected=spec["branch"],
                     actual=f"HEAD ({head[:7]})" if repo.detached and head else repo.branch)
    for b in spec.get("branches", []):
        if f"refs/heads/{b}" not in repo.refs:
            return _fail("branch_missing", name=b)
    for b in spec.get("no_branches", []):
        if f"refs/heads/{b}" in repo.refs:
            return _fail("branch_present", name=b)
    for b in spec.get("no_remote_branches", []):
        if f"refs/remotes/{b}" in repo.refs:
            return _fail("remote_branch_present", name=b)
    if "detached" in spec and repo.detached != bool(spec["detached"]):
        return _fail("detached" if spec["detached"] else "not_detached")

    count = len(world.reachable(repo, head))
    if "commits" in spec and count != int(spec["commits"]):
        return _fail("commits", expected=int(spec["commits"]), actual=count)
    if "min_commits" in spec and count < int(spec["min_commits"]):
        return _fail("min_commits", expected=int(spec["min_commits"]), actual=count)

    if spec.get("no_conflicts") and (repo.conflicts or repo.state):
        return _fail("in_progress", kind=(repo.state or {}).get("kind", "merge"))
    if "in_progress" in spec and (repo.state or {}).get("kind") != spec["in_progress"]:
        return _fail("not_in_progress", kind=spec["in_progress"])

    staged = sorted(p.split(" -> ")[-1] for _, p in ch["staged"])
    unstaged = sorted(p for _, p in ch["unstaged"])
    if spec.get("clean") and (ch["staged"] or ch["unstaged"] or ch["untracked"] or ch["conflicts"]):
        first = (staged + unstaged + ch["untracked"] + ch["conflicts"])[0]
        return _fail("not_clean", path=first)
    if "staged" in spec and staged != sorted(spec["staged"]):
        return _fail("staged", expected=", ".join(sorted(spec["staged"])) or "—", actual=", ".join(staged) or "—")
    if "unstaged" in spec and unstaged != sorted(spec["unstaged"]):
        return _fail("unstaged", expected=", ".join(sorted(spec["unstaged"])) or "—",
                     actual=", ".join(unstaged) or "—")
    for p in spec.get("untracked", []):
        if p not in ch["untracked"]:
            return _fail("untracked", path=p)
    for p in spec.get("tracked", []):
        if p not in head_files:
            return _fail("tracked", path=p)
    for p in spec.get("not_tracked", []):
        if p in head_files or p in repo.index:
            return _fail("not_tracked", path=p)
    for p in spec.get("ignored", []):
        if not world.ignored(repo, p) or p in repo.index:
            return _fail("ignored", path=p)
    for p, text in (spec.get("files") or {}).items():
        if not _same(work.get(p), text):
            return _fail("file", path=p, expected=str(text).rstrip("\n"), actual=(work.get(p) or "—").rstrip("\n"))
    for p in spec.get("missing_files", []):
        if p in work:
            return _fail("file_present", path=p)
    for p, text in (spec.get("head_files") or {}).items():
        blob = head_files.get(p)
        if blob is None:
            return _fail("head_missing", path=p)
        if text is not None and not _same(repo.blobs.get(blob), text):
            return _fail("head_file", path=p, expected=str(text).rstrip("\n"),
                         actual=repo.blobs.get(blob, "").rstrip("\n"))

    msgs = []
    sha = head
    while sha and len(msgs) < 50:
        c = repo.commits[sha]
        msgs.append(c.message.split("\n")[0])
        sha = c.parents[0] if c.parents else None
    if "last_message" in spec:
        if not msgs or not re.search(spec["last_message"], msgs[0]):
            return _fail("last_message", expected=spec.get("show_message", spec["last_message"]),
                         actual=msgs[0] if msgs else "—")
    if "last_body" in spec:
        body = repo.commits[head].message.partition("\n")[2].strip() if head else ""
        if not re.search(spec["last_body"], body):
            return _fail("last_body", expected=spec.get("show_body", spec["last_body"]), actual=body or "—")
    if "messages" in spec:
        want = list(spec["messages"])
        if msgs[:len(want)] != want:
            return _fail("messages", expected=" / ".join(want), actual=" / ".join(msgs[:len(want)]) or "—")
    for b in spec.get("merged", []):
        tip = repo.refs.get(f"refs/heads/{b}") or repo.refs.get(f"refs/remotes/{b}")
        if tip is None or tip not in world.reachable(repo, head):
            return _fail("not_merged", name=b)
    if spec.get("merge_commit") and (not head or len(repo.commits[head].parents) < 2):
        return _fail("no_merge_commit")
    if spec.get("linear"):
        if any(len(repo.commits[s].parents) > 1 for s in world.reachable(repo, head)):
            return _fail("not_linear")

    for b, pattern in (spec.get("tips") or {}).items():
        tip = repo.refs.get(f"refs/heads/{b}")
        if tip is None:
            return _fail("branch_missing", name=b)
        msg = repo.commits[tip].message.split("\n")[0]
        if not re.search(pattern, msg):
            return _fail("tip", name=b, expected=pattern.strip("^$"), actual=msg)
    for t in spec.get("tags", []):
        if f"refs/tags/{t}" not in repo.refs:
            return _fail("tag_missing", name=t)
    for t, pattern in (spec.get("tag_at") or {}).items():
        obj = repo.refs.get(f"refs/tags/{t}")
        if obj is None:
            return _fail("tag_missing", name=t)
        msg = repo.commits[world.peel(repo, obj)].message.split("\n")[0]
        if not re.search(pattern, msg):
            return _fail("tag_at", name=t, expected=pattern.strip("^$"), actual=msg)
    rt = spec.get("remote_tags")
    if rt:
        remote = world.lookup_remote(rt["url"])
        for t in rt.get("tags", []):
            if remote is None or f"refs/tags/{t}" not in remote.refs:
                return _fail("remote_tag_missing", name=t)
    for t in spec.get("annotated", []):
        if repo.refs.get(f"refs/tags/{t}") not in repo.tag_objects:
            return _fail("tag_not_annotated", name=t)
    if "stash" in spec and len(repo.stash) != int(spec["stash"]):
        return _fail("stash", expected=int(spec["stash"]), actual=len(repo.stash))
    for key, value in (spec.get("config") or {}).items():
        got = world.config_get(repo, key)
        if got != value:
            return _fail("config", key=key, expected=value, actual=got or "—")
    for rname, url in (spec.get("remotes") or {}).items():
        if repo.remotes.get(rname) != url:
            return _fail("remote", name=rname, expected=url, actual=repo.remotes.get(rname) or "—")
    for b, up in (spec.get("upstream") or {}).items():
        got = repo.upstream.get(b)
        if got is None or f"{got[0]}/{got[1]}" != up:
            return _fail("upstream", branch=b, expected=up, actual=f"{got[0]}/{got[1]}" if got else "—")
    pushed = spec.get("pushed")
    if pushed:
        branches = pushed if isinstance(pushed, list) else [repo.branch]
        for b in branches:
            local = repo.refs.get(f"refs/heads/{b}")
            up = repo.upstream.get(b, ("origin", b))
            remote = world._remote_of(repo, up[0]) if up[0] in repo.remotes else None
            if remote is None or remote.refs.get(f"refs/heads/{up[1]}") != local:
                return _fail("not_pushed", branch=b)
    rc = spec.get("remote_commits")
    if rc:
        remote = world.lookup_remote(rc["url"])
        n = len(world.reachable(remote, remote.refs.get(f"refs/heads/{rc.get('branch', 'main')}"))) if remote else 0
        if n != int(rc["count"]):
            return _fail("remote_commits", expected=int(rc["count"]), actual=n)
    if "same_as" in spec:
        try:
            other = world.resolve(repo, spec["same_as"])
        except Exception:  # noqa: BLE001 - bulunamayan revizyon: tutmadı
            other = None
        if other != head:
            return _fail("same_as", rev=spec["same_as"])
    if spec.get("blob_of"):
        for p, text in spec["blob_of"].items():
            if repo.index.get(p) != blob_sha(text):
                return _fail("index_file", path=p)
    return _ok()


def check_shell(world: World, spec: dict) -> dict:
    """Depo istemeyen kabuk durumu (terminalin ilk adımları): klasör, dosya, konum.

    Yollar ev klasörüne göre. `files` değeri `None` ise yalnızca varlığına bakılıyor.
    """
    def yol(p: str) -> str:
        return posixpath.normpath(posixpath.join(HOME, p)) if p else HOME

    for d in spec.get("dirs", []):
        if yol(d) not in world.dirs:
            return _fail("dir_missing", path=d)
    for p, text in (spec.get("files") or {}).items():
        got = world.files.get(yol(p))
        if got is None:
            return _fail("file_missing", path=p)
        if text is not None and not _same(got, text):
            return _fail("file", path=p, expected=str(text).rstrip("\n"), actual=got.rstrip("\n"))
    for p in spec.get("missing", []):
        if yol(p) in world.files or yol(p) in world.dirs:
            return _fail("file_present", path=p)
    if "cwd" in spec and world.cwd != yol(spec["cwd"]):
        return _fail("cwd", expected=world.display(yol(spec["cwd"])), actual=world.display(world.cwd))
    return _ok()


def check_config(world: World, spec: dict) -> dict:
    """Ayar düzeyleri ayrı ayrı: `global` (~/.gitconfig) ve `local` (`repo`'nun .git/config'i).

    Değer `null` ise o anahtarın o düzeyde **olmaması** bekleniyor.
    """
    for key, value in (spec.get("global") or {}).items():
        got = world.global_config.get(key.lower())
        if got != value:
            return _fail("config_global", key=key, expected=value if value is not None else "—", actual=got or "—")
    if spec.get("local"):
        repo, name = _repo(world, spec)
        if repo is None:
            return _fail("no_repo", repo=name or spec.get("repo", ""))
        for key, value in spec["local"].items():
            got = repo.config.get(key.lower())
            if got != value:
                return _fail("config_local", key=key, expected=value if value is not None else "—", actual=got or "—")
    return _ok()


def check_command(world: World, spec: dict) -> dict:
    pattern = re.compile(spec["pattern"])
    if any(pattern.search(line) for line in world.history):
        return _ok()
    return _fail("command_missing", command=spec.get("show", spec["pattern"]))


def evaluate(world: World, checks: list[dict]) -> list[dict]:
    """Her kontrol için {type, passed, detail, hint, label}."""
    results = []
    for check in checks:
        kind = check.get("type")
        if kind == "git_state":
            outcome = check_state(world, check)
        elif kind == "git_command":
            outcome = check_command(world, check)
        elif kind == "shell_state":
            outcome = check_shell(world, check)
        elif kind == "git_config":
            outcome = check_config(world, check)
        else:
            outcome = _fail("unknown_type", type=str(kind))
        results.append({"type": kind, "passed": outcome["passed"],
                        "detail": outcome["detail"], "hint": check.get("hint", {}),
                        "label": check.get("label", {})})
    return results
