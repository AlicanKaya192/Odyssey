**Idea:** "If–then" means subset: $p \Rightarrow q$ is true if "the cases where $p$ holds" lie inside "the cases where $q$ holds". Here there is a single case, in which $p$ is true and $q$ false.

**Step 1 — The case sets.** Our single case is in $p$'s set and not in $q$'s.

**Step 2 — Intersection and union.** The case is not in both: $p \wedge q = 0$. It is in at least one: $p \vee q = 1$.

**Step 3 — Subset.** $p$'s set is $\{\text{case}\}$, $q$'s is empty: $\{\text{case}\} \subseteq \emptyset$ is false, $p \Rightarrow q = 0$. The other way, $\emptyset \subseteq \{\text{case}\}$ is true (the empty set is a subset of every set): $q \Rightarrow p = 1$.

**Why the same result?** Logic and sets are one language: "and" is intersection, "or" union, "if–then" subset. That a false premise implies anything is the logical counterpart of the empty set being a subset of every set.

**Answer:** $0$, $1$, $0$, $1$.
