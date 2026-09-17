# How to Run the Project
### Wearable Biometrics & Autonomic Stress Analytics Guide

This guide provides step-by-step instructions on setting up your environment and running all components of the Wearable Physiological Data Analytics project.

---

## 1. Zero-Config Cross-Platform Setup (No Docker Required)

You can run this project on **any system (macOS, Windows, Linux)** with a single command without needing Docker.

### On macOS / Linux:
Run the included automated setup script:
```bash
./setup.sh
```
*(This automatically creates an isolated `.venv`, installs all dependencies, and runs the analytics pipeline).*

### On Windows:
Double-click `setup.bat` or run in Command Prompt / PowerShell:
```cmd
setup.bat
```

---

## 2. Manual Setup (Standard Python virtual environment)

If you prefer to configure the environment manually on any OS:

```bash
# 1. Create a virtual environment
python3 -m venv .venv       # On Windows: python -m venv .venv

# 2. Activate it
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt
```

---

## 2. Running Options

### Option A: Run the End-to-End Analytics Pipeline (Recommended CLI)

To execute the complete data pipeline from raw data to statistical reports and visualization charts:

```bash
python run_analysis.py
```
*(or equivalently: `python main.py`)*

#### What Happens During Execution:
1. **Data Ingestion & Hygiene** (`src/data_pipeline.py`):
   * Ingests `data/raw/wearable_data.csv`.
   * Audits missing values and applies median imputation for sample entropy features.
   * Exports the cleaned dataset to `data/processed/wearable_clean.csv`.
2. **Exploratory Cohort Profiling** (`src/eda_profiler.py`):
   * Generates target state distributions, cohort breakdowns, and sensor correlation heatmaps.
3. **Statistical Hypothesis Testing** (`src/hypothesis_tests.py`):
   * Runs non-parametric Kruskal-Wallis H-tests across states.
   * Computes Eta-squared ($\eta^2$) effect sizes and Bonferroni-corrected pairwise post-hoc tests.
   * Exports results to `reports/statistical_hypothesis_results.csv`.
4. **Biomarker Driver Identification & PCA** (`src/driver_analysis.py`):
   * Performs standardized multivariate logistic regression to derive stress odds ratios ($e^\beta$).
   * Fits PCA to extract sensor factor loadings and latent space representations.
   * Exports top drivers to `reports/biomarker_key_drivers.csv`.

**Execution Time**: ~1–2 seconds.

---

### Option B: Launch the Interactive BI Dashboard (Streamlit)

To explore the findings interactively in a web interface:

```bash
streamlit run dashboard/app.py
```

The app will launch in your default web browser (typically at `http://localhost:8501`).

#### Dashboard Highlights:
* **Sidebar Filters**: Filter telemetry by **Yoga Experience** (`beginner`, `intermediate`, `advanced`), **Posture Difficulty** (`easy`, `medium`, `hard`), and **Gender**.
* **Tabs**:
  1. **📊 Overview & Cohorts**: Session metrics, ANS class balance, and stress prevalence heatmaps.
  2. **📈 Biometric Distributions**: Dynamic boxplot viewer for any sensor modality across states.
  3. **🔬 Statistical Hypothesis Tests**: Full Kruskal-Wallis table with significance flags and effect size ratings.
  4. **⚡ Key Drivers & PCA**: Biomarker odds ratio attribution and 2D latent PCA projection.
  5. **👤 Subject-Level Deep Dive**: Individual participant sensor records benchmarked against cohort averages.

---

### Option C: Run the Jupyter Notebook Walkthrough

To follow the narrative, analysis steps, and visualizations in an interactive notebook:

```bash
jupyter notebook notebooks/wearable_analytics_walkthrough.ipynb
```


---

## 3. Where to Find Generated Outputs

After running the pipeline, generated deliverables are organized in:

| Output Directory | Content |
|---|---|
| `data/processed/wearable_clean.csv` | Cleaned and imputed dataset ready for downstream analysis |
| `reports/statistical_hypothesis_results.csv` | Full statistical test summary (H-stats, p-values, $\eta^2$ effect sizes) |
| `reports/biomarker_key_drivers.csv` | Ranked physiological drivers with standardized betas & odds ratios |
| `reports/figures/` | High-resolution publication charts (`.png`): |
| &nbsp;&nbsp;├─ `state_distribution_and_cohorts.png` | Class prevalence & demographic breakdowns |
| &nbsp;&nbsp;├─ `biometric_boxplots_by_state.png` | Key sensor boxplots across ANS states |
| &nbsp;&nbsp;├─ `sensor_correlation_matrix.png` | Cross-modality sensor correlation matrix |
| &nbsp;&nbsp;├─ `experience_vs_difficulty_stress_heatmap.png` | Stress rate matrix across experience & difficulty |
| &nbsp;&nbsp;├─ `hypothesis_test_significance.png` | Significance & effect size visual rankings |
| &nbsp;&nbsp;├─ `pca_variance_and_biplot.png` | Scree plot & latent biomarker clustering |
| &nbsp;&nbsp;└─ `biomarker_key_drivers.png` | Top 15 positive/negative stress drivers |
| `reports/executive_summary.md` | Executive summary report with clinical & product recommendations |

---

## 4. Troubleshooting & FAQ

* **Issue: `ModuleNotFoundError: No module named 'streamlit'`**
  * *Solution*: Run `pip install streamlit` or `pip install -r requirements.txt`.
* **Issue: File not found when running from a subdirectory**
  * *Solution*: Always run the commands from the root project directory (`Wearable_Physiologicla_Classification/`).
