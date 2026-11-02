# The Logic of Hypothesis Testing

The server team changed the infrastructure. After the change you measured 40
page loads; the average came out a little above 850 ms. Did pages really get
slower, or is this difference the natural wobble of 40 random measurements?
The orderly way to answer this question is called a **hypothesis test**.
First let us see why it is needed: measurements always wobble; in the first
section we saw five samples from the same population give five different
means. To say "there is a difference" you have to show that the difference
is **too large to be explained by chance**.

## The data

```python
from ab_data import make_speed_test

loads = make_speed_test()
print(len(loads), round(loads.mean(), 1), round(loads.std(ddof=1), 1))
```

```text
40 883.2 123.5
```

The mean of the 40 measurements is 883.2 ms; before the change the
average was 850 ms. The difference is 33.2 ms.

## Two hypotheses

A test starts with two sentences:

- **The null hypothesis** ($H_0$): "Nothing changed." The true mean is still
  850 ms; the difference we see comes from chance.
- **The alternative hypothesis** ($H_1$): "Something changed." The true mean
  is not 850 ms.

The test does not try to **prove** $H_0$. It asks: "If $H_0$ were true, how
likely would it be to see a difference at least this large?" If the answer
is very small, believing $H_0$ becomes hard.

<figure class="fig">
<div class="flow">
<span class="node">Write H₀</span>
<span class="arrow">→</span>
<span class="node">Build the H₀ world</span>
<span class="arrow">→</span>
<span class="node">Compare the data with it</span>
<span class="arrow">→</span>
<span class="node acc">Decide</span>
</div>
<figcaption>The four steps of a hypothesis test. "The H₀ world": how the
measurements would be distributed if nothing had changed.</figcaption>
</figure>

## Building the H₀ world by simulation

We hold the population: all load times before the change. If nothing had
changed, samples of 40 would come from there. Let us draw 20,000 of them and
count how many have a mean **at least as far** from 850 as ours (in either
direction: faster or slower).

```python
import numpy as np
from ab_data import make_population, make_speed_test

old = make_population()["load_ms"].to_numpy()
loads = make_speed_test()
gap = abs(loads.mean() - 850)
rng = np.random.default_rng(71)
means = rng.choice(old, size=(20000, 40)).mean(axis=1)
far = np.abs(means - old.mean()) >= gap
print(round(far.mean(), 4))
```

```text
0.0797
```

Even in a world where nothing changed, about 0.080 of 40-sample
means are this far away. That number is the **p-value** itself: "the
probability of a result at least this extreme if $H_0$ is true".

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="405pt" height="222.808781pt" viewBox="0 0 405 222.808781" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 222.808781 
L 405 222.808781 
L 405 0 
L 0 0 
L 0 222.808781 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 7.2 184.608 
L 397.8 184.608 
L 397.8 7.2 
L 7.2 7.2 
L 7.2 184.608 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 24.954545 184.608 
L 29.886364 184.608 
L 29.886364 184.608 
L 24.954545 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_4">
    <path d="M 29.886364 184.608 
L 34.818182 184.608 
L 34.818182 184.608 
L 29.886364 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_5">
    <path d="M 34.818182 184.608 
L 39.75 184.608 
L 39.75 184.608 
L 34.818182 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_6">
    <path d="M 39.75 184.608 
L 44.681818 184.608 
L 44.681818 184.608 
L 39.75 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_7">
    <path d="M 44.681818 184.608 
L 49.613636 184.608 
L 49.613636 184.608 
L 44.681818 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_8">
    <path d="M 49.613636 184.608 
L 54.545455 184.608 
L 54.545455 184.608 
L 49.613636 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_9">
    <path d="M 54.545455 184.608 
L 59.477273 184.608 
L 59.477273 184.608 
L 54.545455 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_10">
    <path d="M 59.477273 184.608 
L 64.409091 184.608 
L 64.409091 184.608 
L 59.477273 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_11">
    <path d="M 64.409091 184.608 
L 69.340909 184.608 
L 69.340909 184.608 
L 64.409091 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_12">
    <path d="M 69.340909 184.608 
L 74.272727 184.608 
L 74.272727 184.608 
L 69.340909 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_13">
    <path d="M 74.272727 184.608 
L 79.204545 184.608 
L 79.204545 184.608 
L 74.272727 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_14">
    <path d="M 79.204545 184.608 
L 84.136364 184.608 
L 84.136364 184.608 
L 79.204545 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_15">
    <path d="M 84.136364 184.608 
L 89.068182 184.608 
L 89.068182 184.608 
L 84.136364 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_16">
    <path d="M 89.068182 184.608 
L 94 184.608 
L 94 184.608 
L 89.068182 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_17">
    <path d="M 94 184.608 
L 98.931818 184.608 
L 98.931818 184.608 
L 94 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_18">
    <path d="M 98.931818 184.608 
L 103.863636 184.608 
L 103.863636 184.608 
L 98.931818 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_19">
    <path d="M 103.863636 184.608 
L 108.795455 184.608 
L 108.795455 184.608 
L 103.863636 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_20">
    <path d="M 108.795455 184.608 
L 113.727273 184.608 
L 113.727273 184.608 
L 108.795455 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_21">
    <path d="M 113.727273 184.608 
L 118.659091 184.608 
L 118.659091 184.608 
L 113.727273 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_22">
    <path d="M 118.659091 184.608 
L 123.590909 184.608 
L 123.590909 184.608 
L 118.659091 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_23">
    <path d="M 123.590909 184.608 
L 128.522727 184.608 
L 128.522727 184.608 
L 123.590909 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_24">
    <path d="M 128.522727 184.608 
L 133.454545 184.608 
L 133.454545 184.608 
L 128.522727 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_25">
    <path d="M 133.454545 184.608 
L 138.386364 184.608 
L 138.386364 171.368597 
L 133.454545 171.368597 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_26">
    <path d="M 138.386364 184.608 
L 143.318182 184.608 
L 143.318182 142.368 
L 138.386364 142.368 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_27">
    <path d="M 143.318182 184.608 
L 148.25 184.608 
L 148.25 128.025313 
L 143.318182 128.025313 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_28">
    <path d="M 148.25 184.608 
L 153.181818 184.608 
L 153.181818 121.405612 
L 148.25 121.405612 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_29">
    <path d="M 153.181818 184.608 
L 158.113636 184.608 
L 158.113636 111.948896 
L 153.181818 111.948896 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_30">
    <path d="M 158.113636 184.608 
L 163.045455 184.608 
L 163.045455 101.073672 
L 158.113636 101.073672 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_31">
    <path d="M 163.045455 184.608 
L 167.977273 184.608 
L 167.977273 85.312478 
L 163.045455 85.312478 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_32">
    <path d="M 167.977273 184.608 
L 172.909091 184.608 
L 172.909091 76.170985 
L 167.977273 76.170985 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_33">
    <path d="M 172.909091 184.608 
L 177.840909 184.608 
L 177.840909 54.420537 
L 172.909091 54.420537 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_34">
    <path d="M 177.840909 184.608 
L 182.772727 184.608 
L 182.772727 40.86591 
L 177.840909 40.86591 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_35">
    <path d="M 182.772727 184.608 
L 187.704545 184.608 
L 187.704545 33.300537 
L 182.772727 33.300537 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_36">
    <path d="M 187.704545 184.608 
L 192.636364 184.608 
L 192.636364 15.805612 
L 187.704545 15.805612 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_37">
    <path d="M 192.636364 184.608 
L 197.568182 184.608 
L 197.568182 20.061134 
L 192.636364 20.061134 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_38">
    <path d="M 197.568182 184.608 
L 202.5 184.608 
L 202.5 19.588299 
L 197.568182 19.588299 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_39">
    <path d="M 202.5 184.608 
L 207.431818 184.608 
L 207.431818 15.648 
L 202.5 15.648 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_40">
    <path d="M 207.431818 184.608 
L 212.363636 184.608 
L 212.363636 21.637254 
L 207.431818 21.637254 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_41">
    <path d="M 212.363636 184.608 
L 217.295455 184.608 
L 217.295455 28.887403 
L 212.363636 28.887403 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_42">
    <path d="M 217.295455 184.608 
L 222.227273 184.608 
L 222.227273 34.246209 
L 217.295455 34.246209 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_43">
    <path d="M 222.227273 184.608 
L 227.159091 184.608 
L 227.159091 53.317254 
L 222.227273 53.317254 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_44">
    <path d="M 227.159091 184.608 
L 232.090909 184.608 
L 232.090909 55.523821 
L 227.159091 55.523821 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_45">
    <path d="M 232.090909 184.608 
L 237.022727 184.608 
L 237.022727 69.393672 
L 232.090909 69.393672 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_46">
    <path d="M 237.022727 184.608 
L 241.954545 184.608 
L 241.954545 83.89397 
L 237.022727 83.89397 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_47">
    <path d="M 241.954545 184.608 
L 246.886364 184.608 
L 246.886364 96.818149 
L 241.954545 96.818149 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_48">
    <path d="M 246.886364 184.608 
L 251.818182 184.608 
L 251.818182 105.486806 
L 246.886364 105.486806 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_49">
    <path d="M 251.818182 184.608 
L 256.75 184.608 
L 256.75 130.074269 
L 251.818182 130.074269 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_50">
    <path d="M 256.75 184.608 
L 261.681818 184.608 
L 261.681818 131.808 
L 256.75 131.808 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_51">
    <path d="M 261.681818 184.608 
L 266.613636 184.608 
L 266.613636 141.737552 
L 261.681818 141.737552 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_52">
    <path d="M 266.613636 184.608 
L 271.545455 184.608 
L 271.545455 177.830687 
L 266.613636 177.830687 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_53">
    <path d="M 271.545455 184.608 
L 276.477273 184.608 
L 276.477273 184.608 
L 271.545455 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_54">
    <path d="M 276.477273 184.608 
L 281.409091 184.608 
L 281.409091 184.608 
L 276.477273 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_55">
    <path d="M 281.409091 184.608 
L 286.340909 184.608 
L 286.340909 184.608 
L 281.409091 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_56">
    <path d="M 286.340909 184.608 
L 291.272727 184.608 
L 291.272727 184.608 
L 286.340909 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_57">
    <path d="M 291.272727 184.608 
L 296.204545 184.608 
L 296.204545 184.608 
L 291.272727 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_58">
    <path d="M 296.204545 184.608 
L 301.136364 184.608 
L 301.136364 184.608 
L 296.204545 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_59">
    <path d="M 301.136364 184.608 
L 306.068182 184.608 
L 306.068182 184.608 
L 301.136364 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_60">
    <path d="M 306.068182 184.608 
L 311 184.608 
L 311 184.608 
L 306.068182 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_61">
    <path d="M 311 184.608 
L 315.931818 184.608 
L 315.931818 184.608 
L 311 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_62">
    <path d="M 315.931818 184.608 
L 320.863636 184.608 
L 320.863636 184.608 
L 315.931818 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_63">
    <path d="M 320.863636 184.608 
L 325.795455 184.608 
L 325.795455 184.608 
L 320.863636 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_64">
    <path d="M 325.795455 184.608 
L 330.727273 184.608 
L 330.727273 184.608 
L 325.795455 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_65">
    <path d="M 330.727273 184.608 
L 335.659091 184.608 
L 335.659091 184.608 
L 330.727273 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_66">
    <path d="M 335.659091 184.608 
L 340.590909 184.608 
L 340.590909 184.608 
L 335.659091 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_67">
    <path d="M 340.590909 184.608 
L 345.522727 184.608 
L 345.522727 184.608 
L 340.590909 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_68">
    <path d="M 345.522727 184.608 
L 350.454545 184.608 
L 350.454545 184.608 
L 345.522727 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_69">
    <path d="M 350.454545 184.608 
L 355.386364 184.608 
L 355.386364 184.608 
L 350.454545 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_70">
    <path d="M 355.386364 184.608 
L 360.318182 184.608 
L 360.318182 184.608 
L 355.386364 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_71">
    <path d="M 360.318182 184.608 
L 365.25 184.608 
L 365.25 184.608 
L 360.318182 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_72">
    <path d="M 365.25 184.608 
L 370.181818 184.608 
L 370.181818 184.608 
L 365.25 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_73">
    <path d="M 370.181818 184.608 
L 375.113636 184.608 
L 375.113636 184.608 
L 370.181818 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_74">
    <path d="M 375.113636 184.608 
L 380.045455 184.608 
L 380.045455 184.608 
L 375.113636 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #8b5cf6; opacity: 0.75"/>
   </g>
   <g id="patch_75">
    <path d="M 24.954545 184.608 
L 29.886364 184.608 
L 29.886364 184.608 
L 24.954545 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_76">
    <path d="M 29.886364 184.608 
L 34.818182 184.608 
L 34.818182 184.608 
L 29.886364 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_77">
    <path d="M 34.818182 184.608 
L 39.75 184.608 
L 39.75 184.608 
L 34.818182 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_78">
    <path d="M 39.75 184.608 
L 44.681818 184.608 
L 44.681818 184.608 
L 39.75 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_79">
    <path d="M 44.681818 184.608 
L 49.613636 184.608 
L 49.613636 184.608 
L 44.681818 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_80">
    <path d="M 49.613636 184.608 
L 54.545455 184.608 
L 54.545455 184.608 
L 49.613636 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_81">
    <path d="M 54.545455 184.608 
L 59.477273 184.608 
L 59.477273 184.450388 
L 54.545455 184.450388 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_82">
    <path d="M 59.477273 184.608 
L 64.409091 184.608 
L 64.409091 184.608 
L 59.477273 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_83">
    <path d="M 64.409091 184.608 
L 69.340909 184.608 
L 69.340909 184.135164 
L 64.409091 184.135164 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_84">
    <path d="M 69.340909 184.608 
L 74.272727 184.608 
L 74.272727 184.608 
L 69.340909 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_85">
    <path d="M 74.272727 184.608 
L 79.204545 184.608 
L 79.204545 183.347104 
L 74.272727 183.347104 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_86">
    <path d="M 79.204545 184.608 
L 84.136364 184.608 
L 84.136364 183.347104 
L 79.204545 183.347104 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_87">
    <path d="M 84.136364 184.608 
L 89.068182 184.608 
L 89.068182 183.189493 
L 84.136364 183.189493 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_88">
    <path d="M 89.068182 184.608 
L 94 184.608 
L 94 181.928597 
L 89.068182 181.928597 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_89">
    <path d="M 94 184.608 
L 98.931818 184.608 
L 98.931818 182.559045 
L 94 182.559045 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_90">
    <path d="M 98.931818 184.608 
L 103.863636 184.608 
L 103.863636 180.982925 
L 98.931818 180.982925 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_91">
    <path d="M 103.863636 184.608 
L 108.795455 184.608 
L 108.795455 178.303522 
L 103.863636 178.303522 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_92">
    <path d="M 108.795455 184.608 
L 113.727273 184.608 
L 113.727273 175.781731 
L 108.795455 175.781731 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_93">
    <path d="M 113.727273 184.608 
L 118.659091 184.608 
L 118.659091 173.890388 
L 113.727273 173.890388 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_94">
    <path d="M 118.659091 184.608 
L 123.590909 184.608 
L 123.590909 169.634866 
L 118.659091 169.634866 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_95">
    <path d="M 123.590909 184.608 
L 128.522727 184.608 
L 128.522727 165.221731 
L 123.590909 165.221731 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_96">
    <path d="M 128.522727 184.608 
L 133.454545 184.608 
L 133.454545 155.134567 
L 128.522727 155.134567 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_97">
    <path d="M 133.454545 184.608 
L 138.386364 184.608 
L 138.386364 163.172776 
L 133.454545 163.172776 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_98">
    <path d="M 138.386364 184.608 
L 143.318182 184.608 
L 143.318182 184.608 
L 138.386364 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_99">
    <path d="M 143.318182 184.608 
L 148.25 184.608 
L 148.25 184.608 
L 143.318182 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_100">
    <path d="M 148.25 184.608 
L 153.181818 184.608 
L 153.181818 184.608 
L 148.25 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_101">
    <path d="M 153.181818 184.608 
L 158.113636 184.608 
L 158.113636 184.608 
L 153.181818 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_102">
    <path d="M 158.113636 184.608 
L 163.045455 184.608 
L 163.045455 184.608 
L 158.113636 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_103">
    <path d="M 163.045455 184.608 
L 167.977273 184.608 
L 167.977273 184.608 
L 163.045455 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_104">
    <path d="M 167.977273 184.608 
L 172.909091 184.608 
L 172.909091 184.608 
L 167.977273 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_105">
    <path d="M 172.909091 184.608 
L 177.840909 184.608 
L 177.840909 184.608 
L 172.909091 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_106">
    <path d="M 177.840909 184.608 
L 182.772727 184.608 
L 182.772727 184.608 
L 177.840909 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_107">
    <path d="M 182.772727 184.608 
L 187.704545 184.608 
L 187.704545 184.608 
L 182.772727 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_108">
    <path d="M 187.704545 184.608 
L 192.636364 184.608 
L 192.636364 184.608 
L 187.704545 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_109">
    <path d="M 192.636364 184.608 
L 197.568182 184.608 
L 197.568182 184.608 
L 192.636364 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_110">
    <path d="M 197.568182 184.608 
L 202.5 184.608 
L 202.5 184.608 
L 197.568182 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_111">
    <path d="M 202.5 184.608 
L 207.431818 184.608 
L 207.431818 184.608 
L 202.5 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_112">
    <path d="M 207.431818 184.608 
L 212.363636 184.608 
L 212.363636 184.608 
L 207.431818 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_113">
    <path d="M 212.363636 184.608 
L 217.295455 184.608 
L 217.295455 184.608 
L 212.363636 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_114">
    <path d="M 217.295455 184.608 
L 222.227273 184.608 
L 222.227273 184.608 
L 217.295455 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_115">
    <path d="M 222.227273 184.608 
L 227.159091 184.608 
L 227.159091 184.608 
L 222.227273 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_116">
    <path d="M 227.159091 184.608 
L 232.090909 184.608 
L 232.090909 184.608 
L 227.159091 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_117">
    <path d="M 232.090909 184.608 
L 237.022727 184.608 
L 237.022727 184.608 
L 232.090909 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_118">
    <path d="M 237.022727 184.608 
L 241.954545 184.608 
L 241.954545 184.608 
L 237.022727 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_119">
    <path d="M 241.954545 184.608 
L 246.886364 184.608 
L 246.886364 184.608 
L 241.954545 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_120">
    <path d="M 246.886364 184.608 
L 251.818182 184.608 
L 251.818182 184.608 
L 246.886364 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_121">
    <path d="M 251.818182 184.608 
L 256.75 184.608 
L 256.75 184.608 
L 251.818182 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_122">
    <path d="M 256.75 184.608 
L 261.681818 184.608 
L 261.681818 184.608 
L 256.75 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_123">
    <path d="M 261.681818 184.608 
L 266.613636 184.608 
L 266.613636 184.608 
L 261.681818 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_124">
    <path d="M 266.613636 184.608 
L 271.545455 184.608 
L 271.545455 160.178149 
L 266.613636 160.178149 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_125">
    <path d="M 271.545455 184.608 
L 276.477273 184.608 
L 276.477273 157.81397 
L 271.545455 157.81397 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_126">
    <path d="M 276.477273 184.608 
L 281.409091 184.608 
L 281.409091 161.911881 
L 276.477273 161.911881 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_127">
    <path d="M 281.409091 184.608 
L 286.340909 184.608 
L 286.340909 169.004418 
L 281.409091 169.004418 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_128">
    <path d="M 286.340909 184.608 
L 291.272727 184.608 
L 291.272727 172.471881 
L 286.340909 172.471881 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_129">
    <path d="M 291.272727 184.608 
L 296.204545 184.608 
L 296.204545 176.885015 
L 291.272727 176.885015 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_130">
    <path d="M 296.204545 184.608 
L 301.136364 184.608 
L 301.136364 178.303522 
L 296.204545 178.303522 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_131">
    <path d="M 301.136364 184.608 
L 306.068182 184.608 
L 306.068182 181.928597 
L 301.136364 181.928597 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_132">
    <path d="M 306.068182 184.608 
L 311 184.608 
L 311 181.770985 
L 306.068182 181.770985 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_133">
    <path d="M 311 184.608 
L 315.931818 184.608 
L 315.931818 182.086209 
L 311 182.086209 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_134">
    <path d="M 315.931818 184.608 
L 320.863636 184.608 
L 320.863636 183.504716 
L 315.931818 183.504716 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_135">
    <path d="M 320.863636 184.608 
L 325.795455 184.608 
L 325.795455 183.81994 
L 320.863636 183.81994 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_136">
    <path d="M 325.795455 184.608 
L 330.727273 184.608 
L 330.727273 184.608 
L 325.795455 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_137">
    <path d="M 330.727273 184.608 
L 335.659091 184.608 
L 335.659091 183.662328 
L 330.727273 183.662328 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_138">
    <path d="M 335.659091 184.608 
L 340.590909 184.608 
L 340.590909 184.608 
L 335.659091 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_139">
    <path d="M 340.590909 184.608 
L 345.522727 184.608 
L 345.522727 184.608 
L 340.590909 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_140">
    <path d="M 345.522727 184.608 
L 350.454545 184.608 
L 350.454545 184.292776 
L 345.522727 184.292776 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_141">
    <path d="M 350.454545 184.608 
L 355.386364 184.608 
L 355.386364 184.608 
L 350.454545 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_142">
    <path d="M 355.386364 184.608 
L 360.318182 184.608 
L 360.318182 184.450388 
L 355.386364 184.450388 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_143">
    <path d="M 360.318182 184.608 
L 365.25 184.608 
L 365.25 184.450388 
L 360.318182 184.450388 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_144">
    <path d="M 365.25 184.608 
L 370.181818 184.608 
L 370.181818 184.608 
L 365.25 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_145">
    <path d="M 370.181818 184.608 
L 375.113636 184.608 
L 375.113636 184.608 
L 370.181818 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="patch_146">
    <path d="M 375.113636 184.608 
L 380.045455 184.608 
L 380.045455 184.608 
L 375.113636 184.608 
z
" clip-path="url(#pf1f00c7e97)" style="fill: #f97316; opacity: 0.9"/>
   </g>
   <g id="matplotlib.axis_1">
    <g id="xtick_1">
     <g id="line2d_1">
      <defs>
       <path id="m15aed4d867" d="M 0 0 
L 0 3.5 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m15aed4d867" x="54.545455" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="54.545455" y="199.205656" transform="rotate(-0 54.545455 199.205656)">775</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="103.863636" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="103.863636" y="199.205656" transform="rotate(-0 103.863636 199.205656)">800</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="153.181818" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="153.181818" y="199.205656" transform="rotate(-0 153.181818 199.205656)">825</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="202.5" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="202.5" y="199.205656" transform="rotate(-0 202.5 199.205656)">850</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="251.818182" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="251.818182" y="199.205656" transform="rotate(-0 251.818182 199.205656)">875</text>
     </g>
    </g>
    <g id="xtick_6">
     <g id="line2d_6">
      <g>
       <use xlink:href="#m15aed4d867" x="301.136364" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_6">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="301.136364" y="199.205656" transform="rotate(-0 301.136364 199.205656)">900</text>
     </g>
    </g>
    <g id="xtick_7">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m15aed4d867" x="350.454545" y="184.608" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="350.454545" y="199.205656" transform="rotate(-0 350.454545 199.205656)">925</text>
     </g>
    </g>
    <g id="text_8">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="202.5" y="213.206438" transform="rotate(-0 202.5 213.206438)">Mean of 40 measurements (ms), if nothing had changed</text>
    </g>
   </g>
   <g id="matplotlib.axis_2"/>
   <g id="line2d_8">
    <path d="M 268.043864 184.608 
L 268.043864 7.2 
" clip-path="url(#pf1f00c7e97)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: currentColor; stroke-width: 1.5"/>
   </g>
   <g id="patch_147">
    <path d="M 7.2 184.608 
L 7.2 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_148">
    <path d="M 397.8 184.608 
L 397.8 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_149">
    <path d="M 7.2 184.608 
L 397.8 184.608 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_150">
    <path d="M 7.2 7.2 
L 397.8 7.2 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_151">
     <path d="M 15.3 22.138594 
L 33.3 22.138594 
L 33.3 15.838594 
L 15.3 15.838594 
z
" style="fill: #8b5cf6; opacity: 0.75"/>
    </g>
    <g id="text_9">
     <text style="font-size: 9px; font-family:inherit; text-anchor: start; fill: currentColor" x="40.5" y="22.138594" transform="rotate(-0 40.5 22.138594)">closer</text>
    </g>
    <g id="patch_152">
     <path d="M 15.3 35.639297 
L 33.3 35.639297 
L 33.3 29.339297 
L 15.3 29.339297 
z
" style="fill: #f97316; opacity: 0.9"/>
    </g>
    <g id="text_10">
     <text style="font-size: 9px; font-family:inherit; text-anchor: start; fill: currentColor" x="40.5" y="35.639297" transform="rotate(-0 40.5 35.639297)">at least as far as ours</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="pf1f00c7e97">
   <rect x="7.2" y="7.2" width="390.6" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>20,000 sample means in the H₀ world. The dashed line is our mean. The share of the orange tails is the p-value.</figcaption>
</figure>

## The same with a formula: the t-test

Usually you do not hold the population. Then we build the H₀ world from the
central limit theorem: if $H_0$ is true, the sample mean comes from a
distribution centred on $\mu_0 = 850$ with width $s/\sqrt{n}$. The number
that measures the difference in standard errors is the **test statistic**:

$$t = \dfrac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

```python
from scipy import stats
from ab_data import make_speed_test

loads = make_speed_test()
result = stats.ttest_1samp(loads, 850)
print(round(result.statistic, 3), round(result.pvalue, 4))
```

```text
1.702 0.0968
```

- $t$ = 1.702: the mean is about 1.7 standard errors from 850.
- p = 0.0968. Close to the simulation (0.080) but not the
  same: the simulation knew the population's true deviation, while the
  t-test estimates it from the sample and pays for that with the heavier
  tails of the t distribution.

## Deciding: the α threshold

How small is "small enough"? We choose it **before** looking at the data.
This threshold is called the **significance level** ($\alpha$); the most
common is 0.05.

- If $p < \alpha$, "we reject $H_0$": the difference is **statistically
  significant**.
- If $p \ge \alpha$, "we fail to reject $H_0$".

Here p = 0.0968 > 0.05: $H_0$ was not rejected. Careful: this does
**not** mean "nothing changed". We generated the data and know the truth:
the new server's true mean is 890 ms, so a 40 ms slowdown **exists**. Forty
measurements were not enough to show it.

## Two kinds of error

| | $H_0$ really true | $H_0$ really false |
|---|---|---|
| $H_0$ rejected | **type I error** (false alarm) | correct decision |
| $H_0$ not rejected | correct decision | **type II error** (a miss) |

- **Type I error**: saying "there is a difference" when there is none. Its
  probability is exactly $\alpha$; since we choose the threshold, we control
  this error.
- **Type II error**: missing a difference that exists. That is what happened
  in our server example.
- **Power**: the probability of catching a difference that exists, that is
  1 − the probability of a type II error.

Let us measure both by simulation. First in the world where nothing
changed, then in the world where loads really became 40 ms slower:

```python
import numpy as np
from scipy import stats
from ab_data import make_population

old = make_population()["load_ms"].to_numpy()
rng = np.random.default_rng(72)
same = rng.choice(old, size=(5000, 40))
p = stats.ttest_1samp(same, 850, axis=1).pvalue
print("H0", round((p < 0.05).mean(), 3))
for n in [40, 160]:
    slower = rng.choice(old, size=(5000, n)) + 40
    p = stats.ttest_1samp(slower, 850, axis=1).pvalue
    print(n, round((p < 0.05).mean(), 3))
```

```text
H0 0.052
40 0.525
160 0.984
```

- In the world where nothing changed, 5.2% of tests gave a false
  alarm: $\alpha = 0.05$ kept its promise.
- With a real 40 ms slowdown and 40 measurements, only 52.5% of
  tests caught it. Our test's miss is not bad luck but common: this design's
  power is about a coin toss.
- With 160 measurements the power is 98.4%. The same difference,
  four times the data: misses almost disappear. Computing in advance how many
  measurements are needed is called **power analysis**; it gets its own
  section later.

## One-sided or two-sided?

The test above was **two-sided**: "different from 850?" Sometimes the
question is one-sided: "did it get slower?" Then only one tail is examined:

```python
from scipy import stats
from ab_data import make_speed_test

loads = make_speed_test()
print(round(stats.ttest_1samp(loads, 850, alternative="greater").pvalue, 4))
```

```text
0.0484
```

One-sided p = 0.0484: half of the two-sided one and below 0.05.
There is a trap here. The direction is chosen **before** looking at the data,
for a reason that comes from the subject. Seeing the result and then saying
"let me make it one-sided" means testing the same data twice and picking
the convenient one, which secretly doubles the false alarm rate. In the next
section we will look at such tricks in detail.

## Summary

- A hypothesis test asks "if $H_0$ were true, how likely is a result this
  extreme?"; the answer is the p-value.
- The H₀ world is built by simulation (if you hold the population) or by a
  formula (the t-test).
- $\alpha$ is chosen before looking at the data; if $p < \alpha$, $H_0$ is
  rejected.
- "Not rejected" ≠ "no difference". A type I error is a false alarm, a type
  II error a miss; power is the chance of not missing and grows with the
  sample.
- A one-sided test is chosen only in advance and with a reason.
