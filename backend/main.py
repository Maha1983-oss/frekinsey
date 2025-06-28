
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import BytesIO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def detect_column_type(column):
    unique_values = column.dropna().unique()
    if len(unique_values) > 0 and all(isinstance(val, str) and ';' in val for val in unique_values):
        return "MA"
    else:
        return "SA"

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    contents = await file.read()
    excel_data = pd.read_excel(BytesIO(contents), sheet_name=None)
    first_sheet = list(excel_data.keys())[0]
    df = excel_data[first_sheet]
    df = df.dropna(how="all")
    headers = df.columns.tolist()
    column_types = {col: detect_column_type(df[col]) for col in headers}
    return {
        "headers": headers,
        "column_types": column_types,
        "rows": df.shape[0]
    }
