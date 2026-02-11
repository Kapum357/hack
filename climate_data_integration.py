"""
Climate Data Integration Module
Integrates IDEAM (Instituto de Hidrología, Meteorología y Estudios Ambientales)
and OpenWeather API data for comprehensive climate analysis in Soacha.

This module provides real-time and historical climate data integration with
temperature, precipitation, humidity, and extreme weather event tracking.
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple
import json

logger = logging.getLogger(__name__)


class ClimateDataIntegrator:
    """
    Manages integration of climate data from multiple meteorological sources.
    Combines IDEAM national climate data with OpenWeather real-time observations.
    """

    def __init__(self, openweather_api_key: str):
        """
        Initialize climate data integrator with API credentials.

        Args:
            openweather_api_key: OpenWeather API key for real-time data access
        """
        self.openweather_api_key = openweather_api_key
        self.soacha_coordinates = (4.7768, -74.1647)  # (latitude, longitude)

        # IDEAM data endpoints
        self.ideam_base_url = "https://www.ideam.gov.co/datos"
        self.openweather_base_url = "https://api.openweathermap.org/data/2.5"

        self.climate_cache = {}
        self.extreme_events = []

        logger.info("Climate Data Integrator initialized for Soacha region")

    def get_openweather_current_conditions(self) -> Dict:
        """
        Retrieve current weather conditions from OpenWeather API.

        Returns:
            Dict: Complete weather data including temperature, precipitation, wind
        """
        try:
            endpoint = f"{self.openweather_base_url}/weather"
            params = {
                'lat': self.soacha_coordinates[0],
                'lon': self.soacha_coordinates[1],
                'appid': self.openweather_api_key,
                'units': 'metric',
                'lang': 'es'
            }

            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()

            weather_data = response.json()
            processed_data = self._process_openweather_response(weather_data)

            self.climate_cache['current_conditions'] = processed_data
            logger.info("Current weather conditions retrieved from OpenWeather")

            return processed_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving OpenWeather data: {str(e)}")
            return None

    @staticmethod
    def _process_openweather_response(raw_data: Dict) -> Dict:
        """
        Process raw OpenWeather API response into standardized format.

        Args:
            raw_data: Raw JSON response from OpenWeather API

        Returns:
            Dict: Processed weather data with relevant metrics
        """
        try:
            processed = {
                'timestamp': datetime.fromtimestamp(raw_data['dt']).isoformat(),
                'temperature_celsius': raw_data['main']['temp'],
                'feels_like_celsius': raw_data['main']['feels_like'],
                'temperature_min_celsius': raw_data['main']['temp_min'],
                'temperature_max_celsius': raw_data['main']['temp_max'],
                'pressure_hpa': raw_data['main']['pressure'],
                'humidity_percent': raw_data['main']['humidity'],
                'visibility_meters': raw_data.get('visibility', None),
                'wind_speed_ms': raw_data['wind']['speed'],
                'wind_gust_ms': raw_data['wind'].get('gust', None),
                'wind_direction_degrees': raw_data['wind'].get('deg', None),
                'cloudiness_percent': raw_data['clouds']['all'],
                'precipitation_mm': raw_data.get('rain', {}).get('1h', 0),
                'weather_main': raw_data['weather'][0]['main'],
                'weather_description': raw_data['weather'][0]['description'],
                'location': f"{raw_data['coord']['lat']}, {raw_data['coord']['lon']}"
            }

            return processed

        except KeyError as e:
            logger.error(f"Error processing OpenWeather response: {str(e)}")
            return None

    def get_openweather_forecast(self, days: int = 5) -> pd.DataFrame:
        """
        Retrieve multi-day weather forecast from OpenWeather API.

        Args:
            days: Number of forecast days (1-5)

        Returns:
            DataFrame: Forecast data with daily weather predictions
        """
        if days > 5:
            logger.warning(f"Requested {days} days, limiting to 5 days for free API tier")
            days = 5

        try:
            endpoint = f"{self.openweather_base_url}/forecast"
            params = {
                'lat': self.soacha_coordinates[0],
                'lon': self.soacha_coordinates[1],
                'appid': self.openweather_api_key,
                'units': 'metric',
                'lang': 'es',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }

            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()

            forecast_data = response.json()
            forecast_df = self._process_forecast_data(forecast_data['list'])

            logger.info(f"5-day forecast retrieved with {len(forecast_df)} records")

            return forecast_df

        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving forecast data: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    def _process_forecast_data(forecast_list: List[Dict]) -> pd.DataFrame:
        """
        Process forecast list into structured DataFrame.

        Args:
            forecast_list: List of forecast entries from API

        Returns:
            DataFrame: Structured forecast data
        """
        records = []

        for entry in forecast_list:
            record = {
                'datetime': datetime.fromtimestamp(entry['dt']).isoformat(),
                'temperature_celsius': entry['main']['temp'],
                'feels_like_celsius': entry['main']['feels_like'],
                'humidity_percent': entry['main']['humidity'],
                'precipitation_mm': entry.get('rain', {}).get('3h', 0),
                'weather_main': entry['weather'][0]['main'],
                'wind_speed_ms': entry['wind']['speed'],
                'cloudiness_percent': entry['clouds']['all'],
                'precipitation_probability': entry.get('pop', 0) * 100
            }
            records.append(record)

        return pd.DataFrame(records)

    def get_ideam_precipitation_data(self, zone_name: str,
                                    days_back: int = 30) -> pd.DataFrame:
        """
        Retrieve historical precipitation data from IDEAM sources.

        Args:
            zone_name: Target geographic zone (e.g., 'El Danubio', 'La María')
            days_back: Number of historical days to retrieve

        Returns:
            DataFrame: Precipitation records with dates and amounts
        """
        # Simulated IDEAM data integration
        # In production, this would query actual IDEAM database or API

        dates = pd.date_range(end=datetime.now(), periods=days_back, freq='D')
        precipitation_mm = np.random.exponential(scale=5, size=days_back)

        # Add realistic seasonal variation for Soacha region
        month_adjustment = np.array([
            0.8, 0.8, 1.2, 1.5, 1.4, 1.1,  # Jan-Jun
            1.0, 1.0, 1.2, 1.5, 1.3, 0.9   # Jul-Dec
        ])
        month_indices = dates.month - 1
        precipitation_mm *= month_adjustment[month_indices]

        precipitation_df = pd.DataFrame({
            'date': dates,
            'zone': zone_name,
            'precipitation_mm': precipitation_mm,
            'anomaly_percent': np.random.normal(0, 15, days_back)  # Deviation from normal
        })

        logger.info(f"IDEAM precipitation data retrieved for {zone_name}: {days_back} days")

        return precipitation_df

    def get_ideam_temperature_data(self, zone_name: str,
                                  days_back: int = 30) -> pd.DataFrame:
        """
        Retrieve historical temperature data from IDEAM sources.

        Args:
            zone_name: Target geographic zone
            days_back: Number of historical days to retrieve

        Returns:
            DataFrame: Daily temperature records with min/max/avg
        """
        # Simulated IDEAM temperature data
        # Soacha typical temperatures: 12-25°C year-round

        dates = pd.date_range(end=datetime.now(), periods=days_back, freq='D')

        # Base temperatures with daily variation
        base_temp = 18.5  # Soacha average temperature
        daily_variation = np.random.normal(0, 0.8, days_back)

        temp_max = base_temp + 6 + daily_variation + np.random.normal(0, 0.5, days_back)
        temp_min = base_temp - 4 + daily_variation + np.random.normal(0, 0.5, days_back)
        temp_avg = (temp_max + temp_min) / 2

        temperature_df = pd.DataFrame({
            'date': dates,
            'zone': zone_name,
            'temp_min_celsius': temp_min,
            'temp_avg_celsius': temp_avg,
            'temp_max_celsius': temp_max,
            'anomaly_celsius': daily_variation
        })

        logger.info(f"IDEAM temperature data retrieved for {zone_name}: {days_back} days")

        return temperature_df

    def detect_extreme_weather_events(self, temperature_df: pd.DataFrame,
                                     precipitation_df: pd.DataFrame,
                                     temp_threshold_celsius: float = 28.0,
                                     precip_threshold_mm: float = 50.0) -> List[Dict]:
        """
        Identify extreme weather events based on threshold criteria.

        Args:
            temperature_df: Temperature observations
            precipitation_df: Precipitation observations
            temp_threshold_celsius: Temperature threshold for alerts
            precip_threshold_mm: Precipitation threshold for alerts

        Returns:
            List: Extreme weather event records
        """
        extreme_events = []

        # Detect temperature extremes
        high_temp_events = temperature_df[temperature_df['temp_max_celsius'] > temp_threshold_celsius]
        for _, row in high_temp_events.iterrows():
            extreme_events.append({
                'event_type': 'Heat Wave',
                'date': row['date'],
                'zone': row['zone'],
                'severity_value': row['temp_max_celsius'],
                'severity_unit': '°C',
                'risk_level': 'High',
                'recommended_action': 'Thermal stress alert - Increase monitoring of vulnerable populations'
            })

        # Detect heavy precipitation events
        high_precip_events = precipitation_df[precipitation_df['precipitation_mm'] > precip_threshold_mm]
        for _, row in high_precip_events.iterrows():
            extreme_events.append({
                'event_type': 'Heavy Rainfall',
                'date': row['date'],
                'zone': row['zone'],
                'severity_value': row['precipitation_mm'],
                'severity_unit': 'mm',
                'risk_level': 'High',
                'recommended_action': 'Flood risk alert - Prepare emergency response teams'
            })

        self.extreme_events = extreme_events
        logger.info(f"Detected {len(extreme_events)} extreme weather events")

        return extreme_events

    def generate_climate_resilience_report(self, zone_name: str) -> Dict:
        """
        Generate comprehensive climate resilience report for a zone.

        Args:
            zone_name: Target geographic zone

        Returns:
            Dict: Comprehensive climate analysis and resilience metrics
        """
        # Retrieve climate data
        temperature_df = self.get_ideam_temperature_data(zone_name, days_back=90)
        precipitation_df = self.get_ideam_precipitation_data(zone_name, days_back=90)
        current_conditions = self.get_openweather_current_conditions()

        # Detect extreme events
        extremes = self.detect_extreme_weather_events(temperature_df, precipitation_df)

        # Calculate resilience metrics
        report = {
            'zone_name': zone_name,
            'report_date': datetime.now().isoformat(),
            'climate_metrics': {
                'avg_temperature_celsius': temperature_df['temp_avg_celsius'].mean(),
                'temp_variability_celsius': temperature_df['temp_avg_celsius'].std(),
                'total_precipitation_mm': precipitation_df['precipitation_mm'].sum(),
                'avg_monthly_precipitation_mm': precipitation_df['precipitation_mm'].mean() * 30
            },
            'current_conditions': current_conditions,
            'extreme_events_detected': len(extremes),
            'recent_extreme_events': extremes[-5:] if extremes else [],
            'climate_risk_assessment': self._assess_climate_risk(temperature_df, precipitation_df),
            'recommendations': self._generate_resilience_recommendations(extremes)
        }

        logger.info(f"Climate resilience report generated for {zone_name}")

        return report

    @staticmethod
    def _assess_climate_risk(temperature_df: pd.DataFrame,
                           precipitation_df: pd.DataFrame) -> Dict:
        """
        Assess overall climate risk for a zone.

        Args:
            temperature_df: Temperature observations
            precipitation_df: Precipitation observations

        Returns:
            Dict: Risk assessment with scores and analysis
        """
        # Temperature variability risk (0-1 scale)
        temp_variability = temperature_df['temp_avg_celsius'].std() / 10
        temp_risk = min(temp_variability, 1.0)

        # Precipitation extremes risk
        precip_extremes = len(precipitation_df[precipitation_df['precipitation_mm'] > 50])
        precip_risk = min(precip_extremes / len(precipitation_df), 1.0)

        overall_risk = (temp_risk + precip_risk) / 2

        return {
            'temperature_variability_risk': round(temp_risk, 3),
            'precipitation_extremes_risk': round(precip_risk, 3),
            'overall_climate_risk': round(overall_risk, 3),
            'risk_level': 'High' if overall_risk > 0.6 else 'Medium' if overall_risk > 0.3 else 'Low'
        }

    @staticmethod
    def _generate_resilience_recommendations(extreme_events: List[Dict]) -> List[str]:
        """
        Generate recommended resilience measures based on climate data.

        Args:
            extreme_events: List of detected extreme weather events

        Returns:
            List: Recommended actions for climate resilience
        """
        recommendations = []

        heat_wave_count = len([e for e in extreme_events if e['event_type'] == 'Heat Wave'])
        if heat_wave_count > 2:
            recommendations.append('Implement urban cooling strategies (green roofs, cool pavements)')
            recommendations.append('Establish heat emergency response protocols')

        flood_count = len([e for e in extreme_events if e['event_type'] == 'Heavy Rainfall'])
        if flood_count > 2:
            recommendations.append('Improve stormwater drainage infrastructure')
            recommendations.append('Restore wetlands for natural water retention')

        if not recommendations:
            recommendations.append('Continue monitoring climate patterns')

        return recommendations
