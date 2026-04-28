"""
Tests unitarios para las entidades del dominio.

Verifica validaciones, reglas de negocio y comportamiento de las entidades.
"""
from datetime import datetime

import pytest

from src.domain.entities import ChatContext, ChatMessage, Product


class TestProduct:
    """Tests para la entidad Product."""

    def test_create_valid_product(self) -> None:
        """Test que un producto válido se crea correctamente."""
        product = Product(
            id=1,
            name="Test Shoe",
            brand="Nike",
            category="Running",
            size="42",
            color="Black",
            price=100.0,
            stock=10,
            description="Test",
        )

        assert product.name == "Test Shoe"
        assert product.price == 100.0
        assert product.stock == 10

    def test_product_price_zero_raises_error(self) -> None:
        """Test que price=0 lanza ValueError."""
        with pytest.raises(ValueError, match="price must be greater than 0"):
            Product(
                id=1,
                name="Test",
                brand="Nike",
                category="Running",
                size="42",
                color="Black",
                price=0,
                stock=10,
                description="Test",
            )

    def test_product_negative_price_raises_error(self) -> None:
        """Test que price negativo lanza ValueError."""
        with pytest.raises(ValueError, match="price must be greater than 0"):
            Product(
                id=1,
                name="Test",
                brand="Nike",
                category="Running",
                size="42",
                color="Black",
                price=-10,
                stock=10,
                description="Test",
            )

    def test_product_negative_stock_raises_error(self) -> None:
        """Test que stock negativo lanza ValueError."""
        with pytest.raises(ValueError, match="stock cannot be negative"):
            Product(
                id=1,
                name="Test",
                brand="Nike",
                category="Running",
                size="42",
                color="Black",
                price=100,
                stock=-5,
                description="Test",
            )

    def test_product_empty_name_raises_error(self) -> None:
        """Test que name vacío lanza ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Product(
                id=1,
                name="",
                brand="Nike",
                category="Running",
                size="42",
                color="Black",
                price=100,
                stock=10,
                description="Test",
            )

    def test_product_whitespace_name_raises_error(self) -> None:
        """Test que name con solo espacios lanza ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            Product(
                id=1,
                name="   ",
                brand="Nike",
                category="Running",
                size="42",
                color="Black",
                price=100,
                stock=10,
                description="Test",
            )

    def test_is_available_returns_true_when_stock_positive(self) -> None:
        """Test que is_available retorna True cuando stock > 0."""
        product = Product(
            id=1,
            name="Test",
            brand="Nike",
            category="Running",
            size="42",
            color="Black",
            price=100,
            stock=5,
            description="Test",
        )

        assert product.is_available() is True

    def test_is_available_returns_false_when_stock_zero(self) -> None:
        """Test que is_available retorna False cuando stock = 0."""
        product = Product(
            id=1,
            name="Test",
            brand="Nike",
            category="Running",
            size="42",
            color="Black",
            price=100,
            stock=0,
            description="Test",
        )

        assert product.is_available() is False

    def test_reduce_stock_happy_path(self) -> None:
        """Test que reduce_stock funciona correctamente."""
        product = Product(
            id=1,
            name="Test",
            brand="Nike",
            category="Running",
            size="42",
            color="Black",
            price=100,
            stock=10,
            description="Test",
        )

        product.reduce_stock(3)
        assert product.stock == 7

    def test_reduce_stock_insufficient_raises_error(self) -> None:
        """Test que reduce_stock con cantidad > stock lanza ValueError."""
        product = Product(
            id=1,
            name="Test",
            brand="Nike",
            category="Running",
            size="42",
            color="Black",
            price=100,
            stock=5,
            description="Test",
        )

        with pytest.raises(ValueError, match="Insufficient stock"):
            product.reduce_stock(10)

    def test_reduce_stock_negative_quantity_raises_error(self) -> None:
        """Test que reduce_stock con cantidad negativa lanza ValueError."""
        product = Product(
            id=1,
            name="Test",
            brand="Nike",
            category="Running",
            size="42",
            color="Black",
            price=100,
            stock=10,
            description="Test",
        )

        with pytest.raises(ValueError, match="Quantity to reduce must be positive"):
            product.reduce_stock(-5)

    def test_increase_stock_happy_path(self) -> None:
        """Test que increase_stock funciona correctamente."""
        product = Product(
            id=1,
            name="Test",
            brand="Nike",
            category="Running",
            size="42",
            color="Black",
            price=100,
            stock=10,
            description="Test",
        )

        product.increase_stock(5)
        assert product.stock == 15

    def test_increase_stock_negative_quantity_raises_error(self) -> None:
        """Test que increase_stock con cantidad negativa lanza ValueError."""
        product = Product(
            id=1,
            name="Test",
            brand="Nike",
            category="Running",
            size="42",
            color="Black",
            price=100,
            stock=10,
            description="Test",
        )

        with pytest.raises(ValueError, match="Quantity to increase must be positive"):
            product.increase_stock(-3)


class TestChatMessage:
    """Tests para la entidad ChatMessage."""

    def test_create_valid_chat_message(self) -> None:
        """Test que un mensaje válido se crea correctamente."""
        msg = ChatMessage(
            id=1,
            session_id="session123",
            role="user",
            message="Hello",
            timestamp=datetime.utcnow(),
        )

        assert msg.session_id == "session123"
        assert msg.role == "user"
        assert msg.message == "Hello"

    def test_invalid_role_raises_error(self) -> None:
        """Test que role inválido lanza ValueError."""
        with pytest.raises(ValueError, match="Role must be 'user' or 'assistant'"):
            ChatMessage(
                id=1,
                session_id="session123",
                role="invalid",
                message="Hello",
                timestamp=datetime.utcnow(),
            )

    def test_empty_message_raises_error(self) -> None:
        """Test que message vacío lanza ValueError."""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            ChatMessage(
                id=1,
                session_id="session123",
                role="user",
                message="",
                timestamp=datetime.utcnow(),
            )

    def test_empty_session_id_raises_error(self) -> None:
        """Test que session_id vacío lanza ValueError."""
        with pytest.raises(ValueError, match="Session ID cannot be empty"):
            ChatMessage(
                id=1,
                session_id="",
                role="user",
                message="Hello",
                timestamp=datetime.utcnow(),
            )

    def test_is_from_user_returns_true_for_user_role(self) -> None:
        """Test que is_from_user retorna True para role='user'."""
        msg = ChatMessage(
            id=1,
            session_id="session123",
            role="user",
            message="Hello",
            timestamp=datetime.utcnow(),
        )

        assert msg.is_from_user() is True
        assert msg.is_from_assistant() is False

    def test_is_from_assistant_returns_true_for_assistant_role(self) -> None:
        """Test que is_from_assistant retorna True para role='assistant'."""
        msg = ChatMessage(
            id=1,
            session_id="session123",
            role="assistant",
            message="Hello",
            timestamp=datetime.utcnow(),
        )

        assert msg.is_from_assistant() is True
        assert msg.is_from_user() is False


class TestChatContext:
    """Tests para la entidad ChatContext."""

    def test_get_recent_messages_returns_all_when_less_than_max(self) -> None:
        """Test que get_recent_messages retorna todos si hay menos que max_messages."""
        messages = [
            ChatMessage(None, "s1", "user", "msg1", datetime.utcnow()),
            ChatMessage(None, "s1", "assistant", "msg2", datetime.utcnow()),
            ChatMessage(None, "s1", "user", "msg3", datetime.utcnow()),
        ]

        context = ChatContext(messages=messages, max_messages=6)
        recent = context.get_recent_messages()

        assert len(recent) == 3
        assert recent == messages

    def test_get_recent_messages_limits_to_max(self) -> None:
        """Test que get_recent_messages limita a max_messages."""
        messages = [
            ChatMessage(None, "s1", "user", f"msg{i}", datetime.utcnow())
            for i in range(10)
        ]

        context = ChatContext(messages=messages, max_messages=6)
        recent = context.get_recent_messages()

        assert len(recent) == 6
        assert recent[0].message == "msg4"
        assert recent[-1].message == "msg9"

    def test_format_for_prompt_produces_expected_string(self) -> None:
        """Test que format_for_prompt produce el formato correcto."""
        messages = [
            ChatMessage(None, "s1", "user", "Hola", datetime.utcnow()),
            ChatMessage(None, "s1", "assistant", "¿En qué puedo ayudarte?", datetime.utcnow()),
            ChatMessage(None, "s1", "user", "Busco zapatos", datetime.utcnow()),
        ]

        context = ChatContext(messages=messages, max_messages=6)
        formatted = context.format_for_prompt()

        expected = "Usuario: Hola\nAsistente: ¿En qué puedo ayudarte?\nUsuario: Busco zapatos"
        assert formatted == expected

    def test_format_for_prompt_empty_context(self) -> None:
        """Test que format_for_prompt maneja contexto vacío."""
        context = ChatContext(messages=[], max_messages=6)
        formatted = context.format_for_prompt()

        assert formatted == ""
