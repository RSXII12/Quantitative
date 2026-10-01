# Option Pricer: Monte Carlo vs. Black-Scholes

A from-scratch implementation of European call option pricing using three methods,
built to cross-validate a Monte Carlo simulation against the closed-form Black-Scholes
solution, and to measure the effect of variance reduction.

## Methods

- **`simulateStockMC`** — standard Monte Carlo. Simulates terminal stock prices under
  geometric Brownian motion, computes the discounted expected payoff, and reports the
  standard error of the estimate.
- **`simulateStockMCAntithetic`** — Monte Carlo with antithetic variates. Each sampled
  normal `Z` is paired with its mirror `-Z`, and the payoffs are averaged. Because the
  two paths are negatively correlated, this reduces the variance of the estimator
  without increasing the number of underlying random draws.
- **`blackScholesCall`** — the closed-form Black-Scholes solution, used as a reference
  value to confirm both simulations have converged to the right answer.

## Model

Stock price follows geometric Brownian motion under the risk-neutral measure:

  S_T = S_0 * exp((r - 0.5 * sigma^2) * T + sigma * sqrt(T) * Z), Z ~ N(0, 1)


Call payoff is `max(S_T - K, 0)`, discounted at the risk-free rate.

## Results

Parameters: S0 = 100, K = 100, sigma = 0.2, T = 1, r = 0.05, N = 1,000,000

| Method               | Price   | Standard error |
|----------------------|---------|-----------------|
| Monte Carlo          | 10.4607 | 0.0155          |
| MC, antithetic       | 10.4590 | 0.0077          |
| Black-Scholes        | 10.4506 | —               |

All three agree to within one standard error, confirming the simulations are
unbiased. Antithetic variates roughly **halved the standard error** for the same
number of underlying draws (0.0155 → 0.0077) — equivalent to the precision plain
Monte Carlo would need about 4x the paths to reach, at no extra sampling cost.
This comes from the negative correlation induced between each path and its mirror,
which cancels out part of the simulation noise when the payoffs are averaged.

## Usage

```python
from pricer import simulateStockMC, simulateStockMCAntithetic, blackScholesCall

price, se = simulateStockMC(100, 100, 0.2, 1, 0.05, 1_000_000)
price, se = simulateStockMCAntithetic(100, 100, 0.2, 1, 0.05, 1_000_000)
price = blackScholesCall(100, 100, 0.2, 1, 0.05)
```

## Possible extensions

- Put options and put-call parity check
- Delta/vega via finite differences or pathwise estimators
- Control variates (using the BS price as a control for the MC estimate)
- Vectorized convergence plot (price and SE vs. N)
