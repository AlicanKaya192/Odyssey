In this module we did everything with small data we generated ourselves and
on the processor: the ideas stay the same, the scale grows. When moving to
real projects:

## Real data sets

- **Classification:** MNIST and Fashion-MNIST (28 × 28 grey), CIFAR-10
  (32 × 32 colour, 10 classes), ImageNet (a thousand classes, millions of
  pictures; most ready-made networks were trained on it).
- **Detection and segmentation:** Pascal VOC (20 classes), COCO (80 classes,
  boxes and masks; the "COCO-style" multi-threshold form of AP comes from
  here).
- `torchvision.datasets` downloads most of them in one line; downloading
  needs the internet and can take gigabytes. Check the licence before
  downloading.

## Pretrained weights

In this module we used `resnet18(weights=None)`. In a real project, weights
trained on ImageNet are usually downloaded with `weights="DEFAULT"`; transfer
learning shows its real power then. The preprocessing those weights expect
(size, normalisation values) comes with the weights: `weights.transforms()`.

## Ready-made detectors and segmenters

- `torchvision.models.detection`: Faster R-CNN, RetinaNet, FCOS
  (anchor-free), SSD. Their outputs are in this module's format: `boxes`
  (xyxy), `scores`, `labels`.
- `torchvision.models.segmentation`: FCN, DeepLabV3; Mask R-CNN for instance
  segmentation.
- Ready-made libraries of the YOLO family are fast, but mind their licences:
  some come with licences (such as AGPL) that require you to open your own
  code too.

## Training faster

- **GPU:** `model.to("cuda")` and `.to("cuda")` for each batch. The code
  stays the same; tens of times faster on big networks.
- **Mixed precision** (`torch.autocast`): memory halves, speed rises.
- Loading data in parallel: `DataLoader(..., num_workers=4)`.

## Going to production

- When saving the model, the settings along with the weights: class names,
  preprocessing, thresholds.
- Exporting to ONNX to run in other environments (`torch.onnx.export`).
- In the real world data drifts (light, camera, season): the model must be
  measured regularly on new data. For a suspected shortcut, the methods in
  the Explaining a Model section.

## Next step

The next module of the Deep Learning track, **Sequences, Generative Models
and Deployment**, builds on this one: sequence models, generative models and
speeding up, exporting and serving a trained model.
