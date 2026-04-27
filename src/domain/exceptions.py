"""
Excepciones específicas del dominio.

Representan errores de negocio, no errores técnicos.
Son más descriptivas que excepciones genéricas y permiten
manejo de errores más granular en capas superiores.
"""


class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe en el repositorio.

    Example:
        >>> raise ProductNotFoundError(42)
        ProductNotFoundError: Producto con ID 42 no encontrado
    """

    def __init__(self, product_id: int = None):
        """
        Inicializa la excepción con un mensaje descriptivo.

        Args:
            product_id: ID del producto no encontrado (opcional).
        """
        if product_id:
            self.message = f"Producto con ID {product_id} no encontrado"
        else:
            self.message = "Producto no encontrado"
        super().__init__(self.message)


class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son inválidos.

    Example:
        >>> raise InvalidProductDataError("El precio no puede ser negativo")
        InvalidProductDataError: El precio no puede ser negativo
    """

    def __init__(self, message: str = None):
        """
        Inicializa la excepción con un mensaje personalizado.

        Args:
            message: Descripción del error (opcional).
        """
        if message:
            self.message = message
        else:
            self.message = "Datos de producto inválidos"
        super().__init__(self.message)


class ChatServiceError(Exception):
    """
    Se lanza cuando hay un error en el servicio de chat.

    Example:
        >>> raise ChatServiceError("Falló la conexión con Gemini AI")
        ChatServiceError: Falló la conexión con Gemini AI
    """

    def __init__(self, message: str = None):
        """
        Inicializa la excepción con un mensaje personalizado.

        Args:
            message: Descripción del error (opcional).
        """
        if message:
            self.message = message
        else:
            self.message = "Error en el servicio de chat"
        super().__init__(self.message)
