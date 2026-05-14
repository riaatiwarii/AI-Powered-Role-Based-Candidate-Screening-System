# Setup and Installation Guide

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 13+ (or use Docker)
- Redis (or use Docker)

## Quick Start with Docker

### 1. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_key_here
```

### 2. Start Services

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Initialize Knowledge Base

```bash
# Backend container will auto-initialize KB on startup
# Or manually run:
docker-compose exec backend python scripts/setup_kb.py
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ..\.env.example .env

# Setup database (ensure PostgreSQL is running)
# Update DATABASE_URL in .env

# Initialize knowledge base
python scripts/setup_kb.py

# Run server
python main.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start dev server
npm run dev
```

## System Architecture

```
┌─────────────────────────────────────┐
│      Frontend (Next.js)             │
│  - React Components                 │
│  - State Management (Zustand)       │
│  - API Integration                  │
└────────────────────┬────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────┐
│     Backend (FastAPI)               │
│  ├─ Resume Processing               │
│  ├─ RAG Pipeline                    │
│  ├─ Question Generation             │
│  └─ Session Management              │
└────────────┬────────────┬───────────┘
             │            │
    ┌────────▼───┐  ┌─────▼────────┐
    │ PostgreSQL │  │ Vector DB    │
    │ (Sessions) │  │ (FAISS)      │
    └────────────┘  └──────────────┘
```

## Key Features

### Resume Processing
- Extracts text from PDF, TXT, DOCX
- Identifies technical skills
- Estimates experience level
- Recognizes domain expertise

### RAG Pipeline
- Chunks knowledge base documents
- Generates embeddings using Sentence Transformers
- Stores vectors in FAISS for fast retrieval
- Supports semantic search

### Question Generation
- Generates contextual questions based on retrieved knowledge
- Adapts difficulty based on candidate experience
- Personalizes questions based on resume skills
- Maintains question variety

### Interview Management
- Multi-question sessions
- Session persistence
- Response tracking
- Performance metrics

## API Endpoints

### Sessions
- `POST /api/session/create` - Create new session
- `GET /api/session/{id}` - Get session details
- `POST /api/session/{id}/complete` - Complete session
- `GET /api/session/{id}/results` - Get interview results
- `GET /api/session/roles` - Get available roles

### Resume
- `POST /api/upload/resume` - Upload and process resume

### Interview
- `POST /api/interview/question` - Generate next question
- `POST /api/interview/answer` - Submit answer

## Configuration

Edit `.env` file to customize:

```
# Server
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/candidate_screening

# AI/ML
OPENAI_API_KEY=your_key
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4-turbo

# Interview
MAX_QUESTIONS_PER_SESSION=5
TOP_K_RETRIEVAL=5
RETRIEVAL_THRESHOLD=0.6
```

## Database Schema

### Key Tables
- `sessions` - Interview sessions
- `interview_questions` - Generated questions
- `candidate_responses` - Candidate answers
- `session_metrics` - Performance metrics
- `kb_chunks` - Knowledge base chunks

## Development

### Testing Backend

```bash
# Run tests
pytest

# With coverage
pytest --cov=app
```

### Linting

```bash
# Backend
pylint app/

# Frontend
npm run lint
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Run: `docker-compose logs postgres`

### OpenAI API Error
- Verify API key in .env
- Check API rate limits
- Ensure correct model name

### Vector DB Issues
- Clear FAISS index: `rm -rf data/vector_db`
- Reinitialize KB: `python scripts/setup_kb.py`

## Performance Tips

- Use appropriate chunk size (1000-2000 tokens)
- Limit retrieved chunks (k=5 is usually sufficient)
- Enable connection pooling for DB
- Use Redis for caching
- Profile with Python profiler: `python -m cProfile main.py`

## Deployment

### Production Checklist
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Use strong database password
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set up monitoring and logging
- [ ] Use proper secrets management
- [ ] Scale with load balancer
- [ ] Setup automated backups
- [ ] Enable rate limiting

### Deployment Platforms
- AWS ECS/EKS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform
- Heroku (deprecated but examples available)

## Contributing

1. Create feature branch
2. Make changes with tests
3. Ensure linting passes
4. Submit PR with description

## License

MIT License - See LICENSE file
