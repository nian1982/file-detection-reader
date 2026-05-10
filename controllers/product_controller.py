from fastapi import Depends, HTTPException, status
from models.product import Product
from services.product_service import ProductService
from services_impl.product_service_impl import ProductServiceImpl
from repositories.product_repository import ProductRepository

class ProductController:
    def __init__(self, service: ProductService):
        self._service = service

    def list_products(self, is_active: bool = True) -> list[Product]:
        return self._service.list_products(is_active)

    def get_product(self, product_id: int) -> Product:
        product = self._service.get_product(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not found",
            )
        return product

    def create_product(self, product_data, create_by: str) -> Product:
        product = Product(
            id=0,
            name=product_data.name,
            brand_id=product_data.brand_id,
            categorie_id=product_data.categorie_id,
            create_by=create_by,
            active=True,
            create_at=None,
            update_at=None,
            presentation=product_data.presentation,
            description=product_data.description,
        )
        return self._service.create_product(product)

    def update_product(self, product_id: int, product_data) -> Product:
        existing = self._service.get_product(product_id)
        if existing is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {product_id} not found",
            )
        product = Product(
            id=product_id,
            name=product_data.name,
            brand_id=product_data.brand_id,
            categorie_id=product_data.categorie_id,
            create_by=existing.create_by,
            active=existing.active,
            create_at=existing.create_at,
            update_at=None,
            presentation=product_data.presentation,
            description=product_data.description,
        )
        return self._service.update_product(product_id, product)

    def delete_product(self, product_id: int) -> Product:
        return self._service.delete_product(product_id)

    def search_products(
        self,
        name: str = None,
        presentation: str = None,
        is_active: bool = True,
    ) -> list[Product]:
        return self._service.search_products(name, presentation, is_active)