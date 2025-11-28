# Guía de Contribución

Gracias por tu interés en contribuir a Codilinks. Este documento explica cómo proponer cambios y mantener la calidad del proyecto.

## Requisitos previos
- Python 3.10+ y `venv` para aislar dependencias.
- Instalar dependencias con `venv\Scripts\pip.exe install -r requirements.txt`.

## Flujo de trabajo recomendado
1. Crea un branch desde `main` para tu cambio.
2. Asegúrate de que la app corre localmente (`link.py`).
3. Si afecta al empaquetado, prueba `build_link.bat` y verifica `dist/Link.exe`.
4. Actualiza documentación en `README.md` o `docs/` si aplica.
5. Envía PR describiendo claramente el cambio y motivación.

## Estilo y prácticas
- Mantén los cambios acotados y con nombres claros en variables y funciones.
- Evita introducir dependencias innecesarias.
- No incluyas archivos generados (`dist/`, `build/`) en commits.

## Reporte de Issues
Incluye pasos para reproducir, entorno, logs relevantes y capturas si aplica.

