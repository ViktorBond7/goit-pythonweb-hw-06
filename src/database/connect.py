
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment or use default PostgreSQL
# url_db = "postgresql://admin:password@localhost:5432/education_management_db"
# url_db = "sqlite:///bookshelf.db"

DB_HOST = os.getenv("DB_HOST", "localhost")
url_db = f"postgresql+psycopg://admin:password@{DB_HOST}:5433/education_management_db"



engine = create_engine(url_db, echo=True)
# conn = engine.connect()
Session = sessionmaker(bind=engine)

session = Session()
