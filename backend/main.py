
from fastapi import FastAPI, UploadFile, File
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    df = pd.read_excel(file.file, engine="openpyxl")
    return {"columns": df.columns.tolist(), "rows": len(df)}
