"""
DTOs (Data Transfer Objects) para transferir datos entre capas.

Usa Pydantic v2 para validación automática de tipos y reglas de negocio.
Los DTOs desacoplan las entidades del dominio de las representaciones HTTP.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator


class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos entre capas.

    Pydantic valida automáticamente los tipos y ejecuta
    validadores personalizados antes de crear la instancia.

    Attributes:
        id: Identificador único (None para productos nuevos)
        name: Nombre del producto
        brand: Marca
        category: Categoría
        size: Talla
        color: Color
        price: Precio en dólares
        stock: Cantidad disponible
        description: Descripción detallada
    """

    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    # Fix 2da vuelta: @validator está deprecado en Pydantic v2, usamos field_validator
    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        """
        Valida que el precio sea mayor a 0.

        Args:
            v: Valor del precio a validar.

        Returns:
            El precio validado.

        Raises:
            ValueError: Si el precio es 0 o negativo.
        """
        if v <= 0:
            raise ValueError("price must be greater than 0")
        return v

    @field_validator("stock")
    @classmethod
    def stock_must_be_non_negative(cls, v: int) -> int:
        """
        Valida que el stock no sea negativo.

        Args:
            v: Valor del stock a validar.

        Returns:
            El stock validado.

        Raises:
            ValueError: Si el stock es negativo.
        """
        if v < 0:
            raise ValueError("stock cannot be negative")
        return v

    class Config:
        """Configuración de Pydantic para este DTO."""

        from_attributes = True


class ChatMessageRequestDTO(BaseModel):
    """
    DTO para recibir mensajes del usuario en el endpoint de chat.

    Attributes:
        session_id: Identificador de la sesión de conversación
        message: Mensaje del usuario
    """

    session_id: str
    message: str

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        """
        Valida que el mensaje no esté vacío.

        Args:
            v: Mensaje a validar.

        Returns:
            El mensaje validado.

        Raises:
            ValueError: Si el mensaje está vacío o solo contiene espacios.
        """
        if not v or not v.strip():
            raise ValueError("message cannot be empty")
        return v

    @field_validator("session_id")
    @classmethod
    def session_id_not_empty(cls, v: str) -> str:
        """
        Valida que el session_id no esté vacío.

        Args:
            v: Session ID a validar.

        Returns:
            El session_id validado.

        Raises:
            ValueError: Si el session_id está vacío o solo contiene espacios.
        """
        if not v or not v.strip():
            raise ValueError("session_id cannot be empty")
        return v


class ChatMessageResponseDTO(BaseModel):
    """
    DTO para enviar respuestas del chat al cliente.

    Attributes:
        session_id: Identificador de la sesión
        user_message: Mensaje original del usuario
        assistant_message: Respuesta generada por la IA
        timestamp: Marca de tiempo de la respuesta
    """

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """
    DTO para mostrar el historial de mensajes de una sesión.

    Attributes:
        id: Identificador del mensaje
        role: Rol del emisor ('user' o 'assistant')
        message: Contenido del mensaje
        timestamp: Marca de tiempo del mensaje
    """

    id: int
    role: str
    message: str
    timestamp: datetime

    class Config:
        """Configuración de Pydantic para este DTO."""

        from_attributes = True
