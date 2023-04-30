from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"  # Sqlite for local fast deployment
engine = create_engine(SQLALCHEMY_DATABASE_URL)
