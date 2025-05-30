from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cognito_secrets import SecretKeys

# Load secret keys including the PostgreSQL database URL
secret_keys = SecretKeys()

# Create the SQLAlchemy engine using the database URL
engine = create_engine(secret_keys.POSTGRES_DB_URL)

# Create a configured "SessionLocal" class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,    # Don't commit transactions automatically
    autoflush=False,     # Don't autoflush changes automatically
    bind=engine          # Bind this session to the created engine
)

# Dependency function to get a database session
def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db         # Yield the session to the caller (pause here)
    finally:
        db.close()       # After use, close the session to free resources
