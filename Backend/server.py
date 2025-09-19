import boto3
from supabase import create_client, Client
import os

from typing import List
from pydantic import BaseModel

import uvicorn  # for fastapi
from fastapi import FastAPI, UploadFile

# --- Supabase connection ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- MinIO (running on Fly.io) ---
MINIO_URL = os.environ.get("MINIO_URL", "http://minio:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "123456789")
MINIO_BUCKET = os.environ.get("MINIO_BUCKET", "photos")

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1"  # dummy, not used by MinIO
)

# Ensure bucket exists
try:
    s3.create_bucket(Bucket=MINIO_BUCKET)
except Exception:
    pass


class PhotoModel(BaseModel):
    id: int
    photo_name: str
    photo_url: str
    is_deleted: bool


app = FastAPI(debug=True)


@app.get("/status")
async def check_status():
    return "ok"


@app.get("/photos", response_model=List[PhotoModel])
async def get_all_photos():
    # Fetch from Supabase table "photo"
    try:
        response = supabase.table("photo").select("*").order("id", desc=True).execute()
        rows = response.data
    except Exception as e:
        return {"error": f"Supabase fetch failed: {str(e)}"}

    formatted_photos = []
    for row in rows:
        formatted_photos.append(
            PhotoModel(
                id=row["id"],
                photo_name=row["photo_name"],
                photo_url=row["photo_url"],
                is_deleted=row["is_deleted"],
            )
        )

    return formatted_photos


@app.post("/photos", status_code=201)
async def add_photo(file: UploadFile):
    # Upload to MinIO
    try:
        s3.upload_fileobj(file.file, MINIO_BUCKET, file.filename)
    except Exception as e:
        return {"error": f"Upload to MinIO failed: {str(e)}"}

    # Public link (Fly.io MinIO URL + bucket + file)
    photo_url = f"{MINIO_URL}/{MINIO_BUCKET}/{file.filename}"

    # Insert metadata into Supabase
    try:
        response = supabase.table("photo").insert(
            {
                "photo_name": file.filename,
                "photo_url": photo_url,
                "is_deleted": False,
            }
        ).execute()

        new_row = response.data[0]
    except Exception as e:
        return {"error": f"Supabase insert failed: {str(e)}"}

    return {
        "id": new_row["id"],
        "photo_name": new_row["photo_name"],
        "photo_url": new_row["photo_url"],
        "is_deleted": new_row["is_deleted"],
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
