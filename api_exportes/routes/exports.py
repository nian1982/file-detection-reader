from fastapi import APIRouter, Depends
from api_exportes.schemas.export_schema import ExportResponse
from api_exportes.controllers.export_controller import ExportController
from api_exportes.dependencies import get_export_controller
from shared.security.dependencies import require_client_role

router = APIRouter(prefix="/exports", tags=["exports"])


@router.get(
    "/plantilla/{nombre}",
    response_model=list[ExportResponse],
)
def export_by_plantilla(
    nombre: str,
    controller: ExportController = Depends(get_export_controller),
    user=Depends(require_client_role("api-exportes", "exports.read")),
):
    return controller.export_by_plantilla(nombre)
