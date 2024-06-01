import hashlib
from queue import Queue
import threading
from fastapi import UploadFile
import whisper
from whisper.utils import get_writer

transcribe_queue = Queue()

class TranscribeJob:
    def __init__(self, file: UploadFile):
        self.checksum = get_checksum(file)
        self.file = file

# blocking  (bad)
def get_checksum(file: UploadFile) -> str:
    return hashlib.md5(file.file.read()).hexdigest()

async def add_job(file: UploadFile) -> str:
    job = TranscribeJob(file)
    transcribe_queue.put(job)
    return job.checksum

def work_loop():
    # block until theres job
    model = whisper.load_model("tiny")
    print("Worker running")
    while True:
        job = transcribe_queue.get(True, None)
        print("Working on job", job)

        result = model.transcribe(job.file.file)

        print("Finished working on job")
        writer = get_writer("srt", output_dir="./results")
        writer(result, "{}.srt".format(job.checksum))
    
t1 = threading.Thread(None, work_loop)
t1.start()