## Command not found

A message such as `rustc : The term 'rustc' is not recognized` means installation finished but
the terminal does not know yet. Rust's folder is `%USERPROFILE%\.cargo\bin`, and only programs
opened **after** the installation can see it.

1. Close and reopen the terminal. Do the same for Odyssey.
2. If that does not help, restart the computer.
3. If it is still missing, installation stopped half way: run `rustup-init.exe` again.

## Linker not found

The message `linker link.exe not found` says the compiler is installed but the part that assembles
the program is missing. That part comes with Visual Studio; this step may have been skipped during
installation. Run `rustup-init.exe` again and accept the Visual Studio step. Detailed instructions:
`https://rust-lang.github.io/rustup/installation/windows-msvc.html`.

## The program compiles but Windows blocks it

On Windows 11, if Smart App Control is on, it may block newly produced, unsigned programs on your
computer. Odyssey then says "Windows blocked the compiled program". Your code is not wrong. This is
a security setting of your computer and the decision is yours.

## Useful rustup commands

| Command | What it does |
|---|---|
| `rustup update` | Upgrades Rust to the latest version |
| `rustup show` | Shows which version is in use |
| `rustup doc` | Opens the local documentation in a browser, no internet needed |
| `rustup self uninstall` | Removes Rust from the computer |

`rustup doc` is especially valuable: the official book (*The Rust Programming Language*) and the full
standard library documentation arrive on your computer with the installation.

## Editor

You do not need a separate editor for Odyssey's exercises. For your own projects, VS Code with the
`rust-analyzer` extension is a common choice: it shows errors as you type and writes types above the line.
