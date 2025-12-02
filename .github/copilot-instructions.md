# Copilot instructions — Proyecto `hack`

Resumen breve
- Repositorio: sitio estático + API prototipo en Flask. Entrada principal: `index.html`. Frontend sin framework (HTML + Tailwind CDN + Leaflet/Chart.js). Backend mínimo en `app.py` que expone `/api/*`.

Qué necesita saber un agente IA
- Estructura clave: archivos estáticos en la raíz, páginas independientes (`1-RPaAS.html`, `2-CRP.html`, `3-DMaF.html`, `5-IGD.html`, `4-Photos.html`), y API en `app.py`.
- Flujo de datos: el cliente puede usar `localStorage` (clave `communityReports`) o la API Flask (`/api/reports`, `/api/alerts`, `/api/photos`, `/api/infografias`).
- Convención de frontend: la mayor parte del JS está embebido al final de cada HTML. Si extraes código, actualiza todas las páginas que lo referencien.

Comandos y workflows (prácticos)
- Instalación:
  - Python: `pip install -r requirements.txt`
  - Node (solo dev tools): `npm install`
- Ejecutar local:
  - Backend: `python app.py` (Flask en debug, puerto 5000)
  - Simular Vercel: `vercel dev --listen <puerto>` (opcional)
- Pruebas rápidas:
  - `bash test_photos_api.sh` — script E2E para el Photos API (si está presente).

Reglas y gotchas del proyecto
- No insertar `vercel dev` dentro del `package.json` como `dev` script (evita recursión). Mantén `build` para Vercel.
- El sitio sirve desde la raíz: mover archivos requiere actualizar rutas en `index.html` y otras páginas.
- IDs clave que aparecen en muchos archivos: `map`, `reportForm`, `dropzone-file`, `latitude`, `longitude`, `alerts-container`. Cambiarlos rompe múltiples páginas.
- No subir `node_modules` ni grandes binarios; usa `assets/` para recursos y migra a almacenamiento externo en producción.

Integraciones y puntos de extensión
- Backend/API: revisar `app.py` para ver rutas y handlers actuales (por ejemplo `/api/photos/*`, `/api/infografias`). Evitar cambios en la API sin pruebas.
- Fotos y metadatos: `assets/3. Fotografías y videos de referencia/` contiene imágenes y `metadata.json` usado por el Photos API.
- Mapas: Leaflet se inicializa típicamente con `L.map('map').setView([4.58, -74.21], 13)` (Soacha).

Archivos que revisar primero
- `index.html`, `app.py`, `requirements.txt`, `vercel.json`, `package.json`, `tailwind.config.cjs`, `assets/`.

Proceso recomendado para cambios no triviales
1. Reproducir local: `pip install -r requirements.txt` → `python app.py` → abrir `http://127.0.0.1:5000`.
2. Validar endpoints con `curl` o `test_photos_api.sh` antes de tocar el frontend.
3. Cambios en HTML: editar la página y verificar que `<script>` esté después del DOM (final del `body`).
4. Para despliegue, usar la CLI de Vercel (`vercel --prod`) en lugar de modificar `package.json`.

Detalles útiles detectados en el código
- `dashboard_data.json` (persistencia ligera usada por algunos endpoints).
- `assets/2. Resultados CRMC infografías/` contiene PDFs referenciados por el dashboard.
- Existen páginas independientes que no comparten un sistema de componentes; buscar lógica duplicada si se refactoriza.
