import yfinance as yf
import datetime

# --- Re-entry signal thresholds ---
REENTRY_VIX_THRESHOLD = 18
REENTRY_SP500_MA_RECOVERY = True  # S&P 500 crosses back above 200-day MA
YIELD_CURVE_NORMALIZATION = True  # 10Y > 3M

# --- Helper Functions ---
def get_price(ticker, period='6mo'):
    return yf.download(ticker, period=period)['Close']

def get_vix():
    return get_price('^VIX').iloc[-1].item()

def get_sp500_vs_ma():
    data = get_price('^GSPC', period='1y')
    current = data.iloc[-1].item()
    ma_200 = data.rolling(window=200).mean().dropna().iloc[-1].item()
    return current, ma_200

def get_yield_curve():
    t10 = get_price('^TNX').iloc[-1].item() / 100  # 10-Year Treasury
    t3m = get_price('^IRX').iloc[-1].item() / 100  # 3-Month Treasury
    return t10, t3m

# --- Signal Evaluation ---
def evaluate_reentry_conditions():
    signals = []

    vix = get_vix()
    if vix < REENTRY_VIX_THRESHOLD:
        signals.append("✅ VIX below 18 — volatility normalized")
    else:
        signals.append("❌ VIX still elevated")

    sp_price, sp_ma = get_sp500_vs_ma()
    if sp_price > sp_ma:
        signals.append("✅ S&P 500 above 200-day MA — trend recovery")
    else:
        signals.append("❌ S&P 500 still below 200-day MA")

    t10, t3m = get_yield_curve()
    if t10 > t3m:
        signals.append("✅ Yield curve normalized (10Y > 3M)")
    else:
        signals.append("❌ Yield curve still inverted")

    return signals

# --- Main Execution ---
if __name__ == "__main__":
    print(f"\n[Re-Entry Signal Monitor] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    results = evaluate_reentry_conditions()
    for line in results:
        print(line)

    conditions_met = [line for line in results if line.startswith("✅")]
    print("\nSummary:")
    if len(conditions_met) == 3:
        print("🔁 All conditions met — Ready for full portfolio re-entry")
    elif len(conditions_met) == 2:
        print("🟡 Consider phased re-entry — monitor for full signal")
    elif len(conditions_met) == 1:
        print("⚠️ Early improvement — not yet time to re-enter")
    else:
        print("🔒 No signals suggest safe re-entry at this time")
