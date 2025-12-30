"""
Main FastAPI application.
Entry point for the Security Incident Management API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, incidents

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    **Security Incident Management API** - A comprehensive system for tracking and managing security incidents.

    ## Features
    * **JWT Authentication** - Secure token-based authentication
    * **Role-Based Access Control** - Admin, Analyst, and Viewer roles
    * **Incident Management** - Full CRUD operations for security incidents
    * **Audit Logging** - Complete audit trail for compliance
    * **File Attachments** - S3-backed file storage
    * **Analytics** - Incident statistics and reporting

    ## Security
    All endpoints (except registration and login) require authentication.
    Include your JWT token in the Authorization header:
    ```
    Authorization: Bearer <your_token>
    ```
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(incidents.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    """
    Root endpoint - API health check.
    """
    return {
        "message": "Security Incident Management API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}
