
# 18+ Digital Art App (Self-Hosted, CivitAI-friendly)

This repo contains:

- `backend/` – FastAPI backend that accepts an image, builds safe erotic prompts, and
  calls a Stable Diffusion server (e.g. Automatic1111) that you control.
- `frontend/` – React + Vite app that can be deployed as static files (e.g. GitHub Pages).

## How this works

- You run Stable Diffusion yourself (e.g. Automatic1111 web UI) and import any models
  or LoRAs you download from CivitAI.
- The backend just sends prompts + your reference image (img2img) to that server.
- The frontend talks to the backend via HTTP.

## Quickstart

1. Start your Stable Diffusion (Automatic1111) locally on port 7860.
2. Backend:

   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   export SD_API_URL=http://localhost:7860
   export SD_API_MODE=automatic1111
   uvicorn app.main:app --reload --port 8000
   ```

3. Frontend:

   ```bash
   cd frontend
   npm install
   VITE_API_BASE=http://localhost:8000 npm run dev
   ```

Open the dev server (usually http://localhost:5173) and test generating art.

## GitHub Pages

- Run `npm run build` in `frontend/`.
- Deploy the `dist/` folder to GitHub Pages.
- Make sure your backend is reachable from that domain and update `VITE_API_BASE`
  at build time to match.
