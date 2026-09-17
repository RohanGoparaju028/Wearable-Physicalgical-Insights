# Wearable Physiological Signal Analytics
### Biometric Stress Profiling, Autonomic Nervous System (ANS) State Classification & Cohort Analysis

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red.svg)](dashboard/app.py)
[![Analytics](https://img.shields.io/badge/Analytics-SciPy%20%7C%20Pandas%20%7C%20Scikit--Learn-orange.svg)](#key-findings--insights)

An end-to-end data analytics case study evaluating multi-modal wearable biometric signals during yoga sessions to assess autonomic nervous system (ANS) transitions across three target states: **Relaxed**, **Parasympathetic** (Rest-and-Digest), and **Sympathetic** (Fight-or-Flight / Stress).

---

## 📌 Executive Summary

Wearable health platforms are shifting from passive step counters to proactive autonomic health monitors. This project investigates how physiological signals (Electrodermal Activity, Blood Volume Pulse, Heart Period RR intervals, Skin Temperature, and 3D Accelerometry) capture acute stress responses, how posture difficulty drives physical and cognitive strain, and how practitioner experience buffers autonomic stability.

### Key Analytical Questions
1. **Biometric Signatures**: Which physiological sensors provide the highest discriminative power for detecting acute autonomic stress?
2. **Experience Buffering**: Does practitioner yoga experience moderate physiological strain during challenging physical postures?
3. **Driver Attribution**: What specific waveform characteristics (sample entropy, peak-to-RMS, variance) serve as the primary drivers of sympathetic activation?
4. **Product Recommendations**: How can digital health devices optimize battery life and deliver adaptive biofeedback?

---

## 🔬 Key Findings & Statistical Evidence

### 1. HRV & Accelerometer Tremor Provide the Strongest Discriminative Signal
Non-parametric **Kruskal-Wallis tests** across all 3 autonomic states revealed significant differences ($p < 0.05$) across all major biometric features:
* **Accelerometer Tremor Std Dev ($H = 88.90, p = 4.95 \times 10^{-20}$)**: Demonstrated the largest overall effect size ($\eta^2 = 0.365$, Large). Dynamic postural micro-tremors sharply differentiate stable parasympathetic states from sympathetic strain.
* **RR Interval HRV Std Dev ($H = 60.46, p = 7.45 \times 10^{-14}$)**: Very large effect size ($\eta^2 = 0.246$, Large). Autonomic stress significantly contracts heart period variability.
* **BVP Light Absorption RMS ($H = 42.10, p = 7.20 \times 10^{-10}$)**: Substantial effect size ($\eta^2 = 0.169$, Large), capturing peripheral vasoconstriction during acute autonomic stress.
* **Electrodermal Activity Mean ($H = 18.10, p = 0.000117$)**: Medium effect size ($\eta^2 = 0.068$), driven by sympathetic sweat gland activation.

### 2. The Experience Buffer Effect
* **Beginners**: Sympathetic stress rates jumped from **18.2%** in easy postures to **58.3%** in hard postures (>3x increase in acute strain).
* **Advanced Practitioners**: Maintained parasympathetic dominance even during difficult postures, keeping sympathetic activation capped below **25%**.
* **Clinical Takeaway**: Regular yoga practice conditions the autonomic nervous system to suppress fight-or-flight over-activation under physical exertion.

### 3. Top Physiological Drivers of Sympathetic Stress
Standardized multivariate logistic regression identified the primary positive drivers increasing the odds of sympathetic stress:
* **`bvp_light_absorption_sample_entropy`** ($\beta = +1.156$, **Odds Ratio = 3.18x**): Irregular pulse waveform complexity triples the odds of acute stress.
* **`eda_microsiemens_peak_to_rms`** ($\beta = +0.725$, **Odds Ratio = 2.07x**): Spiky galvanic skin conductance doubles the likelihood of stress arousal.
* **`accelerometer_magnitude_peak_to_peak`** ($\beta = +0.722$, **Odds Ratio = 2.06x**): Physical instability and dynamic corrections signify imminent strain.

---

## 🏗️ Project Architecture

```
Wearable_Physiological_Analytics/
│
├── data/
│   ├── raw/
│   │   └── wearable_data.csv               # Raw biometrics dataset (241 samples, 48 cols)
│   └── processed/
│       └── wearable_clean.csv              # Imputed, profiled, and standardized dataset
│
├── src/                                     # Modular Python Analytics Package
│   ├── __init__.py
│   ├── data_pipeline.py                    # Data loading, quality audit, and median imputation
│   ├── eda_profiler.py                     # Exploratory profiling, cross-tabs & correlation matrices
│   ├── hypothesis_tests.py                 # Kruskal-Wallis, Mann-Whitney U, and Eta-squared effect sizes
│   └── driver_analysis.py                  # Standardized driver attribution (odds ratios) & PCA
│
├── dashboard/
│   └── app.py                              # Interactive Streamlit BI Dashboard
│
├── notebooks/
│   └── wearable_analytics_walkthrough.ipynb # Narrative analytics walkthrough with figures
│
├── reports/
│   ├── executive_summary.md                # C-suite executive summary & product recommendations
│   ├── statistical_hypothesis_results.csv  # Full hypothesis testing results & p-values
│   ├── biomarker_key_drivers.csv           # Model coefficients, odds ratios, and rankings
│   └── figures/                            # Publication-quality analytical charts
│       ├── state_distribution_and_cohorts.png
│       ├── biometric_boxplots_by_state.png
│       ├── sensor_correlation_matrix.png
│       ├── experience_vs_difficulty_stress_heatmap.png
│       ├── hypothesis_test_significance.png
│       ├── pca_variance_and_biplot.png
│       └── biomarker_key_drivers.png
│
├── archive/
│   └── academic_assignment/                # Preserved original coursework questions & scripts
│
├── run_analysis.py                         # End-to-end analytical pipeline runner
├── main.py                                 # Clean entry point
└── requirements.txt                        # Project dependencies
```

---

## 🚀 Getting Started

### 1. One-Click Setup (No Docker Needed)

* **On macOS / Linux**:
  ```bash
  ./setup.sh
  ```
* **On Windows**:
  ```cmd
  setup.bat
  ```
*(The scripts automatically create an isolated virtual environment `.venv`, install requirements, and execute the analysis pipeline).*

### 2. Manual Execution
```bash
python3 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run_analysis.py
```

### 3. Launch the Interactive Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 📊 Dataset Modalities & Telemetry

| Sensor Modality | Primary Features Extracted | Physiological Relevance |
|---|---|---|
| **EDA (Electrodermal Activity)** | Mean, Std Dev, RMS, Peak-to-RMS, Sample Entropy | Sympathetic nervous tone & sweat gland arousal |
| **BVP (Blood Volume Pulse)** | Mean, Light Absorption RMS, Sample Entropy, Num Peaks | Cardiac cycle blood volume pulse & vasoconstriction |
| **RR Interval (HRV)** | Mean Heart Period, Std Dev, RMS, Derivatives | Parasympathetic vagal tone & heart rate variability |
| **Skin Temperature** | Mean, Std Dev, RMS, Peak-to-Peak | Peripheral thermoregulation & stress vasoconstriction |
| **Accelerometer** | 3-Axis Magnitude Mean, Std Dev, RMS, Tremor | Postural stability, motion artifacts, and muscular strain |

---

## 💡 Strategic Recommendations for Wearable Tech

1. **Hierarchical Sensor Duty-Cycling (Battery Optimization)**:
   * *Problem*: High-power optical BVP and high-frequency accelerometry drain wearable batteries rapidly.
   * *Solution*: Keep ultra-low-power EDA and temperature sensors running as passive sentinels. Trigger high-frequency BVP and accelerometry sampling only when EDA phasic variability indicates active stress transitions.
2. **Adaptive In-Session Biofeedback**:
   * *Problem*: Users often cross the threshold into sympathetic exhaustion before realizing they are straining.
   * *Solution*: When RR-interval variability drops below subject baseline while micro-tremor spikes, trigger subtle haptic pacing prompts (e.g., resonant 4-7-8 breathing) to re-engage parasympathetic vagal control.
3. **Experience-Calibrated Workout Guidance**:
   * *Problem*: Static workout timers cause beginner burnout while failing to challenge experienced users.
   * *Solution*: Adapt posture hold durations dynamically based on individual real-time sympathetic tone rather than fixed intervals.

---

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
