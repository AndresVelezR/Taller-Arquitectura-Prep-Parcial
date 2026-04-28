# E-commerce con Chat

API REST de e-commerce de zapatos con chat inteligente usando Clean Architecture.

## Descripción

Sistema de e-commerce que permite:
- Consultar productos mediante endpoints REST tradicionales
- Conversar con un asistente (Google Gemini) que ayuda a encontrar zapatos
- El asistente mantiene memoria conversacional para respuestas coherentes

Construido con **Clean Architecture** en 3 capas (Domain, Application, Infrastructure).

## Tecnologías

- **Python 3.11**
- **FastAPI** - Framework web para APIs REST
- **SQLAlchemy** - ORM para interacción con base de datos
- **SQLite** - Base de datos ligera
- **Google Gemini** - Modelo de lenguaje para chat conversacional
- **Pydantic v2** - Validación de datos
- **Docker** - Containerización
- **Pytest** - Testing unitario

## Arquitectura

```
src/
├── domain/           # Entidades, interfaces, excepciones (sin dependencias externas)
├── application/      # DTOs, servicios (casos de uso)
└── infrastructure/   # FastAPI, SQLAlchemy, Gemini, repositorios
```

**Principios:**
- Clean Architecture (3 capas)
- Dependency Injection
- Repository Pattern
- Domain-Driven Design

## Requisitos Previos

- Python 3.11+ (si usas pyenv: `pyenv install 3.11.9 && pyenv local 3.11.9`)
- Docker y Docker Compose
- API Key de Google Gemini ([obtener aquí](https://aistudio.google.com/apikey))

## Instalación

### 1. Clonar repositorio

```bash
git clone <tu-repo>
cd e-commerce-chat
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY
```

Contenido del `.env`:

```
GEMINI_API_KEY=tu_api_key_aqui
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
ENVIRONMENT=development
```

### 5. Ejecutar la aplicación

#### Opción A: Local (con venv)

```bash
uvicorn src.infrastructure.api.main:app --reload
```

#### Opción B: Docker

```bash
docker compose up --build
```

La API estará disponible en: **http://localhost:8000**

## Uso

### Documentación interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints principales

#### Productos

```bash
# Listar todos los productos
curl http://localhost:8000/products

# Obtener producto por ID
curl http://localhost:8000/products/1
```

#### Chat con asistente

```bash
# Enviar mensaje al asistente
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user123",
    "message": "Busco zapatos Nike para correr, talla 42"
  }'

# Obtener historial de conversación
curl http://localhost:8000/chat/history/user123?limit=10

# Limpiar historial
curl -X DELETE http://localhost:8000/chat/history/user123
```

#### Health Check

```bash
curl http://localhost:8000/health
```

### Ejemplos de uso del chat

```bash
# Primera interacción
POST /chat
{
  "session_id": "cliente_001",
  "message": "Hola, busco zapatos para correr"
}

# Respuesta:
{
  "session_id": "cliente_001",
  "user_message": "Hola, busco zapatos para correr",
  "assistant_message": "¡Hola! Tengo varias opciones para running. Te recomiendo...",
  "timestamp": "2024-01-15T10:30:00"
}

# Continuar conversación (el asistente recuerda el contexto)
POST /chat
{
  "session_id": "cliente_001",
  "message": "¿Cuál me recomiendas en talla 42?"
}
```

## Testing

### Ejecutar tests

```bash
# Todos los tests (usar pytest del venv)
source venv/bin/activate
pytest -v

# Con coverage
pytest --cov=src --cov-report=term-missing

# Tests específicos
pytest tests/test_entities.py -v
```

### Estructura de tests

```
tests/
├── conftest.py           # Fixtures compartidas
├── test_entities.py      # Tests de entidades del dominio
└── test_services.py      # Tests de servicios de aplicación
```

## Docker

### Comandos útiles

```bash
# Construir y levantar
docker compose up --build

# Levantar en background
docker compose up -d

# Ver logs
docker compose logs -f api

# Detener
docker compose down

# Reconstruir desde cero
docker compose down -v
docker compose up --build
```

### Persistencia de datos

La base de datos SQLite se almacena en `./data/ecommerce_chat.db` y persiste entre reinicios del contenedor gracias al volumen montado.

## Estructura del Proyecto

```
e-commerce-chat/
├── src/
│   ├── domain/                    # Capa de dominio
│   │   ├── entities.py            # Product, ChatMessage, ChatContext
│   │   ├── repositories.py        # Interfaces IProductRepository, IChatRepository
│   │   └── exceptions.py          # Excepciones del dominio
│   ├── application/               # Capa de aplicación
│   │   ├── dtos.py                # DTOs con Pydantic
│   │   ├── product_service.py     # Servicio de productos
│   │   └── chat_service.py        # Servicio de chat
│   └── infrastructure/            # Capa de infraestructura
│       ├── api/
│       │   └── main.py            # FastAPI app
│       ├── db/
│       │   ├── database.py        # Configuración SQLAlchemy
│       │   ├── models.py          # Modelos ORM
│       │   └── init_data.py       # Datos iniciales
│       ├── repositories/
│       │   ├── product_repository.py
│       │   └── chat_repository.py
│       └── llm_providers/
│           └── gemini_service.py  # Integración con Gemini
├── tests/                         # Tests unitarios
├── evidencias/                    # Screenshots de evidencias
├── data/                          # Base de datos SQLite (gitignored)
├── .env                           # Variables de entorno (NO versionar)
├── .env.example                   # Plantilla de variables
├── Dockerfile                     # Imagen Docker
├── docker-compose.yml             # Orquestación
├── requirements.txt               # Dependencias Python
├── pyproject.toml                 # Configuración pytest
└── README.md                      # Este archivo
```

## Características del Sistema

### Gestión de Productos
- Listar todos los productos
- Buscar por ID
- Filtrar por marca y categoría
- Verificar disponibilidad (stock > 0)

### Chat Inteligente
- Conversación natural con asistente
- Memoria conversacional (últimos 6 mensajes)
- Recomendaciones personalizadas
- Información de precios y stock en tiempo real

### Persistencia
- Base de datos SQLite
- 10 productos iniciales precargados
- Historial completo de conversaciones

## Desarrollo

### Agregar un nuevo producto

```python
from src.domain.entities import Product

product = Product(
    id=None,
    name="Nuevo Zapato",
    brand="Marca",
    category="Categoría",
    size="42",
    color="Color",
    price=100.0,
    stock=10,
    description="Descripción"
)
```

### Extender funcionalidad del chat

Editar `src/infrastructure/llm_providers/gemini_service.py` para modificar el prompt del sistema.

## Troubleshooting

### Error: "Unable to locate package python3.11"
Si estás en Kali Linux con Python 3.13, usa `pyenv` para instalar 3.11:
```bash
curl https://pyenv.run | bash
pyenv install 3.11.9
pyenv local 3.11.9
```

### Error: Gemini API key not configured
Verifica que `.env` existe y contiene `GEMINI_API_KEY=tu_key_real`.

### Error: SQLite database is locked
Detén cualquier instancia de uvicorn o Docker que esté usando la BD:
```bash
docker compose down
killall uvicorn
```

### Tests fallan con "No module named 'pytest_asyncio'"
Usa el pytest del venv, no el del sistema:
```bash
source venv/bin/activate
pytest -v
```

## Autor

[Tu Nombre] - Universidad EAFIT

## Licencia

Este proyecto es parte de un taller académico de la Universidad EAFIT.
