"""
Flask Web Application for Climate Resilience Analysis
Integrates geospatial data, climate analysis, and interactive visualizations.

This application provides a comprehensive web interface for viewing, analyzing,
and understanding climate vulnerability and resilience metrics for Soacha zones.
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import pandas as pd
import geopandas as gpd
import logging
from datetime import datetime
import json
from typing import Dict, Optional
from shapely.geometry import Point

# Import custom modules
from geospatial_integration import SoachaGeospatialDatabase
from climate_data_integration import ClimateDataIntegrator
from visualization_module import InteractiveMapVisualizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ResilienceAnalysisApp:
    """
    Flask-based web application for climate resilience analysis in Soacha.
    Provides REST API endpoints and interactive dashboard interface.
    """

    def __init__(self, app_name: str = "Soacha Climate Resilience Platform",
                 debug: bool = False):
        """
        Initialize the resilience analysis application.

        Args:
            app_name: Application name
            debug: Enable debug mode
        """
        self.app = Flask(app_name)
        self.app.config['JSON_SORT_KEYS'] = False

        # Enable CORS for cross-origin requests
        CORS(self.app)

        # Initialize data systems
        self.geo_db = SoachaGeospatialDatabase()
        self.climate_integrator = None  # Will be initialized with API key
        self.map_visualizer = None

        # Application state
        self.loaded_data = {}

        # Register routes
        self._register_routes()

        logger.info(f"{app_name} initialized successfully")

    def index(self):
        """Main dashboard page."""
        return jsonify({
            'status': 'success',
            'message': 'Soacha Climate Resilience Analysis Platform',
            'version': '1.0.0',
            'endpoints': {
                'zones': '/api/zones',
                'vulnerability': '/api/vulnerability/<zone>',
                'climate': '/api/climate/<zone>',
                'map': '/api/map/interactive',
                'health': '/api/health',
                'data_integration': '/api/data/status'
            }
        })

    def get_zones(self):
        """Retrieve all geographic zones."""
        try:
            zones_info = {}
            for zone_name in self.geo_db.zones.keys():
                summary = self.geo_db.get_zone_summary_statistics(zone_name)
                zones_info[zone_name] = summary

            return jsonify({
                'status': 'success',
                'zones': zones_info,
                'count': len(zones_info),
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Error retrieving zones: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    def get_zone_detail(self, zone_name: str):
        """Retrieve detailed information for a specific zone."""
        try:
            if zone_name not in self.geo_db.zones:
                return jsonify({
                    'status': 'error',
                    'message': f'Zone {zone_name} not found'
                }), 404

            # Create and return zone GeoDataFrame
            self.geo_db.create_zone_geodataframe(zone_name)
            summary = self.geo_db.get_zone_summary_statistics(zone_name)

            return jsonify({
                'status': 'success',
                'zone': zone_name,
                'summary': summary,
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Error retrieving zone detail: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    def get_vulnerability_analysis(self, zone_name: str):
        """Retrieve vulnerability index and analysis for a zone."""
        try:
            if zone_name not in self.geo_db.zones:
                return jsonify({
                    'status': 'error',
                    'message': f'Zone {zone_name} not found'
                }), 404

            # Create zone GeoDataFrame if not exists
            if f'avca_{zone_name}' not in self.geo_db.geodataframes:
                # Load sample AVCA data
                sample_data = self._generate_sample_avca_data(zone_name)
                self.geo_db.load_avca_assessment_data(zone_name, sample_data)

            # Calculate vulnerability
            vuln_df = self.geo_db.calculate_vulnerability_index(zone_name)

            if vuln_df is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to calculate vulnerability index'
                }), 500

            # Prepare response data
            vulnerability_summary = {
                'zone': zone_name,
                'total_locations': len(vuln_df),
                'avg_vulnerability_index': float(vuln_df['vulnerability_index'].mean()),
                'max_vulnerability_index': float(vuln_df['vulnerability_index'].max()),
                'min_vulnerability_index': float(vuln_df['vulnerability_index'].min()),
                'std_deviation': float(vuln_df['vulnerability_index'].std()),
                'risk_distribution': vuln_df['risk_category'].value_counts().to_dict(),
                'high_risk_count': len(vuln_df[vuln_df['vulnerability_index'] > 0.7])
            }

            return jsonify({
                'status': 'success',
                'vulnerability': vulnerability_summary,
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Error in vulnerability analysis: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    def get_climate_analysis(self, zone_name: str):
        """Retrieve climate data and analysis for a zone."""
        try:
            if self.climate_integrator is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Climate integrator not initialized. Set API key.'
                }), 503

            # Get climate data
            report = self.climate_integrator.generate_climate_resilience_report(zone_name)

            return jsonify({
                'status': 'success',
                'climate_report': report,
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Error in climate analysis: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    def get_interactive_map(self):
        """Generate and return interactive vulnerability map."""
        try:
            # Initialize map visualizer
            self.map_visualizer = InteractiveMapVisualizer(
                center_coordinates=(4.7768, -74.1647),
                zoom_level=13
            )

            # Create base map
            self.map_visualizer.create_base_map(
                map_name="Soacha Climate Resilience Map",
                tile_provider="OpenStreetMap"
            )

            # Add zone boundaries
            self.map_visualizer.add_zone_boundaries(self.geo_db.zones)

            # Add vulnerability data for each zone
            for zone_name in self.geo_db.zones.keys():
                if f'avca_{zone_name}' not in self.geo_db.geodataframes:
                    sample_data = self._generate_sample_avca_data(zone_name)
                    self.geo_db.load_avca_assessment_data(zone_name, sample_data)

                vuln_df = self.geo_db.calculate_vulnerability_index(zone_name)
                if vuln_df is not None:
                    vuln_gdf = gpd.GeoDataFrame(vuln_df, geometry=[Point(xy) for xy in zip(vuln_df.longitude, vuln_df.latitude)])
                    vuln_gdf.crs = "EPSG:4326"
                    self.map_visualizer.add_vulnerability_heatmap(vuln_gdf)

            # Add utility features
            self.map_visualizer.add_measurement_scale()
            self.map_visualizer.add_fullscreen_button()

            # Get map HTML
            map_html = self.map_visualizer.get_map_html()

            if map_html is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to generate map'
                }), 500

            return jsonify({
                'status': 'success',
                'map_html': map_html,
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Error generating interactive map: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    def health_check(self):
        """System health check endpoint."""
        health_status = {
            'status': 'operational',
            'geospatial_db': 'initialized' if self.geo_db else 'not_initialized',
            'climate_integrator': 'initialized' if self.climate_integrator else 'not_initialized',
            'timestamp': datetime.now().isoformat()
        }

        return jsonify(health_status)

    def data_integration_status(self):
        """Check data integration and loading status."""
        status = {
            'zones_initialized': len(self.geo_db.zones),
            'geodataframes_loaded': len(self.geo_db.geodataframes),
            'vulnerability_analyses': len(self.geo_db.vulnerability_scores),
            'climate_data_cached': len(self.climate_integrator.climate_cache) if self.climate_integrator else 0,
            'timestamp': datetime.now().isoformat()
        }

        return jsonify({
            'status': 'success',
            'data_integration': status
        })

    def initialize_system(self):
        """Initialize all data systems and load base data."""
        try:
            for zone_name in self.geo_db.zones.keys():
                self.geo_db.create_zone_geodataframe(zone_name)
                sample_data = self._generate_sample_avca_data(zone_name)
                self.geo_db.load_avca_assessment_data(zone_name, sample_data)
                self.geo_db.calculate_vulnerability_index(zone_name)

            return jsonify({
                'status': 'success',
                'message': 'System initialized successfully',
                'zones_processed': len(self.geo_db.zones)
            })

        except Exception as e:
            logger.error(f"Error during system initialization: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500

    def _register_routes(self) -> None:
        """Register all Flask application routes."""
        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.app.add_url_rule('/api/zones', 'get_zones', self.get_zones, methods=['GET'])
        self.app.add_url_rule('/api/zones/<zone_name>', 'get_zone_detail', self.get_zone_detail, methods=['GET'])
        self.app.add_url_rule('/api/vulnerability/<zone_name>', 'get_vulnerability_analysis', self.get_vulnerability_analysis, methods=['GET'])
        self.app.add_url_rule('/api/climate/<zone_name>', 'get_climate_analysis', self.get_climate_analysis, methods=['GET'])
        self.app.add_url_rule('/api/map/interactive', 'get_interactive_map', self.get_interactive_map, methods=['GET'])
        self.app.add_url_rule('/api/health', 'health_check', self.health_check, methods=['GET'])
        self.app.add_url_rule('/api/data/status', 'data_integration_status', self.data_integration_status, methods=['GET'])
        self.app.add_url_rule('/api/initialize', 'initialize_system', self.initialize_system, methods=['POST'])

    @staticmethod
    def _generate_sample_avca_data(zone_name: str, num_points: int = 50) -> pd.DataFrame:
        """
        Generate sample AVCA assessment data for demonstration.

        Args:
            zone_name: Zone name for data generation
            num_points: Number of data points to generate

        Returns:
            DataFrame: Sample AVCA data
        """
        import numpy as np
        from shapely.geometry import Point

        zone_center = {
            'El Danubio': (4.7810, -74.1680),
            'La María': (4.7750, -74.1620)
        }

        center_lat, center_lon = zone_center.get(zone_name, (4.7768, -74.1647))

        # Generate random points around zone center
        lats = np.random.normal(center_lat, 0.02, num_points)
        lons = np.random.normal(center_lon, 0.02, num_points)

        data = {
            'latitude': lats,
            'longitude': lons,
            'building_count': np.random.randint(1, 20, num_points),
            'access_to_water': np.random.uniform(0, 1, num_points),
            'vegetation_coverage': np.random.uniform(0, 100, num_points),
            'drainage_quality': np.random.uniform(0, 1, num_points),
            'slope_degree': np.random.uniform(0, 30, num_points),
            'distance_to_evacuation': np.random.uniform(0.1, 5, num_points),
            'assessment_date': datetime.now().isoformat()
        }

        return pd.DataFrame(data)

    def initialize_climate_api(self, openweather_api_key: str) -> bool:
        """
        Initialize climate data integrator with API credentials.

        Args:
            openweather_api_key: OpenWeather API key

        Returns:
            bool: True if successful
        """
        try:
            self.climate_integrator = ClimateDataIntegrator(openweather_api_key)
            logger.info("Climate API initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Error initializing climate API: {str(e)}")
            return False

    def run(self, host: str = '127.0.0.1', port: int = 5000, debug: bool = False):
        """
        Run the Flask application.

        Args:
            host: Server host address
            port: Server port number
            debug: Enable debug mode
        """
        logger.info(f"Starting application on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)


# Application factory
def create_app(openweather_api_key: Optional[str] = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        openweather_api_key: Optional OpenWeather API key

    Returns:
        Flask: Configured Flask application
    """
    app_instance = ResilienceAnalysisApp()

    if openweather_api_key:
        app_instance.initialize_climate_api(openweather_api_key)

    return app_instance.app


# Main execution
if __name__ == '__main__':
    """
    Main entry point for the application.

    Environment variables:
    - OPENWEATHER_API_KEY: Your OpenWeather API key
    - FLASK_PORT: Port number (default: 5000)
    """

    import os

    # Get configuration from environment
    api_key = os.getenv('OPENWEATHER_API_KEY', '')
    port = int(os.getenv('FLASK_PORT', 5000))

    # Create and run application
    app_runner = ResilienceAnalysisApp()

    if api_key:
        app_runner.initialize_climate_api(api_key)
    else:
        logger.warning("No OpenWeather API key provided. Climate API features will be limited.")

    app_runner.run(host='0.0.0.0', port=port, debug=False)


# For gunicorn deployment
import os
api_key = os.getenv('OPENWEATHER_API_KEY', '')
app = create_app(api_key)
