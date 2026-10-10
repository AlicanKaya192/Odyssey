## optimize

| Code | Question |
|---|---|
| `minimize_scalar(f, bounds=(a, b), method="bounded")` | the minimum of one variable |
| `minimize(f, x0=[...])` | the minimum of several variables |
| `minimize(..., method="Nelder-Mead")` | a derivative-free method |
| `minimize(..., bounds=[(0, 1)] * n)` | a limit for each variable |
| `minimize(..., constraints=[{"type": "eq", "fun": g}])` | the constraint `g(x) = 0` |
| `curve_fit(model, x, y, p0=[...])` | model parameters + `cov` |
| `root_scalar(f, bracket=[a, b])` | `f(x) = 0` (opposite signs at the ends) |
| `linprog(c, A_ub=, b_ub=, bounds=)` | minimising under linear constraints |

## The result object

| Field | What |
|---|---|
| `res.x` | the solution |
| `res.fun` | the value at the solution |
| `res.success` / `res.status` | did it succeed |
| `res.message` | an explanation |
| `res.nit`, `res.nfev` | number of steps and function calls |

## interpolate

| Code | Property |
|---|---|
| `np.interp(x, xs, ys)` | linear; repeats the end value outside the range |
| `CubicSpline(xs, ys)` | smooth; may overshoot, extends the curve outside |
| `PchipInterpolator(xs, ys)` | smooth and does not overshoot |
| `make_interp_spline(xs, ys, k=3)` | a general spline |

## Traps

| Symptom | Cause |
|---|---|
| Found the minimum instead of the "maximum" | scipy minimises; give the negative |
| Different start, different answer | a local minimum; try many starts |
| Everything came out zero | a constraint was forgotten |
| `f(a) and f(b) must have different signs` | no root inside the `bracket` |
| `curve_fit` gave nonsense | a bad `p0` |
| A peak / dip never measured | the spline overshot; `Pchip` |
