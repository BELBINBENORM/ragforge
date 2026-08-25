from sqlalchemy import text

from app.database.connection import engine
from app.database.models import Base


def initialize_database():

    with engine.begin() as connection:

        connection.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector")
        )

    Base.metadata.create_all(
        bind=engine
    )


if __name__ == "__main__":
    initialize_database()

    print(
        "Database tables and pgvector extension initialized."
    )