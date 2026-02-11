"""
Configuration Module for Soacha Climate Resilience Analysis Platform

This module centralizes all configuration settings for the geospatial analysis,
climate integration, and web application components.
"""

import os
from datetime import timedelta
from typing import Dict, Tuple


class BaseConfig:
    """
    Base configuration class with common settings.
    """

    # Application settings
    APP_NAME = 'Soacha Climate Resilience Platform'
    APP_VERSION = '1.0.0'
    DEBUG = False
    TESTING = False

    # Flask settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True

    # Geospatial settings
    SOACHA_CENTER = (4.7768, -74.1647)  # latitude, longitude
    DEFAULT_ZOOM_LEVEL = 13
    CRS = 'EPSG:4326'  # WGS84 coordinate reference system

    # Zone definitions (geographical boundaries)
    ZONES = {
        'El Danubio': {
            'center': (4.7810, -74.1680),
            'radius_km': 2.5,
            'risk_level': 'high',
            'population_estimate': 45000
        },
        'La María': {
            'center': (4.7750, -74.1620),
            'radius_km': 2.0,
            'risk_level': 'medium',
            'population_estimate': 35000
        }
    }

    # Vulnerability index weights
    VULNERABILITY_WEIGHTS = {
        'climate': 0.40,
        'demographic': 0.30,
        'infrastructure': 0.20,
        'environmental': 0.10
    }

    # Climate data thresholds for alerts
    CLIMATE_THRESHOLDS = {
        'temperature_alert_celsius': 28.0,
        'precipitation_alert_mm': 50.0,
        'cold_wave_threshold_celsius': 8.0,
        'drought_days_threshold': 30
    }

    # API Configuration
    API_ENDPOINTS = {
        'zones': '/api/zones',
        'vulnerability': '/api/vulnerability/<zone>',
        'climate': '/api/climate/<zone>',
        'map': '/api/map/interactive',
        'health': '/api/health',
        'data_status': '/api/data/status'
    }

    # OpenWeather API settings
    OPENWEATHER_TIMEOUT = 10  # seconds
    OPENWEATHER_UNITS = 'metric'  # Celsius

    # Data processing settings
    DATA_CACHE_EXPIRATION = timedelta(hours=1)
    BATCH_PROCESSING_SIZE = 1000
    MISSING_VALUE_STRATEGY = 'mean'  # mean, median, forward_fill
    OUTLIER_DETECTION_METHOD = 'iqr'  # iqr or zscore
    OUTLIER_THRESHOLD = 1.5

    # Logging settings
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'resilience_analysis.log'

    # Heat map visualization settings
    HEATMAP_COLORMAP = 'YlOrRd'  # Yellow-Orange-Red for vulnerability
    HEATMAP_OPACITY = 0.7
    CIRCLE_MARKER_MAX_RADIUS = 50

    # Map layer styling
    ZONE_STYLE = {
        'El Danubio': {
            'color': 'red',
            'weight': 3,
            'opacity': 0.7,
            'fillOpacity': 0.1
        },
        'La María': {
            'color': 'blue',
            'weight': 3,
            'opacity': 0.7,
            'fillOpacity': 0.1
        }
    }


class DevelopmentConfig(BaseConfig):
    """
    Development environment configuration.
    """

    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'

    # Development server settings
    FLASK_HOST = '127.0.0.1'
    FLASK_PORT = 5000

    # Enable detailed error pages
    EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(BaseConfig):
    """
    Production environment configuration.
    """

    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'INFO'

    # Production server settings
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000

    # Additional security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)


class TestingConfig(BaseConfig):
    """
    Testing environment configuration.
    """

    TESTING = True
    DEBUG = True

    # Use test data instead of API calls
    USE_MOCK_CLIMATE_DATA = True
    USE_MOCK_AVCA_DATA = True


class Config:
    """
    Configuration factory that selects appropriate config based on environment.
    """

    _configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }

    @staticmethod
    def get_config(environment: str = None) -> BaseConfig:
        """
        Get configuration object for specified environment.

        Args:
            environment: Environment name (development, production, testing)
                        If None, uses FLASK_ENV environment variable

        Returns:
            BaseConfig: Configuration object
        """
        if environment is None:
            environment = os.getenv('FLASK_ENV', 'development')

        config_class = Config._configs.get(environment, DevelopmentConfig)
        return config_class()

    @staticmethod
    def get_api_key(key_name: str, default: str = '') -> str:
        """
        Securely retrieve API key from environment variables.

        Args:
            key_name: Name of environment variable
            default: Default value if not found

        Returns:
            str: API key value
        """
        return os.getenv(key_name, default)


# Helper function to load environment configuration
def load_config(env: str = None) -> BaseConfig:
    """
    Load configuration for specified environment.

    Args:
        env: Environment name

    Returns:
        BaseConfig: Configuration object
    """
    return Config.get_config(env)


# Export current configuration
current_config = load_config()
