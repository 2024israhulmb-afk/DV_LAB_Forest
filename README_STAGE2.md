# Stage 2: Advanced Forest Data Analysis and Dashboard Enhancements

## 📌 Project Overview
- **Project Title:** Global Forest Area Change and Forest Sustainability Analysis
- **Dashboard Title:** Global Forest Area Change & Sustainability Dashboard
- **Scope:** Stage 2 — Advanced Forest Change Insights, Multi-Country Rankings, Longitudinal Trajectories, Sustainability Indicators, and Methodological Data Quality Diagnostics.
- **Data Source:** Official Food and Agriculture Organization (FAO) Global Forest Resources Assessment (FRA) official data release (Date of export: October 16, 2026).

---

## 🚀 How to Run the Dashboard

Make sure your terminal is located in the project folder:
```powershell
cd C:\Users\user\Desktop\DV_LAB_Forest
```

### Install Dependencies:
```powershell
pip install -r requirements.txt
```

### Start the Dashboard:
```powershell
streamlit run app.py
```
Open your browser to:
```
http://localhost:8501
```

---

## 🌟 New Features in Stage 2

### 1. Dedicated "Forest Change Insights" Page
- **Arbitrary Reporting Milestone Selection:** Allows comparing any valid pair of reporting milestone years (1990, 2000, 2010, 2015, 2020, 2025) where ending year > starting year.
- **Dynamic Period KPI Performance Cards:**
  - *Period Net Change (M ha and %)*
  - *Annualized Change Rate (M ha/year)*
  - *Count of Forest Expanding Nations*
  - *Count of Forest Declining Nations*
- **Gainers vs Losers Visualizations:**
  - *Top 10 Forest Gainers* (emerald green, formatted with absolute M ha gain and % relative increase).
  - *Top 10 Forest Losers* (crimson/coral, formatted with absolute M ha loss and % relative decrease).
- **Searchable Period Change Data Table & CSV Download:** Users can search any country and download the filtered analysis results directly via a built-in download button.
- **Scientific Methodology Callout:** Explicitly clarifies the difference between **Net Forest-Area Change** (algebraic sum of expansions minus deforestation) and **Gross Deforestation / Satellite Tree-Cover Loss**.

### 2. Dedicated "Country Rankings & Comparisons" Page
- **Three Ranking Modes:**
  1. *Top Countries by Total Forest Area* for any selected year (with % share of global/regional total).
  2. *Top Countries with Forest Area Increase* over the chosen period.
  3. *Top Countries with Forest Area Decrease* over the chosen period.
- Filterable by continent/region, with a dynamic slider to choose the number of ranked nations (5 to 25).
- Accompanying tabulated data summaries with formatted columns and clear units.

### 3. Enhanced "Multi-Country Trend Analysis" Page
- **Interactive Multi-Country Comparison:** Select 2 to 10 specific countries simultaneously (e.g., Brazil, China, DR Congo, Russia, USA, Indonesia) to evaluate their trajectories side-by-side.
- **Milestone Subsetting:** Filter to any subset of actual FRA milestone years (no interpolated or synthetic observations).
- **Global Total Reference Trace:** Option to overlay the global total forest area trajectory on a secondary axis.
- **Interval Rates Integration:** Tabulated annual average rates of expansion, afforestation, and deforestation from `Intervals_2026-10-16.csv`.

### 4. Dedicated "Forest Sustainability Indicators" Page
- **Natural vs Planted Forests:** Evaluates naturally regenerating forests vs planted forests for major nations, proving that natural forests represent ~92% of world canopy while planted forests constitute ~8%. Avoids double-counting: `Natural + Planted ≈ Total Forest Area`.
- **Forest Area as a % of Land Area:** Ranks countries with the highest (e.g. Suriname, Guyana, Gabon >80%) and lowest forest cover density relative to national land area.
- **Primary (Old-Growth) Forest Extent:** Maps the preservation extent of intact native primary ecosystems (Brazil, Canada, Russia, DR Congo, Peru, Indonesia).
- **Policy & Governance Adoption:** Integrates `ForestPolicy_2026-10-16.csv`, reporting national adoption rates for SFM policies (81.4%), dedicated legislation (84.3%), stakeholder platforms (64.0%), and wood traceability systems (43.2%).

### 5. Comprehensive "Data Quality & Diagnostics" Page
- **Column Type Audit:** Detailed counts of numeric vs categorical/text columns for all 9 project datasets.
- **Observation Status Flags Matrix:** Stacked bar chart and audit table breaking down Official Reported Data (`Flag A`), Imputed / Desk Studies (`Flag I`), Denominator Zero / Inapplicable (`Flag M`), and Unreported Missing Values (`Flag O`) across all milestone years.
- **Empirical Confidence Tiers:** Visualizes data confidence ratings from `Tiers_2026-10-16.csv` (High Tier = field NFI / wall-to-wall satellite mapping; Medium Tier = partial/regional surveys; Low Tier = desk study / model extrapolation).
- **Blanks & Nulls Integrity:** Explains why blanks are preserved as nulls and never falsely fabricated as zero.

### 6. Usability Enhancements
- **Global Filter Reset:** A dedicated button in the sidebar to reset all filters to global defaults with one click.
- **Filtered Data CSV Export:** Streamlit download button allowing export of custom period analysis.

---

## 📐 Formulas & Mathematical Definitions

1. **Absolute Forest Area Change:**
   $$\Delta \text{Area} = \text{Forest Area}_{\text{end\_year}} - \text{Forest Area}_{\text{start\_year}} \quad [1,000\text{ ha}]$$
   $$\Delta \text{Area}_{\text{Mha}} = \frac{\Delta \text{Area}}{1,000} \quad [\text{Million ha}]$$

2. **Relative Percentage Change:**
   $$\% \Delta = \left(\frac{\Delta \text{Area}}{\text{Forest Area}_{\text{start\_year}}}\right) \times 100 \quad [\%]$$
   *(Guard applied: Evaluated only when $\text{Forest Area}_{\text{start\_year}} > 0$; otherwise returns `NaN` to prevent division-by-zero).*

3. **Annualized Change Rate:**
   $$\text{Annual Rate} = \frac{\Delta \text{Area}_{\text{Mha}}}{\text{end\_year} - \text{start\_year}} \quad [\text{Million ha/year}]$$

4. **Forest Cover Percentage of Land Area:**
   $$\text{Forest Cover } \% = \left(\frac{\text{1a\_forestArea}}{\text{1a\_landArea}}\right) \times 100 \quad [\%]$$

5. **Structural Forest Component Shares:**
   $$\text{Natural Forest Share } \% = \left(\frac{\text{1b\_naturallyRegeneratingForest}}{\text{1a\_forestArea}}\right) \times 100$$
   $$\text{Planted Forest Share } \% = \left(\frac{\text{1b\_plantedForest}}{\text{1a\_forestArea}}\right) \times 100$$
   $$\text{Natural Forest Share } \% + \text{Planted Forest Share } \% \approx 100\%$$

---

## 📁 Files Modified in Stage 2

1. [**`data_loader.py`**](file:///c:/Users/user/Desktop/DV_LAB_Forest/data_loader.py):
   - Added `calculate_period_change()` with validation and paired country matching.
   - Added `get_top_gainers()` and `get_top_losers()`.
   - Added `get_top_countries_by_area()`.
   - Added `get_sustainability_metrics()` for natural vs planted and primary forests.
   - Added `get_flag_audit_report()` for observation flag tracking.
   - Added `get_tiers_report()` and `get_policy_adoption_report()`.
   - Updated `get_dataset_inventory()` with numeric and categorical column counts.
2. [**`visualizations.py`**](file:///c:/Users/user/Desktop/DV_LAB_Forest/visualizations.py):
   - Added `plot_top_gainers_chart()` and `plot_top_losers_chart()`.
   - Added `plot_top_countries_ranking()`.
   - Added `plot_enhanced_trend_line()` supporting multi-country comparison.
   - Added `plot_natural_vs_planted_bar()`.
   - Added `plot_forest_cover_percentage_ranking()`.
   - Added `plot_primary_forest_share()`.
   - Added `plot_flag_coverage_by_year()`.
   - Added `plot_tiers_summary()`.
3. [**`app.py`**](file:///c:/Users/user/Desktop/DV_LAB_Forest/app.py):
   - Added 7-tab navigation routing.
   - Integrated Stage 2 pages: *Forest Change Insights*, *Country Rankings & Comparisons*, *Multi-Country Trend Analysis*, *Forest Sustainability Indicators*, and *Data Quality & Diagnostics*.
   - Added filter reset button and CSV export feature.

---

## 🧪 Testing Performed & Verification Results

All tests were implemented in an automated test script (`test_stage2_full.py`) and verified against the live code:

| Test Case | Method | Result | Notes |
| :--- | :--- | :---: | :--- |
| **Invalid Year Selections** | Tested `start_year == end_year` and `start_year > end_year` | **PASSED** | Gracefully caught, returns `is_valid = False` with informative error message. |
| **Paired Matching Across All Years** | Tested all 15 pairwise milestone combinations ($1990 \dots 2025$) | **PASSED** | Over 200 countries evaluated per interval; zero crashes. |
| **Division by Zero Handling** | Injected synthetic $0.0$ starting forest area | **PASSED** | Returns `NaN` for percentage change; zero division error avoided. |
| **Sustainability Non-Overlapping Check** | Verified $\text{Natural} + \text{Planted} \approx \text{Total}$ | **PASSED** | Discrepancy $< 0.05\%$; hierarchy validated. |
| **Data Quality Inventory** | Verified row, column, numeric, and categorical counts | **PASSED** | All 9 datasets correctly audited with type breakdowns. |
| **Plotly Chart Generators** | Tested with both valid datasets and empty dataframes | **PASSED** | Clean fallback annotations rendered without crashing. |
| **Streamlit Server Health Check** | Checked HTTP response at `http://localhost:8501` | **PASSED** | Returned `HTTP 200 OK`. |

---

*Stage 2 implementation is complete, verified, and tested.*
