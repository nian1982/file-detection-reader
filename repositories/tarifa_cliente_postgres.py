from datetime import date as date_type
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from config import get_settings
from models.tarifa_cliente import TarifaCliente
from repositories.tarifa_cliente_repository import TarifaClienteRepository


class PostgresTarifaClienteRepository(TarifaClienteRepository):
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

    def _dict_to_tarifa(self, row: dict) -> TarifaCliente:
        return TarifaCliente(
            id=row["id"],
            cliente=row["cliente"],
            identificacion=row.get("identificacion"),
            contrato=row.get("contrato"),
            activo=row["activo"],
            vigencia_inicial=row["vigencia_inicial"],
            vigencia_final=row.get("vigencia_final"),
            contacto=row.get("contacto"),
            direccion=row.get("direccion"),
            telefono=row.get("telefono"),
            clase_fd=row.get("clase_fd"),
            zona_transporte=row.get("zona_transporte"),
            servicio=row.get("servicio"),
            operacion=row.get("operacion"),
            insumo=row.get("insumo"),
            tipo_fd=row.get("tipo_fd"),
            tamanio=row.get("tamanio"),
            modulo=row.get("modulo"),
            rango_inicial=row.get("rango_inicial"),
            rango_final=row.get("rango_final"),
            tarifa=row.get("tarifa"),
            valor_fijo=row.get("valor_fijo"),
            factor_crecimiento=row.get("factor_crecimiento"),
            responsable=row.get("responsable"),
            ciudad=row.get("ciudad"),
            sucursal=row.get("sucursal"),
            centro_costo=row.get("centro_cosoto"),
            prioridad=row.get("prioridad"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
            created_by=row.get("created_by"),
            active=row.get("active", True),
        )

    def find_by_filters(
            self,
            ciudad: Optional[str] = None,
            cliente: Optional[str] = None,
            fecha: Optional[date_type] = None,
        ) -> list[TarifaCliente]:
        conditions = []
        params = []

        conditions.append("TRIM(activo) = 'SI'")

        if ciudad:
            conditions.append("ciudad = %s")
            params.append(ciudad.upper())

        if cliente:
            conditions.append("UPPER(cliente) LIKE %s")
            params.append(f"%{cliente.upper()}%")

        if fecha:
            conditions.append("vigencia_inicial <= %s")
            conditions.append("COALESCE(vigencia_final, %s) >= %s")
            params.extend([fecha, fecha, fecha])

        query = "SELECT * FROM tarifas_cliente"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        rows = self._execute(query, tuple(params))
        return [self._dict_to_tarifa(dict(r)) for r in rows]

    def get_by_id(self, id: int) -> Optional[TarifaCliente]:
        query = "SELECT * FROM tarifas_cliente WHERE id = %s"
        rows = self._execute(query, (id,))
        return self._dict_to_tarifa(dict(rows[0])) if rows else None

    def create(self, tarifa: TarifaCliente) -> TarifaCliente:
        query = """
            INSERT INTO tarifas_cliente (
                cliente, identificacion, contrato, vigencia_inicial, vigencia_final,
                contacto, direccion, telefono, clase_fd, zona_transporte,
                servicio, operacion, insumo, tipo_fd, tamanio, modulo,
                rango_inicial, rango_final, tarifa, valor_fijo, factor_crecimiento,
                responsable, ciudad, sucursal, centro_cosoto, prioridad, activo, created_by
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, 'SI', %s
            )
            RETURNING id
        """
        params = (
            tarifa.cliente, tarifa.identificacion, tarifa.contrato, tarifa.vigencia_inicial,
            tarifa.vigencia_final, tarifa.contacto, tarifa.direccion, tarifa.telefono,
            tarifa.clase_fd, tarifa.zona_transporte, tarifa.servicio, tarifa.operacion,
            tarifa.insumo, tarifa.tipo_fd, tarifa.tamanio, tarifa.modulo,
            tarifa.rango_inicial, tarifa.rango_final, tarifa.tarifa,
            tarifa.valor_fijo, tarifa.factor_crecimiento, tarifa.responsable,
            tarifa.ciudad, tarifa.sucursal, tarifa.centro_costo,
            tarifa.prioridad, tarifa.created_by,
        )
        rows = self._execute(query, params)
        return self._dict_to_tarifa(dict(rows[0]))

    def update(self, id: int, tarifa: TarifaCliente) -> TarifaCliente:
        query = """
            UPDATE tarifas_cliente SET
                cliente=%s, identificacion=%s, contrato=%s,
                vigencia_inicial=%s, vigencia_final=%s,
                contacto=%s, direccion=%s, telefono=%s,
                updated_at=NOW()
            WHERE id=%s
            RETURNING id
        """
        rows = self._execute(query, (
            tarifa.cliente, tarifa.identificacion, tarifa.contrato,
            tarifa.vigencia_inicial, tarifa.vigencia_final,
            tarifa.contacto, tarifa.direccion, tarifa.telefono, id,
        ))
        return self._dict_to_tarifa(dict(rows[0]))

    def delete(self, id: int) -> TarifaCliente:
        query = "UPDATE tarifas_cliente SET activo='NO' WHERE id=%s RETURNING *"
        rows = self._execute(query, (id,))
        if not rows:
            raise ValueError(f"Tarifa {id} no encontrada")
        return self._dict_to_tarifa(dict(rows[0]))