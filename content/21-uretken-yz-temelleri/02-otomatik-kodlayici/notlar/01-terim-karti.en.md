| Term | Meaning |
|---|---|
| **Autoencoder** | A network that learns to compress its input into a narrow code and rebuild the same input |
| **Encoder** | The half that reduces the input to the code |
| **Decoder** | The half that rebuilds the input from the code |
| **Code** / **latent code** | The few numbers in the bottleneck |
| **Latent space** | The space of all possible codes; if it is 2-dimensional it can be drawn on a plane |
| **Reconstruction error** | The difference between input and output, here the mean squared error |
| **Unsupervised learning** | Learning structure from data without labels |
| **PCA** | A linear method that projects the data onto the directions in which it spreads most; like a linear autoencoder |
| **Momentum** | Each update carrying part of the previous update; speeds training up |
| **Denoising** | Passing a noisy input through the code to recover the shared structure |
| **Anomaly detection** | Flagging an example that is rebuilt badly as "different" |

**Keep in mind:**

- The code must be narrow; a wide code memorises everything and learns
  nothing.
- An autoencoder is good at compressing and weak at **generating**: the latent
  space has gaps and a random code often gives a meaningless image (in the
  section the share of clear digits was 32%, against 69% for real ones).
- The non-linear network beat PCA (with a 2-dimensional code 0.0539 →
  0.0393), but the price is long training.
