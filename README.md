# WIP Security Incident Management API

A production-ready REST API for managing security incidents, built with modern backend technologies and security best practices. This system provides comprehensive incident tracking, role-based access control, audit logging for compliance, and real-time analytics.

## Features

### Core Functionality
- **Incident Management**: Full CRUD operations for security incidents with severity levels, categories, and status tracking
- **JWT Authentication**: Secure token-based authentication with password hashing (bcrypt)
- **Role-Based Access Control (RBAC)**: Three-tier permission system (Admin, Analyst, Viewer)
- **Audit Logging**: Complete audit trail of all actions for compliance and forensics
- **Analytics Dashboard**: Real-time statistics including incident counts, severity distribution, and average resolution time
- **File Attachments**: S3-backed file storage for evidence and documentation (ready for AWS integration)

### Technical Highlights
- **RESTful API Design**: Clean, intuitive endpoints following REST principles
- **Type-Safe**: Pydantic schemas for request/response validation
- **Database Optimization**: Indexed queries, efficient relationships, pagination support
- **Security First**: Input validation, SQL injection prevention, secure password storage
- **Production Ready**: Docker containerization, health checks, CORS configuration
- **Auto-Generated Documentation**: Interactive API docs (Swagger UI + ReDoc)

## Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens) with python-jose
- **Password Hashing**: Bcrypt via passlib
- **Containerization**: Docker + Docker Compose
- **Cloud Ready**: AWS S3 integration (boto3)

## Project Structure

```
security-incident-api/
├── app/
│   ├── api/v1/              # API endpoints
│   │   ├── auth.py          # Authentication (login, register)
│   │   └── incidents.py     # Incident management
│   ├── core/                # Core functionality
│   │   ├── config.py        # Settings management
│   │   ├── database.py      # Database connection
│   │   ├── security.py      # JWT & password hashing
│   │   └── dependencies.py  # Auth dependencies (RBAC)
│   ├── models/              # SQLAlchemy database models
│   │   ├── user.py          # User model
│   │   ├── incident.py      # Incident model
│   │   ├── attachment.py    # File attachment model
│   │   └── audit_log.py     # Audit log model
│   ├── schemas/             # Pydantic schemas (validation)
│   │   ├── user.py
│   │   ├── incident.py
│   │   ├── attachment.py
│   │   └── audit_log.py
│   ├── utils/               # Utility functions
│   │   └── audit.py         # Audit logging utilities
│   └── main.py              # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container definition
├── docker-compose.yml      # Multi-container setup
└── README.md               # This file
```

## Architecture

### Database Schema

```
┌─────────────┐       ┌──────────────┐       ┌─────────────────┐
│   Users     │       │  Incidents   │       │  Attachments    │
├─────────────┤       ├──────────────┤       ├─────────────────┤
│ id          │───┐   │ id           │───┬───│ id              │
│ email       │   │   │ title        │   │   │ incident_id (FK)│
│ username    │   └───│ reporter_id  │   │   │ filename        │
│ password    │       │ severity     │   │   │ s3_key          │
│ role        │   ┌───│ status       │   │   │ uploaded_by (FK)│
│ is_active   │   │   │ category     │   │   └─────────────────┘
│ created_at  │   │   │ assigned_to  │   │
└─────────────┘   │   │ source_ip    │   │   ┌─────────────────┐
                  │   │ created_at   │   │   │  Audit Logs     │
                  │   │ resolved_at  │   │   ├─────────────────┤
                  │   └──────────────┘   └───│ id              │
                  │                          │ user_id (FK)    │
                  └──────────────────────────│ action          │
                                             │ resource_type   │
                                             │ resource_id     │
                                             │ ip_address      │
                                             │ timestamp       │
                                             └─────────────────┘
```

### Security Design

1. **Authentication Flow**:
   - User registers → Password hashed with bcrypt → Stored in database
   - User logs in → Password verified → JWT token generated (30-min expiration)
   - Subsequent requests → Token validated → User identity confirmed

2. **Authorization (RBAC)**:
   - **Viewer**: Can view incidents (read-only)
   - **Analyst**: Can create and update incidents
   - **Admin**: Full access including user management and incident deletion

3. **Audit Trail**:
   - Every significant action logged (who, what, when, where)
   - Immutable audit logs for compliance
   - Includes IP address and user agent for forensics

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (recommended)
- PostgreSQL 15+ (if not using Docker)

### Quick Start with Docker (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/security-incident-api.git
   cd security-incident-api
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

   This starts:
   - PostgreSQL database on port 5432
   - FastAPI application on port 8000

3. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Manual Setup (Without Docker)

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL**:
   ```bash
   # Create database
   createdb incident_db
   ```

4. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secret key
   ```

5. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Usage Examples

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "analyst@example.com",
    "username": "security_analyst",
    "password": "SecurePass123!",
    "full_name": "John Doe",
    "role": "analyst"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "security_analyst",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create an Incident

```bash
curl -X POST "http://localhost:8000/api/v1/incidents/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Unauthorized Access Attempt",
    "description": "Multiple failed login attempts detected from suspicious IP",
    "severity": "high",
    "category": "unauthorized_access",
    "source_ip": "192.168.1.100",
    "affected_systems": "Web Server, Database"
  }'
```

### 4. List Incidents (with filtering)

```bash
# All incidents
curl -X GET "http://localhost:8000/api/v1/incidents/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Filter by severity
curl -X GET "http://localhost:8000/api/v1/incidents/?severity=critical" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Pagination
curl -X GET "http://localhost:8000/api/v1/incidents/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 5. Get Statistics

```bash
curl -X GET "http://localhost:8000/api/v1/incidents/stats/summary" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

Response:
```json
{
  "total_incidents": 42,
  "open_incidents": 8,
  "in_progress_incidents": 12,
  "resolved_incidents": 20,
  "closed_incidents": 2,
  "critical_incidents": 3,
  "high_incidents": 15,
  "incidents_by_category": {
    "unauthorized_access": 12,
    "malware": 8,
    "phishing": 15,
    "data_breach": 7
  },
  "avg_resolution_time_hours": 4.25
}
```

## API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` - Register new user
- `POST /login` - Login and receive JWT token
- `GET /me` - Get current user info

### Incidents (`/api/v1/incidents`)
- `POST /` - Create incident (Analyst+)
- `GET /` - List incidents (with filters)
- `GET /{id}` - Get specific incident
- `PATCH /{id}` - Update incident (Analyst+)
- `DELETE /{id}` - Delete incident (Admin only)
- `GET /stats/summary` - Get analytics

## Security Considerations

- **Password Security**: Bcrypt hashing with automatic salt generation
- **Token Expiration**: JWT tokens expire after 30 minutes
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **Input Validation**: Pydantic schemas validate all inputs
- **CORS**: Configured for specific origins (update in production)
- **Audit Trail**: All actions logged with IP address and timestamp

## Development Roadmap

### Completed
- ✅ JWT authentication
- ✅ Role-based access control
- ✅ Incident CRUD operations
- ✅ Audit logging
- ✅ Analytics endpoints
- ✅ Docker containerization

### Future Enhancements
- 🔲 S3 file upload implementation
- 🔲 Real-time notifications (WebSocket)
- 🔲 Email alerts for critical incidents
- 🔲 Advanced search and filtering
- 🔲 Incident assignment and workflow
- 🔲 Integration with SIEM systems
- 🔲 Rate limiting
- 🔲 API key authentication for service accounts

## Testing

Access the interactive API documentation at `/docs` to test endpoints directly in your browser:

1. Go to http://localhost:8000/docs
2. Create a user using `/auth/register`
3. Login using `/auth/login` and copy the token
4. Click "Authorize" button and paste your token
5. Try any endpoint!

## Environment Variables

Key environment variables (see `.env.example`):

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/incident_db

# Security
SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS (optional, for file uploads)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET_NAME=incident-attachments
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact

Jesus Almonte - [LinkedIn](https://www.linkedin.com/in/jesus-almonte-0754a823a) 

Project Link: [https://github.com/silverslayz/security-incident-api](https://github.com/silverslayz/security-incident-api)

---

** AI tools (e.g., ChatGPT) were used to help generate ideas, troubleshoot errors, and improve code readability. All final code decisions, integration, and testing were done by me

**Built with Python FastAPI | Showcasing backend engineering, security practices, and cloud-ready architecture**
