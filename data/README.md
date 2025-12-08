# Data Directory

This directory contains geospatial data files for the Soacha Climate Resilience application.

## Supported File Formats

- **GeoJSON** (`.geojson`, `.json`)
- **KML** (`.kml`)

## File Naming Conventions

The ingestion command automatically categorizes files based on their names:

### Flood Threat Data
Files containing "flood" or "inundacion" in their name will be imported as flood threat areas.

Example: `flood_inundacion.geojson`, `flood_zones.kml`

**Required/Optional Properties:**
- `name`: Name of the flood area (optional, auto-generated if missing)
- `description`: Description of the area (optional)
- `threat_level`: One of "LOW", "MEDIUM", "HIGH", "VERY_HIGH" (optional, defaults to "MEDIUM")

### Social Vulnerability Data
Files containing "vuln" or "social" in their name will be imported as social vulnerability areas.

Example: `social_vulnerability.geojson`, `vulnerable_areas.kml`

**Required/Optional Properties:**
- `name`: Name of the area (optional, auto-generated if missing)
- `description`: Description of the area (optional)
- `vulnerability_index`: Float value from 0 to 1 (optional, defaults to 0.5)
- `affected_population`: Number of people affected (optional, defaults to 0)
- `linked_families`: Number of families linked to Red Cross programs (optional, defaults to 0)

## Example GeoJSON Structure

### Flood Threat Example
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Zona Inundable Río Bogotá",
        "description": "Área propensa a inundaciones",
        "threat_level": "HIGH"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-74.230, 4.570], [-74.230, 4.575], ...]]
      }
    }
  ]
}
```

### Social Vulnerability Example
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Zona Vulnerable Compartir",
        "description": "Área con alta vulnerabilidad social",
        "vulnerability_index": 0.85,
        "affected_population": 3500,
        "linked_families": 175
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[-74.225, 4.575], [-74.225, 4.580], ...]]
      }
    }
  ]
}
```

## Usage

### Import Data
```bash
python manage.py ingest_data
```

### Import from Custom Directory
```bash
python manage.py ingest_data --data-dir /path/to/data
```

### Clear Existing Data Before Import
```bash
python manage.py ingest_data --clear
```

## Notes

- If the data directory doesn't exist, the command will create sample data for Soacha.
- All geometries are stored in SRID 4326 (WGS 84) coordinate system.
- Point and LineString geometries are automatically buffered to create polygon areas.
- Polygon geometries are converted to MultiPolygon for consistency.
