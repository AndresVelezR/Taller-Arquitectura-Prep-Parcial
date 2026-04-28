# Evidencias del Taller

Esta carpeta contiene las 6 capturas de pantalla requeridas para la entrega del taller.

## Screenshots Requeridos

### 1. `01-swagger-ui.png`
**Contenido:** Documentación interactiva de Swagger UI  
**URL:** http://localhost:8000/docs  
**Debe mostrar:**
- Todos los endpoints listados (GET /products, POST /chat, etc.)
- Fecha/hora del sistema operativo visible
- Nombre de usuario de tu PC visible

**Cómo tomar:**
1. Arrancar la app: `uvicorn src.infrastructure.api.main:app --reload`
2. Abrir http://localhost:8000/docs en navegador
3. Screenshot de pantalla completa mostrando la barra del sistema operativo

---

### 2. `02-docker-logs.png`
**Contenido:** Logs del contenedor Docker  
**Comando:** `docker compose logs api`  
**Debe mostrar:**
- Logs de Uvicorn iniciando
- Mensajes de creación de BD y seed de productos
- Nombre de usuario visible en el prompt de terminal
- Fecha/hora del sistema

**Cómo tomar:**
1. `docker compose up --build`
2. En otra terminal: `docker compose logs api`
3. Screenshot mostrando el prompt con tu usuario

---

### 3. `03-docker-running.png`
**Contenido:** Docker mostrando contenedores corriendo  
**Comando:** `docker ps`  
**Debe mostrar:**
- Contenedor `ecommerce-api` en estado `Up`
- Puerto 8000:8000
- Fecha/hora del sistema visible

**Cómo tomar:**
1. Con Docker corriendo: `docker ps`
2. Screenshot del terminal mostrando la salida

**Alternativa (si usas Docker Desktop):**
- Screenshot de Docker Desktop mostrando el contenedor activo

---

### 4. `04-api-call-products.png`
**Contenido:** Request GET a `/products` desde Postman/Insomnia/httpie  
**Debe mostrar:**
- Request GET http://localhost:8000/products
- Response JSON con la lista de 10 productos
- Status 200 OK
- Fecha/hora visible

**Cómo tomar con httpie:**
```bash
http GET localhost:8000/products
```

**Cómo tomar con Postman:**
1. Crear GET request a http://localhost:8000/products
2. Send
3. Screenshot mostrando request y response

---

### 5. `05-api-call-chat.png`
**Contenido:** Request POST a `/chat` con respuesta de Gemini AI  
**Debe mostrar:**
- Request POST http://localhost:8000/chat
- Body JSON con `session_id` y `message`
- Response con `assistant_message` generado por IA en español
- Status 200 OK

**Cómo tomar con httpie:**
```bash
http POST localhost:8000/chat \
  session_id=user123 \
  message="Busco zapatos Nike para correr, talla 42"
```

**Body ejemplo:**
```json
{
  "session_id": "user123",
  "message": "Busco zapatos Nike para correr, talla 42"
}
```

---

### 6. `06-database.png`
**Contenido:** Visualización de la base de datos SQLite con productos  
**Herramienta:** DB Browser for SQLite  
**Debe mostrar:**
- Tabla `products` con las 10 filas de productos
- Columnas: id, name, brand, category, size, color, price, stock, description
- Fecha/hora visible en la barra del sistema

**Cómo tomar:**
1. Instalar DB Browser: `sudo apt install sqlitebrowser` (Kali/Debian)
2. Abrir `data/ecommerce_chat.db` con DB Browser
3. Click en pestaña "Browse Data"
4. Seleccionar tabla "products"
5. Screenshot mostrando las filas

**Alternativa (VS Code):**
- Instalar extensión "SQLite Viewer"
- Abrir `data/ecommerce_chat.db`
- Screenshot de la vista de tabla

---

## Checklist de Evidencias

Antes de entregar, verifica que:

- [ ] Las 6 capturas están en formato PNG
- [ ] Todas muestran fecha/hora del sistema operativo
- [ ] Todas muestran tu nombre de usuario (en terminal o barra del sistema)
- [ ] Los nombres de archivo coinciden exactamente: `01-swagger-ui.png`, etc.
- [ ] Las imágenes son legibles (no borrosas, tamaño adecuado)
- [ ] `05-api-call-chat.png` muestra una respuesta real de Gemini AI en español

## Notas

- Estas evidencias demuestran que el proyecto funciona completamente
- Son requeridas para la evaluación del taller
- Deben mostrar que es tu computadora (tu usuario de Kali Linux)
