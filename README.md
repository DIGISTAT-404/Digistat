# DIGISAT Cyber Risk Prototype

AI-powered continuous cyber risk quantification and investment optimization prototype.

## Structure
- `frontend/` React + Vite dashboard
- `backend/` FastAPI REST API + synthetic cybersecurity dataset

## Frontend
```bash
cd frontend
npm install
npm run dev
```

## Backend
Open another terminal:
```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

The dataset is synthetic demo data for the prototype and should be replaced with authorized production telemetry before deployment.
