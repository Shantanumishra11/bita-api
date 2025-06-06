from fastapi import FastAPI
from models import BacktestRequest
from utils import *
import pandas as pd
import time
import os

app = FastAPI()

@app.post("/backtest")
def run_backtest(request: BacktestRequest):
    start_time = time.time()

    if request.calendar_rule == "custom":
        revision_dates = [str(d) for d in request.custom_calendar.dates]
    else:
        revision_dates = generate_quarter_end_dates(
            pd.Timestamp(request.quarterly_calendar.initial_date),
            pd.Timestamp("2025-01-22")
        )

    results = {}

    for date in revision_dates:
        if request.filter_rule == "top_n":
            df = pd.read_parquet(f"{request.data_path}/{request.top_n_filter.D}.parquet")
            securities = apply_top_n_filter(df.loc[date], request.top_n_filter.N)
        else:
            df = pd.read_parquet(f"{request.data_path}/{request.value_filter.D}.parquet")
            securities = apply_value_filter(df.loc[date], request.value_filter.P)

        if request.weighting["method"] == "equal":
            weights = apply_equal_weighting(securities)
        else:
            wdf = pd.read_parquet(f"{request.data_path}/{request.weighting['D']}.parquet")
            weights = apply_optimized_weighting(securities, wdf.loc[date], request.weighting["lb"], request.weighting["ub"])

        results[date] = weights

    end_time = time.time()
    return {
        "execution_time_seconds": round(end_time - start_time, 4),
        "weights": results
    }

