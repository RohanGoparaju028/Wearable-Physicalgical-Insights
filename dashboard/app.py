"""
dashboard/app.py
================
Interactive Streamlit Business Intelligence Dashboard for Wearable Biometrics
and Autonomic Nervous System (ANS) State Analytics.

Usage:
  streamlit run dashboard/app.py
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(
    page_title="Wearable Biometrics & ANS Analytics",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    /* Completely remove Streamlit Deploy button and cloud toolbar */
    [data-testid="stAppDeployButton"],
    .stAppDeployButton,
    .stDeployButton,
    [data-testid="stDeployButton"],
    [data-testid="stToolbarActions"],
    header [data-testid="stToolbarActions"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
        width: 0px !important;
        overflow: hidden !important;
        pointer-events: none !important;
    }

    /* Hide ONLY the screen recording item in the hamburger menu */
    [data-testid="stMainMenuItem-recordScreencast"] {
        display: none !important;
    }

    /* Hide Streamlit footer */
    footer {
        visibility: hidden !important;
    }

    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #2b8cbe;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    clean_path = 'data/processed/wearable_clean.csv'
    if not os.path.exists(clean_path):
        clean_path = 'wearable_data.csv'
    df = pd.read_csv(clean_path)
    return df


@st.cache_data
def load_stats():
    stats_path = 'reports/statistical_hypothesis_results.csv'
    if os.path.exists(stats_path):
        return pd.read_csv(stats_path)
    return None


@st.cache_data
def load_drivers():
    driver_path = 'reports/biomarker_key_drivers.csv'
    if os.path.exists(driver_path):
        return pd.read_csv(driver_path)
    return None


df_all = load_data()
df_stats = load_stats()
df_drivers = load_drivers()

# ── Sidebar Controls ─────────────────────────────────────────────────────────
st.sidebar.title("🩺 Cohort Filters")
st.sidebar.markdown("Filter sessions across participant demographics and session constraints:")

# Experience filter
exp_options = ['All'] + sorted(list(df_all['yoga_experience'].unique()))
selected_exp = st.sidebar.selectbox("Yoga Experience Level", exp_options)

# Difficulty filter
diff_options = ['All'] + sorted(list(df_all['difficulty_level'].unique()))
selected_diff = st.sidebar.selectbox("Posture Difficulty", diff_options)

# Gender filter
gender_options = ['All'] + sorted(list(df_all['gender'].unique()))
selected_gender = st.sidebar.selectbox("Gender Cohort", gender_options)

# Apply filters
df_filtered = df_all.copy()
if selected_exp != 'All':
    df_filtered = df_filtered[df_filtered['yoga_experience'] == selected_exp]
if selected_diff != 'All':
    df_filtered = df_filtered[df_filtered['difficulty_level'] == selected_diff]
if selected_gender != 'All':
    df_filtered = df_filtered[df_filtered['gender'] == selected_gender]

# ── Header ───────────────────────────────────────────────────────────────────
st.title("Wearable Biometrics & Autonomic Stress Analytics")
st.markdown("### Executive Dashboard for Digital Health, Wearable Sensors & ANS Monitoring")
st.markdown("---")

# ── Top KPIs ─────────────────────────────────────────────────────────────────
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_sessions = len(df_filtered)
unique_subjects = df_filtered['subject'].nunique()
sympathetic_count = (df_filtered['state'] == 'sympathetic').sum()
stress_rate = (sympathetic_count / total_sessions * 100) if total_sessions > 0 else 0
parasym_rate = ((df_filtered['state'] == 'parasympathetic').sum() / total_sessions * 100) if total_sessions > 0 else 0

kpi1.metric("Monitored Sessions", f"{total_sessions}", delta=f"{len(df_filtered) - len(df_all)} vs Total" if len(df_filtered) != len(df_all) else None)
kpi2.metric("Active Participants", f"{unique_subjects} Subjects")
kpi3.metric("Sympathetic (Stress) Rate", f"{stress_rate:.1f}%")
kpi4.metric("Parasympathetic (Recovery)", f"{parasym_rate:.1f}%")

# ── Tab Navigation ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview & Cohorts",
    "📈 Biometric Distributions",
    "🔬 Statistical Hypothesis Tests",
    "⚡ Key Drivers & PCA",
    "👤 Subject-Level Deep Dive"
])

# ── TAB 1: OVERVIEW & COHORTS ─────────────────────────────────────────────────
with tab1:
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.subheader("Autonomic Nervous System State Distribution")
        fig, ax = plt.subplots(figsize=(7, 4.5))
        state_order = ['relaxed', 'parasympathetic', 'sympathetic']
        colors = {'relaxed': '#2b8cbe', 'parasympathetic': '#7bccc4', 'sympathetic': '#e34a33'}
        sns.countplot(data=df_filtered, x='state', hue='state', order=state_order, palette=colors, legend=False, ax=ax)
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f"{int(height)} ({height/len(df_filtered)*100:.1f}%)",
                            (p.get_x() + p.get_width() / 2., height),
                            ha='center', va='baseline', fontsize=10, xytext=(0, 4), textcoords='offset points')
        ax.set_ylabel("Session Count")
        ax.set_xlabel("Autonomic State")
        st.pyplot(fig)
        plt.close()

    with col_b:
        st.subheader("Stress Rate (% Sympathetic) by Posture & Experience")
        crosstab = pd.crosstab(
            index=df_all['difficulty_level'],
            columns=df_all['yoga_experience'],
            values=(df_all['state'] == 'sympathetic').astype(int),
            aggfunc='mean'
        ) * 100

        fig, ax = plt.subplots(figsize=(7, 4.5))
        sns.heatmap(crosstab, annot=True, fmt='.1f', cmap='Reds', cbar_kws={'label': '% Sympathetic'}, ax=ax)
        ax.set_xlabel("Yoga Experience")
        ax.set_ylabel("Posture Difficulty")
        st.pyplot(fig)
        plt.close()

    st.info("💡 **Executive Takeaway**: Sympathetic stress arousal increases steeply with posture difficulty for beginners, but advanced practitioners maintain parasympathetic dominance even under harder physical postures.")

# ── TAB 2: BIOMETRIC DISTRIBUTIONS ───────────────────────────────────────────
with tab2:
    st.subheader("Biometric Signal Profiles Across Autonomic States")
    
    sensor_map = {
        'EDA - Mean Skin Conductance (µS)': 'eda_microsiemens_mean',
        'EDA - Phasic Variability (Std Dev)': 'eda_microsiemens_std_dev',
        'RR Interval - Heart Period (ms)': 'rr_interval_milliseconds_mean',
        'RR Interval - HRV Std Dev': 'rr_interval_milliseconds_std_dev',
        'BVP - Blood Volume Pulse RMS (nW)': 'bvp_light_absorption_nW_rms',
        'Skin Temperature (°C)': 'temperature_celcius_mean',
        'Accelerometer - Movement Magnitude': 'accelerometer_magnitude_mean',
        'Accelerometer - Tremor (Std Dev)': 'accelerometer_magnitude_std_dev'
    }

    selected_marker_label = st.selectbox("Select Physiological Biomarker to Inspect", list(sensor_map.keys()))
    feature_key = sensor_map[selected_marker_label]

    col_box, col_stats = st.columns([2, 1])

    with col_box:
        fig, ax = plt.subplots(figsize=(8, 4.5))
        colors = {'relaxed': '#2b8cbe', 'parasympathetic': '#7bccc4', 'sympathetic': '#e34a33'}
        sns.boxplot(data=df_filtered, x='state', y=feature_key, hue='state',
                    order=['relaxed', 'parasympathetic', 'sympathetic'], palette=colors, legend=False,
                    showmeans=True, meanprops={"marker": "o", "markerfacecolor": "white", "markeredgecolor": "black"}, ax=ax)
        ax.set_title(f"Distribution of {selected_marker_label}", fontsize=12, fontweight='bold')
        ax.set_xlabel("Autonomic State")
        ax.set_ylabel(feature_key)
        st.pyplot(fig)
        plt.close()

    with col_stats:
        st.markdown("**Descriptive Statistics by State:**")
        grp_stats = df_filtered.groupby('state')[feature_key].agg(['count', 'mean', 'std', 'median']).round(2)
        st.dataframe(grp_stats, use_container_width=True)

# ── TAB 3: STATISTICAL HYPOTHESIS TESTS ───────────────────────────────────────
with tab3:
    st.subheader("Non-Parametric Hypothesis Testing (Kruskal-Wallis & Post-Hoc)")
    st.markdown("Evaluating whether physiological signals show statistically significant differences across Autonomic States:")

    if df_stats is not None:
        display_stats = df_stats[[
            'Biomarker', 'Kruskal_H_Statistic', 'P_Value', 'Significant_at_0.05',
            'Eta_Squared_Effect_Size', 'Effect_Magnitude',
            'Sig_Rel_vs_Sym_Bonferroni', 'Sig_Para_vs_Sym_Bonferroni'
        ]].copy()
        display_stats['P_Value'] = display_stats['P_Value'].apply(lambda x: f"{x:.2e}")
        st.dataframe(display_stats, use_container_width=True)

        st.markdown("""
        * **Kruskal-Wallis H-Test**: Evaluates differences across `relaxed`, `parasympathetic`, and `sympathetic`.
        * **Eta-Squared ($\eta^2$)**: Quantifies effect magnitude ($\eta^2 \ge 0.14$ indicates a Large discriminative effect).
        * **Bonferroni Post-Hoc**: Evaluates pairwise contrasts with family-wise error rate control ($\alpha = 0.0167$).
        """)
    else:
        st.warning("Run `python run_analysis.py` to generate the hypothesis test results.")

# ── TAB 4: KEY DRIVERS & PCA ─────────────────────────────────────────────────
with tab4:
    col_d1, col_d2 = st.columns(2)

    with col_d1:
        st.subheader("Top Physiological Drivers of Stress")
        if df_drivers is not None:
            top_10 = df_drivers.head(10)
            fig, ax = plt.subplots(figsize=(8, 5))
            colors = ['#e34a33' if b > 0 else '#2b8cbe' for b in top_10['Standardized_Beta']]
            ax.barh(top_10['Feature'], top_10['Standardized_Beta'], color=colors, edgecolor='black')
            ax.axvline(0, color='black', linewidth=1)
            ax.set_xlabel("Standardized Model Coefficient (Beta)")
            ax.set_title("Biomarker Attribution: Sympathetic Activation Odds", fontsize=11, fontweight='bold')
            st.pyplot(fig)
            plt.close()
        else:
            st.warning("Driver analysis table not found. Run `python run_analysis.py` first.")

    with col_d2:
        st.subheader("PCA Latent Structure & Clustering")
        pca_fig_path = 'reports/figures/pca_variance_and_biplot.png'
        if os.path.exists(pca_fig_path):
            st.image(pca_fig_path, caption="PCA Scree Plot & 2D Latent Representation")
        else:
            st.info("Run `python run_analysis.py` to generate PCA biplot.")

# ── TAB 5: SUBJECT DEEP DIVE ─────────────────────────────────────────────────
with tab5:
    st.subheader("Subject-Level Biometric Profile")
    all_subjects = sorted(list(df_all['subject'].unique()))
    chosen_sub = st.selectbox("Select Subject", all_subjects)

    sub_df = df_all[df_all['subject'] == chosen_sub]
    c1, c2, c3 = st.columns(3)
    c1.metric("Subject Sessions", len(sub_df))
    c2.metric("Experience", sub_df['yoga_experience'].iloc[0].capitalize())
    c3.metric("Gender", sub_df['gender'].iloc[0].capitalize())

    st.markdown(f"**Session Breakdown for Subject `{chosen_sub}`:**")
    st.dataframe(sub_df[['state', 'posture_type', 'difficulty_level', 'eda_microsiemens_mean', 'rr_interval_milliseconds_mean', 'temperature_celcius_mean']].head(10), use_container_width=True)
