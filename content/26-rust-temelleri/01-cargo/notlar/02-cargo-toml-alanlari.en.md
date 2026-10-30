## The package heading

| Field | Example | Note |
|---|---|---|
| `name` | `"todo-cli"` | Lowercase and hyphens are common |
| `version` | `"1.2.3"` | Major, minor, patch parts |
| `edition` | `"2024"` | If omitted, the oldest rules (2015) apply |
| `description` | `"Short text"` | Needed when publishing a package |
| `license` | `"MIT"` | Needed when publishing a package |
| `rust-version` | `"1.85"` | The lowest supported compiler |

## How is a version written?

The version you write for a dependency is a range, not a single version:

| Written | Accepted |
|---|---|
| `"1.2.3"` | 1.2.3 and above, below 2.0.0 |
| `"1.2"` | 1.2.0 and above, below 2.0.0 |
| `"1"` | 1.0.0 and above, below 2.0.0 |
| `"=1.2.3"` | Only 1.2.3 |

The rule is **semantic versioning** (semver): as long as the major number stays the same, old code should keep working.

## If you forget the edition

If `edition` is missing, Cargo warns and uses the oldest edition. Then words such as `async` are not
recognised and you see odd errors. One of this section's exercises shows exactly this.

## Values Cargo provides at compile time

They can be read with `env!`:

| Name | Value |
|---|---|
| `CARGO_PKG_NAME` | `name` |
| `CARGO_PKG_VERSION` | `version` |
| `CARGO_PKG_DESCRIPTION` | `description` |
