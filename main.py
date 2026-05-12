from fastapi import FastAPI
from config import get_settings
from routes import products
from routes import tarifas
from routes import notifications
from api_exportes.routes.exports import router as exportes_router

app = FastAPI(
    title=get_settings().app_name,
    version=get_settings().app_version,
)

app.include_router(products.router)
app.include_router(tarifas.router)
app.include_router(notifications.router)
app.include_router(exportes_router)


@app.get("/")
def root():
    return {"message": get_settings().app_name, "version": get_settings().app_version}


@app.get("/health")
def health():
    return {"status": "healthy"}
