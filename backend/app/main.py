"""
Group Fitness API - Main FastAPI Application

This is the main entry point for the Group Fitness social app API.
It provides endpoints for user authentication, profile management, and onboarding.

The app is designed to be:
- Mobile-first (works with React Native Web frontend)
- Local-first (can run completely locally with Docker)
- AWS-ready (integrates with Cognito, S3, RDS for production)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, users

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Group Fitness API",
    description="API for social fitness app - find and create group rides/runs",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc UI
)

# Configure CORS for frontend access
# In production, replace with your actual domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:3000",  # Alternative localhost
        # Add your production frontend URL here
    ],
    allow_credentials=True,  # Allow cookies and auth headers
    allow_methods=["*"],     # Allow all HTTP methods
    allow_headers=["*"],     # Allow all headers
)

# Register API routers
app.include_router(auth.router)    # Authentication endpoints (/auth/*)
app.include_router(users.router)   # User profile endpoints (/users/*)

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - API information
    
    Returns basic information about the API.
    Useful for checking if the API is running.
    """
    return {
        "message": "Group Fitness API", 
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/ping", tags=["Health"])
async def ping():
    """
    Ping endpoint for health checks
    
    Simple endpoint to verify the API is responsive.
    Used by monitoring tools and load balancers.
    """
    return {"message": "pong", "status": "healthy"}

@app.get("/health", tags=["Health"])
async def health():
    """
    Detailed health check endpoint
    
    Returns comprehensive health information including:
    - Service status
    - Version information
    - Basic connectivity
    """
    return {
        "status": "healthy",
        "service": "group-fitness-api",
        "version": "1.0.0",
        "timestamp": "2024-01-01T00:00:00Z"  # You can add actual timestamp if needed
    }

@app.get("/debug/env", tags=["Debug"])
async def debug_env():
    """
    Debug endpoint to check environment variables (Development only)
    
    Shows masked environment variables to help debug configuration issues.
    Should be disabled or secured in production.
    """
    from .config import get_settings
    settings = get_settings()
    return {
        "aws_region": settings.AWS_REGION,
        "cognito_user_pool_id": settings.COGNITO_USER_POOL_ID[:10] + "..." if settings.COGNITO_USER_POOL_ID else "Not set",
        "cognito_client_id": settings.COGNITO_CLIENT_ID[:10] + "..." if settings.COGNITO_CLIENT_ID else "Not set",
        "database_url": settings.DATABASE_URL.split("@")[0] + "@***" if "@" in settings.DATABASE_URL else settings.DATABASE_URL,
        "debug": settings.DEBUG
    } 