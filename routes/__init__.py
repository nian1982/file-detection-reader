from routes.products import router as products_router
from routes.tarifas import router as tarifas_router
from routes.notifications import router as notifications_router

__all__ = ["products_router", "tarifas_router", "notifications_router"]