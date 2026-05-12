# Módulo api_exportes

## ¿Qué hace este módulo?

Este módulo **consulta notificaciones pendientes** en una base de datos Oracle. Recibes el nombre de una plantilla y el sistema busca en la base de datos todas las notificaciones que estén pendientes de enviar para esa plantilla.

### ¿Qué devuelve?

Por cada notificación encuentra, te entrega:

| Dato | ¿Qué es? |
|------|----------|
| `recipients` | A quién va dirigida la notificación (emails, teléfonos, etc.) |
| `data` | Información adicional de la notificación |
| `subject` | El asunto del mensaje |
| `message_template` | La plantilla del mensaje (puede ser HTML, texto, etc.) |
| `variables` | Las variables que se usan dentro de la plantilla |

---

## ¿Cómo está construido? (La "fábrica" por dentro)

El módulo está organizado como una **línea de ensamblaje**. Cada pieza hace una sola cosa y se la pasa a la siguiente:

```
                    ┌─────────────────────────┐
                    │     ROUTES (Rutas)      │
                    │  La puerta de entrada   │
                    │  Recibe la petición HTTP│
                    └─────────┬───────────────┘
                              │
                    ┌─────────▼───────────────┐
                    │   CONTROLLER (Control)  │
                    │  El organizador         │
                    │  Valida, dirige,        │
                    │  maneja errores         │
                    └─────────┬───────────────┘
                              │
                    ┌─────────▼───────────────┐
                    │   SERVICE (Servicio)    │
                    │  El supervisor          │
                    │  Aplica reglas:         │
                    │  "Si no hay resultados, │
                    │   avisar que está vacío"│
                    └─────────┬───────────────┘
                              │
                    ┌─────────▼───────────────┐
                    │  REPOSITORY (Almacén)   │
                    │  El que busca los datos │
                    │  Hace la consulta SQL   │
                    │  a Oracle               │
                    └─────────┬───────────────┘
                              │
                    ┌─────────▼───────────────┐
                    │   ORACLE DATABASE       │
                    │  La base de datos       │
                    │  donde están las        │
                    │  notificaciones         │
                    └─────────────────────────┘
```

### Explicación simple de cada capa:

1. **Routes** — Es la **puerta de entrada**. Cuando alguien llama a la API por internet, el primero en recibir el llamado es Routes. Ej: `GET /exports/plantilla/MiPlantilla`

2. **Controller** — Es el **organizador**. Recibe la petición, llama al servicio y si algo sale mal (ej: no se encuentra la plantilla), responde con un error claro.

3. **Service** — Es el **supervisor**. Contiene las reglas del negocio. Por ejemplo: "si no hay notificaciones pendientes, avisar que no hay resultados".

4. **Repository** — Es el **almacén**. Es el único que sabe cómo hablar con la base de datos. Aquí está la consulta SQL.

5. **Database** — Es la **conexión a la base de datos**. Aquí se configura cómo conectarse a Oracle.

### ¿Por qué está separado en capas?

Para que sea **fácil de cambiar**:
- ¿Cambias de Oracle a PostgreSQL? Solo cambias la capa de Database y Repository.
- ¿Cambia la consulta SQL? Solo tocas el Repository.
- ¿Cambian las reglas de negocio? Solo tocas el Service.
- ¿Cambia la forma de llamar la API? Solo tocas Routes.

Cada capa hace su trabajo y no sabe cómo funcionan las demás.

---

## Flujo paso a paso (cuando alguien llama a la API)

### Caso: Consultar notificaciones de la plantilla "ReporteDiario"

```
Paso 1: Tú (o un programa) llamas a la API:
        GET http://localhost:8000/exports/plantilla/ReporteDiario
        (con un token de seguridad en el encabezado)

Paso 2: Routes recibe la petición y le pasa el nombre "ReporteDiario"
        al Controller.

Paso 3: El Controller le pide al Service que busque las notificaciones
        de la plantilla "ReporteDiario".

Paso 4: El Service le pide al Repository que haga la consulta en Oracle.

Paso 5: El Repository ejecuta esta consulta SQL en la base de datos:
        
        SELECT recipients, data, subject, message_template, variables
        FROM notification_queue
        JOIN message_templates ON ...
        WHERE status = 'P' AND name = 'ReporteDiario'

Paso 6: Oracle devuelve los resultados (o vacío si no hay nada).

Paso 7: El Repository convierte los resultados al formato del módulo
        y se los devuelve al Service.

Paso 8: El Service verifica que haya resultados. Si no hay, lanza
        un error. Si hay, los devuelve al Controller.

Paso 9: El Controller le devuelve los datos a Routes.

Paso 10: Routes responde con los datos en formato JSON.
```

---

## ¿Cómo lo uso?

### Opción 1: Como servicio web (API)

La API corre como un servidor al que le hablas por internet.

**Paso 1 — Prender el servidor:**
```bash
cd /ruta/del/proyecto/api
source .venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Paso 2 — Obtener token de seguridad (Keycloak):**
```bash
TOKEN=$(curl -s -X POST http://localhost:8080/realms/muhoco/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=api-exportes" \
  -d "client_secret=EL_SECRET_DEL_CLIENTE" \
  -d "grant_type=client_credentials" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
```

**Paso 3 — Consultar una plantilla:**
```bash
curl -s http://localhost:8000/exports/plantilla/ReporteDiario \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Respuesta ejemplo:**
```json
[
  {
    "recipients": "juan@empresa.com, maria@empresa.com",
    "data": "{\"job_id\": 456}",
    "subject": "Reporte Diario - Procesado",
    "message_template": "<h1>Reporte {{nombre}}</h1><p>Fecha: {{fecha}}</p>",
    "variables": "nombre, fecha"
  }
]
```

### Opción 2: Como script (sin servidor)

No necesitas prender el servidor. El script se conecta directo a la base de datos.

```bash
cd /ruta/del/proyecto/api
source .venv/bin/activate
python -m api_exportes.cli ReporteDiario
```

Esto imprime los resultados en la terminal.

### Opción 3: Desde otro código Python

Puedes usar el servicio directamente desde cualquier script Python:

```python
from api_exportes.repositories.oracle_database import OracleDatabase
from api_exportes.repositories.oracle_plantilla_repository import OraclePlantillaRepository
from api_exportes.services_impl.export_service_impl import ExportServiceImpl

# 1. Conectar a Oracle
db = OracleDatabase()

# 2. Crear el repositorio
repo = OraclePlantillaRepository(db)

# 3. Crear el servicio
service = ExportServiceImpl(repo)

# 4. Consultar
resultados = service.export_by_plantilla("ReporteDiario")

# 5. Mostrar resultados
for r in resultados:
    print(f"Asunto: {r.subject}")
    print(f"Para: {r.recipients}")
    print("---")
```

---

## Configuración antes de usar

Edita el archivo `.env` en la raíz del proyecto con los datos de tu base de datos Oracle:

```env
ORACLE_HOST=localhost              # Dirección del servidor Oracle
ORACLE_PORT=1521                   # Puerto de Oracle (default: 1521)
ORACLE_SERVICE_NAME=XE             # Nombre del servicio Oracle
ORACLE_USER=mi_usuario             # Usuario de la base de datos
ORACLE_PASSWORD=mi_contraseña      # Contraseña
ORACLE_MIN_POOL=1                  # Conexiones mínimas (dejar 1)
ORACLE_MAX_POOL=5                  # Conexiones máximas
```

### Configurar Keycloak (seguridad)

1. En Keycloak, crea un cliente llamado `api-exportes`
2. En ese cliente, crea un rol `exports.read`
3. Asigna ese rol a los usuarios o clientes que vayan a consumir la API

---

## Si quieres cambiar la base de datos (ej: pasar a PostgreSQL)

El módulo ya incluye un adaptador para PostgreSQL (`postgres_database.py`).

Para cambiar, solo editas el archivo `dependencies.py`:

```python
# Antes (Oracle):
from api_exportes.repositories.oracle_database import OracleDatabase
from api_exportes.repositories.oracle_plantilla_repository import OraclePlantillaRepository

# Después (PostgreSQL):
from api_exportes.repositories.postgres_database import PostgresDatabase
# Necesitas crear un PostgresPlantillaRepository similar
```

---

## Resumen de archivos del módulo

| Archivo | ¿Qué hace? |
|---------|-----------|
| `models/plantilla_notificacion.py` | Define cómo se ve una notificación (sus campos) |
| `schemas/export_schema.py` | Define cómo se entregan los datos por la API |
| `repositories/database.py` | Define cómo debe ser una conexión a BD |
| `repositories/oracle_database.py` | Conexión a Oracle (usa pool de conexiones) |
| `repositories/postgres_database.py` | Conexión a PostgreSQL (alternativa) |
| `repositories/plantilla_repository.py` | Define cómo debe ser un almacén de plantillas |
| `repositories/oracle_plantilla_repository.py` | El almacén real: contiene la consulta SQL |
| `services/export_service.py` | Define cómo debe ser el servicio |
| `services_impl/export_service_impl.py` | El servicio real con las reglas de negocio |
| `controllers/export_controller.py` | El organizador: maneja errores HTTP |
| `routes/exports.py` | La puerta de entrada: define la ruta `/exports/plantilla/{nombre}` |
| `dependencies.py` | El cableado: conecta todas las piezas |
| `cli.py` | El script para usar desde la terminal |

---

## ¿Preguntas?

Si algo no queda claro, revisa los comentarios en cada archivo o pregunta al equipo de desarrollo.
