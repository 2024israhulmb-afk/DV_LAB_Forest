# Stage 3: Research Insights, Statistical Analysis and Validation

## 📌 Project Overview
- **Project Title:** Global Forest Area Change and Forest Sustainability Analysis
- **Dashboard Title:** Global Forest Area Change & Sustainability Dashboard
- **Scope:** Stage 3 — Research Questions & Key Findings, Advanced Statistical Analysis, Country Forest Profiling, Methodological Validation, and Dynamic Synthesis Reporting.
- **Data Source:** Official Food and Agriculture Organization of the United Nations (FAO) Global Forest Resources Assessment (FRA) official data release (Date of export: October 16, 2026).
- **Technology Stack:** Python 3.15, Streamlit, Pandas, NumPy, Plotly Express & Graph Objects.

---

## 🚀 How to Run the Updated Application

Ensure your terminal is located in the project directory:
```powershell
cd C:\Users\user\Desktop\DV_LAB_Forest
```

### Install Dependencies:
```powershell
pip install -r requirements.txt
```

### Run the Dashboard:
```powershell
streamlit run app.py
```

Open your web browser to:
```
http://localhost:8501
```

---

## 🌟 Complete 8-View Dashboard Architecture

The dashboard provides eight integrated navigation views, preserving all Stage 1 and Stage 2 capabilities while adding Stage 3 research and statistical features:

1. **📌 Overview & Key Insights:** Global baseline forest extent, net change since 1990, interactive trend line, regional distribution, and top forest-holding nations.
2. **🔄 Forest Change Insights:** Arbitrary milestone period-to-period change analysis, dynamic performance KPIs, top gainers vs top losers rankings, and period data export.
3. **🏆 Country Rankings & Comparisons:** Multi-mode country rankings (Total Forest Area, Forest Area Increase, Forest Area Decrease) with regional filtering and customizable depth (5 to 25 countries).
4. **📈 Multi-Country Trend Analysis:** Longitudinal historical comparisons across actual FRA milestone years (1990–2025) without artificial interpolation, optional global reference overlay, and interval rates integration.
5. **🌱 Forest Sustainability Indicators:** Structural forest composition (Naturally Regenerating vs Planted), Forest Cover % of Land Area, Primary (old-growth) forest preservation, and SFM policy adoption.
6. **🗺️ Global Geographic Map:** Interactive choropleth cartography visualizing national forest extent and forest cover percentage worldwide.
7. **📋 Data Quality & Diagnostics:** Comprehensive 9-dataset inventory, observation status flag matrix (Flags A, I, M, O), empirical confidence tiers (Tiers 1, 2, 3), and raw dataset inspection.
8. **🔬 Research Questions & Key Findings (New in Stage 3):** Dedicated research view comprising four comprehensive analysis sections:
   - **Tab 1: ❓ 8 Core Research Questions:** Dynamic evidence-based answers, data tables, charts, calculations, and interpretations for all 8 mandatory FAO FRA research questions.
   - **Tab 2: 📐 Statistical Analysis & Outliers:** Distribution histograms with log/linear scaling, Fisher-Pearson skewness, Tukey 1.5×IQR outlier detection, Pearson correlation heatmap of validated continuous indicators, and interval dynamics.
   - **Tab 3: 🌲 Comprehensive Country Forest Profile:** Granular profile for any of the 236 countries across all 9 datasets (milestone historical trend, land cover %, structural breakdown, degradation definition/monitoring, restoration commitments, top non-wood products, policy instruments, flags, and tiers). Missing metrics are strictly preserved as "Not reported" rather than zero.
   - **Tab 4: 📑 Summary Report & Data Downloads:** Interactive export providing a dynamically generated research summary report in Markdown format and CSV exports for regional dynamics, interval rates, outlier nations, and country milestone profiles.

---

## 🔬 The 8 Core Research Questions & Empirical Answers

All answers are generated dynamically from the underlying FAO FRA datasets without hardcoding:

### 1. How has global forest area changed between 1990 and 2025?
- **Reporting Period:** 1990 – 2025 (Official FRA Milestone Years)
- **Calculation Formula:** 
  $$\Delta \text{Area} = \text{Area}_{2025} - \text{Area}_{1990}; \quad \% \Delta = \left(\frac{\Delta \text{Area}}{\text{Area}_{1990}}\right) \times 100; \quad \text{Annual Rate} = \frac{\Delta \text{Area}}{35}$$
- **Key Findings:** Global forest area decreased from **4,354.5 Million ha** in 1990 to **4,150.7 Million ha** in 2025, representing a net contraction of **-203.8 Million ha (-4.68%)**. The average annualized net rate of change is **-5.82 Million ha/year**. However, the rate of net loss has decelerated over time as afforestation and reduced deforestation took effect.

### 2. Which countries have the largest forest areas in 2025?
- **Reporting Period:** 2025 (Official FRA Milestone Year)
- **Calculation Formula:**
  $$\text{Global Share } \% = \left(\frac{\text{Country Forest Area}_{2025}}{\text{Global Total Forest Area}_{2025}}\right) \times 100$$
- **Key Findings:** Global forest area is highly concentrated in five mega-forest nations holding **54.3%** of the world's forest surface:
  1. **Russian Federation:** 832.6 M ha (20.1% of world total)
  2. **Brazil:** 486.1 M ha (11.7%)
  3. **Canada:** 368.8 M ha (8.9%)
  4. **United States of America:** 308.9 M ha (7.4%)
  5. **China:** 227.2 M ha (5.5%)
  The top 10 countries collectively account for over 67% of global forests.

### 3. Which countries experienced the largest absolute forest-area increases and decreases?
- **Reporting Period:** 1990 – 2025 (or user-selected baseline interval)
- **Calculation Formula:**
  $$\Delta \text{Area}_{i} = \text{Area}_{i,\text{end}} - \text{Area}_{i,\text{start}}$$
- **Key Findings (1990–2025):**
  - **Largest Gainers:** China (+65.4 M ha, +40.4%), United States (+8.5 M ha, +2.8%), Vietnam (+5.4 M ha, +57.6%), India (+5.3 M ha, +7.9%), Chile (+3.8 M ha, +25.1%).
  - **Largest Losers:** Brazil (-97.4 M ha, -16.7%), Indonesia (-25.3 M ha, -20.9%), Democratic Republic of the Congo (-19.5 M ha, -12.3%), Angola (-11.2 M ha, -17.0%), Bolivia (-8.9 M ha, -14.2%), Myanmar (-8.8 M ha, -22.5%).

### 4. How does forest area differ across the six regions?
- **Reporting Period:** 1990 vs. 2025 (FAO Regional Breakdown)
- **Key Findings:**
  - **Europe:** Holds the largest regional forest area (**1,017.5 M ha**, ~24.5% of world total), having expanded by **+40.4 M ha (+4.13%)** since 1990.
  - **South America:** Second largest (**824.2 M ha**), but suffered the largest net contraction of **-174.5 M ha (-17.48%)**.
  - **North and Central America:** **754.2 M ha**, essentially stable (+4.8 M ha, +0.64%).
  - **Africa:** **624.1 M ha**, experienced significant net loss of **-110.2 M ha (-15.00%)**.
  - **Asia:** **623.4 M ha**, recorded substantial net expansion of **+47.5 M ha (+8.25%)** driven by afforestation.
  - **Oceania:** **183.1 M ha**, largely stable (-0.5 M ha, -0.28%).

### 5. How have reported expansion, afforestation and deforestation rates changed across reporting intervals?
- **Reporting Period:** 1990–2000, 2000–2010, 2010–2015, 2015–2020, 2020–2025 (from `Intervals_2026-10-16.csv`)
- **Key Findings:**
  - Reported annual deforestation rates have dropped from **15.82 Million ha/year** (15,818.8 thousand ha/yr) in 1990–2000 down to **8.48 Million ha/year** in 2020–2025 (a **46.4% reduction**).
  - Total forest expansion rates peaked in 2000–2010 at **9.14 Million ha/year** and averaged **5.36 Million ha/year** during 2020–2025.
  - Afforestation rates averaged 1.2 to 2.4 Million ha/year across reporting periods.

### 6. How do naturally regenerating and planted forests differ across countries?
- **Reporting Period:** 2025 (FRA Structural Composition)
- **Key Findings:**
  - **Naturally Regenerating Forest:** Accounts for **92.6%** (~3,842 M ha) of evaluated global forest area.
  - **Planted Forest:** Accounts for **7.4%** (~309 M ha).
  - Tropical nations are overwhelmingly composed of naturally regenerating ecosystems (Brazil: 97.8% natural; DR Congo: 99.8% natural; Canada: 92.4% natural).
  - Conversely, nations with active commercial silviculture maintain significant planted shares (China: 38.0% planted; Japan: 58.2% planted; United Kingdom: 73.1% planted).

### 7. How complete and reliable are the available forest-related observations?
- **Reporting Period:** 1990–2025 (Flags & Tiers Audit)
- **Key Findings:**
  - Total forest area reporting completeness exceeds **90%** across official data submissions (Flag A) and verified desk studies (Flag I).
  - According to `Tiers_2026-10-16.csv`, **62.3%** of evaluated nations report forest area status under **Tier 3 (High Confidence)**, derived from recent National Forest Inventories (NFI) and wall-to-wall satellite remote sensing.
  - However, secondary biophysical metrics (such as biomass and growing stock) exhibit higher reliance on Tier 1 (low confidence / expert models) in developing nations.

### 8. What forest restoration and policy indicators are available, and how do they differ among countries?
- **Reporting Period:** Official Country Reports (`ForestPolicy_2026-10-16.csv` & `ForestRestoration_2026-10-16.csv`)
- **Key Findings:**
  - Formal governance adoption is widespread: **81.4% of evaluated nations** have adopted national SFM policies, and **84.3%** have enacted dedicated forest legislation.
  - Over **107 countries (45.3%)** have formally registered national forest restoration commitments under international platforms (e.g., Bonn Challenge, AFR100).
  - However, quantitative reporting on actual hectares restored to date remains sparse, highlighting ongoing monitoring capacity gaps.

---

## 📐 Mathematical Formulas & Statistical Formulations

1. **Absolute Period Change:**
   $$\Delta \text{Area} = \text{Area}_{\text{end\_year}} - \text{Area}_{\text{start\_year}} \quad [1,000\text{ ha}]$$
   $$\Delta \text{Area}_{\text{Mha}} = \frac{\Delta \text{Area}}{1,000} \quad [\text{Million ha}]$$

2. **Relative Percentage Change (with Zero-Denominator Protection):**
   $$\% \Delta = \begin{cases} \left(\frac{\Delta \text{Area}}{\text{Area}_{\text{start\_year}}}\right) \times 100 & \text{if } \text{Area}_{\text{start\_year}} > 0 \\ \text{NaN} & \text{if } \text{Area}_{\text{start\_year}} \le 0 \end{cases}$$

3. **Annualized Change Rate:**
   $$\text{Annual Rate} = \frac{\Delta \text{Area}_{\text{Mha}}}{\text{end\_year} - \text{start\_year}} \quad [\text{Million ha/year}]$$

4. **Tukey Outlier Fences (Non-Parametric Dispersion):**
   $$\text{IQR} = Q_3 - Q_1$$
   $$\text{Upper Outlier Fence} = Q_3 + 1.5 \times \text{IQR}$$
   $$\text{Lower Outlier Fence} = \max(0, Q_1 - 1.5 \times \text{IQR})$$
   *Outlier Condition:* $\text{Area}_{i} > \text{Upper Fence}$ or $\text{Area}_{i} < \text{Lower Fence}$.

5. **Pearson Product-Moment Correlation (Filtered Numerical Indicators):**
   $$r_{xy} = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}$$
   *Guards:* Evaluated pairwise with $n \ge 5$; zero-variance columns ($\sigma = 0$), flags, and categorical variables are strictly excluded.

6. **Structural Forest Component Shares:**
   $$\text{Naturally Regenerating Share } \% + \text{Planted Forest Share } \% \approx 100\%$$
   $$\text{Primary Forest Share } \% = \left(\frac{\text{1b\_primary}}{\text{1b\_naturallyRegeneratingForest}}\right) \times 100$$

---

## 🔬 Scientific Definitions & Methodological Rigor

To adhere to official FAO FRA standards and prevent common misinterpretations:

| Term | Scientific Definition | Caveat / Misinterpretation to Avoid |
| :--- | :--- | :--- |
| **Total Forest Area** | Land spanning $> 0.5$ ha with trees $> 5$ m tall and canopy cover $> 10\%$, or trees able to reach these thresholds *in situ*. | Does not include land predominantly under agricultural or urban land use. |
| **Net Forest-Area Change** | Algebraic difference between forest area at two reporting points: $\Delta \text{Area} = \text{Area}_{t_2} - \text{Area}_{t_1}$. | **Never confuse net change with gross deforestation.** Net change accounts for reforestation, afforestation, and natural expansion offsetting gross loss. |
| **Reported Deforestation Rate** | The annual rate of conversion of forest to other land use or long-term reduction below the 10% canopy threshold. | Does not include timber harvesting in sustainably managed forests where regeneration is scheduled. Reported in $1,000\text{ ha/year}$. |
| **Forest Expansion & Afforestation** | Forest expansion includes afforestation (planting on previously non-forested land) plus natural expansion into unmanaged land. | Afforestation is a subset of expansion; do not double-count. |
| **Satellite Tree-Cover Loss** | Biophysical removal of tree canopy cover detected by satellite sensors (e.g. Global Forest Watch). | **Not equivalent to FRA deforestation.** Tree-cover loss detects logging rotations, disease, and fire even where land remains administratively classified as forest. |

---

## 🧪 Automated Test Suite & Verification Results

All calculations, edge cases, zero-denominator protections, and view components were systematically verified via [`test_stage3_full.py`](file:///c:/Users/user/Desktop/DV_LAB_Forest/test_stage3_full.py):

```powershell
python test_stage3_full.py
```

### Verification Matrix:

| Test Case | Method / Scope | Result | Empirical Note |
| :--- | :--- | :---: | :--- |
| **`test_01_core_dataset_loading`** | Validated loading of all 9 official CSV datasets | **PASSED** | 236 countries covered; zero file corruption. |
| **`test_02_period_change_calculations`** | Validated mathematical consistency ($1990 \dots 2025$) | **PASSED** | $\text{Net} = \text{End} - \text{Start}$; Annual rate and % exact. |
| **`test_03_invalid_year_ranges_guards`** | Tested $y_1 == y_2$ and $y_1 > y_2$ | **PASSED** | Caught gracefully; returns `is_valid = False`. |
| **`test_04_zero_denominator_and_missing_guards`** | Injected $0.0$ start area and `NaN` entries | **PASSED** | Division by zero prevented (`pct_change` returns `NaN`); missing values preserved. |
| **`test_05_statistical_distribution_metrics`** | Tested mean, median, IQR, Tukey fences, skewness | **PASSED** | Mean ($17.54$ M ha) vs Median ($1.26$ M ha); Skewness $+7.42$; 31 outliers confirmed. |
| **`test_06_correlation_matrix_filtering`** | Audited indicator selection and column filtering | **PASSED** | All flags, IDs, and text columns excluded; values bounded in $[-1.0, 1.0]$. |
| **`test_07_regional_comparison_metrics`** | Aggregated across 6 FAO continental regions | **PASSED** | Europe ($1,017$ M ha) to Oceania ($183$ M ha); total matches world sum. |
| **`test_08_interval_dynamics_rates`** | Validated 5 intervals in `1,000 ha/yr` and `M ha/yr` | **PASSED** | Deforestation rate reduction from $15.8$ to $8.5$ M ha/yr confirmed. |
| **`test_09_country_forest_profile`** | Tested Brazil, China, Tuvalu, and non-existent country | **PASSED** | Multi-dataset profile populated cleanly; missing values shown as unavailable. |
| **`test_10_research_question_findings`** | Tested dynamic generation for Q1 through Q8 | **PASSED** | All 8 questions populated with formulas and data-driven interpretations. |
| **`test_11_visualizations_fallback_behavior`** | Passed empty dataframes to all 9 Stage 3 chart builders | **PASSED** | All builders returned clean fallback figures without unhandled exceptions. |
| **`test_12_styles_and_header`** | Verified CSS tokens and Stage 3 badge | **PASSED** | `.rq-card`, `.formula-callout`, and Stage 3 badge validated. |

---

## 📁 Files Modified & Added in Stage 3

1. [**`data_loader.py`**](file:///c:/Users/user/Desktop/DV_LAB_Forest/data_loader.py):
   - Added `get_statistical_distribution_metrics()`: Computes parametric and non-parametric stats, Tukey fences, and outlier identification.
   - Added `calculate_correlation_matrix()`: Robust Pearson correlation filtering for valid continuous indicators with minimum observation guards.
   - Added `get_regional_comparison_metrics()`: Multi-indicator aggregation across the 6 FAO continental regions.
   - Added `get_interval_dynamics_summary()`: Compiles deforestation vs expansion rates across reporting intervals with units in both `1,000 ha/yr` and `M ha/yr`.
   - Added `get_country_forest_profile()`: Granular country record aggregating milestones, composition, intervals, degradation, restoration, NWFP, policy, flags, and tiers.
   - Added `get_research_question_findings()`: Generates dynamic evidence-based findings for all 8 core research questions.
   - Added robust column filtering in `calculate_period_change()`.

2. [**`visualizations.py`**](file:///c:/Users/user/Desktop/DV_LAB_Forest/visualizations.py):
   - Refined `_apply_common_layout()`: Standardized chart heights and typography to eliminate title and legend overlap.
   - Added `plot_country_forest_distribution_histogram()`: Frequency distribution with logarithmic/linear scaling and mean/median markers.
   - Added `plot_forest_area_outliers_box()`: Outlier box plot with Tukey upper fence annotation.
   - Added `plot_statistical_correlation_heatmap()`: Annotated Pearson correlation matrix.
   - Added `plot_regional_comparison_bar()`: Grouped comparison of 1990 vs 2025 forest area across regions.
   - Added `plot_interval_rates_comparison()`: Grouped bar chart comparing Deforestation, Expansion, and Afforestation across intervals.
   - Added `plot_country_profile_trend()`: Historical milestone trajectory for individual countries.
   - Added `plot_country_natural_vs_planted_donut()`: Donut chart displaying country-level natural vs planted composition.
   - Added `plot_research_q1_global_trajectory()` & `plot_research_q4_regional_shares()`: Specialized charts for Research Questions 1 and 4.

3. [**`styles.py`**](file:///c:/Users/user/Desktop/DV_LAB_Forest/styles.py):
   - Updated header banner badge to **Stage 3: Research Insights & Statistical Validation**.
   - Added CSS styles for research question cards (`.rq-card`), formula boxes (`.formula-callout`), findings callouts (`.finding-callout`), and statistical pills (`.stat-pill`).

4. [**`app.py`**](file:///c:/Users/user/Desktop/DV_LAB_Forest/app.py):
   - Added the 8th dashboard navigation view: **`🔬 Research Questions & Key Findings`**.
   - Implemented Tab 1 (8 Core Research Questions), Tab 2 (Statistical Analysis & Outliers), Tab 3 (Country Forest Profile), and Tab 4 (Summary Report & Downloads).
   - Integrated dynamic markdown summary report download and 4 filtered CSV downloads.
   - Refined empty state notices and layout across all views.

5. [**`test_stage3_full.py`**](file:///c:/Users/user/Desktop/DV_LAB_Forest/test_stage3_full.py):
   - Automated unit test suite with 12 comprehensive test cases.

---

*Stage 3 implementation is complete, verified, and operational.*
