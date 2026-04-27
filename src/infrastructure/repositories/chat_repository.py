"""
Implementación del repositorio de chat usando SQLAlchemy.

Gestiona el historial de mensajes de conversación.
"""
from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.domain.entities import ChatMessage
from src.domain.repositories import IChatRepository

from ..db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """
    Implementación SQL del repositorio de chat.

    Usa SQLAlchemy para persistir y recuperar mensajes de chat,
    manteniendo el orden cronológico correcto para el contexto conversacional.

    Attributes:
        db: Sesión de SQLAlchemy para interactuar con la BD.
    """

    def __init__(self, db: Session) -> None:
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db: Sesión de SQLAlchemy activa.
        """
        self.db = db

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje en el historial."""
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión.

        Los mensajes se retornan en orden cronológico (más antiguos primero).
        """
        query = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp)
        )

        if limit:
            query = query.limit(limit)

        models = query.all()
        return [self._model_to_entity(m) for m in models]

    def delete_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.

        Returns:
            Cantidad de mensajes eliminados.
        """
        count = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .delete()
        )
        self.db.commit()
        return count

    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        Obtiene los últimos N mensajes de una sesión en orden cronológico.

        Consulta los más recientes primero (DESC) y luego invierte el resultado
        para retornarlos de más antiguo a más reciente.
        """
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(desc(ChatMemoryModel.timestamp))
            .limit(count)
            .all()
        )
        models.reverse()
        return [self._model_to_entity(m) for m in models]

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """
        Convierte un modelo ORM a entidad de dominio.

        Args:
            model: Modelo ORM de mensaje de chat.

        Returns:
            Entidad de mensaje de chat del dominio.
        """
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """
        Convierte una entidad de dominio a modelo ORM.

        Args:
            entity: Entidad de mensaje de chat del dominio.

        Returns:
            Modelo ORM de mensaje de chat.
        """
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp,
        )
