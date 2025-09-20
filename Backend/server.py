from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or put your site origin here, e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Config: Your ML pipeline URL (via ngrok)
# -----------------------------
ML_PIPELINE_URL = "http://ml-pipeline:5000/predict"

# -----------------------------
# Dummy image generation endpoint
# -----------------------------
@app.get("/generate")
async def generate_images(count: int = 10):
    return "ok"
    """Generate dummy images (for frontend demo)"""
    import base64, io
    from PIL import Image
    import random

    images = []
    for i in range(count):
        img = Image.new(
            "RGB",
            (128, 128),
            color=(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        )
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        img_bytes = buf.getvalue()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
        images.append({"name": f"image_{i}.png", "data": img_b64})

    return JSONResponse(content={"images": images})

# -----------------------------
# Forward file to your ML pipeline
# -----------------------------
@app.post("/ml-predict")
async def ml_predict(file: UploadFile):
    try:
        files = {"image": (file.filename, file.file, file.content_type)}
        resp = requests.post(ML_PIPELINE_URL, files=files, timeout=20)
        return JSONResponse(content=resp.json())
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
