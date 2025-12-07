
import os
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .config import settings
from .models import GenerateRequest, GenerateResponse
from .prompt_engine import build_prompt
from .sd_client import generate_image

app = FastAPI(title="18+ Digital Art Generator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(
    file: UploadFile = File(...),
    style_family: str = Form(...),
    intensity: str = Form(...),
    art_style_variant: str = Form("oil_painting"),
    pose_description: str = Form(...),
    clothing_description: str = Form(...),
    environment_description: str = Form(...),
):
    # Save upload
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are allowed")

    upload_id = uuid.uuid4().hex
    upload_path = os.path.join(UPLOAD_DIR, f"input_{upload_id}.png")
    with open(upload_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Build prompts
    prompt, negative_prompt = build_prompt(
        style_family=style_family,
        intensity=intensity,  # type: ignore
        art_variant=art_style_variant,
        pose=pose_description,
        clothing=clothing_description,
        environment=environment_description,
    )

    try:
        out_path = generate_image(upload_path, prompt, negative_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {e}")

    # Expose via static file endpoint style
    abs_out_path = os.path.abspath(out_path)
    # We'll serve via /api/file/{filename}
    file_name = os.path.basename(abs_out_path)
    image_url = f"/api/file/{file_name}"

    job_id = upload_id

    return GenerateResponse(job_id=job_id, image_url=image_url, prompt_used=prompt)


@app.get("/api/file/{filename}")
def get_file(filename: str):
    path = os.path.join(settings.OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)
