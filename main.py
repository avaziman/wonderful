from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from transcriber import  add_job

app = FastAPI()

@app.post("/transcribe")
async def root(file: UploadFile):
    checksum = await add_job(file)
    return {"checksum": checksum}

# client will poll his results from here, 404 if not finished
app.mount("/result", StaticFiles(directory="results"), name="static")