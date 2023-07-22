from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'sqlite:///F:/semester7/FYP_Project/Database/fyp2.db'

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database object
database = Database(DATABASE_URL)