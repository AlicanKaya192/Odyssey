# What Is a Time Series?

In most of the tables you have worked with so far, the order of the rows did
not matter. Shuffle the car prices table and a model would learn exactly the
same thing; each row was a car on its own.

This track works with data where that is not true. Daily sales, hourly
electricity use, monthly passenger numbers, a stock's closing price, a sensor
reading every minute... They all share one thing:

**Measurements ordered in time.** This is called a **time series**, and in
this kind of data **the order of the rows is the data itself.**

In this section you do not learn new code yet; you learn how to look at a
time series. The tools for working with dates come in the next sections.

## The parts of a time series

The dataset we will keep coming back to is three years of daily sales from
one shop (`store_sales.csv`). Its first eight rows:

```text
      date  sales
2022-01-01    305
2022-01-02    277
2022-01-03    201
2022-01-04    182
2022-01-05    184
2022-01-06    211
2022-01-07    251
2022-01-08    299
```

<figure class="fig">
  <div class="anat">
    <div class="anat-row"><span>Timestamp</span><span><code>date</code>: when the measurement was taken</span></div>
    <div class="anat-row"><span>Value</span><span><code>sales</code>: what is measured, that day's sales</span></div>
    <div class="anat-row"><span>Frequency</span><span>The gap between two measurements: here <b>one day</b></span></div>
    <div class="anat-row"><span>Observation</span><span>One (time, value) pair; one row of the table</span></div>
    <div class="anat-row"><span>Length</span><span><b>1096</b> observations: three years from 2022-01-01 to 2024-12-31</span></div>
  </div>
  <figcaption>Every time series has at least these two columns: when and how much.</figcaption>
</figure>

Look at how the date is written: `2022-01-01`, that is **year-month-day**.
This format is called **ISO 8601** and you will meet it almost everywhere in
time series work. Its biggest advantage: **it sorts correctly even as
text.** Dates written day first, like `01.02.2022`, get scrambled when sorted
as text; we will see this in Section 02.

## All three years

The first thing to do with a time series is to **plot it.** The table gives
you 1096 numbers; the chart shows three things at a glance:

<figure class="fig">
  <svg viewBox="0 0 680 250" width="680" xmlns="http://www.w3.org/2000/svg"><line class="grid" x1="44" y1="180.3" x2="666" y2="180.3"/><text class="dim" x="38" y="183.8" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="129.0" x2="666" y2="129.0"/><text class="dim" x="38" y="132.5" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="77.8" x2="666" y2="77.8"/><text class="dim" x="38" y="81.3" font-size="10.5" text-anchor="end">400</text><line class="grid" x1="44" y1="26.6" x2="666" y2="26.6"/><text class="dim" x="38" y="30.1" font-size="10.5" text-anchor="end">500</text><line class="line" x1="44" y1="220" x2="666" y2="220"/><line class="line" x1="44.0" y1="220" x2="44.0" y2="224"/><text class="dim" x="44.0" y="236" font-size="10.5" text-anchor="middle">2022</text><line class="line" x1="251.3" y1="220" x2="251.3" y2="224"/><text class="dim" x="251.3" y="236" font-size="10.5" text-anchor="middle">2023</text><line class="line" x1="458.7" y1="220" x2="458.7" y2="224"/><text class="dim" x="458.7" y="236" font-size="10.5" text-anchor="middle">2024</text><line class="line" x1="666.0" y1="220" x2="666.0" y2="224"/><text class="dim" x="666.0" y="236" font-size="10.5" text-anchor="middle">31 Dec</text><polyline class="curve" style="stroke-width:1.1" points="44.0,126.5 44.6,140.8 45.1,179.8 45.7,189.5 46.3,188.5 46.8,174.6 47.4,154.1 48.0,129.6 48.5,140.3 49.1,181.8 49.7,180.3 50.2,184.9 50.8,181.3 51.4,151.1 52.0,132.1 52.5,145.9 53.1,194.1 53.7,186.9 54.2,188.0 54.8,179.8 55.4,154.7 55.9,141.3 56.5,154.1 57.1,185.9 57.6,188.5 58.2,182.8 58.8,177.2 59.3,157.7 59.9,136.2 60.5,150.0 61.0,186.9 61.6,182.8 62.2,180.3 62.7,167.0 63.3,164.4 63.9,127.5 64.4,154.7 65.0,193.1 65.6,178.7 66.2,184.9 66.7,179.2 67.3,169.5 67.9,147.0 68.4,149.5 69.0,194.6 69.6,181.8 70.1,172.6 70.7,178.2 71.3,169.0 71.8,134.2 72.4,149.5 73.0,190.5 73.5,186.9 74.1,176.2 74.7,171.1 75.2,159.3 75.8,142.4 76.4,155.2 76.9,186.4 77.5,189.0 78.1,188.0 78.7,183.3 79.2,168.0 79.8,142.4 80.4,158.8 80.9,183.9 81.5,193.1 82.1,180.3 82.6,177.7 83.2,164.4 83.8,144.4 84.3,159.8 84.9,180.3 85.5,188.5 86.0,183.3 86.6,177.2 87.2,160.3 87.7,142.4 88.3,161.8 88.9,192.6 89.4,191.5 90.0,182.8 90.6,180.8 91.1,165.9 91.7,141.8 92.3,152.6 92.9,196.2 93.4,193.6 94.0,182.8 94.6,183.3 95.1,166.4 95.7,148.0 96.3,160.3 96.8,191.0 97.4,199.2 98.0,192.6 98.5,181.3 99.1,156.7 99.7,142.4 100.2,161.8 100.8,199.2 101.4,190.5 101.9,203.8 102.5,184.9 103.1,172.1 103.6,149.0 104.2,149.5 104.8,209.0 105.3,193.6 105.9,190.0 106.5,182.8 107.1,180.3 107.6,149.5 108.2,172.1 108.8,196.7 109.3,192.6 109.9,190.0 110.5,186.9 111.0,171.1 111.6,147.0 112.2,161.8 112.7,196.2 113.3,204.4 113.9,196.2 114.4,184.9 115.0,177.7 115.6,153.1 116.1,164.4 116.7,197.2 117.3,190.0 117.8,189.0 118.4,189.5 119.0,172.6 119.5,165.4 120.1,170.0 120.7,198.2 121.3,209.0 121.8,194.1 122.4,185.9 123.0,168.0 123.5,147.5 124.1,155.2 124.7,189.0 125.2,204.9 125.8,194.1 126.4,188.5 126.9,173.6 127.5,153.6 128.1,162.3 128.6,193.6 129.2,204.4 129.8,187.4 130.3,191.5 130.9,168.0 131.5,147.0 132.0,167.0 132.6,186.4 133.2,190.5 133.7,192.6 134.3,186.4 134.9,160.3 135.5,142.4 136.0,160.8 136.6,196.2 137.2,192.6 137.7,191.5 138.3,196.2 138.9,168.5 139.4,147.5 140.0,173.1 140.6,200.8 141.1,196.7 141.7,190.5 142.3,177.7 142.8,173.1 143.4,160.3 144.0,161.3 144.5,197.7 145.1,204.9 145.7,204.9 146.2,192.6 146.8,170.5 147.4,152.6 148.0,160.8 148.5,198.2 149.1,193.1 149.7,187.4 150.2,182.8 150.8,177.7 151.4,136.7 151.9,174.6 152.5,196.7 153.1,199.2 153.6,183.9 154.2,192.6 154.8,176.7 155.3,152.6 155.9,170.0 156.5,198.2 157.0,191.5 157.6,195.1 158.2,194.1 158.7,171.6 159.3,145.4 159.9,157.2 160.4,198.7 161.0,193.1 161.6,183.3 162.2,189.0 162.7,169.0 163.3,145.4 163.9,168.0 164.4,193.6 165.0,184.4 165.6,175.2 166.1,190.5 166.7,161.8 167.3,135.7 167.8,151.6 168.4,194.6 169.0,188.0 169.5,190.0 170.1,177.7 170.7,158.8 171.2,141.3 171.8,155.7 172.4,185.9 172.9,184.4 173.5,189.0 174.1,171.6 174.6,161.3 175.2,137.2 175.8,154.7 176.4,185.4 176.9,181.3 177.5,190.5 178.1,182.8 178.6,172.1 179.2,133.1 179.8,151.1 180.3,190.0 180.9,192.1 181.5,174.6 182.0,167.5 182.6,151.6 183.2,133.1 183.7,150.6 184.3,185.9 184.9,184.9 185.4,187.4 186.0,178.2 186.6,154.1 187.1,131.6 187.7,151.6 188.3,186.4 188.8,172.6 189.4,170.5 190.0,167.0 190.6,155.7 191.1,135.7 191.7,145.9 192.3,185.4 192.8,177.7 193.4,171.6 194.0,175.2 194.5,147.5 195.1,126.5 195.7,144.4 196.2,185.4 196.8,180.8 197.4,175.7 197.9,171.1 198.5,155.2 199.1,127.0 199.6,131.6 200.2,181.8 200.8,174.1 201.3,174.1 201.9,184.9 202.5,133.7 203.1,122.4 203.6,144.4 204.2,172.1 204.8,168.5 205.3,176.2 205.9,171.6 206.5,154.7 207.0,118.3 207.6,138.3 208.2,173.6 208.7,176.2 209.3,174.6 209.9,164.4 210.4,151.1 211.0,114.7 211.6,135.2 212.1,173.6 212.7,171.6 213.3,172.6 213.8,173.6 214.4,139.3 215.0,110.1 215.5,140.3 216.1,170.5 216.7,172.1 217.3,169.5 217.8,162.3 218.4,149.5 219.0,115.2 219.5,134.2 220.1,173.1 220.7,175.2 221.2,165.9 221.8,164.9 222.4,146.5 222.9,112.6 223.5,135.7 224.1,179.2 224.6,173.6 225.2,171.1 225.8,159.8 226.3,138.8 226.9,108.0 227.5,135.7 228.0,174.6 228.6,168.5 229.2,175.2 229.7,154.7 230.3,134.7 230.9,106.5 231.5,142.9 232.0,170.5 232.6,179.8 233.2,160.3 233.7,170.0 234.3,147.0 234.9,104.4 235.4,134.7 236.0,183.9 236.6,171.1 237.1,157.2 237.7,159.3 238.3,138.8 238.8,97.3 239.4,119.3 240.0,156.2 240.5,154.7 241.1,156.7 241.7,150.6 242.2,119.8 242.8,94.7 243.4,118.8 243.9,155.7 244.5,158.2 245.1,158.2 245.7,137.7 246.2,114.7 246.8,90.1 247.4,108.0 247.9,156.2 248.5,150.6 249.1,147.0 249.6,144.4 250.2,113.7 250.8,77.8 251.3,127.5 251.9,166.4 252.5,163.4 253.0,161.3 253.6,172.1 254.2,144.9 254.7,107.0 255.3,123.9 255.9,176.2 256.4,172.1 257.0,154.1 257.6,172.1 258.1,141.3 258.7,111.6 259.3,131.1 259.9,172.6 260.4,164.4 261.0,158.8 261.6,140.3 262.1,129.6 262.7,109.1 263.3,128.0 263.8,164.9 264.4,153.6 265.0,165.9 265.5,156.2 266.1,141.3 266.7,102.4 267.2,137.7 267.8,170.5 268.4,176.7 268.9,163.9 269.5,154.1 270.1,143.4 270.6,111.6 271.2,124.4 271.8,172.6 272.4,166.4 272.9,167.5 273.5,164.9 274.1,144.4 274.6,99.3 275.2,133.7 275.8,172.6 276.3,163.9 276.9,164.4 277.5,157.2 278.0,130.1 278.6,107.5 279.2,137.7 279.7,170.0 280.3,174.6 280.9,169.5 281.4,155.2 282.0,143.4 282.6,115.7 283.1,137.2 283.7,173.6 284.3,173.6 284.8,162.9 285.4,161.3 286.0,145.9 286.6,97.8 287.1,133.7 287.7,179.8 288.3,180.3 288.8,176.2 289.4,171.1 290.0,147.0 290.5,117.3 291.1,133.7 291.7,182.3 292.2,176.7 292.8,174.1 293.4,155.2 293.9,147.0 294.5,115.7 295.1,132.1 295.6,176.2 296.2,175.7 296.8,174.1 297.3,167.5 297.9,149.0 298.5,121.4 299.0,140.8 299.6,168.0 300.2,183.9 300.8,184.4 301.3,164.9 301.9,142.4 302.5,122.9 303.0,136.2 303.6,170.0 304.2,178.7 304.7,172.6 305.3,172.6 305.9,155.2 306.4,125.5 307.0,138.3 307.6,172.1 308.1,174.1 308.7,179.8 309.3,173.1 309.8,154.7 310.4,124.4 311.0,140.3 311.5,189.5 312.1,184.9 312.7,165.4 313.2,167.0 313.8,151.1 314.4,133.7 315.0,138.8 315.5,178.7 316.1,188.0 316.7,183.3 317.2,167.0 317.8,161.8 318.4,123.4 318.9,148.5 319.5,178.7 320.1,175.2 320.6,166.4 321.2,181.3 321.8,163.4 322.3,128.0 322.9,136.7 323.5,180.3 324.0,189.0 324.6,172.6 325.2,172.6 325.7,148.5 326.3,135.2 326.9,141.8 327.5,176.2 328.0,186.9 328.6,177.2 329.2,170.0 329.7,155.2 330.3,134.2 330.9,141.8 331.4,189.5 332.0,181.3 332.6,175.7 333.1,170.5 333.7,153.6 334.3,139.8 334.8,160.8 335.4,183.3 336.0,180.3 336.5,171.1 337.1,174.1 337.7,158.2 338.2,138.3 338.8,145.9 339.4,176.2 339.9,184.4 340.5,176.2 341.1,166.4 341.7,150.6 342.2,124.4 342.8,142.4 343.4,203.3 343.9,192.6 344.5,176.7 345.1,182.3 345.6,151.6 346.2,132.6 346.8,156.7 347.3,179.2 347.9,185.4 348.5,183.9 349.0,168.5 349.6,157.7 350.2,135.7 350.7,153.1 351.3,193.1 351.9,172.1 352.4,170.5 353.0,172.1 353.6,159.8 354.1,125.5 354.7,147.5 355.3,178.7 355.9,177.2 356.4,177.2 357.0,173.1 357.6,151.6 358.1,127.0 358.7,155.2 359.3,181.3 359.8,170.0 360.4,178.7 361.0,169.0 361.5,156.2 362.1,124.4 362.7,145.9 363.2,168.5 363.8,176.7 364.4,175.7 364.9,168.0 365.5,152.1 366.1,116.2 366.6,147.0 367.2,185.4 367.8,175.2 368.3,175.7 368.9,172.1 369.5,161.8 370.1,122.9 370.6,144.9 371.2,173.6 371.8,183.3 372.3,171.1 372.9,167.5 373.5,153.6 374.0,113.7 374.6,131.6 375.2,180.3 375.7,176.7 376.3,183.9 376.9,160.3 377.4,149.0 378.0,112.1 378.6,140.3 379.1,173.6 379.7,171.6 380.3,167.5 380.8,166.4 381.4,150.0 382.0,122.9 382.5,134.7 383.1,180.3 383.7,170.0 384.3,179.2 384.8,154.7 385.4,141.3 386.0,113.7 386.5,138.3 387.1,178.7 387.7,173.6 388.2,163.4 388.8,159.3 389.4,140.3 389.9,106.5 390.5,128.0 391.1,167.5 391.6,170.0 392.2,171.1 392.8,151.1 393.3,133.1 393.9,118.8 394.5,130.6 395.0,157.7 395.6,160.8 396.2,157.7 396.8,170.0 397.3,140.3 397.9,111.1 398.5,128.0 399.0,169.5 399.6,160.3 400.2,164.9 400.7,156.2 401.3,141.3 401.9,112.6 402.4,122.9 403.0,161.3 403.6,164.9 404.1,152.6 404.7,155.7 405.3,131.1 405.8,113.2 406.4,120.8 407.0,156.2 407.5,167.0 408.1,156.2 408.7,149.5 409.2,134.2 409.8,97.8 410.4,121.9 411.0,168.5 411.5,161.8 412.1,158.8 412.7,149.5 413.2,142.9 413.8,99.3 414.4,112.6 414.9,159.3 415.5,153.1 416.1,156.2 416.6,142.4 417.2,119.3 417.8,97.3 418.3,117.3 418.9,144.9 419.5,161.3 420.0,164.9 420.6,137.7 421.2,126.0 421.7,100.9 422.3,121.9 422.9,158.2 423.4,164.9 424.0,157.2 424.6,153.6 425.2,124.4 425.7,90.6 426.3,123.4 426.9,150.6 427.4,161.3 428.0,153.6 428.6,132.1 429.1,124.9 429.7,91.6 430.3,114.7 430.8,153.1 431.4,158.2 432.0,161.8 432.5,150.6 433.1,126.0 433.7,88.1 434.2,119.3 434.8,156.2 435.4,156.7 435.9,155.7 436.5,143.4 437.1,110.6 437.6,88.1 438.2,110.1 438.8,151.6 439.4,154.1 439.9,145.9 440.5,138.8 441.1,127.0 441.6,79.3 442.2,109.1 442.8,154.7 443.3,149.0 443.9,150.0 444.5,130.6 445.0,107.5 445.6,60.9 446.2,100.3 446.7,149.0 447.3,133.1 447.9,147.0 448.4,131.6 449.0,96.3 449.6,69.6 450.1,76.3 450.7,143.9 451.3,143.4 451.9,131.1 452.4,122.4 453.0,100.9 453.6,58.8 454.1,81.4 454.7,138.3 455.3,137.2 455.8,126.0 456.4,116.7 457.0,100.3 457.5,46.0 458.1,75.8 458.7,147.0 459.2,154.1 459.8,153.1 460.4,144.4 460.9,112.1 461.5,79.9 462.1,107.5 462.6,161.3 463.2,154.7 463.8,147.0 464.3,136.7 464.9,121.4 465.5,76.3 466.1,108.5 466.6,148.0 467.2,160.3 467.8,143.9 468.3,142.4 468.9,131.1 469.5,80.4 470.0,111.1 470.6,149.5 471.2,159.3 471.7,148.5 472.3,138.8 472.9,129.6 473.4,87.0 474.0,105.5 474.6,160.8 475.1,157.2 475.7,143.9 476.3,126.0 476.8,124.9 477.4,83.4 478.0,113.2 478.5,148.0 479.1,157.2 479.7,148.5 480.3,135.7 480.8,128.0 481.4,84.0 482.0,112.1 482.5,167.5 483.1,158.2 483.7,150.6 484.2,146.5 484.8,118.3 485.4,90.6 485.9,111.1 486.5,155.7 487.1,143.9 487.6,148.0 488.2,149.0 488.8,115.7 489.3,89.6 489.9,112.1 490.5,166.4 491.0,158.8 491.6,151.6 492.2,154.7 492.7,128.0 493.3,92.2 493.9,119.3 494.5,152.6 495.0,148.5 495.6,161.8 496.2,158.2 496.7,135.2 497.3,86.0 497.9,123.4 498.4,163.4 499.0,151.6 499.6,151.1 500.1,142.9 500.7,128.5 501.3,82.9 501.8,120.8 502.4,170.0 503.0,159.8 503.5,140.3 504.1,140.8 504.7,132.1 505.2,106.5 505.8,119.3 506.4,161.3 506.9,158.2 507.5,158.2 508.1,156.7 508.7,135.2 509.2,96.8 509.8,113.7 510.4,159.3 510.9,163.9 511.5,159.8 512.1,145.4 512.6,127.0 513.2,98.3 513.8,135.7 514.3,174.1 514.9,159.8 515.5,153.6 516.0,150.6 516.6,134.2 517.2,102.9 517.7,122.4 518.3,175.7 518.9,169.0 519.4,157.7 520.0,156.2 520.6,136.7 521.2,104.4 521.7,123.9 522.3,171.6 522.9,172.1 523.4,160.3 524.0,165.4 524.6,138.3 525.1,113.7 525.7,120.8 526.3,155.7 526.8,173.6 527.4,157.7 528.0,159.3 528.5,141.8 529.1,109.6 529.7,126.0 530.2,166.4 530.8,171.6 531.4,167.5 531.9,151.1 532.5,131.1 533.1,113.7 533.6,130.6 534.2,164.9 534.8,156.2 535.4,162.9 535.9,155.2 536.5,144.9 537.1,102.9 537.6,126.5 538.2,173.1 538.8,168.5 539.3,152.1 539.9,149.5 540.5,131.6 541.0,114.2 541.6,136.7 542.2,180.3 542.7,165.4 543.3,171.6 543.9,164.4 544.4,133.7 545.0,119.8 545.6,127.0 546.1,178.2 546.7,168.5 547.3,151.6 547.8,156.7 548.4,141.8 549.0,110.6 549.6,131.6 550.1,174.6 550.7,178.2 551.3,170.0 551.8,150.6 552.4,133.1 553.0,105.5 553.5,130.1 554.1,167.5 554.7,167.0 555.2,161.3 555.8,149.5 556.4,132.6 556.9,110.6 557.5,134.2 558.1,182.3 558.6,172.1 559.2,164.9 559.8,158.2 560.3,139.3 560.9,105.5 561.5,122.9 562.0,178.7 562.6,173.1 563.2,169.0 563.8,153.1 564.3,128.0 564.9,105.5 565.5,124.9 566.0,172.6 566.6,172.1 567.2,166.4 567.7,147.0 568.3,137.7 568.9,106.5 569.4,122.9 570.0,168.0 570.6,159.8 571.1,161.8 571.7,153.1 572.3,133.1 572.8,107.0 573.4,127.0 574.0,163.9 574.5,163.9 575.1,163.9 575.7,153.6 576.3,120.3 576.8,102.9 577.4,127.5 578.0,163.9 578.5,154.1 579.1,160.3 579.7,153.6 580.2,135.2 580.8,107.5 581.4,121.9 581.9,158.8 582.5,159.8 583.1,157.2 583.6,160.3 584.2,133.1 584.8,103.9 585.3,134.7 585.9,167.0 586.5,157.2 587.0,161.8 587.6,153.6 588.2,119.3 588.7,91.6 589.3,110.1 589.9,154.7 590.5,155.2 591.0,154.7 591.6,144.4 592.2,118.8 592.7,91.1 593.3,114.2 593.9,159.3 594.4,152.1 595.0,155.7 595.6,135.7 596.1,119.3 596.7,93.7 597.3,102.9 597.8,168.5 598.4,168.5 599.0,147.5 599.5,147.5 600.1,126.5 600.7,84.5 601.2,104.4 601.8,144.4 602.4,151.1 602.9,153.1 603.5,138.3 604.1,122.4 604.7,87.5 605.2,101.9 605.8,148.0 606.4,162.3 606.9,141.3 607.5,138.8 608.1,115.2 608.6,87.5 609.2,111.6 609.8,156.2 610.3,147.0 610.9,146.5 611.5,139.8 612.0,111.1 612.6,84.0 613.2,114.2 613.7,149.0 614.3,155.2 614.9,142.9 615.4,129.6 616.0,118.8 616.6,79.9 617.1,108.5 617.7,150.6 618.3,151.1 618.9,152.1 619.4,135.2 620.0,106.5 620.6,81.4 621.1,97.8 621.7,152.6 622.3,155.7 622.8,132.6 623.4,129.6 624.0,109.1 624.5,75.8 625.1,107.0 625.7,141.8 626.2,147.5 626.8,128.5 627.4,134.7 627.9,110.1 628.5,70.1 629.1,96.3 629.6,143.4 630.2,142.4 630.8,136.2 631.3,132.1 631.9,97.8 632.5,66.5 633.1,94.2 633.6,143.4 634.2,145.9 634.8,137.7 635.3,126.0 635.9,102.9 636.5,55.3 637.0,91.1 637.6,140.8 638.2,144.9 638.7,127.5 639.3,127.5 639.9,91.6 640.4,73.2 641.0,81.4 641.6,142.9 642.1,139.3 642.7,139.3 643.3,121.4 643.8,94.7 644.4,69.1 645.0,86.5 645.6,144.9 646.1,135.7 646.7,130.6 647.3,130.6 647.8,110.6 648.4,61.4 649.0,81.4 649.5,144.9 650.1,134.2 650.7,124.4 651.2,121.9 651.8,99.8 652.4,52.7 652.9,72.7 653.5,132.1 654.1,120.3 654.6,128.5 655.2,97.8 655.8,83.4 656.3,44.5 656.9,60.4 657.5,128.5 658.0,124.9 658.6,117.3 659.2,118.8 659.8,73.2 660.3,32.2 660.9,62.4 661.5,126.0 662.0,106.5 662.6,108.5 663.2,100.3 663.7,65.5 664.3,25.0 664.9,55.3 665.4,109.1 666.0,105.0"/></svg>
  <figcaption>Three years of daily sales. An upward trend, a peak at the end of every year, and a thick band made of weekly ups and downs.</figcaption>
</figure>

- **The series rises.** The yearly averages are 225.5 → 260.4 → 294.0.
- **Every year ends with a peak.** December averages 327.3, May 230.1.
- **The line looks like a thick band.** That is not a flaw: the series goes
  up and down every week, and on a three-year chart those swings are packed
  together.

To see the third one you need to zoom in.

## Up close: the week

Four weeks of March 2024:

<figure class="fig">
  <svg viewBox="0 0 680 240" width="680" xmlns="http://www.w3.org/2000/svg"><rect class="box" x="155.1" y="14" width="44.4" height="196" opacity="0.7" style="stroke:none"/><rect class="box" x="310.6" y="14" width="44.4" height="196" opacity="0.7" style="stroke:none"/><rect class="box" x="466.1" y="14" width="44.4" height="196" opacity="0.7" style="stroke:none"/><rect class="box" x="621.6" y="14" width="44.4" height="196" opacity="0.7" style="stroke:none"/><line class="grid" x1="44" y1="209.6" x2="666" y2="209.6"/><text class="dim" x="38" y="213.1" font-size="10.5" text-anchor="end">200</text><line class="grid" x1="44" y1="163.1" x2="666" y2="163.1"/><text class="dim" x="38" y="166.6" font-size="10.5" text-anchor="end">250</text><line class="grid" x1="44" y1="116.6" x2="666" y2="116.6"/><text class="dim" x="38" y="120.1" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="44" y1="70.2" x2="666" y2="70.2"/><text class="dim" x="38" y="73.7" font-size="10.5" text-anchor="end">350</text><line class="grid" x1="44" y1="23.7" x2="666" y2="23.7"/><text class="dim" x="38" y="27.2" font-size="10.5" text-anchor="end">400</text><line class="line" x1="44" y1="210" x2="666" y2="210"/><line class="line" x1="55.1" y1="210" x2="55.1" y2="214"/><text class="dim" x="55.1" y="226" font-size="10.5" text-anchor="middle">4 Mar</text><line class="line" x1="210.6" y1="210" x2="210.6" y2="214"/><text class="dim" x="210.6" y="226" font-size="10.5" text-anchor="middle">11 Mar</text><line class="line" x1="366.1" y1="210" x2="366.1" y2="214"/><text class="dim" x="366.1" y="226" font-size="10.5" text-anchor="middle">18 Mar</text><line class="line" x1="521.6" y1="210" x2="521.6" y2="214"/><text class="dim" x="521.6" y="226" font-size="10.5" text-anchor="middle">25 Mar</text><polyline class="curve" points="55.1,159.4 77.3,152.0 99.5,176.2 121.8,169.6 144.0,127.8 166.2,38.5 188.4,106.4 210.6,178.9 232.8,157.6 255.0,156.6 277.2,141.8 299.5,115.7 321.7,33.0 343.9,101.8 366.1,191.0 388.3,172.4 410.5,137.1 432.8,138.0 455.0,122.2 477.2,75.7 499.4,99.0 521.6,175.2 543.8,169.6 566.0,169.6 588.2,166.9 610.5,127.8 632.7,58.1 654.9,88.8"/><circle class="dot" cx="55.1" cy="159.4" r="3.2"/><circle class="dot" cx="77.3" cy="152.0" r="3.2"/><circle class="dot" cx="99.5" cy="176.2" r="3.2"/><circle class="dot" cx="121.8" cy="169.6" r="3.2"/><circle class="dot" cx="144.0" cy="127.8" r="3.2"/><circle class="dot" cx="166.2" cy="38.5" r="3.2"/><circle class="dot" cx="188.4" cy="106.4" r="3.2"/><circle class="dot" cx="210.6" cy="178.9" r="3.2"/><circle class="dot" cx="232.8" cy="157.6" r="3.2"/><circle class="dot" cx="255.0" cy="156.6" r="3.2"/><circle class="dot" cx="277.2" cy="141.8" r="3.2"/><circle class="dot" cx="299.5" cy="115.7" r="3.2"/><circle class="dot" cx="321.7" cy="33.0" r="3.2"/><circle class="dot" cx="343.9" cy="101.8" r="3.2"/><circle class="dot" cx="366.1" cy="191.0" r="3.2"/><circle class="dot" cx="388.3" cy="172.4" r="3.2"/><circle class="dot" cx="410.5" cy="137.1" r="3.2"/><circle class="dot" cx="432.8" cy="138.0" r="3.2"/><circle class="dot" cx="455.0" cy="122.2" r="3.2"/><circle class="dot" cx="477.2" cy="75.7" r="3.2"/><circle class="dot" cx="499.4" cy="99.0" r="3.2"/><circle class="dot" cx="521.6" cy="175.2" r="3.2"/><circle class="dot" cx="543.8" cy="169.6" r="3.2"/><circle class="dot" cx="566.0" cy="169.6" r="3.2"/><circle class="dot" cx="588.2" cy="166.9" r="3.2"/><circle class="dot" cx="610.5" cy="127.8" r="3.2"/><circle class="dot" cx="632.7" cy="58.1" r="3.2"/><circle class="dot" cx="654.9" cy="88.8" r="3.2"/><text class="dim" x="177.3" y="17.2" font-size="10" text-anchor="middle">Sat+Sun</text><text class="dim" x="332.8" y="17.2" font-size="10" text-anchor="middle">Sat+Sun</text><text class="dim" x="488.3" y="17.2" font-size="10" text-anchor="middle">Sat+Sun</text><text class="dim" x="643.8" y="17.2" font-size="10" text-anchor="middle">Sat+Sun</text></svg>
  <figcaption>4–31 March 2024. Shaded columns are weekends. A peak every Saturday, a dip every Monday: a pattern that repeats every 7 days.</figcaption>
</figure>

A peak every Saturday, a dip every Monday. Averaged over three years:

```text
day      Mon    Tue    Wed    Thu    Fri    Sat    Sun
mean   217.6  220.6  228.6  241.1  278.9  336.1  296.9
```

**Saturday is 1.54 times Monday.** The pattern is so regular that you can
roughly answer "what will sales be next Saturday?" before building any model.

## Why order matters

Let us measure it. Remember from the Data Science track: **correlation** says
how much two sequences of numbers move together, between -1 and 1.

Pair each day's sales with **the day before** and look at the correlation.
Then do the same with **the same day a week before.** Finally, shuffle the
rows and measure again:

```text
today - yesterday                 0.695
today - same day last week        0.958
shuffled: today - yesterday       0.018
```

Three things come out:

1. **Today remembers yesterday.** 0.695 is a strong link: the day after a
   high-sales day is usually high too.
2. **Today looks even more like the same day last week.** 0.958. The weekly
   pattern is a stronger clue than yesterday.
3. **Shuffling wipes it all out.** 0.018, practically zero. The numbers are
   the same numbers; the only thing lost is **the order.**

<figure class="fig">
  <svg viewBox="0 0 680 200" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="grid" x1="40" y1="108.1" x2="316" y2="108.1"/><text class="dim" x="34" y="111.6" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="40" y1="35.9" x2="316" y2="35.9"/><text class="dim" x="34" y="39.4" font-size="10.5" text-anchor="end">400</text><line class="line" x1="40" y1="170" x2="316" y2="170"/><polyline class="curve" style="stroke-width:1.8" points="40.0,133.4 44.7,143.5 49.4,142.1 54.0,129.8 58.7,84.3 63.4,38.8 68.1,77.8 72.7,153.6 77.4,144.2 82.1,133.4 86.8,118.9 91.5,97.3 96.1,33.7 100.8,79.2 105.5,134.8 110.2,152.2 114.8,129.1 119.5,126.9 124.2,111.0 128.9,39.5 133.6,82.8 138.2,137.0 142.9,150.7 147.6,135.6 152.3,121.8 156.9,108.8 161.6,48.9 166.3,74.9 171.0,152.9 175.7,147.8 180.3,129.1 185.0,103.8 189.7,102.3 194.4,43.8 199.1,85.7 203.7,134.8 208.4,147.8 213.1,135.6 217.8,117.5 222.4,106.7 227.1,44.5 231.8,84.3 236.5,162.3 241.2,149.3 245.8,138.4 250.5,132.7 255.2,92.9 259.9,53.9 264.5,82.8 269.2,145.7 273.9,129.1 278.6,134.8 283.3,136.3 287.9,89.3 292.6,52.5 297.3,84.3 302.0,160.8 306.6,150.0 311.3,139.9 316.0,144.2"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">In order: 0.70</text></g><g transform="translate(350,0)"><line class="grid" x1="40" y1="108.1" x2="316" y2="108.1"/><text class="dim" x="34" y="111.6" font-size="10.5" text-anchor="end">300</text><line class="grid" x1="40" y1="35.9" x2="316" y2="35.9"/><text class="dim" x="34" y="39.4" font-size="10.5" text-anchor="end">400</text><line class="line" x1="40" y1="170" x2="316" y2="170"/><polyline class="curve2" style="stroke-width:1.8" points="40.0,150.7 44.7,133.4 49.4,129.8 54.0,117.5 58.7,135.6 63.4,142.1 68.1,126.9 72.7,106.7 77.4,149.3 82.1,145.7 86.8,108.8 91.5,82.8 96.1,129.1 100.8,135.6 105.5,92.9 110.2,84.3 114.8,97.3 119.5,150.0 124.2,103.8 128.9,134.8 133.6,129.1 138.2,111.0 142.9,144.2 147.6,152.9 152.3,33.7 156.9,139.9 161.6,143.5 166.3,162.3 171.0,79.2 175.7,138.4 180.3,137.0 185.0,82.8 189.7,121.8 194.4,152.2 199.1,102.3 203.7,132.7 208.4,136.3 213.1,118.9 217.8,53.9 222.4,84.3 227.1,134.8 231.8,44.5 236.5,74.9 241.2,147.8 245.8,144.2 250.5,133.4 255.2,77.8 259.9,43.8 264.5,48.9 269.2,85.7 273.9,84.3 278.6,129.1 283.3,134.8 287.9,147.8 292.6,153.6 297.3,52.5 302.0,38.8 306.6,89.3 311.3,39.5 316.0,160.8"/><text class="ink" x="40" y="16" font-size="12" text-anchor="start" font-weight="600">Shuffled: 0.02</text></g></svg>
  <figcaption>The same 60 values from January–February 2024. Left, in their real order: the weekly wave is visible. Right, shuffled: the same numbers, no pattern. The number in the title is the today-yesterday correlation.</figcaption>
</figure>

**In a time series the information is not in the numbers themselves but in
their order.** The past says something about the future; that is what makes
forecasting possible.

## Four patterns

You will see the same four parts in time series again and again:

<figure class="fig">
  <svg viewBox="0 0 680 310" width="680" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0,0)"><line class="line" x1="14" y1="138" x2="320" y2="138"/><polyline class="curve" style="stroke-width:2" points="14.0,128.1 16.6,123.5 19.1,123.9 21.7,123.2 24.3,119.2 26.9,128.8 29.4,126.0 32.0,127.8 34.6,122.6 37.1,117.8 39.7,120.8 42.3,118.2 44.9,126.3 47.4,118.0 50.0,121.1 52.6,110.5 55.1,113.1 57.7,112.1 60.3,115.1 62.9,111.9 65.4,111.0 68.0,113.9 70.6,113.7 73.1,111.6 75.7,112.7 78.3,111.9 80.9,110.0 83.4,110.9 86.0,104.7 88.6,112.6 91.1,103.0 93.7,107.6 96.3,106.6 98.9,108.8 101.4,103.6 104.0,103.3 106.6,100.9 109.1,102.8 111.7,99.8 114.3,92.7 116.9,97.2 119.4,100.0 122.0,93.7 124.6,96.9 127.1,93.5 129.7,92.7 132.3,95.7 134.9,100.6 137.4,94.1 140.0,90.0 142.6,92.7 145.1,89.0 147.7,86.2 150.3,91.1 152.9,83.9 155.4,81.7 158.0,82.9 160.6,81.9 163.1,81.4 165.7,76.4 168.3,83.3 170.9,83.2 173.4,80.3 176.0,85.1 178.6,86.7 181.1,83.5 183.7,78.2 186.3,77.1 188.9,83.7 191.4,84.3 194.0,77.8 196.6,76.6 199.1,75.3 201.7,71.9 204.3,69.2 206.9,72.1 209.4,70.0 212.0,75.5 214.6,75.1 217.1,69.1 219.7,66.8 222.3,65.9 224.9,65.6 227.4,64.2 230.0,63.3 232.6,72.0 235.1,67.6 237.7,62.4 240.3,61.2 242.9,68.2 245.4,57.6 248.0,62.8 250.6,61.3 253.1,58.7 255.7,56.2 258.3,63.5 260.9,53.9 263.4,56.5 266.0,58.9 268.6,56.3 271.1,62.6 273.7,56.2 276.3,52.4 278.9,55.0 281.4,52.8 284.0,51.4 286.6,50.0 289.1,45.7 291.7,48.8 294.3,48.9 296.9,45.2 299.4,38.8 302.0,47.0 304.6,43.1 307.1,50.1 309.7,38.6 312.3,40.4 314.9,37.2 317.4,41.5 320.0,44.4"/><text class="ink" x="14" y="16" font-size="12" text-anchor="start" font-weight="600">Trend</text></g><g transform="translate(350,0)"><line class="line" x1="14" y1="138" x2="320" y2="138"/><polyline class="curve2" style="stroke-width:2" points="14.0,83.0 16.6,60.1 19.1,43.3 21.7,37.2 24.3,43.3 26.9,60.1 29.4,83.0 32.0,105.9 34.6,122.7 37.1,128.8 39.7,122.7 42.3,105.9 44.9,83.0 47.4,60.1 50.0,43.3 52.6,37.2 55.1,43.3 57.7,60.1 60.3,83.0 62.9,105.9 65.4,122.7 68.0,128.8 70.6,122.7 73.1,105.9 75.7,83.0 78.3,60.1 80.9,43.3 83.4,37.2 86.0,43.3 88.6,60.1 91.1,83.0 93.7,105.9 96.3,122.7 98.9,128.8 101.4,122.7 104.0,105.9 106.6,83.0 109.1,60.1 111.7,43.3 114.3,37.2 116.9,43.3 119.4,60.1 122.0,83.0 124.6,105.9 127.1,122.7 129.7,128.8 132.3,122.7 134.9,105.9 137.4,83.0 140.0,60.1 142.6,43.3 145.1,37.2 147.7,43.3 150.3,60.1 152.9,83.0 155.4,105.9 158.0,122.7 160.6,128.8 163.1,122.7 165.7,105.9 168.3,83.0 170.9,60.1 173.4,43.3 176.0,37.2 178.6,43.3 181.1,60.1 183.7,83.0 186.3,105.9 188.9,122.7 191.4,128.8 194.0,122.7 196.6,105.9 199.1,83.0 201.7,60.1 204.3,43.3 206.9,37.2 209.4,43.3 212.0,60.1 214.6,83.0 217.1,105.9 219.7,122.7 222.3,128.8 224.9,122.7 227.4,105.9 230.0,83.0 232.6,60.1 235.1,43.3 237.7,37.2 240.3,43.3 242.9,60.1 245.4,83.0 248.0,105.9 250.6,122.7 253.1,128.8 255.7,122.7 258.3,105.9 260.9,83.0 263.4,60.1 266.0,43.3 268.6,37.2 271.1,43.3 273.7,60.1 276.3,83.0 278.9,105.9 281.4,122.7 284.0,128.8 286.6,122.7 289.1,105.9 291.7,83.0 294.3,60.1 296.9,43.3 299.4,37.2 302.0,43.3 304.6,60.1 307.1,83.0 309.7,105.9 312.3,122.7 314.9,128.8 317.4,122.7 320.0,105.9"/><text class="ink" x="14" y="16" font-size="12" text-anchor="start" font-weight="600">Seasonality: every 12 steps</text></g><g transform="translate(0,160)"><line class="line" x1="14" y1="138" x2="320" y2="138"/><polyline class="curve4" style="stroke-width:2" points="14.0,83.0 16.6,74.6 19.1,66.4 21.7,58.9 24.3,52.1 26.9,46.4 29.4,42.0 32.0,38.9 34.6,37.4 37.1,37.4 39.7,38.9 42.3,42.0 44.9,46.4 47.4,52.1 50.0,58.9 52.6,66.4 55.1,74.6 57.7,83.0 60.3,91.4 62.9,99.6 65.4,107.1 68.0,113.9 70.6,119.6 73.1,124.0 75.7,127.1 78.3,128.6 80.9,128.6 83.4,127.1 86.0,124.0 88.6,119.6 91.1,113.9 93.7,107.1 96.3,99.6 98.9,91.4 101.4,83.0 104.0,70.1 106.6,58.2 109.1,48.4 111.7,41.3 114.3,37.6 116.9,37.6 119.4,41.3 122.0,48.4 124.6,58.2 127.1,70.1 129.7,83.0 132.3,95.9 134.9,107.8 137.4,117.6 140.0,124.7 142.6,128.4 145.1,128.4 147.7,124.7 150.3,117.6 152.9,107.8 155.4,95.9 158.0,83.0 160.6,76.5 163.1,70.1 165.7,64.0 168.3,58.2 170.9,53.0 173.4,48.4 176.0,44.4 178.6,41.3 181.1,39.0 183.7,37.6 186.3,37.2 188.9,37.6 191.4,39.0 194.0,41.3 196.6,44.4 199.1,48.4 201.7,53.0 204.3,58.2 206.9,64.0 209.4,70.1 212.0,76.5 214.6,83.0 217.1,89.5 219.7,95.9 222.3,102.0 224.9,107.8 227.4,113.0 230.0,117.6 232.6,121.6 235.1,124.7 237.7,127.0 240.3,128.4 242.9,128.8 245.4,128.4 248.0,127.0 250.6,124.7 253.1,121.6 255.7,117.6 258.3,113.0 260.9,107.8 263.4,102.0 266.0,95.9 268.6,89.5 271.1,83.0 273.7,68.8 276.3,56.1 278.9,45.9 281.4,39.4 284.0,37.2 286.6,39.4 289.1,45.9 291.7,56.1 294.3,68.8 296.9,83.0 299.4,97.2 302.0,109.9 304.6,120.1 307.1,126.6 309.7,128.8 312.3,126.6 314.9,120.1 317.4,109.9 320.0,97.2"/><text class="ink" x="14" y="16" font-size="12" text-anchor="start" font-weight="600">Cycle: waves of different lengths</text></g><g transform="translate(350,160)"><line class="line" x1="14" y1="138" x2="320" y2="138"/><polyline class="curve3" style="stroke-width:2" points="14.0,68.9 16.6,71.3 19.1,101.0 21.7,112.2 24.3,76.9 26.9,88.3 29.4,37.2 32.0,96.4 34.6,94.8 37.1,87.2 39.7,115.7 42.3,101.4 44.9,54.9 47.4,87.5 50.0,96.3 52.6,108.5 55.1,74.5 57.7,73.0 60.3,80.4 62.9,92.3 65.4,79.5 68.0,78.1 70.6,97.6 73.1,73.7 75.7,123.9 78.3,108.8 80.9,90.7 83.4,87.1 86.0,106.5 88.6,79.1 91.1,65.7 93.7,76.8 96.3,81.0 98.9,69.9 101.4,77.7 104.0,106.1 106.6,88.8 109.1,61.4 111.7,106.0 114.3,84.0 116.9,92.3 119.4,101.6 122.0,103.7 124.6,83.3 127.1,79.3 129.7,79.4 132.3,111.7 134.9,90.4 137.4,78.8 140.0,67.7 142.6,72.8 145.1,69.9 147.7,65.0 150.3,70.0 152.9,100.1 155.4,84.1 158.0,98.2 160.6,128.8 163.1,116.0 165.7,46.8 168.3,105.6 170.9,126.3 173.4,95.9 176.0,57.2 178.6,85.9 181.1,77.6 183.7,90.1 186.3,86.6 188.9,61.9 191.4,70.5 194.0,86.7 196.6,68.8 199.1,65.4 201.7,89.1 204.3,80.2 206.9,80.5 209.4,97.4 212.0,64.0 214.6,88.2 217.1,96.5 219.7,115.9 222.3,108.3 224.9,57.1 227.4,106.0 230.0,77.2 232.6,91.9 235.1,75.7 237.7,74.1 240.3,99.4 242.9,90.5 245.4,83.3 248.0,83.0 250.6,85.6 253.1,90.9 255.7,73.6 258.3,60.9 260.9,75.2 263.4,98.7 266.0,77.8 268.6,84.0 271.1,76.6 273.7,51.3 276.3,89.0 278.9,85.3 281.4,101.4 284.0,90.4 286.6,95.6 289.1,55.7 291.7,79.5 294.3,95.6 296.9,49.7 299.4,109.5 302.0,69.3 304.6,66.5 307.1,74.6 309.7,89.9 312.3,87.5 314.9,91.4 317.4,70.7 320.0,127.9"/><text class="ink" x="14" y="16" font-size="12" text-anchor="start" font-weight="600">Noise</text></g></svg>
  <figcaption>The four parts on their own. In real series they are stacked on top of each other; the shop's sales combine a trend, two seasonalities and noise.</figcaption>
</figure>

**Trend.** The long-term direction of the series: up, down or flat. The shop
grows by about 35 units a year.

**Seasonality.** A pattern that repeats with a **fixed length.** It is tied
to the calendar: day of the week, month of the year, hour of the day. The
shop has two: 7 days (weekends high) and 12 months (December high).

**Cycle.** Ups and downs again, but **with no fixed length.** Economic swings
are like this: one downturn lasts 2 years, the next 5. This is the part most
often confused with seasonality. One question tells them apart: **is the
repeat tied to the calendar?** If yes, it is seasonality; if not, a cycle.

**Noise.** What is left over that none of the above explains. It cannot be
predicted; a good model is not expected to predict the noise but to capture
everything else and leave only the noise out.

A fifth case needs adding: **a structural break.** The rules of the series
change overnight: a new branch opens, the pricing policy changes, a pandemic
starts. Data from before the break struggles to describe what comes after.
Section 21 finds these automatically.

## Regular and irregular series

The shop series has **exactly one** row for every day; the gap between two
measurements is always one day. This is a **regular** series.

Not every series is like that:

- A sensor may send a reading only **when the value changes.**
- Transactions on a bank account arrive at random times of day.
- The recording system may have crashed on some days and saved nothing.

These are **irregular** series. Most time series tools expect a regular
series; turning an irregular one into a regular one (one value per hour, for
example) is the subject of Section 05.

## One, many and many at once

Three terms get mixed up; let us separate them from the start:

<figure class="fig">
  <div class="versus">
    <div><h4>Univariate</h4><p><b>One</b> value per date.</p><pre><code class="language-text">date        sales
2024-03-01    288
2024-03-02    384</code></pre></div>
    <div><h4>Multivariate</h4><p><b>Several</b> values per date.</p><pre><code class="language-text">date        sales  price
2024-03-01    288   19.9
2024-03-02    384   17.5</code></pre></div>
    <div><h4>Many series</h4><p>The same measure for <b>different units</b>.</p><pre><code class="language-text">date        store  sales
2024-03-01      A    288
2024-03-01      B    141</code></pre></div>
  </div>
  <figcaption>In a multivariate series the columns affect each other (price goes down, sales go up). With many series, each shop is a series of its own.</figcaption>
</figure>

Most of this track works with a univariate series, because every core idea
lives there. Outside variables come in Section 18, working with many series
in Section 08.

## What you do with a time series

There are three jobs and this track teaches all three:

1. **Understand it.** Is there a trend, which seasonality, did something
   break? Why did sales drop in March?
2. **Forecast it.** What will sales be over the next 30 days? How much stock
   is needed? How much load will the grid carry tomorrow at 18:00?
3. **Catch the unusual.** Why did site traffic drop to zero last night? Is
   this payment fraud?

## What changes from machine learning

What you learned in the Machine Learning track still applies here, but a few
rules flip:

<figure class="fig">
  <div class="versus">
    <div class="dim"><h4>Ordinary table</h4><p>Rows are <b>independent</b>; one does not affect another.<br>Shuffling is harmless.<br>Features come from other columns.<br>A random split is fine.</p></div>
    <div class="ok"><h4>Time series</h4><p>Neighbouring rows are <b>linked</b>.<br>Shuffling destroys the information.<br>The strongest feature is the series' <b>own past</b>.<br>Split <b>by time</b>: train on the past, test on the future.</p></div>
  </div>
  <figcaption>The model can be the same model; what changes is how the data is prepared and how it is measured.</figcaption>
</figure>

The last one matters most: **do not look at the future.** When you evaluate a
model you must imitate real life. In real life, on the day you forecast, you
only know the past.

A random split breaks this rule quietly. Split the shop data at random with
`train_test_split` and **219 of the 220 test days** fall **before** the last
day in the training data. The model sees December 2024 and "predicts" March
2022. The score looks great; in real life it is useless.

The right split is **by time**: the first 80% for training, the last 20% for
testing.

```text
train  2022-01-01 .. 2024-05-25   876 days
test   2024-05-26 .. 2024-12-31   220 days
```

The last training day comes before the first test day. The model learns only
from the past and is tested on a future it has never seen. Section 15 turns
this into a sturdier method (backtesting).

## The road through this track

<figure class="fig">
  <div class="flow">
    <span class="node">Dates</span><span class="arrow">→</span>
    <span class="node">The time index</span><span class="arrow">→</span>
    <span class="node">Resampling and windows</span><span class="arrow">→</span>
    <span class="node">Analysis</span><span class="arrow">→</span>
    <span class="node">Measuring</span><span class="arrow">→</span>
    <span class="node acc">Forecasting models</span>
  </div>
  <figcaption>The Basic level teaches working with dates, the Intermediate level reading and measuring a series, the Advanced level the models.</figcaption>
</figure>

The order is deliberate: forecasting models come last, because to know
whether a model works you first have to read the data correctly and measure
correctly. Most mistakes in time series are made not in the model but **in
the dates and in the measuring.**

## Summary

- A time series is **measurements ordered in time.** The order is the data;
  shuffle it and the information is gone (0.695 → 0.018).
- Its parts: **timestamp, value, frequency.** Dates are written in ISO 8601
  (`2022-01-01`).
- The first job is **to plot it.** A chart shows at a glance what the table
  cannot.
- Four patterns: **trend, seasonality** (fixed length, tied to the calendar),
  **cycle** (varying length), **noise.** Plus **structural breaks.**
- Series can be regular or irregular; univariate, multivariate, or many
  series at once.
- The biggest difference from machine learning: **no random splits.** Train
  on the past, test on the future.
