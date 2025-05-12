import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/fastapi_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
