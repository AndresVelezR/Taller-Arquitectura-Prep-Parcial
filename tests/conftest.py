"""
Configuración compartida de pytest.

Define fixtures reutilizables para los tests.
"""
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.domain.entities import ChatMessage, Product


@pytest.fixture
def sample_product() -> Product:
    """
    Fixture que retorna un producto de ejemplo válido.

    Returns:
        Product: Producto con datos de prueba.
    """
    return Product(
        id=1,
        name="Test Shoe",
        brand="Nike",
        category="Running",
        size="42",
        color="Black",
        price=100.0,
        stock=10,
        description="Test description",
    )


@pytest.fixture
def sample_chat_message() -> ChatMessage:
    """
    Fixture que retorna un mensaje de chat de ejemplo.

    Returns:
        ChatMessage: Mensaje del usuario con datos de prueba.
    """
    return ChatMessage(
        id=1,
        session_id="test_session",
        role="user",
        message="Test message",
        timestamp=datetime.utcnow(),
    )


@pytest.fixture
def mock_product_repository() -> MagicMock:
    """
    Fixture que retorna un mock del repositorio de productos.

    Returns:
        MagicMock: Mock de IProductRepository.
    """
    return MagicMock()


@pytest.fixture
def mock_chat_repository() -> MagicMock:
    """
    Fixture que retorna un mock del repositorio de chat.

    Returns:
        MagicMock: Mock de IChatRepository.
    """
    return MagicMock()


@pytest.fixture
def mock_assistant_service() -> MagicMock:
    """
    Fixture que retorna un mock del servicio del asistente.

    Returns:
        MagicMock: Mock de GeminiService.
    """
    return MagicMock()
