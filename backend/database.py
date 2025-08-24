from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration for production (Cloud SQL) vs development (SQLite)
def get_database_url():
    """Get database URL based on environment"""
    environment = os.getenv("ENVIRONMENT", "development")
    
    # Check if DATABASE_URL is provided (Cloud Run deployment)
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    
    if environment == "production":
        # Production: Cloud SQL PostgreSQL
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "founder_sourcing_agent")
        db_user = os.getenv("DB_USER", "founder_app")
        db_password = os.getenv("DB_PASSWORD")
        
        if not all([db_host, db_user, db_password]):
            raise ValueError("Missing required database environment variables for production")
        
        return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        # Development: SQLite
        return os.getenv("DATABASE_URL", "sqlite:///./founder_sourcing.db")

# Get database URL
SQLALCHEMY_DATABASE_URL = get_database_url()

# Create engine with appropriate configuration
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for development
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL configuration for production
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
