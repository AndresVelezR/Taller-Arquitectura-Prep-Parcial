"""
Aplicación FastAPI principal.

Define endpoints HTTP para productos, chat y health check.
"""
from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.application.chat_service import ChatService
from src.application.dtos import (
    ChatHistoryDTO,
    ChatMessageRequestDTO,
    ChatMessageResponseDTO,
    ProductDTO,
)
from src.application.product_service import ProductService
from src.infrastructure.db.database import get_db, init_db
from src.infrastructure.db.init_data import load_initial_data
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.repositories.product_repository import SQLProductRepository

app = FastAPI(
    title="E-commerce Chat AI",
    description="API REST de e-commerce de zapatos con chat inteligente",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Fix 2da vuelta: @app.on_event("startup") está deprecado en FastAPI reciente,
# pero la guía del taller lo pide explícitamente
@app.on_event("startup")
def startup_event() -> None:
    """
    Evento que se ejecuta al iniciar la aplicación.

    Inicializa la base de datos y carga datos iniciales.
    """
    init_db()
    load_initial_data()


@app.get("/")
def read_root():
    """
    Endpoint raíz con información básica de la API.

    Returns:
        Información de la API, versión y endpoints disponibles.
    """
    return {
        "name": "E-commerce Chat AI",
        "version": "1.0.0",
        "description": "API REST de e-commerce de zapatos con chat inteligente",
        "endpoints": {
            "products": "/products",
            "product_by_id": "/products/{id}",
            "chat": "/chat",
            "chat_history": "/chat/history/{session_id}",
            "health": "/health",
            "docs": "/docs",
        },
    }


@app.get("/products", response_model=List[ProductDTO])
def get_products(db: Session = Depends(get_db)):
    """
    Obtiene la lista completa de productos disponibles.

    Args:
        db: Sesión de base de datos inyectada por FastAPI.

    Returns:
        Lista de productos con toda su información.
    """
    repo = SQLProductRepository(db)
    service = ProductService(repo)
    return service.get_all_products()


@app.get("/products/{product_id}", response_model=ProductDTO)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un producto por su ID.

    Args:
        product_id: ID del producto a buscar.
        db: Sesión de base de datos inyectada por FastAPI.

    Returns:
        Producto encontrado.

    Raises:
        HTTPException: 404 si el producto no existe.
    """
    repo = SQLProductRepository(db)
    service = ProductService(repo)

    try:
        return service.get_product_by_id(product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/chat", response_model=ChatMessageResponseDTO)
async def chat(request: ChatMessageRequestDTO, db: Session = Depends(get_db)):
    """
    Procesa un mensaje de chat y retorna respuesta del asistente IA.

    Args:
        request: Mensaje del usuario con session_id.
        db: Sesión de base de datos inyectada por FastAPI.

    Returns:
        Respuesta generada por la IA con timestamp.

    Raises:
        HTTPException: 500 si hay un error procesando el mensaje.
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()

    service = ChatService(product_repo, chat_repo, ai_service)

    try:
        return await service.process_message(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}",
        )


@app.get("/chat/history/{session_id}", response_model=List[ChatHistoryDTO])
def get_chat_history(
    session_id: str,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Obtiene el historial de mensajes de una sesión.

    Args:
        session_id: Identificador de la sesión.
        limit: Número máximo de mensajes a retornar (default: 10).
        db: Sesión de base de datos inyectada por FastAPI.

    Returns:
        Lista de mensajes del historial.
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()

    service = ChatService(product_repo, chat_repo, ai_service)
    return service.get_session_history(session_id, limit)


@app.delete("/chat/history/{session_id}")
def delete_chat_history(session_id: str, db: Session = Depends(get_db)):
    """
    Elimina todo el historial de una sesión.

    Args:
        session_id: Identificador de la sesión a limpiar.
        db: Sesión de base de datos inyectada por FastAPI.

    Returns:
        Cantidad de mensajes eliminados.
    """
    product_repo = SQLProductRepository(db)
    chat_repo = SQLChatRepository(db)
    ai_service = GeminiService()

    service = ChatService(product_repo, chat_repo, ai_service)
    deleted_count = service.clear_session_history(session_id)

    return {"deleted": deleted_count, "session_id": session_id}


@app.get("/health")
def health_check():
    """
    Health check endpoint para verificar que la API está funcionando.

    Returns:
        Status ok y timestamp actual.
    """
    return {
        "status": "ok",
        # Fix 2da vuelta: datetime.utcnow() está deprecado en Python 3.12+,
        # pero la guía del taller lo pide explícitamente
        "timestamp": datetime.utcnow().isoformat(),
    }
