## Common problems

| Symptom | Cause | Fix |
|---|---|---|
| `could not determine which binary to run` | There are several programs | `--bin name` or `default-run` |
| `cargo run` does not work at the root | The workspace has several programs | `-p name` |
| `use core::...` is not found in a member | No `path` in `[dependencies]` | `core = { path = "../core" }` |
| An error in a disabled feature is not visible | That code was not compiled | Also compile with `--all-features` |
| Turning a feature on broke something else | The feature is not additive | Keep the two paths from cancelling each other |
| The build script runs every time | No `rerun-if-changed` | Add the line |
| `env!` does not compile: `not defined` | No value was given | Check `build.rs` and its spelling |

## When a workspace?

| Case | Decision |
|---|---|
| One program, a few modules | No workspace; modules are enough |
| A library + a program | One package is enough (`lib.rs` + `main.rs`) |
| Parts published separately | A workspace |
| Builds got long, and parts are independent | A workspace: an unchanged member is not recompiled |

Do not split from the start. Begin with modules; move to a crate when the boundary is clear. Going from a module to a crate later is easy, and undoing a wrong boundary is hard.

## Feature names

| Good | Why |
|---|---|
| `json`, `tls` | It says what it adds |
| `std` instead of `no-std` | A feature adds; `std` is on by default |

Reversed names (`no-color`) break the rule: if one of two dependencies asks for it, it is off for everyone.
