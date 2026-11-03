Every line added for a package brings someone else's code into your
program. Most packages are trustworthy, and not reinventing the wheel is a
sound decision. But that decision is made once and deliberately; "I
installed it and it worked" is not enough.

## Before adding a new package

| Question | Why? |
|---|---|
| Is it really needed? Could it be written in a few lines? | Every package is a risk and a maintenance load |
| Is its name spelled right? | Malicious lookalike packages exist |
| Is it still maintained? When was the last release? | An abandoned package's vulnerabilities never close |
| How many people use it, who develops it? | A community notices problems |
| How many transitive dependencies does it bring? | One package may be dozens |
| Does its licence suit the project? | Legal risk is a risk too |
| Does it have known vulnerabilities? | Look at the dependency scan |

## Update policy

Pinned versions do not update themselves; that is why a policy is needed:

- **Security updates at once:** when a critical advisory arrives, the
  package involved is updated first (the Patch Management note).
- **Other updates regularly:** for example once a month, with tests, in
  small steps.
- **The lock file is regenerated on every update** and the change goes
  through code review: which package, from which version to which.

## In the build pipeline

1. Installation is done from the lock file with hash verification.
2. Dependency scanning runs on every change; a critical finding blocks the
   merge.
3. An SBOM is produced and kept with every release: when a new
   vulnerability is announced, "which of our releases are affected?" is
   answered in minutes.
4. Which index internal packages come from is written explicitly in the
   configuration.

## Trust, but verify

The account of a popular package's developer can be taken over and a
malicious version published. That is why even with the most trusted
package, moving to a new version is a reviewed change, not a blind step.
Packages that run install scripts and unexpected new transitive
dependencies need particular attention.
