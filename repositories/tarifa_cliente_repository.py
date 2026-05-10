from typing import Protocol, Optional
from datetime import date as date_type
from models.tarifa_cliente import TarifaCliente


class TarifaClienteRepository(Protocol):
    def find_by_filters(
        self,
        ciudad: Optional[str] = None,
        cliente: Optional[str] = None,
        fecha: Optional[date_type] = None,
    ) -> list[TarifaCliente]: ...
    
    def get_by_id(self, id: int) -> Optional[TarifaCliente]: ...
    def create(self, tarifa: TarifaCliente) -> TarifaCliente: ...
    def update(self, id: int, tarifa: TarifaCliente) -> TarifaCliente: ...
    def delete(self, id: int) -> TarifaCliente: ...