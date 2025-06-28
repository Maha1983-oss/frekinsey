
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pandas as pd
from typing import List
import uvicorn
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Survey Dashboard</title>
        </head>
        <body>
            <h2>Upload your Excel file</h2>
            <form action="/upload" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
            </form>
        </body>
    </html>
    """

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    all_sheets = {}
    for file in files:
        df_dict = pd.read_excel(file.file, sheet_name=None)
        all_sheets[file.filename] = df_dict
    summary = {fname: list(sheets.keys()) for fname, sheets in all_sheets.items()}
    return {"Uploaded Files and Sheets": summary}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
