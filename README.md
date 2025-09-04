# LabelCraft

A local-first image labeling platform skeleton with FastAPI backend and Vue 3 frontend.

## Backend

```bash
cd api
pip install -e .[test]
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Testing

Run backend tests:

```bash
cd api
pytest
```

Run frontend tests:

```bash
cd frontend
npm test
```
