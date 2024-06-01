import hashlib
from queue import Queue
import threading
from fastapi import UploadFile
import torch
import whisper
from whisper.utils import get_writer

transcribe_queue = Queue()

class TranscribeJob:
    def __init__(self, src: str, checksum: str):
        self.checksum = checksum 
        self.src = src

# can be split
async def get_checksum(file: UploadFile) -> str:
    abytes = await file.read()
    await file.seek(0)
    return hashlib.md5(abytes).hexdigest()

async def add_job(file: UploadFile) -> str:
    checksum = await get_checksum(file); 
    # save in fs
    
    src = './results/src/{}'.format(file.filename)
    with open(src, 'wb') as f:
        src_bytes = await file.read()
        f.write(src_bytes)

    job = TranscribeJob(src, checksum)
    transcribe_queue.put(job)


    return job.checksum

def work_loop():
    model = whisper.load_model("tiny")
    print("CUDA IS AVAIL", torch.cuda.is_available())
    print(torch.cuda.get_device_name(0))
    print("Worker running")

    while True:
        # block until theres job
        job = transcribe_queue.get(True, None)
        print("Working on job", job.src)

        result = model.transcribe(job.src)

        print("Finished working on job")
        writer = get_writer("srt", output_dir="./results")
        writer(result, "{}.srt".format(job.checksum))
    
t1 = threading.Thread(None, work_loop)
t1.start()