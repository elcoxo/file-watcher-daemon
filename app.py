import os
from typing import Union

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import uvicorn

from watcher import directory_import

app = FastAPI()

@app.get("/")
def file_watcher_status():
    contents = {}
    
    directory_list = directory_import()
    print(directory_list)
    for directory in directory_list:
        print(directory)
        contents.update({directory: os.listdir(directory)})
        
    return JSONResponse(content=contents)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8127)