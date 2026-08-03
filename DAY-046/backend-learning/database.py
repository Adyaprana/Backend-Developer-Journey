from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def ensure_schema():
    """
    Apply lightweight dev migrations that create_all() cannot handle.
    create_all() creates new tables but never alters existing ones.
    """
    inspector = inspect(engine)

    if not inspector.has_table("users"):
        return

    columns = {col["name"] for col in inspector.get_columns("users")}

    if "hashed_password" not in columns:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "ALTER TABLE users "
                    "ADD COLUMN hashed_password VARCHAR NOT NULL DEFAULT ''"
                )
            )


def get_db():
    """Provide a database session for each request."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
