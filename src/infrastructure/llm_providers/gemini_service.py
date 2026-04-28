"""
Servicio de integración con Google Gemini.

Genera respuestas conversacionales contextuales usando el modelo
de lenguaje Gemini de Google.
"""
import asyncio
from typing import List

import google.generativeai as genai

from src.config import GEMINI_API_KEY
from src.domain.entities import ChatContext, Product


class GeminiService:
    """
    Servicio para interactuar con Google Gemini.

    Genera respuestas contextuales para el chat del e-commerce,
    considerando el inventario de productos y el historial conversacional.

    Attributes:
        model: Modelo generativo de Gemini configurado.
    """

    def __init__(self) -> None:
        """
        Inicializa el servicio configurando el cliente de Gemini.

        Raises:
            ValueError: Si GEMINI_API_KEY no está configurada.
        """
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured in environment")

        # Fix 2da vuelta: SDK 0.8.x requiere configure() antes de usar GenerativeModel
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate_response(
        self,
        user_message: str,
        products: List[Product],
        context: ChatContext,
    ) -> str:
        """
        Genera una respuesta conversacional usando Gemini.

        Args:
            user_message: Mensaje actual del usuario.
            products: Lista de productos disponibles en inventario.
            context: Contexto conversacional con mensajes recientes.

        Returns:
            Respuesta generada por el asistente.

        Raises:
            Exception: Si hay un error en la comunicación con Gemini API.
        """
        # Fix 2da vuelta: SDK 0.8 es síncrono, envolvemos en to_thread para mantener firma async
        return await asyncio.to_thread(
            self._generate_sync,
            user_message,
            products,
            context,
        )

    def _generate_sync(
        self,
        user_message: str,
        products: List[Product],
        context: ChatContext,
    ) -> str:
        """
        Versión síncrona de la generación de respuesta.

        Args:
            user_message: Mensaje del usuario.
            products: Lista de productos disponibles.
            context: Contexto conversacional.

        Returns:
            Respuesta generada por Gemini.
        """
        products_info = self._format_products_info(products)
        history = context.format_for_prompt()

        prompt = f"""Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
{products_info}

INSTRUCCIONES:
- Sé amigable y profesional
- Usa el contexto de la conversación anterior
- Recomienda productos específicos cuando sea apropiado
- Menciona precios, tallas y disponibilidad de stock
- Si un producto no tiene stock (stock=0), menciona que está agotado
- Si no tienes información sobre algo, sé honesto
- Responde en español de manera natural y conversacional

HISTORIAL DE CONVERSACIÓN:
{history}

Usuario: {user_message}

Asistente:"""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")

    def _format_products_info(self, products: List[Product]) -> str:
        """
        Formatea la lista de productos en texto legible para el prompt.

        Args:
            products: Lista de productos a formatear.

        Returns:
            String con productos formateados, uno por línea.

        Example:
            - Air Zoom Pegasus | Nike | $120 | Talla 42 | Stock: 15
            - Ultraboost 23 | Adidas | $180 | Talla 41 | Stock: 8
        """
        if not products:
            return "No hay productos disponibles."

        lines = []
        for p in products:
            stock_info = f"Stock: {p.stock}" if p.stock > 0 else "AGOTADO"
            lines.append(f"- {p.name} | {p.brand} | ${p.price} | Talla {p.size} | {stock_info}")

        return "\n".join(lines)
