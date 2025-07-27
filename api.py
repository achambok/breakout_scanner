from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from utils import check_symbol
import json

app = FastAPI()

# Enable CORS for mobile app access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your app domain or IP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load watchlist from file
with open("watchlist.json") as f:
    symbols = json.load(f)["symbols"]

# Define the API response model
class ScanResult(BaseModel):
    Symbol: str
    Breakout_Up: bool
    Breakout_Down: bool
    FRD: bool
    FGD: bool
    Inside_Day: bool
    TwoPlus_Up: bool
    TwoPlus_Down: bool
    Close: float
    Week_High: float
    Week_Low: float
    Month_High: float
    Month_Low: float

@app.get("/api/breakouts", response_model=List[ScanResult])
async def breakouts():
    results = []
    for sym in symbols:
        r = check_symbol(sym)
        if r:
            results.append({
                "Symbol": r["Symbol"],
                "Breakout_Up": r["Breakout Up"],
                "Breakout_Down": r["Breakout Down"],
                "FRD": r["FRD"],
                "FGD": r["FGD"],
                "Inside_Day": r["Inside Day"],
                "TwoPlus_Up": r["2+ Up"],
                "TwoPlus_Down": r["2+ Down"],
                "Close": r["Close"],
                "Week_High": r["Week High"],
                "Week_Low": r["Week Low"],
                "Month_High": r["Month High"],
                "Month_Low": r["Month Low"]
            })
    return results
