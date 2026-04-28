"""Configuracion global cargada desde variables de entorno."""
import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/ecommerce_chat.db")
ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
