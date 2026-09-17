"""
run_analysis.py
===============
End-to-end execution script for the Wearable Physiological Data Analytics pipeline.

Executes:
  1. Data Ingestion, Profiling & Median Imputation
  2. Exploratory Biometric & Cohort Analysis
  3. Non-Parametric Hypothesis Testing & Effect Size Analysis
  4. Biomarker Driver Identification & PCA Latent Mapping
"""

import sys
import time
from src.data_pipeline import load_and_clean_data
from src.eda_profiler import generate_eda_reports
from src.hypothesis_tests import run_statistical_hypothesis_tests
from src.driver_analysis import run_biomarker_driver_analysis


def main():
    start_time = time.time()
    print("=" * 80)
    print("  WEARABLE BIOMETRICS & AUTONOMIC STRESS DATA ANALYTICS PIPELINE")
    print("=" * 80)

    # 1. Ingestion & Quality Audit
    print("\n[1/4] Ingesting & Cleaning Data...")
    df_clean, profile = load_and_clean_data(
        raw_data_path='data/raw/wearable_data.csv',
        processed_data_path='data/processed/wearable_clean.csv'
    )
    print(f"      Initial records: {profile['initial_shape'][0]} rows, {profile['initial_shape'][1]} columns")
    print(f"      Clean dataset:   {profile['clean_shape'][0]} rows, {profile['clean_shape'][1]} columns")
    print(f"      Features imputed: {len(profile['cols_imputed'])} features using robust median strategy")
    print(f"      Unique subjects: {profile['subjects_count']}")
    print(f"      State distribution: {profile['classes']}")

    # 2. Exploratory Data Analysis & Cohort Profiling
    print("\n[2/4] Generating Exploratory Biometric & Cohort Visualizations...")
    eda_results = generate_eda_reports(df_clean, output_dir='reports/figures')
    print(f"      Generated {len(eda_results['figures'])} analytical visualizations:")
    for fig in eda_results['figures']:
        print(f"        • {fig}")

    # 3. Statistical Hypothesis Testing
    print("\n[3/4] Running Inferential Statistical Hypothesis Tests (Kruskal-Wallis & Post-hoc)...")
    hypo_results = run_statistical_hypothesis_tests(
        df_clean,
        output_csv='reports/statistical_hypothesis_results.csv',
        output_fig_dir='reports/figures'
    )
    sig_count = (hypo_results['Significant_at_0.05'] == 'Yes').sum()
    print(f"      Tested {len(hypo_results)} key biomarkers across ANS states.")
    print(f"      {sig_count}/{len(hypo_results)} biomarkers showed statistically significant differences (p < 0.05).")
    print(f"      Results saved to: reports/statistical_hypothesis_results.csv")

    # 4. Biomarker Driver Analysis & PCA
    print("\n[4/4] Extracting Biomarker Drivers & Latent PCA Variance...")
    driver_results = run_biomarker_driver_analysis(
        df_clean,
        output_csv='reports/biomarker_key_drivers.csv',
        output_fig_dir='reports/figures'
    )
    top_5_pos = driver_results['driver_df'].sort_values(by='Standardized_Beta', ascending=False).head(5)
    print("\n      Top 5 Positive Drivers of Sympathetic Stress (Odds Ratio > 1):")
    for _, row in top_5_pos.iterrows():
        print(f"        • {row['Feature'][:38]:<38} | Beta: {row['Standardized_Beta']:+.3f} | OR: {row['Odds_Ratio']:.2f}x")

    elapsed = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"  PIPELINE EXECUTION COMPLETED IN {elapsed:.2f} SECONDS")
    print("  Artifacts created:")
    print("    - Clean Data:       data/processed/wearable_clean.csv")
    print("    - Hypothesis Stats: reports/statistical_hypothesis_results.csv")
    print("    - Biomarker Drivers: reports/biomarker_key_drivers.csv")
    print("    - Analytical Plots: reports/figures/")
    print("=" * 80)


if __name__ == '__main__':
    main()
