"""
Entidades del dominio que representan conceptos de negocio del e-commerce.

Este módulo contiene la lógica de negocio pura, independiente de frameworks
y bases de datos.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    """
    Entidad que representa un producto (zapato) en el e-commerce.

    Contiene la lógica de negocio relacionada con productos, incluyendo
    validaciones de precio, stock y disponibilidad.

    Attributes:
        id: Identificador único del producto (None si aún no está persistido)
        name: Nombre del producto
        brand: Marca (Nike, Adidas, Puma, etc.)
        category: Categoría (Running, Casual, Formal)
        size: Talla del zapato
        color: Color del producto
        price: Precio en dólares, debe ser mayor a 0
        stock: Cantidad disponible en inventario, no puede ser negativo
        description: Descripción detallada del producto
    """

    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self) -> None:
        """
        Valida las reglas de negocio del producto después de la inicialización.

        Raises:
            ValueError: Si price <= 0, stock < 0, o name está vacío.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty")

        if self.price <= 0:
            raise ValueError("Product price must be greater than 0")

        if self.stock < 0:
            raise ValueError("Product stock cannot be negative")

    def is_available(self) -> bool:
        """
        Verifica si el producto tiene stock disponible para venta.

        Returns:
            True si stock > 0, False en caso contrario.
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto en la cantidad especificada.

        Args:
            quantity: Cantidad a reducir del stock. Debe ser positivo.

        Raises:
            ValueError: Si quantity es negativo o mayor al stock disponible.

        Example:
            >>> product = Product(id=1, name="Zapato", brand="Nike",
            ...                   category="Running", size="42", color="Negro",
            ...                   price=100, stock=10, description="...")
            >>> product.reduce_stock(3)
            >>> print(product.stock)
            7
        """
        if quantity <= 0:
            raise ValueError("Quantity to reduce must be positive")

        if quantity > self.stock:
            raise ValueError(
                f"Insufficient stock. Available: {self.stock}, requested: {quantity}"
            )

        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto en la cantidad especificada.

        Args:
            quantity: Cantidad a agregar al stock. Debe ser positivo.

        Raises:
            ValueError: Si quantity es negativo o cero.
        """
        if quantity <= 0:
            raise ValueError("Quantity to increase must be positive")

        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en la conversación del chat.

    Permite distinguir entre mensajes del usuario y respuestas del asistente
    de IA para mantener el historial conversacional.

    Attributes:
        id: Identificador único del mensaje (None si aún no está persistido)
        session_id: Identificador de la sesión de conversación
        role: Rol del emisor ('user' o 'assistant')
        message: Contenido del mensaje
        timestamp: Marca de tiempo de creación del mensaje
    """

    id: Optional[int]
    session_id: str
    role: str
    message: str
    timestamp: datetime

    def __post_init__(self) -> None:
        """
        Valida las reglas de negocio del mensaje después de la inicialización.

        Raises:
            ValueError: Si role no es 'user' o 'assistant', o si message/session_id están vacíos.
        """
        if not self.session_id or not self.session_id.strip():
            raise ValueError("Session ID cannot be empty")

        if not self.message or not self.message.strip():
            raise ValueError("Message cannot be empty")

        if self.role not in ("user", "assistant"):
            raise ValueError("Role must be 'user' or 'assistant'")

    def is_from_user(self) -> bool:
        """
        Verifica si el mensaje proviene del usuario.

        Returns:
            True si el mensaje es del usuario, False si es del asistente.
        """
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """
        Verifica si el mensaje proviene del asistente de IA.

        Returns:
            True si el mensaje es del asistente, False si es del usuario.
        """
        return self.role == "assistant"


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.

    Mantiene los mensajes recientes para dar coherencia al chat y permitir
    que la IA tenga "memoria" de la conversación anterior.

    Attributes:
        messages: Lista de mensajes de la conversación
        max_messages: Número máximo de mensajes recientes a mantener (default: 6)
    """

    messages: list[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> list[ChatMessage]:
        """
        Retorna los últimos N mensajes según max_messages.

        Returns:
            Lista con los últimos max_messages mensajes, o todos si hay menos.
        """
        return self.messages[-self.max_messages:]

    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes recientes para incluirlos en el prompt de IA.

        Returns:
            String formateado con el historial, una línea por mensaje.
            Formato: "Usuario: <mensaje>\\nAsistente: <respuesta>\\n..."

        Example:
            >>> ctx = ChatContext([
            ...     ChatMessage(None, "s1", "user", "Hola", datetime.now()),
            ...     ChatMessage(None, "s1", "assistant", "¿Cómo puedo ayudarte?", datetime.now())
            ... ])
            >>> print(ctx.format_for_prompt())
            Usuario: Hola
            Asistente: ¿Cómo puedo ayudarte?
        """
        recent = self.get_recent_messages()
        lines = []

        for msg in recent:
            role_label = "Usuario" if msg.is_from_user() else "Asistente"
            lines.append(f"{role_label}: {msg.message}")

        return "\n".join(lines)
