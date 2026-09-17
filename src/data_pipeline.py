"""
src/data_pipeline.py
====================
Data ingestion, missing value imputation, quality audit, and feature standardization.
"""

import os
import pandas as pd
import numpy as np

# Sensor modality column groupings
MODALITY_COLS = {
    'accelerometer': [
        'accelerometer_magnitude_mean', 'accelerometer_magnitude_std_dev',
        'accelerometer_magnitude_mean_derivative', 'accelerometer_magnitude_rms',
        'accelerometer_magnitude_peak_to_peak', 'accelerometer_magnitude_peak_to_rms',
        'accelerometer_magnitude_num_peaks', 'accelerometer_magnitude_sample_entropy',
    ],
    'BVP': [
        'bvp_light_absorption_nW_mean', 'bvp_light_absorption_nW_std_dev',
        'bvp_light_absorption_nW_mean_derivative', 'bvp_light_absorption_nW_rms',
        'bvp_light_absorption_nW_peak_to_peak', 'bvp_light_absorption_nW_peak_to_rms',
        'bvp_light_absorption_nW_num_peaks', 'bvp_light_absorption_nW_sample_entropy',
    ],
    'EDA': [
        'eda_microsiemens_mean', 'eda_microsiemens_std_dev',
        'eda_microsiemens_mean_derivative', 'eda_microsiemens_rms',
        'eda_microsiemens_peak_to_peak', 'eda_microsiemens_peak_to_rms',
        'eda_microsiemens_num_peaks', 'eda_microsiemens_sample_entropy',
    ],
    'temperature': [
        'temperature_celcius_mean', 'temperature_celcius_std_dev',
        'temperature_celcius_mean_derivative', 'temperature_celcius_rms',
        'temperature_celcius_peak_to_peak', 'temperature_celcius_peak_to_rms',
        'temperature_celcius_num_peaks', 'temperature_celcius_sample_entropy',
    ],
    'RR_interval': [
        'rr_interval_milliseconds_mean', 'rr_interval_milliseconds_std_dev',
        'rr_interval_milliseconds_mean_derivative', 'rr_interval_milliseconds_rms',
        'rr_interval_milliseconds_peak_to_peak', 'rr_interval_milliseconds_peak_to_rms',
        'rr_interval_milliseconds_num_peaks', 'rr_interval_milliseconds_sample_entropy',
    ],
}

ALL_NUMERICAL_COLS = [col for cols in MODALITY_COLS.values() for col in cols]
METADATA_COLS = ['posture_type', 'subject', 'gender', 'yoga_experience', 'difficulty_level', 'state']


def load_and_clean_data(raw_data_path: str = 'data/raw/wearable_data.csv',
                        processed_data_path: str = 'data/processed/wearable_clean.csv') -> tuple:
    """
    Ingests raw wearable biometrics dataset, performs data hygiene checks,
    handles missingness via median imputation, and generates a clean analytics-ready dataset.

    Returns:
        tuple: (df_clean, data_profile_dict)
    """
    if not os.path.exists(raw_data_path):
        # Fallback to current directory if not found in data/raw
        if os.path.exists('wearable_data.csv'):
            raw_data_path = 'wearable_data.csv'
        else:
            raise FileNotFoundError(f"Raw data file not found at {raw_data_path}")

    df_raw = pd.read_csv(raw_data_path)
    initial_shape = df_raw.shape

    # Identify missing values before imputation
    missing_counts = df_raw.isnull().sum()
    cols_with_missing = missing_counts[missing_counts > 0].to_dict()

    # Drop non-feature administrative columns if present
    drop_candidates = ['timestamp', 'subject_state']
    df_clean = df_raw.drop(columns=[c for c in drop_candidates if c in df_raw.columns]).copy()

    # Median imputation for numerical features (robust to sensor outliers)
    imputed_cols = []
    for col in ALL_NUMERICAL_COLS:
        if col in df_clean.columns and df_clean[col].isnull().any():
            median_val = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(median_val)
            imputed_cols.append(col)

    # Standardize string representations for categorical metadata
    for cat_col in METADATA_COLS:
        if cat_col in df_clean.columns:
            df_clean[cat_col] = df_clean[cat_col].astype(str).str.strip().str.lower()

    # Create processed directory and persist clean dataset
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    df_clean.to_csv(processed_data_path, index=False)

    data_profile = {
        'initial_shape': initial_shape,
        'clean_shape': df_clean.shape,
        'missing_columns_count': len(cols_with_missing),
        'cols_imputed': imputed_cols,
        'total_samples': len(df_clean),
        'subjects_count': df_clean['subject'].nunique() if 'subject' in df_clean.columns else None,
        'classes': df_clean['state'].value_counts().to_dict() if 'state' in df_clean.columns else {}
    }

    return df_clean, data_profile
