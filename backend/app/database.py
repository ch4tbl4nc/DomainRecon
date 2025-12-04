# =============================================================================
# DomainRecon - Configuration Base de Données
# =============================================================================

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://domainrecon_user:domainrecon_secret_2024@localhost:5432/domainrecon_db"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Fournit une session de BDD pour chaque requête."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    db = SessionLocal()
    try:
        yield db  # Fournit la session au endpoint
    finally:
        db.close()  # Ferme toujours la session, même en cas d'erreur
