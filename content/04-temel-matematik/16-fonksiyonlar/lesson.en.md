# Functions

A **function** is a rule that assigns exactly one output to each input.
Price and quantity, time and distance, temperature and sales… all describe
how one quantity depends on another. In machine learning a model is also a
function: it takes an example as input and gives a prediction as output. A
neural network is many functions applied one after another. In this
section we will see what a function is, its graph, its domain, composition
and the inverse.

Prerequisite: Linear Equations, Sets and Logic.

## A function is a machine

<figure class="fig">
  <div class="flow">
    <span class="node">input<br><b>x = 4</b></span>
    <span class="arrow">→</span>
    <span class="node acc"><b>f(x) = 2x + 3</b><br>rule</span>
    <span class="arrow">→</span>
    <span class="node">output<br><b>f(4) = 11</b></span>
  </div>
  <figcaption>A function is like a machine: it takes the input, applies the rule and gives a single output. The same input always gives the same output.</figcaption>
</figure>

$f(x)$ is read "f of x": the rule $f$ applied to the input $x$.

$$
f(x) = 2x + 3: \qquad f(4) = 11, \quad f(0) = 3, \quad f(-2) = -1
$$

**An expression can go in place of the letter too.** $f(a + 1) = 2(a + 1)
+ 3 = 2a + 5$. Write the new input, with brackets, in place of every $x$.

## Function or not?

The heart of the definition: **one output for each input.** If an input
goes to two different outputs, the rule is not a function. (Two different
inputs going to the same output is fine: in $x^2$, both $2$ and $-2$ give
$4$.)

<figure class="fig">
<svg viewBox="0 0 480 244" width="480"><line class="grid" x1="30.0" y1="210.0" x2="30.0" y2="30.0"/><line class="grid" x1="60.0" y1="210.0" x2="60.0" y2="30.0"/><line class="grid" x1="90.0" y1="210.0" x2="90.0" y2="30.0"/><line class="grid" x1="120.0" y1="210.0" x2="120.0" y2="30.0"/><line class="grid" x1="150.0" y1="210.0" x2="150.0" y2="30.0"/><line class="grid" x1="180.0" y1="210.0" x2="180.0" y2="30.0"/><line class="grid" x1="210.0" y1="210.0" x2="210.0" y2="30.0"/><line class="grid" x1="30.0" y1="210.0" x2="210.0" y2="210.0"/><line class="grid" x1="30.0" y1="180.0" x2="210.0" y2="180.0"/><line class="grid" x1="30.0" y1="150.0" x2="210.0" y2="150.0"/><line class="grid" x1="30.0" y1="120.0" x2="210.0" y2="120.0"/><line class="grid" x1="30.0" y1="90.0" x2="210.0" y2="90.0"/><line class="grid" x1="30.0" y1="60.0" x2="210.0" y2="60.0"/><line class="grid" x1="30.0" y1="30.0" x2="210.0" y2="30.0"/><line class="line" x1="30.0" y1="120.0" x2="210.0" y2="120.0"/><line class="line" x1="120.0" y1="210.0" x2="120.0" y2="30.0"/><polyline class="curve" fill="none" points="53.6,33.1 54.8,38.1 55.9,42.9 57.0,47.7 58.1,52.4 59.2,57.0 60.4,61.5 61.5,65.9 62.6,70.3 63.8,74.5 64.9,78.7 66.0,82.8 67.1,86.8 68.2,90.7 69.4,94.6 70.5,98.3 71.6,102.0 72.8,105.6 73.9,109.1 75.0,112.5 76.1,115.8 77.2,119.1 78.4,122.2 79.5,125.3 80.6,128.3 81.8,131.2 82.9,134.1 84.0,136.8 85.1,139.5 86.2,142.0 87.4,144.5 88.5,146.9 89.6,149.2 90.8,151.5 91.9,153.6 93.0,155.7 94.1,157.7 95.2,159.6 96.4,161.4 97.5,163.1 98.6,164.8 99.8,166.3 100.9,167.8 102.0,169.2 103.1,170.5 104.2,171.7 105.4,172.9 106.5,173.9 107.6,174.9 108.8,175.8 109.9,176.6 111.0,177.3 112.1,177.9 113.2,178.5 114.4,178.9 115.5,179.3 116.6,179.6 117.8,179.8 118.9,180.0 120.0,180.0 121.1,180.0 122.3,179.8 123.4,179.6 124.5,179.3 125.6,178.9 126.8,178.5 127.9,177.9 129.0,177.3 130.1,176.6 131.2,175.8 132.4,174.9 133.5,173.9 134.6,172.9 135.8,171.7 136.9,170.5 138.0,169.2 139.1,167.8 140.2,166.3 141.4,164.8 142.5,163.1 143.6,161.4 144.8,159.6 145.9,157.7 147.0,155.7 148.1,153.6 149.2,151.5 150.4,149.2 151.5,146.9 152.6,144.5 153.8,142.0 154.9,139.5 156.0,136.8 157.1,134.1 158.2,131.2 159.4,128.3 160.5,125.3 161.6,122.2 162.8,119.1 163.9,115.8 165.0,112.5 166.1,109.1 167.2,105.6 168.4,102.0 169.5,98.3 170.6,94.6 171.8,90.7 172.9,86.8 174.0,82.8 175.1,78.7 176.2,74.5 177.4,70.3 178.5,65.9 179.6,61.5 180.8,57.0 181.9,52.4 183.0,47.7 184.1,42.9 185.2,38.1 186.4,33.1"/><line class="curve2" stroke-dasharray="5 4" x1="150.0" y1="30.0" x2="150.0" y2="210.0"/><circle class="dot2" cx="150.0" cy="150.0" r="5"/><text class="ink" x="120" y="20" font-size="12" text-anchor="middle">y = x² − 2: a function</text><text class="dim" x="120" y="232" font-size="10" text-anchor="middle">every vertical line meets it at most once</text><line class="grid" x1="270.0" y1="210.0" x2="270.0" y2="30.0"/><line class="grid" x1="300.0" y1="210.0" x2="300.0" y2="30.0"/><line class="grid" x1="330.0" y1="210.0" x2="330.0" y2="30.0"/><line class="grid" x1="360.0" y1="210.0" x2="360.0" y2="30.0"/><line class="grid" x1="390.0" y1="210.0" x2="390.0" y2="30.0"/><line class="grid" x1="420.0" y1="210.0" x2="420.0" y2="30.0"/><line class="grid" x1="450.0" y1="210.0" x2="450.0" y2="30.0"/><line class="grid" x1="270.0" y1="210.0" x2="450.0" y2="210.0"/><line class="grid" x1="270.0" y1="180.0" x2="450.0" y2="180.0"/><line class="grid" x1="270.0" y1="150.0" x2="450.0" y2="150.0"/><line class="grid" x1="270.0" y1="120.0" x2="450.0" y2="120.0"/><line class="grid" x1="270.0" y1="90.0" x2="450.0" y2="90.0"/><line class="grid" x1="270.0" y1="60.0" x2="450.0" y2="60.0"/><line class="grid" x1="270.0" y1="30.0" x2="450.0" y2="30.0"/><line class="line" x1="270.0" y1="120.0" x2="450.0" y2="120.0"/><line class="line" x1="360.0" y1="210.0" x2="360.0" y2="30.0"/><polyline class="curve" fill="none" points="420.0,120.0 419.9,116.9 419.7,113.7 419.3,110.6 418.7,107.5 418.0,104.5 417.1,101.5 416.0,98.5 414.8,95.6 413.5,92.8 412.0,90.0 410.3,87.3 408.5,84.7 406.6,82.2 404.6,79.9 402.4,77.6 400.1,75.4 397.8,73.4 395.3,71.5 392.7,69.7 390.0,68.0 387.2,66.5 384.4,65.2 381.5,64.0 378.5,62.9 375.5,62.0 372.5,61.3 369.4,60.7 366.3,60.3 363.1,60.1 360.0,60.0 356.9,60.1 353.7,60.3 350.6,60.7 347.5,61.3 344.5,62.0 341.5,62.9 338.5,64.0 335.6,65.2 332.8,66.5 330.0,68.0 327.3,69.7 324.7,71.5 322.2,73.4 319.9,75.4 317.6,77.6 315.4,79.9 313.4,82.2 311.5,84.7 309.7,87.3 308.0,90.0 306.5,92.8 305.2,95.6 304.0,98.5 302.9,101.5 302.0,104.5 301.3,107.5 300.7,110.6 300.3,113.7 300.1,116.9 300.0,120.0 300.1,123.1 300.3,126.3 300.7,129.4 301.3,132.5 302.0,135.5 302.9,138.5 304.0,141.5 305.2,144.4 306.5,147.2 308.0,150.0 309.7,152.7 311.5,155.3 313.4,157.8 315.4,160.1 317.6,162.4 319.9,164.6 322.2,166.6 324.7,168.5 327.3,170.3 330.0,172.0 332.8,173.5 335.6,174.8 338.5,176.0 341.5,177.1 344.5,178.0 347.5,178.7 350.6,179.3 353.7,179.7 356.9,179.9 360.0,180.0 363.1,179.9 366.3,179.7 369.4,179.3 372.5,178.7 375.5,178.0 378.5,177.1 381.5,176.0 384.4,174.8 387.2,173.5 390.0,172.0 392.7,170.3 395.3,168.5 397.8,166.6 400.1,164.6 402.4,162.4 404.6,160.1 406.6,157.8 408.5,155.3 410.3,152.7 412.0,150.0 413.5,147.2 414.8,144.4 416.0,141.5 417.1,138.5 418.0,135.5 418.7,132.5 419.3,129.4 419.7,126.3 419.9,123.1 420.0,120.0"/><line class="curve2" stroke-dasharray="5 4" x1="390.0" y1="30.0" x2="390.0" y2="210.0"/><circle class="dot2" cx="390.0" cy="68.0" r="5"/><circle class="dot2" cx="390.0" cy="172.0" r="5"/><text class="ink" x="360" y="20" font-size="12" text-anchor="middle">x² + y² = 4: not a function</text><text class="dim" x="360" y="232" font-size="10" text-anchor="middle">the line x = 1 meets it twice</text></svg>
  <figcaption>The vertical line test: if every vertical line meets the graph at most once, the graph is the graph of a function. On the left the parabola passes; the circle on the right fails, because the input $x = 1$ has two outputs ($\sqrt{3}$ and $-\sqrt{3}$).</figcaption>
</figure>

## Domain and range

The **domain** is the set of inputs the function accepts; the **range** is
the set of outputs that can come out. Given a formula, the domain is
usually "everywhere the formula makes sense":

| Function | Forbidden | Domain |
|---|---|---|
| $2x + 3$ | nothing | all real numbers |
| $\dfrac{1}{x - 2}$ | the denominator cannot be zero | $x \neq 2$ |
| $\sqrt{x - 3}$ | the inside of the root cannot be negative | $x \ge 3$ |

The range of $x^2$ is $y \ge 0$: a square cannot come out negative.

## Graphs

The graph of a function is the set of all points $(x, f(x))$. It is drawn
by working out a few points and joining them.

<figure class="fig">
<svg viewBox="0 0 486 160" width="486"><line class="grid" x1="14.0" y1="130.0" x2="14.0" y2="30.0"/><line class="grid" x1="30.7" y1="130.0" x2="30.7" y2="30.0"/><line class="grid" x1="47.3" y1="130.0" x2="47.3" y2="30.0"/><line class="grid" x1="64.0" y1="130.0" x2="64.0" y2="30.0"/><line class="grid" x1="80.7" y1="130.0" x2="80.7" y2="30.0"/><line class="grid" x1="97.3" y1="130.0" x2="97.3" y2="30.0"/><line class="grid" x1="114.0" y1="130.0" x2="114.0" y2="30.0"/><line class="grid" x1="14.0" y1="130.0" x2="114.0" y2="130.0"/><line class="grid" x1="14.0" y1="113.3" x2="114.0" y2="113.3"/><line class="grid" x1="14.0" y1="96.7" x2="114.0" y2="96.7"/><line class="grid" x1="14.0" y1="80.0" x2="114.0" y2="80.0"/><line class="grid" x1="14.0" y1="63.3" x2="114.0" y2="63.3"/><line class="grid" x1="14.0" y1="46.7" x2="114.0" y2="46.7"/><line class="grid" x1="14.0" y1="30.0" x2="114.0" y2="30.0"/><line class="line" x1="14.0" y1="96.7" x2="114.0" y2="96.7"/><line class="line" x1="64.0" y1="130.0" x2="64.0" y2="30.0"/><polyline class="curve" fill="none" points="30.9,129.8 31.5,129.2 32.1,128.5 32.8,127.9 33.4,127.3 34.0,126.7 34.6,126.0 35.2,125.4 35.9,124.8 36.5,124.2 37.1,123.5 37.8,122.9 38.4,122.3 39.0,121.7 39.6,121.0 40.2,120.4 40.9,119.8 41.5,119.2 42.1,118.5 42.8,117.9 43.4,117.3 44.0,116.7 44.6,116.0 45.2,115.4 45.9,114.8 46.5,114.2 47.1,113.5 47.8,112.9 48.4,112.3 49.0,111.7 49.6,111.0 50.2,110.4 50.9,109.8 51.5,109.2 52.1,108.5 52.8,107.9 53.4,107.3 54.0,106.7 54.6,106.0 55.2,105.4 55.9,104.8 56.5,104.2 57.1,103.5 57.8,102.9 58.4,102.3 59.0,101.7 59.6,101.0 60.2,100.4 60.9,99.8 61.5,99.2 62.1,98.5 62.8,97.9 63.4,97.3 64.0,96.7 64.6,96.0 65.2,95.4 65.9,94.8 66.5,94.2 67.1,93.5 67.8,92.9 68.4,92.3 69.0,91.7 69.6,91.0 70.2,90.4 70.9,89.8 71.5,89.2 72.1,88.5 72.8,87.9 73.4,87.3 74.0,86.7 74.6,86.0 75.2,85.4 75.9,84.8 76.5,84.2 77.1,83.5 77.8,82.9 78.4,82.3 79.0,81.7 79.6,81.0 80.2,80.4 80.9,79.8 81.5,79.2 82.1,78.5 82.8,77.9 83.4,77.3 84.0,76.7 84.6,76.0 85.2,75.4 85.9,74.8 86.5,74.2 87.1,73.5 87.8,72.9 88.4,72.3 89.0,71.7 89.6,71.0 90.2,70.4 90.9,69.8 91.5,69.2 92.1,68.5 92.8,67.9 93.4,67.3 94.0,66.7 94.6,66.0 95.2,65.4 95.9,64.8 96.5,64.2 97.1,63.5 97.8,62.9 98.4,62.3 99.0,61.7 99.6,61.0 100.2,60.4 100.9,59.8 101.5,59.2 102.1,58.5 102.8,57.9 103.4,57.3 104.0,56.7 104.6,56.0 105.2,55.4 105.9,54.8 106.5,54.2 107.1,53.5 107.8,52.9 108.4,52.3 109.0,51.7 109.6,51.0 110.2,50.4 110.9,49.8 111.5,49.2 112.1,48.5 112.8,47.9 113.4,47.3 114.0,46.7"/><text class="ink" x="64" y="20" font-size="12" text-anchor="middle">y = x</text><text class="dim" x="64" y="148" font-size="10" text-anchor="middle">line</text><line class="grid" x1="132.0" y1="130.0" x2="132.0" y2="30.0"/><line class="grid" x1="148.7" y1="130.0" x2="148.7" y2="30.0"/><line class="grid" x1="165.3" y1="130.0" x2="165.3" y2="30.0"/><line class="grid" x1="182.0" y1="130.0" x2="182.0" y2="30.0"/><line class="grid" x1="198.7" y1="130.0" x2="198.7" y2="30.0"/><line class="grid" x1="215.3" y1="130.0" x2="215.3" y2="30.0"/><line class="grid" x1="232.0" y1="130.0" x2="232.0" y2="30.0"/><line class="grid" x1="132.0" y1="130.0" x2="232.0" y2="130.0"/><line class="grid" x1="132.0" y1="113.3" x2="232.0" y2="113.3"/><line class="grid" x1="132.0" y1="96.7" x2="232.0" y2="96.7"/><line class="grid" x1="132.0" y1="80.0" x2="232.0" y2="80.0"/><line class="grid" x1="132.0" y1="63.3" x2="232.0" y2="63.3"/><line class="grid" x1="132.0" y1="46.7" x2="232.0" y2="46.7"/><line class="grid" x1="132.0" y1="30.0" x2="232.0" y2="30.0"/><line class="line" x1="132.0" y1="96.7" x2="232.0" y2="96.7"/><line class="line" x1="182.0" y1="130.0" x2="182.0" y2="30.0"/><polyline class="curve" fill="none" points="148.9,30.8 149.5,33.3 150.1,35.7 150.8,38.1 151.4,40.4 152.0,42.7 152.6,44.9 153.2,47.1 153.9,49.2 154.5,51.3 155.1,53.3 155.8,55.3 156.4,57.3 157.0,59.2 157.6,61.0 158.2,62.8 158.9,64.6 159.5,66.3 160.1,68.0 160.8,69.6 161.4,71.1 162.0,72.7 162.6,74.1 163.2,75.6 163.9,77.0 164.5,78.3 165.1,79.6 165.8,80.8 166.4,82.0 167.0,83.2 167.6,84.3 168.2,85.3 168.9,86.3 169.5,87.3 170.1,88.2 170.8,89.1 171.4,89.9 172.0,90.7 172.6,91.4 173.2,92.1 173.9,92.7 174.5,93.3 175.1,93.8 175.8,94.3 176.4,94.8 177.0,95.2 177.6,95.5 178.2,95.8 178.9,96.1 179.5,96.3 180.1,96.5 180.8,96.6 181.4,96.6 182.0,96.7 182.6,96.6 183.2,96.6 183.9,96.5 184.5,96.3 185.1,96.1 185.8,95.8 186.4,95.5 187.0,95.2 187.6,94.8 188.2,94.3 188.9,93.8 189.5,93.3 190.1,92.7 190.8,92.1 191.4,91.4 192.0,90.7 192.6,89.9 193.2,89.1 193.9,88.2 194.5,87.3 195.1,86.3 195.8,85.3 196.4,84.3 197.0,83.2 197.6,82.0 198.2,80.8 198.9,79.6 199.5,78.3 200.1,77.0 200.8,75.6 201.4,74.1 202.0,72.7 202.6,71.1 203.2,69.6 203.9,68.0 204.5,66.3 205.1,64.6 205.8,62.8 206.4,61.0 207.0,59.2 207.6,57.3 208.2,55.3 208.9,53.3 209.5,51.3 210.1,49.2 210.8,47.1 211.4,44.9 212.0,42.7 212.6,40.4 213.2,38.1 213.9,35.7 214.5,33.3 215.1,30.8"/><text class="ink" x="182" y="20" font-size="12" text-anchor="middle">y = x²</text><text class="dim" x="182" y="148" font-size="10" text-anchor="middle">parabola</text><line class="grid" x1="250.0" y1="130.0" x2="250.0" y2="30.0"/><line class="grid" x1="266.7" y1="130.0" x2="266.7" y2="30.0"/><line class="grid" x1="283.3" y1="130.0" x2="283.3" y2="30.0"/><line class="grid" x1="300.0" y1="130.0" x2="300.0" y2="30.0"/><line class="grid" x1="316.7" y1="130.0" x2="316.7" y2="30.0"/><line class="grid" x1="333.3" y1="130.0" x2="333.3" y2="30.0"/><line class="grid" x1="350.0" y1="130.0" x2="350.0" y2="30.0"/><line class="grid" x1="250.0" y1="130.0" x2="350.0" y2="130.0"/><line class="grid" x1="250.0" y1="113.3" x2="350.0" y2="113.3"/><line class="grid" x1="250.0" y1="96.7" x2="350.0" y2="96.7"/><line class="grid" x1="250.0" y1="80.0" x2="350.0" y2="80.0"/><line class="grid" x1="250.0" y1="63.3" x2="350.0" y2="63.3"/><line class="grid" x1="250.0" y1="46.7" x2="350.0" y2="46.7"/><line class="grid" x1="250.0" y1="30.0" x2="350.0" y2="30.0"/><line class="line" x1="250.0" y1="96.7" x2="350.0" y2="96.7"/><line class="line" x1="300.0" y1="130.0" x2="300.0" y2="30.0"/><polyline class="curve" fill="none" points="250.0,46.7 250.6,47.3 251.2,47.9 251.9,48.5 252.5,49.2 253.1,49.8 253.8,50.4 254.4,51.0 255.0,51.7 255.6,52.3 256.2,52.9 256.9,53.5 257.5,54.2 258.1,54.8 258.8,55.4 259.4,56.0 260.0,56.7 260.6,57.3 261.2,57.9 261.9,58.5 262.5,59.2 263.1,59.8 263.8,60.4 264.4,61.0 265.0,61.7 265.6,62.3 266.2,62.9 266.9,63.5 267.5,64.2 268.1,64.8 268.8,65.4 269.4,66.0 270.0,66.7 270.6,67.3 271.2,67.9 271.9,68.5 272.5,69.2 273.1,69.8 273.8,70.4 274.4,71.0 275.0,71.7 275.6,72.3 276.2,72.9 276.9,73.5 277.5,74.2 278.1,74.8 278.8,75.4 279.4,76.0 280.0,76.7 280.6,77.3 281.2,77.9 281.9,78.5 282.5,79.2 283.1,79.8 283.8,80.4 284.4,81.0 285.0,81.7 285.6,82.3 286.2,82.9 286.9,83.5 287.5,84.2 288.1,84.8 288.8,85.4 289.4,86.0 290.0,86.7 290.6,87.3 291.2,87.9 291.9,88.5 292.5,89.2 293.1,89.8 293.8,90.4 294.4,91.0 295.0,91.7 295.6,92.3 296.2,92.9 296.9,93.5 297.5,94.2 298.1,94.8 298.8,95.4 299.4,96.0 300.0,96.7 300.6,96.0 301.2,95.4 301.9,94.8 302.5,94.2 303.1,93.5 303.8,92.9 304.4,92.3 305.0,91.7 305.6,91.0 306.2,90.4 306.9,89.8 307.5,89.2 308.1,88.5 308.8,87.9 309.4,87.3 310.0,86.7 310.6,86.0 311.2,85.4 311.9,84.8 312.5,84.2 313.1,83.5 313.8,82.9 314.4,82.3 315.0,81.7 315.6,81.0 316.2,80.4 316.9,79.8 317.5,79.2 318.1,78.5 318.8,77.9 319.4,77.3 320.0,76.7 320.6,76.0 321.2,75.4 321.9,74.8 322.5,74.2 323.1,73.5 323.8,72.9 324.4,72.3 325.0,71.7 325.6,71.0 326.2,70.4 326.9,69.8 327.5,69.2 328.1,68.5 328.8,67.9 329.4,67.3 330.0,66.7 330.6,66.0 331.2,65.4 331.9,64.8 332.5,64.2 333.1,63.5 333.8,62.9 334.4,62.3 335.0,61.7 335.6,61.0 336.2,60.4 336.9,59.8 337.5,59.2 338.1,58.5 338.8,57.9 339.4,57.3 340.0,56.7 340.6,56.0 341.2,55.4 341.9,54.8 342.5,54.2 343.1,53.5 343.8,52.9 344.4,52.3 345.0,51.7 345.6,51.0 346.2,50.4 346.9,49.8 347.5,49.2 348.1,48.5 348.8,47.9 349.4,47.3 350.0,46.7"/><text class="ink" x="300" y="20" font-size="12" text-anchor="middle">y = |x|</text><text class="dim" x="300" y="148" font-size="10" text-anchor="middle">V shape</text><line class="grid" x1="368.0" y1="130.0" x2="368.0" y2="30.0"/><line class="grid" x1="384.7" y1="130.0" x2="384.7" y2="30.0"/><line class="grid" x1="401.3" y1="130.0" x2="401.3" y2="30.0"/><line class="grid" x1="418.0" y1="130.0" x2="418.0" y2="30.0"/><line class="grid" x1="434.7" y1="130.0" x2="434.7" y2="30.0"/><line class="grid" x1="451.3" y1="130.0" x2="451.3" y2="30.0"/><line class="grid" x1="468.0" y1="130.0" x2="468.0" y2="30.0"/><line class="grid" x1="368.0" y1="130.0" x2="468.0" y2="130.0"/><line class="grid" x1="368.0" y1="113.3" x2="468.0" y2="113.3"/><line class="grid" x1="368.0" y1="96.7" x2="468.0" y2="96.7"/><line class="grid" x1="368.0" y1="80.0" x2="468.0" y2="80.0"/><line class="grid" x1="368.0" y1="63.3" x2="468.0" y2="63.3"/><line class="grid" x1="368.0" y1="46.7" x2="468.0" y2="46.7"/><line class="grid" x1="368.0" y1="30.0" x2="468.0" y2="30.0"/><line class="line" x1="368.0" y1="96.7" x2="468.0" y2="96.7"/><line class="line" x1="418.0" y1="130.0" x2="418.0" y2="30.0"/><polyline class="curve" fill="none" points="418.0,96.7 418.3,94.4 418.6,93.4 418.9,92.7 419.2,92.1 419.6,91.6 419.9,91.1 420.2,90.6 420.5,90.2 420.8,89.8 421.1,89.4 421.4,89.1 421.8,88.8 422.1,88.4 422.4,88.1 422.7,87.8 423.0,87.5 423.3,87.3 423.6,87.0 423.9,86.7 424.2,86.5 424.6,86.2 424.9,86.0 425.2,85.7 425.5,85.5 425.8,85.3 426.1,85.0 426.4,84.8 426.8,84.6 427.1,84.4 427.4,84.2 427.7,84.0 428.0,83.8 428.3,83.6 428.6,83.4 428.9,83.2 429.2,83.0 429.6,82.8 429.9,82.6 430.2,82.4 430.5,82.2 430.8,82.1 431.1,81.9 431.4,81.7 431.8,81.5 432.1,81.4 432.4,81.2 432.7,81.0 433.0,80.9 433.3,80.7 433.6,80.5 433.9,80.4 434.2,80.2 434.6,80.1 434.9,79.9 435.2,79.7 435.5,79.6 435.8,79.4 436.1,79.3 436.4,79.1 436.8,79.0 437.1,78.8 437.4,78.7 437.7,78.6 438.0,78.4 438.3,78.3 438.6,78.1 438.9,78.0 439.2,77.8 439.6,77.7 439.9,77.6 440.2,77.4 440.5,77.3 440.8,77.2 441.1,77.0 441.4,76.9 441.8,76.8 442.1,76.6 442.4,76.5 442.7,76.4 443.0,76.3 443.3,76.1 443.6,76.0 443.9,75.9 444.2,75.8 444.6,75.6 444.9,75.5 445.2,75.4 445.5,75.3 445.8,75.1 446.1,75.0 446.4,74.9 446.8,74.8 447.1,74.7 447.4,74.5 447.7,74.4 448.0,74.3 448.3,74.2 448.6,74.1 448.9,74.0 449.2,73.8 449.6,73.7 449.9,73.6 450.2,73.5 450.5,73.4 450.8,73.3 451.1,73.2 451.4,73.1 451.8,72.9 452.1,72.8 452.4,72.7 452.7,72.6 453.0,72.5 453.3,72.4 453.6,72.3 453.9,72.2 454.2,72.1 454.6,72.0 454.9,71.9 455.2,71.8 455.5,71.7 455.8,71.6 456.1,71.5 456.4,71.4 456.8,71.3 457.1,71.2 457.4,71.0 457.7,70.9 458.0,70.8 458.3,70.7 458.6,70.6 458.9,70.5 459.2,70.4 459.6,70.3 459.9,70.2 460.2,70.2 460.5,70.1 460.8,70.0 461.1,69.9 461.4,69.8 461.8,69.7 462.1,69.6 462.4,69.5 462.7,69.4 463.0,69.3 463.3,69.2 463.6,69.1 463.9,69.0 464.2,68.9 464.6,68.8 464.9,68.7 465.2,68.6 465.5,68.5 465.8,68.4 466.1,68.3 466.4,68.3 466.8,68.2 467.1,68.1 467.4,68.0 467.7,67.9 468.0,67.8"/><text class="ink" x="418" y="20" font-size="12" text-anchor="middle">y = √x</text><text class="dim" x="418" y="148" font-size="10" text-anchor="middle">only x ≥ 0</text></svg>
  <figcaption>Four common shapes. $y = x$ is a line, $y = x^2$ a parabola, $y = |x|$ a V that bends at zero, and $y = \sqrt{x}$ a curve defined only for $x \ge 0$ that grows more and more slowly.</figcaption>
</figure>

Reading a graph: $f(3)$ is the height at $x = 3$; the solutions of $f(x) =
0$ are where the graph crosses the $x$-axis.

## Composition

Connecting two machines in a row: first $f$, then $g$.

$$
(g \circ f)(x) = g(f(x))
$$

For $f(x) = 2x + 3$ and $g(x) = x^2$:

$$
g(f(1)) = g(5) = 25, \qquad f(g(1)) = f(1) = 5
$$

**Order matters:** $g \circ f$ and $f \circ g$ are usually different. The
inner function is applied first.

## The inverse function

A function that undoes what $f$ does is called the **inverse function**,
written $f^{-1}$: if $f(3) = 9$ then $f^{-1}(9) = 3$.

To find it, write $y = f(x)$ and get $x$ out:

$$
y = 2x + 3 \quad\Rightarrow\quad x = \frac{y - 3}{2} \quad\Rightarrow\quad f^{-1}(x) = \frac{x - 3}{2}
$$

**Check:** $f^{-1}(f(4)) = f^{-1}(11) = \frac{11 - 3}{2} = 4$ ✓.

**Careful:** $f^{-1}$ is not an exponent; do not confuse it with
$\dfrac{1}{f(x)}$.

Not every function has an inverse: in $x^2$, $f(2) = f(-2) = 4$; undoing
$4$, we cannot tell whether to say $2$ or $-2$.

## Functions in machine learning

**A model is a function.** The linear model $f(x) = wx + b$ takes the input
and gives a prediction. Training means choosing this function's $w$ and $b$.

**Activations.** Two functions used often in neural networks:

$$
\text{ReLU}(x) = \max(0, x), \qquad \sigma(x) = \frac{1}{1 + e^{-x}}
$$

ReLU sets negatives to zero and leaves positives as they are. $\sigma$
(the sigmoid) squeezes every number into the range between $0$ and $1$;
that is why it is used for probability outputs. (We will meet the number
$e$ in the Exponential Functions section.)

**Layers are a composition.** A neural network is a composition of layers:
$f_3(f_2(f_1(x)))$. Each layer takes the previous one's output as its
input.

## Common mistakes

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Wrong</h4>
      <p>$f(x + 1) = f(x) + 1$</p>
      <p>$f^{-1}(x) = \dfrac{1}{f(x)}$</p>
      <p>$g(f(x)) = f(g(x))$</p>
      <p>$f(2x) = 2f(x)$</p>
    </div>
    <div class="ok">
      <h4>Right</h4>
      <p>Put $x + 1$ in place of $x$</p>
      <p>$f^{-1}$ is the inverse function</p>
      <p>Order matters; the inner one first</p>
      <p>Usually not: for $f(x) = x^2$, $4x^2 \neq 2x^2$</p>
    </div>
  </div>
  <figcaption>$f$ is a rule, not a number; the rule applies to whatever is written inside it.</figcaption>
</figure>

- **Substituting without brackets.** If $f(x) = x^2$, then $f(-3) = (-3)^2 =
  9$, not $-3^2$.
- **Forgetting the domain.** $\sqrt{x - 3}$ has no input $x = 1$.

## Summary

- A function: one output for each input; $f(x)$ is $f$ applied to $x$.
- The vertical line test: every vertical line meets the graph at most once.
- Domain: the denominator is not zero, the inside of a root is not negative.
- The graph is the set of points $(x, f(x))$.
- Composition $(g \circ f)(x) = g(f(x))$; order matters.
- The inverse $f^{-1}$ undoes $f$; it is found by getting $x$ out of $y = f(x)$.
- Models, activations and layers are all functions; a neural network is a composition.
