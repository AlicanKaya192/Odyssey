"""Kabuk benzeticisi: Komut Satırı patikasının ve Git patikasının terminali.

`git_sim.World` bu sınıftan türüyor; dosya sistemi (`files`, `dirs`, `cwd`)
ikisinin ortak durumu. Burada bash'in küçük ama gerçekçi bir kopyası var:

- satır çözümleme: tırnaklar, `\\`, `$AD`, `${AD}`, `$1`, `$?`, `$(komut)`,
  `$((işlem))`, `~`, joker karakterler (`*`, `?`, `[...]`), süslü parantez
  (`{a,b}`, `{1..3}`);
- boru `|`, yönlendirme `>`, `>>`, `<`, `2>`, `2>&1`, `&>`, `/dev/null`;
- `&&`, `||`, `;`, `!`, `if`, `for`, `while`, `until`, `{ }`, `( )`,
  fonksiyon, betik (`#!/bin/bash`, `./betik.sh`, `bash betik.sh`, `$1`);
- komutlar: ls cat head tail wc grep sort uniq cut tr find cp mv rm rmdir
  mkdir touch chmod echo printf test whoami id env printenv export ...

Çıktılar Git Bash'teki (GNU coreutils) metinlerle karşılaştırıldı:
`Plan/araclar/kabuk_testi.py`. Windows'un gösteremediği yerler (izinler,
sahip, tarih, `whoami`) Linux'taki gibi; o farklar testte gerekçesiyle yazılı.

Kişinin bilgisayarına dokunulmuyor: her şey bellekte, saf Python.
"""

from __future__ import annotations

import ast as pyast
import fnmatch
import posixpath
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

HOME = "/home/ada"
USER = "ada"
SHELL_TZ = timezone(timedelta(hours=3))
DEFAULT_PATH = "/usr/local/bin:/usr/bin:/bin"
# Terminal genişliği: `ls` sütunları bu genişliğe göre diziliyor.
LINE_WIDTH = 80
# Kaçak döngüye karşı bir satırda en fazla bu kadar komut çalışıyor.
MAX_STEPS = 20000
MAX_DEPTH = 60
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTHS_LONG = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
               "October", "November", "December"]
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DAYS_LONG = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Linux kipi (Komut Satırı patikası): kökte sistem klasörleri, sahibi root.
SYSTEM_DIRS = ["/bin", "/etc", "/root", "/tmp", "/usr", "/usr/bin", "/usr/local", "/usr/local/bin", "/var", "/var/log"]
SYSTEM_FILES = {
    "/etc/passwd": "root:x:0:0:root:/root:/bin/bash\n"
                   "daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\n"
                   "ada:x:1000:1000:Ada Lovelace:/home/ada:/bin/bash\n",
    "/etc/hostname": "odyssey\n",
    "/etc/shells": "/bin/sh\n/bin/bash\n",
}
# Ev klasöründe hazır duran gizli ayar dosyası (gerçek Linux'taki gibi; `ls -a` gösterir).
BASHRC = ("# ~/.bashrc: bash reads this file when a new terminal opens.\n"
          "# Aliases and settings written here last for every session.\n")

RESERVED = {"if", "then", "elif", "else", "fi", "for", "in", "do", "done", "while", "until", "{", "}", "!",
            "case", "esac", "function", "select", "time", "[["}
BUILTINS = {"cd", "pwd", "echo", "printf", "export", "unset", "exit", "return", "break", "continue", "true",
            "false", ":", "test", "[", "[[", "source", ".", "type", "alias", "unalias", "read", "shift",
            "history", "local", "kill", "jobs", "bg", "fg", "wait", "help", "set", "eval", "exec", "let"}
# Benzeticinin /usr/bin'de duran programları.
EXTERNAL = {"ls", "cat", "head", "tail", "wc", "grep", "sort", "uniq", "cut", "tr", "find", "cp", "mv", "rm",
            "rmdir", "mkdir", "touch", "chmod", "whoami", "id", "groups", "env", "printenv", "seq",
            "basename", "dirname", "clear", "sleep", "date", "which", "bash", "sh", "git"}
EDITORS = {"nano", "vim", "vi", "code", "notepad", "emacs", "gedit", "pico"}
PAGERS = {"less", "more", "most"}
PROCESS_TOOLS = {"ps", "top", "htop", "pkill", "killall", "nohup", "pgrep"}
NETWORK_TOOLS = {"ssh", "scp", "sftp", "curl", "wget", "ping", "rsync", "ftp", "telnet"}
ADMIN_TOOLS = {"sudo", "su", "apt", "apt-get", "dnf", "yum", "pacman", "brew", "snap", "choco", "winget",
               "pip", "pip3", "npm"}
OTHER_PROGRAMS = {"python", "python3", "py", "node", "java", "gcc", "make", "awk", "sed", "xargs", "tree",
                  "du", "df", "stat", "file", "ln", "tee", "diff", "zip", "unzip", "tar", "gzip", "man",
                  "info", "watch", "crontab", "systemctl", "service", "chown", "chgrp", "umask"}

SHELL_TEXT = {
    "tr": {
        "needs_input": "odyssey: {cmd} klavyeden girdi bekliyor; bu terminal klavye girdisi veremiyor."
                       " Bir dosya ver ({cmd} notes.txt) ya da boruyla gönder (cat notes.txt | {cmd}).",
        "incomplete": "odyssey: Komut tamamlanmadı ('{word}' eksik). Bu terminalde komutun tamamını tek"
                      " satıra yaz, örneğin: if [ -f a.txt ]; then echo var; fi",
        "heredoc": "odyssey: '<<' (heredoc) bu terminalde yok; dosyayı echo ve >> ile satır satır yaz.",
        "background": "odyssey: Arka plan işleri (&) bu terminalde yok; komutu & olmadan çalıştır."
                      " Süreçler derste anlatılıyor.",
        "process": "odyssey: '{cmd}' süreçlerle çalışır; bu benzeticide gerçek süreç yok."
                   " Derstekine bakabilirsin.",
        "network": "odyssey: '{cmd}' başka bir bilgisayara ya da internete bağlanır; bu terminal bilgisayarının"
                   " dışına çıkmaz.",
        "admin": "odyssey: '{cmd}' program kurar ya da yönetici izni ister; bu terminalde yok."
                 " Paket yöneticileri derste anlatılıyor.",
        "pager": "odyssey: {cmd} tam ekran çalışır; burada cat, head ya da tail kullan.",
        "program": "odyssey: '{cmd}' bu benzeticide yok.",
        "exit_top": "odyssey: Bu terminal kapanmaz; exit betiklerin içinde işe yarar.",
        "new_shell": "odyssey: Bu terminalde yeni bir kabuk açılmıyor; betiği bash betik.sh ile çalıştır.",
        "interpreter": "odyssey: Bu terminal yalnızca bash betiklerini çalıştırır (ilk satır: {line}).",
        "too_many": "odyssey: Komut çok uzun sürdü ve durduruldu (bitmeyen bir döngü olabilir).",
        "eval": "odyssey: '{cmd}' bu benzeticide yok.",
        "rm_ask": "odyssey: rm -i her dosya için 'silinsin mi?' diye sorar ve cevabı klavyeden bekler;"
                  " bu terminal cevap veremediği için hiçbir şey silinmedi.",
    },
    "en": {
        "needs_input": "odyssey: {cmd} is waiting for keyboard input, which this terminal cannot give."
                       " Give it a file ({cmd} notes.txt) or send it through a pipe (cat notes.txt | {cmd}).",
        "incomplete": "odyssey: The command is not finished ('{word}' is missing). In this terminal write the"
                      " whole command on one line, for example: if [ -f a.txt ]; then echo yes; fi",
        "heredoc": "odyssey: '<<' (heredoc) is not available in this terminal; write the file line by line"
                   " with echo and >>.",
        "background": "odyssey: Background jobs (&) are not available in this terminal; run the command"
                      " without &. Processes are explained in the lesson.",
        "process": "odyssey: '{cmd}' works with processes; this simulator has no real processes."
                   " See the lesson.",
        "network": "odyssey: '{cmd}' connects to another computer or the internet; this terminal never leaves"
                   " your computer.",
        "admin": "odyssey: '{cmd}' installs programs or needs administrator rights; not available here."
                 " Package managers are explained in the lesson.",
        "pager": "odyssey: {cmd} needs a full screen; use cat, head or tail here.",
        "program": "odyssey: '{cmd}' is not available in this simulator.",
        "exit_top": "odyssey: This terminal stays open; exit is useful inside scripts.",
        "new_shell": "odyssey: No new shell opens in this terminal; run the script with bash script.sh.",
        "interpreter": "odyssey: This terminal only runs bash scripts (first line: {line}).",
        "too_many": "odyssey: The command took too long and was stopped (maybe a loop that never ends).",
        "eval": "odyssey: '{cmd}' is not available in this simulator.",
        "rm_ask": "odyssey: rm -i asks 'remove?' for every file and waits for an answer from the keyboard;"
                  " this terminal cannot answer, so nothing was deleted.",
    },
}


# --- hatalar ve denetim akışı ----------------------------------------------

class ShellSyntax(Exception):
    """Satır çözümlenemedi: `kind` quote / incomplete / token / heredoc."""

    def __init__(self, kind: str, token: str = "", line: int = 1) -> None:
        super().__init__(kind)
        self.kind = kind
        self.token = token
        self.line = line


class CmdError(Exception):
    """Komutun kendi hata metni (stderr) ve çıkış kodu."""

    def __init__(self, text: str, code: int = 1) -> None:
        super().__init__(text)
        self.text = text
        self.code = code


class _Exit(Exception):
    def __init__(self, code: int) -> None:
        super().__init__(code)
        self.code = code


class _Return(_Exit):
    pass


class _Loop(Exception):
    def __init__(self, kind: str, n: int) -> None:
        super().__init__(kind)
        self.kind = kind
        self.n = n


class _Abort(Exception):
    pass


# --- akışlar ----------------------------------------------------------------

class Stream:
    """Komutun girdisi (boru ya da `<` dosyası)."""

    def __init__(self, text: str = "") -> None:
        self.text = text
        self.pos = 0

    def read_all(self) -> str:
        rest = self.text[self.pos:]
        self.pos = len(self.text)
        return rest

    def read_line(self) -> str | None:
        if self.pos >= len(self.text):
            return None
        end = self.text.find("\n", self.pos)
        if end < 0:
            line, self.pos = self.text[self.pos:], len(self.text)
        else:
            line, self.pos = self.text[self.pos:end], end + 1
        return line


class Sink:
    """Çıktı: (metin, renk, stderr mi) parçaları; metin satır sonlarını taşıyor."""

    def __init__(self, tty: bool = False) -> None:
        self.chunks: list[tuple[str, str, bool]] = []
        self.tty = tty

    def write(self, text: str, color: str = "") -> None:
        if text:
            self.chunks.append((text, color, False))

    def err(self, text: str, color: str = "red") -> None:
        if not text.endswith("\n"):
            text += "\n"
        self.chunks.append((text, color, True))

    def text(self) -> str:
        return "".join(c[0] for c in self.chunks)

    def stdout_text(self) -> str:
        return "".join(c[0] for c in self.chunks if not c[2])


class NullSink(Sink):
    def write(self, text: str, color: str = "") -> None:
        pass

    def err(self, text: str, color: str = "red") -> None:
        pass


class FileSink(Sink):
    """`> dosya`: komut bitince dosyaya yazılıyor (dosya açılışta boşaltıldı)."""

    def __init__(self, world: "Shell", path: str) -> None:
        super().__init__()
        self.world = world
        self.path = path

    def flush(self) -> None:
        if self.chunks:
            self.world._put(self.path, self.world.files.get(self.path, "") + self.text())
            self.chunks = []


@dataclass
class IO:
    stdin: Stream | None
    out: Sink
    err: Sink


def chunks_to_lines(chunks: list[tuple[str, str, bool]]) -> list[tuple[str, str]]:
    """Terminalde görünen satırlar (git_sim.Out biçimi): her satır ilk parçasının renginde."""
    lines: list[tuple[str, str]] = []
    cur, color = "", None
    for text, c, _ in chunks:
        parts = text.split("\n")
        for k, part in enumerate(parts):
            if color is None and (part or k < len(parts) - 1):
                color = c
            cur += part
            if k < len(parts) - 1:
                lines.append((cur, color or ""))
                cur, color = "", None
    if cur:
        lines.append((cur, color or ""))
    return lines


# --- sözdizimi ağacı ----------------------------------------------------------

@dataclass
class Tok:
    kind: str  # W (kelime), OP, IO
    value: object
    line: int = 1


@dataclass
class Redir:
    fd: int  # 0, 1, 2; -1 = ikisi birden (&>)
    op: str  # >, >>, <, >&
    target: str


@dataclass
class Simple:
    assigns: list[str]
    words: list[str]
    redirs: list[Redir]
    line: int = 1


@dataclass
class Pipeline:
    cmds: list
    negate: bool = False


@dataclass
class AndOr:
    first: object
    rest: list  # [(op, Pipeline)]


@dataclass
class Seq:
    items: list  # [(node, arka planda mı)]


@dataclass
class If:
    branches: list  # [(koşul Seq, gövde Seq)]
    orelse: object = None
    redirs: list = field(default_factory=list)


@dataclass
class For:
    var: str
    words: list | None
    body: object
    redirs: list = field(default_factory=list)


@dataclass
class While:
    cond: object
    body: object
    until: bool = False
    redirs: list = field(default_factory=list)


@dataclass
class Group:
    body: object
    subshell: bool = False
    redirs: list = field(default_factory=list)


@dataclass
class FuncDef:
    name: str
    body: object


OPERATORS = ["&&", "||", ";;", "&>>", "&>", ">>", "<<<", "<<", ">&", "<&", ">|", "|&", "|", "&", ";", "<", ">",
             "(", ")"]
NAME_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
ASSIGN_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)=(.*)", re.S)


def _scan_dquote(text: str, i: int) -> int:
    """`"` ile başlayan parçanın bittiği yer (kapanış tırnağından sonra)."""
    j = i + 1
    while j < len(text):
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == '"':
            return j + 1
        if c == "$" and j + 1 < len(text) and text[j + 1] == "(":
            j = _scan_dollar(text, j)
            continue
        if c == "`":
            k = text.find("`", j + 1)
            if k < 0:
                raise ShellSyntax("quote")
            j = k + 1
            continue
        j += 1
    raise ShellSyntax("quote")


def _scan_dollar(text: str, i: int) -> int:
    """`$(`, `$((` ya da `${` ile başlayan parçanın bittiği yer."""
    if text[i + 1] == "{":
        k = text.find("}", i + 2)
        if k < 0:
            raise ShellSyntax("incomplete", "}")
        return k + 1
    depth = 0
    j = i + 1
    while j < len(text):
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "'":
            k = text.find("'", j + 1)
            if k < 0:
                raise ShellSyntax("quote")
            j = k + 1
            continue
        if c == '"':
            j = _scan_dquote(text, j)
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    raise ShellSyntax("incomplete", ")")


def lex(text: str) -> list[Tok]:
    toks: list[Tok] = []
    buf: list[str] | None = None
    line = 1
    i, n = 0, len(text)

    def flush() -> None:
        nonlocal buf
        if buf is not None:
            toks.append(Tok("W", "".join(buf), line))
            buf = None

    while i < n:
        c = text[i]
        if c in " \t\r":
            flush()
            i += 1
            continue
        if c == "\n":
            flush()
            toks.append(Tok("OP", "\n", line))
            line += 1
            i += 1
            continue
        if c == "#" and buf is None:
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "\\":
            if i + 1 < n and text[i + 1] == "\n":
                i += 2
                line += 1
                continue
            buf = (buf or []) + [text[i:i + 2]]
            i += 2
            continue
        if c == "'":
            k = text.find("'", i + 1)
            if k < 0:
                raise ShellSyntax("quote", line=line)
            buf = (buf or []) + [text[i:k + 1]]
            line += text.count("\n", i, k)
            i = k + 1
            continue
        if c == '"':
            k = _scan_dquote(text, i)
            buf = (buf or []) + [text[i:k]]
            line += text.count("\n", i, k)
            i = k
            continue
        if c == "`":
            k = text.find("`", i + 1)
            if k < 0:
                raise ShellSyntax("quote", line=line)
            buf = (buf or []) + [text[i:k + 1]]
            i = k + 1
            continue
        if c == "$" and i + 1 < n and text[i + 1] in "({":
            k = _scan_dollar(text, i)
            buf = (buf or []) + [text[i:k]]
            i = k
            continue
        if c in "|&;<>()":
            fd = None
            if c in "<>" and buf is not None and "".join(buf).isdigit() and len("".join(buf)) == 1:
                fd = int("".join(buf))
                buf = None
            else:
                flush()
            op = next(o for o in OPERATORS if text.startswith(o, i))
            i += len(op)
            if op in ("<<", "<<<"):
                raise ShellSyntax("heredoc", line=line)
            if op in (">", ">>", ">|"):
                toks.append(Tok("IO", (1 if fd is None else fd, ">>" if op == ">>" else ">"), line))
            elif op == "<":
                toks.append(Tok("IO", (0 if fd is None else fd, "<"), line))
            elif op in (">&", "<&"):
                toks.append(Tok("IO", (1 if fd is None else fd, ">&"), line))
            elif op in ("&>", "&>>"):
                toks.append(Tok("IO", (-1, ">>" if op == "&>>" else ">"), line))
            else:
                toks.append(Tok("OP", op, line))
            continue
        buf = (buf or []) + [c]
        i += 1
    flush()
    return toks


class Parser:
    def __init__(self, toks: list[Tok]) -> None:
        self.toks = toks
        self.i = 0

    def peek(self) -> Tok | None:
        return self.toks[self.i] if self.i < len(self.toks) else None

    def take(self) -> Tok:
        tok = self.toks[self.i]
        self.i += 1
        return tok

    def is_word(self, *words: str) -> bool:
        tok = self.peek()
        return tok is not None and tok.kind == "W" and tok.value in words

    def is_op(self, *ops: str) -> bool:
        tok = self.peek()
        return tok is not None and tok.kind == "OP" and tok.value in ops

    def skip_newlines(self) -> None:
        while self.is_op("\n"):
            self.i += 1

    def unexpected(self) -> ShellSyntax:
        tok = self.peek()
        if tok is None:
            return ShellSyntax("token", "newline")
        value = tok.value if tok.kind != "IO" else (">" if tok.value[1] != "<" else "<")
        return ShellSyntax("token", "newline" if value == "\n" else str(value), tok.line)

    def expect(self, word: str) -> None:
        if self.peek() is None:
            raise ShellSyntax("incomplete", word)
        if not self.is_word(word):
            raise self.unexpected()
        self.i += 1

    def parse(self) -> Seq:
        seq = self.parse_list(set())
        if self.peek() is not None:
            raise self.unexpected()
        return seq

    def parse_list(self, stops: set[str]) -> Seq:
        items = []
        self.skip_newlines()
        while True:
            tok = self.peek()
            if tok is None or (tok.kind == "W" and tok.value in stops) or self.is_op(")"):
                break
            if self.is_op(";", "&", ";;", "|", "||", "&&", "|&"):
                raise self.unexpected()
            node = self.parse_andor()
            bg = False
            if self.is_op(";", "&", "\n"):
                bg = self.take().value == "&"
            elif self.peek() is not None and not self.is_op(")") and not (
                    self.peek().kind == "W" and self.peek().value in stops):
                raise self.unexpected()
            items.append((node, bg))
            self.skip_newlines()
        return Seq(items)

    def parse_andor(self) -> object:
        first = self.parse_pipeline()
        rest = []
        while self.is_op("&&", "||"):
            op = self.take().value
            self.skip_newlines()
            if self.peek() is None:
                raise ShellSyntax("incomplete", "command")
            rest.append((op, self.parse_pipeline()))
        return AndOr(first, rest) if rest else first

    def parse_pipeline(self) -> object:
        negate = False
        if self.is_word("!"):
            self.i += 1
            negate = True
        cmds = [self.parse_command()]
        while self.is_op("|"):
            self.i += 1
            self.skip_newlines()
            if self.peek() is None:
                raise ShellSyntax("incomplete", "command")
            cmds.append(self.parse_command())
        if len(cmds) == 1 and not negate:
            return cmds[0]
        return Pipeline(cmds, negate)

    def parse_redirs(self) -> list[Redir]:
        redirs = []
        while self.peek() is not None and self.peek().kind == "IO":
            redirs.append(self.parse_redir())
        return redirs

    def parse_redir(self) -> Redir:
        fd, op = self.take().value
        tok = self.peek()
        if tok is None or tok.kind != "W":
            raise self.unexpected()
        self.i += 1
        return Redir(fd, op, tok.value)

    def parse_command(self) -> object:
        tok = self.peek()
        if tok is None:
            raise ShellSyntax("incomplete", "command")
        if tok.kind == "OP" and tok.value == "(":
            self.i += 1
            body = self.parse_list(set())
            if self.peek() is None:
                raise ShellSyntax("incomplete", ")")
            if not self.is_op(")"):
                raise self.unexpected()
            self.i += 1
            return Group(body, True, self.parse_redirs())
        if tok.kind == "W":
            word = tok.value
            if word == "if":
                return self.parse_if()
            if word in ("while", "until"):
                self.i += 1
                cond = self.parse_list({"do"})
                self.expect("do")
                body = self.parse_list({"done"})
                self.expect("done")
                return While(cond, body, word == "until", self.parse_redirs())
            if word == "for":
                return self.parse_for()
            if word == "{":
                self.i += 1
                body = self.parse_list({"}"})
                self.expect("}")
                return Group(body, False, self.parse_redirs())
            if word == "function":
                self.i += 1
                name = self.take().value if self.peek() is not None else ""
                if self.is_op("("):
                    self.i += 1
                    if not self.is_op(")"):
                        raise self.unexpected()
                    self.i += 1
                self.skip_newlines()
                return FuncDef(str(name), self.parse_command())
            if word in ("case", "select"):
                raise ShellSyntax("unsupported", word)
            if word in ("then", "elif", "else", "fi", "do", "done", "}", "esac", "in"):
                raise ShellSyntax("token", word, tok.line)
            nxt = self.toks[self.i + 1] if self.i + 1 < len(self.toks) else None
            nxt2 = self.toks[self.i + 2] if self.i + 2 < len(self.toks) else None
            if (NAME_RE.fullmatch(word) and nxt is not None and nxt.kind == "OP" and nxt.value == "("
                    and nxt2 is not None and nxt2.kind == "OP" and nxt2.value == ")"):
                self.i += 3
                self.skip_newlines()
                return FuncDef(word, self.parse_command())
        return self.parse_simple()

    def parse_simple(self) -> Simple:
        assigns, words, redirs = [], [], []
        line = self.peek().line if self.peek() else 1
        while True:
            tok = self.peek()
            if tok is None:
                break
            if tok.kind == "IO":
                redirs.append(self.parse_redir())
                continue
            if tok.kind != "W":
                break
            self.i += 1
            if not words and ASSIGN_RE.fullmatch(tok.value):
                assigns.append(tok.value)
            else:
                words.append(tok.value)
        if not assigns and not words and not redirs:
            raise self.unexpected()
        return Simple(assigns, words, redirs, line)

    def parse_if(self) -> If:
        self.i += 1
        branches = []
        cond = self.parse_list({"then"})
        self.expect("then")
        body = self.parse_list({"elif", "else", "fi"})
        branches.append((cond, body))
        orelse = None
        while True:
            if self.is_word("elif"):
                self.i += 1
                cond = self.parse_list({"then"})
                self.expect("then")
                body = self.parse_list({"elif", "else", "fi"})
                branches.append((cond, body))
                continue
            if self.is_word("else"):
                self.i += 1
                orelse = self.parse_list({"fi"})
            self.expect("fi")
            break
        return If(branches, orelse, self.parse_redirs())

    def parse_for(self) -> For:
        self.i += 1
        tok = self.peek()
        if tok is None:
            raise ShellSyntax("incomplete", "do")
        if tok.kind != "W" or not NAME_RE.fullmatch(str(tok.value)):
            raise self.unexpected()
        self.i += 1
        var = str(tok.value)
        words = None
        self.skip_newlines()
        if self.is_word("in"):
            self.i += 1
            words = []
            while self.peek() is not None and self.peek().kind == "W":
                words.append(self.take().value)
            if self.peek() is None:
                raise ShellSyntax("incomplete", "do")
            if not self.is_op(";", "\n"):
                raise self.unexpected()
            self.i += 1
        elif self.is_op(";"):
            self.i += 1
        self.skip_newlines()
        self.expect("do")
        body = self.parse_list({"done"})
        self.expect("done")
        return For(var, words, body, self.parse_redirs())


def parse(text: str) -> Seq:
    return Parser(lex(text)).parse()


# --- küçük yardımcılar ------------------------------------------------------

def _glob_escape(text: str) -> str:
    return re.sub(r"([*?\[])", r"[\1]", text)


def _has_magic(text: str) -> bool:
    return any(ch in text for ch in "*?[")


def human_size(n: int) -> str:
    """`ls -h` biçimi (GNU: 1024'ün kuvvetleri, yukarı yuvarlama, 10'dan küçükse bir ondalık)."""
    if n < 1024:
        return str(n)
    value = float(n)
    for unit in "KMGTPE":
        value /= 1024
        if value < 1024 or unit == "E":
            if value < 10:
                tenths = int(-(-value * 10 // 1))  # yukarı yuvarlama
                if tenths >= 100:
                    return f"10{unit}"
                return f"{tenths // 10}.{tenths % 10}{unit}"
            return f"{int(-(-value // 1))}{unit}"
    return str(n)


def _c_escapes(text: str) -> str:
    """printf / echo -e kaçışları."""
    table = {"n": "\n", "t": "\t", "\\": "\\", "a": "\a", "r": "\r", "b": "\b", "f": "\f", "v": "\v",
             '"': '"', "'": "'", "e": "\x1b", "0": "\0"}
    out = []
    i = 0
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text) and text[i + 1] in table:
            out.append(table[text[i + 1]])
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _bre_to_py(pattern: str, extended: bool) -> str:
    """grep'in temel (BRE) ya da genişletilmiş (ERE) düzenli ifadesi → Python."""
    out = []
    i = 0
    n = len(pattern)
    classes = {"digit": "0-9", "alpha": "a-zA-Z", "upper": "A-Z", "lower": "a-z", "alnum": "a-zA-Z0-9",
               "space": r" \t\n\r\f\v", "blank": r" \t", "punct": r"!-/:-@\[-`{-~", "xdigit": "0-9A-Fa-f"}
    while i < n:
        c = pattern[i]
        if c == "\\" and i + 1 < n:
            nx = pattern[i + 1]
            if not extended and nx in "(){}|+?":
                out.append(nx)
            elif nx in "<>":
                out.append(r"\b")
            else:
                out.append("\\" + nx)
            i += 2
            continue
        if c == "[":
            j = i + 1
            if j < n and pattern[j] == "^":
                j += 1
            if j < n and pattern[j] == "]":
                j += 1
            while j < n and pattern[j] != "]":
                if pattern.startswith("[:", j):
                    k = pattern.find(":]", j)
                    j = k + 2 if k > 0 else j + 1
                else:
                    j += 1
            if j >= n:
                raise CmdError("grep: Unmatched [, [^, [:, [., or [=", 2)
            body = pattern[i + 1:j]
            neg = body.startswith("^")
            if neg:
                body = body[1:]
            body = re.sub(r"\[:(\w+):\]", lambda m: classes.get(m.group(1), ""), body.replace("\\", "\\\\"))
            out.append("[" + ("^" if neg else "") + body.replace("[", "\\[") + "]")
            i = j + 1
            continue
        if not extended and c in "+?(){}|":
            out.append("\\" + c)
        elif c == "*" and (not out or out[-1] in ("^", "(", "|")):
            out.append(r"\*")
        else:
            out.append(c)
        i += 1
    return "".join(out)


def _tr_set(spec: str) -> list[str]:
    """tr kümesi: kaçışlar, a-z aralıkları ve [:lower:] gibi sınıflar."""
    classes = {
        "lower": [chr(c) for c in range(ord("a"), ord("z") + 1)],
        "upper": [chr(c) for c in range(ord("A"), ord("Z") + 1)],
        "digit": [chr(c) for c in range(ord("0"), ord("9") + 1)],
        "space": list(" \t\n\r\f\v"), "blank": [" ", "\t"],
        "punct": [chr(c) for c in range(33, 127) if not chr(c).isalnum()],
    }
    classes["alpha"] = classes["upper"] + classes["lower"]
    classes["alnum"] = classes["digit"] + classes["upper"] + classes["lower"]
    chars: list[str] = []
    i = 0
    text = spec
    while i < len(text):
        m = re.match(r"\[:(\w+):\]", text[i:])
        if m and m.group(1) in classes:
            chars.extend(classes[m.group(1)])
            i += m.end()
            continue
        c = text[i]
        if c == "\\" and i + 1 < len(text):
            c = _c_escapes(text[i:i + 2]) if text[i + 1] in "ntr\\" else text[i + 1]
            i += 2
        else:
            i += 1
        if i + 1 < len(text) and text[i] == "-":
            end = text[i + 1]
            i += 2
            chars.extend(chr(x) for x in range(ord(c), ord(end) + 1))
            continue
        chars.append(c)
    return chars


def _cut_list(spec: str) -> list[tuple[int, int]] | None:
    ranges = []
    for part in spec.split(","):
        m = re.fullmatch(r"(\d*)-(\d*)|(\d+)", part.strip())
        if not m or part.strip() in ("-", ""):
            return None
        if m.group(3):
            a = b = int(m.group(3))
        else:
            a = int(m.group(1)) if m.group(1) else 1
            b = int(m.group(2)) if m.group(2) else 10 ** 9
        if a < 1:
            return None
        ranges.append((a, b))
    return ranges


def _in_ranges(k: int, ranges: list[tuple[int, int]]) -> bool:
    return any(a <= k <= b for a, b in ranges)


# --- kabuk ------------------------------------------------------------------

class Shell:
    """Kabuğun kendisi; `git_sim.World` bundan türüyor (files, dirs, cwd orada kuruluyor)."""

    files: dict[str, str]
    dirs: set[str]
    cwd: str
    history: list[str]

    def _shell_init(self, linux: bool) -> None:
        self.linux = linux
        self.modes: dict[str, int] = {}
        self.owners: dict[str, str] = {}
        self.mtimes: dict[str, int] = {}
        self.vars: dict[str, str] = {
            "HOME": HOME, "USER": USER, "LOGNAME": USER, "SHELL": "/bin/bash", "PATH": DEFAULT_PATH,
            "PWD": HOME, "LANG": "en_US.UTF-8", "TERM": "xterm-256color",
        }
        self.exported: set[str] = set(self.vars)
        self.params: list[str] = []
        self.script_name = "bash"
        self.functions: dict[str, object] = {}
        self.aliases: dict[str, str] = {}
        self.hashed: set[str] = set()
        self.last_status = 0
        self.outputs: list[tuple[str, str]] = []
        self._script: str | None = None
        self._lineno = 1
        self._loops = 0
        self._fdepth = 0
        self._locals: list[dict] = []
        self._steps = 0
        self._err_sink: Sink = Sink()
        if linux:
            for d in SYSTEM_DIRS:
                self.dirs.add(d)
                self.owners[d] = "root"
            for d in ("/", "/home"):
                self.owners[d] = "root"
            self.modes["/tmp"] = 0o1777
            self.modes["/root"] = 0o700
            for p, text in SYSTEM_FILES.items():
                self.files[p] = text
                self.owners[p] = "root"
            self.files[HOME + "/.bashrc"] = BASHRC

    # --- metin ve dosya yardımcıları --------------------------------------

    def st(self, key: str, **kw) -> str:
        lang = getattr(self, "lang", "en")
        return SHELL_TEXT.get(lang, SHELL_TEXT["en"])[key].format(**kw)

    def _prefix(self) -> str:
        """bash'in kendi hatalarının öneki: etkileşimde `bash`, betikte `betik.sh: line N`."""
        if self._script is not None:
            return f"{self._script}: line {self._lineno}"
        return "bash"

    def _now(self) -> int:
        return getattr(self, "_time", 0)

    def _is_gitdir(self, p: str) -> bool:
        return p.endswith("/.git") and p[:-5] in getattr(self, "repos", {})

    def _isdir(self, p: str) -> bool:
        return p in self.dirs or self._is_gitdir(p)

    def _exists(self, p: str) -> bool:
        return p in self.files or self._isdir(p)

    def _mode(self, p: str) -> int:
        if p in self.modes:
            return self.modes[p]
        return 0o755 if self._isdir(p) else 0o644

    def _owner(self, p: str) -> str:
        return self.owners.get(p, USER)

    def _can(self, p: str, perm: str) -> bool:
        mode = self._mode(p)
        bits = (mode >> 6) & 7 if self._owner(p) == USER else mode & 7
        return bool(bits & {"r": 4, "w": 2, "x": 1}[perm])

    def _children(self, d: str) -> list[str]:
        pref = d.rstrip("/") + "/"
        names = set()
        for p in list(self.files) + list(self.dirs):
            if p.startswith(pref) and p != d:
                names.add(p[len(pref):].split("/")[0])
        return sorted(names)

    def _entries(self, d: str) -> list[str]:
        """Klasördeki adlar (deponun gizli `.git` klasörü dahil), C sırasıyla."""
        names = set(self._children(d))
        if d in getattr(self, "repos", {}):
            names.add(".git")
        return sorted(names)

    def _put(self, p: str, text: str) -> None:
        self.write_file(p, text)  # git_sim.World: üst klasörleri de açıyor
        self.mtimes[p] = self._now()

    def _write_check(self, p: str, shown: str) -> str | None:
        """Bu yola yazılabilir mi; değilse sebep (No such file or directory, Is a directory...)."""
        parent = posixpath.dirname(p)
        if self._isdir(p):
            return "Is a directory"
        if parent not in self.dirs:
            return "Not a directory" if parent in self.files else "No such file or directory"
        if p in self.files and not self._can(p, "w"):
            return "Permission denied"
        if p not in self.files and not self._can(parent, "w"):
            return "Permission denied"
        return None

    def _read_text(self, cmd: str, name: str, style: str = "plain") -> str:
        """Dosyayı okur; okuyamazsa komutun kendi biçiminde CmdError."""
        if name == "/dev/null":
            return ""
        p = self.abspath(name)
        reason = None
        if self._isdir(p):
            reason = "Is a directory"
        elif p not in self.files:
            reason = "No such file or directory"
        elif not self._can(p, "r"):
            reason = "Permission denied"
        if reason is None:
            return self.files[p]
        if style == "open":
            if reason == "Is a directory":
                raise CmdError(f"{cmd}: error reading '{name}': Is a directory")
            raise CmdError(f"{cmd}: cannot open '{name}' for reading: {reason}")
        if style == "sort":
            if reason == "Is a directory":
                raise CmdError(f"sort: read failed: {name}: Is a directory", 2)
            raise CmdError(f"sort: cannot read: {name}: {reason}", 2)
        raise CmdError(f"{cmd}: {name}: {reason}")

    def _remove_path(self, p: str) -> None:
        """Dosyayı ya da klasörü (içindekilerle, içindeki depolarla) siler."""
        if p in self.files:
            del self.files[p]
            self.modes.pop(p, None)
            return
        pref = p.rstrip("/") + "/"
        for f in [f for f in self.files if f.startswith(pref)]:
            del self.files[f]
            self.modes.pop(f, None)
        for d in [d for d in self.dirs if d == p or d.startswith(pref)]:
            self.dirs.discard(d)
            self.modes.pop(d, None)
        repos = getattr(self, "repos", {})
        for r in [r for r in repos if r == p or r.startswith(pref)]:
            del repos[r]

    def _move_path(self, src: str, dst: str) -> None:
        if src in self.files:
            self._put(dst, self.files.pop(src))
            if src in self.modes:
                self.modes[dst] = self.modes.pop(src)
            return
        pref = src.rstrip("/") + "/"

        def moved(path: str) -> str:
            return dst + path[len(src):]
        for f in [f for f in self.files if f.startswith(pref)]:
            self.files[moved(f)] = self.files.pop(f)
        for table in (self.modes, self.mtimes):
            for k in [k for k in table if k == src or k.startswith(pref)]:
                table[moved(k)] = table.pop(k)
        for d in [d for d in self.dirs if d == src or d.startswith(pref)]:
            self.dirs.discard(d)
            self.dirs.add(moved(d))
        repos = getattr(self, "repos", {})
        for r in [r for r in repos if r == src or r.startswith(pref)]:
            repo = repos.pop(r)
            repo.root = moved(r)
            repos[repo.root] = repo

    # --- satır çalıştırma ---------------------------------------------------

    def run(self, line: str):
        """Bir satırı çalıştırır: (çıktı, çıkış kodu). Satır geçmişe yazılıyor."""
        from .git_sim import Out

        out = Out()
        line = line.strip()
        if not line or line.startswith("#"):
            return out, 0
        self.history.append(line)
        sink = Sink(tty=True)
        self._steps = 0
        try:
            tree = parse(line)
        except ShellSyntax as exc:
            text, color = self._syntax_text(exc)
            sink.err(text, color)
            code = 2
        else:
            code = self._run_top(tree, IO(None, sink, sink))
        out.lines.extend(chunks_to_lines(sink.chunks))
        self.last_status = code
        self.outputs.append((line, sink.stdout_text()))
        return out, code

    def _syntax_text(self, exc: ShellSyntax, where: str = "bash") -> tuple[str, str]:
        if exc.kind == "quote":
            return f"{where}: syntax error: unexpected end of file (a quote is not closed)", "red"
        if exc.kind == "incomplete":
            return self.st("incomplete", word=exc.token), "yellow"
        if exc.kind == "heredoc":
            return self.st("heredoc"), "yellow"
        if exc.kind == "unsupported":
            return self.t("unsupported", what=exc.token), "yellow"
        return f"{where}: syntax error near unexpected token `{exc.token}'", "red"

    def _run_top(self, tree, io: IO) -> int:
        try:
            return self._exec(tree, io)
        except _Return as exc:
            return exc.code
        except _Exit as exc:
            io.err.err(self.st("exit_top"), "yellow")
            return exc.code
        except _Abort:
            io.err.err(self.st("too_many"), "yellow")
            return 130

    def _capture(self, text: str) -> str:
        """`$(komut)`: alt kabukta çalıştırıp çıktısını verir (sondaki satır sonları atılıyor)."""
        try:
            tree = parse(text)
        except ShellSyntax as exc:
            self._err_sink.err(self._syntax_text(exc)[0])
            return ""
        sink = Sink()
        saved = self._save()
        try:
            self.last_status = self._exec(tree, IO(None, sink, self._err_sink))
        except _Exit as exc:
            self.last_status = exc.code
        finally:
            status = self.last_status
            self._restore(saved)
            self.last_status = status
        return sink.text().rstrip("\n")

    def _save(self) -> dict:
        return {"vars": dict(self.vars), "exported": set(self.exported), "params": list(self.params),
                "script_name": self.script_name, "cwd": self.cwd, "functions": dict(self.functions),
                "aliases": dict(self.aliases), "script": self._script, "loops": self._loops,
                "fdepth": self._fdepth, "locals": self._locals}

    def _restore(self, s: dict) -> None:
        self.vars, self.exported, self.params = s["vars"], s["exported"], s["params"]
        self.script_name, self.functions, self.aliases = s["script_name"], s["functions"], s["aliases"]
        self._script, self._loops, self._fdepth, self._locals = s["script"], s["loops"], s["fdepth"], s["locals"]
        self.cwd = s["cwd"] if s["cwd"] in self.dirs else self.cwd

    def _exec(self, node, io: IO) -> int:
        self._steps += 1
        if self._steps > MAX_STEPS:
            raise _Abort()
        if isinstance(node, Seq):
            code = 0
            for item, bg in node.items:
                if bg:
                    io.err.err(self.st("background"), "yellow")
                    code = 1
                    continue
                code = self._exec(item, io)
                self.last_status = code
            return code
        if isinstance(node, AndOr):
            code = self._exec(node.first, io)
            self.last_status = code
            for op, part in node.rest:
                if (op == "&&") == (code == 0):
                    code = self._exec(part, io)
                    self.last_status = code
            return code
        if isinstance(node, Pipeline):
            code = self._pipeline(node, io)
        elif isinstance(node, Simple):
            code = self._simple(node, io)
        elif isinstance(node, FuncDef):
            self.functions[node.name] = node.body
            code = 0
        else:
            code = self._with_redirs(node.redirs, io, lambda sub: self._compound(node, sub))
        self.last_status = code
        return code

    def _pipeline(self, node: Pipeline, io: IO) -> int:
        stdin = io.stdin
        code = 0
        for i, cmd in enumerate(node.cmds):
            last = i == len(node.cmds) - 1
            pipe = io.out if last else Sink()
            saved = self._save() if len(node.cmds) > 1 else None
            try:
                code = self._exec(cmd, IO(stdin, pipe, io.err))
            except _Exit as exc:
                if saved is None:
                    raise
                code = exc.code
            finally:
                if saved is not None:
                    self._restore(saved)
            if not last:
                stdin = Stream(pipe.text())
        if node.negate:
            code = 0 if code else 1
        return code

    def _compound(self, node, io: IO) -> int:
        if isinstance(node, If):
            for cond, body in node.branches:
                if self._exec(cond, io) == 0:
                    return self._exec(body, io)
            return self._exec(node.orelse, io) if node.orelse is not None else 0
        if isinstance(node, Group):
            if not node.subshell:
                return self._exec(node.body, io)
            saved = self._save()
            try:
                return self._exec(node.body, io)
            except _Exit as exc:
                return exc.code
            finally:
                self._restore(saved)
        if isinstance(node, For):
            if node.words is None:
                items = list(self.params)
            else:
                items = []
                for w in node.words:
                    for b in self._braces(w):
                        items.extend(self._expand(b))
            return self._loop(lambda: iter(items), node.var, node.body, io)
        if isinstance(node, While):
            def turns():
                while True:
                    yield None
            return self._loop(turns, None, node.body, io, node.cond, node.until)
        return 0

    def _loop(self, make, var, body, io, cond=None, until=False) -> int:
        code = 0
        self._loops += 1
        try:
            for value in make():
                if cond is not None:
                    if (self._exec(cond, io) == 0) == until:
                        break
                if var is not None:
                    self._setvar(var, value)
                try:
                    code = self._exec(body, io)
                except _Loop as exc:
                    if exc.n > 1:
                        exc.n -= 1
                        raise
                    if exc.kind == "break":
                        break
        finally:
            self._loops -= 1
        return code

    # --- değişkenler -----------------------------------------------------

    def _getvar(self, name: str) -> str | None:
        if name == "PWD":
            return self.cwd
        return self.vars.get(name)

    def _setvar(self, name: str, value: str, export: bool = False) -> None:
        self.vars[name] = value
        if export:
            self.exported.add(name)

    def _special(self, name: str) -> str | None:
        if name == "?":
            return str(self.last_status)
        if name == "#":
            return str(len(self.params))
        if name in ("@", "*"):
            return " ".join(self.params)
        if name == "0":
            return self.script_name
        if name == "$":
            return "4242"
        if name.isdigit():
            k = int(name)
            return self.params[k - 1] if 0 < k <= len(self.params) else ""
        return None

    def _param(self, expr: str) -> str:
        """`${...}` içi: ad, `#ad`, `ad:-yedek`, `ad-yedek`."""
        if expr.startswith("#") and len(expr) > 1:
            return str(len(self._param(expr[1:])))
        m = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*|\d+|[?#@*$])(?:(:?-)(.*))?", expr, re.S)
        if not m:
            raise CmdError(f"{self._prefix()}: ${{{expr}}}: bad substitution", 1)
        name, op, alt = m.groups()
        value = self._special(name) if not NAME_RE.fullmatch(name) else self._getvar(name)
        if op == ":-" and not value:
            return self._expand_one(alt)
        if op == "-" and value is None:
            return self._expand_one(alt)
        return value or ""

    # --- genişletme -------------------------------------------------------

    def _dollar(self, raw: str, i: int) -> tuple[str | None, int, bool]:
        """`$` ya da `` ` `` ile başlayan genişletme: (değer, yeni konum, "$@" mi)."""
        if raw[i] == "`":
            j = raw.index("`", i + 1)
            return self._capture(raw[i + 1:j]), j + 1, False
        nxt = raw[i + 1] if i + 1 < len(raw) else ""
        if nxt == "(":
            j = _scan_dollar(raw, i)
            if raw.startswith("((", i + 1) and raw[j - 2:j] == "))":
                return str(self._arith(raw[i + 3:j - 2])), j, False
            return self._capture(raw[i + 2:j - 1]), j, False
        if nxt == "{":
            j = raw.index("}", i)
            return self._param(raw[i + 2:j]), j + 1, raw[i + 2:j] == "@"
        m = NAME_RE.match(raw, i + 1)
        if m:
            return self._getvar(m.group(0)) or "", m.end(), False
        if nxt and (nxt.isdigit() or nxt in "?#@*$0"):
            return self._special(nxt) or "", i + 2, nxt == "@"
        return None, i + 1, False

    def _expand_one(self, raw: str) -> str:
        """Bölmeden ve joker açmadan tek metin (atama değeri, yönlendirme hedefi)."""
        return " ".join(self._expand(raw, split=False, glob=False)) if raw else ""

    def _expand(self, raw: str, split: bool = True, glob: bool = True) -> list[str]:
        fields: list[list[tuple[str, bool]]] = [[]]
        keep = [False]

        def add(text: str, quoted: bool) -> None:
            fields[-1].append((text, quoted))
            if quoted:
                keep[-1] = True

        def new_field() -> None:
            fields.append([])
            keep.append(False)

        def add_split(value: str) -> None:
            if not split:
                if value:
                    add(value, False)
                return
            parts = re.split(r"[ \t\n]+", value)
            for k, part in enumerate(parts):
                if k > 0 and (fields[-1] or keep[-1]):
                    new_field()
                if part:
                    add(part, False)

        i, n, quoted = 0, len(raw), False
        while i < n:
            c = raw[i]
            if not quoted:
                if c == "'":
                    j = raw.index("'", i + 1)
                    add(raw[i + 1:j], True)
                    i = j + 1
                    continue
                if c == '"':
                    quoted = True
                    keep[-1] = True
                    i += 1
                    continue
                if c == "\\":
                    add(raw[i + 1] if i + 1 < n else "\\", True)
                    i += 2
                    continue
                if c == "~" and i == 0 and (n == 1 or raw[1] == "/"):
                    add(self._getvar("HOME") or HOME, True)
                    i += 1
                    continue
                if c in "$`":
                    value, i, _ = self._dollar(raw, i)
                    if value is None:
                        add("$", False)
                    else:
                        add_split(value)
                    continue
                add(c, False)
                i += 1
                continue
            if c == '"':
                quoted = False
                i += 1
                continue
            if c == "\\" and i + 1 < n and raw[i + 1] in '$`"\\\n':
                add(raw[i + 1], True)
                i += 2
                continue
            if c in "$`":
                value, i, at = self._dollar(raw, i)
                if value is None:
                    add("$", True)
                elif at:
                    for k, p in enumerate(self.params):
                        if k > 0:
                            new_field()
                        add(p, True)
                else:
                    add(value, True)
                continue
            add(c, True)
            i += 1

        result = []
        for segs, k in zip(fields, keep):
            if not segs and not k:
                continue
            text = "".join(t for t, _ in segs)
            if glob and any(not q and _has_magic(t) for t, q in segs):
                pattern = "".join(t if not q else _glob_escape(t) for t, q in segs)
                matches = self._glob(pattern)
                if matches:
                    result.extend(matches)
                    continue
            result.append(text)
        return result

    def _glob(self, pattern: str) -> list[str]:
        absolute = pattern.startswith("/")
        parts = pattern.split("/")
        cands = [("/" if absolute else "", "/" if absolute else self.cwd)]
        for idx, part in enumerate(parts):
            if part == "":
                if idx == len(parts) - 1 and idx > 0:
                    cands = [(d + "/", r) for d, r in cands if self._isdir(r)]
                continue
            new = []
            for disp, real in cands:
                if not self._isdir(real):
                    continue
                if _has_magic(part):
                    for name in self._entries(real):
                        if name.startswith(".") and not part.startswith("."):
                            continue
                        if fnmatch.fnmatchcase(name, part):
                            new.append((self._join_disp(disp, name), posixpath.join(real, name)))
                else:
                    p = posixpath.normpath(posixpath.join(real, part))
                    if self._exists(p):
                        new.append((self._join_disp(disp, part), p))
            cands = new
        return sorted(d for d, _ in cands)

    @staticmethod
    def _join_disp(disp: str, name: str) -> str:
        if disp == "":
            return name
        return disp + name if disp.endswith("/") else disp + "/" + name

    def _braces(self, raw: str) -> list[str]:
        """`{a,b}` ve `{1..3}` (tırnak dışında)."""
        i, n = 0, len(raw)
        while i < n:
            c = raw[i]
            if c == "\\":
                i += 2
                continue
            if c == "'":
                i = raw.find("'", i + 1) + 1 or n
                continue
            if c == '"':
                try:
                    i = _scan_dquote(raw, i)
                except ShellSyntax:
                    return [raw]
                continue
            if c == "$" and i + 1 < n and raw[i + 1] in "({":
                try:
                    i = _scan_dollar(raw, i)
                except ShellSyntax:
                    return [raw]
                continue
            if c == "{":
                depth, j, commas = 0, i, []
                while j < n:
                    ch = raw[j]
                    if ch == "\\":
                        j += 2
                        continue
                    if ch in "'\"":
                        break
                    if ch == "{":
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                        if depth == 0:
                            break
                    elif ch == "," and depth == 1:
                        commas.append(j)
                    j += 1
                if j < n and raw[j] == "}":
                    inner = raw[i + 1:j]
                    alts = None
                    if commas:
                        cuts = [i] + commas + [j]
                        alts = [raw[a + 1:b] for a, b in zip(cuts, cuts[1:])]
                    else:
                        m = re.fullmatch(r"(-?\d+)\.\.(-?\d+)", inner)
                        if m:
                            a, b = int(m.group(1)), int(m.group(2))
                            step = 1 if b >= a else -1
                            alts = [str(x) for x in range(a, b + step, step)]
                        m = re.fullmatch(r"([A-Za-z])\.\.([A-Za-z])", inner)
                        if m:
                            a, b = ord(m.group(1)), ord(m.group(2))
                            step = 1 if b >= a else -1
                            alts = [chr(x) for x in range(a, b + step, step)]
                    if alts is not None:
                        out = []
                        for alt in alts:
                            out.extend(self._braces(raw[:i] + alt + raw[j + 1:]))
                        return out
            i += 1
        return [raw]

    def _arith(self, expr: str) -> int:
        text = self._expand_one(expr) if ("$" in expr or "`" in expr) else expr
        shown = text.strip()

        def name_value(m):
            word = m.group(0)
            value = self._getvar(word) or "0"
            return value if re.fullmatch(r"-?\d+", value.strip()) else "0"
        py = re.sub(r"[A-Za-z_][A-Za-z0-9_]*", name_value, text)
        py = py.replace("&&", " and ").replace("||", " or ")
        py = re.sub(r"!(?!=)", " not ", py)
        try:
            tree = pyast.parse(py.strip() or "0", mode="eval")
            return int(self._arith_eval(tree.body, shown))
        except CmdError:
            raise
        except (SyntaxError, ValueError, TypeError, RecursionError):
            raise CmdError(f"{self._prefix()}: {shown}: syntax error in expression", 1) from None

    def _arith_eval(self, node, shown: str) -> int:
        if isinstance(node, pyast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
            return node.value
        if isinstance(node, pyast.UnaryOp):
            v = self._arith_eval(node.operand, shown)
            if isinstance(node.op, pyast.USub):
                return -v
            if isinstance(node.op, pyast.UAdd):
                return v
            if isinstance(node.op, pyast.Not):
                return 0 if v else 1
        if isinstance(node, pyast.BinOp):
            a, b = self._arith_eval(node.left, shown), self._arith_eval(node.right, shown)
            op = node.op
            if isinstance(op, pyast.Add):
                return a + b
            if isinstance(op, pyast.Sub):
                return a - b
            if isinstance(op, pyast.Mult):
                return a * b
            if isinstance(op, (pyast.Div, pyast.FloorDiv, pyast.Mod)):
                if b == 0:
                    raise CmdError(f"{self._prefix()}: {shown}: division by 0", 1)
                q = abs(a) // abs(b) * (1 if (a >= 0) == (b >= 0) else -1)
                return q if not isinstance(op, pyast.Mod) else a - q * b
            if isinstance(op, pyast.Pow):
                return a ** b if 0 <= b < 64 else 0
        if isinstance(node, pyast.Compare) and len(node.ops) == 1:
            a, b = self._arith_eval(node.left, shown), self._arith_eval(node.comparators[0], shown)
            ops = {pyast.Lt: a < b, pyast.Gt: a > b, pyast.LtE: a <= b, pyast.GtE: a >= b,
                   pyast.Eq: a == b, pyast.NotEq: a != b}
            return 1 if ops[type(node.ops[0])] else 0
        if isinstance(node, pyast.BoolOp):
            values = [self._arith_eval(v, shown) for v in node.values]
            return 1 if (all(values) if isinstance(node.op, pyast.And) else any(values)) else 0
        raise ValueError(shown)

    # --- basit komut ---------------------------------------------------------

    def _simple(self, node: Simple, io: IO) -> int:
        self._lineno = node.line
        self._err_sink = io.err
        try:
            words: list[str] = []
            for w in node.words:
                for b in self._braces(w):
                    words.extend(self._expand(b))
            assigns = []
            for a in node.assigns:
                name, value = ASSIGN_RE.fullmatch(a).groups()
                assigns.append((name, self._expand_one(value)))
        except CmdError as exc:
            io.err.err(exc.text)
            return exc.code
        if not words:
            for name, value in assigns:
                self._setvar(name, value)
            if node.redirs:
                return self._with_redirs(node.redirs, io, lambda sub: 0)
            return self.last_status if node.assigns and any("$(" in a or "`" in a for a in node.assigns) else 0
        if (node.words and NAME_RE.fullmatch(node.words[0]) and words and words[0] in self.aliases):
            words = self._expand_alias(words[0]) + words[1:]
            if not words:
                return 0
        if assigns:
            old = {name: (self.vars.get(name), name in self.exported) for name, _ in assigns}
            for name, value in assigns:
                self._setvar(name, value, export=True)
            try:
                return self._with_redirs(node.redirs, io, lambda sub: self._dispatch(words, sub))
            finally:
                for name, (value, was) in old.items():
                    if value is None:
                        self.vars.pop(name, None)
                    else:
                        self.vars[name] = value
                    if not was:
                        self.exported.discard(name)
        return self._with_redirs(node.redirs, io, lambda sub: self._dispatch(words, sub))

    def _expand_alias(self, name: str) -> list[str]:
        try:
            toks = lex(self.aliases[name])
        except ShellSyntax:
            return [name]
        words = []
        for tok in toks:
            if tok.kind == "W":
                for b in self._braces(str(tok.value)):
                    words.extend(self._expand(b))
        return words

    def _with_redirs(self, redirs: list[Redir], io: IO, fn) -> int:
        if not redirs:
            return fn(io)
        stdin, out, err = io.stdin, io.out, io.err
        opened: list[FileSink] = []
        try:
            for r in redirs:
                target = self._expand_one(r.target)
                if r.op == ">&":
                    if target == "1":
                        err = out
                    elif target == "2":
                        out = err
                    else:
                        io.err.err(f"{self._prefix()}: {target}: ambiguous redirect")
                        return 1
                    continue
                if r.op == "<":
                    if target == "/dev/null":
                        stdin = Stream("")
                        continue
                    p = self.abspath(target)
                    if p not in self.files:
                        reason = "Is a directory" if self._isdir(p) else "No such file or directory"
                        if self._isdir(p):
                            stdin = Stream("")
                            continue
                        io.err.err(f"{self._prefix()}: {target}: {reason}")
                        return 1
                    if not self._can(p, "r"):
                        io.err.err(f"{self._prefix()}: {target}: Permission denied")
                        return 1
                    stdin = Stream(self.files[p])
                    continue
                if target == "/dev/null":
                    sink: Sink = NullSink()
                else:
                    p = self.abspath(target)
                    reason = self._write_check(p, target)
                    if reason:
                        io.err.err(f"{self._prefix()}: {target}: {reason}")
                        return 1
                    if r.op == ">" or p not in self.files:
                        self._put(p, "")
                    sink = FileSink(self, p)
                    opened.append(sink)
                if r.fd in (1, -1):
                    out = sink
                if r.fd in (2, -1):
                    err = sink
            return fn(IO(stdin, out, err))
        finally:
            for sink in opened:
                sink.flush()

    def _dispatch(self, argv: list[str], io: IO) -> int:
        name, args = argv[0], argv[1:]
        if name in self.functions:
            return self._call_function(name, args, io)
        if name in BUILTINS:
            return getattr(self, "b_" + {"[": "test_bracket", "[[": "test_double", ":": "true",
                                          ".": "source"}.get(name, name))(args, io)
        if "/" in name:
            return self._exec_path(name, args, io)
        if name in EXTERNAL and self._system_in_path():
            self.hashed.add(name)
            return getattr(self, "c_" + name)(args, io)
        found = self._path_lookup(name)
        if found:
            return self._run_file(found, found, args, io)
        if name in EDITORS:
            io.err.err(self.t("no_editor_file", name=args[0] if args else "file.txt"), "yellow")
            return 1
        for group, key in ((PAGERS, "pager"), (PROCESS_TOOLS, "process"), (NETWORK_TOOLS, "network"),
                           (ADMIN_TOOLS, "admin"), (OTHER_PROGRAMS, "program")):
            if name in group:
                io.err.err(self.st(key, cmd=name), "yellow")
                return 1
        io.err.err(f"{self._prefix()}: {name}: command not found")
        return 127

    def _path_dirs(self) -> list[str]:
        return [d for d in (self._getvar("PATH") or "").split(":") if d]

    def _system_in_path(self) -> bool:
        return any(d.rstrip("/") in ("/usr/bin", "/bin") for d in self._path_dirs())

    def _path_lookup(self, name: str) -> str | None:
        for d in self._path_dirs():
            p = posixpath.join(self.abspath(d), name)
            if p in self.files and self._can(p, "x"):
                return p
        return None

    def _call_function(self, name: str, args: list[str], io: IO) -> int:
        if self._fdepth >= MAX_DEPTH:
            io.err.err(f"{self._prefix()}: {name}: maximum function nesting level exceeded ({MAX_DEPTH})")
            return 1
        saved_params = self.params
        self.params = list(args)
        self._fdepth += 1
        self._locals = self._locals + [{}]
        try:
            return self._exec(self.functions[name], io)
        except _Return as exc:
            return exc.code
        finally:
            for var, (value, was) in self._locals[-1].items():
                if value is None:
                    self.vars.pop(var, None)
                else:
                    self.vars[var] = value
                if not was:
                    self.exported.discard(var)
            self._locals = self._locals[:-1]
            self._fdepth -= 1
            self.params = saved_params

    def _exec_path(self, name: str, args: list[str], io: IO) -> int:
        p = self.abspath(name)
        if self._isdir(p):
            io.err.err(f"{self._prefix()}: {name}: Is a directory")
            return 126
        if p not in self.files:
            io.err.err(f"{self._prefix()}: {name}: No such file or directory")
            return 127
        if not self._can(p, "x") or not self._can(p, "r"):
            io.err.err(f"{self._prefix()}: {name}: Permission denied")
            return 126
        return self._run_file(p, name, args, io)

    def _run_file(self, path: str, name: str, args: list[str], io: IO, source: bool = False) -> int:
        """Betiği çalıştırır: alt kabukta (ya da `source` ile bu kabukta)."""
        text = self.files[path]
        first = text.split("\n", 1)[0]
        if first.startswith("#!") and not re.search(r"(^|[/ ])(ba)?sh\s*$", first[2:].strip()):
            io.err.err(self.st("interpreter", line=first), "yellow")
            return 126
        if self._fdepth >= MAX_DEPTH:
            io.err.err(self.st("too_many"), "yellow")
            return 1
        try:
            tree = parse(text)
        except ShellSyntax as exc:
            msg, color = self._syntax_text(exc, f"{name}: line {exc.line}")
            io.err.err(msg, color)
            return 2
        saved = self._save()
        if not source:
            self.vars = {k: v for k, v in self.vars.items() if k in self.exported}
            self.functions, self.aliases, self._locals = {}, {}, []
            self._loops = 0
            self.script_name = name
        if args or not source:
            self.params = list(args)
        self._script = name
        self._fdepth += 1
        try:
            code = self._exec(tree, io)
        except _Exit as exc:
            code = exc.code
        finally:
            if source:
                kept_vars, kept_exp, kept_fn, kept_al = self.vars, self.exported, self.functions, self.aliases
                kept_cwd = self.cwd
                self._restore(saved)
                self.vars, self.exported, self.functions, self.aliases = kept_vars, kept_exp, kept_fn, kept_al
                self.cwd = kept_cwd
            else:
                self._restore(saved)
        return code

    # --- yerleşik komutlar (builtins) -------------------------------------

    def b_cd(self, args, io):
        if len(args) > 1:
            io.err.err(f"{self._prefix()}: cd: too many arguments")
            return 2
        arg = args[0] if args else None
        if arg is None:
            target = self._getvar("HOME") or HOME
        elif arg == "-":
            old = self._getvar("OLDPWD")
            if not old:
                io.err.err(f"{self._prefix()}: cd: OLDPWD not set")
                return 1
            target = old
        else:
            target = self.abspath(arg)
        shown = arg if arg is not None else target
        if target in self.files:
            io.err.err(f"{self._prefix()}: cd: {shown}: Not a directory")
            return 1
        if target not in self.dirs:
            io.err.err(f"{self._prefix()}: cd: {shown}: No such file or directory")
            return 1
        if not self._can(target, "x"):
            io.err.err(f"{self._prefix()}: cd: {shown}: Permission denied")
            return 1
        self.vars["OLDPWD"] = self.cwd
        self.cwd = target
        self.vars["PWD"] = target
        if arg == "-":
            io.out.write(target + "\n")
        return 0

    def b_pwd(self, args, io):
        io.out.write(self.cwd + "\n")
        return 0

    def b_echo(self, args, io):
        newline, escapes = True, False
        while args and re.fullmatch(r"-[neE]+", args[0]):
            newline = newline and "n" not in args[0]
            if "e" in args[0]:
                escapes = True
            if "E" in args[0]:
                escapes = False
            args = args[1:]
        text = " ".join(args)
        if escapes:
            if "\\c" in text:
                text, newline = text.split("\\c", 1)[0], False
            text = _c_escapes(text)
        io.out.write(text + ("\n" if newline else ""))
        return 0

    def b_printf(self, args, io):
        if not args:
            io.err.err(f"{self._prefix()}: printf: usage: printf [-v var] format [arguments]")
            return 2
        fmt, values = args[0], args[1:]
        spec = re.compile(r"%(?P<flags>[-+ 0#]*)(?P<width>\d*)(?:\.(?P<prec>\d+))?(?P<conv>[sdifboxXc%])")
        out = []
        code = 0
        idx = 0
        while True:
            used = 0
            pos = 0
            for m in spec.finditer(fmt):
                out.append(_c_escapes(fmt[pos:m.start()]))
                pos = m.end()
                conv = m.group("conv")
                if conv == "%":
                    out.append("%")
                    continue
                value = values[idx] if idx < len(values) else ""
                if idx < len(values):
                    used += 1
                idx += 1
                width = m.group("width") or ""
                flags = m.group("flags") or ""
                prec = m.group("prec")
                if conv in "di":
                    try:
                        num = int(value) if value else 0
                    except ValueError:
                        io.err.err(f"{self._prefix()}: printf: {value}: invalid number")
                        code = 1
                        num = 0
                    text = format(num, f"{flags}{width}d")
                elif conv == "f":
                    try:
                        num = float(value) if value else 0.0
                    except ValueError:
                        io.err.err(f"{self._prefix()}: printf: {value}: invalid number")
                        code = 1
                        num = 0.0
                    text = format(num, f"{flags}{width}.{prec or 6}f")
                elif conv == "b":
                    text = _c_escapes(value)
                elif conv == "c":
                    text = value[:1]
                elif conv in "oxX":
                    try:
                        num = int(value) if value else 0
                    except ValueError:
                        num = 0
                    text = format(num, f"{flags}{width}{conv}")
                else:
                    if prec is not None:
                        value = value[:int(prec)]
                    text = value.ljust(int(width)) if "-" in flags and width else value.rjust(int(width or 0))
                out.append(text)
            out.append(_c_escapes(fmt[pos:]))
            if idx >= len(values) or used == 0:
                break
        io.out.write("".join(out))
        return code

    def b_export(self, args, io):
        args = [a for a in args if a != "-p"]
        if not args:
            for name in sorted(self.exported):
                if name in self.vars or name == "PWD":
                    value = self._getvar(name) or ""
                    io.out.write(f'declare -x {name}="{value}"\n')
            return 0
        code = 0
        for a in args:
            m = ASSIGN_RE.fullmatch(a)
            name = m.group(1) if m else a
            if not NAME_RE.fullmatch(name):
                io.err.err(f"{self._prefix()}: export: `{a}': not a valid identifier")
                code = 1
                continue
            if m:
                self._setvar(name, m.group(2), export=True)
            else:
                self.exported.add(name)
        return code

    def b_unset(self, args, io):
        funcs = "-f" in args
        for a in [x for x in args if not x.startswith("-")]:
            if funcs:
                self.functions.pop(a, None)
            else:
                self.vars.pop(a, None)
                self.exported.discard(a)
        return 0

    def b_local(self, args, io):
        if not self._locals:
            io.err.err(f"{self._prefix()}: local: can only be used in a function")
            return 1
        frame = self._locals[-1]
        for a in args:
            m = ASSIGN_RE.fullmatch(a)
            name = m.group(1) if m else a
            if name not in frame:
                frame[name] = (self.vars.get(name), name in self.exported)
            self.vars[name] = m.group(2) if m else self.vars.get(name, "")
        return 0

    def b_exit(self, args, io):
        code = self.last_status
        if args:
            try:
                code = int(args[0]) & 255
            except ValueError:
                io.err.err(f"{self._prefix()}: exit: {args[0]}: numeric argument required")
                code = 2
        raise _Exit(code)

    def b_return(self, args, io):
        if self._fdepth == 0:
            io.err.err(f"{self._prefix()}: return: can only `return' from a function or sourced script")
            return 1
        code = self.last_status
        if args:
            try:
                code = int(args[0]) & 255
            except ValueError:
                code = 2
        raise _Return(code)

    def _loop_jump(self, kind, args, io):
        if self._loops == 0:
            io.err.err(f"{self._prefix()}: {kind}: only meaningful in a `for', `while', or `until' loop")
            return 0
        n = int(args[0]) if args and args[0].isdigit() and int(args[0]) > 0 else 1
        raise _Loop(kind, min(n, self._loops))

    def b_break(self, args, io):
        return self._loop_jump("break", args, io)

    def b_continue(self, args, io):
        return self._loop_jump("continue", args, io)

    def b_true(self, args, io):
        return 0

    def b_false(self, args, io):
        return 1

    def b_shift(self, args, io):
        n = int(args[0]) if args and args[0].isdigit() else 1
        if n > len(self.params):
            return 1
        self.params = self.params[n:]
        return 0

    def b_history(self, args, io):
        for k, line in enumerate(self.history, 1):
            io.out.write(f"{k:5d}  {line}\n")
        return 0

    def b_read(self, args, io):
        raw = False
        names = []
        it = iter(args)
        for a in it:
            if a == "-r":
                raw = True
            elif a == "-p":
                next(it, None)
            else:
                names.append(a)
        if io.stdin is None:
            io.err.err(self.st("needs_input", cmd="read"), "yellow")
            return 1
        line = io.stdin.read_line()
        names = names or ["REPLY"]
        if line is None:
            for name in names:
                self.vars[name] = ""
            return 1
        if not raw:
            line = re.sub(r"\\(.)", r"\1", line)
        parts = line.strip().split(None, len(names) - 1) if names != ["REPLY"] else [line]
        for k, name in enumerate(names):
            self.vars[name] = parts[k] if k < len(parts) else ""
        return 0

    def b_source(self, args, io):
        if not args:
            io.err.err(f"{self._prefix()}: source: filename argument required")
            return 2
        p = self.abspath(args[0])
        if p not in self.files:
            io.err.err(f"{self._prefix()}: {args[0]}: No such file or directory")
            return 1
        return self._run_file(p, args[0], args[1:], io, source=True)

    def b_type(self, args, io):
        code = 0
        for name in args:
            if name in self.aliases:
                io.out.write(f"{name} is aliased to `{self.aliases[name]}'\n")
            elif name in RESERVED:
                io.out.write(f"{name} is a shell keyword\n")
            elif name in self.functions:
                io.out.write(f"{name} is a function\n")
            elif name in BUILTINS:
                io.out.write(f"{name} is a shell builtin\n")
            elif name in EXTERNAL and self._system_in_path():
                where = f"/usr/bin/{name}"
                io.out.write(f"{name} is hashed ({where})\n" if name in self.hashed else f"{name} is {where}\n")
            elif self._path_lookup(name):
                io.out.write(f"{name} is {self._path_lookup(name)}\n")
            else:
                io.err.err(f"{self._prefix()}: type: {name}: not found")
                code = 1
        return code

    def b_alias(self, args, io):
        if not args:
            for name in sorted(self.aliases):
                io.out.write(f"alias {name}='{self.aliases[name]}'\n")
            return 0
        code = 0
        for a in args:
            if "=" in a:
                name, value = a.split("=", 1)
                self.aliases[name] = value
            elif a in self.aliases:
                io.out.write(f"alias {a}='{self.aliases[a]}'\n")
            else:
                io.err.err(f"{self._prefix()}: alias: {a}: not found")
                code = 1
        return code

    def b_unalias(self, args, io):
        code = 0
        for a in args:
            if self.aliases.pop(a, None) is None:
                io.err.err(f"{self._prefix()}: unalias: {a}: not found")
                code = 1
        return code

    def b_kill(self, args, io):
        io.err.err(self.st("process", cmd="kill"), "yellow")
        return 1

    def b_jobs(self, args, io):
        io.err.err(self.st("process", cmd="jobs"), "yellow")
        return 1

    b_bg = b_fg = b_wait = b_jobs

    def b_help(self, args, io):
        io.err.err(self.st("program", cmd="help"), "yellow")
        return 1

    def b_set(self, args, io):
        io.err.err(self.st("program", cmd="set"), "yellow")
        return 1

    def b_eval(self, args, io):
        io.err.err(self.st("eval", cmd="eval"), "yellow")
        return 1

    b_exec = b_let = b_eval

    # --- test / [ ----------------------------------------------------------

    def b_test(self, args, io, name="test"):
        try:
            return 0 if self._test(list(args), name) else 1
        except CmdError as exc:
            io.err.err(f"{self._prefix()}: {name}: {exc.text}")
            return 2

    def b_test_bracket(self, args, io):
        if not args or args[-1] != "]":
            io.err.err(f"{self._prefix()}: [: missing `]'")
            return 2
        return self.b_test(args[:-1], io, "[")

    def b_test_double(self, args, io):
        if not args or args[-1] != "]]":
            io.err.err(f"{self._prefix()}: syntax error: missing `]]'")
            return 2
        return self.b_test(args[:-1], io, "[[")

    def _int(self, text: str) -> int:
        if re.fullmatch(r"\s*[-+]?\d+\s*", text):
            return int(text)
        raise CmdError(f"{text}: integer expected")

    def _unary(self, op: str, arg: str) -> bool:
        p = self.abspath(arg) if arg else ""
        if op == "-z":
            return arg == ""
        if op == "-n":
            return arg != ""
        if not arg:
            return False
        if op == "-e":
            return self._exists(p)
        if op == "-f":
            return p in self.files
        if op == "-d":
            return self._isdir(p)
        if op == "-s":
            return p in self.files and self.files[p] != "" or self._isdir(p)
        if op in ("-r", "-w", "-x"):
            return self._exists(p) and self._can(p, op[1])
        if op in ("-L", "-h"):
            return False
        raise CmdError(f"{op}: unary operator expected")

    def _binary(self, a: str, op: str, b: str) -> bool:
        if op in ("=", "=="):
            return a == b
        if op == "!=":
            return a != b
        if op == "<":
            return a < b
        if op == ">":
            return a > b
        x, y = self._int(a), self._int(b)
        return {"-eq": x == y, "-ne": x != y, "-lt": x < y, "-le": x <= y, "-gt": x > y, "-ge": x >= y}[op]

    UNARY_OPS = {"-z", "-n", "-e", "-f", "-d", "-s", "-r", "-w", "-x", "-L", "-h"}
    BINARY_OPS = {"=", "==", "!=", "<", ">", "-eq", "-ne", "-lt", "-le", "-gt", "-ge"}

    def _test(self, a: list[str], name: str) -> bool:
        n = len(a)
        if n == 0:
            return False
        if n == 1:
            return a[0] != ""
        if n == 2:
            if a[0] == "!":
                return not self._test(a[1:], name)
            if a[0] in self.UNARY_OPS:
                return self._unary(a[0], a[1])
            raise CmdError(f"{a[0]}: unary operator expected")
        if n == 3:
            if a[1] in self.BINARY_OPS:
                return self._binary(a[0], a[1], a[2])
            if a[1] == "-a":
                return self._test(a[:1], name) and self._test(a[2:], name)
            if a[1] == "-o":
                return self._test(a[:1], name) or self._test(a[2:], name)
            if a[0] == "!":
                return not self._test(a[1:], name)
            if a[0] == "(" and a[2] == ")":
                return self._test(a[1:2], name)
            raise CmdError(f"{a[1]}: binary operator expected")
        if n == 4 and a[0] == "!":
            return not self._test(a[1:], name)
        if n == 4 and a[0] == "(" and a[3] == ")":
            return self._test(a[1:3], name)
        for op in ("-o", "-a"):
            for k in range(n - 2, 0, -1):
                if a[k] == op:
                    left, right = self._test(a[:k], name), self._test(a[k + 1:], name)
                    return (left or right) if op == "-o" else (left and right)
        raise CmdError("too many arguments")

    # --- programlar: seçenek ayrıştırma --------------------------------------

    def _opts(self, cmd: str, args: list[str], flags: str, valued: str = "", io: IO | None = None):
        """Kısa seçenekler (`-la`, `-n 3`, `-n3`): (seçenekler, işlenenler) ya da None (hata yazıldı)."""
        opts: dict[str, object] = {}
        operands: list[str] = []
        i = 0
        while i < len(args):
            a = args[i]
            if a == "--":
                operands.extend(args[i + 1:])
                break
            if a.startswith("-") and len(a) > 1:
                if a.startswith("--"):
                    if io is not None:
                        io.err.err(self.t("unsupported", what=f"{cmd} {a}"), "yellow")
                    return None
                k = 1
                while k < len(a):
                    ch = a[k]
                    if ch in valued:
                        value = a[k + 1:]
                        if not value:
                            i += 1
                            if i >= len(args):
                                if io is not None:
                                    io.err.err(f"{cmd}: option requires an argument -- '{ch}'\n"
                                               f"Try '{cmd} --help' for more information.")
                                return None
                            value = args[i]
                        opts[ch] = value
                        break
                    if ch not in flags:
                        if io is not None:
                            io.err.err(self.t("unsupported", what=f"{cmd} -{ch}"), "yellow")
                        return None
                    opts[ch] = True
                    k += 1
            else:
                operands.append(a)
            i += 1
        return opts, operands

    def _inputs(self, cmd: str, names: list[str], io: IO, style: str = "plain"):
        """[(ad, metin)], hata oldu mu; girdi yoksa None (mesaj yazıldı)."""
        if not names:
            if io.stdin is None:
                io.err.err(self.st("needs_input", cmd=cmd), "yellow")
                return None, True
            return [("-", io.stdin.read_all())], False
        out, failed = [], False
        for name in names:
            if name == "-":
                out.append(("-", io.stdin.read_all() if io.stdin else ""))
                continue
            try:
                out.append((name, self._read_text(cmd, name, style)))
            except CmdError as exc:
                io.err.err(exc.text)
                failed = True
        return out, failed

    @staticmethod
    def _lines(text: str) -> list[str]:
        return text.splitlines(keepends=True)

    # --- ls -------------------------------------------------------------------

    def _indicator(self, p: str, shown: str = "") -> str:
        if shown in (".", "..") and not self.linux:
            # Git patikasının dersleri bu hâlle yazıldı (gerçek `ls -aF` ./ ../ yazıyor).
            return ""
        if self._isdir(p):
            return "/"
        if p in self.files and self._mode(p) & 0o111:
            return "*"
        return ""

    def _perm_text(self, p: str) -> str:
        mode = self._mode(p)
        kind = "d" if self._isdir(p) else "-"
        chars = []
        for shift in (6, 3, 0):
            bits = (mode >> shift) & 7
            chars.append(("r" if bits & 4 else "-") + ("w" if bits & 2 else "-") + ("x" if bits & 1 else "-"))
        text = kind + "".join(chars)
        if mode & 0o1000:
            text = text[:-1] + ("t" if mode & 1 else "T")
        return text

    def _size(self, p: str) -> int:
        return len(self.files[p].encode("utf-8")) if p in self.files else 4096

    def _blocks(self, p: str) -> int:
        if p not in self.files:
            return 4
        size = self._size(p)
        return -(-size // 4096) * 4

    def _nlink(self, p: str) -> int:
        if not self._isdir(p):
            return 1
        if self._is_gitdir(p):
            return 2
        return 2 + sum(1 for n in self._entries(p) if self._isdir(posixpath.join(p, n)))

    def _date(self, p: str) -> str:
        when = datetime.fromtimestamp(self.mtimes.get(p, self._now()), SHELL_TZ)
        return f"{MONTHS[when.month - 1]} {when.day:>2} {when.hour:02d}:{when.minute:02d}"

    def _ls_long(self, rows: list[tuple[str, str]], human: bool, io: IO, total: bool) -> None:
        if total:
            blocks = sum(self._blocks(p) for _, p in rows)
            io.out.write(f"total {human_size(blocks * 1024) if human else blocks}\n")
        if not rows:
            return
        cells = []
        for shown, p in rows:
            size = self._size(p)
            cells.append((self._perm_text(p), str(self._nlink(p)), self._owner(p), self._owner(p),
                          human_size(size) if human else str(size), self._date(p),
                          shown + self._indicator(p)))
        w = [max(len(c[k]) for c in cells) for k in range(5)]
        for c in cells:
            io.out.write(f"{c[0]} {c[1]:>{w[1]}} {c[2]:<{w[2]}} {c[3]:<{w[3]}} {c[4]:>{w[4]}} {c[5]} {c[6]}\n")

    @staticmethod
    def _columns(names: list[str], width: int = LINE_WIDTH) -> list[str]:
        """GNU ls -C dizilimi (sütunlar yukarıdan aşağı)."""
        n = len(names)
        if n == 0:
            return []
        lens = [len(x) for x in names]
        max_cols = max(1, min(n, width // 3))
        best = (1, [max(lens)])
        for cols in range(1, max_cols + 1):
            rows = -(-n // cols)
            arr = [0] * cols
            for k, ln in enumerate(lens):
                idx = k // rows
                real = ln + (0 if idx == cols - 1 else 2)
                arr[idx] = max(arr[idx], real)
            if sum(arr) < width:
                best = (cols, arr)
        cols, arr = best
        rows = -(-n // cols)
        lines = []
        for r in range(rows):
            parts = []
            for c in range(cols):
                k = c * rows + r
                if k >= n:
                    break
                last = (c + 1) * rows + r >= n
                parts.append(names[k] if last else names[k].ljust(arr[c]))
            lines.append("".join(parts).rstrip())
        return lines

    def _ls_block(self, rows: list[tuple[str, str]], opts: dict, io: IO, total: bool) -> None:
        if opts.get("l"):
            self._ls_long(rows, bool(opts.get("h")), io, total)
            return
        names = [shown + self._indicator(p, shown) for shown, p in rows]
        if io.out.tty and not opts.get("1"):
            for line in self._columns(names):
                io.out.write(line + "\n")
        else:
            for name in names:
                io.out.write(name + "\n")

    def _dir_rows(self, p: str, opts: dict) -> list[tuple[str, str]]:
        names = self._entries(p)
        if not (opts.get("a") or opts.get("A")):
            names = [x for x in names if not x.startswith(".")]
        rows = [(x, posixpath.join(p, x)) for x in names]
        if opts.get("a"):
            rows = [(".", p), ("..", posixpath.dirname(p) if p != "/" else "/")] + rows
        return rows

    def c_ls(self, args, io):
        parsed = self._opts("ls", args, "laAh1RdF", io=io)
        if parsed is None:
            return 2
        opts, targets = parsed
        code = 0
        files, dirs = [], []
        for t in targets or ["."]:
            p = self.abspath(t)
            if not self._exists(p):
                io.err.err(f"ls: cannot access '{t}': No such file or directory")
                code = 2
                continue
            if self._isdir(p) and not opts.get("d"):
                dirs.append((t, p))
            else:
                files.append((t, p))
        files.sort()
        dirs.sort()
        if files:
            self._ls_block(files, opts, io, False)
        many = len(targets) > 1 or opts.get("R")
        first = not files

        def show_dir(t, p):
            nonlocal first
            if not first:
                io.out.write("\n")
            first = False
            if many:
                io.out.write(f"{t}:\n")
            if self._isdir(p) and not self._can(p, "r"):
                io.err.err(f"ls: cannot open directory '{t}': Permission denied")
                return
            rows = self._dir_rows(p, opts)
            self._ls_block(rows, opts, io, True)
            if opts.get("R"):
                for shown, q in rows:
                    if shown in (".", "..") or not self._isdir(q) or self._is_gitdir(q):
                        continue
                    show_dir(self._join_disp(t if t != "." else ".", shown), q)
        for t, p in dirs:
            show_dir(t, p)
        return code

    # --- içerik okuyan programlar ----------------------------------------------

    def c_cat(self, args, io):
        """Dosyalar ve hatalar sırayla (gerçek cat gibi); -n satırları baştan sona numaralar."""
        parsed = self._opts("cat", args, "n", io=io)
        if parsed is None:
            return 1
        opts, names = parsed
        if not names:
            if io.stdin is None:
                io.err.err(self.st("needs_input", cmd="cat"), "yellow")
                return 1
            names = ["-"]
        failed = False
        number = 0
        for name in names:
            try:
                if name == "-":
                    text = io.stdin.read_all() if io.stdin else ""
                else:
                    text = self._read_text("cat", name)
            except CmdError as exc:
                io.err.err(exc.text)
                failed = True
                continue
            if opts.get("n"):
                parts = []
                for line in self._lines(text):
                    number += 1
                    parts.append(f"{number:6d}\t{line}")
                text = "".join(parts)
            io.out.write(text)
        return 1 if failed else 0

    def c_head(self, args, io):
        return self._head_tail("head", args, io)

    def c_tail(self, args, io):
        return self._head_tail("tail", args, io)

    def _head_tail(self, cmd, args, io):
        count, plus = "10", False
        rest = []
        i = 0
        while i < len(args):
            a = args[i]
            if re.fullmatch(r"-\d+", a):
                count = a[1:]
            elif a == "-n" and i + 1 < len(args):
                count = args[i + 1]
                i += 1
            elif a.startswith("-n") and len(a) > 2:
                count = a[2:]
            elif a.startswith("-") and a != "-":
                io.err.err(self.t("unsupported", what=f"{cmd} {a}"), "yellow")
                return 1
            else:
                rest.append(a)
            i += 1
        if cmd == "tail" and count.startswith("+"):
            plus, count = True, count[1:]
        if not re.fullmatch(r"\d+", count):
            io.err.err(f"{cmd}: invalid number of lines: '{count}'")
            return 1
        n = int(count)
        inputs, failed = self._inputs(cmd, rest, io, "open")
        if inputs is None:
            return 1
        show_names = len(rest) > 1
        first = True
        for name, text in inputs:
            if show_names:
                io.out.write(("" if first else "\n") + f"==> {name if name != '-' else 'standard input'} <==\n")
            first = False
            lines = self._lines(text)
            if cmd == "head":
                part = lines[:n]
            elif plus:
                part = lines[max(n - 1, 0):]
            else:
                part = lines[-n:] if n else []
            io.out.write("".join(part))
        return 1 if failed else 0

    def c_wc(self, args, io):
        parsed = self._opts("wc", args, "lwcm", io=io)
        if parsed is None:
            return 1
        opts, names = parsed
        selected = [k for k in "lwmc" if opts.get(k)] or ["l", "w", "c"]
        inputs, failed = self._inputs("wc", names, io)
        if inputs is None:
            return 1
        rows = []
        for name, text in inputs:
            counts = {"l": text.count("\n"), "w": len(text.split()), "c": len(text.encode("utf-8")),
                      "m": len(text)}
            rows.append(([counts[k] for k in selected], "" if name == "-" else name))
        if len(selected) == 1 and len(inputs) + (1 if failed else 0) == 1:
            width = 1
        else:
            regular = sum(len(t.encode("utf-8")) for nm, t in inputs if nm != "-")
            width = max(1, len(str(regular)))
            if any(nm == "-" for nm, _ in inputs):
                width = max(width, 7)
        if len(rows) > 1:
            rows.append(([sum(r[0][k] for r in rows) for k in range(len(selected))], "total"))
        for counts, name in rows:
            text = " ".join(str(c).rjust(width) for c in counts)
            io.out.write(text + (f" {name}" if name else "") + "\n")
        return 1 if failed else 0

    def c_grep(self, args, io):
        parsed = self._opts("grep", args, "invcrRlLwxEFhHoqs", "e", io=io)
        if parsed is None:
            return 2
        opts, rest = parsed
        if "e" in opts:
            pattern = str(opts["e"])
        elif rest:
            pattern, rest = rest[0], rest[1:]
        else:
            io.err.err("Usage: grep [OPTION]... PATTERN [FILE]...\nTry 'grep --help' for more information.")
            return 2
        try:
            if opts.get("F"):
                body = re.escape(pattern)
            else:
                body = _bre_to_py(pattern, bool(opts.get("E")))
            if opts.get("w"):
                body = rf"(?<!\w)(?:{body})(?!\w)"
            if opts.get("x"):
                body = rf"^(?:{body})$"
            regex = re.compile(body, re.I if opts.get("i") else 0)
        except CmdError as exc:
            io.err.err(exc.text)
            return 2
        except re.error:
            io.err.err("grep: Invalid regular expression")
            return 2
        recursive = opts.get("r") or opts.get("R")
        targets: list[tuple[str, str | None]] = []  # (gösterilen ad, metin ya da None = stdin)
        failed = False
        if not rest:
            if recursive:
                for shown, p in self._walk_files(self.cwd, ""):
                    targets.append((shown, self.files[p]))
            elif io.stdin is None:
                io.err.err(self.st("needs_input", cmd="grep"), "yellow")
                return 2
            else:
                targets.append(("(standard input)", io.stdin.read_all()))
        for name in rest:
            p = self.abspath(name)
            if self._isdir(p):
                if recursive:
                    for shown, q in self._walk_files(p, name):
                        targets.append((shown, self.files[q]))
                else:
                    io.err.err(f"grep: {name}: Is a directory")
                    failed = True
                continue
            try:
                targets.append((name, self._read_text("grep", name)))
            except CmdError as exc:
                if not opts.get("s"):
                    io.err.err(f"grep: {name}: " + exc.text.split(": ", 2)[-1])
                failed = True
        any_dir = any(self._isdir(self.abspath(x)) for x in rest)
        show = (len(rest) > 1 or (recursive and (any_dir or not rest))) and not opts.get("h") or opts.get("H")
        found = False
        for shown, text in targets:
            count = 0
            for k, line in enumerate(text.splitlines(), 1):
                hit = bool(regex.search(line))
                if hit == bool(opts.get("v")):
                    continue
                count += 1
                found = True
                if opts.get("q"):
                    return 0
                if opts.get("c") or opts.get("l") or opts.get("L"):
                    continue
                pre = (f"{shown}:" if show else "") + (f"{k}:" if opts.get("n") else "")
                if opts.get("o") and not opts.get("v"):
                    for m in regex.finditer(line):
                        if m.group(0):
                            io.out.write(pre + m.group(0) + "\n")
                else:
                    io.out.write(pre + line + "\n")
            if opts.get("c"):
                io.out.write((f"{shown}:" if show else "") + f"{count}\n")
            elif opts.get("l") and count:
                io.out.write(shown + "\n")
            elif opts.get("L") and not count:
                io.out.write(shown + "\n")
        if failed:
            return 2
        return 0 if found else 1

    def _walk_files(self, p: str, shown: str):
        """Klasörün altındaki dosyalar (derinlemesine, C sırası): (gösterilen yol, gerçek yol)."""
        for name in self._children(p):
            q = posixpath.join(p, name)
            disp = self._join_disp(shown, name)
            if q in self.files:
                yield disp, q
            elif q in self.dirs:
                yield from self._walk_files(q, disp)

    def c_sort(self, args, io):
        parsed = self._opts("sort", args, "rnufb", "kt", io=io)
        if parsed is None:
            return 2
        opts, names = parsed
        inputs, failed = self._inputs("sort", names, io, "sort")
        if inputs is None:
            return 2
        if failed:
            return 2
        lines = []
        for _, text in inputs:
            lines.extend(text.splitlines())
        delim = opts.get("t")
        key_spec = opts.get("k")
        numeric = bool(opts.get("n"))
        start = end = None
        if key_spec:
            m = re.fullmatch(r"(\d+)([a-z]*)(?:,(\d+)([a-z]*))?", str(key_spec))
            if not m:
                io.err.err(f"sort: invalid number at field start: invalid count at start of '{key_spec}'")
                return 2
            start = int(m.group(1))
            end = int(m.group(3)) if m.group(3) else None
            numeric = numeric or "n" in (m.group(2) or "") + (m.group(4) or "")

        def key_text(line: str) -> str:
            if start is None:
                return line
            if delim:
                fields = line.split(str(delim))
                part = fields[start - 1:end] if end else fields[start - 1:]
                return str(delim).join(part)
            fields = re.findall(r"\s*\S+", line)
            part = fields[start - 1:end] if end else fields[start - 1:]
            return "".join(part)

        def primary(line: str):
            text = key_text(line)
            if opts.get("f"):
                text = text.upper()
            if numeric:
                m = re.match(r"\s*(-?\d+(?:\.\d+)?)", text)
                return (float(m.group(1)) if m else 0.0,)
            return (text.encode("utf-8"),)

        if opts.get("u"):
            order = sorted(lines, key=primary, reverse=bool(opts.get("r")))
            out, last = [], object()
            for line in order:
                k = primary(line)
                if k != last:
                    out.append(line)
                    last = k
        else:
            out = sorted(lines, key=lambda x: (primary(x), x.encode("utf-8")), reverse=bool(opts.get("r")))
        io.out.write("".join(x + "\n" for x in out))
        return 0

    def c_uniq(self, args, io):
        parsed = self._opts("uniq", args, "cdui", io=io)
        if parsed is None:
            return 1
        opts, names = parsed
        if len(names) > 1:
            io.err.err(self.t("unsupported", what="uniq INPUT OUTPUT"), "yellow")
            return 1
        inputs, failed = self._inputs("uniq", names, io)
        if inputs is None or failed:
            return 1
        groups: list[list] = []
        for line in inputs[0][1].splitlines():
            k = line.lower() if opts.get("i") else line
            if groups and groups[-1][0] == k:
                groups[-1][2] += 1
            else:
                groups.append([k, line, 1])
        for _, line, count in groups:
            if opts.get("d") and count < 2 or opts.get("u") and count > 1:
                continue
            io.out.write((f"{count:7d} " if opts.get("c") else "") + line + "\n")
        return 0

    def c_cut(self, args, io):
        parsed = self._opts("cut", args, "s", "dfcb", io=io)
        if parsed is None:
            return 1
        opts, names = parsed
        spec = opts.get("f") or opts.get("c") or opts.get("b")
        if not spec:
            io.err.err("cut: you must specify a list of bytes, characters, or fields\n"
                       "Try 'cut --help' for more information.")
            return 1
        ranges = _cut_list(str(spec))
        if ranges is None:
            io.err.err(f"cut: invalid field value '{spec}'\nTry 'cut --help' for more information.")
            return 1
        delim = str(opts.get("d", "\t"))
        if len(delim) != 1:
            io.err.err("cut: the delimiter must be a single character\nTry 'cut --help' for more information.")
            return 1
        inputs, failed = self._inputs("cut", names, io)
        if inputs is None:
            return 1
        out = []
        for _, text in inputs:
            for line in text.splitlines():
                if opts.get("f"):
                    if delim not in line:
                        if not opts.get("s"):
                            out.append(line)
                        continue
                    fields = line.split(delim)
                    out.append(delim.join(f for k, f in enumerate(fields, 1) if _in_ranges(k, ranges)))
                else:
                    out.append("".join(ch for k, ch in enumerate(line, 1) if _in_ranges(k, ranges)))
        io.out.write("".join(x + "\n" for x in out))
        return 1 if failed else 0

    def c_tr(self, args, io):
        parsed = self._opts("tr", args, "ds", io=io)
        if parsed is None:
            return 1
        opts, sets = parsed
        if not sets:
            io.err.err("tr: missing operand\nTry 'tr --help' for more information.")
            return 1
        need = 1 if opts.get("d") and not opts.get("s") else (2 if not opts.get("s") or len(sets) > 1 else 1)
        if opts.get("d") and opts.get("s"):
            need = 2
        if len(sets) < need:
            io.err.err(f"tr: missing operand after '{sets[-1]}'\nTwo strings must be given when translating.\n"
                       "Try 'tr --help' for more information.")
            return 1
        if len(sets) > need:
            io.err.err(f"tr: extra operand '{sets[need]}'\nTry 'tr --help' for more information.")
            return 1
        if io.stdin is None:
            io.err.err(self.st("needs_input", cmd="tr"), "yellow")
            return 1
        text = io.stdin.read_all()
        set1 = _tr_set(sets[0])
        set2 = _tr_set(sets[1]) if len(sets) > 1 else []
        if opts.get("d"):
            text = "".join(ch for ch in text if ch not in set1)
            squeeze = set2
        elif set2:
            table = {c: set2[min(k, len(set2) - 1)] for k, c in enumerate(set1)}
            text = "".join(table.get(ch, ch) for ch in text)
            squeeze = set2
        else:
            squeeze = set1
        if opts.get("s"):
            out = []
            for ch in text:
                if out and out[-1] == ch and ch in squeeze:
                    continue
                out.append(ch)
            text = "".join(out)
        io.out.write(text)
        return 0

    # --- find --------------------------------------------------------------------

    def c_find(self, args, io):
        paths = []
        i = 0
        while i < len(args) and not args[i].startswith("-") and args[i] not in ("!", "("):
            paths.append(args[i])
            i += 1
        expr = args[i:]
        tests = []
        maxdepth, mindepth = None, 0
        action = None
        k = 0
        negate = False
        while k < len(expr):
            a = expr[k]
            if a in ("!", "-not"):
                negate = not negate
                k += 1
                continue
            if a in ("-name", "-iname", "-type", "-maxdepth", "-mindepth"):
                if k + 1 >= len(expr):
                    io.err.err(f"find: missing argument to `{a}'")
                    return 1
                value = expr[k + 1]
                if a == "-type" and value not in ("f", "d"):
                    io.err.err(f"find: Unknown argument to -type: {value}")
                    return 1
                if a in ("-maxdepth", "-mindepth"):
                    if not value.isdigit():
                        io.err.err(f"find: Expected a positive decimal integer argument to {a}, but got"
                                   f" `{value}'")
                        return 1
                    if a == "-maxdepth":
                        maxdepth = int(value)
                    else:
                        mindepth = int(value)
                else:
                    tests.append((a, value, negate))
                negate = False
                k += 2
                continue
            if a == "-print":
                k += 1
                continue
            if a == "-delete":
                action = ("delete",)
                k += 1
                continue
            if a == "-exec":
                end = k + 1
                while end < len(expr) and expr[end] != ";":
                    end += 1
                if end >= len(expr):
                    io.err.err("find: missing argument to `-exec'")
                    return 1
                action = ("exec", expr[k + 1:end])
                k = end + 1
                continue
            io.err.err(f"find: unknown predicate `{a}'" if a.startswith("-") else
                       f"find: paths must precede expression: `{a}'")
            return 1

        def match(p: str, shown: str) -> bool:
            name = posixpath.basename(shown.rstrip("/")) or shown
            for kind, value, neg in tests:
                if kind == "-name":
                    ok = fnmatch.fnmatchcase(name, value)
                elif kind == "-iname":
                    ok = fnmatch.fnmatchcase(name.lower(), value.lower())
                else:
                    ok = self._isdir(p) if value == "d" else p in self.files
                if ok == neg:
                    return False
            return True

        code = 0
        found: list[tuple[str, str]] = []

        def walk(p: str, shown: str, depth: int):
            if depth >= mindepth and match(p, shown):
                found.append((shown, p))
            if self._isdir(p) and not self._is_gitdir(p) and (maxdepth is None or depth < maxdepth):
                for name in self._children(p):
                    walk(posixpath.join(p, name), self._join_disp(shown, name), depth + 1)

        for start in paths or ["."]:
            p = self.abspath(start)
            if not self._exists(p):
                io.err.err(f"find: '{start}': No such file or directory")
                code = 1
                continue
            walk(p, start, 0)
        if action is None:
            for shown, _ in found:
                io.out.write(shown + "\n")
        elif action[0] == "delete":
            for shown, p in reversed(found):
                if p in self.files:
                    self._remove_path(p)
                elif p in self.dirs and not self._children(p) and p != self.cwd:
                    self._remove_path(p)
                elif p in self.dirs:
                    io.err.err(f"find: cannot delete '{shown}': Directory not empty")
                    code = 1
        else:
            for shown, _ in found:
                argv = [shown if w == "{}" else w.replace("{}", shown) for w in action[1]]
                if argv:
                    self._dispatch(argv, io)
        return code

    # --- dosya ve klasör işlemleri ------------------------------------------

    def c_mkdir(self, args, io):
        parsed = self._opts("mkdir", args, "pv", io=io)
        if parsed is None:
            return 1
        opts, names = parsed
        if not names:
            io.err.err("mkdir: missing operand\nTry 'mkdir --help' for more information.")
            return 1
        code = 0
        for a in names:
            p = self.abspath(a)
            if opts.get("p"):
                chain = []
                d = p
                while d not in self.dirs and d != "/":
                    chain.append(d)
                    d = posixpath.dirname(d)
                bad = None
                for d in reversed(chain):
                    if d in self.files:
                        bad = "File exists"
                    elif not self._can(posixpath.dirname(d), "w"):
                        bad = "Permission denied"
                    if bad:
                        io.err.err(f"mkdir: cannot create directory '{a}': {bad}")
                        code = 1
                        break
                    self.dirs.add(d)
                    self.mtimes[d] = self._now()
                continue
            parent = posixpath.dirname(p)
            if self._exists(p):
                io.err.err(f"mkdir: cannot create directory '{a}': File exists")
                code = 1
            elif parent not in self.dirs:
                io.err.err(f"mkdir: cannot create directory '{a}': " +
                           ("Not a directory" if parent in self.files else "No such file or directory"))
                code = 1
            elif not self._can(parent, "w"):
                io.err.err(f"mkdir: cannot create directory '{a}': Permission denied")
                code = 1
            else:
                self.dirs.add(p)
                self.mtimes[p] = self._now()
        return code

    def c_touch(self, args, io):
        names = [a for a in args if not a.startswith("-")]
        if not names:
            io.err.err("touch: missing file operand\nTry 'touch --help' for more information.")
            return 1
        code = 0
        for a in names:
            p = self.abspath(a)
            if self._isdir(p):
                self.mtimes[p] = self._now()
                continue
            reason = self._write_check(p, a)
            if reason:
                io.err.err(f"touch: cannot touch '{a}': {reason}")
                code = 1
                continue
            self._put(p, self.files.get(p, ""))
        return code

    def c_rm(self, args, io):
        parsed = self._opts("rm", args, "rRfivd", io=io)
        if parsed is None:
            return 1
        opts, names = parsed
        recursive = opts.get("r") or opts.get("R")
        if opts.get("i") and names:
            # Gerçek rm -i her dosya için soru sorup klavyeden cevap bekler; burada klavye girdisi yok.
            io.err.err(self.st("rm_ask"), "yellow")
            return 1
        if not names:
            if opts.get("f"):
                return 0
            io.err.err("rm: missing operand\nTry 'rm --help' for more information.")
            return 1
        code = 0
        for a in names:
            p = self.abspath(a)
            if recursive and p == "/":
                io.err.err("rm: it is dangerous to operate recursively on '/'\n"
                           "rm: use --no-preserve-root to override this failsafe")
                code = 1
                continue
            if posixpath.basename(a.rstrip("/")) in (".", ".."):
                io.err.err(f"rm: refusing to remove '.' or '..' directory: skipping '{a}'")
                code = 1
                continue
            if not self._exists(p):
                if not opts.get("f"):
                    io.err.err(f"rm: cannot remove '{a}': No such file or directory")
                    code = 1
                continue
            parent = posixpath.dirname(p)
            if not self._can(parent, "w"):
                io.err.err(f"rm: cannot remove '{a}': Permission denied")
                code = 1
                continue
            if self._isdir(p) and not recursive:
                if opts.get("d") and not self._children(p):
                    self._remove_path(p)
                    continue
                io.err.err(f"rm: cannot remove '{a}': Is a directory")
                code = 1
                continue
            if self._is_gitdir(p):
                getattr(self, "repos", {}).pop(p[:-5], None)
                continue
            self._remove_path(p)
        return code

    def c_rmdir(self, args, io):
        names = [a for a in args if not a.startswith("-")]
        if not names:
            io.err.err("rmdir: missing operand\nTry 'rmdir --help' for more information.")
            return 1
        code = 0
        for a in names:
            p = self.abspath(a)
            if p in self.files:
                reason = "Not a directory"
            elif not self._isdir(p):
                reason = "No such file or directory"
            elif self._entries(p):
                reason = "Directory not empty"
            elif not self._can(posixpath.dirname(p), "w"):
                reason = "Permission denied"
            else:
                self._remove_path(p)
                continue
            io.err.err(f"rmdir: failed to remove '{a}': {reason}")
            code = 1
        return code

    def _two_operands(self, cmd: str, names: list[str], io: IO) -> bool:
        if not names:
            io.err.err(f"{cmd}: missing file operand\nTry '{cmd} --help' for more information.")
            return False
        if len(names) == 1:
            io.err.err(f"{cmd}: missing destination file operand after '{names[0]}'\n"
                       f"Try '{cmd} --help' for more information.")
            return False
        return True

    def c_cp(self, args, io):
        parsed = self._opts("cp", args, "rRivfpa", io=io)
        if parsed is None:
            return 1
        opts, names = parsed
        if not self._two_operands("cp", names, io):
            return 1
        recursive = opts.get("r") or opts.get("R") or opts.get("a")
        *srcs, dest = names
        dp = self.abspath(dest)
        if len(srcs) > 1 and not self._isdir(dp):
            io.err.err(f"cp: target '{dest}' is not a directory")
            return 1
        code = 0
        for src in srcs:
            sp = self.abspath(src)
            if not self._exists(sp):
                io.err.err(f"cp: cannot stat '{src}': No such file or directory")
                code = 1
                continue
            if self._isdir(sp) and not recursive:
                io.err.err(f"cp: -r not specified; omitting directory '{src}'")
                code = 1
                continue
            into = self._isdir(dp)
            tp = posixpath.join(dp, posixpath.basename(sp)) if into else dp
            tshown = self._join_disp(dest.rstrip("/") or "/", posixpath.basename(sp)) if into else dest
            if sp in self.files:
                if tp == sp:
                    io.err.err(f"cp: '{src}' and '{tshown}' are the same file")
                    code = 1
                    continue
                if not self._can(sp, "r"):
                    io.err.err(f"cp: cannot open '{src}' for reading: Permission denied")
                    code = 1
                    continue
                reason = self._write_check(tp, tshown)
                if reason:
                    io.err.err(f"cp: cannot create regular file '{tshown}': {reason}")
                    code = 1
                    continue
                self._put(tp, self.files[sp])
                self.modes[tp] = self._mode(sp)
                continue
            if tp == sp or tp.startswith(sp + "/"):
                io.err.err(f"cp: cannot copy a directory, '{src}', into itself, '{tshown}'")
                code = 1
                continue
            if posixpath.dirname(tp) not in self.dirs:
                io.err.err(f"cp: cannot create directory '{tshown}': No such file or directory")
                code = 1
                continue
            self._copy_tree(sp, tp)
        return code

    def _copy_tree(self, sp: str, tp: str) -> None:
        pref = sp.rstrip("/") + "/"
        self.dirs.add(tp)
        self.modes[tp] = self._mode(sp)
        for d in sorted(d for d in self.dirs if d.startswith(pref)):
            self.dirs.add(tp + d[len(sp):])
            if d in self.modes:
                self.modes[tp + d[len(sp):]] = self.modes[d]
        for f in [f for f in self.files if f.startswith(pref)]:
            self._put(tp + f[len(sp):], self.files[f])
            if f in self.modes:
                self.modes[tp + f[len(sp):]] = self.modes[f]

    def c_mv(self, args, io):
        parsed = self._opts("mv", args, "ivfn", io=io)
        if parsed is None:
            return 1
        opts, names = parsed
        if not self._two_operands("mv", names, io):
            return 1
        *srcs, dest = names
        dp = self.abspath(dest)
        if len(srcs) > 1 and not self._isdir(dp):
            io.err.err(f"mv: target '{dest}' is not a directory")
            return 1
        code = 0
        for src in srcs:
            sp = self.abspath(src)
            if not self._exists(sp):
                io.err.err(f"mv: cannot stat '{src}': No such file or directory")
                code = 1
                continue
            into = self._isdir(dp)
            tp = posixpath.join(dp, posixpath.basename(sp)) if into else dp
            tshown = self._join_disp(dest.rstrip("/") or "/", posixpath.basename(sp)) if into else dest
            if tp == sp:
                io.err.err(f"mv: '{src}' and '{tshown}' are the same file")
                code = 1
                continue
            if self._isdir(sp) and tp.startswith(sp + "/"):
                io.err.err(f"mv: cannot move '{src}' to a subdirectory of itself, '{tshown}'")
                code = 1
                continue
            parent = posixpath.dirname(tp)
            if parent not in self.dirs:
                io.err.err(f"mv: cannot move '{src}' to '{tshown}': No such file or directory")
                code = 1
                continue
            if not self._can(parent, "w") or not self._can(posixpath.dirname(sp), "w"):
                io.err.err(f"mv: cannot move '{src}' to '{tshown}': Permission denied")
                code = 1
                continue
            if self._isdir(sp) and tp in self.files:
                io.err.err(f"mv: cannot overwrite non-directory '{tshown}' with directory '{src}'")
                code = 1
                continue
            if sp in self.files and self._isdir(tp):
                io.err.err(f"mv: cannot overwrite directory '{tshown}' with non-directory")
                code = 1
                continue
            if self._isdir(sp) and self._isdir(tp):
                if self._entries(tp):
                    io.err.err(f"mv: cannot move '{src}' to '{tshown}': Directory not empty")
                    code = 1
                    continue
                self._remove_path(tp)
            if tp in self.files:
                self._remove_path(tp)
            self._move_path(sp, tp)
            if self.cwd == sp or self.cwd.startswith(sp + "/"):
                self.cwd = tp + self.cwd[len(sp):]
        return code

    def c_chmod(self, args, io):
        recursive = False
        rest = []
        for a in args:
            if a in ("-R", "--recursive"):
                recursive = True
            else:
                rest.append(a)
        if not rest:
            io.err.err("chmod: missing operand\nTry 'chmod --help' for more information.")
            return 1
        mode_text, names = rest[0], rest[1:]
        if not names:
            io.err.err(f"chmod: missing operand after '{mode_text}'\nTry 'chmod --help' for more information.")
            return 1
        if not (re.fullmatch(r"[0-7]{1,4}", mode_text) or
                re.fullmatch(r"([ugoa]*[-+=][rwxXt]*)(,[ugoa]*[-+=][rwxXt]*)*", mode_text)):
            io.err.err(f"chmod: invalid mode: '{mode_text}'\nTry 'chmod --help' for more information.")
            return 1
        code = 0
        for a in names:
            p = self.abspath(a)
            if not self._exists(p):
                io.err.err(f"chmod: cannot access '{a}': No such file or directory")
                code = 1
                continue
            targets = [p]
            if recursive and self._isdir(p):
                pref = p.rstrip("/") + "/"
                targets += sorted(x for x in list(self.dirs) + list(self.files) if x.startswith(pref))
            for t in targets:
                if self._owner(t) != USER:
                    io.err.err(f"chmod: changing permissions of '{a}': Operation not permitted")
                    code = 1
                    break
                self.modes[t] = self._new_mode(self._mode(t), mode_text, self._isdir(t))
        return code

    @staticmethod
    def _new_mode(mode: int, text: str, is_dir: bool) -> int:
        if re.fullmatch(r"[0-7]{1,4}", text):
            return int(text, 8)
        for clause in text.split(","):
            m = re.fullmatch(r"([ugoa]*)([-+=])([rwxXt]*)", clause)
            who, op, perms = m.groups()
            masked = not who
            who = who or "a"
            if "a" in who:
                who = "ugo"
            bits = 0
            for ch in perms:
                if ch == "X" and not (is_dir or mode & 0o111):
                    continue
                if ch == "t":
                    bits |= 0o1000
                    continue
                value = {"r": 4, "w": 2, "x": 1, "X": 1}[ch]
                for w in who:
                    bits |= value << {"u": 6, "g": 3, "o": 0}[w]
            if masked:
                bits &= ~0o022 | 0o1000
            whomask = sum(7 << {"u": 6, "g": 3, "o": 0}[w] for w in who)
            if op == "+":
                mode |= bits
            elif op == "-":
                mode &= ~bits
            else:
                mode = (mode & ~whomask) | bits
        return mode

    # --- küçük programlar -------------------------------------------------------

    def c_whoami(self, args, io):
        io.out.write(USER + "\n")
        return 0

    def c_id(self, args, io):
        io.out.write(f"uid=1000({USER}) gid=1000({USER}) groups=1000({USER})\n")
        return 0

    def c_groups(self, args, io):
        io.out.write(USER + "\n")
        return 0

    def _env_items(self) -> list[tuple[str, str]]:
        return [(k, self._getvar(k) or "") for k in self.vars if k in self.exported]

    def c_env(self, args, io):
        if args:
            io.err.err(self.t("unsupported", what="env " + " ".join(args)), "yellow")
            return 1
        for k, v in self._env_items():
            io.out.write(f"{k}={v}\n")
        return 0

    def c_printenv(self, args, io):
        if not args:
            return self.c_env(args, io)
        code = 0
        for name in args:
            if name in self.exported and (name in self.vars or name == "PWD"):
                io.out.write((self._getvar(name) or "") + "\n")
            else:
                code = 1
        return code

    def c_seq(self, args, io):
        if not args:
            io.err.err("seq: missing operand\nTry 'seq --help' for more information.")
            return 1
        nums = []
        for a in args:
            if not re.fullmatch(r"-?\d+", a):
                io.err.err(f"seq: invalid floating point argument: '{a}'\nTry 'seq --help' for more information.")
                return 1
            nums.append(int(a))
        if len(nums) == 1:
            first, step, last = 1, 1, nums[0]
        elif len(nums) == 2:
            first, step, last = nums[0], 1, nums[1]
        else:
            first, step, last = nums[0], nums[1], nums[2]
        if step == 0:
            io.err.err("seq: invalid Zero increment value: '0'\nTry 'seq --help' for more information.")
            return 1
        values = range(first, last + (1 if step > 0 else -1), step)
        if len(values) > 100000:
            io.err.err(self.st("too_many"), "yellow")
            return 1
        io.out.write("".join(f"{v}\n" for v in values))
        return 0

    def c_basename(self, args, io):
        if not args:
            io.err.err("basename: missing operand\nTry 'basename --help' for more information.")
            return 1
        name = args[0].rstrip("/") or "/"
        base = posixpath.basename(name) or "/"
        if len(args) > 1 and base.endswith(args[1]) and base != args[1]:
            base = base[:-len(args[1])]
        io.out.write(base + "\n")
        return 0

    def c_dirname(self, args, io):
        if not args:
            io.err.err("dirname: missing operand\nTry 'dirname --help' for more information.")
            return 1
        for a in args:
            d = posixpath.dirname(a.rstrip("/")) or "."
            io.out.write(d + "\n")
        return 0

    def c_clear(self, args, io):
        return 0

    def c_sleep(self, args, io):
        if not args or not re.fullmatch(r"\d+(\.\d+)?[smhd]?", args[0]):
            io.err.err("sleep: missing operand\nTry 'sleep --help' for more information." if not args else
                       f"sleep: invalid time interval '{args[0]}'\nTry 'sleep --help' for more information.")
            return 1
        return 0

    def c_date(self, args, io):
        when = datetime.fromtimestamp(self._now(), SHELL_TZ)
        fmt = args[0][1:] if args and args[0].startswith("+") else "%a %b %e %H:%M:%S %Z %Y"
        table = {
            "Y": f"{when.year}", "m": f"{when.month:02d}", "d": f"{when.day:02d}", "H": f"{when.hour:02d}",
            "M": f"{when.minute:02d}", "S": f"{when.second:02d}", "a": DAYS[when.weekday()],
            "A": DAYS_LONG[when.weekday()], "b": MONTHS[when.month - 1], "B": MONTHS_LONG[when.month - 1],
            "e": f"{when.day:>2}", "Z": "+03", "z": "+0300", "j": f"{when.timetuple().tm_yday:03d}",
            "s": str(self._now()), "%": "%", "y": f"{when.year % 100:02d}",
        }
        table["F"] = f"{table['Y']}-{table['m']}-{table['d']}"
        table["T"] = f"{table['H']}:{table['M']}:{table['S']}"
        text = re.sub(r"%(.)", lambda m: table.get(m.group(1), m.group(0)), fmt)
        io.out.write(text + "\n")
        return 0

    def c_which(self, args, io):
        code = 0
        for name in args:
            if name in EXTERNAL and self._system_in_path():
                io.out.write(f"/usr/bin/{name}\n")
                continue
            found = self._path_lookup(name)
            if found:
                io.out.write(found + "\n")
                continue
            io.err.err(f"which: no {name} in ({self._getvar('PATH') or ''})")
            code = 1
        return code

    def c_bash(self, args, io):
        if not args:
            io.err.err(self.st("new_shell"), "yellow")
            return 1
        if args[0] == "-c":
            if len(args) < 2:
                io.err.err("bash: -c: option requires an argument")
                return 2
            try:
                tree = parse(args[1])
            except ShellSyntax as exc:
                io.err.err(*self._syntax_text(exc, "bash: -c: line 1"))
                return 2
            saved = self._save()
            self.vars = {k: v for k, v in self.vars.items() if k in self.exported}
            self.params = args[3:]
            try:
                return self._exec(tree, io)
            except _Exit as exc:
                return exc.code
            finally:
                self._restore(saved)
        name = args[0]
        p = self.abspath(name)
        if p not in self.files:
            io.err.err(f"bash: {name}: " + ("Is a directory" if self._isdir(p) else "No such file or directory"))
            return 126 if self._isdir(p) else 127
        if not self._can(p, "r"):
            io.err.err(f"bash: {name}: Permission denied")
            return 126
        return self._run_file(p, name, args[1:], io)

    c_sh = c_bash

    def c_git(self, args, io):
        from .git_sim import GitError, Out

        gout = Out()
        try:
            code = self.git(args, gout)
        except GitError as exc:
            for text, color in gout.lines:
                io.out.write(text + "\n", color)
            # Out'taki gibi: metnin sonundaki boş satır da korunuyor.
            io.err.err(exc.text + "\n", "red" if exc.text.startswith(("fatal", "error")) else "")
            return exc.code
        for text, color in gout.lines:
            io.out.write(text + "\n", color)
        return code
