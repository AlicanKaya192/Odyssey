## Concepts

| Concept | Meaning |
|---|---|
| Direct dependency | A package you install explicitly |
| Transitive dependency | The packages your packages use |
| SBOM | The list of every package used |
| Pinning | Writing the exact version: `package==1.2.3` |
| Lock file | Version + file hash; a reproducible installation |
| Security advisory | Which versions are affected, which one fixed it |
| Typosquatting | A malicious package named like a popular one |
| Dependency confusion | An internal package name imitated on a public index |

## Ways of writing requirements.txt

| Line | Meaning | Pinned? |
|---|---|---|
| `numpy==2.1.3` | Exactly this version | Yes |
| `pandas>=2.0` | 2.0 or newer | No |
| `flask~=3.0` | The newest within 3.x | No |
| `flask` | Whatever comes | No |
| `# comment` | Ignored | — |

## Python patterns

- Separating the package name: `re.split(r"[<>=!~ ;\[]", line)[0]`.
- Is it pinned: `"==" in line`.
- Transitive dependencies: a stack + a `seen` set (against cycles).
- Is it affected: `version(introduced) <= version(installed) < version(fixed)`.
- A similar name: `difflib.get_close_matches(name, popular, n=1, cutoff=0.8)`.
- A file hash: `hashlib.sha256(data).hexdigest()`.

## Keep in mind

- A package's vulnerability is your vulnerability, transitive ones
  included.
- A pinned version does not update itself; updating is a regular job.
- Pinning without a hash does not prove the file has not changed.
- Every new dependency is reviewed by a human.
