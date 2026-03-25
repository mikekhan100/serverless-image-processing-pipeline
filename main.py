import os
import shutil
from fastapi import FastAPI, UploadFile, File
from tasks import process_image_task  # Import the Celery task

app = FastAPI()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/")
def home():
    return {"message": "Image Pipeline is Asynchronous!"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # 1. Save the file locally
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Hand off the work to Celery using .delay()
    # This returns IMMEDIATELY without waiting for Pillow
    task = process_image_task.delay(file_path)
    
    return {
        "status": "Task Received",
        "task_id": task.id,
        "message": "Your image is being processed in the background."
    }

@app.get("/status/{task_id}")
def get_status(task_id: str):
    # Allows the user to check if their image is done
    from tasks import celery_app
    result = celery_app.AsyncResult(task_id)
    return {        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }