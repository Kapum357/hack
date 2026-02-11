"""
Data Processing and Analysis Utilities Module
Provides helper functions for data cleaning, normalization, and analysis
for climate resilience assessment.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
from scipy import stats

logger = logging.getLogger(__name__)


class DataNormalizer:
    """
    Utility class for normalizing and standardizing climate and vulnerability data.
    Handles missing values, outliers, and data scaling.
    """

    @staticmethod
    def normalize_vulnerability_scores(scores: pd.Series,
                                      method: str = 'minmax') -> pd.Series:
        """
        Normalize vulnerability scores to 0-1 range.

        Args:
            scores: Series of vulnerability scores
            method: Normalization method ('minmax' or 'zscore')

        Returns:
            Series: Normalized scores
        """
        if method == 'minmax':
            min_val = scores.min()
            max_val = scores.max()

            if min_val == max_val:
                return pd.Series([0.5] * len(scores), index=scores.index)

            return (scores - min_val) / (max_val - min_val)

        elif method == 'zscore':
            return (scores - scores.mean()) / scores.std()

        else:
            logger.warning(f"Unknown normalization method: {method}")
            return scores

    @staticmethod
    def handle_missing_values(dataframe: pd.DataFrame,
                            strategy: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values in climate data.

        Args:
            dataframe: Input DataFrame with potential missing values
            strategy: Filling strategy ('mean', 'median', 'forward_fill')

        Returns:
            DataFrame: DataFrame with filled missing values
        """
        df_clean = dataframe.copy()

        if strategy == 'mean':
            df_clean = df_clean.fillna(df_clean.mean())

        elif strategy == 'median':
            df_clean = df_clean.fillna(df_clean.median())

        elif strategy == 'forward_fill':
            df_clean = df_clean.fillna(method='ffill').fillna(method='bfill')

        logger.info(f"Missing values handled using {strategy} strategy")

        return df_clean

    @staticmethod
    def detect_and_handle_outliers(series: pd.Series,
                                  method: str = 'iqr',
                                  threshold: float = 1.5) -> pd.Series:
        """
        Detect and handle outliers in data series.

        Args:
            series: Data series to process
            method: Detection method ('iqr' or 'zscore')
            threshold: Sensitivity threshold

        Returns:
            Series: Series with outliers handled
        """
        series_clean = series.copy()

        if method == 'iqr':
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            # Cap outliers
            series_clean = series_clean.clip(lower_bound, upper_bound)

        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(series.dropna()))
            threshold_z = 3

            series_clean = series[z_scores < threshold_z]

        logger.info(f"Outliers handled using {method} method")

        return series_clean


class VulnerabilityIndexCalculator:
    """
    Advanced vulnerability index calculation with multiple factor weighting.
    """

    # Default vulnerability factor weights
    DEFAULT_WEIGHTS = {
        'climate': 0.40,
        'demographic': 0.30,
        'infrastructure': 0.20,
        'environmental': 0.10
    }

    @classmethod
    def calculate_composite_index(cls,
                                 climate_data: pd.Series,
                                 demographic_data: pd.Series,
                                 infrastructure_data: pd.Series,
                                 environmental_data: Optional[pd.Series] = None,
                                 weights: Optional[Dict] = None) -> pd.Series:
        """
        Calculate composite vulnerability index from multiple factors.

        Args:
            climate_data: Climate vulnerability scores
            demographic_data: Demographic vulnerability scores
            infrastructure_data: Infrastructure vulnerability scores
            environmental_data: Optional environmental/ecological scores
            weights: Custom weight distribution

        Returns:
            Series: Composite vulnerability index
        """
        if weights is None:
            weights = cls.DEFAULT_WEIGHTS

        # Normalize all inputs to 0-1 range
        climate_norm = DataNormalizer.normalize_vulnerability_scores(climate_data)
        demographic_norm = DataNormalizer.normalize_vulnerability_scores(demographic_data)
        infrastructure_norm = DataNormalizer.normalize_vulnerability_scores(infrastructure_data)

        # Calculate weighted sum
        composite = (
            weights['climate'] * climate_norm +
            weights['demographic'] * demographic_norm +
            weights['infrastructure'] * infrastructure_norm
        )

        # Include environmental data if provided
        if environmental_data is not None:
            environmental_norm = DataNormalizer.normalize_vulnerability_scores(environmental_data)
            env_weight = weights.get('environmental', 0.1)
            composite = composite + env_weight * environmental_norm

            # Renormalize to 0-1 range
            composite = DataNormalizer.normalize_vulnerability_scores(composite)

        return composite

    @staticmethod
    def categorize_vulnerability(index_values: pd.Series,
                               num_categories: int = 5) -> pd.Series:
        """
        Categorize vulnerability indices into discrete risk levels.

        Args:
            index_values: Vulnerability index values
            num_categories: Number of categories to create

        Returns:
            Series: Categorical vulnerability levels
        """
        category_labels = [
            'Very Low', 'Low', 'Medium', 'High', 'Very High'
        ][:num_categories]

        return pd.cut(
            index_values,
            bins=num_categories,
            labels=category_labels,
            include_lowest=True
        )


class TemporalAnalyzer:
    """
    Analyze temporal trends in climate and vulnerability data.
    """

    @staticmethod
    def calculate_trend(timeseries: pd.Series,
                       method: str = 'linear') -> Dict:
        """
        Calculate temporal trend in time series data.

        Args:
            timeseries: Time-indexed Series
            method: Trend calculation method ('linear' or 'polynomial')

        Returns:
            Dict: Trend analysis results
        """
        # Remove missing values
        clean_data = timeseries.dropna()

        if len(clean_data) < 2:
            logger.warning("Insufficient data for trend analysis")
            return None

        x = np.arange(len(clean_data))
        y = clean_data.values

        if method == 'linear':
            # Linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

            return {
                'trend': 'increasing' if slope > 0 else 'decreasing',
                'slope': float(slope),
                'intercept': float(intercept),
                'r_squared': float(r_value ** 2),
                'p_value': float(p_value),
                'std_error': float(std_err),
                'statistically_significant': p_value < 0.05
            }

        elif method == 'polynomial':
            # Polynomial trend (degree 2)
            coeffs = np.polyfit(x, y, 2)
            poly = np.poly1d(coeffs)
            y_fit = poly(x)
            ss_res = np.sum((y - y_fit) ** 2)
            ss_tot = np.sum((y - y.mean()) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

            return {
                'trend_type': 'polynomial_2nd_order',
                'coefficients': [float(c) for c in coeffs],
                'r_squared': float(r_squared),
                'curvature': 'accelerating' if coeffs[0] > 0 else 'decelerating'
            }

        return None

    @staticmethod
    def calculate_seasonal_decomposition(timeseries: pd.Series,
                                        period: int = 12) -> Dict:
        """
        Decompose time series into trend, seasonal, and residual components.

        Args:
            timeseries: Time-indexed Series with regular frequency
            period: Seasonal period (e.g., 12 for monthly data)

        Returns:
            Dict: Decomposition results
        """
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose

            # Ensure sufficient data
            if len(timeseries) < 2 * period:
                logger.warning("Insufficient data for seasonal decomposition")
                return None

            decomposition = seasonal_decompose(timeseries, model='additive', period=period)

            return {
                'trend': decomposition.trend.to_dict(),
                'seasonal': decomposition.seasonal.to_dict(),
                'residual': decomposition.resid.to_dict(),
                'seasonal_strength': float(
                    1 - (decomposition.resid.var() / decomposition.seasonal.var())
                    if decomposition.seasonal.var() > 0 else 0
                )
            }

        except ImportError:
            logger.warning("statsmodels not available for seasonal decomposition")
            return None

        except Exception as e:
            logger.error(f"Error in seasonal decomposition: {str(e)}")
            return None


class StatisticalAnalyzer:
    """
    Statistical analysis tools for climate and vulnerability assessment.
    """

    @staticmethod
    def calculate_correlation_matrix(dataframe: pd.DataFrame,
                                    method: str = 'pearson') -> pd.DataFrame:
        """
        Calculate correlation matrix between variables.

        Args:
            dataframe: Input DataFrame
            method: Correlation method ('pearson', 'spearman', 'kendall')

        Returns:
            DataFrame: Correlation matrix
        """
        return dataframe.corr(method=method)

    @staticmethod
    def perform_statistical_test(group1: pd.Series,
                                group2: pd.Series,
                                test_type: str = 'ttest') -> Dict:
        """
        Perform statistical comparison between two groups.

        Args:
            group1: First data group
            group2: Second data group
            test_type: Statistical test ('ttest', 'mannwhitneyu', 'ks')

        Returns:
            Dict: Test results and interpretation
        """
        if test_type == 'ttest':
            t_stat, p_value = stats.ttest_ind(group1, group2)

            return {
                'test': 't-test',
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'significant_difference': p_value < 0.05,
                'interpretation': 'Means are significantly different' if p_value < 0.05
                                   else 'No significant difference in means'
            }

        elif test_type == 'mannwhitneyu':
            u_stat, p_value = stats.mannwhitneyu(group1, group2)

            return {
                'test': 'Mann-Whitney U Test',
                'u_statistic': float(u_stat),
                'p_value': float(p_value),
                'significant_difference': p_value < 0.05,
                'interpretation': 'Distributions are significantly different' if p_value < 0.05
                                   else 'No significant difference in distributions'
            }

        elif test_type == 'ks':
            ks_stat, p_value = stats.ks_2samp(group1, group2)

            return {
                'test': 'Kolmogorov-Smirnov Test',
                'ks_statistic': float(ks_stat),
                'p_value': float(p_value),
                'significant_difference': p_value < 0.05
            }

        return None
