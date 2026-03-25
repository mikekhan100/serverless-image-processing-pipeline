from celery import Celery
from processor import ImageProcessor
import os

# 1. Initialize Celery to use Redis as the broker
celery_app = Celery(
    "image_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def process_image_task(file_path):
    """The background worker logic."""
    if not os.path.exists(file_path):
        return {"error": "File not found"}
        
    processor = ImageProcessor(file_path)
    processed_files = processor.generate_all()
    
    return {
        "status": "Completed",
        "output_files": processed_files
    }