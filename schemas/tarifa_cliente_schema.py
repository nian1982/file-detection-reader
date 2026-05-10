from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional, Any, List, Dict


class TarifaClienteRequest(BaseModel):
    cliente: str
    identificacion: Optional[str] = None
    contrato: Optional[str] = None
    vigencia_inicial: date
    vigencia_final: Optional[date] = None
    contacto: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    clase_fd: Optional[str] = None
    zona_transporte: Optional[str] = None
    servicio: Optional[str] = None
    operacion: Optional[str] = None
    insumo: Optional[str] = None
    tipo_fd: Optional[str] = None
    tamanio: Optional[str] = None
    modulo: Optional[str] = None
    rango_inicial: Optional[Any] = None
    rango_final: Optional[Any] = None
    tarifa: Optional[float] = None
    valor_fijo: Optional[float] = None
    factor_crecimiento: Optional[str] = None
    responsable: Optional[str] = None
    ciudad: str
    sucursal: Optional[str] = None
    centro_costo: Optional[str] = None
    prioridad: Optional[str] = None


class TarifaClienteResponse(BaseModel):
    id: int
    cliente: str
    identificacion: Optional[str] = None
    contrato: Optional[str] = None
    activo: str
    vigencia_inicial: date
    vigencia_final: Optional[date] = None
    contacto: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    clase_fd: Optional[str] = None
    zona_transporte: Optional[str] = None
    servicio: Optional[str] = None
    operacion: Optional[str] = None
    insumo: Optional[str] = None
    tipo_fd: Optional[str] = None
    tamanio: Optional[str] = None
    modulo: Optional[str] = None
    rango_inicial: Optional[Any] = None
    rango_final: Optional[Any] = None
    tarifa: Optional[float] = None
    valor_fijo: Optional[float] = None
    factor_crecimiento: Optional[str] = None
    responsable: Optional[str] = None
    ciudad: Optional[str] = None
    sucursal: Optional[str] = None
    centro_costo: Optional[str] = None
    prioridad: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TarifaResponseWrapper(BaseModel):
    success: bool = True
    registros: Optional[int] = None
    tipo_reporte: str = "CATALOGO"
    data: Optional[List[TarifaClienteResponse]] = None
    filtros: Optional[Dict] = None
    metadata: Optional[Dict] = None