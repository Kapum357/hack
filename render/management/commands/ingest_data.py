import json
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.contrib.gis.gdal import DataSource
from render.models import FloodThreat, SocialVulnerability


class Command(BaseCommand):
    help = 'Ingest geospatial data from source files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default='data',
            help='Directory containing KML/GeoJSON files (default: data/)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before ingestion'
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting data ingestion...')
        
        data_dir = Path(options['data_dir'])
        
        # Clear existing data if requested
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            FloodThreat.objects.all().delete()
            SocialVulnerability.objects.all().delete()
            self.stdout.write(self.style.WARNING('Existing data cleared'))
        
        # Check if data directory exists
        if not data_dir.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Data directory "{data_dir}" does not exist. Creating sample data...'
                )
            )
            self._create_sample_data()
            self.stdout.write(self.style.SUCCESS('Data ingestion completed with sample data'))
            return
        
        # Process files in data directory
        flood_count = 0
        vuln_count = 0
        
        for file_path in data_dir.glob('*'):
            if file_path.suffix.lower() in ['.geojson', '.json', '.kml']:
                self.stdout.write(f'Processing {file_path.name}...')
                try:
                    if 'flood' in file_path.name.lower() or 'inundacion' in file_path.name.lower():
                        count = self._ingest_flood_data(file_path)
                        flood_count += count
                    elif 'vuln' in file_path.name.lower() or 'social' in file_path.name.lower():
                        count = self._ingest_vulnerability_data(file_path)
                        vuln_count += count
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Skipping {file_path.name} (unclear data type)'
                            )
                        )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error processing {file_path.name}: {str(e)}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Data ingestion completed: {flood_count} flood threats, '
                f'{vuln_count} vulnerability areas'
            )
        )

    def _ingest_flood_data(self, file_path):
        """Ingest flood threat data from GeoJSON or KML file"""
        count = 0
        
        if file_path.suffix.lower() in ['.geojson', '.json']:
            # Read GeoJSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
            
            features = geojson_data.get('features', [])
            for feature in features:
                geometry = self._ensure_multipolygon(
                    GEOSGeometry(json.dumps(feature['geometry']))
                )
                properties = feature.get('properties', {})
                
                FloodThreat.objects.create(
                    name=properties.get('name', f'Flood Area {count + 1}'),
                    description=properties.get('description', ''),
                    threat_level=properties.get('threat_level', 'MEDIUM'),
                    geometry=geometry
                )
                count += 1
        else:
            # Read KML file using GDAL
            ds = DataSource(str(file_path))
            for layer in ds:
                for feature in layer:
                    geometry = self._ensure_multipolygon(feature.geom.geos)
                    
                    FloodThreat.objects.create(
                        name=feature.get('name') or f'Flood Area {count + 1}',
                        description=feature.get('description') or '',
                        threat_level='MEDIUM',
                        geometry=geometry
                    )
                    count += 1
        
        return count

    def _ingest_vulnerability_data(self, file_path):
        """Ingest social vulnerability data from GeoJSON or KML file"""
        count = 0
        
        if file_path.suffix.lower() in ['.geojson', '.json']:
            # Read GeoJSON file
            with open(file_path, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
            
            features = geojson_data.get('features', [])
            for feature in features:
                geometry = self._ensure_multipolygon(
                    GEOSGeometry(json.dumps(feature['geometry']))
                )
                properties = feature.get('properties', {})
                
                SocialVulnerability.objects.create(
                    name=properties.get('name', f'Vulnerability Area {count + 1}'),
                    description=properties.get('description', ''),
                    vulnerability_index=float(properties.get('vulnerability_index', 0.5)),
                    affected_population=int(properties.get('affected_population', 0)),
                    linked_families=int(properties.get('linked_families', 0)),
                    geometry=geometry
                )
                count += 1
        else:
            # Read KML file using GDAL
            ds = DataSource(str(file_path))
            for layer in ds:
                for feature in layer:
                    geometry = self._ensure_multipolygon(feature.geom.geos)
                    
                    SocialVulnerability.objects.create(
                        name=feature.get('name') or f'Vulnerability Area {count + 1}',
                        description=feature.get('description') or '',
                        vulnerability_index=0.5,
                        affected_population=0,
                        linked_families=0,
                        geometry=geometry
                    )
                    count += 1
        
        return count

    def _ensure_multipolygon(self, geometry):
        """Convert geometry to MultiPolygon if needed"""
        if geometry.geom_type == 'Polygon':
            return MultiPolygon(geometry)
        elif geometry.geom_type == 'MultiPolygon':
            return geometry
        else:
            # For points, lines, etc., create a small buffer
            buffered = geometry.buffer(0.001)
            if buffered.geom_type == 'Polygon':
                return MultiPolygon(buffered)
            return buffered

    def _create_sample_data(self):
        """Create sample geospatial data for Soacha"""
        from django.contrib.gis.geos import Polygon, MultiPolygon
        
        # Sample flood threat area (polygon around Soacha center)
        flood_polygon = Polygon((
            (-74.230, 4.570),
            (-74.230, 4.575),
            (-74.225, 4.575),
            (-74.225, 4.570),
            (-74.230, 4.570),
        ))
        
        FloodThreat.objects.create(
            name='Zona Inundable Centro',
            description='Área susceptible a inundaciones en época de lluvias',
            threat_level='HIGH',
            geometry=MultiPolygon(flood_polygon)
        )
        
        # Sample vulnerability area
        vuln_polygon = Polygon((
            (-74.225, 4.575),
            (-74.225, 4.580),
            (-74.220, 4.580),
            (-74.220, 4.575),
            (-74.225, 4.575),
        ))
        
        SocialVulnerability.objects.create(
            name='Zona Vulnerable Norte',
            description='Área con alta vulnerabilidad social',
            vulnerability_index=0.75,
            affected_population=5000,
            linked_families=250,
            geometry=MultiPolygon(vuln_polygon)
        )
        
        self.stdout.write('Sample data created: 1 flood threat, 1 vulnerability area')
