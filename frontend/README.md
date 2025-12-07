
# Frontend - 18+ Digital Art Generator

## Local dev

```bash
cd frontend
npm install
# or: pnpm install / yarn
VITE_API_BASE=http://localhost:8000 npm run dev
```

## Build for GitHub Pages

```bash
npm run build
```

The output will be in `dist/`. You can deploy that folder to GitHub Pages
as a static site. Set `VITE_API_BASE` at build time to point to your
deployed FastAPI backend.
