# One-time run to create tables
from models import Base
from database import engine

Base.metadata.create_all(bind=engine)
