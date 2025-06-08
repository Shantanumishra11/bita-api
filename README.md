## BITA Backtesting API

The POST API allows users to accept custom or quarterly dates, applies a filter (top-N or value-based) on financial data, and assigns portfolio weights (equal or optimized) to selected securities. It returns the calculated weights per date along with the total execution time.


## Project Structure

bita-api/
main.py               # FastAPI application logic
models.py             # Request/response models using Pydantic
utils.py              # Core logic: calendar, filters, weighting
generate_data.py      # Script to create test Parquet files
requirements.txt      # Python dependencies
data/                 # Folder to store Parquet datasets
README.md             # Description of the project
Test.txt              # Some unit testcases along with its response


## Setup Instructions (MacOS)

1. Create and Activate Virtual Environment

python3 -m venv bita-env
source bita-env/bin/activate

2. Create the Project Folder

mkdir bita-api && cd bita-api

3. Install Dependencies

Create "requirements.txt":

fastapi
uvicorn
pandas
numpy
pydantic
pyarrow

Install them using below command:

pip install -r requirements.txt

## Command to Generate Dummy Test Data

python generate_data.py

This will create four '.parquet' files under 'data/' folder

## Run the FastAPI Server

uvicorn main:app --reload

Swagger docs available at:
http://127.0.0.1:8000/docs


## API Endpoint and Request-Response body

POST /backtest

http://127.0.0.1:8000/backtest

## Request Body Schema
{
  "calendar_rule": "quarterly",
  "quarterly_calendar": {"initial_date": "2024-01-01"},
  "custom_calendar": null,
  "filter_rule": "top_n",
  "top_n_filter": {"N": 5, "D": "market_capitalization"},
  "value_filter": null,
  "weighting": {"method": "equal"},
  "data_path": "data"
}

## Response
{
  "execution_time_seconds": 0.43,
  "weights": {
    "2024-03-31": {"12": 0.2, "45": 0.2, "78": 0.2, "83": 0.2, "99": 0.2},
    "2024-06-30": {"23": 0.2, "31": 0.2, "59": 0.2, "67": 0.2, "88": 0.2}
  }
}


## Supported Logic

1. Calendar Rules
custom: Use user-specified dates.
quarterly: Generate quarter-end dates from start date to 2025-01-22.

2. Filter Rules
top_n: Select top N securities by value in a given data field.
value: Include securities with field value > P.

3. Weighting Methods
equal: Assign equal weight to each security.
optimized: Assign weights between 'lb' and 'ub' to maximize the field value.


