All the models in this module were trained in seconds on a laptop's
processor. That was a deliberate choice: to be able to run every line and see
its result. In real projects the same ideas are applied at a larger scale. A
few directions to go from here:

## Larger models, a graphics card

- **A graphics card:** the device-independent code from the Performance
  section runs unchanged on a GPU; with large batches and
  `autocast("cuda", float16)` training gets tens of times faster.
- **Pretrained models:** ready models with millions of parameters for
  language and images are downloaded and fine-tuned. In this module we did not
  download weights; the idea in the LoRA section is exactly for such models.
- **Distributed training:** models that do not fit in a single card's memory
  are split over several cards (`torch.distributed`).

## Better generative models

- **Diffusion models:** we saw the idea in the Generative AI Fundamentals
  module; they have largely replaced GANs in image generation. In PyTorch they
  are built with a U-Net and a noise schedule.
- **Language models:** the Transformer block from the Embeddings and Language
  Models module, stacked and trained on very large text, is the basis of
  today's language models.

## Operating a model

- **Serving a model:** the "Serving an ML Model" section of the Writing REST
  APIs with FastAPI module puts the prediction function from the
  Reproducibility section behind a web endpoint.
- **Packaging:** the Docker track explains putting the model and its
  dependencies into an image.
- **Monitoring and refreshing:** the MLOps and ML System Design module
  covers watching a live model for data drift and safely releasing a new
  version.

## Your own project

The best next step is a small project with your own data: a sensor, a text
collection, a time series. Follow the order of the capstone: get to know the
data, set a simple rule, train the model, evaluate it with the right measure,
prepare a delivery package. Measure the result at every step; do not guess.
