from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Database session
SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit=False
)

# base class for database models
class Base(DeclarativeBase):
    pass

# Database session dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()