from fastapi import HTTPException, status
from datetime import datetime, date
from typing import Optional
from models.tarifa_cliente import TarifaCliente
from services.tarifa_cliente_service import TarifaClienteService


class TarifaClienteController:
    def __init__(self, service: TarifaClienteService):
        self._service = service

    def find_by_filters(
            self,
            ciudad: Optional[str] = None,
            cliente: Optional[str] = None,
            fecha: Optional[date] = None,
        ) -> list[TarifaCliente]:
        return self._service.find_by_filters(
            ciudad=ciudad,
            cliente=cliente,
            fecha=fecha,
        )

    def get_by_id(self, id: int) -> TarifaCliente:
        tarifa = self._service.get_by_id(id)
        if not tarifa:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarifa {id} no encontrada",
            )
        return tarifa

    def create(
            self,
            data,
            created_by: str,
        ) -> TarifaCliente:
        tarifa = TarifaCliente(
            id=0,
            cliente=data.cliente,
            identificacion=data.identificacion,
            contrato=data.contrato,
            activo=True,
            vigencia_inicial=data.vigencia_inicial,
            vigencia_final=data.vigencia_final,
            contacto=data.contacto,
            direccion=data.direccion,
            telefono=data.telefono,
            clase_fd=data.clase_fd,
            zona_transporte=data.zona_transporte,
            servicio=data.servicio,
            operacion=data.operacion,
            insumo=data.insumo,
            tipo_fd=data.tipo_fd,
            tamanio=data.tamanio,
            modulo=data.modulo,
            rango_inicial=data.rango_inicial,
            rango_final=data.rango_final,
            tarifa=data.tarifa,
            valor_fijo=data.valor_fijo,
            factor_crecimiento=data.factor_crecimiento,
            responsable=data.responsable,
            ciudad=data.ciudad,
            sucursal=data.sucursal,
            centro_costo=data.centro_costo,
            prioridad=data.prioridad,
            created_by=created_by,
            active=True,
        )
        return self._service.create(tarifa)

    def update(self, id: int, data) -> TarifaCliente:
        existing = self._service.get_by_id(id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tarifa {id} no encontrada",
            )
        tarifa = TarifaCliente(
            id=id,
            cliente=data.cliente,
            identificacion=data.identificacion,
            contrato=data.contrato,
            activo=existing.activo,
            vigencia_inicial=data.vigencia_inicial,
            vigencia_final=data.vigencia_final,
            contacto=data.contacto,
            direccion=data.direccion,
            telefono=data.telefono,
            clase_fd=data.clase_fd,
            zona_transporte=data.zona_transporte,
            servicio=data.servicio,
            operacion=data.operacion,
            insumo=data.insumo,
            tipo_fd=data.tipo_fd,
            tamanio=data.tamanio,
            modulo=data.modulo,
            rango_inicial=data.rango_inicial,
            rango_final=data.rango_final,
            tarifa=data.tarifa,
            valor_fijo=data.valor_fijo,
            factor_crecimiento=data.factor_crecimiento,
            responsable=data.responsable,
            ciudad=data.ciudad,
            sucursal=data.sucursal,
            centro_costo=data.centro_costo,
            prioridad=data.prioridad,
            created_at=existing.created_at,
            created_by=existing.created_by,
            active=existing.active,
        )
        return self._service.update(id, tarifa)

    def delete(self, id: int) -> TarifaCliente:
        return self._service.delete(id)