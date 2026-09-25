A short version of everything in the lesson. Come back here when you get stuck on a question.

## Update rules

| Method | Rule |
|---|---|
| gradient descent | $\mathbf{w} \leftarrow \mathbf{w} - \eta \nabla L$ |
| momentum | $\mathbf{v} \leftarrow \beta\mathbf{v} + \nabla L$, $\mathbf{w} \leftarrow \mathbf{w} - \eta \mathbf{v}$ |
| RMSProp | $\mathbf{s} \leftarrow \beta\mathbf{s} + (1 - \beta)\mathbf{g}^2$, $\mathbf{w} \leftarrow \mathbf{w} - \eta \dfrac{\mathbf{g}}{\sqrt{\mathbf{s}} + \epsilon}$ |
| Adam | momentum ($\mathbf{m}$) + RMSProp ($\mathbf{s}$) |

## The learning rate (a parabola with curvature λ)

| Situation | Factor $1 - \eta\lambda$ | Behaviour |
|---|---|---|
| $0 < \eta < \frac{1}{\lambda}$ | between $0$ and $1$ | smooth descent |
| $\eta = \frac{1}{\lambda}$ | $0$ | the bottom in one step |
| $\frac{1}{\lambda} < \eta < \frac{2}{\lambda}$ | between $-1$ and $0$ | descent with swings |
| $\eta > \frac{2}{\lambda}$ | $< -1$ | divergence |

With several variables $\lambda \to \lambda_{\max}$; progress in the gentle direction goes by $1 - \eta\lambda_{\min}$.

## Using the data

| Method | Examples per step |
|---|---|
| full | all |
| SGD | $1$ |
| mini-batch | $B$ |

Epoch: one complete pass over the data. Number of steps per epoch $= \frac{n}{B}$.

## Symptoms

| Loss curve | Likely cause |
|---|---|
| drops very slowly | learning rate small; no scaling |
| jumps, `nan` | learning rate large |
| jitters at the bottom | mini-batch noise; reduce the rate |
| zigzag | large condition number; momentum or scaling |

## Practical settings

- Momentum $\beta = 0.9$; Adam $\beta_1 = 0.9$, $\beta_2 = 0.999$.
- Learning rate schedules and warm-up; gradient clipping.
