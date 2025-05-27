from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:12345678@localhost/weatherdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
 