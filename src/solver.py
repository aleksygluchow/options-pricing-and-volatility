import numpy as np
from scipy.optimize import brentq
from src.black_scholes import bs_price

def implied_volatility(market_price, S, K, T, r, option_type='call'):
    objective_func = lambda sigma: bs_price(S, K, T, r, sigma, option_type) - market_price
    try:
        return brentq(objective_func, 1e-3, 3.0)
    except (ValueError, RuntimeError):
        return np.nan