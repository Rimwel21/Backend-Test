import cloudinary
import cloudinary.uploader
from core.config import settings


cloudinary.config(
    cloud_name=settings.cloud_name,
    api_key=settings.api_key,
    api_secret=settings.api_secret,
    secure=True
)

def upload_file(file_bytes: bytes, folder: str):
    result = cloudinary.uploader.upload(
        file_bytes,
        folder=folder
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }

def delete_file(public_id):
    result = cloudinary.uploader.destroy(public_id)
    return result