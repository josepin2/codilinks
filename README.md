# Codilinks

[![Build](https://github.com/josepin2/codilinks/actions/workflows/build.yml/badge.svg)](https://github.com/josepin2/codilinks/actions/workflows/build.yml)

Aplicación para codificar/transformar enlaces en Windows, con interfaz GUI basada en `customtkinter`. Incluye script de empaquetado para generar un ejecutable offline (`Link.exe`) sin necesidad de tener Python instalado.

## Características
- Interfaz gráfica con `customtkinter`.
- Empaquetado en un único ejecutable (`--onefile`) usando PyInstaller.
- Modo sin consola (`--noconsole`) para una experiencia limpia en GUI.
- Soporte opcional de icono (`icon.ico`).

## Estructura del proyecto
```
codilinks/
├─ link.py                # Entrada principal de la app GUI
├─ codificador_enlaces.py # Módulo/funciones auxiliares
├─ build_link.bat         # Script para generar el ejecutable offline
├─ requirements.txt       # Dependencias (customtkinter, etc.)
├─ dist/                  # Salida del ejecutable (Link.exe)
├─ build/                 # Artefactos temporales de PyInstaller
└─ docs/                  # Documentación adicional
```

## Requisitos
- Windows 10/11.
- Python 3.10+ (solo para desarrollo/compilación).
- Entorno virtual recomendado (`venv`).

Instala dependencias (en el venv):
```
venv\Scripts\pip.exe install -r requirements.txt
```

## Uso en desarrollo
Ejecuta la aplicación directamente:
```
venv\Scripts\python.exe link.py
```

## Generar el ejecutable offline
El proyecto incluye `build_link.bat` para compilar a un ejecutable único sin consola.

Pasos:
1. Asegúrate de tener las dependencias instaladas en el venv.
2. Doble clic en `build_link.bat` (o ejecuta `./build_link.bat`).
3. Al finalizar, encontrarás `dist/Link.exe`.

Opciones:
- Icono: coloca `icon.ico` junto al `.bat` y se aplicará automáticamente.
- Si necesitas ver la consola por depuración, edita el `.bat` y elimina `--noconsole`.

## Descargas
- Descarga la última versión del ejecutable desde la página de Releases:
  `https://github.com/josepin2/codilinks/releases`
- Los builds de CI suben un artefacto `Link.exe` por cada push/PR a `main`.

## Publicación en GitHub
Este repositorio está preparado para ser versionado con `git` y subido a GitHub.

Pasos típicos (requiere tener `git` y/o `gh` configurado):
```
git init
git add .
git commit -m "Inicializa repo con documentación y build script"
git branch -M main

# Opción A: usando GitHub CLI (gh)
gh auth status           # Asegúrate de estar autenticado
gh repo create codilinks --source . --public --remote origin --push

# Opción B: manual con git (reemplaza USUARIO por tu nombre de usuario)
git remote add origin https://github.com/USUARIO/codilinks.git
git push -u origin main
```

## Automatización de releases
Cada vez que se crea un tag con formato `v*` (por ejemplo, `v0.1.0`), se ejecuta un workflow que:
- Compila el `Link.exe` en Windows.
- Crea una Release en GitHub y adjunta el ejecutable como asset.

Para publicar una versión:
```
git tag v0.1.0
git push origin v0.1.0
```

## Solución de problemas
- Si el ejecutable no se genera, revisa las rutas y dependencias. Prueba:
  `venv\Scripts\pip.exe install -r requirements.txt`.
- Para incluir archivos extra (p.ej. `assets/`), añade al comando de PyInstaller:
  `--add-data "assets;assets"` en Windows.
- Si tu antivirus bloquea el `.exe`, firma el binario o añade excepción.

## Contribución
Consulta `docs/CONTRIBUTING.md` para la guía de contribución.

## Licencia
No se ha definido una licencia específica. Si planeas publicar públicamente, considera añadir una licencia (MIT, Apache-2.0, etc.).
