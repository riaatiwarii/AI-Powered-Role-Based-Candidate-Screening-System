# Welcome to the AI-Powered Candidate Screening System

**A complete, production-ready full-stack application for intelligent technical interviewing**

## 🎯 Quick Navigation

### Getting Started
- **New to the project?** → Start with [QUICKSTART.md](QUICKSTART.md) (5 minutes)
- **Want to deploy?** → Read [SETUP.md](SETUP.md)
- **Understanding the code?** → Check [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)

### Deep Dives
- **System Architecture** → [ARCHITECTURE.md](ARCHITECTURE.md)
- **Customization & Features** → [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
- **Project Overview** → [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

### API Documentation
- Interactive docs: http://localhost:8000/docs (when running)
- [API Endpoints Reference](SETUP.md#api-endpoints)

---

## 🚀 One-Command Start

```bash
cd d:\ai_powered_resume
docker-compose up -d
# Wait 10-20 seconds...
# Frontend: http://localhost:3000
# API: http://localhost:8000
```

**No Docker?** See Manual Setup in [QUICKSTART.md](QUICKSTART.md)

---

## 📦 What's Included

### ✅ Backend (FastAPI + Python)
- Intelligent RAG pipeline for question generation
- Resume processing with skill extraction
- Semantic search with FAISS vector database
- RESTful API with proper error handling
- PostgreSQL database with normalized schema
- Async operations throughout

### ✅ Frontend (Next.js + React)  
- Beautiful, responsive interview UI
- Resume upload interface
- Real-time Q&A interaction
- Results dashboard with metrics
- Zustand state management
- Tailwind CSS styling

### ✅ ML/AI Components
- Sentence Transformer embeddings
- FAISS vector search
- LLM-powered question generation
- Context-aware prompting
- Resume analysis engine

### ✅ Knowledge Base
- Backend Engineer content
- AI/ML Engineer content
- Frontend Engineer content
- Fullstack Engineer content
- Data Engineer content
- **Easily extensible**

### ✅ Infrastructure
- Docker & docker-compose configuration
- Production-ready Dockerfiles
- Environment configuration
- Comprehensive documentation

---

## 📖 Documentation Map

```
README.md (this file)
├── QUICKSTART.md ..................... 5-minute setup
├── SETUP.md .......................... Detailed installation
├── ARCHITECTURE.md ................... System design deep-dive
├── IMPLEMENTATION_GUIDE.md ........... Customization & features
├── PROJECT_SUMMARY.md ............... Complete overview
└── DIRECTORY_STRUCTURE.md ........... File organization & reference
```

---

## 💡 Core Concepts

### Retrieval-Augmented Generation (RAG)
```
Resume Data
    ↓
Query Construction
    ↓
Semantic Search (FAISS)
    ↓
Context Retrieval
    ↓
LLM Question Generation
```

### Interview Flow
```
1. Candidate Info Input
2. Resume Upload & Analysis
3. Question Loop (5x by default)
   ├─ Generate contextual question
   ├─ Candidate answers
   ├─ Store response
   └─ Repeat
4. View Results & Metrics
```

---

## 🏗️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI, Python 3.11 |
| Frontend | Next.js, React, TypeScript |
| Database | PostgreSQL |
| Vector DB | FAISS |
| Embeddings | Sentence Transformers |
| LLM | OpenAI GPT-4 |
| State | Zustand |
| Styling | Tailwind CSS |
| Containers | Docker, docker-compose |

---

## 📊 Architecture Overview

```
                    ┌─ Next.js Frontend ─┐
                    │  React Components   │
                    │  Zustand State      │
                    └──────┬──────────────┘
                           │ HTTP REST
                    ┌──────▼──────────────┐
                    │  FastAPI Backend    │
                    │  ├─ RAG Pipeline    │
                    │  ├─ Resume Parser   │
                    │  ├─ Question Gen    │
                    │  └─ API Routes      │
                    └─┬──────────────────┬┘
                      │                  │
            ┌─────────▼─────┐  ┌────────▼────────┐
            │  PostgreSQL   │  │ FAISS + Embeddings
            │  Sessions     │  │ Knowledge Base
            └───────────────┘  └──────────────────┘
```

---

## 🎓 What You'll Learn

By exploring this codebase:

1. **AI/ML**: RAG pipelines, embeddings, semantic search
2. **Backend**: FastAPI, async Python, service architecture
3. **Frontend**: Next.js, React hooks, state management
4. **Databases**: PostgreSQL, ORM patterns, schema design
5. **System Design**: Scalability, performance, caching
6. **DevOps**: Docker, containerization, environment management
7. **Best Practices**: Error handling, validation, testing
8. **Production Patterns**: Configuration, monitoring, security

---

## ✨ Highlights

✅ **Production-Ready**: Not a tutorial project - built for real use  
✅ **Well-Architected**: Clear separation of concerns  
✅ **Fully Documented**: Comprehensive guides for every aspect  
✅ **Extensible**: Easy to add roles, customize logic  
✅ **Scalable**: Async operations, connection pooling  
✅ **Secure**: Input validation, error handling  
✅ **Complete**: Backend, frontend, infrastructure, docs  

---

## 🚀 Getting Started

### Option 1: Docker (Easiest)
```bash
cp .env.example .env
# Edit .env, add OPENAI_API_KEY
docker-compose up -d
```
→ [Full Docker guide](QUICKSTART.md)

### Option 2: Manual (Most Flexible)
```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
# In separate terminals:
# Terminal 1: cd backend && python main.py
# Terminal 2: cd frontend && npm run dev
```
→ [Full manual setup](QUICKSTART.md)

### Option 3: Check It Out First
- Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for overview
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for design
- Browse the code: `backend/app/` and `frontend/app/`

---

## 📁 Project Structure

```
ai_powered_resume/
├── backend/          # FastAPI + Python ML
├── frontend/         # Next.js + React
├── knowledge_base/   # Role-specific content (markdown)
├── docker-compose.yml
├── QUICKSTART.md     # ← Start here for fast setup
├── SETUP.md          # ← Detailed installation
├── ARCHITECTURE.md   # ← System design
├── IMPLEMENTATION_GUIDE.md  # ← Customization
└── PROJECT_SUMMARY.md       # ← Complete overview
```

---

## 🎯 Common Tasks

### Start the System
```bash
docker-compose up -d
# or
cd backend && python main.py  # Terminal 1
cd frontend && npm run dev     # Terminal 2
```

### Add a New Role
1. Create `knowledge_base/role_name.md`
2. Update `app/core/constants.py`
3. Run `python scripts/setup_kb.py`

### Customize Questions
Edit `app/ml/question_generator.py` and restart

### Deploy to Production
See [Deployment section in SETUP.md](SETUP.md#deployment)

### View API Docs
Open http://localhost:8000/docs when backend is running

---

## 💻 Development

### Frontend Development
```bash
cd frontend
npm run dev          # Development server
npm run build        # Production build
npm run lint         # Code quality
npm test             # Run tests
```

### Backend Development
```bash
cd backend
python main.py       # Development server
python -m pytest     # Run tests
python scripts/setup_kb.py  # Initialize KB
```

---

## 🔧 Configuration

### Key Environment Variables
```
OPENAI_API_KEY          # Your OpenAI key
DATABASE_URL            # PostgreSQL connection
BACKEND_PORT            # Default: 8000
REACT_APP_API_URL       # Default: http://localhost:8000
MAX_QUESTIONS_PER_SESSION  # Default: 5
```

→ See [.env.example](.env.example) for all options

---

## 📞 Need Help?

1. **Quick Setup**: [QUICKSTART.md](QUICKSTART.md)
2. **Installation Issues**: [SETUP.md](SETUP.md)
3. **Understanding Code**: [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Customizing**: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
5. **File Organization**: [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md)
6. **Overview**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 🎉 Next Steps

### New Users
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Run `docker-compose up -d`
3. Test at http://localhost:3000

### Developers
1. Read [ARCHITECTURE.md](ARCHITECTURE.md)
2. Explore `/backend/app/` and `/frontend/app/`
3. Check [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for customization

### Deployers
1. Read [SETUP.md](SETUP.md)
2. Follow deployment checklist
3. Set up monitoring

---

## 📜 License

MIT License - Free for commercial and personal use

---

## 👏 Ready to Begin?

**Start with**: [QUICKSTART.md](QUICKSTART.md) (5 minutes)  
**Then explore**: [ARCHITECTURE.md](ARCHITECTURE.md) (understanding)  
**Finally customize**: [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) (your needs)

**Let's go! 🚀**
