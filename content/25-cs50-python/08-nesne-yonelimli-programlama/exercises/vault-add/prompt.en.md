A Gringotts vault: `Vault(galleons=0, sickles=0, knuts=0)` stores the three coin counts in instance variables of the same names; `__str__` returns `100 Galleons, 50 Sickles, 25 Knuts`. Write `__add__` so that two vaults can be added with `+`: the result is a **new** `Vault` with each count added separately; neither vault changes.

Odyssey checks your class by really creating it and calling its methods; you may write test code at the end of the file.
