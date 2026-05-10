from models.product import Product
from repositories.product_repository import ProductRepository
from services.product_service import ProductService

class ProductServiceImpl(ProductService):
    def __init__(self, repository: ProductRepository):
        self._repository = repository

    def list_products(self, is_active: bool = True) -> list[Product]:
        return self._repository.list_products(is_active)

    def get_product(self, product_id: int) -> Product | None:
        return self._repository.get_by_id(product_id)

    def create_product(self, product: Product) -> Product:
        return self._repository.create(product)

    def update_product(self, product_id: int, product: Product) -> Product:
        existing = self._repository.get_by_id(product_id)
        if existing is None:
            raise ValueError(f"Product {product_id} not found")
        return self._repository.update(product_id, product)

    def delete_product(self, product_id: int) -> Product:
        return self._repository.delete(product_id)

    def search_products(self, name: str = None, presentation: str = None, is_active: bool = True) -> list[Product]:
        return self._repository.search_products(name, presentation, is_active)