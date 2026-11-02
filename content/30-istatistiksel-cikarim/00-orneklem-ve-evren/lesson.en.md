# Sample and Population

How many minutes do an app's users stay on average? Did the new design
increase sales? The answer to such questions lies in measuring **everyone**.
But most of the time you cannot measure everyone: it is too expensive, it
takes too long, or not everyone exists yet (tomorrow's users are part of the
question too). So you measure **some** of them and say something about
**all** of them.

This part of statistics is called **inference**: drawing a conclusion about
the whole from a small part, and saying how sure you are. Every section of
this module is a piece of that one idea. The first step is to tell two words
apart: **population** and **sample**.

## Population and sample

- **Population**: the **whole** group you want to say something about. Here,
  all the users of the app.
- **Sample**: the part you pick from the population and actually measure.

On this path we built the population ourselves: `make_population` in
`ab_data.py` produces the 100,000 users of a made-up shopping app. It runs
with a fixed seed, so every computer gets the same numbers. In real life you
never hold the population; here you do, because the only way to see whether
a method finds the **right** answer is to know the right answer.

```python
from ab_data import make_population

users = make_population()
print(len(users))
print(users.head(3).to_string())
print(round(users["minutes"].mean(), 2))
print(round(users["bought"].mean(), 3))
```

```text
100000
   user_id  age  visits  minutes  bought  spend  load_ms
0  U000001   38       1     7.22       0    0.0      813
1  U000002   41       4     3.15       0    0.0      708
2  U000003   35       8    10.88       0    0.0      767
9.04
0.114
```

- Each row is a user. `minutes` is the average session length (in minutes),
  `visits` the number of visits last month, `bought` is 1 if they bought
  something last month.
- Over all users the average session is 9.04 minutes and the share
  who bought is 11.4%. These are the **population's** true values.

## Parameter and statistic

A number computed from the population is a **parameter**; one computed from
a sample is a **statistic**. They are written with different letters so they
are not confused:

| | Population | Sample |
|---|---|---|
| How many people | $N$ | $n$ |
| Mean | $\mu$ ("mu") | $\bar{x}$ ("x bar") |
| Share (proportion) | $p$ | $\hat{p}$ ("p hat") |
| Known? | Almost never | Always: you measured it |

The whole job of inference: use the $\bar{x}$ you have to talk about the
$\mu$ you do not know.

## Every sample gives a different answer

Now let us pretend we do not know the population and pick 100 users at
random. `sample(n=100, random_state=...)` gives every user an equal chance of
being picked; this is a **simple random sample**. `random_state` fixes which
100 people are picked.

```python
from ab_data import make_population

users = make_population()
for seed in range(1, 6):
    sample = users.sample(n=100, random_state=seed)
    print(seed, round(sample["minutes"].mean(), 2))
```

```text
1 9.58
2 9.65
3 9.69
4 10.02
5 9.66
```

- Five samples, five different means; none is exactly 9.04. There
  is no bug: a different 100 people give a different mean.
- All five came out above the truth. That is chance too: below, with a
  thousand samples, we will see that about half of the means fall below the
  truth. Reading a direction from five samples is as risky as from one.
- The way a sample statistic misses the population parameter by chance is
  called **sampling error**. The word "error" does not mean someone did
  something wrong; it is the natural wobble of random selection.

## Look at thousands of samples, not one

We cannot tell how lucky a single sample was. But we can repeat the
experiment a thousand times: pick another 100 people each time and note the
mean. That shows **how** the sample mean wobbles. This method is called
**simulation**, and we will use it often on this path.

```python
import numpy as np
from ab_data import make_population

users = make_population()
true_mean = users["minutes"].mean()
for n in [25, 100, 400]:
    means = []
    for seed in range(1000):
        sample = users["minutes"].sample(n=n, random_state=seed)
        means.append(sample.mean())
    miss = np.abs(np.array(means) - true_mean)
    print(n, round(min(means), 2), round(max(means), 2),
          round(miss.mean(), 3), round((miss <= 1).mean(), 3))
```

```text
25 5.67 14.04 0.983 0.565
100 7.37 11.21 0.514 0.885
400 8.04 9.98 0.245 0.999
```

Columns: the sample size, the smallest and largest of the thousand means, how
far they missed on average (minutes) and the share that landed within 1
minute of the truth.

- With 25-person samples the mean wandered between 5.67 and
  14.04; only 56.5% were within 1 minute of the truth.
- With 400 people the range narrowed to 8.04–9.98 and
  99.9% fell within 1 minute.
- A sample 16 times larger cut the average miss from 0.98 to
  0.24 minutes: four times smaller, not 16. We will measure this
  "square-root rule" in the Estimation and Standard Error section.

<figure class="fig">
<svg style="stroke-linejoin:round;stroke-linecap:butt" xmlns:xlink="http://www.w3.org/1999/xlink" width="438.725781pt" height="225.724983pt" viewBox="0 0 438.725781 225.724983" xmlns="http://www.w3.org/2000/svg" version="1.1">
 <g id="figure_1">
  <g id="patch_1">
   <path d="M 0 225.724983 
L 438.725781 225.724983 
L 438.725781 0 
L 0 0 
L 0 225.724983 
z
" style="fill: none"/>
  </g>
  <g id="axes_1">
   <g id="patch_2">
    <path d="M 40.925781 187.524201 
L 431.525781 187.524201 
L 431.525781 10.116201 
L 40.925781 10.116201 
L 40.925781 187.524201 
z
" style="fill: none"/>
   </g>
   <g id="patch_3">
    <path d="M 58.680327 187.524201 
L 66.571236 187.524201 
L 66.571236 185.00241 
L 58.680327 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_4">
    <path d="M 66.571236 187.524201 
L 74.462145 187.524201 
L 74.462145 187.524201 
L 66.571236 187.524201 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_5">
    <path d="M 74.462145 187.524201 
L 82.353054 187.524201 
L 82.353054 182.480619 
L 74.462145 182.480619 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_6">
    <path d="M 82.353054 187.524201 
L 90.243963 187.524201 
L 90.243963 182.480619 
L 82.353054 182.480619 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_7">
    <path d="M 90.243963 187.524201 
L 98.134872 187.524201 
L 98.134872 167.349873 
L 90.243963 167.349873 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_8">
    <path d="M 98.134872 187.524201 
L 106.025781 187.524201 
L 106.025781 169.871664 
L 98.134872 169.871664 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_9">
    <path d="M 106.025781 187.524201 
L 113.91669 187.524201 
L 113.91669 157.262709 
L 106.025781 157.262709 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_10">
    <path d="M 113.91669 187.524201 
L 121.807599 187.524201 
L 121.807599 147.175545 
L 113.91669 147.175545 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_11">
    <path d="M 121.807599 187.524201 
L 129.698509 187.524201 
L 129.698509 139.610171 
L 121.807599 139.610171 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_12">
    <path d="M 129.698509 187.524201 
L 137.589418 187.524201 
L 137.589418 104.305097 
L 129.698509 104.305097 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_13">
    <path d="M 137.589418 187.524201 
L 145.480327 187.524201 
L 145.480327 99.261515 
L 137.589418 99.261515 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_14">
    <path d="M 145.480327 187.524201 
L 153.371236 187.524201 
L 153.371236 63.95644 
L 145.480327 63.95644 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_15">
    <path d="M 153.371236 187.524201 
L 161.262145 187.524201 
L 161.262145 56.391067 
L 153.371236 56.391067 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_16">
    <path d="M 161.262145 187.524201 
L 169.153054 187.524201 
L 169.153054 81.608977 
L 161.262145 81.608977 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_17">
    <path d="M 169.153054 187.524201 
L 177.043963 187.524201 
L 177.043963 63.95644 
L 169.153054 63.95644 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_18">
    <path d="M 177.043963 187.524201 
L 184.934872 187.524201 
L 184.934872 46.303903 
L 177.043963 46.303903 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_19">
    <path d="M 184.934872 187.524201 
L 192.825781 187.524201 
L 192.825781 23.607783 
L 184.934872 23.607783 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_20">
    <path d="M 192.825781 187.524201 
L 200.71669 187.524201 
L 200.71669 43.782112 
L 192.825781 43.782112 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_21">
    <path d="M 200.71669 187.524201 
L 208.607599 187.524201 
L 208.607599 18.564201 
L 200.71669 18.564201 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_22">
    <path d="M 208.607599 187.524201 
L 216.498509 187.524201 
L 216.498509 48.825694 
L 208.607599 48.825694 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_23">
    <path d="M 216.498509 187.524201 
L 224.389418 187.524201 
L 224.389418 36.216739 
L 216.498509 36.216739 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_24">
    <path d="M 224.389418 187.524201 
L 232.280327 187.524201 
L 232.280327 79.087186 
L 224.389418 79.087186 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_25">
    <path d="M 232.280327 187.524201 
L 240.171236 187.524201 
L 240.171236 84.130768 
L 232.280327 84.130768 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_26">
    <path d="M 240.171236 187.524201 
L 248.062145 187.524201 
L 248.062145 106.826888 
L 240.171236 106.826888 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_27">
    <path d="M 248.062145 187.524201 
L 255.953054 187.524201 
L 255.953054 79.087186 
L 248.062145 79.087186 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_28">
    <path d="M 255.953054 187.524201 
L 263.843963 187.524201 
L 263.843963 132.044798 
L 255.953054 132.044798 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_29">
    <path d="M 263.843963 187.524201 
L 271.734872 187.524201 
L 271.734872 109.348679 
L 263.843963 109.348679 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_30">
    <path d="M 271.734872 187.524201 
L 279.625781 187.524201 
L 279.625781 129.523007 
L 271.734872 129.523007 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_31">
    <path d="M 279.625781 187.524201 
L 287.51669 187.524201 
L 287.51669 144.653753 
L 279.625781 144.653753 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_32">
    <path d="M 287.51669 187.524201 
L 295.407599 187.524201 
L 295.407599 157.262709 
L 287.51669 157.262709 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_33">
    <path d="M 295.407599 187.524201 
L 303.298509 187.524201 
L 303.298509 154.740918 
L 295.407599 154.740918 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_34">
    <path d="M 303.298509 187.524201 
L 311.189418 187.524201 
L 311.189418 167.349873 
L 303.298509 167.349873 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_35">
    <path d="M 311.189418 187.524201 
L 319.080327 187.524201 
L 319.080327 159.7845 
L 311.189418 159.7845 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_36">
    <path d="M 319.080327 187.524201 
L 326.971236 187.524201 
L 326.971236 172.393455 
L 319.080327 172.393455 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_37">
    <path d="M 326.971236 187.524201 
L 334.862145 187.524201 
L 334.862145 185.00241 
L 326.971236 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_38">
    <path d="M 334.862145 187.524201 
L 342.753054 187.524201 
L 342.753054 182.480619 
L 334.862145 182.480619 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_39">
    <path d="M 342.753054 187.524201 
L 350.643963 187.524201 
L 350.643963 182.480619 
L 342.753054 182.480619 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_40">
    <path d="M 350.643963 187.524201 
L 358.534872 187.524201 
L 358.534872 179.958828 
L 350.643963 179.958828 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_41">
    <path d="M 358.534872 187.524201 
L 366.425781 187.524201 
L 366.425781 187.524201 
L 358.534872 187.524201 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_42">
    <path d="M 366.425781 187.524201 
L 374.31669 187.524201 
L 374.31669 187.524201 
L 366.425781 187.524201 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_43">
    <path d="M 374.31669 187.524201 
L 382.207599 187.524201 
L 382.207599 185.00241 
L 374.31669 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_44">
    <path d="M 382.207599 187.524201 
L 390.098509 187.524201 
L 390.098509 187.524201 
L 382.207599 187.524201 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_45">
    <path d="M 390.098509 187.524201 
L 397.989418 187.524201 
L 397.989418 187.524201 
L 390.098509 187.524201 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_46">
    <path d="M 397.989418 187.524201 
L 405.880327 187.524201 
L 405.880327 187.524201 
L 397.989418 187.524201 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_47">
    <path d="M 405.880327 187.524201 
L 413.771236 187.524201 
L 413.771236 182.480619 
L 405.880327 182.480619 
z
" clip-path="url(#p745cbc8068)" style="fill: #1f77b4; opacity: 0.65"/>
   </g>
   <g id="patch_48">
    <path d="M 159.156842 187.524201 
L 160.98964 187.524201 
L 160.98964 185.00241 
L 159.156842 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_49">
    <path d="M 160.98964 187.524201 
L 162.822438 187.524201 
L 162.822438 185.00241 
L 160.98964 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_50">
    <path d="M 162.822438 187.524201 
L 164.655236 187.524201 
L 164.655236 187.524201 
L 162.822438 187.524201 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_51">
    <path d="M 164.655236 187.524201 
L 166.488034 187.524201 
L 166.488034 185.00241 
L 164.655236 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_52">
    <path d="M 166.488034 187.524201 
L 168.320832 187.524201 
L 168.320832 185.00241 
L 166.488034 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_53">
    <path d="M 168.320832 187.524201 
L 170.15363 187.524201 
L 170.15363 185.00241 
L 168.320832 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_54">
    <path d="M 170.15363 187.524201 
L 171.986428 187.524201 
L 171.986428 185.00241 
L 170.15363 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_55">
    <path d="M 171.986428 187.524201 
L 173.819226 187.524201 
L 173.819226 182.480619 
L 171.986428 182.480619 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_56">
    <path d="M 173.819226 187.524201 
L 175.652024 187.524201 
L 175.652024 167.349873 
L 173.819226 167.349873 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_57">
    <path d="M 175.652024 187.524201 
L 177.484822 187.524201 
L 177.484822 172.393455 
L 175.652024 172.393455 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_58">
    <path d="M 177.484822 187.524201 
L 179.31762 187.524201 
L 179.31762 164.828082 
L 177.484822 164.828082 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_59">
    <path d="M 179.31762 187.524201 
L 181.150418 187.524201 
L 181.150418 142.131962 
L 179.31762 142.131962 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_60">
    <path d="M 181.150418 187.524201 
L 182.983216 187.524201 
L 182.983216 142.131962 
L 181.150418 142.131962 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_61">
    <path d="M 182.983216 187.524201 
L 184.816014 187.524201 
L 184.816014 111.87047 
L 182.983216 111.87047 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_62">
    <path d="M 184.816014 187.524201 
L 186.648812 187.524201 
L 186.648812 116.914052 
L 184.816014 116.914052 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_63">
    <path d="M 186.648812 187.524201 
L 188.48161 187.524201 
L 188.48161 124.479425 
L 186.648812 124.479425 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_64">
    <path d="M 188.48161 187.524201 
L 190.314408 187.524201 
L 190.314408 91.696142 
L 188.48161 91.696142 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_65">
    <path d="M 190.314408 187.524201 
L 192.147205 187.524201 
L 192.147205 74.043604 
L 190.314408 74.043604 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_66">
    <path d="M 192.147205 187.524201 
L 193.980003 187.524201 
L 193.980003 58.912858 
L 192.147205 58.912858 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_67">
    <path d="M 193.980003 187.524201 
L 195.812801 187.524201 
L 195.812801 106.826888 
L 193.980003 106.826888 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_68">
    <path d="M 195.812801 187.524201 
L 197.645599 187.524201 
L 197.645599 61.434649 
L 195.812801 61.434649 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_69">
    <path d="M 197.645599 187.524201 
L 199.478397 187.524201 
L 199.478397 28.651365 
L 197.645599 28.651365 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_70">
    <path d="M 199.478397 187.524201 
L 201.311195 187.524201 
L 201.311195 26.129574 
L 199.478397 26.129574 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_71">
    <path d="M 201.311195 187.524201 
L 203.143993 187.524201 
L 203.143993 36.216739 
L 201.311195 36.216739 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_72">
    <path d="M 203.143993 187.524201 
L 204.976791 187.524201 
L 204.976791 71.521813 
L 203.143993 71.521813 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_73">
    <path d="M 204.976791 187.524201 
L 206.809589 187.524201 
L 206.809589 84.130768 
L 204.976791 84.130768 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_74">
    <path d="M 206.809589 187.524201 
L 208.642387 187.524201 
L 208.642387 53.869276 
L 206.809589 53.869276 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_75">
    <path d="M 208.642387 187.524201 
L 210.475185 187.524201 
L 210.475185 71.521813 
L 208.642387 71.521813 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_76">
    <path d="M 210.475185 187.524201 
L 212.307983 187.524201 
L 212.307983 76.565395 
L 210.475185 76.565395 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_77">
    <path d="M 212.307983 187.524201 
L 214.140781 187.524201 
L 214.140781 106.826888 
L 212.307983 106.826888 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_78">
    <path d="M 214.140781 187.524201 
L 215.973579 187.524201 
L 215.973579 101.783306 
L 214.140781 101.783306 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_79">
    <path d="M 215.973579 187.524201 
L 217.806377 187.524201 
L 217.806377 109.348679 
L 215.973579 109.348679 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_80">
    <path d="M 217.806377 187.524201 
L 219.639175 187.524201 
L 219.639175 116.914052 
L 217.806377 116.914052 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_81">
    <path d="M 219.639175 187.524201 
L 221.471973 187.524201 
L 221.471973 134.566589 
L 219.639175 134.566589 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_82">
    <path d="M 221.471973 187.524201 
L 223.304771 187.524201 
L 223.304771 134.566589 
L 221.471973 134.566589 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_83">
    <path d="M 223.304771 187.524201 
L 225.137569 187.524201 
L 225.137569 149.697336 
L 223.304771 149.697336 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_84">
    <path d="M 225.137569 187.524201 
L 226.970367 187.524201 
L 226.970367 159.7845 
L 225.137569 159.7845 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_85">
    <path d="M 226.970367 187.524201 
L 228.803165 187.524201 
L 228.803165 174.915246 
L 226.970367 174.915246 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_86">
    <path d="M 228.803165 187.524201 
L 230.635963 187.524201 
L 230.635963 169.871664 
L 228.803165 169.871664 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_87">
    <path d="M 230.635963 187.524201 
L 232.468761 187.524201 
L 232.468761 174.915246 
L 230.635963 174.915246 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_88">
    <path d="M 232.468761 187.524201 
L 234.301559 187.524201 
L 234.301559 182.480619 
L 232.468761 182.480619 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_89">
    <path d="M 234.301559 187.524201 
L 236.134357 187.524201 
L 236.134357 185.00241 
L 234.301559 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_90">
    <path d="M 236.134357 187.524201 
L 237.967155 187.524201 
L 237.967155 185.00241 
L 236.134357 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_91">
    <path d="M 237.967155 187.524201 
L 239.799953 187.524201 
L 239.799953 185.00241 
L 237.967155 185.00241 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
   </g>
   <g id="patch_92">
    <path d="M 239.799953 187.524201 
L 241.632751 187.524201 
L 241.632751 182.480619 
L 239.799953 182.480619 
z
" clip-path="url(#p745cbc8068)" style="fill: #ff7f0e; opacity: 0.65"/>
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
       <use xlink:href="#m15aed4d867" x="72.595478" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_1">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="72.595478" y="202.121858" transform="rotate(-0 72.595478 202.121858)">6</text>
     </g>
    </g>
    <g id="xtick_2">
     <g id="line2d_2">
      <g>
       <use xlink:href="#m15aed4d867" x="157.443963" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_2">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="157.443963" y="202.121858" transform="rotate(-0 157.443963 202.121858)">8</text>
     </g>
    </g>
    <g id="xtick_3">
     <g id="line2d_3">
      <g>
       <use xlink:href="#m15aed4d867" x="242.292448" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_3">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="242.292448" y="202.121858" transform="rotate(-0 242.292448 202.121858)">10</text>
     </g>
    </g>
    <g id="xtick_4">
     <g id="line2d_4">
      <g>
       <use xlink:href="#m15aed4d867" x="327.140933" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_4">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="327.140933" y="202.121858" transform="rotate(-0 327.140933 202.121858)">12</text>
     </g>
    </g>
    <g id="xtick_5">
     <g id="line2d_5">
      <g>
       <use xlink:href="#m15aed4d867" x="411.989418" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_5">
      <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="411.989418" y="202.121858" transform="rotate(-0 411.989418 202.121858)">14</text>
     </g>
    </g>
    <g id="text_6">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="236.225781" y="216.122639" transform="rotate(-0 236.225781 216.122639)">Sample mean (minutes)</text>
    </g>
   </g>
   <g id="matplotlib.axis_2">
    <g id="ytick_1">
     <g id="line2d_6">
      <defs>
       <path id="m5c8d5162d3" d="M 0 0 
L -3.5 0 
" style="stroke: currentColor; stroke-width: 0.8"/>
      </defs>
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="187.524201" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_7">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="191.323029" transform="rotate(-0 33.925781 191.323029)">0</text>
     </g>
    </g>
    <g id="ytick_2">
     <g id="line2d_7">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="162.306291" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_8">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="166.105119" transform="rotate(-0 33.925781 166.105119)">10</text>
     </g>
    </g>
    <g id="ytick_3">
     <g id="line2d_8">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="137.08838" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_9">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="140.887208" transform="rotate(-0 33.925781 140.887208)">20</text>
     </g>
    </g>
    <g id="ytick_4">
     <g id="line2d_9">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="111.87047" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_10">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="115.669298" transform="rotate(-0 33.925781 115.669298)">30</text>
     </g>
    </g>
    <g id="ytick_5">
     <g id="line2d_10">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="86.652559" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_11">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="90.451388" transform="rotate(-0 33.925781 90.451388)">40</text>
     </g>
    </g>
    <g id="ytick_6">
     <g id="line2d_11">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="61.434649" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_12">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="65.233477" transform="rotate(-0 33.925781 65.233477)">50</text>
     </g>
    </g>
    <g id="ytick_7">
     <g id="line2d_12">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="36.216739" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_13">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="40.015567" transform="rotate(-0 33.925781 40.015567)">60</text>
     </g>
    </g>
    <g id="ytick_8">
     <g id="line2d_13">
      <g>
       <use xlink:href="#m5c8d5162d3" x="40.925781" y="10.998828" style="fill: currentColor; stroke: currentColor; stroke-width: 0.8"/>
      </g>
     </g>
     <g id="text_14">
      <text style="font-size: 10px; font-family:inherit; text-anchor: end; fill: currentColor" x="33.925781" y="14.797656" transform="rotate(-0 33.925781 14.797656)">70</text>
     </g>
    </g>
    <g id="text_15">
     <text style="font-size: 10px; font-family:inherit; text-anchor: middle; fill: currentColor" x="14.798438" y="98.820201" transform="rotate(-90 14.798438 98.820201)">Number of samples</text>
    </g>
   </g>
   <g id="line2d_14">
    <path d="M 201.669853 187.524201 
L 201.669853 10.116201 
" clip-path="url(#p745cbc8068)" style="fill: none; stroke-dasharray: 5.55,2.4; stroke-dashoffset: 0; stroke: currentColor; stroke-width: 1.5"/>
   </g>
   <g id="patch_93">
    <path d="M 40.925781 187.524201 
L 40.925781 10.116201 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_94">
    <path d="M 431.525781 187.524201 
L 431.525781 10.116201 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_95">
    <path d="M 40.925781 187.524201 
L 431.525781 187.524201 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="patch_96">
    <path d="M 40.925781 10.116201 
L 431.525781 10.116201 
" style="fill: none; stroke: currentColor; stroke-width: 0.8; stroke-linejoin: miter; stroke-linecap: square"/>
   </g>
   <g id="legend_1">
    <g id="patch_97">
     <path d="M 354.364844 26.714639 
L 374.364844 26.714639 
L 374.364844 19.714639 
L 354.364844 19.714639 
z
" style="fill: #1f77b4; opacity: 0.65"/>
    </g>
    <g id="text_16">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="382.364844" y="26.714639" transform="rotate(-0 382.364844 26.714639)">n = 25</text>
    </g>
    <g id="patch_98">
     <path d="M 354.364844 41.71542 
L 374.364844 41.71542 
L 374.364844 34.71542 
L 354.364844 34.71542 
z
" style="fill: #ff7f0e; opacity: 0.65"/>
    </g>
    <g id="text_17">
     <text style="font-size: 10px; font-family:inherit; text-anchor: start; fill: currentColor" x="382.364844" y="41.71542" transform="rotate(-0 382.364844 41.71542)">n = 400</text>
    </g>
   </g>
  </g>
 </g>
 <defs>
  <clipPath id="p745cbc8068">
   <rect x="40.925781" y="10.116201" width="390.6" height="177.408"/>
  </clipPath>
 </defs>
</svg>
<figcaption>The means of a thousand samples. The dashed line is the population's true mean. The 400-person samples (orange) gather much closer to the truth.</figcaption>
</figure>

## A biased sample: making it bigger does not help

Sampling error shrinks as the sample grows. But another kind of error does
not. Say you show a survey only to users **after their fifth visit**. The
sample is not random: frequent visitors get picked, and in this app frequent
visitors stay longer.

```python
import numpy as np
from ab_data import make_population

users = make_population()
heavy = users[users["visits"] >= 5]
print(len(heavy))
for n in [100, 1000, 10000]:
    biased, fair = [], []
    for seed in range(200):
        biased.append(heavy["minutes"].sample(n=n, random_state=seed).mean())
        fair.append(users["minutes"].sample(n=n, random_state=seed).mean())
    print(n, round(np.mean(biased), 2), round(np.mean(fair), 2))
```

```text
18470
100 10.91 9.08
1000 10.94 9.06
10000 10.94 9.04
```

- We repeated each sample size 200 times. The right column (random samples)
  sits around the truth (9.04).
- The middle column (frequent visitors only) is around 10.9 with 100
  people and with 10,000 people alike: about 2 minutes above the truth.
- An error that pushes in the same direction every time is called **bias**.
  Asking more people does not fix it; it only makes you surer of the wrong
  answer. The cure is to fix **the selection itself**: give everyone an equal
  chance.

<figure class="fig">
<div class="versus">
<div class="ok"><h4>Sampling error</h4>
<p>Comes from chance; its direction changes each time.</p>
<p>Shrinks as the sample grows.</p>
<p>Its size can be calculated.</p></div>
<div class="no"><h4>Bias</h4>
<p>Comes from how you select; always pushes the same way.</p>
<p>Stays even when the sample grows.</p>
<p>Cannot be seen in the data; look at the selection.</p></div>
</div>
<figcaption>Two kinds of error. Statistics measures the first; only good
design prevents the second.</figcaption>
</figure>

## Summary

- The **population** is the whole group your question is about, the
  **sample** is the part you measure. A population number is a
  **parameter** ($\mu$, $p$), a sample number is a **statistic** ($\bar{x}$,
  $\hat{p}$).
- Random samples give different results (**sampling error**); the wobble
  shrinks as the sample grows.
- If the selection favours a group, the result always slides the same way
  (**bias**); a bigger sample does not fix it.
- Looking at one sample you cannot tell whether it was lucky; with
  simulation you can draw thousands of samples and see the behaviour.
