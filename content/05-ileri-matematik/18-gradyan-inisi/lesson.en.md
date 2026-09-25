# Gradient Descent

The previous sections prepared the pieces one by one: the derivative
shows the direction, the gradient the steepest way, Taylor why the step
must be small, convexity where we will end up. **Gradient descent**
combines them into a single algorithm, and behind almost every model
trained today there is this algorithm or one of its relatives.

In this section we will look at the algorithm, the effect of the learning
rate, the speed of convergence, the stochastic and mini-batch versions,
and improvements such as momentum and Adam.

Prerequisite: the Partial Derivatives and the Gradient, Jacobian and
Hessian, and Convexity sections.

## The algorithm

Choose a starting point $\mathbf{w}_0$ and repeat:

$$
\mathbf{w}_{k+1} = \mathbf{w}_k - \eta \, \nabla L(\mathbf{w}_k)
$$

$\eta$ is the **learning rate** (the step size). Stopping criteria: the
gradient has become very small, the loss no longer drops meaningfully,
or a set number of steps has been taken.

A one-variable example: $L(w) = (w - 4)^2$, $w_0 = 0$, $\eta = 0.25$.
$L'(w) = 2(w - 4)$:

| $k$ | $w_k$ | $L'(w_k)$ | $w_{k+1}$ |
|---|---|---|---|
| $0$ | $0$ | $-8$ | $2$ |
| $1$ | $2$ | $-4$ | $3$ |
| $2$ | $3$ | $-2$ | $3.5$ |

At each step the distance to the best point ($w = 4$) halves.

## The learning rate

For $L(w) = w^2$ the step is $w_{k+1} = w_k - 2\eta w_k = (1 - 2\eta)\,w_k$.
The distance is multiplied by $1 - 2\eta$ at each step:

<figure class="fig">
<svg viewBox="0 0 465 216" width="465"><line class="grid" x1="30.6" y1="170.0" x2="30.6" y2="20.0"/><line class="grid" x1="56.5" y1="170.0" x2="56.5" y2="20.0"/><line class="grid" x1="82.5" y1="170.0" x2="82.5" y2="20.0"/><line class="grid" x1="108.5" y1="170.0" x2="108.5" y2="20.0"/><line class="grid" x1="134.4" y1="170.0" x2="134.4" y2="20.0"/><line class="grid" x1="15.0" y1="163.4" x2="150.0" y2="163.4"/><line class="grid" x1="15.0" y1="141.3" x2="150.0" y2="141.3"/><line class="grid" x1="15.0" y1="119.3" x2="150.0" y2="119.3"/><line class="grid" x1="15.0" y1="97.2" x2="150.0" y2="97.2"/><line class="grid" x1="15.0" y1="75.1" x2="150.0" y2="75.1"/><line class="grid" x1="15.0" y1="53.1" x2="150.0" y2="53.1"/><line class="grid" x1="15.0" y1="31.0" x2="150.0" y2="31.0"/><line class="line" x1="15.0" y1="163.4" x2="150.0" y2="163.4"/><line class="line" x1="82.5" y1="170.0" x2="82.5" y2="20.0"/><polyline class="curve" fill="none" points="16.1,19.2 16.7,21.6 17.2,24.0 17.8,26.4 18.4,28.8 18.9,31.2 19.5,33.5 20.1,35.8 20.6,38.1 21.2,40.3 21.8,42.6 22.3,44.8 22.9,47.0 23.4,49.2 24.0,51.4 24.6,53.5 25.1,55.6 25.7,57.7 26.2,59.8 26.8,61.9 27.4,63.9 27.9,65.9 28.5,67.9 29.1,69.9 29.6,71.9 30.2,73.8 30.8,75.7 31.3,77.6 31.9,79.5 32.4,81.4 33.0,83.2 33.6,85.0 34.1,86.8 34.7,88.6 35.2,90.3 35.8,92.0 36.4,93.8 36.9,95.4 37.5,97.1 38.1,98.8 38.6,100.4 39.2,102.0 39.8,103.6 40.3,105.1 40.9,106.7 41.4,108.2 42.0,109.7 42.6,111.2 43.1,112.6 43.7,114.1 44.2,115.5 44.8,116.9 45.4,118.3 45.9,119.6 46.5,121.0 47.1,122.3 47.6,123.6 48.2,124.8 48.8,126.1 49.3,127.3 49.9,128.5 50.4,129.7 51.0,130.9 51.6,132.1 52.1,133.2 52.7,134.3 53.2,135.4 53.8,136.4 54.4,137.5 54.9,138.5 55.5,139.5 56.1,140.5 56.6,141.5 57.2,142.4 57.8,143.3 58.3,144.2 58.9,145.1 59.4,146.0 60.0,146.8 60.6,147.6 61.1,148.4 61.7,149.2 62.2,150.0 62.8,150.7 63.4,151.4 63.9,152.1 64.5,152.8 65.1,153.4 65.6,154.1 66.2,154.7 66.8,155.3 67.3,155.8 67.9,156.4 68.4,156.9 69.0,157.4 69.6,157.9 70.1,158.4 70.7,158.8 71.2,159.2 71.8,159.6 72.4,160.0 72.9,160.4 73.5,160.7 74.1,161.1 74.6,161.4 75.2,161.6 75.8,161.9 76.3,162.1 76.9,162.3 77.4,162.5 78.0,162.7 78.6,162.9 79.1,163.0 79.7,163.1 80.3,163.2 80.8,163.3 81.4,163.3 81.9,163.4 82.5,163.4 83.1,163.4 83.6,163.3 84.2,163.3 84.8,163.2 85.3,163.1 85.9,163.0 86.4,162.9 87.0,162.7 87.6,162.5 88.1,162.3 88.7,162.1 89.2,161.9 89.8,161.6 90.4,161.4 90.9,161.1 91.5,160.7 92.1,160.4 92.6,160.0 93.2,159.6 93.7,159.2 94.3,158.8 94.9,158.4 95.4,157.9 96.0,157.4 96.6,156.9 97.1,156.4 97.7,155.8 98.2,155.3 98.8,154.7 99.4,154.1 99.9,153.4 100.5,152.8 101.1,152.1 101.6,151.4 102.2,150.7 102.8,150.0 103.3,149.2 103.9,148.4 104.4,147.6 105.0,146.8 105.6,146.0 106.1,145.1 106.7,144.2 107.2,143.3 107.8,142.4 108.4,141.5 108.9,140.5 109.5,139.5 110.1,138.5 110.6,137.5 111.2,136.4 111.8,135.4 112.3,134.3 112.9,133.2 113.4,132.1 114.0,130.9 114.6,129.7 115.1,128.5 115.7,127.3 116.2,126.1 116.8,124.8 117.4,123.6 117.9,122.3 118.5,121.0 119.1,119.6 119.6,118.3 120.2,116.9 120.8,115.5 121.3,114.1 121.9,112.6 122.4,111.2 123.0,109.7 123.6,108.2 124.1,106.7 124.7,105.1 125.3,103.6 125.8,102.0 126.4,100.4 126.9,98.8 127.5,97.1 128.1,95.4 128.6,93.8 129.2,92.0 129.8,90.3 130.3,88.6 130.9,86.8 131.4,85.0 132.0,83.2 132.6,81.4 133.1,79.5 133.7,77.6 134.2,75.7 134.8,73.8 135.4,71.9 135.9,69.9 136.5,67.9 137.1,65.9 137.6,63.9 138.2,61.9 138.8,59.8 139.3,57.7 139.9,55.6 140.4,53.5 141.0,51.4 141.6,49.2 142.1,47.0 142.7,44.8 143.2,42.6 143.8,40.3 144.4,38.1 144.9,35.8 145.5,33.5 146.1,31.2 146.6,28.8 147.2,26.4 147.8,24.0 148.3,21.6 148.9,19.2"/><line class="curve2" stroke-width="1.8" x1="129.2" y1="91.9" x2="119.9" y2="117.6"/><line class="curve2" stroke-width="1.8" x1="119.9" y1="117.6" x2="112.4" y2="134.1"/><line class="curve2" stroke-width="1.8" x1="112.4" y1="134.1" x2="106.4" y2="144.6"/><line class="curve2" stroke-width="1.8" x1="106.4" y1="144.6" x2="101.6" y2="151.4"/><line class="curve2" stroke-width="1.8" x1="101.6" y1="151.4" x2="97.8" y2="155.7"/><line class="curve2" stroke-width="1.8" x1="97.8" y1="155.7" x2="94.8" y2="158.5"/><circle class="dot3" cx="129.2" cy="91.9" r="4"/><circle class="dot2" cx="119.9" cy="117.6" r="3"/><circle class="dot2" cx="112.4" cy="134.1" r="3"/><circle class="dot2" cx="106.4" cy="144.6" r="3"/><circle class="dot2" cx="101.6" cy="151.4" r="3"/><circle class="dot2" cx="97.8" cy="155.7" r="3"/><circle class="dot2" cx="94.8" cy="158.5" r="3"/><text class="ink" x="82" y="190" font-size="11" text-anchor="middle">η = 0.1: slow</text><text class="dim" x="82" y="206" font-size="10" text-anchor="middle">0.8 times per step</text><line class="grid" x1="180.6" y1="170.0" x2="180.6" y2="20.0"/><line class="grid" x1="206.5" y1="170.0" x2="206.5" y2="20.0"/><line class="grid" x1="232.5" y1="170.0" x2="232.5" y2="20.0"/><line class="grid" x1="258.5" y1="170.0" x2="258.5" y2="20.0"/><line class="grid" x1="284.4" y1="170.0" x2="284.4" y2="20.0"/><line class="grid" x1="165.0" y1="163.4" x2="300.0" y2="163.4"/><line class="grid" x1="165.0" y1="141.3" x2="300.0" y2="141.3"/><line class="grid" x1="165.0" y1="119.3" x2="300.0" y2="119.3"/><line class="grid" x1="165.0" y1="97.2" x2="300.0" y2="97.2"/><line class="grid" x1="165.0" y1="75.1" x2="300.0" y2="75.1"/><line class="grid" x1="165.0" y1="53.1" x2="300.0" y2="53.1"/><line class="grid" x1="165.0" y1="31.0" x2="300.0" y2="31.0"/><line class="line" x1="165.0" y1="163.4" x2="300.0" y2="163.4"/><line class="line" x1="232.5" y1="170.0" x2="232.5" y2="20.0"/><polyline class="curve" fill="none" points="166.1,19.2 166.7,21.6 167.2,24.0 167.8,26.4 168.4,28.8 168.9,31.2 169.5,33.5 170.1,35.8 170.6,38.1 171.2,40.3 171.8,42.6 172.3,44.8 172.9,47.0 173.4,49.2 174.0,51.4 174.6,53.5 175.1,55.6 175.7,57.7 176.2,59.8 176.8,61.9 177.4,63.9 177.9,65.9 178.5,67.9 179.1,69.9 179.6,71.9 180.2,73.8 180.8,75.7 181.3,77.6 181.9,79.5 182.4,81.4 183.0,83.2 183.6,85.0 184.1,86.8 184.7,88.6 185.2,90.3 185.8,92.0 186.4,93.8 186.9,95.4 187.5,97.1 188.1,98.8 188.6,100.4 189.2,102.0 189.8,103.6 190.3,105.1 190.9,106.7 191.4,108.2 192.0,109.7 192.6,111.2 193.1,112.6 193.7,114.1 194.2,115.5 194.8,116.9 195.4,118.3 195.9,119.6 196.5,121.0 197.1,122.3 197.6,123.6 198.2,124.8 198.8,126.1 199.3,127.3 199.9,128.5 200.4,129.7 201.0,130.9 201.6,132.1 202.1,133.2 202.7,134.3 203.2,135.4 203.8,136.4 204.4,137.5 204.9,138.5 205.5,139.5 206.1,140.5 206.6,141.5 207.2,142.4 207.8,143.3 208.3,144.2 208.9,145.1 209.4,146.0 210.0,146.8 210.6,147.6 211.1,148.4 211.7,149.2 212.2,150.0 212.8,150.7 213.4,151.4 213.9,152.1 214.5,152.8 215.1,153.4 215.6,154.1 216.2,154.7 216.8,155.3 217.3,155.8 217.9,156.4 218.4,156.9 219.0,157.4 219.6,157.9 220.1,158.4 220.7,158.8 221.2,159.2 221.8,159.6 222.4,160.0 222.9,160.4 223.5,160.7 224.1,161.1 224.6,161.4 225.2,161.6 225.8,161.9 226.3,162.1 226.9,162.3 227.4,162.5 228.0,162.7 228.6,162.9 229.1,163.0 229.7,163.1 230.2,163.2 230.8,163.3 231.4,163.3 231.9,163.4 232.5,163.4 233.1,163.4 233.6,163.3 234.2,163.3 234.8,163.2 235.3,163.1 235.9,163.0 236.4,162.9 237.0,162.7 237.6,162.5 238.1,162.3 238.7,162.1 239.2,161.9 239.8,161.6 240.4,161.4 240.9,161.1 241.5,160.7 242.1,160.4 242.6,160.0 243.2,159.6 243.8,159.2 244.3,158.8 244.9,158.4 245.4,157.9 246.0,157.4 246.6,156.9 247.1,156.4 247.7,155.8 248.2,155.3 248.8,154.7 249.4,154.1 249.9,153.4 250.5,152.8 251.1,152.1 251.6,151.4 252.2,150.7 252.8,150.0 253.3,149.2 253.9,148.4 254.4,147.6 255.0,146.8 255.6,146.0 256.1,145.1 256.7,144.2 257.2,143.3 257.8,142.4 258.4,141.5 258.9,140.5 259.5,139.5 260.1,138.5 260.6,137.5 261.2,136.4 261.8,135.4 262.3,134.3 262.9,133.2 263.4,132.1 264.0,130.9 264.6,129.7 265.1,128.5 265.7,127.3 266.2,126.1 266.8,124.8 267.4,123.6 267.9,122.3 268.5,121.0 269.1,119.6 269.6,118.3 270.2,116.9 270.8,115.5 271.3,114.1 271.9,112.6 272.4,111.2 273.0,109.7 273.6,108.2 274.1,106.7 274.7,105.1 275.2,103.6 275.8,102.0 276.4,100.4 276.9,98.8 277.5,97.1 278.1,95.4 278.6,93.8 279.2,92.0 279.8,90.3 280.3,88.6 280.9,86.8 281.4,85.0 282.0,83.2 282.6,81.4 283.1,79.5 283.7,77.6 284.2,75.7 284.8,73.8 285.4,71.9 285.9,69.9 286.5,67.9 287.1,65.9 287.6,63.9 288.2,61.9 288.8,59.8 289.3,57.7 289.9,55.6 290.4,53.5 291.0,51.4 291.6,49.2 292.1,47.0 292.7,44.8 293.2,42.6 293.8,40.3 294.4,38.1 294.9,35.8 295.5,33.5 296.1,31.2 296.6,28.8 297.2,26.4 297.8,24.0 298.3,21.6 298.9,19.2"/><line class="curve2" stroke-width="1.8" x1="279.2" y1="91.9" x2="241.8" y2="160.5"/><line class="curve2" stroke-width="1.8" x1="241.8" y1="160.5" x2="234.4" y2="163.3"/><line class="curve2" stroke-width="1.8" x1="234.4" y1="163.3" x2="232.9" y2="163.4"/><line class="curve2" stroke-width="1.8" x1="232.9" y1="163.4" x2="232.6" y2="163.4"/><line class="curve2" stroke-width="1.8" x1="232.6" y1="163.4" x2="232.5" y2="163.4"/><line class="curve2" stroke-width="1.8" x1="232.5" y1="163.4" x2="232.5" y2="163.4"/><circle class="dot3" cx="279.2" cy="91.9" r="4"/><circle class="dot2" cx="241.8" cy="160.5" r="3"/><circle class="dot2" cx="234.4" cy="163.3" r="3"/><circle class="dot2" cx="232.9" cy="163.4" r="3"/><circle class="dot2" cx="232.6" cy="163.4" r="3"/><circle class="dot2" cx="232.5" cy="163.4" r="3"/><circle class="dot2" cx="232.5" cy="163.4" r="3"/><text class="ink" x="232" y="190" font-size="11" text-anchor="middle">η = 0.4: good</text><text class="dim" x="232" y="206" font-size="10" text-anchor="middle">0.2 times per step</text><line class="grid" x1="330.6" y1="170.0" x2="330.6" y2="20.0"/><line class="grid" x1="356.5" y1="170.0" x2="356.5" y2="20.0"/><line class="grid" x1="382.5" y1="170.0" x2="382.5" y2="20.0"/><line class="grid" x1="408.5" y1="170.0" x2="408.5" y2="20.0"/><line class="grid" x1="434.4" y1="170.0" x2="434.4" y2="20.0"/><line class="grid" x1="315.0" y1="163.4" x2="450.0" y2="163.4"/><line class="grid" x1="315.0" y1="141.3" x2="450.0" y2="141.3"/><line class="grid" x1="315.0" y1="119.3" x2="450.0" y2="119.3"/><line class="grid" x1="315.0" y1="97.2" x2="450.0" y2="97.2"/><line class="grid" x1="315.0" y1="75.1" x2="450.0" y2="75.1"/><line class="grid" x1="315.0" y1="53.1" x2="450.0" y2="53.1"/><line class="grid" x1="315.0" y1="31.0" x2="450.0" y2="31.0"/><line class="line" x1="315.0" y1="163.4" x2="450.0" y2="163.4"/><line class="line" x1="382.5" y1="170.0" x2="382.5" y2="20.0"/><polyline class="curve" fill="none" points="316.1,19.2 316.7,21.6 317.2,24.0 317.8,26.4 318.4,28.8 318.9,31.2 319.5,33.5 320.1,35.8 320.6,38.1 321.2,40.3 321.8,42.6 322.3,44.8 322.9,47.0 323.4,49.2 324.0,51.4 324.6,53.5 325.1,55.6 325.7,57.7 326.2,59.8 326.8,61.9 327.4,63.9 327.9,65.9 328.5,67.9 329.1,69.9 329.6,71.9 330.2,73.8 330.8,75.7 331.3,77.6 331.9,79.5 332.4,81.4 333.0,83.2 333.6,85.0 334.1,86.8 334.7,88.6 335.2,90.3 335.8,92.0 336.4,93.8 336.9,95.4 337.5,97.1 338.1,98.8 338.6,100.4 339.2,102.0 339.8,103.6 340.3,105.1 340.9,106.7 341.4,108.2 342.0,109.7 342.6,111.2 343.1,112.6 343.7,114.1 344.2,115.5 344.8,116.9 345.4,118.3 345.9,119.6 346.5,121.0 347.1,122.3 347.6,123.6 348.2,124.8 348.8,126.1 349.3,127.3 349.9,128.5 350.4,129.7 351.0,130.9 351.6,132.1 352.1,133.2 352.7,134.3 353.2,135.4 353.8,136.4 354.4,137.5 354.9,138.5 355.5,139.5 356.1,140.5 356.6,141.5 357.2,142.4 357.8,143.3 358.3,144.2 358.9,145.1 359.4,146.0 360.0,146.8 360.6,147.6 361.1,148.4 361.7,149.2 362.2,150.0 362.8,150.7 363.4,151.4 363.9,152.1 364.5,152.8 365.1,153.4 365.6,154.1 366.2,154.7 366.8,155.3 367.3,155.8 367.9,156.4 368.4,156.9 369.0,157.4 369.6,157.9 370.1,158.4 370.7,158.8 371.2,159.2 371.8,159.6 372.4,160.0 372.9,160.4 373.5,160.7 374.1,161.1 374.6,161.4 375.2,161.6 375.8,161.9 376.3,162.1 376.9,162.3 377.4,162.5 378.0,162.7 378.6,162.9 379.1,163.0 379.7,163.1 380.2,163.2 380.8,163.3 381.4,163.3 381.9,163.4 382.5,163.4 383.1,163.4 383.6,163.3 384.2,163.3 384.8,163.2 385.3,163.1 385.9,163.0 386.4,162.9 387.0,162.7 387.6,162.5 388.1,162.3 388.7,162.1 389.2,161.9 389.8,161.6 390.4,161.4 390.9,161.1 391.5,160.7 392.1,160.4 392.6,160.0 393.2,159.6 393.8,159.2 394.3,158.8 394.9,158.4 395.4,157.9 396.0,157.4 396.6,156.9 397.1,156.4 397.7,155.8 398.2,155.3 398.8,154.7 399.4,154.1 399.9,153.4 400.5,152.8 401.1,152.1 401.6,151.4 402.2,150.7 402.8,150.0 403.3,149.2 403.9,148.4 404.4,147.6 405.0,146.8 405.6,146.0 406.1,145.1 406.7,144.2 407.2,143.3 407.8,142.4 408.4,141.5 408.9,140.5 409.5,139.5 410.1,138.5 410.6,137.5 411.2,136.4 411.8,135.4 412.3,134.3 412.9,133.2 413.4,132.1 414.0,130.9 414.6,129.7 415.1,128.5 415.7,127.3 416.2,126.1 416.8,124.8 417.4,123.6 417.9,122.3 418.5,121.0 419.1,119.6 419.6,118.3 420.2,116.9 420.8,115.5 421.3,114.1 421.9,112.6 422.4,111.2 423.0,109.7 423.6,108.2 424.1,106.7 424.7,105.1 425.2,103.6 425.8,102.0 426.4,100.4 426.9,98.8 427.5,97.1 428.1,95.4 428.6,93.8 429.2,92.0 429.8,90.3 430.3,88.6 430.9,86.8 431.4,85.0 432.0,83.2 432.6,81.4 433.1,79.5 433.7,77.6 434.2,75.7 434.8,73.8 435.4,71.9 435.9,69.9 436.5,67.9 437.1,65.9 437.6,63.9 438.2,61.9 438.8,59.8 439.3,57.7 439.9,55.6 440.4,53.5 441.0,51.4 441.6,49.2 442.1,47.0 442.7,44.8 443.2,42.6 443.8,40.3 444.4,38.1 444.9,35.8 445.5,33.5 446.1,31.2 446.6,28.8 447.2,26.4 447.8,24.0 448.3,21.6 448.9,19.2"/><line class="curve2" stroke-width="1.8" x1="429.2" y1="91.9" x2="331.1" y2="76.9"/><line class="curve2" stroke-width="1.8" x1="331.1" y1="76.9" x2="439.0" y2="58.7"/><line class="curve2" stroke-width="1.8" x1="439.0" y1="58.7" x2="320.3" y2="36.8"/><circle class="dot3" cx="429.2" cy="91.9" r="4"/><circle class="dot2" cx="331.1" cy="76.9" r="3"/><circle class="dot2" cx="439.0" cy="58.7" r="3"/><circle class="dot2" cx="320.3" cy="36.8" r="3"/><text class="ink" x="382" y="190" font-size="11" text-anchor="middle">η = 1.05: diverges</text><text class="dim" x="382" y="206" font-size="10" text-anchor="middle">−1.1 times per step</text></svg>
  <figcaption>The same parabola, the same start, three learning rates. A small rate is safe but slow; a well-chosen rate reaches the bottom in a few steps; a rate that is too large is thrown to both sides of the bottom and goes further out each time.</figcaption>
</figure>

| $\eta$ | $1 - 2\eta$ | Behaviour |
|---|---|---|
| $0.1$ | $0.8$ | slow, smooth descent |
| $0.5$ | $0$ | the bottom in one step |
| $0.9$ | $-0.8$ | descent that swings across the bottom |
| $1.05$ | $-1.1$ | divergence: the loss grows |

The general rule: on a parabola with curvature (second derivative)
$\lambda$, the factor is $1 - \eta\lambda$; for convergence
$\lvert 1 - \eta\lambda \rvert < 1$, that is,

$$
0 < \eta < \frac{2}{\lambda}
$$

With several variables $\lambda$ is replaced by the largest eigenvalue of
the Hessian: **the steepest direction sets the upper limit for the
learning rate.**

## Narrow valleys and zigzags

If the curvature of the loss differs greatly between directions (the
condition number is large), trouble starts. The learning rate has to be
small enough for the steep direction; that rate is far too small for the
gentle direction.

<figure class="fig">
<svg viewBox="0 0 470 202" width="470"><line class="grid" x1="20.0" y1="150.0" x2="20.0" y2="20.0"/><line class="grid" x1="40.0" y1="150.0" x2="40.0" y2="20.0"/><line class="grid" x1="60.0" y1="150.0" x2="60.0" y2="20.0"/><line class="grid" x1="80.0" y1="150.0" x2="80.0" y2="20.0"/><line class="grid" x1="100.0" y1="150.0" x2="100.0" y2="20.0"/><line class="grid" x1="120.0" y1="150.0" x2="120.0" y2="20.0"/><line class="grid" x1="140.0" y1="150.0" x2="140.0" y2="20.0"/><line class="grid" x1="160.0" y1="150.0" x2="160.0" y2="20.0"/><line class="grid" x1="180.0" y1="150.0" x2="180.0" y2="20.0"/><line class="grid" x1="200.0" y1="150.0" x2="200.0" y2="20.0"/><line class="grid" x1="220.0" y1="150.0" x2="220.0" y2="20.0"/><line class="grid" x1="20.0" y1="125.6" x2="220.0" y2="125.6"/><line class="grid" x1="20.0" y1="85.0" x2="220.0" y2="85.0"/><line class="grid" x1="20.0" y1="44.4" x2="220.0" y2="44.4"/><polyline class="curve3" fill="none" points="148.3,85.0 148.1,82.7 147.4,80.5 146.3,78.3 144.8,76.2 142.9,74.3 140.6,72.6 138.0,71.0 135.2,69.7 132.0,68.6 128.7,67.7 125.3,67.2 121.8,66.9 118.2,66.9 114.7,67.2 111.3,67.7 108.0,68.6 104.8,69.7 102.0,71.0 99.4,72.6 97.1,74.3 95.2,76.2 93.7,78.3 92.6,80.5 91.9,82.7 91.7,85.0 91.9,87.3 92.6,89.5 93.7,91.7 95.2,93.8 97.1,95.7 99.4,97.4 102.0,99.0 104.8,100.3 108.0,101.4 111.3,102.3 114.7,102.8 118.2,103.1 121.8,103.1 125.3,102.8 128.7,102.3 132.0,101.4 135.2,100.3 138.0,99.0 140.6,97.4 142.9,95.7 144.8,93.8 146.3,91.7 147.4,89.5 148.1,87.3 148.3,85.0"/><polyline class="curve3" fill="none" points="169.0,85.0 168.6,81.1 167.5,77.2 165.5,73.4 162.9,69.8 159.6,66.5 155.7,63.5 151.2,60.8 146.3,58.4 140.9,56.5 135.1,55.1 129.2,54.1 123.1,53.6 116.9,53.6 110.8,54.1 104.9,55.1 99.1,56.5 93.7,58.4 88.8,60.8 84.3,63.5 80.4,66.5 77.1,69.8 74.5,73.4 72.5,77.2 71.4,81.1 71.0,85.0 71.4,88.9 72.5,92.8 74.5,96.6 77.1,100.2 80.4,103.5 84.3,106.5 88.8,109.2 93.7,111.6 99.1,113.5 104.9,114.9 110.8,115.9 116.9,116.4 123.1,116.4 129.2,115.9 135.1,114.9 140.9,113.5 146.3,111.6 151.2,109.2 155.7,106.5 159.6,103.5 162.9,100.2 165.5,96.6 167.5,92.8 168.6,88.9 169.0,85.0"/><polyline class="curve3" fill="none" points="189.3,85.0 188.7,79.4 187.1,73.9 184.4,68.6 180.7,63.6 176.1,58.8 170.5,54.5 164.2,50.7 157.1,47.4 149.5,44.7 141.4,42.7 133.0,41.3 124.4,40.6 115.6,40.6 107.0,41.3 98.6,42.7 90.5,44.7 82.9,47.4 75.8,50.7 69.5,54.5 63.9,58.8 59.3,63.6 55.6,68.6 52.9,73.9 51.3,79.4 50.7,85.0 51.3,90.6 52.9,96.1 55.6,101.4 59.3,106.4 63.9,111.2 69.5,115.5 75.8,119.3 82.9,122.6 90.5,125.3 98.6,127.3 107.0,128.7 115.6,129.4 124.4,129.4 133.0,128.7 141.4,127.3 149.5,125.3 157.1,122.6 164.2,119.3 170.5,115.5 176.1,111.2 180.7,106.4 184.4,101.4 187.1,96.1 188.7,90.6 189.3,85.0"/><polyline class="curve3" fill="none" points="209.4,85.0 208.7,77.8 206.6,70.7 203.2,63.9 198.4,57.3 192.4,51.2 185.2,45.7 177.0,40.7 167.9,36.5 158.1,33.0 147.6,30.4 136.8,28.6 125.6,27.7 114.4,27.7 103.2,28.6 92.4,30.4 81.9,33.0 72.1,36.5 63.0,40.7 54.8,45.7 47.6,51.2 41.6,57.3 36.8,63.9 33.4,70.7 31.3,77.8 30.6,85.0 31.3,92.2 33.4,99.3 36.8,106.1 41.6,112.7 47.6,118.8 54.8,124.3 63.0,129.3 72.1,133.5 81.9,137.0 92.4,139.6 103.2,141.4 114.4,142.3 125.6,142.3 136.8,141.4 147.6,139.6 158.1,137.0 167.9,133.5 177.0,129.3 185.2,124.3 192.4,118.8 198.4,112.7 203.2,106.1 206.6,99.3 208.7,92.2 209.4,85.0"/><polyline class="curve2" fill="none" stroke-width="2" points="30.0,36.2 46.2,124.0 59.5,53.8 70.4,110.0 79.3,65.0 86.6,101.0 92.6,72.2 97.6,95.2 101.6,76.8 104.9,91.5 107.6,79.8 109.9,89.2 111.7,81.6 113.2,87.7 114.4,82.9"/><circle class="dot3" cx="30.0" cy="36.2" r="4"/><circle class="dot" cx="120.0" cy="85.0" r="4"/><text class="ink" x="120" y="170" font-size="11" text-anchor="middle">gradient descent: zigzag</text><line class="grid" x1="250.0" y1="150.0" x2="250.0" y2="20.0"/><line class="grid" x1="270.0" y1="150.0" x2="270.0" y2="20.0"/><line class="grid" x1="290.0" y1="150.0" x2="290.0" y2="20.0"/><line class="grid" x1="310.0" y1="150.0" x2="310.0" y2="20.0"/><line class="grid" x1="330.0" y1="150.0" x2="330.0" y2="20.0"/><line class="grid" x1="350.0" y1="150.0" x2="350.0" y2="20.0"/><line class="grid" x1="370.0" y1="150.0" x2="370.0" y2="20.0"/><line class="grid" x1="390.0" y1="150.0" x2="390.0" y2="20.0"/><line class="grid" x1="410.0" y1="150.0" x2="410.0" y2="20.0"/><line class="grid" x1="430.0" y1="150.0" x2="430.0" y2="20.0"/><line class="grid" x1="450.0" y1="150.0" x2="450.0" y2="20.0"/><line class="grid" x1="250.0" y1="125.6" x2="450.0" y2="125.6"/><line class="grid" x1="250.0" y1="85.0" x2="450.0" y2="85.0"/><line class="grid" x1="250.0" y1="44.4" x2="450.0" y2="44.4"/><polyline class="curve3" fill="none" points="378.3,85.0 378.1,82.7 377.4,80.5 376.3,78.3 374.8,76.2 372.9,74.3 370.6,72.6 368.0,71.0 365.2,69.7 362.0,68.6 358.7,67.7 355.3,67.2 351.8,66.9 348.2,66.9 344.7,67.2 341.3,67.7 338.0,68.6 334.8,69.7 332.0,71.0 329.4,72.6 327.1,74.3 325.2,76.2 323.7,78.3 322.6,80.5 321.9,82.7 321.7,85.0 321.9,87.3 322.6,89.5 323.7,91.7 325.2,93.8 327.1,95.7 329.4,97.4 332.0,99.0 334.8,100.3 338.0,101.4 341.3,102.3 344.7,102.8 348.2,103.1 351.8,103.1 355.3,102.8 358.7,102.3 362.0,101.4 365.2,100.3 368.0,99.0 370.6,97.4 372.9,95.7 374.8,93.8 376.3,91.7 377.4,89.5 378.1,87.3 378.3,85.0"/><polyline class="curve3" fill="none" points="399.0,85.0 398.6,81.1 397.5,77.2 395.5,73.4 392.9,69.8 389.6,66.5 385.7,63.5 381.2,60.8 376.3,58.4 370.9,56.5 365.1,55.1 359.2,54.1 353.1,53.6 346.9,53.6 340.8,54.1 334.9,55.1 329.1,56.5 323.7,58.4 318.8,60.8 314.3,63.5 310.4,66.5 307.1,69.8 304.5,73.4 302.5,77.2 301.4,81.1 301.0,85.0 301.4,88.9 302.5,92.8 304.5,96.6 307.1,100.2 310.4,103.5 314.3,106.5 318.8,109.2 323.7,111.6 329.1,113.5 334.9,114.9 340.8,115.9 346.9,116.4 353.1,116.4 359.2,115.9 365.1,114.9 370.9,113.5 376.3,111.6 381.2,109.2 385.7,106.5 389.6,103.5 392.9,100.2 395.5,96.6 397.5,92.8 398.6,88.9 399.0,85.0"/><polyline class="curve3" fill="none" points="419.3,85.0 418.7,79.4 417.1,73.9 414.4,68.6 410.7,63.6 406.1,58.8 400.5,54.5 394.2,50.7 387.1,47.4 379.5,44.7 371.4,42.7 363.0,41.3 354.4,40.6 345.6,40.6 337.0,41.3 328.6,42.7 320.5,44.7 312.9,47.4 305.8,50.7 299.5,54.5 293.9,58.8 289.3,63.6 285.6,68.6 282.9,73.9 281.3,79.4 280.7,85.0 281.3,90.6 282.9,96.1 285.6,101.4 289.3,106.4 293.9,111.2 299.5,115.5 305.8,119.3 312.9,122.6 320.5,125.3 328.6,127.3 337.0,128.7 345.6,129.4 354.4,129.4 363.0,128.7 371.4,127.3 379.5,125.3 387.1,122.6 394.2,119.3 400.5,115.5 406.1,111.2 410.7,106.4 414.4,101.4 417.1,96.1 418.7,90.6 419.3,85.0"/><polyline class="curve3" fill="none" points="439.4,85.0 438.7,77.8 436.6,70.7 433.2,63.9 428.4,57.3 422.4,51.2 415.2,45.7 407.0,40.7 397.9,36.5 388.1,33.0 377.6,30.4 366.8,28.6 355.6,27.7 344.4,27.7 333.2,28.6 322.4,30.4 311.9,33.0 302.1,36.5 293.0,40.7 284.8,45.7 277.6,51.2 271.6,57.3 266.8,63.9 263.4,70.7 261.3,77.8 260.6,85.0 261.3,92.2 263.4,99.3 266.8,106.1 271.6,112.7 277.6,118.8 284.8,124.3 293.0,129.3 302.1,133.5 311.9,137.0 322.4,139.6 333.2,141.4 344.4,142.3 355.6,142.3 366.8,141.4 377.6,139.6 388.1,137.0 397.9,133.5 407.0,129.3 415.2,124.3 422.4,118.8 428.4,112.7 433.2,106.1 436.6,99.3 438.7,92.2 439.4,85.0"/><polyline class="curve2" fill="none" stroke-width="2" points="260.0,36.2 265.4,65.5 274.3,97.7 285.0,112.6 296.4,106.5 307.6,89.3 318.0,74.7 327.2,70.7 335.0,76.4 341.4,85.6 346.3,91.7 350.0,91.9 352.6,87.9 354.3,83.4 355.2,81.2 355.5,81.9 355.4,84.3 355.0,86.4 354.4,87.0 353.7,86.2 353.1,85.0 352.4,84.1 351.8,84.0 351.2,84.6 350.8,85.2 350.4,85.5 350.2,85.4 349.9,85.1 349.8,84.8 349.7,84.7 349.7,84.8"/><circle class="dot3" cx="260.0" cy="36.2" r="4"/><circle class="dot" cx="350.0" cy="85.0" r="4"/><text class="ink" x="350" y="170" font-size="11" text-anchor="middle">momentum: the oscillation dies down</text><text class="dim" x="235" y="192" font-size="11" text-anchor="middle">f = x² + 10y² (y is 10 times steeper)</text></svg>
  <figcaption>Level ellipses of f = x² + 10y². On the left, gradient descent is thrown from side to side in the steep y direction while it creeps along the gentle x direction. On the right, momentum: the swings cancel out and speed builds up in the consistent x direction.</figcaption>
</figure>

In the gentle direction the distance is multiplied by $1 - \eta \lambda_{\min}$
at each step. With $\eta \approx \frac{1}{\lambda_{\max}}$ this factor is
$1 - \frac{\lambda_{\min}}{\lambda_{\max}}$: if the condition number is
$100$, each step makes only one percent progress. Scaling (standardising)
the features lowers the condition number and speeds up training.

## Stochastic and mini-batch gradient descent

The loss is usually an average over examples: $L = \frac{1}{n}\sum_i \ell_i$.
Its gradient is the average of the example gradients too. With millions
of examples, computing them all for every step is far too expensive.

| Method | Used at each step | Property |
|---|---|---|
| (full) gradient descent | all examples | accurate but slow steps |
| stochastic (SGD) | one example | very cheap, very noisy |
| mini-batch | $B$ examples (e.g. $32$–$512$) | the balance used in practice |

The mini-batch gradient is a **noisy but unbiased** estimate of the true
gradient: on average it points the right way. One pass over the whole
data is called an **epoch**. The noise has a benefit too: it helps escape
saddle points and shallow pits. The price: unless the learning rate is
reduced towards the end, the loss keeps jittering around the bottom.

## Momentum

Think of a ball: a ball rolling downhill moves according not only to the
slope right now but also to the speed it has gained.

$$
\begin{aligned}
\mathbf{v}_{k+1} &= \beta \, \mathbf{v}_k + \nabla L(\mathbf{w}_k) \\
\mathbf{w}_{k+1} &= \mathbf{w}_k - \eta \, \mathbf{v}_{k+1}
\end{aligned}
$$

$\beta$ (usually $0.9$) is how much of the past gradients is remembered.
The zigzagging components change sign at each step, so they cancel out;
the components in a consistent direction build up. The result: much
faster progress in narrow valleys.

## Adaptive methods: Adam

Give each parameter its own learning rate: make the step smaller for a
parameter whose gradient is always large, and larger for one whose
gradient is always small. **RMSProp** keeps a moving average of the
squared gradients for each parameter and divides the step by its square
root. **Adam** combines this with momentum:

$$
\begin{aligned}
\mathbf{m} &\leftarrow \beta_1 \mathbf{m} + (1 - \beta_1) \mathbf{g} \\
\mathbf{s} &\leftarrow \beta_2 \mathbf{s} + (1 - \beta_2) \mathbf{g}^2 \\
\mathbf{w} &\leftarrow \mathbf{w} - \eta \, \frac{\mathbf{m}}{\sqrt{\mathbf{s}} + \epsilon}
\end{aligned}
$$

(Squares and division are element-wise; $\epsilon$ is a small number that
prevents division by zero. The real Adam also adds a factor that corrects
the smallness of the first steps.) This is the most used method in deep
learning; with the default settings (β₁ = 0.9, β₂ = 0.999) it often works
well.

## In practice

- **Watch the loss curve.** A smooth descent is good; no descent at all
  may mean the rate is too small; jumps or `nan` mean it is too large.
- **Learning rate schedules.** Start with a large rate and reduce it over
  time (in steps or in a cosine shape). For large models, slowly raising
  the rate from zero over the first few hundred steps (**warm-up**) gives
  stability.
- **Scale the features.** It lowers the condition number.
- **Gradient clipping.** Shrinking the gradient when its length passes a
  threshold stops a single bad step from ruining everything.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$\mathbf{w} \leftarrow \mathbf{w} + \eta \nabla L$</p>
      <p>A larger learning rate is always faster</p>
      <p>If the loss is rising, take more steps</p>
      <p>The SGD gradient is the true gradient</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>Minus: against the gradient</p>
      <p>$\eta > 2/\lambda_{\max}$ diverges</p>
      <p>Reduce the learning rate</p>
      <p>A noisy estimate that is right on average</p>
    </div>
  </div>
  <figcaption>The learning rate is the most important setting: too small wastes time, too large ruins training.</figcaption>
</figure>

## Summary

- Gradient descent: $\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$; small steps in the direction of steepest descent.
- On a parabola the distance is multiplied by $1 - \eta\lambda$ at each step; convergence needs $\eta < \frac{2}{\lambda_{\max}}$.
- A large condition number means zigzags and slow progress; scaling helps.
- SGD and mini-batch: a cheap, noisy but unbiased estimate of the gradient; an epoch is one pass over the data.
- Momentum accumulates past gradients and damps the zigzag.
- Adam: momentum plus an adaptive step size per parameter.
- In practice: watch the loss curve, use a learning rate schedule, warm-up, scaling and gradient clipping.
