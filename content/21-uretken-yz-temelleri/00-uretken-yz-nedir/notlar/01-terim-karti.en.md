| Term | Meaning |
|---|---|
| **Generative model** | A model that learns the distribution of the data and can produce new examples from it |
| **Discriminative model** | A model that only answers "what is this example's label?", $p(y \mid x)$ |
| **Distribution** | A description of which values appear and how often |
| **Sampling** | Drawing values that are random but fit a distribution |
| **Seed** | The starting number of a random generator; the same seed gives the same result |
| **Normal distribution** (Gaussian) | A bell-shaped distribution set by a mean and a covariance |
| **Covariance matrix** | How the measurements spread and change together |
| **Likelihood** (probability density) | A measure of how well an example fits a distribution |
| **Prior** | A class's overall share before looking at the data |
| **Memorisation** | The model returning training examples almost verbatim |
| **Nearest neighbour distance** | The distance from a generated sample to the closest training example; close to 0 means a copy |

**Keep in mind:**

- A generative model can also be used as a classifier; not the other way
  round.
- In generation there is no "right answer". Look at the statistics of many
  samples, not at single samples.
- A sample that looks very real is not always good: it may be a copy of the
  training data.
- The same seed gives the same samples. That is why the seed is fixed when
  outputs are compared.
