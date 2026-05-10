import os
from datetime import datetime
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from config import get_settings
from models.product import Product
from repositories.product_repository import ProductRepository

class PostgresProductRepository(ProductRepository):
    def __init__(self):
        settings = get_settings()
        self._conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_database,
        )

    def _execute(self, query: str, params: tuple = None):
        with self._conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            self._conn.commit()
            return cur.fetchall()

    def _dict_to_product(self, row: dict) -> Product:
        return Product(
            id=row["id"],
            name=row["name"],
            presentation=row.get("presentation"),
            description=row.get("description"),
            brand_id=row["brand_id"],
            categorie_id=row["categorie_id"],
            create_by=row["create_by"],
            active=row["active"],
            create_at=row["create_at"],
            update_at=row.get("update_at"),
        )

    def list_products(self, is_active: bool = True) -> list[Product]:
        query = "SELECT * FROM products WHERE active = %s"
        rows = self._execute(query, (is_active,))
        return [self._dict_to_product(dict(r)) for r in rows]

    def get_by_id(self, product_id: int) -> Optional[Product]:
        query = "SELECT * FROM products WHERE id = %s"
        rows = self._execute(query, (product_id,))
        return self._dict_to_product(dict(rows[0])) if rows else None

    def create(self, product: Product) -> Product:
        query = """
            INSERT INTO products (name, brand_id, categorie_id, create_by, active, presentation, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, create_at, update_at
        """
        rows = self._execute(query, (
            product.name,
            product.brand_id,
            product.categorie_id,
            product.create_by,
            product.active,
            product.presentation,
            product.description,
        ))
        row = rows[0]
        
        return Product(
            id=row["id"],
            name=product.name,
            brand_id=product.brand_id,
            categorie_id=product.categorie_id,
            create_by=product.create_by,
            active=product.active,
            create_at=row["create_at"],
            update_at=row.get("update_at"),
            presentation=product.presentation,
            description=product.description,
        )

    def update(self, product_id: int, product: Product) -> Product:
        query = """
            UPDATE products 
            SET name=%s, brand_id=%s, categorie_id=%s, presentation=%s, description=%s, update_at=%s
            WHERE id=%s
            RETURNING create_at
        """
        existing = self.get_by_id(product_id)
        if not existing:
            raise ValueError(f"Product {product_id} not found")
        
        rows = self._execute(query, (
            product.name,
            product.brand_id,
            product.categorie_id,
            product.presentation,
            product.description,
            datetime.now(),
            product_id,
        ))
        row = rows[0]
        
        return Product(
            id=product_id,
            name=product.name,
            brand_id=product.brand_id,
            categorie_id=product.categorie_id,
            create_by=existing.create_by,
            active=existing.active,
            create_at=existing.create_at,
            update_at=datetime.now(),
            presentation=product.presentation,
            description=product.description,
        )

    def delete(self, product_id: int) -> Product:
        query = """
            UPDATE products SET active = false, update_at = %s
            WHERE id = %s
            RETURNING *
        """
        rows = self._execute(query, (datetime.now(), product_id))
        if not rows:
            raise ValueError(f"Product {product_id} not found")
        return self._dict_to_product(dict(rows[0]))

    def search_products(
        self, name: str = None, presentation: str = None, is_active: bool = True
    ) -> list[Product]:
        conditions = []
        params = []
        
        if is_active is not None:
            conditions.append("active = %s")
            params.append(is_active)
        
        if name:
            conditions.append("LOWER(name) LIKE %s")
            params.append(f"%{name.lower()}%")
        
        if presentation:
            conditions.append("LOWER(presentation) LIKE %s")
            params.append(f"%{presentation.lower()}%")
        
        query = "SELECT * FROM products"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        rows = self._execute(query, tuple(params))
        return [self._dict_to_product(dict(r)) for r in rows]