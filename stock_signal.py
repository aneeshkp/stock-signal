import openai
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load OpenAI client
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

def get_technical_analysis(symbol):
    prompt = (
        f"Based on current technical analysis only, is the stock {symbol} a bullish or bearish trade? "
        "Summarize using RSI, MACD, moving averages (50/200-day), and general trend. Keep it under 50 words."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial analyst who gives concise technical summaries."},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content.strip()
    bias = "Bullish" if "bullish" in reply.lower() else "Bearish" if "bearish" in reply.lower() else "Neutral"
    return reply, bias


def fetch_stock_data(symbol, period='1mo', interval='1d'):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period, interval=interval)
    return hist

def plot_stock(symbol, hist):
    plt.figure(figsize=(8, 4))
    plt.plot(hist.index, hist['Close'], marker='o')
    plt.title(f'{symbol} - Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def analyze_stocks(symbols):
    results = []

    for symbol in symbols:
        print(f"\n🔍 Analyzing {symbol}...")

        hist = fetch_stock_data(symbol)
        current_price = hist['Close'].iloc[-1]
        summary, bias = get_technical_analysis(symbol)

        results.append({
            "Symbol": symbol,
            "Current Price (USD)": round(current_price, 2),
            "Bias": bias,
            "Summary": summary
        })
        if show_charts:
            plot_stock(symbol, hist)

    df = pd.DataFrame(results)
    return df

# 🔧 Customize your stock list here
symbols = ["AAPL", "GOOG", "MSFT", "TSLA","SMCI","QQQ","NVDA"]

# Ask the user whether to show charts
show_charts = input("Do you want to display charts? (y/n): ").strip().lower() == "y"
# Run analysis
df = analyze_stocks(symbols)

# Show table
print("\n📊 Technical Analysis Summary:\n")
print(df.to_markdown(index=False))

