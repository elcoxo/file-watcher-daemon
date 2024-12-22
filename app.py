import os
from typing import Union

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def file_watcher_status():
    text = "Hello, World!"
    return {"text": text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('APP_PORT')))