from typing import List, Optional
from datetime import date as date_type
import base64

from fastapi import APIRouter, Depends, status, Header, HTTPException, Query, Request
from fastapi.responses import Response

from schemas.tarifa_cliente_schema import (
    TarifaClienteRequest,
    TarifaClienteResponse,
    TarifaResponseWrapper,
)
from controllers.tarifa_cliente_controller import TarifaClienteController
from services.export_service import exportar_a_csv, exportar_a_txt, exportar_a_excel, exportar_a_parquet


router = APIRouter(prefix="/tarifas", tags=["tarifas"])


def get_tarifa_controller():
    from repositories.tarifa_cliente_postgres import PostgresTarifaClienteRepository
    from services_impl.tarifa_cliente_service_impl import TarifaClienteServiceImpl
    from controllers.tarifa_cliente_controller import TarifaClienteController
    
    repo = PostgresTarifaClienteRepository()
    service = TarifaClienteServiceImpl(repo)
    return TarifaClienteController(service)


TARIFAS_HEADERS = [
    "id", "cliente", "identificacion", "contrato", "activo",
    "vigencia_inicial", "vigencia_final", "contacto", "direccion", "telefono",
    "clase_fd", "zona_transporte", "servicio", "operacion", "insumo",
    "tipo_fd", "tamanio", "modulo", "tarifa", "valor_fijo",
    "factor_crecimiento", "responsable", "ciudad", "sucursal", "centro_costo", "prioridad"
]


def convert_to_dict(results):
    data = []
    for r in results:
        data.append({
            "id": r.id,
            "cliente": r.cliente,
            "identificacion": r.identificacion,
            "contrato": r.contrato,
            "activo": r.activo,
            "vigencia_inicial": str(r.vigencia_inicial) if r.vigencia_inicial else "",
            "vigencia_final": str(r.vigencia_final) if r.vigencia_final else "",
            "contacto": r.contacto,
            "direccion": r.direccion,
            "telefono": r.telefono,
            "clase_fd": r.clase_fd,
            "zona_transporte": r.zona_transporte,
            "servicio": r.servicio,
            "operacion": r.operacion,
            "insumo": r.insumo,
            "tipo_fd": r.tipo_fd,
            "tamanio": r.tamanio,
            "modulo": r.modulo,
            "tarifa": r.tarifa,
            "valor_fijo": r.valor_fijo,
            "factor_crecimiento": r.factor_crecimiento,
            "responsable": r.responsable,
            "ciudad": r.ciudad,
            "sucursal": r.sucursal,
            "centro_costo": r.centro_costo,
            "prioridad": r.prioridad,
        })
    return data


@router.get("")
def list_or_export_tarifas(
        request: Request,
        ciudad: Optional[str] = None,
        cliente: Optional[str] = None,
        fecha: Optional[date_type] = None,
        download: bool = Query(True, description="True=incluye data, False=solo metadata"),
        controller: TarifaClienteController = Depends(get_tarifa_controller),
    ):
    """Lista tarifas con metadata
    
    Siempre retorna JSON. Para formatos de archivo, retorna archivo para descargar.
    
    Uso:
    - GET /tarifas?ciudad=YUMBO                    → JSON con data
    - GET /tarifas?ciudad=YUMBO&download=false    → Solo metadata
    - GET /tarifas?ciudad=YUMBO&format=csv         → Archivo CSV para descargar
    """
    results = controller.find_by_filters(
        ciudad=ciudad,
        cliente=cliente,
        fecha=fecha,
    )
    
    accept = request.headers.get("Accept", "application/json")
    data = convert_to_dict(results)
    registro_count = len(results)
    
    # Determinar formato por header Accept
    if "text/csv" in accept.lower():
        file_type = "csv"
        media_type = "text/csv"
    elif "text/plain" in accept.lower():
        file_type = "txt"
        media_type = "text/plain"
    elif "application/vnd.openxmlformats" in accept.lower():
        file_type = "xlsx"
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif "application/octet-stream" in accept.lower():
        file_type = "parquet"
        media_type = "application/octet-stream"
    else:
        file_type = "json"
        media_type = None
    
    # Si es formato de archivo, retornar archivo para descargar directamente
    if file_type != "json":
        if file_type == "csv":
            content = exportar_a_csv(data, TARIFAS_HEADERS)
        elif file_type == "txt":
            content = exportar_a_txt(data, TARIFAS_HEADERS)
        elif file_type == "xlsx":
            content = exportar_a_excel(data, TARIFAS_HEADERS)
        elif file_type == "parquet":
            content = exportar_a_parquet(data, TARIFAS_HEADERS)
        
        return Response(
            content=content,
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename=tarifas.{file_type}",
                "X-Total-Registros": str(registro_count),
                "X-Formato": file_type,
            }
        )
    
    # JSON response con metadata
    metadata = {
        "formato": "json",
        "filename": "tarifas.json",
        "total_registros": registro_count,
        "columnas": len(TARIFAS_HEADERS),
    }
    
    response = {
        "success": True,
        "filtros": {
            "ciudad": ciudad,
            "cliente": cliente,
            "fecha": str(fecha) if fecha else None,
        },
        "metadata": metadata,
    }
    
    # Solo metadata
    if not download:
        return response
    
    # Con data
    response["data"] = data
    response["registros"] = registro_count
    
    return response


@router.get("/search", response_model=TarifaResponseWrapper)
def search_tarifas(
        ciudad: Optional[str] = None,
        cliente: Optional[str] = None,
        fecha: Optional[date_type] = None,
        controller: TarifaClienteController = Depends(get_tarifa_controller),
    ):
    """Busca tarifas por filtros"""
    results = controller.find_by_filters(
        ciudad=ciudad,
        cliente=cliente,
        fecha=fecha,
    )
    return TarifaResponseWrapper(
        success=True,
        registros=len(results),
        tipo_reporte="CATALOGO",
        data=results,
    )


@router.get("/{tarifa_id}", response_model=TarifaClienteResponse)
def get_tarifa(
        tarifa_id: int,
        controller: TarifaClienteController = Depends(get_tarifa_controller),
    ):
    """Obtiene una tarifa por ID"""
    return controller.get_by_id(tarifa_id)


@router.post("", response_model=TarifaClienteResponse, status_code=status.HTTP_201_CREATED)
def create_tarifa(
        data: TarifaClienteRequest,
        controller: TarifaClienteController = Depends(get_tarifa_controller),
        x_created_by: str = Header(default="system"),
    ):
    """Crea una nueva tarifa"""
    return controller.create(data, x_created_by)


@router.put("/{tarifa_id}", response_model=TarifaClienteResponse)
def update_tarifa(
        tarifa_id: int,
        data: TarifaClienteRequest,
        controller: TarifaClienteController = Depends(get_tarifa_controller),
    ):
    """Actualiza una tarifa"""
    return controller.update(tarifa_id, data)


@router.delete("/{tarifa_id}", response_model=TarifaClienteResponse)
def delete_tarifa(
        tarifa_id: int,
        controller: TarifaClienteController = Depends(get_tarifa_controller),
    ):
    """Elimina lógicamente una tarifa"""
    return controller.delete(tarifa_id)


@router.get("/export")
def export_tarifas(
        format: str = Query("csv", description="Formato: csv, txt, excel, parquet"),
        ciudad: Optional[str] = None,
        cliente: Optional[str] = None,
        fecha: Optional[date_type] = None,
        controller: TarifaClienteController = Depends(get_tarifa_controller),
    ):
    """Exporta tarifas a archivo"""
    results = controller.find_by_filters(ciudad=ciudad, cliente=cliente, fecha=fecha)
    data = convert_to_dict(results)
    formato = format.lower()
    
    if formato == "csv":
        content = exportar_a_csv(data, TARIFAS_HEADERS)
        return Response(content=content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=tarifas.csv"})
    elif formato == "txt":
        content = exportar_a_txt(data, TARIFAS_HEADERS)
        return Response(content=content, media_type="text/plain", headers={"Content-Disposition": "attachment; filename=tarifas.txt"})
    elif formato == "excel":
        content = exportar_a_excel(data, TARIFAS_HEADERS)
        return Response(content=content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=tarifas.xlsx"})
    elif formato == "parquet":
        content = exportar_a_parquet(data, TARIFAS_HEADERS)
        return Response(content=content, media_type="application/octet-stream", headers={"Content-Disposition": "attachment; filename=tarifas.parquet"})
    else:
        content = exportar_a_csv(data, TARIFAS_HEADERS)
        return Response(content=content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=tarifas.csv"})