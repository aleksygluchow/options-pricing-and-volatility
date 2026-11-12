# Options Pricing & Volatility

A compact quantitative finance project for analyzing option prices, implied volatility, volatility skew and option Greeks using real market data.

The project combines the **Black–Scholes model**, numerical implied-volatility solving and live option-chain data from Yahoo Finance to create a practical, data-driven view of the options market.

---

## Overview

This project answers several important questions:

- How are options priced under the Black–Scholes model?
- What is the implied volatility embedded in market prices?
- How does implied volatility change across strike prices?
- Does a polynomial volatility-skew model outperform a constant-volatility assumption?
- How do option Greeks behave across different levels of moneyness?

The analysis focuses on SPY options by default, but the ticker can be changed easily.

---

## Features

- Black–Scholes pricing for European call and put options
- Implied volatility calculation using the Brent root-finding algorithm
- Calculation of key option Greeks:
  - Delta
  - Gamma
  - Vega
- Automatic retrieval of live option-chain data using `yfinance`
- Filtering of liquid out-of-the-money puts and calls
- Moneyness calculation:

```text
Moneyness = Strike / Spot Price
```

- Volatility-skew analysis
- Quadratic polynomial regression for implied volatility
- Comparison between:
  - Constant implied volatility
  - Polynomial volatility-skew model
- Visualization of implied volatility and option Greeks

---

## Mathematical Foundation

### Black–Scholes Call Price

```text
C = S · N(d₁) − K · e⁻ʳᵀ · N(d₂)
```

### Black–Scholes Put Price

```text
P = K · e⁻ʳᵀ · N(−d₂) − S · N(−d₁)
```

where:

```text
d₁ = [ln(S / K) + (r + ½σ²)T] / (σ√T)

d₂ = d₁ − σ√T
```

Parameters:

| Symbol | Description |
|---|---|
| `S` | Current price of the underlying asset |
| `K` | Option strike price |
| `T` | Time to expiration in years |
| `r` | Risk-free interest rate |
| `σ` | Volatility |
| `N(·)` | Cumulative standard normal distribution |

Implied volatility is obtained numerically by finding the volatility that makes the theoretical Black–Scholes price equal to the observed market price.

---

## Project Structure

```text
options-pricing-and-volatility/
│
├── notebooks/
│   └── main_analysis.ipynb
│
├── src/
│   ├── black_scholes.py
│   ├── data_loader.py
│   ├── solver.py
│   └── __init__.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Data Pipeline

The project automatically:

1. Downloads the latest underlying price.
2. Selects a future option expiration date.
3. Retrieves the corresponding call and put chains.
4. Calculates bid–ask midpoint prices.
5. Removes options with invalid or illiquid quotes.
6. Selects out-of-the-money puts and calls.
7. Calculates moneyness.
8. Solves for implied volatility.
9. Calculates Delta, Gamma and Vega.
10. Prepares the dataset for statistical analysis and visualization.

The default filters focus on:

- OTM puts with strikes between `85%` and `100%` of the spot price
- OTM calls with strikes between `100%` and `115%` of the spot price
- Positive bid, ask and trading volume

---

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/<your-username>/options-pricing-and-volatility.git
cd options-pricing-and-volatility

python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```text
notebooks/main_analysis.ipynb
```

The notebook downloads current SPY option data and generates:

- Market implied-volatility observations
- A fitted quadratic volatility-skew curve
- A constant-volatility benchmark
- Model error comparison using mean squared error
- Delta profiles for OTM puts and calls

---

## Python API

### Calculate an option price

```python
from src.black_scholes import bs_price

price = bs_price(
    S=450,
    K=460,
    T=30 / 365,
    r=0.04,
    sigma=0.20,
    option_type="call"
)

print(price)
```

### Calculate implied volatility

```python
from src.solver import implied_volatility

iv = implied_volatility(
    market_price=8.50,
    S=450,
    K=460,
    T=30 / 365,
    r=0.04,
    option_type="call"
)

print(iv)
```

### Calculate option Greeks

```python
from src.black_scholes import bs_greeks

delta, gamma, vega = bs_greeks(
    S=450,
    K=460,
    T=30 / 365,
    r=0.04,
    sigma=0.20,
    option_type="call"
)

print(delta, gamma, vega)
```

### Fetch and prepare market data

```python
from src.data_loader import fetch_and_prepare_options

options, spot_price, expiry = fetch_and_prepare_options("SPY")

print(options.head())
print(f"Spot price: {spot_price}")
print(f"Expiration: {expiry}")
```

---

## Analysis Output

The notebook compares the observed implied-volatility curve with a second-degree polynomial regression:

```text
IV = β₀ + β₁ · Moneyness + β₂ · Moneyness²
```

It also compares the regression model against a simple constant-volatility benchmark using mean squared error:

```text
MSE = 1/n · Σ(yᵢ − ŷᵢ)²
```

This allows the market volatility structure to be evaluated against the simplifying assumption that volatility is constant across strikes.

---

## Important Assumptions

This project is intended for educational and analytical purposes. The implementation uses several simplifying assumptions:

- Black–Scholes assumes European-style exercise.
- Volatility is assumed constant within the pricing model.
- The risk-free rate is provided manually.
- Market prices are approximated using bid–ask midpoints.
- Yahoo Finance data may contain missing, delayed or imperfect quotes.
- Implied volatility is solved within the interval `0.1%–300%`.
- The selected expiration is based on the available option-chain list.

The results should not be interpreted as investment advice or as a production-grade trading system.

---

## Technologies

- Python
- NumPy
- Pandas
- SciPy
- Matplotlib
- scikit-learn
- yfinance
- Jupyter Notebook

---

## Possible Extensions

Potential directions for further development include:

- Adding real-time risk-free rates
- Supporting multiple expirations
- Building a full volatility surface
- Adding put–call parity checks
- Calculating Theta and Rho
- Implementing American option pricing
- Comparing Black–Scholes volatility with historical volatility
- Adding interactive Plotly visualizations
- Testing alternative regression and interpolation methods
- Creating a dashboard for live volatility monitoring

---

## Disclaimer

This repository is an educational quantitative-finance project. It is not financial advice, an investment recommendation or a guarantee of market behavior.
