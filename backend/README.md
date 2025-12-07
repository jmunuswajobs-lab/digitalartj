
# Backend - 18+ Digital Art Generator

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export SD_API_URL=http://localhost:7860
export SD_API_MODE=automatic1111  # or mock
uvicorn app.main:app --reload --port 8000
```

The backend expects an Automatic1111-compatible Stable Diffusion server running
at `SD_API_URL`. You can load any models / LoRAs you downloaded from CivitAI
into that UI; this app just builds prompts and calls img2img.
