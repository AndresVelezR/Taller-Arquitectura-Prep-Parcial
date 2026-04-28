"""
Modelos ORM de SQLAlchemy para mapear tablas de la base de datos.

Estos modelos son la representación técnica de los datos en SQL,
separados de las entidades del dominio.
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text

from .database import Base


class ProductModel(Base):
    """
    Modelo ORM para la tabla de productos.

    Attributes:
        id: Clave primaria autoincremental
        name: Nombre del producto
        brand: Marca del zapato
        category: Categoría (Running, Casual, Formal)
        size: Talla del zapato
        color: Color del producto
        price: Precio en dólares
        stock: Cantidad disponible en inventario
        description: Descripción detallada del producto
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100), index=True)
    category = Column(String(100), index=True)
    size = Column(String(20))
    color = Column(String(50))
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    description = Column(Text)


class ChatMemoryModel(Base):
    """
    Modelo ORM para la tabla de historial de chat.

    Attributes:
        id: Clave primaria autoincremental
        session_id: Identificador de la sesión de conversación
        role: Rol del emisor ('user' o 'assistant')
        message: Contenido del mensaje
        timestamp: Marca de tiempo de creación del mensaje
    """

    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    # Fix 2da vuelta: datetime.utcnow está deprecado en Python 3.12+, guía lo pide explícitamente
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_session_timestamp", "session_id", "timestamp"),
    )
