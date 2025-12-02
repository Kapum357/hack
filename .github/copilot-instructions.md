
# Copilot instructions — Proyecto `hack` (sitio estático en Vercel)

Resumen rápido
- Proyecto: sitio estático (HTML/CSS/JS) desplegado en Vercel. La UI principal está en `index.html`; la lógica de cliente vive en `script.js`; estilos en `styles.css`; configuración de Tailwind en `tailwind-config.js`.
- Objetivo del documento: dar a un agente IA lo mínimo necesario para ser productivo aquí (comandos, patrones, riesgos comunes).

Arquitectura y flujo de datos (big picture)
- Contenido estático servido desde la raíz: `index.html` es la entrada principal. No hay framework front-end (single-file pages + Tailwind CDN).
- Interacciones cliente: `script.js` gestiona selección en mapa (`getLatLongFromClick`), carga de archivos (`#dropzone-file`) y persistencia temporal en `localStorage` (`communityReports`).
- Estilos: `styles.css` contiene reglas específicas (overlay de mapa, mensajes). Tailwind se usa vía CDN y `tailwind-config.js` inyecta configuración al runtime de CDN.
- Edge/middleware: el repo puede integrar `@vercel/edge` (dependencia presente). Si existe `middleware.js`, se usa para añadir headers globales (next/rewrite). No asumas siempre su presencia; revisa `middleware.js` antes de editar.
- Backend Python: `app.py` (Flask) proporciona API REST para persistencia de datos (`/api/reports`, `/api/alerts`, `/api/dashboard/layout`), reemplazando localStorage. Datos almacenados en `dashboard_data.json` (para producción, usar base de datos).
- Componentes independientes: múltiples archivos HTML (1-RPaAS.html, 2-CRP.html, etc.) cada uno implementando una funcionalidad específica (predicción de riesgos, reporte comunitario, gestión de datos, dashboard). Cada página tiene JS embebido en `<script>` al final, sin compartir código común.
- Flujo de datos: persistencia servidor vía API REST (Flask), datos compartidos entre páginas vía endpoints. Cliente hace fetch a `/api/*` para CRUD operations.

Comandos y flujo de desarrollo (ejemplos concretos)
- Instalación: `npm install` (para dependencias Node), `pip install -r requirements.txt` (para Python backend)
- Ejecutar local (recomendado para desarrollo con middleware):
	- `vercel login` (si no estás autenticado)
	- `vercel dev` (simula entorno Vercel; usa `--listen <puerto>` si necesitas otro puerto)
	- `python app.py` (ejecuta servidor Flask en localhost:5000 para backend completo)
- Despliegue: `vercel --prod` o push a `main` si está conectado al proyecto en Vercel (para frontend estático); para backend, desplegar Flask en servicio como Heroku o Railway.

Notas importantes sobre Vercel y configuración
- `vercel.json` actual: uses `framework: null`, `buildCommand: null`, `outputDirectory: "."` — esto sirve archivos desde la raíz y salta paso de build.
- `package.json` debe contener un `build` script (Vercel lo espera). En este repo hay un `build` que imprime "Static site - no build required"; no lo reemplaces por `vercel dev` (evita invocar `vercel dev` recursivamente desde `npm run dev`).
- Si añades `dev` script, evita `"vercel dev"` dentro del `package.json` (genera invocación recursiva). Preferir usar la CLI directamente.

Patrones y convenciones del proyecto
- Servir desde la raíz: las rutas en `index.html` asumen archivos en la raíz (`script.js`, `styles.css`, `tailwind-config.js`). Si mueves archivos, actualiza rutas.
- Persistencia cliente simple: `localStorage` con clave `communityReports` — útil para prototipos; para producción se espera un backend separado.
- JS embebido: lógica en `<script>` al final de cada HTML, no en archivos separados (excepto `script.js` que no se usa).
- IDs específicos: elementos clave tienen IDs fijos (`map`, `reportForm`, `dropzone-file`, `latitude`, `longitude`, `alerts-container`).
- Mapas interactivos: usa Leaflet.js para mapas, con marcadores, polígonos de riesgo y clics para selección de ubicación.
- Gráficos: Chart.js para barras y líneas en dashboard.
- Evita añadir grandes `node_modules` al repositorio; Vercel instala dependencias vía `npm install` según `installCommand`.

Puntos que un agente IA debe vigilar antes de editar
- Verificar que `index.html` siga siendo la entrada; cambios en su estructura afectarán `script.js` (IDs: `map`, `reportForm`, `dropzone-file`, `latitude`, `longitude`).
- Antes de tocar middleware, revisar si `middleware.js` existe y cuál es su contrato con `@vercel/edge` (ej.: uso de `next({ headers: {...} })`).
- No cambiar `vercel.json` sin motivo — es la razón por la que el sitio no requiere build. Cambios aquí afectan despliegues.
- Al editar páginas HTML independientes, mantener consistencia en estilos y JS embebido.
- Para mapas: inicializar con `L.map('map').setView([4.58, -74.21], 13)` centrado en Soacha.
- Para datos: usar localStorage para compartir entre páginas; claves específicas como `communityReports`.

Errores y trampas comunes (qué revisar si algo falla)
- Si `vercel dev` falla: comprobar `package.json` tiene `build` script y que no hay `dev` que invoque `vercel dev`.
- Conflicto de puerto: usar `vercel dev --listen <puerto>` o cerrar procesos que ocupen `3000`.
- Rutas rotas: las referencias CDN (Tailwind, Google Fonts, Material Symbols) están en `index.html`; si trabajas offline, ten en cuenta dependencias externas.
- JS no funciona: verificar que `<script>` esté al final del `<body>`, después de elementos DOM.
- Mapas no cargan: asegurar Leaflet CSS y JS incluidos, y div con ID `map` presente.

Referencias rápidas (archivos clave)
- `index.html`: estructura y referencias a assets
- `script.js`: lógica de formulario, mapa, validación y `localStorage`
- `styles.css`: reglas específicas (map overlay, mensajes)
- `tailwind-config.js`: configuración aplicada al runtime CDN
- `vercel.json` / `package.json`: controlan comportamiento de build/dev
- `app.py`: servidor Flask con API REST para persistencia
- `requirements.txt`: dependencias Python
- Páginas componentes: `1-RPaAS.html` (predicción de riesgos), `2-CRP.html` (reporte comunitario), `3-DMaF.html` (gestión de datos), etc.

¿Algo que falta o que quieres que aclare? Responde con áreas concretas (por ejemplo: pruebas, CI, añadir una API para persistencia), y actualizo el documento.
