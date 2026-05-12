"""
Ejemplo portable para usar el módulo readers en otro proyecto.

Copia toda la carpeta readers/ a tu proyecto y usa `from readers import process_file`.
La config de columnas se define en un JSON (lee config/file_configs.json como referencia).
"""
from pathlib import Path

from readers import process_file


def main():
    # Ajustá estas rutas a tu proyecto
    config = Path("readers/config/file_configs.json")
    archivos = [
        ("datos.csv", config),
        ("reporte.xlsx", config),
        ("desconocido.xyz", config),
        ("/home/nian/Downloads/SR2104000_VIGENCIA_CONTRATOADMIN_SIGLA_20260422163137.csv", config)
    ]

    for ruta, cfg in archivos:
        resultado = process_file(ruta, config_path=cfg, preview_rows=5)

        if resultado.success and resultado.df is not None:
            print(f"[OK] {resultado.file_name}")
            print(f"      config: {resultado.config_id}")
            print(f"      filas:  {resultado.raw_row_count} → {resultado.final_row_count}")
            print(f"      columnas: {list(resultado.df.columns)}")
            print(f"df:\n {resultado.df}")
        else:
            print(f"[ERR] {resultado.file_name}: {resultado.error}")

        print()


if __name__ == "__main__":
    main()
