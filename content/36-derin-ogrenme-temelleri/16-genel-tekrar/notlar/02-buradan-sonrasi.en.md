## After this module

All the networks in this module were **fully connected**: every input number
is connected to every neuron of the next layer. That is a natural choice for a
flat list of features, but it does not use the structure of data **that has
structure**, such as images, sound and text. The next two modules cover
networks that use that structure:

- **Computer Vision:** networks that process neighbouring pixels of an image
  together with convolution, data augmentation, transfer learning with
  pretrained models (the `strict=False` and freezing you saw in this module
  are useful there), object detection and segmentation.
- **Sequences, Generative Models and Deployment:** recurrent networks and the
  Transformer for sequential data (gradient clipping and LayerNorm are
  everywhere there), autoencoders and generative models, and speeding up,
  shrinking and serving a trained model.

## To try on your own

- Try the hidden layer of the digit classifier with 16, 64 and 256 neurons;
  how do the validation loss and the parameter count change?
- In the capstone, remove the dropout, then add `weight_decay`; at which epoch
  does early stopping kick in?
- On the table data, try learning rates from 0.001 to 1, growing tenfold each
  time, and run the single-batch memorising test with each.
- Load a small CSV dataset of your choice with a `Dataset` class and train it
  with the `fit` skeleton from the Quick Reference.

## Three things to remember

- Look at the numbers first: shape, type, starting loss.
- The validation set is for choosing; the test set is used once, at the end.
- Load a model file only with `weights_only=True`.
