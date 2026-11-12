import yfinance as yf
import pandas as pd
import numpy as np
from src.solver import implied_volatility
from src.black_scholes import bs_greeks

def fetch_and_prepare_options(ticker_symbol="SPY", risk_free_rate=0.04):
    spy = yf.Ticker(ticker_symbol)
    S = spy.history(period="1d")['Close'].iloc[-1]
    
    target_expiry = spy.options[4]
    chain = spy.option_chain(target_expiry)
    
    # 1. Pobranie opcji Put i Call
    puts = chain.puts.copy()
    calls = chain.calls.copy()
    
    # Obliczenie czasu do wygaśnięcia
    today = pd.Timestamp.today().tz_localize(None)
    expiry_date = pd.to_datetime(target_expiry).tz_localize(None)
    T = (expiry_date - today).days / 365.25
    
    # 2. Czyszczenie i wybór opcji OTM Put (Strike < Spot)
    puts['mid_price'] = (puts['bid'] + puts['ask']) / 2
    valid_puts = puts[(puts['bid'] > 0) & (puts['ask'] > 0) & (puts['volume'] > 0)].copy()
    # Zostawiamy tylko opcje Put poniżej ceny rynkowej (Moneyness < 1.0)
    valid_puts = valid_puts[(valid_puts['strike'] >= S * 0.85) & (valid_puts['strike'] < S)]
    valid_puts['option_type'] = 'put'
    
    # 3. Czyszczenie i wybór opcji OTM Call (Strike >= Spot)
    calls['mid_price'] = (calls['bid'] + calls['ask']) / 2
    valid_calls = calls[(calls['bid'] > 0) & (calls['ask'] > 0) & (calls['volume'] > 0)].copy()
    # Zostawiamy tylko opcje Call powyżej ceny rynkowej (Moneyness >= 1.0)
    valid_calls = valid_calls[(valid_calls['strike'] >= S) & (valid_calls['strike'] <= S * 1.15)]
    valid_calls['option_type'] = 'call'
    
    # 4. Połączenie w jedną gładką krzywą i sortowanie
    df = pd.concat([valid_puts, valid_calls], ignore_index=True)
    df = df.sort_values('strike').reset_index(drop=True)
    
    # Obliczenie Moneyness
    df['Moneyness'] = df['strike'] / S
    
    # 5. Wyliczenie IV oraz Greków (uwzględniając dynamicznie typ opcji: Call lub Put)
    df['IV'] = df.apply(
        lambda row: implied_volatility(row['mid_price'], S, row['strike'], T, risk_free_rate, row['option_type']), 
        axis=1
    )
    df = df.dropna(subset=['IV']).copy()
    
    df[['Delta', 'Gamma', 'Vega']] = df.apply(
        lambda row: pd.Series(bs_greeks(S, row['strike'], T, risk_free_rate, row['IV'], row['option_type'])), 
        axis=1
    )
    
    return df, S, target_expiry