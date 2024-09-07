from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.POSTGRES_DATABASE_URI)
Session = sessionmaker(bind=engine)
session_singleton = Session()
