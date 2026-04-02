from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_NAME = "google_play_store.db"
DATABASE_URL = f"sqlite:///{os.path.abspath(DB_NAME)}"

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(bind=engine)
session = Session()