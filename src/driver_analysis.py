"""
src/driver_analysis.py
======================
Dimensionality reduction (PCA), factor loading extraction, and driver attribution
via standardized Multinomial Logistic Regression odds ratios and feature importance.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

from .data_pipeline import ALL_NUMERICAL_COLS


def run_biomarker_driver_analysis(df: pd.DataFrame,
                                  output_csv: str = 'reports/biomarker_key_drivers.csv',
                                  output_fig_dir: str = 'reports/figures') -> dict:
    """
    Identifies the primary physiological signals driving autonomic nervous system transitions
    using Principal Component Analysis (PCA) and standardized Logistic Regression Driver Analysis.
    """
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(output_fig_dir, exist_ok=True)

    # 1. Prepare numerical feature matrix
    feat_cols = [c for c in ALL_NUMERICAL_COLS if c in df.columns]
    X = df[feat_cols].values
    y = df['state'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 2. PCA Dimensionality Reduction & Variance Explained
    pca = PCA(n_components=min(10, X_scaled.shape[1]))
    X_pca = pca.fit_transform(X_scaled)
    var_exp = pca.explained_variance_ratio_ * 100
    cum_var_exp = np.cumsum(var_exp)

    # Factor Loadings for PC1 and PC2
    loadings_df = pd.DataFrame(
        pca.components_[:2, :].T,
        index=feat_cols,
        columns=['PC1_Loading', 'PC2_Loading']
    )

    # 3. Driver Analysis via Standardized Logistic Regression
    # Binary target: Sympathetic Stress (1) vs Non-Sympathetic (0)
    y_stress = (df['state'] == 'sympathetic').astype(int).values
    clf = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    clf.fit(X_scaled, y_stress)

    coefs = clf.coef_[0]
    odds_ratios = np.exp(coefs)

    driver_df = pd.DataFrame({
        'Feature': feat_cols,
        'Standardized_Beta': coefs,
        'Odds_Ratio': odds_ratios,
        'Absolute_Importance': np.abs(coefs)
    }).sort_values(by='Absolute_Importance', ascending=False)

    driver_df.to_csv(output_csv, index=False)

    # 4. Generate Visualizations
    # Figure 1: PCA Variance Explained & Biplot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Scree Plot
    comps = np.arange(1, len(var_exp) + 1)
    ax1.bar(comps, var_exp, alpha=0.7, color='#2b8cbe', label='Individual Explained Variance (%)')
    ax1.step(comps, cum_var_exp, where='mid', color='#e34a33', linewidth=2.5, label='Cumulative Variance (%)')
    ax1.axhline(80, color='grey', linestyle='--', label='80% Threshold')
    ax1.set_xlabel('Principal Component', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Explained Variance (%)', fontsize=11, fontweight='bold')
    ax1.set_title('PCA Scree & Cumulative Variance Profile', fontsize=12, fontweight='bold')
    ax1.set_xticks(comps)
    ax1.legend(loc='center right')

    # PC1 vs PC2 Scatter colored by state
    state_palette = {'relaxed': '#2b8cbe', 'parasympathetic': '#7bccc4', 'sympathetic': '#e34a33'}
    for state_name in ['relaxed', 'parasympathetic', 'sympathetic']:
        mask = (y == state_name)
        ax2.scatter(X_pca[mask, 0], X_pca[mask, 1], label=state_name.capitalize(),
                    alpha=0.75, s=50, color=state_palette[state_name], edgecolors='none')
    ax2.set_xlabel(f'PC1 ({var_exp[0]:.1f}% Variance)', fontsize=11, fontweight='bold')
    ax2.set_ylabel(f'PC2 ({var_exp[1]:.1f}% Variance)', fontsize=11, fontweight='bold')
    ax2.set_title('Biomarker Clustering in Latent Space (PC1 vs PC2)', fontsize=12, fontweight='bold')
    ax2.legend(title='Autonomic State', loc='upper right')

    plt.tight_layout()
    fig_path1 = os.path.join(output_fig_dir, 'pca_variance_and_biplot.png')
    plt.savefig(fig_path1, dpi=300, bbox_inches='tight')
    plt.close()

    # Figure 2: Top 15 Physiological Drivers of Sympathetic Stress
    top_drivers = driver_df.head(15).copy().sort_values(by='Standardized_Beta', ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#e34a33' if b > 0 else '#2b8cbe' for b in top_drivers['Standardized_Beta']]
    bars = ax.barh(top_drivers['Feature'], top_drivers['Standardized_Beta'], color=colors, edgecolor='black', alpha=0.85)
    ax.axvline(0, color='black', linestyle='-', linewidth=1)
    ax.set_xlabel('Standardized Model Coefficient (Beta)\n[Red: Increases Odds of Stress | Blue: Protective / Recovery]',
                  fontsize=11, fontweight='bold')
    ax.set_title('Top 15 Physiological Biomarker Drivers of Sympathetic Stress', fontsize=13, fontweight='bold', pad=15)

    plt.tight_layout()
    fig_path2 = os.path.join(output_fig_dir, 'biomarker_key_drivers.png')
    plt.savefig(fig_path2, dpi=300, bbox_inches='tight')
    plt.close()

    return {
        'driver_df': driver_df,
        'loadings_df': loadings_df,
        'var_exp': var_exp,
        'cum_var_exp': cum_var_exp
    }
