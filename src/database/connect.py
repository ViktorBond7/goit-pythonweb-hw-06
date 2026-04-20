
from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
import os


DB_HOST = os.getenv("DB_HOST", "localhost")
url_db = f"postgresql+psycopg://admin:password@{DB_HOST}:5433/education_management_db"

engine = create_engine(url_db, echo=True)

# Session = sessionmaker(bind=engine)

# session = Session()
