"""
Project Lazarus Configuration
Centralized configuration management for the vital streaming API
Architectural Choice: Using Pydantic Settings for type-safe env var loading
with explicit validation for production deployment safety.
"""

import os
from typing import Dict, List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field, validator
import logging

class Settings(BaseSettings):
    """Main application settings with validation"""
    
    # API Configuration
    api_title: str = "Project Lazarus Feed API"
    api_version: str = "1.3.0"
    api_description: str = "Live System Vitals & Adversarial Chaos Training Telemetry"
    api_port: int = Field(default=8000, ge=1024, le=65535)
    api_host: str = "0.0.0.0"
    api_debug: bool = False
    
    # Security
    secret_key: str = Field(default=os.getenv("SECRET_KEY", "dev-secret-replace-in-production"))
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    rate_limit_per_minute: int = 60
    
    # Firebase Configuration (CRITICAL - Ecosystem Standard)
    firebase_project_id: str = Field(..., description="Firebase Project ID")
    firebase_private_key: str = Field(..., description="Firebase Service Account Private Key")
    firebase_client_email: str = Field(..., description="Firebase Service Account Client Email")
    
    # Tier Configuration
    tier_configs: Dict[str, Dict] = {
        "base": {
            "sample_rate_seconds": 5,
            "data_retention_days": 7,
            "max_connections": 3,
            "anonymized": True
        },
        "premium": {
            "sample_rate_seconds": 1,
            "data_retention_days": 30,
            "max_connections": 10,
            "anonymized": False,
            "raw_logs": True,
            "chaos_training_cert": True
        }
    }
    
    # Data Collection
    hive_mind_version: str = "HiveMind Ontario v1.3"
    collection_intervals: Dict[str, int] = {
        "cpu": 2,
        "memory": 3,
        "emotional": 5,
        "strategy": 10
    }
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "JSON"
    
    @validator('firebase_private_key')
    def validate_private_key(cls, v):
        """Ensure Firebase key is properly formatted"""
        if not v:
            raise ValueError("Firebase private key is required")
        if "-----BEGIN PRIVATE KEY-----" not in v:
            raise ValueError("Invalid Firebase private key format")
        return v.replace('\\n', '\n')
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        """Ensure production secret key is strong"""
        if v == "dev-secret-replace-in-production" and os.getenv("ENVIRONMENT") == "production":
            raise ValueError("Must set SECRET_KEY in production")
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "forbid"  # Prevent extra fields for security

# Global settings instance
settings = Settings()

# Initialize logging configuration
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)