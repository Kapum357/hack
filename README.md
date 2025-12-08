## Soacha Climate Resilience Application

This application provides geospatial visualization for climate resilience data in Soacha, Colombia, including:
- **Flood threat areas** (Amenaza de Inundación)
- **Social vulnerability zones** (Vulnerabilidad Social)

### Features

- Interactive Leaflet map centered on Soacha
- Toggle-able information layers
- Statistics dashboard (affected population, linked families)
- Geospatial data ingestion from GeoJSON and KML files
- PostGIS-powered spatial database

### Data Ingestion

The application includes a Django management command for ingesting geospatial data:

```bash
# Import data from the default 'data/' directory
python manage.py ingest_data

# Import from a custom directory
python manage.py ingest_data --data-dir /path/to/data

# Clear existing data before import
python manage.py ingest_data --clear
```

Place your GeoJSON or KML files in the `data/` directory with appropriate naming:
- Files containing "flood" or "inundacion" → Flood threat data
- Files containing "vuln" or "social" → Social vulnerability data

See `data/README.md` for detailed file format specifications.

## Deployment on Render

Fork the repo and use the button below to deploy this app with one click.

<a href="https://render.com/deploy" referrerpolicy="no-referrer-when-downgrade" rel="nofollow">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render" />
</a>

To deploy manually, see the guide at https://docs.render.com/deploy-django.
