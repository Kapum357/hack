# RCU Soacha - Sistema de Resiliencia Climática Urbana

**Herramienta interactiva para análisis de vulnerabilidad climática y alerta preventiva en Soacha, Colombia**

## Inicio Rápido

### Requisitos
- Python 3.12+
- Navegador moderno (Chrome, Firefox, Edge, Safari)
- Conexión a internet (para datos climáticos)

### Instalación (Desarrollo Local)

```bash
# 1. Clonar o descargar el proyecto
git clone https://github.com/Kapum357/hack.git
cd hack

# 2. Crear entorno virtual
python -m venv .venv

# Activar (Linux/Mac)
source .venv/bin/activate

# Activar (Windows)
.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar servidor
python app.py

# 5. Acceder
# Frontend: http://localhost:5000/dashboard-resilience.html
# API: http://localhost:5000/api/weather
```

## Interfaces Disponibles

### 1. **Dashboard Principal** (`dashboard-resilience.html`)
**Uso:** Visualización general de riesgo y análisis

- Métricas clave (población en riesgo, zonas críticas, reportes)
- Mapa con zonas de vulnerabilidad
- Panel de análisis por zona
- Alertas preventivas
- Condiciones climáticas actuales
- Gráficos de distribución poblacional

**Cómo usar:**
1. Abre `http://localhost:5000/dashboard-resilience.html`
2. Observa mapa con zonas coloreadas
3. Haz clic en zona para ver detalles de riesgo
4. Lee alertas en panel derecho
5. Botón "Actualizar" para refrescar datos

### 2. **Reporte Comunitario** (`2-CRP.html`)
**Uso:** Registro de eventos por ciudadanos

- Selecciona tipo de evento
- Ubica en mapa (click para coordenadas)
- Ingresa estimación de afectados
- Carga fotos/videos
- Envía reporte

**Cómo usar:**
1. Abre `http://localhost:5000/2-CRP.html`
2. Selecciona "Tipo de Evento" (ej: Inundación)
3. Haz clic en el mapa para establecer ubicación
4. Ingresa población afectada
5. Carga fotos adjuntas
6. Click en "Enviar Reporte"

### 3. **Gestión de Datos** (`3-DMaF.html`)
**Uso:** Filtrado y análisis de datos de campo

- Filtros por período, zona, capas de datos
- Tablas de vulnerabilidad y riesgo
- Exportación de datos

---

## Datos de Ejemplo

### Zonas de Vulnerabilidad Pre-configuradas

| Zona | Ubicación | Riesgo | Población |
|------|-----------|--------|-----------|
| Danubio | 4.57, -74.22 | Alto | 3,200 |
| La María | 4.60, -74.19 | Medio | 2,100 |
| Zona 1 | 4.58, -74.21 | Alto | 2,500 |
| Zona 2 | 4.59, -74.20 | Medio | 1,800 |

### Tipos de Evento Soportados
- 🌊 **Inundación** - Desbordamientos de agua
- 🏔️ **Deslizamiento** - Movimientos de tierra
- 🏢 **Daño Infraestructura** - Daños a viviendas/servicios
- 🆘 **Necesidad Comunitaria** - Solicitudes de ayuda

### Reglas de Alertas Automáticas

```
Ola de Calor (ROJO):        Temperatura > 33°C
Riesgo Alto Inundación:    Precipitación > 15mm
Advertencia Inundación:    Precipitación > 5mm
Humedad Crítica:            Humedad > 85%
Patrón de Riesgo:           > 3 eventos similares en 30 días
```

---

## Ejemplos de Casos de Uso

### Caso 1: Identificar Zona Crítica

1. **Abrir dashboard:** `dashboard-resilience.html`
2. **Observar:** Círculos rojos más grandes = riesgo alto
3. **Click en zona:** Ver detalles (población, score de riesgo)
4. **Conclusión:** El Danubio necesita intervención prioritaria

### Caso 2: Reportar Evento Ciudadano

1. **Abrir:** `2-CRP.html`
2. **Evento:** Seleccionar "Inundación"
3. **Ubicación:** Click en mapa (obtiene lat/long automáticamente)
4. **Afectados:** Ingresar 250 personas
5. **Fotos:** Adjuntar 2 imágenes
6. **Enviar:** Sistema registra automáticamente en base de datos

### Caso 3: Análisis de Impacto

```bash
# 1. Obtener datos poblacionales
curl http://localhost:5000/api/population-stats > stats.json

# 2. Abrir stats.json en Excel/JSON viewer
# 3. Análisis: 1,200 personas afectadas por inundaciones en 30 días
# 4. Conclusión: Mayor inversión en drenaje en El Danubio
```

---

## Configuración Avanzada

### Cambiar API Key de OpenWeather

```python
# En app.py
WEATHER_API_KEY = 'tu_api_key_aqui'

# Obtener en: https://openweathermap.org/api
```

### Agregar Nueva Zona de Vulnerabilidad

```python
# En app.py, agregar a VULNERABILITY_ZONES:
'tu_zona': {
    'lat': 4.58,
    'lng': -74.21,
    'risk_level': 'high',  # high|medium|low
    'population': 2000
}
```

### Cambiar Umbrales de Alertas

```python
# En app.py, función generate_alerts():
if temp > 35:  # Cambiar de 33 a 35
    alerts.append(...)

if precipitation > 20:  # Cambiar de 15 a 20
    alerts.append(...)
```

---

## 🐛 Troubleshooting

### Error: "No module named 'geopandas'"
```bash
pip install geopandas fiona shapely
```

### Error: "Address already in use"
```bash
# El puerto 5000 está ocupado
# Opción 1: Liberar puerto
lsof -ti:5000 | xargs kill -9

# Opción 2: Usar otro puerto
python app.py --port 8000
```

### API retorna 404
```
Asegurate que Flask está corriendo:
python app.py

Y accede a:
http://localhost:5000/api/weather
```

### Mapa no carga
- Verifica conexión a internet
- Leaflet.js debe cargarse desde CDN
- Abre consola (F12) para ver errores
