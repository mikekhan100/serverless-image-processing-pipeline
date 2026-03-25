# Serverless Image Processing Pipeline

An asynchronous, distributed image manipulation service built with **Python**, **FastAPI**, and **Celery**.  This project demonstrates how to handle CPU-intensive tasks (Image Processing) without blocking the main web server, ensuring high availability and low latency.

## 🚀 Key Features
* **Asynchronous Processing:** Offloads heavy image manipulation to background workers using Celery and Redis.
* **Image Transformations:** Automatically generates high-quality Thumbnails, Grayscale versions, and Gaussian Blurred images using the Pillow library.
* **Status Polling:** Includes a dedicated endpoint to track the real-time status of background tasks via Task IDs.
* **Robust File Handling:** Implements memory-efficient file streaming and handles PNG-to-JPEG transparency conversions.

## 🛠️ Tech Stack
* **Framework:** FastAPI
* **Task Queue:** Celery
* **Message Broker:** Redis (Docker)
* **Image Engine:** Pillow (PIL)
* **Infrastructure:** Docker Desktop

## ⚙️ How It Works
1. **The Client** uploads an image to the `/upload/` endpoint.
2. **FastAPI** saves the file and dispatches a task to **Redis**.
3. **The Worker (Celery)** picks up the task and performs the image maths.
4. **The Client** polls the `/status/{task_id}` endpoint to retrieve the finished file paths.

## 🚦 Quick Start
1. Start Redis: `docker run -d -p 6379:6379 redis`
2. Start Celery: `celery -A tasks worker --loglevel=info -P solo`
3. Start API: `uvicorn main:app --reload`
4. Visit: `http://127.0.0.1:8000/docs`