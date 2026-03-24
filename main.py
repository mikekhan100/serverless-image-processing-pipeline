import os
import shutil
from fastapi import FastAPI, UploadFile, File
from processor import ImageProcessor

app = FastAPI()

# Create a directory for uploaded images
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.get("/")
def home():
    return {"message": "Image Processing API is online!"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # 1. Save the uploaded file locally
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Call the "Engine" (processor.py)
    # Note: This is currently "blocking" (Synchronous)
    processor = ImageProcessor(file_path)
    processed_files = processor.generate_all()
    
    return {
        "status": "Processed",
        "filename": file.filename,
        "outputs": processed_files
    }