# Getting Started Quick Reference

## Fastest Way to Run

```bash
# 1. Navigate to project
cd ai_powered_resume

# 2. Create .env (single command)
cat > .env << EOF
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://pgagi_user:pgagi_password@postgres:5432/candidate_screening
REDIS_URL=redis://redis:6379/0
ENVIRONMENT=development
DEBUG=True
BACKEND_PORT=8000
REACT_APP_API_URL=http://localhost:8000
EOF

# 3. Start with Docker
docker-compose up -d

# 4. Wait for services to be healthy (10-20 seconds)
docker-compose ps

# 5. Open browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

## Manual Setup (No Docker)

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL running locally
- Redis running locally

### Backend (Terminal 1)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env
cp ..\.env.example .env

# Update DATABASE_URL to: postgresql://user:password@localhost:5432/candidate_screening

python scripts/setup_kb.py
python main.py

# Backend runs on http://localhost:8000
```

### Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev

# Frontend runs on http://localhost:3000
```

## Quick Test Flow

1. **Open** http://localhost:3000
2. **Enter** your name and select "Backend Engineer" role
3. **Upload** a sample resume (create a simple text file with skills)
4. **Answer** 5 interview questions
5. **View** results and Q&A transcript

## API Quick Test

```bash
# Get available roles
curl http://localhost:8000/api/session/roles

# Create session
curl -X POST http://localhost:8000/api/session/create \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "John Doe",
    "role": "backend_engineer"
  }'

# Health check
curl http://localhost:8000/health
```

## Common Issues & Fixes

### Port already in use
```bash
# Kill process on port 8000 (backend)
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Database connection error
```bash
# Check PostgreSQL is running
psql -U pgagi_user -d candidate_screening

# If using Docker:
docker-compose logs postgres
```

### Knowledge base not loading
```bash
# Reinitialize KB
docker-compose exec backend python scripts/setup_kb.py

# Or manually:
cd backend
python scripts/setup_kb.py
```

### OpenAI API errors
- Verify API key in .env
- Check account has credits
- Ensure correct model name

## Next Steps

1. **Customize knowledge base**: Edit markdown files in `knowledge_base/`
2. **Add new roles**: Follow role addition guide in IMPLEMENTATION_GUIDE.md
3. **Deploy**: See SETUP.md deployment section
4. **Extend features**: Check ARCHITECTURE.md for enhancement ideas

## Useful Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop all services
docker-compose down

# Reset database
docker-compose down -v  # Removes volumes

# Rebuild containers
docker-compose build --no-cache

# SSH into container
docker-compose exec backend bash

# View backend API documentation
# Navigate to: http://localhost:8000/docs
```

## File Structure Overview

```
ai_powered_resume/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── ml/             # ML/RAG pipeline
│   │   ├── db/             # Database models
│   │   ├── services/       # Business logic
│   │   └── core/           # Config, constants
│   ├── scripts/            # Setup scripts
│   └── main.py             # Entry point
├── frontend/               # Next.js frontend
│   ├── app/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page routes
│   │   ├── services/      # API client
│   │   └── types/         # TypeScript types
│   └── package.json
├── knowledge_base/         # Role-specific KB
│   ├── backend_engineer.md
│   ├── ai_ml_engineer.md
│   ├── frontend_engineer.md
│   └── ...
└── docker-compose.yml      # Container orchestration
```

## Environment Variables Reference

```bash
# Server
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Database
DATABASE_URL=postgresql://...
REDIS_URL=redis://...

# AI/ML
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo

# Interview
MAX_QUESTIONS_PER_SESSION=5
TOP_K_RETRIEVAL=5
RETRIEVAL_THRESHOLD=0.6

# General
ENVIRONMENT=development
DEBUG=True
```

## Support

- Check SETUP.md for detailed setup instructions
- Check ARCHITECTURE.md for system design
- Check IMPLEMENTATION_GUIDE.md for customization
- API docs: http://localhost:8000/docs (when running)

**Questions?** Refer to specific documentation files or check error messages carefully.
