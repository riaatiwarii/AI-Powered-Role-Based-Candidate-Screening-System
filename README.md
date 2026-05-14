# AI-Powered Role-Based Candidate Screening System

An intelligent system that conducts dynamic, role-based technical interviews using Retrieval-Augmented Generation (RAG).

## System Architecture

```
┌─────────────────┐
│   React/Next.js │ (Frontend)
│    UI Layer     │
└────────┬────────┘
         │
         │ HTTP/REST
         ▼
┌─────────────────────────────┐
│   FastAPI Backend           │ 
│  ├─ Session Management      │
│  ├─ Resume Processing       │
│  ├─ RAG Pipeline            │
│  └─ Question Generation     │
└────────┬────────────────────┘
         │
    ┌────┴────┬─────────────┐
    ▼         ▼             ▼
┌────────┐ ┌────────────┐ ┌──────────────┐
│Database│ │Vector DB   │ │LLM Service   │
│(PG)    │ │(FAISS/etc) │ │(OpenAI)      │
└────────┘ └────────────┘ └──────────────┘
```

## Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m backend.scripts.setup_kb  # Initialize knowledge base
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Features

- ✅ Dynamic resume processing with skill extraction
- ✅ Role-based interview customization
- ✅ RAG pipeline for contextual question generation
- ✅ Real-time interview interaction
- ✅ Session persistence and tracking
- ✅ Structured response storage and analysis

## Project Structure

```
ai_powered_resume/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── upload.py
│   │   │   │   ├── interview.py
│   │   │   │   └── session.py
│   │   │   └── schemas.py
│   │   ├── ml/
│   │   │   ├── rag_pipeline.py
│   │   │   ├── embeddings.py
│   │   │   ├── question_generator.py
│   │   │   └── resume_processor.py
│   │   ├── db/
│   │   │   ├── models.py
│   │   │   ├── database.py
│   │   │   └── crud.py
│   │   ├── services/
│   │   │   ├── session_service.py
│   │   │   ├── interview_service.py
│   │   │   └── kb_service.py
│   │   └── core/
│   │       ├── config.py
│   │       ├── constants.py
│   │       └── exceptions.py
│   ├── scripts/
│   │   ├── setup_kb.py
│   │   └── seed_data.py
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── components/
│   │   │   ├── ResumeUpload.tsx
│   │   │   ├── RoleSelector.tsx
│   │   │   ├── InterviewSession.tsx
│   │   │   └── ResultsView.tsx
│   │   ├── pages/
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   ├── styles/
│   │   └── hooks/
│   ├── public/
│   ├── package.json
│   └── next.config.js
├── knowledge_base/
│   ├── backend_engineer.md
│   ├── ai_ml_engineer.md
│   └── frontend_engineer.md
├── docker-compose.yml
└── README.md
```

## API Endpoints

- `POST /api/upload` - Upload resume
- `GET /api/roles` - Get available roles
- `POST /api/session/create` - Create interview session
- `GET /api/session/{session_id}` - Get session details
- `POST /api/interview/question` - Generate next question
- `POST /api/interview/answer` - Submit answer
- `GET /api/interview/{session_id}/results` - Get interview results
