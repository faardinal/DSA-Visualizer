# DSA Visualizer

Full-stack DSA execution visualizer.

## Frontend: Vercel

The frontend is a Vite + React app. Production builds read the backend URL from
`.env.production`.

```bash
npm ci
npm run build
```

Required production variable:

```bash
VITE_API_BASE_URL=https://dsa-visualizer-1-x27w.onrender.com
```

Vercel is configured with `vercel.json` to install with `npm ci`, build with
`npm run build`, and serve the `dist` output directory.

## Backend: Render

The backend is a Flask app under `backend/`. Render is configured by
`render.yaml`.

```bash
pip install -r backend/requirements.txt
gunicorn "backend.app:create_app()" --bind 0.0.0.0:$PORT
```

Health check:

```bash
curl https://dsa-visualizer-1-x27w.onrender.com/api/health
```
