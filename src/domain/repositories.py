"""
Interfaces (contratos) de repositorios del dominio.

Define CÓMO acceder a los datos sin especificar la implementación.
Esto permite que el dominio sea independiente de la base de datos
(Clean Architecture - Dependency Inversion).
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import ChatMessage, Product


class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.

    Las implementaciones concretas (SQLAlchemy, MongoDB, etc.)
    estarán en la capa de infraestructura.
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Obtiene todos los productos del repositorio.

        Returns:
            Lista de todos los productos, vacía si no hay ninguno.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Busca un producto por su identificador único.

        Args:
            product_id: ID del producto a buscar.

        Returns:
            El producto encontrado, o None si no existe.
        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """
        Obtiene productos de una marca específica.

        Args:
            brand: Nombre de la marca a filtrar (ej: "Nike", "Adidas").

        Returns:
            Lista de productos de esa marca, vacía si no hay coincidencias.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """
        Obtiene productos de una categoría específica.

        Args:
            category: Categoría a filtrar (ej: "Running", "Casual", "Formal").

        Returns:
            Lista de productos de esa categoría, vacía si no hay coincidencias.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto en el repositorio.

        Si el producto tiene ID, actualiza el existente.
        Si no tiene ID (es None), crea uno nuevo y asigna ID.

        Args:
            product: Producto a guardar.

        Returns:
            El producto guardado con su ID asignado.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto del repositorio por su ID.

        Args:
            product_id: ID del producto a eliminar.

        Returns:
            True si se eliminó exitosamente, False si no existía.
        """
        pass


class IChatRepository(ABC):
    """
    Interface para gestionar el historial de conversaciones del chat.

    Permite guardar y recuperar mensajes para mantener contexto
    conversacional entre diferentes solicitudes del usuario.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en el historial de chat.

        Args:
            message: Mensaje a guardar.

        Returns:
            El mensaje guardado con su ID asignado.
        """
        pass

    @abstractmethod
    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión de conversación.

        Args:
            session_id: Identificador de la sesión.
            limit: Número máximo de mensajes a retornar (None = todos).

        Returns:
            Lista de mensajes en orden cronológico (más antiguos primero).
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión de conversación.

        Args:
            session_id: Identificador de la sesión a limpiar.

        Returns:
            Cantidad de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión.

        Args:
            session_id: Identificador de la sesión.
            count: Número de mensajes recientes a obtener.

        Returns:
            Lista de los últimos N mensajes en orden cronológico.
        """
        pass
