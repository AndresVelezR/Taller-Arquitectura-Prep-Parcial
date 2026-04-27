"""
Configuración de la base de datos con SQLAlchemy.

Define el motor de conexión, factory de sesiones y clase base
para modelos ORM.
"""
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.config import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para FastAPI que proporciona una sesión de base de datos.

    La sesión se cierra automáticamente al terminar la request,
    incluso si hay una excepción.

    Yields:
        Session: Sesión de SQLAlchemy para interactuar con la BD.

    Example:
        @app.get("/products")
        def get_products(db: Session = Depends(get_db)):
            return db.query(ProductModel).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Inicializa la base de datos creando todas las tablas.

    Crea el directorio data/ si no existe y luego crea las tablas
    definidas en los modelos ORM si no existen.
    """
    os.makedirs("data", exist_ok=True)
    Base.metadata.create_all(bind=engine)
