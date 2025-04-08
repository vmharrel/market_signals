
import yfinance as yf
import pandas as pd
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv
from fredapi import Fred

# Load secrets
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
FRED_API_KEY = os.getenv("FRED_API_KEY")

fred = Fred(api_key=FRED_API_KEY)

def get_price(ticker, period='6mo'):
    return yf.download(ticker, period=period)['Close']

def get_vix():
    return get_price("^VIX", period="5d").iloc[-1].item()

def get_sp500_vs_ma():
    data = get_price("^GSPC", period='1y')
    current = data.iloc[-1].item()
    ma_200 = data.rolling(window=200).mean().dropna().iloc[-1].item()
    return current, ma_200

def get_yield_curve():
    t10 = get_price("^TNX", period="5d").iloc[-1].item() / 100
    t3m = get_price("^IRX", period="5d").iloc[-1].item() / 100
    return t10, t3m

def fetch_latest_fred(series_id, frequency='m'):
    data = fred.get_series(series_id)
    df = data.to_frame(name="value").reset_index()
    df.columns = ["Date", "Value"]
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    if frequency == 'q':
        df = df[df["Date"].dt.month.isin([3, 6, 9, 12])]
    return df.iloc[-1]["Value"]

def build_report():
    vix = get_vix()
    sp_price, sp_ma = get_sp500_vs_ma()
    t10, t3m = get_yield_curve()
    cpi = fetch_latest_fred("CPIAUCSL")
    oas = fetch_latest_fred("BAMLH0A0HYM2")
    gdp = fetch_latest_fred("GDP", frequency='q')
    lei = fetch_latest_fred("USSLIND")

    data = []
    data.append(("VIX > 20", vix > 20, "📘 2025 Market Dynamics Plan", "Rotate into real assets, floating-rate"))
    data.append(("VIX > 25", vix > 25, "📙 Tax-Sensitive Defensive Plan", "Rebalance IRAs immediately"))
    data.append(("VIX < 18", vix < 18, "📗 Re-entry Plan", "Volatility normalized – phased re-entry"))

    data.append(("S&P < 200-Day MA", sp_price < sp_ma, "📘 2025 Market Dynamics Plan", "Shift to value/dividend assets"))
    data.append(("S&P Correction >10%", sp_price < sp_ma * 0.9, "📙 Tax-Sensitive Defensive Plan", "Harvest losses, short ETFs"))
    data.append(("S&P > 200-Day MA", sp_price > sp_ma, "📗 Re-entry Plan", "Trend recovery confirmed"))

    data.append(("Yield Curve Inverted", t10 < t3m, "📘 2025 Market Dynamics Plan", "Add gold, reduce long bonds"))
    data.append(("Yield Curve Normalized", t10 > t3m, "📗 Re-entry Plan", "Bond market normalization"))

    data.append((f"CPI YoY > 4% ({cpi:.2f})", cpi > 4.0, "📘 2025 Market Dynamics Plan", "Add TIPS, commodities"))
    data.append((f"CPI YoY < 3.5% ({cpi:.2f})", cpi < 3.5, "📗 Re-entry Plan", "CPI stabilized"))

    data.append((f"HY OAS > 500bps ({oas:.0f})", oas > 500, "📘 2025 Market Dynamics Plan", "Exit high-yield, raise cash"))
    data.append((f"GDP < 0% ({gdp:.2f})", gdp < 0, "📙 Tax-Sensitive Defensive Plan", "Lock in cash reserves"))
    data.append((f"LEI < 101 ({lei:.2f})", lei < 101, "📙 Tax-Sensitive Defensive Plan", "Prepare liquidity buffer"))

    df = pd.DataFrame(data, columns=["Signal", "Triggered", "Plan", "Action"])
    df["Status"] = df["Triggered"].map(lambda x: "🟥 ALERT" if x else "✅ OK")
    return df

def send_email_report(df):
    lines = [f"{row['Status']} {row['Signal']} — {row['Plan']}
Action: {row['Action']}" for _, row in df.iterrows()]
    body = "\n\n".join(lines)

    msg = EmailMessage()
    msg["Subject"] = "📬 Weekly Market Signal Report – Harrell Family"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    report = build_report()
    send_email_report(report)
