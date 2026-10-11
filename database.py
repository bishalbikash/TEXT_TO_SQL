import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from langchain_community.utilities import SQLDatabase


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Database configuration
# --------------------------------------------------

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")


DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# --------------------------------------------------
# SQLAlchemy engine
# --------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# --------------------------------------------------
# LangChain SQLDatabase
# --------------------------------------------------

db = SQLDatabase(
    engine,
    sample_rows_in_table_info=1
)


# --------------------------------------------------
# Test database connection
# --------------------------------------------------

def test_connection():
    """Test the MySQL database connection."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception as e:
        print(f"Database connection failed: {e}")
        return False