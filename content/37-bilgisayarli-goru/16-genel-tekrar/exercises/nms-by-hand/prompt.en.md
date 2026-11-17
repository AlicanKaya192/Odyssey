`nms_by_hand(boxes, scores, threshold)` should apply NMS to xyxy boxes and
return the positions of the kept boxes in score order (high to low): a box is
kept if its IoU with every kept box is not above the threshold. Do not use
torchvision's `nms`; compute the IoU yourself.

**Expected output:**

```
[3, 2]
[3, 0, 1, 2]
```
