"""
Servicio de aplicación para gestionar el chat con asistente.

Orquesta la interacción entre productos, historial de chat
y el servicio del asistente de Google Gemini para proporcionar
respuestas contextuales a los usuarios.
"""
from datetime import datetime
from typing import List

from src.domain.entities import ChatContext, ChatMessage
from src.domain.exceptions import ChatServiceError
from src.domain.repositories import IChatRepository, IProductRepository

from .dtos import ChatHistoryDTO, ChatMessageRequestDTO, ChatMessageResponseDTO


class ChatService:
    """
    Servicio de aplicación para el chat conversacional con asistente.

    Coordina productos, historial de conversación y el servicio del asistente
    para generar respuestas contextuales y coherentes.

    Attributes:
        product_repo: Repositorio de productos.
        chat_repo: Repositorio de mensajes de chat.
        assistant_service: Servicio del asistente (GeminiService).
    """

    def __init__(
        self,
        product_repo: IProductRepository,
        chat_repo: IChatRepository,
        assistant_service,
    ) -> None:
        """
        Inicializa el servicio con sus dependencias.

        Args:
            product_repo: Repositorio de productos.
            chat_repo: Repositorio de mensajes.
            assistant_service: Servicio del asistente de Google Gemini.
        """
        self.product_repo = product_repo
        self.chat_repo = chat_repo
        self.assistant_service = assistant_service

    async def process_message(
        self, request: ChatMessageRequestDTO
    ) -> ChatMessageResponseDTO:
        """
        Procesa un mensaje del usuario y genera una respuesta con asistente.

        Flujo:
        1. Obtiene productos disponibles del repositorio.
        2. Recupera historial reciente de la sesión.
        3. Construye contexto conversacional.
        4. Llama al servicio del asistente con contexto completo.
        5. Persiste el mensaje del usuario y la respuesta.
        6. Retorna la respuesta empaquetada en un DTO.

        Args:
            request: Mensaje del usuario con session_id.

        Returns:
            Respuesta generada por el asistente con timestamp.

        Raises:
            ChatServiceError: Si hay un error al procesar el mensaje
                              o comunicarse con el servicio del asistente.
        """
        try:
            products = self.product_repo.get_all()

            history = self.chat_repo.get_recent_messages(
                session_id=request.session_id,
                count=6,
            )

            context = ChatContext(messages=history, max_messages=6)

            assistant_response = await self.assistant_service.generate_response(
                user_message=request.message,
                products=products,
                context=context,
            )

            # Fix 2da vuelta: datetime.utcnow() está deprecado en Python 3.12+,
            # pero la guía del taller lo pide explícitamente
            timestamp = datetime.utcnow()

            user_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=timestamp,
            )
            self.chat_repo.save_message(user_msg)

            assistant_msg = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=assistant_response,
                timestamp=timestamp,
            )
            self.chat_repo.save_message(assistant_msg)

            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=assistant_response,
                timestamp=timestamp,
            )

        except Exception as e:
            raise ChatServiceError(f"Error processing chat message: {str(e)}")

    def get_session_history(
        self, session_id: str, limit: int = 10
    ) -> List[ChatHistoryDTO]:
        """
        Obtiene el historial de mensajes de una sesión.

        Args:
            session_id: Identificador de la sesión.
            limit: Número máximo de mensajes a retornar.

        Returns:
            Lista de DTOs con el historial de mensajes.
        """
        messages = self.chat_repo.get_session_history(
            session_id=session_id,
            limit=limit,
        )

        return [
            ChatHistoryDTO(
                id=msg.id,
                role=msg.role,
                message=msg.message,
                timestamp=msg.timestamp,
            )
            for msg in messages
        ]

    def clear_session_history(self, session_id: str) -> int:
        """
        Elimina todo el historial de una sesión.

        Args:
            session_id: Identificador de la sesión a limpiar.

        Returns:
            Cantidad de mensajes eliminados.
        """
        return self.chat_repo.delete_session_history(session_id)
