import yfinance as yf
import smtplib
from email.message import EmailMessage
import ssl
import datetime
import os
from dotenv import load_dotenv

# ----------- Load Environment Variables -----------
load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# Thresholds
VIX_ALERT_LEVEL = 20
SP500_MOVING_AVG_DAYS = 200

# ----------- Utility Functions -----------
def fetch_vix_level():
    vix = yf.download("^VIX", period="5d")['Close']
    return vix.iloc[-1].item()

def fetch_sp500_vs_moving_avg():
    sp500 = yf.download("^GSPC", period="1y")['Close']
    current_price = sp500.iloc[-1].item()
    moving_avg = sp500.rolling(window=SP500_MOVING_AVG_DAYS).mean().dropna().iloc[-1].item()
    return current_price, moving_avg

def fetch_yield_curve():
    t10 = yf.download("^TNX", period="5d")['Close'].iloc[-1].item() / 100  # 10Y
    t3m = yf.download("^IRX", period="5d")['Close'].iloc[-1].item() / 100  # 3M
    return t10, t3m

# ----------- Evaluation Logic -----------
def evaluate_conditions():
    alerts = []

    vix = fetch_vix_level()
    if vix > VIX_ALERT_LEVEL:
        alerts.append(f"VIX elevated: {vix:.2f}")

    sp_price, sp_ma = fetch_sp500_vs_moving_avg()
    if sp_price < sp_ma:
        alerts.append(f"S&P 500 dropped below 200-day MA: {sp_price:.2f} < {sp_ma:.2f}")

    t10, t3m = fetch_yield_curve()
    if t10 < t3m:
        alerts.append(f"Yield curve inversion: 10Y={t10:.2f}% < 3M={t3m:.2f}%")

    return alerts

# ----------- Email Notification -----------
def send_email(alerts):
    msg = EmailMessage()
    msg['Subject'] = '🚨 Market Alert: Defensive Portfolio Transition Signal'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL

    msg.set_content("\n".join(alerts))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# ----------- Main Entry Point -----------
if __name__ == "__main__":
    print(f"Running market signal monitor at {datetime.datetime.now()}...")
    signals = evaluate_conditions()
    if signals:
        print("Signals detected:", signals)
        send_email(signals)
    else:
        print("No alerts triggered.")
