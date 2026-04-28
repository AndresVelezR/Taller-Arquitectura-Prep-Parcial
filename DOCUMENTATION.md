# Documentación del Código

Este proyecto sigue el estilo de docstrings Google en español.

## Verificación de Documentación

Todos los módulos, clases y métodos públicos están documentados:

### ✓ Dominio
- [x] `src/domain/entities.py` - Product, ChatMessage, ChatContext
- [x] `src/domain/repositories.py` - IProductRepository, IChatRepository
- [x] `src/domain/exceptions.py` - Excepciones personalizadas

### ✓ Aplicación
- [x] `src/application/dtos.py` - DTOs con Pydantic v2
- [x] `src/application/product_service.py` - ProductService
- [x] `src/application/chat_service.py` - ChatService

### ✓ Infraestructura
- [x] `src/infrastructure/db/database.py` - Configuración SQLAlchemy
- [x] `src/infrastructure/db/models.py` - Modelos ORM
- [x] `src/infrastructure/db/init_data.py` - Datos iniciales
- [x] `src/infrastructure/repositories/product_repository.py` - SQLProductRepository
- [x] `src/infrastructure/repositories/chat_repository.py` - SQLChatRepository
- [x] `src/infrastructure/llm_providers/gemini_service.py` - GeminiService
- [x] `src/infrastructure/api/main.py` - FastAPI endpoints

### ✓ Tests
- [x] `tests/conftest.py` - Fixtures
- [x] `tests/test_entities.py` - Tests de entidades
- [x] `tests/test_services.py` - Tests de servicios

### ✓ Configuración
- [x] `src/config.py` - Variables de entorno

## Formato de Docstrings

Todos siguen el estilo Google:

```python
def metodo(self, arg1: tipo) -> tipo_retorno:
    """
    Breve descripción de una línea.

    Descripción más detallada si es necesario.
    Puede ocupar múltiples líneas.

    Args:
        arg1: Descripción del argumento.

    Returns:
        Descripción del valor de retorno.

    Raises:
        ExcepcionTipo: Cuándo se lanza.

    Example:
        >>> metodo(valor)
        resultado_esperado
    """
```

## Verificar Documentación

```bash
# Ver docstrings de un módulo
python -m pydoc src.domain.entities

# Ver docs de FastAPI
# Abrir http://localhost:8000/docs después de arrancar la app
```
