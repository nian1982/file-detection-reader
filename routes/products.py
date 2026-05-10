from typing import List
from fastapi import APIRouter, Depends, status, Header, HTTPException
from fastapi.responses import JSONResponse
from schemas.product_schema import (ProductRequest, ProductResponse,)
from controllers.product_controller import ProductController
from dependencies import get_controller
from shared.security.dependencies import (require_client_role)

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/search", response_model=List[ProductResponse])
def search_products(
    name: str = None,
    presentation: str = None,
    is_active: bool = True,
    controller: ProductController = Depends(get_controller),
):
    """Busca productos con filtros opcionales"""
    return controller.search_products(name=name, presentation=presentation, is_active=is_active)


@router.get("/filter", response_model=ProductResponse)
def filter_product(
    name: str,
    presentation: str,
    is_active: bool = True,
    controller: ProductController = Depends(get_controller),
):
    """Busca un producto específico con 3 filtros: name + presentation + is_active"""
    results = controller.search_products(name=name, presentation=presentation, is_active=is_active)
    if not results:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if len(results) > 1:
        raise HTTPException(status_code=400, detail="Múltiples productos encontrados")
    return results[0]
    

@router.get("", response_model=List[ProductResponse])
def list_products(
        controller: ProductController = Depends(get_controller),
        user=Depends(
            require_client_role(
                "api-products",
                "products.read"
            )
        )
    ):

    return controller.list_products(
        is_active=True
    )


# @router.get("", response_model=List[ProductResponse])
# def list_products(
#     controller: ProductController = Depends(get_controller),
#     user=Depends(get_current_user)
# ):
#     """Lista todos los productos activos"""

#     return controller.list_products(is_active=True)


# @router.get("", response_model=List[ProductResponse])
# def list_products(controller: ProductController = Depends(get_controller)):
#     """Lista todos los productos activos"""
#     return controller.list_products(is_active=True)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, controller: ProductController = Depends(get_controller)):
    """Obtiene un producto por ID"""
    return controller.get_product(product_id)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductRequest,
    controller: ProductController = Depends(get_controller),
    x_created_by: str = Header(default="system"),
    user=Depends(
            require_client_role(
                "api-products",
                "products.create"
            )
        )):
    """Crea un nuevo producto"""
    return controller.create_product(product_data, x_created_by)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductRequest,
    controller: ProductController = Depends(get_controller),
    user=Depends(
            require_client_role(
                "api-products",
                "products.update"
            )
        )):
    """Actualiza un producto"""
    return controller.update_product(product_id, product_data)


@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, controller: ProductController = Depends(get_controller),
    user=Depends(
            require_client_role(
                "api-products",
                "products.delete"
            )
        )):
    """Elimina lógicamente un producto"""
    return controller.delete_product(product_id)