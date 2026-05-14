# Architecture and Design Document

## System Overview

The AI-Powered Candidate Screening System is a full-stack application that conducts intelligent, role-based technical interviews using Retrieval-Augmented Generation (RAG).

## Core Design Principles

1. **Modularity**: Each component is independent and testable
2. **Scalability**: Designed to handle multiple concurrent sessions
3. **Extensibility**: Easy to add new roles, knowledge bases, or question generation strategies
4. **Robustness**: Comprehensive error handling and validation

## Component Architecture

### Frontend Layer (Next.js + React)

**Responsibilities:**
- User interface for interview flow
- Resume upload handling
- Real-time question display and answer submission
- Results visualization

**Key Components:**
- `page.tsx`: Main orchestrator component
- `ResumeUpload.tsx`: Resume file handling
- `RoleSelector.tsx`: Role selection UI
- `InterviewSession.tsx`: Interview Q&A flow
- `ResultsView.tsx`: Results display

**State Management:**
- Zustand for global state (session, current question, answers)
- React hooks for component-level state
- API service for backend communication

**Technology Choices:**
- Next.js: Modern React framework with SSR
- TypeScript: Type safety
- Tailwind CSS: Utility-first styling
- Axios: HTTP client

### Backend Layer (FastAPI + Python)

**Responsibilities:**
- Business logic orchestration
- Resume processing
- RAG pipeline execution
- Question generation
- Session persistence

**Architecture Layers:**

```
API Layer (Routes)
    ↓
Service Layer (Business Logic)
    ↓
ML Layer (RAG, Question Generation)
    ↓
Database Layer (ORM)
    ↓
Data Layer (PostgreSQL)
```

**API Routes:**
- `/api/session/*` - Session management
- `/api/upload/*` - Resume processing
- `/api/interview/*` - Question and answer handling

**Services:**
- `InterviewService`: Core interview logic
- `SessionService`: Session operations
- `KnowledgeBaseService`: KB management

**ML Pipeline:**
- Resume text extraction and analysis
- Embedding generation
- Vector search and retrieval
- Question generation with context

### Database Layer

**PostgreSQL Schema:**
- `sessions`: Interview session metadata
- `interview_questions`: Generated questions with context
- `candidate_responses`: Answer storage
- `session_metrics`: Performance metrics
- `kb_chunks`: Knowledge base chunks

**Design Decisions:**
- Normalized schema for efficient queries
- JSON columns for flexible metadata
- Cascade delete for referential integrity
- Indexes on frequently queried columns

### ML Pipeline Architecture

#### 1. Knowledge Ingestion

```
Knowledge Base Files (Markdown)
    ↓
Text Chunking (1000 tokens with overlap)
    ↓
Embedding Generation (Sentence Transformers)
    ↓
Vector Storage (FAISS Index)
    ↓
Persistence (Database + Disk)
```

**Chunking Strategy:**
- Fixed-size chunks (1000 tokens)
- Overlap for context preservation (200 tokens)
- Metadata tracking for source attribution

#### 2. Retrieval Mechanism

```
Resume + Role Selection
    ↓
Query Construction
    ↓
Query Embedding
    ↓
Semantic Search (FAISS)
    ↓
Result Ranking & Filtering
    ↓
Context Assembly
```

**Key Algorithms:**
- Cosine similarity for ranking (L2 distance in FAISS)
- Threshold filtering (0.6 by default)
- Top-K retrieval (5 results)
- Context window optimization

#### 3. Question Generation

```
Retrieved Context + Resume Info
    ↓
Prompt Construction (with role context)
    ↓
LLM Generation
    ↓
Question Formatting
    ↓
Metadata Attachment (sources, difficulty)
```

**Generation Strategy:**
- Context-aware prompting
- Resume-personalized difficulty scaling
- Fallback template-based generation
- Source tracking for traceability

## Data Flow

### Session Lifecycle

```
1. Candidate Entry
   ├─ User inputs name and email
   └─ Selects target role
   
2. Session Creation
   └─ Backend creates session record
   
3. Resume Upload
   ├─ File received by backend
   ├─ Text extraction (PDF/DOCX/TXT)
   ├─ Skill extraction
   ├─ Resume stored in session
   └─ Frontend receives analysis
   
4. Interview Initiation
   ├─ KB loaded for selected role
   └─ First question generated
   
5. Q&A Cycle (Repeat N times)
   ├─ Question displayed to candidate
   ├─ Candidate submits answer
   ├─ Answer stored in database
   ├─ Next question generation triggered
   └─ Cycle repeats
   
6. Session Completion
   ├─ Metrics calculation
   ├─ Results aggregation
   └─ Display to candidate
```

## Retrieval-Augmented Generation (RAG)

### Why RAG?

1. **Grounding**: Answers grounded in actual knowledge base
2. **Currency**: Easy to update knowledge without retraining
3. **Traceability**: Transparent source attribution
4. **Relevance**: Contextual information from curated sources

### RAG Pipeline Flow

```
┌──────────────┐
│   Resume     │
│   Analysis   │
└──────┬───────┘
       │
       ├─────► Extract Skills
       │       Extract Experience
       │       Extract Domains
       │
┌──────▼────────────┐
│  Query Builder    │
│  (Role + Skills)  │
└──────┬────────────┘
       │
┌──────▼────────────────┐
│  Embedding Manager    │
│  (Query Vectorization)│
└──────┬────────────────┘
       │
┌──────▼────────────────┐
│   Vector DB (FAISS)   │
│   Semantic Search     │
└──────┬────────────────┘
       │
┌──────▼────────────────┐
│  Retrieved Chunks     │
│  (Top 5 Similar)      │
└──────┬────────────────┘
       │
┌──────▼────────────────┐
│  Context Assembly     │
│  (Window Optimization)│
└──────┬────────────────┘
       │
┌──────▼────────────────┐
│  Question Generator   │
│  (LLM + Context)      │
└──────┬────────────────┘
       │
       └─────► Generated Question
               with Source Attribution
```

## Question Generation Strategy

### Context-Aware Generation

1. **Resume Analysis**: Extract skills, experience, domains
2. **Role Matching**: Understand role-specific requirements
3. **Context Retrieval**: Get relevant knowledge base chunks
4. **Difficulty Scaling**: Adjust based on experience level
5. **Question Formulation**: Create specific, answerable questions
6. **Source Tracking**: Attribute to knowledge base source

### Difficulty Levels

- **Easy**: Foundational concepts, definitions
- **Medium**: Applied understanding, practical scenarios
- **Hard**: Design decisions, optimization, trade-offs

**Scaling Logic:**
```
Junior + Easy → Basic concept questions
Mid + Medium → Practical application questions
Senior + Hard → Architecture and optimization questions
```

## Scalability Considerations

### Current Architecture Supports

- **Single-threaded**: Currently designed for sequential question generation
- **Session Isolation**: Each session independent
- **Concurrent Sessions**: Multiple candidates simultaneously

### Future Enhancements

- Async question generation pipeline
- Distributed vector indexing
- Connection pooling for DB
- Caching layer (Redis)
- Message queue for async processing

## Error Handling

### Application Exceptions

```python
AppException (base)
├── ResumeProcessingError
├── EmbeddingError
├── RetrievalError
├── QuestionGenerationError
├── SessionError
├── ValidationError
├── NotFoundError
└── KnowledgeBaseError
```

**Error Flow:**
1. Exception raised in service/ML layer
2. Caught by API route handler
3. Converted to HTTP response
4. Returned with appropriate status code and message

## Testing Strategy

### Unit Tests
- Resume processor functions
- Embedding manager
- Vector DB operations
- Question generation logic

### Integration Tests
- API endpoints with in-memory DB
- Full session workflow
- Resume upload to results

### End-to-End Tests
- Complete interview flow
- Frontend-backend interaction

## Security Considerations

1. **Input Validation**: All inputs validated with Pydantic
2. **File Upload**: Whitelist file types, size limits
3. **API Security**: CORS configured, rate limiting
4. **Database**: Parameterized queries, no SQL injection
5. **Secrets**: Environment variables for API keys

## Performance Optimization

### Database
- Indexes on frequently queried columns
- Connection pooling
- Query optimization

### ML Pipeline
- Embedding caching
- Batch processing support
- Vector DB optimization (FAISS)

### Frontend
- Code splitting with Next.js
- Lazy component loading
- API response caching

## Monitoring and Logging

### Application Metrics
- Request latency
- Error rates
- Session completion rates
- Average answer quality

### Logging
- All API requests
- ML pipeline operations
- Database queries
- Error stack traces

## Knowledge Base Management

### File Organization
```
knowledge_base/
├── backend_engineer.md
├── ai_ml_engineer.md
├── frontend_engineer.md
├── fullstack_engineer.md
└── data_engineer.md
```

### Update Process
1. Update markdown files
2. Rerun `setup_kb.py`
3. FAISS index automatically rebuilt
4. No service restart needed

## Future Enhancement Opportunities

1. **Dynamic Question Adaptation**: Adjust questions based on answer quality
2. **Answer Evaluation**: Automatic scoring of responses
3. **Feedback Generation**: AI-generated detailed feedback
4. **Interview Analytics**: Dashboard showing trends
5. **Multi-turn Conversations**: Follow-up questions based on answers
6. **Video Recording**: Record and transcribe candidate responses
7. **Code Evaluation**: Support for coding questions with execution
8. **Real-time Collaboration**: Live interview with evaluator
9. **ML Model Fine-tuning**: Customize to company needs
10. **Bias Detection**: Identify and mitigate bias in questions
