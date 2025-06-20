import yfinance as yf
import json
import datetime

# === Load Watchlist ===
with open("watchlist.json", "r") as f:
    watchlist = json.load(f)["symbols"]

# === Config ===
BREAKOUT_DAYS = 3
EXTREME_THRESHOLD = 5  # 10%
today = datetime.datetime.now()
weekday = today.weekday()  # Monday = 0, Sunday = 6

is_tuesday_or_thursday = weekday in [1, 3]
is_week_start = weekday == 0
is_week_end = weekday == 4
is_month_start = today.day <= 2
is_month_end = today.day >= 28  # rough approx

date_filter_ok = any([is_tuesday_or_thursday, is_week_start, is_week_end, is_month_start, is_month_end])

def check_symbol(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1mo", interval="1d")
        if len(data) < 21:
            return None

        closes = data["Close"]
        highs = data["High"]
        lows = data["Low"]

                # Relaxed breakout logic: close > max high of previous 3 candles
        breakout_count = 0
        for i in range(-BREAKOUT_DAYS, 0):
            recent_high = highs.iloc[i - 3:i].max()
            if closes.iloc[i] > recent_high:
                breakout_count += 1
       

        if breakout_count < BREAKOUT_DAYS:
            return None

        # 2. Extreme check: near weekly or monthly high/low
        recent_close = closes[-1]
        week_high = highs[-5:].max()
        week_low = lows[-5:].min()
        month_high = highs[-21:].max()
        month_low = lows[-21:].min()

        near_extreme = any([
            recent_close >= week_high * (1 - EXTREME_THRESHOLD),
            recent_close <= week_low * (1 + EXTREME_THRESHOLD),
            recent_close >= month_high * (1 - EXTREME_THRESHOLD),
            recent_close <= month_low * (1 + EXTREME_THRESHOLD),
        ])

        if not near_extreme:
            return None

        # 3. Date Filter
        if not date_filter_ok:
            return None

        return {
            "symbol": symbol,
            "close": round(recent_close, 2),
            "breakout_days": breakout_count,
            "week_high": round(week_high, 2),
            "week_low": round(week_low, 2)
        }

    except Exception as e:
        print(f"Error processing {symbol}: {e}")
        return None


print("🔍 Scanning symbols...\n")
for sym in watchlist:
    result = check_symbol(sym)
    if result:
        print(f"✅ {result['symbol']} - Close: {result['close']} | Breakout Days: {result['breakout_days']}")
    else:
        print(f"❌ {sym} does not match criteria.")
