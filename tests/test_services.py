"""
Tests unitarios para los servicios de aplicación.

Usa mocks para aislar la lógica de los servicios de las dependencias.
"""
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.chat_service import ChatService
from src.application.dtos import ChatMessageRequestDTO, ProductDTO
from src.application.product_service import ProductService
from src.domain.entities import ChatMessage, Product
from src.domain.exceptions import ProductNotFoundError


class TestProductService:
    """Tests para ProductService."""

    def test_get_all_products_returns_list(
        self, mock_product_repository: MagicMock, sample_product: Product
    ) -> None:
        """Test que get_all_products retorna lista de DTOs."""
        mock_product_repository.get_all.return_value = [sample_product]
        service = ProductService(mock_product_repository)

        result = service.get_all_products()

        assert len(result) == 1
        assert isinstance(result[0], ProductDTO)
        assert result[0].name == "Test Shoe"
        mock_product_repository.get_all.assert_called_once()

    def test_get_product_by_id_returns_dto_when_found(
        self, mock_product_repository: MagicMock, sample_product: Product
    ) -> None:
        """Test que get_product_by_id retorna DTO cuando encuentra el producto."""
        mock_product_repository.get_by_id.return_value = sample_product
        service = ProductService(mock_product_repository)

        result = service.get_product_by_id(1)

        assert isinstance(result, ProductDTO)
        assert result.id == 1
        assert result.name == "Test Shoe"
        mock_product_repository.get_by_id.assert_called_once_with(1)

    def test_get_product_by_id_raises_error_when_not_found(
        self, mock_product_repository: MagicMock
    ) -> None:
        """Test que get_product_by_id lanza excepción cuando no encuentra."""
        mock_product_repository.get_by_id.return_value = None
        service = ProductService(mock_product_repository)

        with pytest.raises(ProductNotFoundError):
            service.get_product_by_id(999)

        mock_product_repository.get_by_id.assert_called_once_with(999)

    def test_get_available_products_filters_correctly(
        self, mock_product_repository: MagicMock
    ) -> None:
        """Test que get_available_products filtra productos con stock."""
        available = Product(1, "Available", "Nike", "Running", "42", "Black", 100, 10, "Test")
        out_of_stock = Product(2, "Out", "Nike", "Running", "42", "Black", 100, 0, "Test")

        mock_product_repository.get_all.return_value = [available, out_of_stock]
        service = ProductService(mock_product_repository)

        result = service.get_available_products()

        assert len(result) == 1
        assert result[0].name == "Available"


class TestChatService:
    """Tests para ChatService."""

    @pytest.mark.asyncio
    async def test_process_message_calls_ai_service_with_correct_args(
        self,
        mock_product_repository: MagicMock,
        mock_chat_repository: MagicMock,
        mock_ai_service: MagicMock,
        sample_product: Product,
    ) -> None:
        """Test que process_message llama al servicio de IA con los argumentos correctos."""
        mock_product_repository.get_all.return_value = [sample_product]
        mock_chat_repository.get_recent_messages.return_value = []
        mock_chat_repository.save_message.return_value = ChatMessage(
            1, "test", "user", "test", datetime.utcnow()
        )
        mock_ai_service.generate_response = AsyncMock(return_value="AI response")

        service = ChatService(mock_product_repository, mock_chat_repository, mock_ai_service)
        request = ChatMessageRequestDTO(session_id="test", message="Hola")

        result = await service.process_message(request)

        assert result.assistant_message == "AI response"
        assert result.user_message == "Hola"
        mock_ai_service.generate_response.assert_called_once()
        assert mock_chat_repository.save_message.call_count == 2

    @pytest.mark.asyncio
    async def test_process_message_saves_both_messages(
        self,
        mock_product_repository: MagicMock,
        mock_chat_repository: MagicMock,
        mock_ai_service: MagicMock,
        sample_product: Product,
    ) -> None:
        """Test que process_message guarda mensaje del usuario y del asistente."""
        mock_product_repository.get_all.return_value = [sample_product]
        mock_chat_repository.get_recent_messages.return_value = []
        mock_chat_repository.save_message.return_value = ChatMessage(
            1, "test", "user", "test", datetime.utcnow()
        )
        mock_ai_service.generate_response = AsyncMock(return_value="AI response")

        service = ChatService(mock_product_repository, mock_chat_repository, mock_ai_service)
        request = ChatMessageRequestDTO(session_id="test", message="Hola")

        await service.process_message(request)

        assert mock_chat_repository.save_message.call_count == 2

    def test_get_session_history_returns_list(
        self,
        mock_product_repository: MagicMock,
        mock_chat_repository: MagicMock,
        mock_ai_service: MagicMock,
        sample_chat_message: ChatMessage,
    ) -> None:
        """Test que get_session_history retorna lista de DTOs."""
        mock_chat_repository.get_session_history.return_value = [sample_chat_message]
        service = ChatService(mock_product_repository, mock_chat_repository, mock_ai_service)

        result = service.get_session_history("test", limit=10)

        assert len(result) == 1
        assert result[0].message == "Test message"
        mock_chat_repository.get_session_history.assert_called_once_with(
            session_id="test",
            limit=10,
        )

    def test_clear_session_history_returns_count(
        self,
        mock_product_repository: MagicMock,
        mock_chat_repository: MagicMock,
        mock_ai_service: MagicMock,
    ) -> None:
        """Test que clear_session_history retorna cantidad eliminada."""
        mock_chat_repository.delete_session_history.return_value = 5
        service = ChatService(mock_product_repository, mock_chat_repository, mock_ai_service)

        result = service.clear_session_history("test")

        assert result == 5
        mock_chat_repository.delete_session_history.assert_called_once_with("test")
