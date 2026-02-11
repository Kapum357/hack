"""
Geospatial Visualization Module
Creates interactive maps, heat maps, and risk visualizations for climate resilience analysis.

This module uses Folium for interactive OpenStreetMap-based visualizations with
custom layers for vulnerability heat maps and zoned boundary overlays.
"""

import folium
from folium import plugins
import geopandas as gpd
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
import json
from datetime import datetime
import matplotlib.cm as cm

logger = logging.getLogger(__name__)


class InteractiveMapVisualizer:
    """
    Creates interactive web-based maps with multiple visualization layers.
    Manages OpenStreetMap base layers, zone boundaries, heat maps, and data overlays.
    """

    # Error messages
    BASE_MAP_NOT_INITIALIZED_ERROR = "Base map not initialized"

    def __init__(self, center_coordinates: Tuple[float, float], zoom_level: int = 13):
        """
        Initialize the map visualizer.

        Args:
            center_coordinates: Central coordinates for map (latitude, longitude)
            zoom_level: Initial zoom level (1-18)
        """
        self.center_coords = center_coordinates
        self.zoom_level = zoom_level
        self.map = None
        self.feature_groups = {}

        logger.info(f"Interactive Map Visualizer initialized for coordinates {center_coordinates}")

    def create_base_map(self, map_name: str = "Soacha Resilience Map",
                       tile_provider: str = "OpenStreetMap") -> folium.Map:
        """
        Create the base interactive map layer.

        Args:
            map_name: Title for the map
            tile_provider: Map tile provider (OpenStreetMap, CartoDB, Satellite, etc.)

        Returns:
            folium.Map: The base folium map object
        """
        # Define available tile providers
        tile_providers = {
            'OpenStreetMap': 'OpenStreetMap',
            'CartoDB': 'CartoDB positron',
            'CartoDarkMatter': 'CartoDB positron',
            'Satellite': 'OpenStreetMap.Mapnik',
            'Terrain': 'USGS.USTopo'
        }

        self.map = folium.Map(
            location=self.center_coords,
            zoom_start=self.zoom_level,
            tiles=tile_providers.get(tile_provider, 'OpenStreetMap'),
            name=map_name,
            prefer_canvas=True
        )

        # Add layer control
        folium.LayerControl().add_to(self.map)

        logger.info(f"Base map created with {tile_provider} tiles")

        return self.map

    def add_zone_boundaries(self, zones: Dict, zone_style: Optional[Dict] = None) -> None:
        """
        Add geographic zone boundaries as overlay layers.

        Args:
            zones: Dictionary of zones with polygon geometries
            zone_style: Optional styling dictionary with color, weight, opacity
        """
        if self.map is None:
            logger.error(self.BASE_MAP_NOT_INITIALIZED_ERROR)
            return

        # Default zone styling
        if zone_style is None:
            zone_style = {
                'El Danubio': {'color': 'red', 'weight': 3, 'opacity': 0.7, 'fillOpacity': 0.1},
                'La María': {'color': 'blue', 'weight': 3, 'opacity': 0.7, 'fillOpacity': 0.1}
            }

        feature_group = folium.FeatureGroup(name='Zone Boundaries', show=True)

        for zone_name, zone_data in zones.items():
            polygon = zone_data['polygon']
            center = zone_data['center']

            # Extract polygon coordinates
            coords = list(polygon.exterior.coords)

            # Create polygon layer
            folium.Polygon(
                locations=[(lat, lon) for lon, lat in coords],
                popup=f"<b>{zone_name}</b><br/>Risk: {zone_data['risk_level']}",
                tooltip=f"{zone_name} - {zone_data['risk_level']} Risk",
                color=zone_style[zone_name]['color'],
                weight=zone_style[zone_name]['weight'],
                opacity=zone_style[zone_name]['opacity'],
                fillOpacity=zone_style[zone_name]['fillOpacity'],
                fill=True
            ).add_to(feature_group)

            # Add zone center marker
            folium.CircleMarker(
                location=center,
                radius=8,
                popup=f"<b>{zone_name} Center</b>",
                tooltip=zone_name,
                color=zone_style[zone_name]['color'],
                fill=True,
                fillColor=zone_style[zone_name]['color'],
                fillOpacity=0.8,
                weight=2
            ).add_to(feature_group)

        feature_group.add_to(self.map)
        self.feature_groups['zone_boundaries'] = feature_group

        logger.info(f"Added {len(zones)} zone boundaries to map")

    def add_vulnerability_heatmap(self, vulnerability_gdf: gpd.GeoDataFrame,
                                 column_name: str = 'vulnerability_index',
                                 colormap_name: str = 'YlOrRd',
                                 opacity: float = 0.7) -> None:
        """
        Add vulnerability heat map visualization.

        Args:
            vulnerability_gdf: GeoDataFrame with vulnerability data
            column_name: Column name containing vulnerability scores (0-1)
            colormap_name: Folium colormap name (YlOrRd, RdYlGn_r, Viridis, etc.)
            opacity: Layer opacity (0-1)
        """
        if self.map is None:
            logger.error(self.BASE_MAP_NOT_INITIALIZED_ERROR)
            return

        if vulnerability_gdf.empty:
            logger.warning("Empty vulnerability GeoDataFrame provided")
            return

        # Normalize vulnerability indices to 0-1 range if needed
        vuln_values = vulnerability_gdf[column_name]
        vuln_min = vuln_values.min()
        vuln_max = vuln_values.max()

        if vuln_min == vuln_max:
            vuln_normalized = vuln_values * 0.5
        else:
            vuln_normalized = (vuln_values - vuln_min) / (vuln_max - vuln_min)

        # Create heat map feature group
        heatmap_group = folium.FeatureGroup(name='Vulnerability Heat Map', show=True)

        # Get colormap from matplotlib
        colormap = cm.get_cmap(colormap_name)

        # Add circle markers for each location
        for idx, (_, row) in enumerate(vulnerability_gdf.iterrows()):
            color = colormap(vuln_normalized.iloc[idx])

            # Convert matplotlib color (RGBA) to hex
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(color[0] * 255),
                int(color[1] * 255),
                int(color[2] * 255)
            )

            popup_text = f"""
            <b>Vulnerability Analysis</b><br/>
            Index: {vuln_values.iloc[idx]:.3f}<br/>
            Risk: {row.get('risk_category', 'Unknown')}<br/>
            Climate: {row.get('climate_vulnerability', 'N/A'):.3f}<br/>
            Demographic: {row.get('demographic_vulnerability', 'N/A'):.3f}
            """

            folium.CircleMarker(
                location=(row.geometry.y, row.geometry.x),
                radius=6,
                popup=folium.Popup(popup_text, max_width="300"),
                tooltip=f"Vulnerability: {vuln_values.iloc[idx]:.3f}",
                color=hex_color,
                fill=True,
                fillColor=hex_color,
                fillOpacity=opacity,
                weight=1
            ).add_to(heatmap_group)

        heatmap_group.add_to(self.map)
        self.feature_groups['vulnerability_heatmap'] = heatmap_group

        logger.info(f"Vulnerability heat map added with {len(vulnerability_gdf)} data points")

    def add_climate_data_layer(self, climate_stations: pd.DataFrame,
                              data_type: str = 'temperature') -> None:
        """
        Add climate monitoring station data as map layer.

        Args:
            climate_stations: DataFrame with station data (latitude, longitude, value)
            data_type: Type of climate data ('temperature', 'precipitation', 'humidity')
        """
        if self.map is None:
            logger.error(self.BASE_MAP_NOT_INITIALIZED_ERROR)
            return

        feature_group = folium.FeatureGroup(
            name=f'Climate Data - {data_type.title()}',
            show=True
        )

        # Define data type styling
        type_config = {
            'temperature': {'icon': '🌡️', 'unit': '°C', 'threshold': 25},
            'precipitation': {'icon': '🌧️', 'unit': 'mm', 'threshold': 50},
            'humidity': {'icon': '💧', 'unit': '%', 'threshold': 80}
        }

        config = type_config.get(data_type, type_config['temperature'])

        # Add markers for each climate station
        required_cols = ['latitude', 'longitude']
        value_col = next((col for col in climate_stations.columns
                         if col not in required_cols), None)

        if value_col is None:
            logger.warning(f"No value column found in climate data")
            return

        for _, station in climate_stations.iterrows():
            try:
                lat = station.get('latitude') or station.get('lat')
                lon = station.get('longitude') or station.get('lon')
                value = station[value_col]

                popup_text = f"""
                <b>{data_type.upper()} Station</b><br/>
                Value: {value:.2f} {config['unit']}<br/>
                Location: ({lat:.4f}, {lon:.4f})
                """

                folium.Marker(
                    location=(lat, lon),
                    popup=folium.Popup(popup_text, max_width="250"),
                    tooltip=f"{data_type}: {value:.2f} {config['unit']}",
                    icon=folium.Icon(
                        color='red' if value > config['threshold'] else 'blue',
                        icon='info-sign'
                    )
                ).add_to(feature_group)

            except (KeyError, TypeError) as e:
                logger.warning(f"Error processing climate station: {str(e)}")
                continue

        feature_group.add_to(self.map)
        self.feature_groups[f'climate_{data_type}'] = feature_group

        logger.info(f"Climate data layer added for {data_type}")

    def add_extreme_events_markers(self, extreme_events: List[Dict]) -> None:
        """
        Add markers for detected extreme weather events.

        Args:
            extreme_events: List of extreme event dictionaries with location/severity
        """
        if self.map is None:
            logger.error(self.BASE_MAP_NOT_INITIALIZED_ERROR)
            return

        feature_group = folium.FeatureGroup(name='Extreme Weather Events', show=True)

        event_colors = {
            'Heat Wave': 'orange',
            'Heavy Rainfall': 'purple',
            'Drought': 'brown',
            'Strong Winds': 'gray'
        }

        for event in extreme_events:
            event_type = event.get('event_type', 'Unknown')
            severity = event.get('severity_value', 0)
            zone = event.get('zone', 'Unknown')

            popup_text = f"""
            <b>{event_type}</b><br/>
            Severity: {severity:.2f} {event.get('severity_unit', '')}<br/>
            Zone: {zone}<br/>
            Risk Level: {event.get('risk_level', 'Unknown')}<br/>
            Action: {event.get('recommended_action', 'N/A')}
            """

            folium.Marker(
                location=(np.random.uniform(4.77, 4.79), np.random.uniform(-74.17, -74.16)),
                popup=folium.Popup(popup_text, max_width="300"),
                tooltip=f"{event_type} - {zone}",
                icon=folium.Icon(
                    color=event_colors.get(event_type, 'blue'),
                    icon='warning',
                    prefix='fa'
                )
            ).add_to(feature_group)

        feature_group.add_to(self.map)
        self.feature_groups['extreme_events'] = feature_group

        logger.info(f"Added {len(extreme_events)} extreme weather events to map")

    def add_demographic_distribution(self, demographic_gdf: gpd.GeoDataFrame,
                                    column_name: str = 'population',
                                    circle_max_radius: float = 50) -> None:
        """
        Add demographic data visualization as circle markers.

        Args:
            demographic_gdf: GeoDataFrame with demographic data
            column_name: Column name for population/density data
            circle_max_radius: Maximum circle radius in pixels
        """
        if self.map is None:
            logger.error(self.BASE_MAP_NOT_INITIALIZED_ERROR)
            return

        feature_group = folium.FeatureGroup(name='Population Distribution', show=True)

        # Normalize population data
        pop_values = demographic_gdf[column_name]
        pop_min = pop_values.min()
        pop_max = pop_values.max()

        if pop_min == pop_max:
            pop_normalized = [circle_max_radius / 2] * len(pop_values)
        else:
            pop_normalized = [
                (val - pop_min) / (pop_max - pop_min) * circle_max_radius
                for val in pop_values
            ]

        for idx, (_, row) in enumerate(demographic_gdf.iterrows()):
            popup_text = f"""
            <b>Population Area</b><br/>
            {column_name}: {pop_values.iloc[idx]:.0f}<br/>
            Coordinates: ({row.geometry.y:.4f}, {row.geometry.x:.4f})
            """

            folium.CircleMarker(
                location=(row.geometry.y, row.geometry.x),
                radius=int(pop_normalized[idx]),
                popup=folium.Popup(popup_text, max_width="250"),
                tooltip=f"{column_name}: {pop_values.iloc[idx]:.0f}",
                color='green',
                fill=True,
                fillColor='lightgreen',
                fillOpacity=0.6,
                weight=2
            ).add_to(feature_group)

        feature_group.add_to(self.map)
        self.feature_groups['demographics'] = feature_group

        logger.info(f"Demographic distribution layer added")

    def add_measurement_scale(self) -> None:
        """Add scale control to map."""
        if self.map is not None:
            folium.ScaleControl().add_to(self.map)  # type: ignore

    def add_fullscreen_button(self) -> None:
        """Add fullscreen toggle button to map."""
        if self.map is not None:
            plugins.Fullscreen().add_to(self.map)

    def save_map(self, filepath: str) -> bool:
        """
        Save the interactive map to an HTML file.

        Args:
            filepath: Output file path (e.g., 'map.html')

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.map is None:
                logger.error("No map to save")
                return False

            self.map.save(filepath)
            logger.info(f"Map saved successfully to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error saving map: {str(e)}")
            return False

    def get_map_html(self) -> Optional[str]:
        """
        Return map as HTML string for embedding in web applications.

        Returns:
            str: HTML representation of the map
        """
        if self.map is None:
            logger.error("No map to export")
            return None

        return self.map._repr_html_()
