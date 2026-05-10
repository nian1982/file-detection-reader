from datetime import date as date_type
from typing import Optional
from models.tarifa_cliente import TarifaCliente
from repositories.tarifa_cliente_repository import TarifaClienteRepository
from services.tarifa_cliente_service import TarifaClienteService


class TarifaClienteServiceImpl(TarifaClienteService):
    def __init__(self, repository: TarifaClienteRepository):
        self._repository = repository

    def find_by_filters(
        self,
        ciudad: Optional[str] = None,
        cliente: Optional[str] = None,
        fecha: Optional[date_type] = None,
    ) -> list[TarifaCliente]:
        return self._repository.find_by_filters(ciudad, cliente, fecha)

    def get_by_id(self, id: int) -> TarifaCliente | None:
        return self._repository.get_by_id(id)

    def create(self, tarifa: TarifaCliente) -> TarifaCliente:
        return self._repository.create(tarifa)

    def update(self, id: int, tarifa: TarifaCliente) -> TarifaCliente:
        existing = self._repository.get_by_id(id)
        if not existing:
            raise ValueError(f"Tarifa {id} no encontrada")
        return self._repository.update(id, tarifa)

    def delete(self, id: int) -> TarifaCliente:
        return self._repository.delete(id)