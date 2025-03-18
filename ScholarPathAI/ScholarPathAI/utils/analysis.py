import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy import stats

def perform_descriptive_statistics(data):
    """Calculate descriptive statistics for numerical data"""
    description = data.describe()
    skewness = data.skew()
    kurtosis = data.kurtosis()
    
    return {
        'description': description,
        'skewness': skewness,
        'kurtosis': kurtosis
    }

def perform_correlation_analysis(data):
    """Calculate correlation matrix"""
    return data.corr()

def perform_hypothesis_test(group1, group2, test_type='t-test'):
    """Perform statistical hypothesis testing"""
    if test_type == 't-test':
        statistic, p_value = stats.ttest_ind(group1, group2)
    elif test_type == 'mann-whitney':
        statistic, p_value = stats.mannwhitneyu(group1, group2)
    else:
        raise ValueError("Unsupported test type")
    
    return {
        'statistic': statistic,
        'p_value': p_value,
        'significant': p_value < 0.05
    }

def normalize_data(data):
    """Normalize numerical data"""
    scaler = StandardScaler()
    normalized_data = scaler.fit_transform(data)
    return pd.DataFrame(normalized_data, columns=data.columns)
