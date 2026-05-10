from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True, slots=True)
class TarifaCliente:
    id: int
    cliente: str
    identificacion: str
    contrato: str
    activo: bool
    vigencia_inicial: datetime
    vigencia_final: Optional[datetime] = None
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
    rango_inicial: Optional[datetime] = None
    rango_final: Optional[datetime] = None
    tarifa: Optional[float] = None
    valor_fijo: Optional[float] = None
    factor_crecimiento: Optional[float] = None
    responsable: Optional[str] = None
    ciudad: Optional[str] = None
    sucursal: Optional[str] = None
    centro_costo: Optional[str] = None
    prioridad: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    active: bool = True