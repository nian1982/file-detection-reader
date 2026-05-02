# Product API

API REST para gestión de productos con arquitectura limpia.


## Installation

```bash
pip install -r requirements.txt
```


## Configuración

Editar el archivo `.env`:

```bash
# Almacenamiento: json | postgres
STORAGE_TYPE=json

# Configuración JSON
JSON_FILE_PATH=data/products.json

# Configuración PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DATABASE=products_db
```


## Ejecución

```bash
uvicorn main:app --reload
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000

Documentación Swagger: http://localhost:8000/docs


## Endpoints

| Método | Ruta | Descripción |
|--------|-----|-------------|
| GET | /products | Lista productos activos |
| GET | /products/{id} | Obtiene un producto por ID |
| POST | /products | Crea un nuevo producto |
| PUT | /products/{id} | Actualiza un producto |
| DELETE | /products/{id} | Elimina lógicamente un producto |


## Flujo de la Arquitectura

```
routes/products.py
        ↓
controllers/product_controller.py
        ↓
services_impl/product_service_impl.py
        ↓
repositories/[json|postgres]_product_repository.py
        ↓
models/product.py
```

### Descripción de capas

1. **routes/** - Endpoints FastAPI (sin lógica)
2. **controllers/** - Lógica HTTP (parsers, respuestas, errores)
3. **services_impl/** - Lógica de negocio (casos de uso)
4. **repositories/** - Acceso a datos (Protocol + implementaciones)
5. **models/** - Entidades del dominio

### Inyección de dependencias

`dependencies.py` crea los objetos según `STORAGE_TYPE`:

- `json` → `JsonProductRepository`
- `postgres` → `PostgresProductRepository`

Para cambiar el origen de datos, soloModify `STORAGE_TYPE` en `.env`.


## Ejemplo de uso

```bash
# Listar productos
curl http://localhost:8000/products

# Crear producto
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -H "x-created-by: admin" \
  -d '{
    "name": "Paracetamol",
    "brand_id": 1,
    "categorie_id": 1,
    "presentation": "500mg",
    "description": "Analgésico"
  }'
```


## SQL para PostgreSQL

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand_id INTEGER NOT NULL,
    categorie_id INTEGER NOT NULL,
    create_by VARCHAR(255) NOT NULL,
    active BOOLEAN DEFAULT TRUE,
    presentation VARCHAR(255),
    description TEXT,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP
);
```


## Estructura de archivos

```
api/
├── config.py              - Configuración centralizada
├── dependencies.py     - Inyección de dependencias
├── main.py             - FastAPI app
├── .env               - Variables de entorno
├── models/             - Entidades
├── repositories/      - Acceso a datos
├── services/          - Interfaces de servicio
├── services_impl/      - Lógica de negocio
├── controllers/       - Lógica HTTP
├── schemas/            - Schemas Pydantic
└── routes/            - Endpoints
```

# Test
## Ejecución
python -m pytest tests/ -v
# Solo PostgreSQL
python -m pytest tests/test_postgres.py -v
# Con coverage

|Comando                        |Qué hace                       |
|-------------------------------|-------------------------------|            
|`coverage run -m pytest tests/`|Ejecuta tests midiendo coverage|                               -
|`coverage report`              |Muestra tabla de coverage      |
|`coverage report -m`           |Muestra líneas exacta          |
|`coverage html`                |Genera reporte HTML navegable  |	
	

GET /products/search                          → 10 productos (activos por defecto)
GET /products/search?name=iPhone              → 1 producto (iPhone 15)
GET /products/search?presentation=GB        → 2 productos
GET /products/search?is_active=false       → 3 productos inactivos
GET /products/search?name=iPhone&presentation=128  → combination
GET /curl -s "http://localhost:8000/products/filter?name=Galaxy%20S23&presentation=256GB&is_active=true"
---
Resumen del flujo
Cliente → Routes (products.py)
         ├──接收参数: name, presentation, is_active
         ├──llama: controller.search_products()
         
         → Controller (product_controller.py)
         ├──pasa parámetros
         ├──llama: service.search_products()
         
         → Service (product_service_impl.py)
         ├──delega al repositorio
         ├──llama: repository.search_products()
         
         → Repository (JSON o PostgreSQL)
         ├──ejecuta la búsqueda con filtros
         
         ← Devuelve lista de Product
         ← ProductResponse
         ← JSON al cliente	

## Servicio catalogo particular
GET /tarifas/search?ciudad=YUMBO&cliente=BGP&fecha=2026-04-26
Parámetros (todos opcionales):
Parámetro	Descripción
ciudad	Ciudad (ej: YUMBO, MEDELLIN)
cliente	Nombre parcial del cliente (búsqueda flexible)
fecha	Fecha para validar rango vigencia
Equivalente SQL:
SELECT * FROM tarifas_cliente 
WHERE TRIM(activo) = 'SI' 
  AND ciudad = 'YUMBO'
  AND cliente LIKE '%BGP%'
  AND '2026-04-26' >= vigencia_inicial 
  AND '2026-04-26	

# Parámetros de filtro (query)
ciudad=YUMBO
cliente=BGP  
fecha=2026-04-26
# Formato con header Accept:
-H "Accept: text/csv"   → CSV
-H "Accept: text/plain"  → TXT  
-H "Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" → Excel
-H "Accept: application/octet-stream" → Parquet
Ejemplos completos:
# CSV con 3 filtros
curl -H "Accept: text/csv" "http://localhost:8000/tarifas?ciudad=YUMBO&cliente=BGP&fecha=2026-04-26" -o tarifas.csv
# TXT
curl -H "Accept: text/plain" "http://localhost:8000/tarifas?ciudad=YUMBO" -o tarifas.txt
# Excel
curl -H "Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" "http://localhost:8000/tarifas?ciudad=YUMBO" -o tarifas.xlsx
# JSON (default) - No necesita header
curl "http://localhost:8000/tarifas?ciudad=YUMBO" | jq
Con 3 filtros (ciudad + cliente + fecha):
curl -H "Accept: text/csv" \
  "http://localhost:8000/tarifas?ciudad=YUMBO&cliente=BGP&fecha=2026-04-26" \
  -o tarifas.csv

1. Preview - Ver metadata antes de descargar (download=false)
curl "http://localhost:8000/tarifas?ciudad=YUMBO&cliente=BGP&download=false"
Respuesta:
{
  "success": true,
  "filtros": {"ciudad": "YUMBO", "cliente": "BGP", "fecha": null},
  "metadata": {
    "formato": "json",
    "filename": "tarifas.json",
    "total_registros": 51,
    "columnas": 26
  }
}
2. JSON (default)
curl "http://localhost:8000/tarifas?ciudad=YUMBO"
3. CSV (con Accept header)
curl -H "Accept: text/csv" "http://localhost:8000/tarifas?ciudad=YUMBO&cliente=BGP" -o archivo.csv
4. Otros formatos
# TXT
curl -H "Accept: text/plain" "http://localhost:8000/tarifas?ciudad=YUMBO" -o archivo.txt
# Excel  
curl -H "Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" "http://localhost:8000/tarifas?ciudad=YUMBO" -o data/archivo.xlsx
---
Parámetros:
Parámetro	Descripción
ciudad	Ciudad (filtro)
cliente	Cliente (filtro parcial)
fecha	Fecha vigencia
download	false = solo metadata, true = descargar (default)


Estructura del comando:
curl -H "Accept: [FORMATO]" "[URL]?[filtro1]&[filtro2]&[filtro3]" -o [archivo.formato]
Formato	Header Accept
CSV	text/csv
TXT	text/plain
Excel	application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
JSON	application/json (default)