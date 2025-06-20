import streamlit as st
import pandas as pd
import json
import threading, time, schedule
from utils import check_symbol, alert_desktop

# --- Streamlit Setup ---
st.set_page_config(page_title="Breakout Scanner", layout="wide")

# --- Custom Styles & Logo ---
st.markdown("""
<style>
div.block-container { padding-top: 0.5rem !important; }
h1, h2, .stButton > button, .stMetric {
  text-align: center; margin: auto;
}
.navbar { background-color: #0d6efd; padding: 0.4rem; }
.navbar-brand { color: white; font-weight: bold; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 3])
with col_logo:
    st.image("logo.jpg", width=90)
with col_title:
    st.markdown("<h2 style='color:#0d6efd;'>📈 Breakout & Signal Scanner</h2>", unsafe_allow_html=True)

# --- Load symbols ---
with open("watchlist.json") as f:
    symbols = json.load(f)["symbols"]

# --- Session state init ---
if "results" not in st.session_state:
    st.session_state.results = {}
if "badge" not in st.session_state:
    st.session_state.badge = "gray"

# --- Core scan logic ---
def run_scan():
    new = {}
    with st.spinner("⏳ Scanning symbols..."):
        raw = [check_symbol(s) for s in symbols]
        for r in raw:
            if not r:
                continue
            sym = r["Symbol"]
            prev = st.session_state.results.get(sym, {})
            if prev.get("Breakout Up") or prev.get("Breakout Down"):
                if r["Inside Day"]:
                    continue  # reset on inside day
                else:
                    new[sym] = r
            else:
                new[sym] = r
        st.session_state.results = new
        st.session_state.badge = "green" if new else "gray"
        if new:
            alert_desktop("Breakout Scanner", f"{len(new)} pairs matched")
            st.success(f"✅ {len(new)} breakout/signal pairs found.")
            st.balloons()
        else:
            st.info("No new breakout/signal pairs detected.")

# --- Scheduler for daily scan @16:01 ---
def scheduler_loop():
    schedule.every().day.at("16:01").do(run_scan)
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=scheduler_loop, daemon=True).start()

# --- UI Controls ---
st.markdown("### 🔍 Scan Controls")
col1, col2 = st.columns(2)
with col1:
    if st.button("🕵️ Run Scan Now"):
        run_scan()
with col2:
    st.markdown(
        f"<div style='text-align:center;'>🔄 Status: <span style='color:{'green' if st.session_state.badge=='green' else 'gray'}'>{st.session_state.badge.upper()}</span></div>",
        unsafe_allow_html=True
    )

# --- Display Results ---
results = st.session_state.results
if results:
    df = pd.DataFrame(results.values()).drop(columns=["TV_Symbol"], errors="ignore")

    df = df[[
        "Symbol", "Breakout Up", "Breakout Down", "FRD", "FGD", "Inside Day",
        "2+ Up", "2+ Down", "Close", "Week High", "Week Low", "Month High", "Month Low"
    ]]

    st.metric("📊 Symbols Scanned", len(symbols))
    st.metric("📈 Active Pairs", len(df))

    styled = df.style\
        .applymap(lambda v: "color:green" if v else "", subset=["Breakout Up", "FGD", "2+ Up"])\
        .applymap(lambda v: "color:red" if v else "", subset=["Breakout Down", "FRD", "2+ Down"])\
        .applymap(lambda v: "color:gray" if v else "", subset=["Inside Day"])

    st.dataframe(styled, use_container_width=True)
else:
    st.info("No active breakout pairs yet. Click 'Run Scan Now' to begin.")

# --- Footer ---
st.markdown("---")
st.caption("""
📘 **Legend**  
- 🟢 Breakout Up / FGD / 2+ Up = Bullish  
- 🔴 Breakout Down / FRD / 2+ Down = Bearish  
- ⚪ Inside Day = Neutral (resets trend tracking)  
- 🔁 Breakouts persist until next Inside Day  
- 🕐 Auto-scans daily at 16:01 + manual scan option available  
""")