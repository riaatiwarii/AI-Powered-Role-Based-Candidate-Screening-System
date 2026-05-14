# Backend Engineer Knowledge Base

## System Design Fundamentals

### Scalability Patterns
- Horizontal scaling: Adding more servers to handle increased load
- Vertical scaling: Increasing resources of existing servers
- Load balancing: Distributing traffic across multiple servers
- Database sharding: Partitioning data across multiple databases
- Caching strategies: Using in-memory stores like Redis for frequently accessed data

### Database Design
- ACID properties: Atomicity, Consistency, Isolation, Durability
- CAP theorem: Consistency, Availability, Partition tolerance trade-offs
- SQL vs NoSQL: Relational databases vs document stores
- Indexing strategies: B-tree indexes, hash indexes for query optimization
- Query optimization: Execution plans, index usage analysis

### API Design
- REST principles: Stateless, cacheable, uniform interface
- HTTP methods: GET, POST, PUT, DELETE, PATCH
- Status codes: 200, 201, 400, 404, 500, etc.
- API versioning: URL-based, header-based approaches
- Rate limiting and throttling: Protecting APIs from overuse

## Backend Architecture

### Microservices
- Service independence: Each service owns its data
- Service communication: Synchronous (REST, gRPC) vs asynchronous (message queues)
- Service discovery: How services find each other
- Circuit breaker pattern: Preventing cascading failures
- API gateway: Single entry point for all services

### Message Queues
- Purpose: Decoupling services for asynchronous processing
- Popular systems: RabbitMQ, Apache Kafka, AWS SQS
- Message ordering: Ensuring message delivery sequence
- Exactly-once delivery: Guaranteeing message processing

### Caching Strategies
- Cache-aside pattern: Application manages cache
- Write-through: Writing to cache and database simultaneously
- Write-behind: Writing to cache, then database asynchronously
- Cache invalidation: TTL, manual invalidation
- Distributed caching: Memcached, Redis

## Security

### Authentication and Authorization
- JWT tokens: Stateless authentication mechanism
- OAuth 2.0: Third-party authorization
- Session management: Server-side session storage
- Role-based access control (RBAC): Permission management
- Principle of least privilege: Minimum necessary permissions

### Data Security
- Encryption in transit: TLS/SSL protocols
- Encryption at rest: Encrypting stored data
- Hashing: One-way cryptographic functions
- Salting: Adding random data to hashes
- SQL injection prevention: Parameterized queries

### API Security
- CORS (Cross-Origin Resource Sharing): Restricting requests
- CSRF (Cross-Site Request Forgery) protection: Token validation
- Input validation: Sanitizing user inputs
- Output encoding: Preventing XSS attacks

## Performance Optimization

### Database Optimization
- Query optimization: Using indexes and execution plans
- Connection pooling: Reusing database connections
- Denormalization: Storing redundant data for faster queries
- Read replicas: Distributing read load across multiple instances
- Database monitoring: Performance tracking and alerting

### Application Performance
- Profiling: Identifying bottlenecks
- Memory management: Preventing leaks
- Async/await patterns: Non-blocking operations
- Thread pooling: Managing concurrent requests
- Load testing: Stress testing systems

### Infrastructure Optimization
- CDN usage: Content delivery networks
- Compression: Gzip, Brotli for data compression
- HTTP/2: Protocol improvements
- DNS optimization: Reducing resolution time
- Monitoring and logging: Performance tracking

## DevOps and Deployment

### Containerization
- Docker basics: Images, containers, registries
- Multi-stage builds: Optimizing image size
- Container orchestration: Managing containers
- Resource limits: CPU and memory constraints

### CI/CD Pipeline
- Continuous integration: Automated testing
- Continuous deployment: Automated releases
- Version control: Git workflows
- Testing strategies: Unit, integration, end-to-end tests
- Blue-green deployment: Zero-downtime deployments

### Monitoring and Logging
- Application metrics: Request rate, latency, errors
- Distributed tracing: Tracking requests across services
- Log aggregation: Centralized logging
- Alerting: Automated notifications
- Dashboards: Visualizing system health
