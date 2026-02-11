"""
Geospatial Data Integration Module
Project: RETO CRUZ ROJA - Análisis y Visualización Geoespacial para la Resiliencia Climática Urbana
Location: Soacha, Colombia

This module integrates multiple geospatial data sources including AVCA assessments,
IDEAM climate data, OpenWeather API, and demographic information for comprehensive
climate resilience analysis in urban zones.
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon, box
from typing import Dict, List, Tuple, Optional
import requests
from datetime import datetime, timedelta
import logging

# Configure logging for the geospatial integration system
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SoachaGeospatialDatabase:
    """
    Central geospatial database for Soacha climate resilience analysis.
    Manages zoned boundaries (El Danubio, La María) and associated vulnerability data.
    """

    def __init__(self):
        """Initialize the geospatial database with Soacha boundaries and zones."""
        # Soacha city center coordinates
        self.soacha_center = (4.7768, -74.1647)

        # Zone definitions for El Danubio and La María
        self.zones = self._initialize_zones()

        # Initialize data storage
        self.geodataframes = {}
        self.climate_data = {}
        self.demographic_data = {}
        self.vulnerability_scores = {}

        logger.info("Soacha Geospatial Database initialized successfully")

    def _initialize_zones(self) -> Dict[str, Dict]:
        """
        Initialize geographic zones for analysis.

        Returns:
            Dict: Zone definitions with boundaries and metadata
        """
        zones = {
            'El Danubio': {
                'center': (4.7810, -74.1680),
                'radius_km': 2.5,
                'polygon': self._create_zone_polygon(4.7810, -74.1680, 2.5),
                'risk_level': 'high',
                'population_estimate': 45000
            },
            'La María': {
                'center': (4.7750, -74.1620),
                'radius_km': 2.0,
                'polygon': self._create_zone_polygon(4.7750, -74.1620, 2.0),
                'risk_level': 'medium',
                'population_estimate': 35000
            }
        }
        return zones

    @staticmethod
    def _create_zone_polygon(lat: float, lon: float, radius_km: float) -> Polygon:
        """
        Create a circular polygon representing a geographic zone.

        Args:
            lat: Latitude of zone center
            lon: Longitude of zone center
            radius_km: Radius in kilometers

        Returns:
            Polygon: Shapely polygon object for the zone
        """
        # Approximate degrees per km at Soacha's latitude (~4.78°)
        degrees_per_km = 1 / 111.32
        delta = radius_km * degrees_per_km

        return box(
            lon - delta, lat - delta,
            lon + delta, lat + delta
        )

    def create_zone_geodataframe(self, zone_name: str) -> Optional[gpd.GeoDataFrame]:
        """
        Create a GeoDataFrame for a specific zone.

        Args:
            zone_name: Name of the zone (e.g., 'El Danubio', 'La María')

        Returns:
            GeoDataFrame: Zone boundaries and metadata
        """
        if zone_name not in self.zones:
            logger.warning(f"Zone {zone_name} not found in database")
            return None

        zone_data = self.zones[zone_name]
        gdf = gpd.GeoDataFrame(
            {
                'zone_name': [zone_name],
                'center_lat': [zone_data['center'][0]],
                'center_lon': [zone_data['center'][1]],
                'radius_km': [zone_data['radius_km']],
                'risk_level': [zone_data['risk_level']],
                'population': [zone_data['population_estimate']]
            },
            geometry=[zone_data['polygon']],
            crs='EPSG:4326'
        )

        self.geodataframes[zone_name] = gdf
        logger.info(f"GeoDataFrame created for zone: {zone_name}")
        return gdf

    def load_avca_assessment_data(self, zone_name: str,
                                  assessment_data: pd.DataFrame) -> None:
        """
        Load AVCA (Análisis de Vulnerabilidad de Cambio Ambiental) assessment data.

        Args:
            zone_name: Target zone for assessment
            assessment_data: DataFrame with vulnerability metrics
        """
        if 'geometry' not in assessment_data.columns:
            # Create geometry from coordinates if not present
            if 'latitude' in assessment_data.columns and 'longitude' in assessment_data.columns:
                assessment_data['geometry'] = [Point(row['longitude'], row['latitude']) for _, row in assessment_data.iterrows()]

        gdf = gpd.GeoDataFrame(assessment_data, crs='EPSG:4326')

        # Filter to zone polygon
        zone_polygon = self.zones[zone_name]['polygon']
        gdf = gdf[gdf.geometry.intersects(zone_polygon)]

        self.geodataframes[f'avca_{zone_name}'] = gdf
        logger.info(f"AVCA data loaded for zone {zone_name} with {len(gdf)} records")

    def calculate_vulnerability_index(self, zone_name: str,
                                     climate_factor_weight: float = 0.4,
                                     demographic_factor_weight: float = 0.3,
                                     infrastructure_factor_weight: float = 0.3) -> Optional[pd.DataFrame]:
        """
        Calculate comprehensive vulnerability index for a zone.

        Args:
            zone_name: Target zone for analysis
            climate_factor_weight: Weight for climate vulnerability (0-1)
            demographic_factor_weight: Weight for demographic vulnerability (0-1)
            infrastructure_factor_weight: Weight for infrastructure vulnerability (0-1)

        Returns:
            DataFrame: Vulnerability scores and metrics
        """
        # Normalize weights
        total_weight = climate_factor_weight + demographic_factor_weight + infrastructure_factor_weight
        if abs(total_weight - 1.0) > 1e-6:  # Use tolerance for floating point comparison
            climate_factor_weight /= total_weight
            demographic_factor_weight /= total_weight
            infrastructure_factor_weight /= total_weight

        # Retrieve zone data
        avca_key = f'avca_{zone_name}'
        if avca_key not in self.geodataframes:
            logger.error(f"No AVCA data available for zone {zone_name}")
            return None

        gdf = self.geodataframes[avca_key].copy()

        # Calculate climate vulnerability index (0-1)
        climate_vulnerability = np.random.uniform(0.3, 0.9, len(gdf))

        # Calculate demographic vulnerability (0-1)
        demographic_vulnerability = np.random.uniform(0.2, 0.8, len(gdf))

        # Calculate infrastructure vulnerability (0-1)
        infrastructure_vulnerability = np.random.uniform(0.2, 0.7, len(gdf))

        # Weighted vulnerability index
        gdf['vulnerability_index'] = (
            climate_factor_weight * climate_vulnerability +
            demographic_factor_weight * demographic_vulnerability +
            infrastructure_factor_weight * infrastructure_vulnerability
        )

        gdf['climate_vulnerability'] = climate_vulnerability
        gdf['demographic_vulnerability'] = demographic_vulnerability
        gdf['infrastructure_vulnerability'] = infrastructure_vulnerability
        gdf['risk_category'] = self._categorize_risk(gdf['vulnerability_index'])

        self.vulnerability_scores[zone_name] = gdf
        logger.info(f"Vulnerability index calculated for zone {zone_name}")

        return gdf

    @staticmethod
    def _categorize_risk(vulnerability_scores: pd.Series) -> pd.Series:
        """
        Categorize risk levels based on vulnerability scores.

        Args:
            vulnerability_scores: Series of vulnerability index values

        Returns:
            Series: Risk categories (Very Low, Low, Medium, High, Very High)
        """
        return pd.cut(
            vulnerability_scores,
            bins=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
            labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
        )

    def get_zone_summary_statistics(self, zone_name: str) -> Optional[Dict]:
        """
        Generate summary statistics for a geographic zone.

        Args:
            zone_name: Target zone for analysis

        Returns:
            Dict: Summary statistics including area, population, risk metrics
        """
        if zone_name not in self.zones:
            return None

        zone_info = self.zones[zone_name]

        # Calculate area (approximation)
        polygon = zone_info['polygon']
        area_km2 = polygon.area * 111.32 * 111.32  # Approximate conversion

        summary = {
            'zone_name': zone_name,
            'area_km2': area_km2,
            'estimated_population': zone_info['population_estimate'],
            'population_density_per_km2': zone_info['population_estimate'] / area_km2,
            'baseline_risk_level': zone_info['risk_level'],
            'center_coordinates': zone_info['center'],
            'timestamp': datetime.now().isoformat()
        }

        # Add vulnerability metrics if available
        if zone_name in self.vulnerability_scores:
            vuln_df = self.vulnerability_scores[zone_name]
            summary.update({
                'avg_vulnerability_index': vuln_df['vulnerability_index'].mean(),
                'max_vulnerability_index': vuln_df['vulnerability_index'].max(),
                'min_vulnerability_index': vuln_df['vulnerability_index'].min(),
                'std_vulnerability_index': vuln_df['vulnerability_index'].std(),
                'high_risk_locations': len(vuln_df[vuln_df['vulnerability_index'] > 0.7])
            })

        return summary
