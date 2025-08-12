"""
Configuration Management for Group Fitness API

This module handles all environment variables and application settings.
It uses pydantic for validation and caching for performance.

Environment Variables:
- AWS_REGION: AWS region for Cognito and other services
- COGNITO_USER_POOL_ID: AWS Cognito User Pool ID
- COGNITO_CLIENT_ID: AWS Cognito App Client ID
- DATABASE_URL: PostgreSQL connection string
- REDIS_URL: Redis connection string
- S3_*: S3/MinIO configuration for file storage
"""

import os
from functools import lru_cache
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
# This allows us to use the same configuration locally and in production
load_dotenv()

class Settings:
    # AWS Cognito Configuration
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    COGNITO_USER_POOL_ID: str = os.getenv("COGNITO_USER_POOL_ID", "")
    COGNITO_CLIENT_ID: str = os.getenv("COGNITO_CLIENT_ID", "")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://dev_user:dev_password@localhost:5432/group_fitness_dev")
    
    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # S3/MinIO Configuration
    S3_ENDPOINT: str = os.getenv("S3_ENDPOINT", "http://localhost:9000")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "minioadmin")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY", "minioadmin")
    S3_BUCKET: str = os.getenv("S3_BUCKET", "group-fitness-dev")
    
    # JWT Configuration (for development fallback)
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

@lru_cache()
def get_settings() -> Settings:
    return Settings() 