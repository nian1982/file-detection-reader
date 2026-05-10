import os
import json
from datetime import datetime
from typing import Optional
from config import get_settings
from models.product import Product
from repositories.product_repository import ProductRepository

class JsonProductRepository(ProductRepository):
    def __init__(self, file_path: str = None):
        self._file_path = file_path or get_settings().json_file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        if not os.path.exists(self._file_path):
            with open(self._file_path, "w") as f:
                json.dump([], f)

    def _load_products(self) -> list[dict]:
        with open(self._file_path, "r") as f:
            return json.load(f)

    def _save_products(self, products: list[dict]):
        with open(self._file_path, "w") as f:
            json.dump(products, f, indent=2, default=str)

    def _dict_to_product(self, data: dict) -> Product:
        return Product(
            id=data["id"],
            name=data["name"],
            presentation=data.get("presentation"),
            description=data.get("description"),
            brand_id=data["brand_id"],
            categorie_id=data["categorie_id"],
            create_by=data["create_by"],
            active=data["active"],
            create_at=datetime.fromisoformat(data["create_at"]) if data.get("create_at") else None,
            update_at=datetime.fromisoformat(data["update_at"]) if data.get("update_at") else None,
        )

    def list_products(self, is_active: bool = True) -> list[Product]:
        products = self._load_products()
        if is_active:
            products = [p for p in products if p.get("active", True)]
        return [self._dict_to_product(p) for p in products]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        products = self._load_products()
        for p in products:
            if p["id"] == product_id:
                return self._dict_to_product(p)
        return None

    def create(self, product: Product) -> Product:
        products = self._load_products()
        new_id = max([p["id"] for p in products], default=0) + 1
        new_product = {
            "id": new_id,
            "name": product.name,
            "presentation": product.presentation,
            "description": product.description,
            "brand_id": product.brand_id,
            "categorie_id": product.categorie_id,
            "create_by": product.create_by,
            "active": product.active,
            "create_at": datetime.now().isoformat(),
            "update_at": None,
        }
        products.append(new_product)
        self._save_products(products)
        return self._dict_to_product(new_product)

    def update(self, product_id: int, product: Product) -> Product:
        products = self._load_products()
        for i, p in enumerate(products):
            if p["id"] == product_id:
                products[i] = {
                    "id": product_id,
                    "name": product.name,
                    "presentation": product.presentation,
                    "description": product.description,
                    "brand_id": product.brand_id,
                    "categorie_id": product.categorie_id,
                    "create_by": product.create_by,
                    "active": product.active,
                    "create_at": p["create_at"],
                    "update_at": datetime.now().isoformat(),
                }
                self._save_products(products)
                return self._dict_to_product(products[i])
        raise ValueError(f"Product {product_id} not found")

    def delete(self, product_id: int) -> Product:
        products = self._load_products()
        for i, p in enumerate(products):
            if p["id"] == product_id:
                products[i]["active"] = False
                products[i]["update_at"] = datetime.now().isoformat()
                self._save_products(products)
                return self._dict_to_product(products[i])
        raise ValueError(f"Product {product_id} not found")

    def search_products(
        self, name: str = None, presentation: str = None, is_active: bool = True
    ) -> list[Product]:
        products = self._load_products()
        
        # Filtrar por activos
        if is_active is not None:
            products = [p for p in products if p.get("active", True) == is_active]
        
        # Filtrar por name (contiene texto)
        if name:
            products = [p for p in products if name.lower() in p.get("name", "").lower()]
        
        # Filtrar por presentation (contiene texto)
        if presentation:
            products = [p for p in products if presentation.lower() in p.get("presentation", "").lower()]
        
        return [self._dict_to_product(p) for p in products]