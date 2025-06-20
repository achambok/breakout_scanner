import yfinance as yf
import datetime
import asyncio
from desktop_notifier import DesktopNotifier
from typing import Optional

BREAKOUT_DAYS = 3
EXTREME_THRESHOLD = 0.10
notifier = DesktopNotifier()

async def _notify_async(title: str, message: str):
    await notifier.send(title=title, message=message)

def alert_desktop(title: str, message: str):
    asyncio.run(_notify_async(title, message))

EXCHANGE_MAP = {
    'nasdaq': 'NASDAQ', 'nyse': 'NYSE', 'nysemkt': 'AMEX',
    'asx': 'ASX', 'tsx': 'TSX', 'lse': 'LSE', 'hkse': 'HKEX',
    'hkex': 'HKEX', 'tse': 'JPX', 'nse': 'NSE', 'bse': 'BSE',
    'sse': 'SSE', 'szse': 'SZSE',
}

TRADINGVIEW_OVERRIDES = {
    "NG=F": "NYMEX:NG1!", "CL=F": "NYMEX:CL1!", "GC=F": "COMEX:GC1!",
    "SI=F": "COMEX:SI1!", "ES=F": "CME_MINI:ES1!", "NQ=F": "CME_MINI:NQ1!",
    "YM=F": "CBOT:YM1!", "BTC-USD": "BINANCE:BTCUSDT", "ETH-USD": "BINANCE:ETHUSDT"
}

def get_tradingview_symbol(yf_symbol: str) -> str:
    if yf_symbol in TRADINGVIEW_OVERRIDES:
        return TRADINGVIEW_OVERRIDES[yf_symbol]
    try:
        info = yf.Ticker(yf_symbol).info
        ex = info.get("exchange", "").lower()
        prefix = EXCHANGE_MAP.get(ex, "NASDAQ")
    except:
        prefix = "NASDAQ"
    sym = yf_symbol.replace("-", ".").replace("=F", "")
    for suffix in [".TO", ".AX", ".L", ".HK"]:
        sym = sym.replace(suffix, "")
    return f"{prefix}:{sym}"

def is_inside_day(df, idx: int) -> bool:
    return (df['High'].iloc[idx] <= df['High'].iloc[idx - 1] and
            df['Low'].iloc[idx] >= df['Low'].iloc[idx - 1])

def date_filter_ok() -> bool:
    d = datetime.datetime.now()
    wd, day = d.weekday(), d.day
    return (wd in [1, 3] or wd == 0 or wd == 4 or day <= 2 or day >= 28)

def check_symbol(symbol: str) -> Optional[dict]:
    try:
        df = yf.Ticker(symbol).history(period="1mo", interval="1d")
        if len(df) < 5:
            return None

        closes = df['Close']
        highs = df['High']
        lows = df['Low']
        opens = df['Open']
        idx = len(df) - 1
        prev = idx - 1

        up_breaks = sum(closes.iloc[-i] > highs.iloc[-i - 1] for i in range(1, BREAKOUT_DAYS + 1))
        dn_breaks = sum(closes.iloc[-i] < lows.iloc[-i - 1] for i in range(1, BREAKOUT_DAYS + 1))
        is_up = up_breaks >= BREAKOUT_DAYS
        is_dn = dn_breaks >= BREAKOUT_DAYS
        if not (is_up or is_dn) or not date_filter_ok():
            return None

        last_close = closes.iloc[idx]
        wh, wl = highs.iloc[idx - 4:idx + 1].max(), lows.iloc[idx - 4:idx + 1].min()
        mh, ml = highs.iloc[idx - 20:idx + 1].max(), lows.iloc[idx - 20:idx + 1].min()
        near_extreme = any([
            last_close >= wh * (1 - EXTREME_THRESHOLD),
            last_close <= wl * (1 + EXTREME_THRESHOLD),
            last_close >= mh * (1 - EXTREME_THRESHOLD),
            last_close <= ml * (1 + EXTREME_THRESHOLD),
        ])
        if not near_extreme:
            return None

        frd = is_up and opens.iloc[idx] > closes.iloc[prev] and closes.iloc[idx] < opens.iloc[idx]
        fgd = is_dn and opens.iloc[idx] < closes.iloc[prev] and closes.iloc[idx] > opens.iloc[idx]
        inside = is_inside_day(df, idx)

        up2 = closes.iloc[-1] > closes.iloc[-2] > closes.iloc[-3]
        dn2 = closes.iloc[-1] < closes.iloc[-2] < closes.iloc[-3]

        return {
            "Symbol": symbol,
            "Breakout Up": is_up,
            "Breakout Down": is_dn,
            "FRD": frd,
            "FGD": fgd,
            "Inside Day": inside,
            "2+ Up": up2,
            "2+ Down": dn2,
            "Close": round(last_close, 2),
            "Week High": round(wh, 2),
            "Week Low": round(wl, 2),
            "Month High": round(mh, 2),
            "Month Low": round(ml, 2),
            "TV_Symbol": get_tradingview_symbol(symbol)
        }

    except Exception as e:
        print(f"[ERROR] {symbol}: {e}")
        return None