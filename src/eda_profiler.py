"""
src/eda_profiler.py
===================
Exploratory data analysis, cohort profiling, sensor cross-correlation, and visualization.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns

from .data_pipeline import MODALITY_COLS, ALL_NUMERICAL_COLS

sns.set_theme(style="whitegrid", palette="muted")


def generate_eda_reports(df: pd.DataFrame, output_dir: str = 'reports/figures') -> dict:
    """
    Generates exploratory visual analytics, sensor cross-modality correlations,
    and demographic/cohort breakdowns.

    Returns:
        dict of summary DataFrames and saved figure paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    generated_figures = []

    # 1. State Distribution & Cohort Breakdowns
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    plt.subplots_adjust(hspace=0.35, wspace=0.3)

    # State distribution
    palette_state = {'relaxed': '#2b8cbe', 'parasympathetic': '#7bccc4', 'sympathetic': '#e34a33'}
    sns.countplot(data=df, x='state', hue='state', order=['relaxed', 'parasympathetic', 'sympathetic'],
                  palette=palette_state, legend=False, ax=axes[0, 0])
    axes[0, 0].set_title('Target State Distribution (ANS Arousal)', fontsize=13, fontweight='bold')
    axes[0, 0].set_xlabel('Autonomic State')
    axes[0, 0].set_ylabel('Sample Count')
    for p in axes[0, 0].patches:
        axes[0, 0].annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='baseline', fontsize=11, xytext=(0, 4), textcoords='offset points')

    # Yoga experience breakdown
    sns.countplot(data=df, x='yoga_experience', hue='state',
                  hue_order=['relaxed', 'parasympathetic', 'sympathetic'],
                  palette=palette_state, ax=axes[0, 1])
    axes[0, 1].set_title('State Prevalence by Yoga Experience', fontsize=13, fontweight='bold')
    axes[0, 1].set_xlabel('Experience Level')
    axes[0, 1].set_ylabel('Count')

    # Posture difficulty breakdown
    sns.countplot(data=df, x='difficulty_level', hue='state',
                  hue_order=['relaxed', 'parasympathetic', 'sympathetic'],
                  palette=palette_state, ax=axes[1, 0])
    axes[1, 0].set_title('State Prevalence by Posture Difficulty', fontsize=13, fontweight='bold')
    axes[1, 0].set_xlabel('Difficulty Level')
    axes[1, 0].set_ylabel('Count')

    # Gender breakdown
    sns.countplot(data=df, x='gender', hue='state',
                  hue_order=['relaxed', 'parasympathetic', 'sympathetic'],
                  palette=palette_state, ax=axes[1, 1])
    axes[1, 1].set_title('State Prevalence by Gender Cohort', fontsize=13, fontweight='bold')
    axes[1, 1].set_xlabel('Gender')
    axes[1, 1].set_ylabel('Count')

    fig_path1 = os.path.join(output_dir, 'state_distribution_and_cohorts.png')
    plt.savefig(fig_path1, dpi=300, bbox_inches='tight')
    plt.close()
    generated_figures.append(fig_path1)

    # 2. Key Biomarker Boxplots across States
    key_markers = [
        ('eda_microsiemens_mean', 'EDA Mean (µS)', 'Skin Conductance / Sympathetic Tone'),
        ('rr_interval_milliseconds_mean', 'RR Interval Mean (ms)', 'Heart Period (Inversely related to HR)'),
        ('temperature_celcius_mean', 'Skin Temp Mean (°C)', 'Peripheral Vasoconstriction'),
        ('bvp_light_absorption_nW_rms', 'BVP RMS (nW)', 'Blood Volume Pulse Amplitude'),
        ('accelerometer_magnitude_mean', 'Accel Magnitude Mean', 'Physical Movement Intensity'),
        ('accelerometer_magnitude_std_dev', 'Accel Magnitude Std', 'Posture Dynamic Tremor')
    ]

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    plt.subplots_adjust(hspace=0.35, wspace=0.3)
    axes = axes.flatten()

    for i, (col, title, subtitle) in enumerate(key_markers):
        if col in df.columns:
            sns.boxplot(data=df, x='state', y=col, hue='state', order=['relaxed', 'parasympathetic', 'sympathetic'],
                        palette=palette_state, legend=False, ax=axes[i], showmeans=True,
                        meanprops={"marker": "o", "markerfacecolor": "white", "markeredgecolor": "black"})
            axes[i].set_title(f'{title}\n({subtitle})', fontsize=11, fontweight='bold')
            axes[i].set_xlabel('State')
            axes[i].set_ylabel(title)

    fig_path2 = os.path.join(output_dir, 'biometric_boxplots_by_state.png')
    plt.savefig(fig_path2, dpi=300, bbox_inches='tight')
    plt.close()
    generated_figures.append(fig_path2)

    # 3. Sensor Cross-Modality Correlation Heatmap
    primary_sensor_cols = [
        'eda_microsiemens_mean', 'eda_microsiemens_std_dev',
        'rr_interval_milliseconds_mean', 'rr_interval_milliseconds_std_dev',
        'temperature_celcius_mean', 'temperature_celcius_rms',
        'bvp_light_absorption_nW_mean', 'bvp_light_absorption_nW_rms',
        'accelerometer_magnitude_mean', 'accelerometer_magnitude_rms'
    ]
    avail_cols = [c for c in primary_sensor_cols if c in df.columns]
    corr_matrix = df[avail_cols].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1,
                linewidths=0.5, cbar_kws={'label': 'Pearson Correlation (r)'}, ax=ax)
    ax.set_title('Sensor Cross-Modality Correlation Matrix', fontsize=14, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right')

    fig_path3 = os.path.join(output_dir, 'sensor_correlation_matrix.png')
    plt.savefig(fig_path3, dpi=300, bbox_inches='tight')
    plt.close()
    generated_figures.append(fig_path3)

    # 4. Stress Rate Heatmap: Experience Level vs Posture Difficulty
    # Compute proportion of sympathetic state (acute stress)
    stress_crosstab = pd.crosstab(
        index=df['difficulty_level'],
        columns=df['yoga_experience'],
        values=(df['state'] == 'sympathetic').astype(int),
        aggfunc='mean'
    ) * 100

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(stress_crosstab, annot=True, fmt='.1f', cmap='Reds', cbar_kws={'label': '% Sympathetic Arousal'}, ax=ax)
    ax.set_title('Sympathetic Activation Rate (%) by Difficulty & Experience', fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel('Yoga Experience Level')
    ax.set_ylabel('Posture Difficulty Level')

    fig_path4 = os.path.join(output_dir, 'experience_vs_difficulty_stress_heatmap.png')
    plt.savefig(fig_path4, dpi=300, bbox_inches='tight')
    plt.close()
    generated_figures.append(fig_path4)

    # Summary Statistics Table
    stats_summary = df.groupby('state')[avail_cols].agg(['mean', 'std']).T

    return {
        'figures': generated_figures,
        'stress_crosstab': stress_crosstab,
        'stats_summary': stats_summary
    }
