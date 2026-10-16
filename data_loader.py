"""
data_loader.py - Data ingestion, cleaning, and metric preparation module.
Reads and caches FAO Global Forest Resources Assessment (FRA) CSV datasets.
Preserves original data, standardizes numeric columns, and provides robust filtering.
"""

import os
import glob
import pandas as pd
import numpy as np
import streamlit as st

# Base directory for relative dataset paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Human-readable labels for FRA variables
FRA_VARIABLE_MAP = {
    '1a_forestArea': 'Total Forest Area (1,000 ha)',
    '1a_landArea': 'Total Land Area (1,000 ha)',
    '1a_otherWoodedLand': 'Other Wooded Land (1,000 ha)',
    '1b_naturallyRegeneratingForest': 'Naturally Regenerating Forest (1,000 ha)',
    '1b_plantedForest': 'Planted Forest (1,000 ha)',
    '1b_plantationForest': 'Plantation Forest (1,000 ha)',
    '1b_primary': 'Primary Forest (1,000 ha)',
    '2a_gs_tot_forest': 'Total Growing Stock in Forest (Million m³)',
    '2c_agb_total': 'Above-Ground Biomass Total (Million tonnes)',
    '2c_bgb_total': 'Below-Ground Biomass Total (Million tonnes)',
    '2d_carbon_agb_total': 'Carbon in Above-Ground Biomass (Million tonnes)',
    '3a_tot_biodiv': 'Forest Designated for Biodiversity (1,000 ha)',
    '3b_protected': 'Forest Area in Protected Areas (1,000 ha)',
    '3b_forMngt': 'Forest Area with Management Plan (1,000 ha)'
}

@st.cache_data(show_spinner=False)
def load_fra_years() -> pd.DataFrame:
    """
    Loads FRA_Years_2026-10-16.csv containing multi-variable time series for 1990-2025.
    Converts numeric indicators, drops redundant flags for main analytics, and standardizes columns.
    """
    filepath = os.path.join(BASE_DIR, "FRA_Years_2026-10-16.csv")
    if not os.path.exists(filepath):
        # Fallback to wildcard search if date stamp changes
        matches = glob.glob(os.path.join(BASE_DIR, "FRA_Years_*.csv")) or glob.glob(os.path.join(BASE_DIR, "FRA_years_*.csv"))
        if matches:
            filepath = matches[0]
        else:
            raise FileNotFoundError(f"Dataset not found at {filepath}")

    df = pd.read_csv(filepath, low_memory=False)
    
    # Ensure year is integer
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    
    # Clean numeric indicators
    for col in FRA_VARIABLE_MAP.keys():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    df = df.copy()
    # Calculate Forest Cover Percentage if both land area and forest area exist
    if '1a_forestArea' in df.columns and '1a_landArea' in df.columns:
        df['forest_cover_pct'] = np.where(
            df['1a_landArea'] > 0,
            (df['1a_forestArea'] / df['1a_landArea']) * 100,
            np.nan
        )
        
    return df

@st.cache_data(show_spinner=False)
def load_intervals() -> pd.DataFrame:
    """
    Loads Intervals_2026-10-16.csv containing average annual rates:
    expansion, afforestation, natural expansion, deforestation.
    """
    filepath = os.path.join(BASE_DIR, "Intervals_2026-10-16.csv")
    if not os.path.exists(filepath):
        matches = glob.glob(os.path.join(BASE_DIR, "Intervals_*.csv"))
        filepath = matches[0] if matches else None

    if not filepath or not os.path.exists(filepath):
        return pd.DataFrame()

    df = pd.read_csv(filepath, low_memory=False)
    for col in ['1d_expansion', '1d_afforestation', '1d_nat_exp', '1d_deforestation']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

@st.cache_data(show_spinner=False)
def load_annual_disturbances() -> pd.DataFrame:
    """
    Loads Annual_2026-10-16.csv containing forest disturbances by year (2000-2023):
    insects, diseases, weather, fire, and others.
    """
    filepath = os.path.join(BASE_DIR, "Annual_2026-10-16.csv")
    if not os.path.exists(filepath):
        matches = glob.glob(os.path.join(BASE_DIR, "Annual_*.csv"))
        filepath = matches[0] if matches else None

    if not filepath or not os.path.exists(filepath):
        return pd.DataFrame()

    df = pd.read_csv(filepath, low_memory=False)
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    dist_cols = ['5a_insect', '5a_diseases', '5a_weather', '5a_other', '5b_fire_forest', '5b_fire_land']
    for col in dist_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

@st.cache_data(show_spinner=False)
def load_forest_policy() -> pd.DataFrame:
    """Loads ForestPolicy_2026-10-16.csv."""
    filepath = os.path.join(BASE_DIR, "ForestPolicy_2026-10-16.csv")
    if os.path.exists(filepath):
        return pd.read_csv(filepath, low_memory=False)
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_degraded_forest() -> pd.DataFrame:
    """Loads DegradedForest_2026-10-16.csv."""
    filepath = os.path.join(BASE_DIR, "DegradedForest_2026-10-16.csv")
    if os.path.exists(filepath):
        df = pd.read_csv(filepath, low_memory=False)
        if 'Degraded forest area' in df.columns:
            df['degraded_area_num'] = pd.to_numeric(df['Degraded forest area'], errors='coerce')
        return df
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_forest_restoration() -> pd.DataFrame:
    """Loads ForestRestoration_2026-10-16.csv."""
    filepath = os.path.join(BASE_DIR, "ForestRestoration_2026-10-16.csv")
    if os.path.exists(filepath):
        return pd.read_csv(filepath, low_memory=False)
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_nwfp() -> pd.DataFrame:
    """Loads NWFP_2026-10-16.csv."""
    filepath = os.path.join(BASE_DIR, "NWFP_2026-10-16.csv")
    if os.path.exists(filepath):
        return pd.read_csv(filepath, low_memory=False)
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_tiers() -> pd.DataFrame:
    """Loads Tiers_2026-10-16.csv."""
    filepath = os.path.join(BASE_DIR, "Tiers_2026-10-16.csv")
    if os.path.exists(filepath):
        return pd.read_csv(filepath, low_memory=False)
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_ndp() -> pd.DataFrame:
    """Loads NDPYear_2026-10-16.csv."""
    filepath = os.path.join(BASE_DIR, "NDPYear_2026-10-16.csv")
    if os.path.exists(filepath):
        return pd.read_csv(filepath, low_memory=False)
    return pd.DataFrame()

def filter_fra_data(df: pd.DataFrame, 
                    selected_regions: list = None, 
                    selected_countries: list = None,
                    selected_years: list = None) -> pd.DataFrame:
    """
    Filters the FRA years dataframe according to user selections.
    """
    filtered = df.copy()
    
    if selected_regions and "All Regions" not in selected_regions:
        filtered = filtered[filtered['regions'].isin(selected_regions)]
        
    if selected_countries and "All Countries" not in selected_countries:
        filtered = filtered[filtered['name'].isin(selected_countries)]
        
    if selected_years:
        filtered = filtered[filtered['year'].isin(selected_years)]
        
    return filtered

def calculate_kpis(df_fra: pd.DataFrame, 
                   selected_year: int = 2025, 
                   baseline_year: int = 1990,
                   selected_regions: list = None, 
                   selected_countries: list = None) -> dict:
    """
    Computes real, data-driven KPI metrics for selected filter criteria:
    - Number of countries/regions covered
    - Number of reporting years covered
    - Total forest area (in Million ha)
    - Net forest area change & % change since baseline
    - Reliable verification flag
    """
    kpis = {
        'countries_count': 0,
        'regions_count': 0,
        'years_count': 0,
        'total_forest_area_mha': None,
        'forest_area_display': "Not available",
        'net_change_mha': None,
        'pct_change': None,
        'change_display': "Not available",
        'change_subtext': "",
        'trend_positive': True,
        'is_reliable': False
    }
    
    if df_fra.empty:
        return kpis

    # Apply geographic filtering (without restricting years yet)
    geo_df = df_fra.copy()
    if selected_regions and "All Regions" not in selected_regions:
        geo_df = geo_df[geo_df['regions'].isin(selected_regions)]
    if selected_countries and "All Countries" not in selected_countries:
        geo_df = geo_df[geo_df['name'].isin(selected_countries)]
        
    kpis['countries_count'] = int(geo_df['name'].nunique())
    kpis['regions_count'] = int(geo_df['regions'].dropna().nunique())
    
    available_years = sorted(geo_df['year'].dropna().unique().tolist())
    kpis['years_count'] = len(available_years)
    
    # 1. Total Forest Area for selected_year
    target_data = geo_df[geo_df['year'] == selected_year]
    if not target_data.empty and '1a_forestArea' in target_data.columns:
        valid_area = target_data['1a_forestArea'].dropna()
        if len(valid_area) > 0:
            # 1a_forestArea is in 1,000 ha -> divide by 1,000 for Million ha
            total_1000ha = valid_area.sum()
            total_mha = total_1000ha / 1000.0
            kpis['total_forest_area_mha'] = total_mha
            if total_mha >= 1000:
                kpis['forest_area_display'] = f"{total_mha / 1000.0:.2f} B ha"
            else:
                kpis['forest_area_display'] = f"{total_mha:,.1f} M ha"
            kpis['is_reliable'] = True

    # 2. Forest-Area Change between baseline_year and selected_year
    baseline_data = geo_df[geo_df['year'] == baseline_year]
    if not target_data.empty and not baseline_data.empty:
        # Match by country to ensure valid pair comparison
        m = pd.merge(
            baseline_data[['name', '1a_forestArea']].rename(columns={'1a_forestArea': 'base_area'}),
            target_data[['name', '1a_forestArea']].rename(columns={'1a_forestArea': 'target_area'}),
            on='name'
        ).dropna()
        
        if len(m) > 0:
            sum_base = m['base_area'].sum()
            sum_target = m['target_area'].sum()
            if sum_base > 0:
                net_diff_1000ha = sum_target - sum_base
                net_diff_mha = net_diff_1000ha / 1000.0
                pct = (net_diff_1000ha / sum_base) * 100.0
                kpis['net_change_mha'] = net_diff_mha
                kpis['pct_change'] = pct
                
                sign = "+" if net_diff_mha > 0 else ""
                kpis['change_display'] = f"{sign}{net_diff_mha:,.1f} M ha"
                kpis['change_subtext'] = f"{sign}{pct:.2f}% since {baseline_year}"
                kpis['trend_positive'] = net_diff_mha >= 0

    return kpis

@st.cache_data(show_spinner=False)
def get_dataset_inventory() -> pd.DataFrame:
    """
    Scans the project directory and generates an audited inventory table:
    - Available datasets
    - Row and column counts
    - Key columns
    - Missing value percentage & counts
    - Duplicate row counts
    - Functional category
    - Reliability / Notes
    """
    records = []
    
    dataset_metadata = [
        {
            'filename': 'FRA_Years_2026-10-16.csv',
            'category': 'Forest Area & Core Variables',
            'description': 'Reporting years (1990-2025) across 236 countries. Contains forest area, land area, biomass, carbon, growing stock, ownership.',
            'notes': 'Official FAO FRA multi-year compilation. Area in 1,000 ha. Flags in column IA.'
        },
        {
            'filename': 'Intervals_2026-10-16.csv',
            'category': 'Forest Change Dynamics',
            'description': 'Interval periods (1990-2000 to 2020-2025). Annual averages for expansion, afforestation, natural expansion, deforestation.',
            'notes': 'Rates expressed in 1,000 ha/year. Flags in column Q.'
        },
        {
            'filename': 'Annual_2026-10-16.csv',
            'category': 'Forest Disturbances',
            'description': 'Annual series (2000-2023). Area affected by fire, insects, diseases, extreme weather, and other disturbances.',
            'notes': 'Area in 1,000 ha. Burned land vs burned forest separate columns.'
        },
        {
            'filename': 'DegradedForest_2026-10-16.csv',
            'category': 'Degraded Forests',
            'description': 'Qualitative and semi-quantitative country reporting on forest degradation definitions, monitoring systems, and criteria.',
            'notes': 'Self-reported by national authorities. Some free-text comments in French/Spanish.'
        },
        {
            'filename': 'ForestRestoration_2026-10-16.csv',
            'category': 'Forest Restoration',
            'description': 'National restoration commitments, legal mandates, target areas, and hectares restored to date.',
            'notes': 'Significant qualitative responses; quantitative targets available for select nations.'
        },
        {
            'filename': 'ForestPolicy_2026-10-16.csv',
            'category': 'Forest Governance & Policy',
            'description': 'National/subnational policies supporting Sustainable Forest Management (SFM), legislation, stakeholder platforms, traceability.',
            'notes': 'Categorical indicators (yes/no) + policy descriptions in national languages.'
        },
        {
            'filename': 'NWFP_2026-10-16.csv',
            'category': 'Non-Wood Forest Products',
            'description': 'Top 10 reported Non-Wood Forest Products per country with quantity, economic value, category, and currency.',
            'notes': 'Values recorded in local currency. Wide variation in reporting completeness.'
        },
        {
            'filename': 'NDPYear_2026-10-16.csv',
            'category': 'National Data Points & Methods',
            'description': 'Earliest and latest national inventory data points and measurement methodologies (NFI, remote sensing, maps).',
            'notes': 'Documents scientific methodology backing each countrys FRA submission.'
        },
        {
            'filename': 'Tiers_2026-10-16.csv',
            'category': 'Data Quality & Tiers',
            'description': 'Data confidence ratings (Tier 1: low, Tier 2: medium, Tier 3: high) for status and trend of forest area, growing stock, biomass.',
            'notes': 'Indicates empirical strength: high = field inventory/satellite; low = desk study.'
        }
    ]
    
    for item in dataset_metadata:
        fpath = os.path.join(BASE_DIR, item['filename'])
        if os.path.exists(fpath):
            try:
                df = pd.read_csv(fpath, low_memory=False)
                rows, cols = df.shape
                dup_count = int(df.duplicated().sum())
                total_cells = df.size
                missing_count = int(df.isna().sum().sum())
                missing_pct = (missing_count / total_cells * 100) if total_cells > 0 else 0.0
                
                num_cols_count = int(len(df.select_dtypes(include=[np.number]).columns))
                cat_cols_count = int(cols - num_cols_count)

                # Representative columns (excluding flags)
                non_flag_cols = [c for c in df.columns if not c.endswith('_flag') and c != 'Flag']
                key_cols = ", ".join(non_flag_cols[:6])
                if len(non_flag_cols) > 6:
                    key_cols += f", ... (+{len(non_flag_cols)-6} more)"
                
                records.append({
                    'Dataset': item['filename'],
                    'Category': item['category'],
                    'Rows': rows,
                    'Columns': cols,
                    'Numeric Cols': num_cols_count,
                    'Text/Cat Cols': cat_cols_count,
                    'Duplicates': dup_count,
                    'Missing Cells': f"{missing_count:,} ({missing_pct:.1f}%)",
                    'Key Columns': key_cols,
                    'Scope & Notes': item['notes']
                })
            except Exception as e:
                records.append({
                    'Dataset': item['filename'],
                    'Category': item['category'],
                    'Rows': 'Error',
                    'Columns': 'Error',
                    'Duplicates': 'Error',
                    'Missing Cells': str(e),
                    'Key Columns': '-',
                    'Scope & Notes': 'Could not read file'
                })
        else:
            records.append({
                'Dataset': item['filename'],
                'Category': item['category'],
                'Rows': 'Missing',
                'Columns': 'Missing',
                'Duplicates': '-',
                'Missing Cells': '-',
                'Key Columns': '-',
                'Scope & Notes': 'File not found on disk'
            })
            
    return pd.DataFrame(records)

@st.cache_data(show_spinner=False)
def load_raw_dataset(filename: str) -> pd.DataFrame:
    """Loads any dataset by filename for interactive dataset inspection."""
    filepath = os.path.join(BASE_DIR, filename)
    if os.path.exists(filepath):
        return pd.read_csv(filepath, low_memory=False)
    return pd.DataFrame()


def calculate_period_change(df_fra: pd.DataFrame, 
                            start_year: int, 
                            end_year: int, 
                            selected_regions: list = None, 
                            selected_countries: list = None) -> tuple:
    """
    Computes rigorous forest-area change between any two valid FRA reporting years.
    Returns:
    - change_df (pd.DataFrame): country-level paired change records
    - summary_stats (dict): global or filtered period metrics
    
    Formula:
    1. Absolute Change (1,000 ha) = Forest_Area[end_year] - Forest_Area[start_year]
    2. Absolute Change (M ha) = Absolute Change (1,000 ha) / 1,000
    3. Percentage Change (%) = (Absolute Change / Forest_Area[start_year]) * 100, if start_area > 0
    4. Annual Rate (1,000 ha/yr) = Absolute Change / (end_year - start_year)
    """
    summary = {
        'start_year': start_year,
        'end_year': end_year,
        'years_diff': end_year - start_year,
        'is_valid': True,
        'error_msg': "",
        'countries_evaluated': 0,
        'total_start_mha': 0.0,
        'total_end_mha': 0.0,
        'net_change_mha': 0.0,
        'pct_change': 0.0,
        'annual_rate_mha': 0.0,
        'gainers_count': 0,
        'losers_count': 0,
        'stable_count': 0
    }
    
    if start_year >= end_year:
        summary['is_valid'] = False
        summary['error_msg'] = f"Ending year ({end_year}) must be strictly greater than starting year ({start_year})."
        return pd.DataFrame(), summary
        
    if df_fra.empty or '1a_forestArea' not in df_fra.columns:
        summary['is_valid'] = False
        summary['error_msg'] = "Core forest area dataset is empty or missing '1a_forestArea'."
        return pd.DataFrame(), summary

    # Apply geographic filtering
    sub = df_fra.copy()
    if selected_regions and "All Regions" not in selected_regions:
        sub = sub[sub['regions'].isin(selected_regions)]
    if selected_countries and "All Countries" not in selected_countries:
        sub = sub[sub['name'].isin(selected_countries)]

    # Extract paired start and end records for countries that reported both
    start_df = sub[sub['year'] == start_year][['name', 'regions', 'iso3', '1a_forestArea']].rename(
        columns={'1a_forestArea': 'start_area_1000ha'}
    )
    end_df = sub[sub['year'] == end_year][['name', '1a_forestArea']].rename(
        columns={'1a_forestArea': 'end_area_1000ha'}
    )

    merged = pd.merge(start_df, end_df, on='name')
    # Filter out records where either start or end is NaN (never fabricate zero for missing values!)
    merged = merged.dropna(subset=['start_area_1000ha', 'end_area_1000ha']).copy()

    if merged.empty:
        summary['is_valid'] = False
        summary['error_msg'] = f"No countries found with reported forest area in both {start_year} and {end_year}."
        return pd.DataFrame(), summary

    # Calculate metrics
    merged['start_area_mha'] = merged['start_area_1000ha'] / 1000.0
    merged['end_area_mha'] = merged['end_area_1000ha'] / 1000.0
    merged['abs_change_1000ha'] = merged['end_area_1000ha'] - merged['start_area_1000ha']
    merged['abs_change_mha'] = merged['abs_change_1000ha'] / 1000.0
    
    diff_years = max(1, end_year - start_year)
    merged['annual_rate_mha'] = merged['abs_change_mha'] / diff_years
    
    # Percentage change formula: (abs_change / start_area) * 100
    # Guard against division by zero if start_area == 0
    merged['pct_change'] = np.where(
        merged['start_area_1000ha'] > 0,
        (merged['abs_change_1000ha'] / merged['start_area_1000ha']) * 100.0,
        np.nan
    )
    
    # Direction categorization
    def categorize_change(val):
        if val > 0.05:
            return "Increase"
        elif val < -0.05:
            return "Decrease"
        else:
            return "Stable"
            
    merged['direction'] = merged['abs_change_mha'].apply(categorize_change)

    # Compute aggregate summary
    sum_start_1000ha = merged['start_area_1000ha'].sum()
    sum_end_1000ha = merged['end_area_1000ha'].sum()
    net_1000ha = sum_end_1000ha - sum_start_1000ha

    summary['countries_evaluated'] = len(merged)
    summary['total_start_mha'] = sum_start_1000ha / 1000.0
    summary['total_end_mha'] = sum_end_1000ha / 1000.0
    summary['net_change_mha'] = net_1000ha / 1000.0
    summary['annual_rate_mha'] = (net_1000ha / 1000.0) / diff_years
    if sum_start_1000ha > 0:
        summary['pct_change'] = (net_1000ha / sum_start_1000ha) * 100.0
    else:
        summary['pct_change'] = 0.0

    summary['gainers_count'] = int((merged['direction'] == "Increase").sum())
    summary['losers_count'] = int((merged['direction'] == "Decrease").sum())
    summary['stable_count'] = int((merged['direction'] == "Stable").sum())

    return merged, summary


def get_top_gainers(change_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Returns top N countries with highest forest area increase."""
    if change_df.empty or 'abs_change_mha' not in change_df.columns:
        return pd.DataFrame()
    gainers = change_df[change_df['abs_change_mha'] > 0].copy()
    return gainers.sort_values(by='abs_change_mha', ascending=False).head(n)


def get_top_losers(change_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Returns top N countries with highest forest area decrease (sorted most negative first)."""
    if change_df.empty or 'abs_change_mha' not in change_df.columns:
        return pd.DataFrame()
    losers = change_df[change_df['abs_change_mha'] < 0].copy()
    return losers.sort_values(by='abs_change_mha', ascending=True).head(n)


def get_top_countries_by_area(df_fra: pd.DataFrame, year: int = 2025, n: int = 10, selected_regions: list = None) -> pd.DataFrame:
    """Returns top N countries by forest area in a specific year with global/regional share."""
    if df_fra.empty or '1a_forestArea' not in df_fra.columns:
        return pd.DataFrame()
    sub = df_fra[df_fra['year'] == year].copy()
    if selected_regions and "All Regions" not in selected_regions:
        sub = sub[sub['regions'].isin(selected_regions)]
    sub = sub.dropna(subset=['1a_forestArea']).copy()
    total_area = sub['1a_forestArea'].sum()
    sub['forest_area_mha'] = sub['1a_forestArea'] / 1000.0
    sub['share_of_total_pct'] = (sub['1a_forestArea'] / total_area * 100.0) if total_area > 0 else 0.0
    return sub.sort_values(by='forest_area_mha', ascending=False).head(n)


def get_sustainability_metrics(df_fra: pd.DataFrame, year: int = 2025, selected_regions: list = None, selected_countries: list = None) -> pd.DataFrame:
    """
    Computes sustainability indicators:
    - Forest Cover % of Land Area
    - Naturally Regenerating Forest vs Planted Forest components
    - Primary Forest Extent and its share of Natural Forest
    - Protected Area Extent and its share of Total Forest Area
    Avoids double counting: Planted + Naturally Regenerating ≈ Total Forest Area.
    Primary forest is a non-overlapping subset of naturally regenerating forest.
    """
    if df_fra.empty:
        return pd.DataFrame()
    data = df_fra[df_fra['year'] == year].copy()
    if selected_regions and "All Regions" not in selected_regions:
        data = data[data['regions'].isin(selected_regions)]
    if selected_countries and "All Countries" not in selected_countries:
        data = data[data['name'].isin(selected_countries)]
        
    res = pd.DataFrame()
    res['name'] = data['name']
    res['regions'] = data['regions']
    res['iso3'] = data['iso3']
    
    # 1. Forest Area & Land Area
    res['forest_area_mha'] = data['1a_forestArea'] / 1000.0
    res['land_area_mha'] = data['1a_landArea'] / 1000.0
    res['forest_cover_pct'] = np.where(
        data['1a_landArea'] > 0,
        (data['1a_forestArea'] / data['1a_landArea']) * 100.0,
        np.nan
    )
    
    # 2. Naturally Regenerating vs Planted Forest
    res['natural_forest_mha'] = data['1b_naturallyRegeneratingForest'] / 1000.0
    res['planted_forest_mha'] = data['1b_plantedForest'] / 1000.0
    res['natural_share_pct'] = np.where(
        data['1a_forestArea'] > 0,
        (data['1b_naturallyRegeneratingForest'] / data['1a_forestArea']) * 100.0,
        np.nan
    )
    res['planted_share_pct'] = np.where(
        data['1a_forestArea'] > 0,
        (data['1b_plantedForest'] / data['1a_forestArea']) * 100.0,
        np.nan
    )
    
    # 3. Primary Forest (intact old-growth ecosystem subset)
    res['primary_forest_mha'] = data['1b_primary'] / 1000.0
    res['primary_share_pct'] = np.where(
        data['1a_forestArea'] > 0,
        (data['1b_primary'] / data['1a_forestArea']) * 100.0,
        np.nan
    )
    
    # 4. Protected Forest Area
    if '3b_protected' in data.columns:
        res['protected_forest_mha'] = data['3b_protected'] / 1000.0
        res['protected_share_pct'] = np.where(
            data['1a_forestArea'] > 0,
            (data['3b_protected'] / data['1a_forestArea']) * 100.0,
            np.nan
        )
        
    return res


@st.cache_data(show_spinner=False)
def get_flag_audit_report(df_fra: pd.DataFrame) -> pd.DataFrame:
    """
    Audits observation-status flags for key variables across FRA milestone years.
    Categorizes:
    - A: Official Reported Data
    - I: Imputed / Desk Study
    - M: Missing (Denominator zero / impossible)
    - O: Missing (Unreported)
    """
    records = []
    key_flag_cols = [
        ('1a_forestArea_flag', 'Total Forest Area'),
        ('1a_landArea_flag', 'Total Land Area'),
        ('1b_naturallyRegeneratingForest_flag', 'Naturally Regenerating Forest'),
        ('1b_primary_flag', 'Primary Forest'),
        ('2a_gs_tot_forest_flag', 'Growing Stock'),
        ('2c_agb_total_flag', 'Above-Ground Biomass')
    ]
    
    years = sorted(df_fra['year'].dropna().unique())
    for col_flag, var_name in key_flag_cols:
        if col_flag in df_fra.columns:
            for yr in years:
                sub = df_fra[df_fra['year'] == yr]
                total = len(sub)
                flags = sub[col_flag].fillna('O').str.strip().str.upper()
                count_a = int((flags == 'A').sum())
                count_i = int((flags == 'I').sum())
                count_m = int((flags == 'M').sum())
                count_o = int((flags == 'O').sum())
                records.append({
                    'Variable': var_name,
                    'Year': int(yr),
                    'Total Countries': total,
                    'Official Reported (A)': count_a,
                    'Imputed/Desk (I)': count_i,
                    'Cannot Exist (M)': count_m,
                    'Unreported (O)': count_o,
                    'Official Share (%)': round(count_a / total * 100.0, 1) if total > 0 else 0.0
                })
    return pd.DataFrame(records)


@st.cache_data(show_spinner=False)
def get_tiers_report() -> pd.DataFrame:
    """
    Loads Tiers_2026-10-16.csv and calculates distribution of data confidence ratings.
    Ratings: High (Tier 3), Medium (Tier 2), Low (Tier 1).
    """
    tiers_df = load_tiers()
    if tiers_df.empty:
        return pd.DataFrame()
        
    records = []
    tier_cols = [
        ('1a_status', 'Forest Area Status'),
        ('1a_trend', 'Forest Area Trend'),
        ('2a_status', 'Growing Stock Status'),
        ('2c_status', 'Biomass Status')
    ]
    for col, label in tier_cols:
        if col in tiers_df.columns:
            s = tiers_df[col].dropna().str.lower().str.strip()
            total = len(tiers_df)
            high = int((s == 'high').sum())
            med = int((s == 'medium').sum())
            low = int((s == 'low').sum())
            unreported = total - (high + med + low)
            records.append({
                'Indicator': label,
                'High Tier (Satellite/NFI)': high,
                'Medium Tier (Regional/Partial)': med,
                'Low Tier (Desk/Model)': low,
                'Not Reported': unreported,
                'High Tier %': round(high / total * 100.0, 1)
            })
    return pd.DataFrame(records)


@st.cache_data(show_spinner=False)
def get_policy_adoption_report() -> pd.DataFrame:
    """
    Summarizes global and regional Sustainable Forest Management (SFM) policy adoption from ForestPolicy_2026-10-16.csv.
    """
    pol_df = load_forest_policy()
    if pol_df.empty:
        return pd.DataFrame()
        
    records = []
    indicators = [
        ('National policies supporting SFM', 'National SFM Policy'),
        ('National legislations supporting SFM', 'National SFM Legislation'),
        ('National platform for stakeholder participation', 'Stakeholder Platform'),
        ('National existence of traceability system', 'Wood Traceability System')
    ]
    
    total_countries = len(pol_df)
    for col, name in indicators:
        if col in pol_df.columns:
            yes_count = int((pol_df[col].dropna().str.lower() == 'yes').sum())
            records.append({
                'Policy Instrument': name,
                'Countries Adopted': yes_count,
                'Total Evaluated': total_countries,
                'Adoption Rate (%)': round(yes_count / total_countries * 100.0, 1)
            })
    return pd.DataFrame(records)


# ==============================================================================
# STAGE 3: DISTURBANCE, DEGRADATION & RESTORATION MODULES
# ==============================================================================

DISTURBANCE_INDICATORS_MAP = {
    '5b_fire_forest': 'Burned Forest Area',
    '5a_insect': 'Insect Disturbances',
    '5a_weather': 'Extreme Weather Disturbances',
    '5a_diseases': 'Forest Disease Disturbances',
    '5a_other': 'Other Disturbances',
    '5b_fire_land': 'Total Burned Land'
}


def get_disturbance_time_series(df_ann: pd.DataFrame, 
                                selected_regions: list = None, 
                                selected_countries: list = None) -> pd.DataFrame:
    """
    Computes annual disturbance time series (2000-2023) in Million hectares (M ha).
    Aggregates only reported observations without treating missing values as zero.
    """
    if df_ann.empty:
        return pd.DataFrame()
        
    sub = df_ann.copy()
    if selected_regions and "All Regions" not in selected_regions:
        sub = sub[sub['regions'].isin(selected_regions)]
    if selected_countries and "All Countries" not in selected_countries:
        sub = sub[sub['name'].isin(selected_countries)]
        
    dist_cols = ['5b_fire_forest', '5a_insect', '5a_weather', '5a_diseases', '5a_other', '5b_fire_land']
    valid_cols = [c for c in dist_cols if c in sub.columns]
    
    # Group by year and sum reported values
    grouped = sub.groupby('year')[valid_cols].sum(min_count=1).reset_index()
    grouped = grouped.dropna(subset=['year']).sort_values(by='year')
    
    # Scale from 1,000 ha to Million ha
    for c in valid_cols:
        grouped[c + '_mha'] = grouped[c] / 1000.0
        
    # Also calculate total biotic/abiotic disturbance excluding double-counted land fire
    core_disturbances = [c for c in ['5b_fire_forest', '5a_insect', '5a_weather', '5a_diseases', '5a_other'] if c in valid_cols]
    grouped['total_forest_disturbance_mha'] = grouped[[c + '_mha' for c in core_disturbances]].sum(axis=1, min_count=1)
    
    return grouped


def get_top_disturbance_countries(df_ann: pd.DataFrame, 
                                  indicator: str = '5b_fire_forest', 
                                  year: int = None, 
                                  n: int = 10, 
                                  selected_regions: list = None) -> pd.DataFrame:
    """
    Ranks top N countries for a selected disturbance indicator.
    If year is None or 'All Years', computes cumulative disturbance over 2000-2023.
    """
    if df_ann.empty or indicator not in df_ann.columns:
        return pd.DataFrame()
        
    sub = df_ann.copy()
    if selected_regions and "All Regions" not in selected_regions:
        sub = sub[sub['regions'].isin(selected_regions)]
        
    if year is not None and str(year) != "All Years 2000-2023":
        sub = sub[sub['year'] == int(year)]
        
    # Aggregate by country
    agg_df = sub.groupby(['name', 'regions'])[indicator].sum(min_count=1).reset_index()
    agg_df = agg_df.dropna(subset=[indicator])
    agg_df = agg_df[agg_df[indicator] > 0].copy()
    agg_df['disturbance_mha'] = agg_df[indicator] / 1000.0
    
    return agg_df.sort_values(by='disturbance_mha', ascending=False).head(n)


def get_disturbance_kpis(df_ann: pd.DataFrame, 
                         selected_year: int = None, 
                         selected_regions: list = None, 
                         selected_countries: list = None) -> dict:
    """
    Computes summary KPI metrics for disturbance data.
    """
    kpis = {
        'total_fire_mha': 0.0,
        'total_insect_mha': 0.0,
        'total_weather_mha': 0.0,
        'total_disease_mha': 0.0,
        'total_other_mha': 0.0,
        'reporting_countries': 0,
        'is_available': False
    }
    
    if df_ann.empty:
        return kpis
        
    sub = df_ann.copy()
    if selected_regions and "All Regions" not in selected_regions:
        sub = sub[sub['regions'].isin(selected_regions)]
    if selected_countries and "All Countries" not in selected_countries:
        sub = sub[sub['name'].isin(selected_countries)]
        
    if selected_year is not None and str(selected_year) != "All Years 2000-2023":
        sub = sub[sub['year'] == int(selected_year)]
        
    dist_cols = ['5b_fire_forest', '5a_insect', '5a_weather', '5a_diseases', '5a_other']
    has_data = False
    
    if '5b_fire_forest' in sub.columns and sub['5b_fire_forest'].notna().sum() > 0:
        kpis['total_fire_mha'] = float(sub['5b_fire_forest'].sum()) / 1000.0
        has_data = True
    if '5a_insect' in sub.columns and sub['5a_insect'].notna().sum() > 0:
        kpis['total_insect_mha'] = float(sub['5a_insect'].sum()) / 1000.0
        has_data = True
    if '5a_weather' in sub.columns and sub['5a_weather'].notna().sum() > 0:
        kpis['total_weather_mha'] = float(sub['5a_weather'].sum()) / 1000.0
        has_data = True
    if '5a_diseases' in sub.columns and sub['5a_diseases'].notna().sum() > 0:
        kpis['total_disease_mha'] = float(sub['5a_diseases'].sum()) / 1000.0
        has_data = True
    if '5a_other' in sub.columns and sub['5a_other'].notna().sum() > 0:
        kpis['total_other_mha'] = float(sub['5a_other'].sum()) / 1000.0
        has_data = True
        
    # Count of distinct countries reporting at least one non-null disturbance
    active_mask = sub[dist_cols].notna().any(axis=1)
    kpis['reporting_countries'] = int(sub[active_mask]['name'].nunique())
    kpis['is_available'] = has_data
    
    return kpis


def get_degradation_profile(df_deg: pd.DataFrame, 
                            selected_regions: list = None, 
                            selected_countries: list = None) -> dict:
    """
    Extracts structured breakdown of forest degradation monitoring and qualitative definitions.
    Strictly preserves qualitative descriptions without converting text to invented numeric scores.
    """
    if df_deg.empty:
        return {}
        
    sub = df_deg.copy()
    if selected_regions and "All Regions" not in selected_regions:
        sub = sub[sub['regions'].isin(selected_regions)]
    if selected_countries and "All Countries" not in selected_countries:
        sub = sub[sub['name'].isin(selected_countries)]
        
    # Definition counts
    def_s = sub['Has your country nat. definition of degradation'].fillna('unreported').str.lower().str.strip()
    def_counts = {
        'Yes': int((def_s == 'yes').sum()),
        'No': int((def_s == 'no').sum()),
        'Unreported': int((def_s == 'unreported').sum())
    }
    
    # Monitoring counts
    mon_s = sub['Does your country monitor degradation'].fillna('unreported').str.lower().str.strip()
    mon_counts = {
        'Yes': int((mon_s == 'yes').sum()),
        'No': int((mon_s == 'no').sum()),
        'Unreported': int((mon_s == 'unreported').sum())
    }
    
    # Scale counts
    scale_s = sub['Monitoring scale'].fillna('unreported').str.strip()
    scale_counts = scale_s.value_counts().to_dict()
    
    # Monitoring methods applied frequency
    methods_list = []
    for m in sub['Main methods applied'].dropna():
        parts = [p.strip() for p in str(m).split(',') if p.strip()]
        methods_list.extend(parts)
        
    method_df = pd.Series(methods_list).value_counts().reset_index()
    method_df.columns = ['Method', 'Count']
    
    # Country table with usable information
    usable_cols = [
        'name', 'regions', 'Has your country nat. definition of degradation',
        'Does your country monitor degradation', 'Monitoring scale',
        'year of latest assessment', 'Degraded forest area', 'Criteria applied', 'What is the national definition'
    ]
    avail_cols = [c for c in usable_cols if c in sub.columns]
    table = sub[avail_cols].copy().rename(columns={
        'name': 'Country',
        'regions': 'Region',
        'Has your country nat. definition of degradation': 'National Definition',
        'Does your country monitor degradation': 'Monitors Degradation',
        'Monitoring scale': 'Monitoring Scale',
        'year of latest assessment': 'Latest Assessment Year',
        'Degraded forest area': 'Degraded Forest Area (Reported)',
        'Criteria applied': 'Criteria Applied',
        'What is the national definition': 'National Definition Text'
    })
    
    deg_area_num = pd.to_numeric(sub['Degraded forest area'], errors='coerce')
    numeric_count = int(deg_area_num.notna().sum())
    
    return {
        'total_evaluated': len(sub),
        'definition_counts': def_counts,
        'monitoring_counts': mon_counts,
        'scale_counts': scale_counts,
        'methods_df': method_df,
        'numeric_area_reported_count': numeric_count,
        'country_table': table
    }


def get_restoration_profile(df_rest: pd.DataFrame, 
                            selected_regions: list = None, 
                            selected_countries: list = None) -> dict:
    """
    Extracts restoration commitments and regional distributions.
    Clearly distinguishes reported political commitments from measured biophysical outcomes.
    """
    if df_rest.empty:
        return {}
        
    sub = df_rest.copy()
    if selected_regions and "All Regions" not in selected_regions:
        sub = sub[sub['regions'].isin(selected_regions)]
    if selected_countries and "All Countries" not in selected_countries:
        sub = sub[sub['name'].isin(selected_countries)]
        
    comm_s = sub['restoration commitments'].fillna('unreported').str.lower().str.strip()
    comm_counts = {
        'Yes': int((comm_s == 'yes').sum()),
        'No': int((comm_s == 'no').sum()),
        'Unreported': int((comm_s == 'unreported').sum())
    }
    
    # Commitments by region
    reg_comm = sub.groupby(['regions', comm_s]).size().unstack(fill_value=0)
    
    # Target and law counts
    mandates_count = int(sub['Law mandate'].dropna().str.strip().ne('').sum()) if 'Law mandate' in sub.columns else 0
    targets_count = int(sub['restoration targets'].dropna().str.strip().ne('').sum()) if 'restoration targets' in sub.columns else 0
    restored_reported_count = int(sub['ha restored to date'].dropna().str.strip().ne('').sum()) if 'ha restored to date' in sub.columns else 0
    
    usable_cols = [
        'name', 'regions', 'restoration commitments', 'Law mandate', 
        'National definition', 'areas in need of restoration', 
        'restoration targets', 'ha restored to date'
    ]
    avail_cols = [c for c in usable_cols if c in sub.columns]
    table = sub[avail_cols].copy().rename(columns={
        'name': 'Country',
        'regions': 'Region',
        'restoration commitments': 'Restoration Commitment',
        'Law mandate': 'Legal Mandate',
        'National definition': 'National Definition',
        'areas in need of restoration': 'Areas in Need of Restoration',
        'restoration targets': 'Restoration Targets',
        'ha restored to date': 'Hectares Restored to Date'
    })
    
    return {
        'total_evaluated': len(sub),
        'commitments_counts': comm_counts,
        'regional_commitments': reg_comm,
        'mandates_count': mandates_count,
        'targets_count': targets_count,
        'restored_reported_count': restored_reported_count,
        'country_table': table
    }


def get_cross_topic_synthesis(df_fra: pd.DataFrame, 
                             df_ann: pd.DataFrame, 
                             df_deg: pd.DataFrame, 
                             df_rest: pd.DataFrame, 
                             df_pol: pd.DataFrame, 
                             start_year: int = 1990, 
                             end_year: int = 2025,
                             selected_regions: list = None) -> pd.DataFrame:
    """
    Integrates compatible country identifiers across:
    - Forest Area Net Change (1990 - 2025)
    - Cumulative Forest Fire Disturbance (2000 - 2023)
    - Degradation Definition & Monitoring Status
    - Restoration Commitment Status
    - SFM Policy Adoption Status
    
    Strictly emphasizes exploratory nature: correlation does not imply causality.
    """
    if df_fra.empty or df_ann.empty or df_deg.empty or df_rest.empty:
        return pd.DataFrame()
        
    # 1. Forest Area Change
    piv = df_fra.pivot(index='name', columns='year', values='1a_forestArea')
    if start_year not in piv.columns or end_year not in piv.columns:
        return pd.DataFrame()
        
    chg_df = pd.DataFrame({
        'name': piv.index.tolist(),
        'start_forest_mha': (piv[start_year] / 1000.0).tolist(),
        'end_forest_mha': (piv[end_year] / 1000.0).tolist(),
        'net_change_mha': ((piv[end_year] - piv[start_year]) / 1000.0).tolist(),
        'pct_change': (((piv[end_year] - piv[start_year]) / piv[start_year]) * 100.0).tolist()
    })
    
    # 2. Cumulative Fire
    c_fire = df_ann.groupby('name')['5b_fire_forest'].sum(min_count=1).reset_index()
    c_fire['cumul_fire_mha'] = c_fire['5b_fire_forest'] / 1000.0
    
    # 3. Degradation
    deg_cols = ['name', 'regions', 'iso3', 'Has your country nat. definition of degradation', 'Does your country monitor degradation']
    deg_sub = df_deg[[c for c in deg_cols if c in df_deg.columns]].copy().rename(columns={
        'Has your country nat. definition of degradation': 'has_deg_definition',
        'Does your country monitor degradation': 'monitors_degradation'
    })
    
    # 4. Restoration
    rest_sub = df_rest[['name', 'restoration commitments']].copy().rename(columns={
        'restoration commitments': 'has_restoration_commitment'
    })
    
    # 5. Policy
    pol_sub = df_pol[['name', 'National policies supporting SFM']].copy().rename(columns={
        'National policies supporting SFM': 'has_sfm_policy'
    })
    
    # Merge on country name
    merged = pd.merge(deg_sub, chg_df, on='name', how='inner')
    merged = pd.merge(merged, c_fire[['name', 'cumul_fire_mha']], on='name', how='left')
    merged = pd.merge(merged, rest_sub, on='name', how='left')
    merged = pd.merge(merged, pol_sub, on='name', how='left')
    
    if selected_regions and "All Regions" not in selected_regions:
        merged = merged[merged['regions'].isin(selected_regions)]
        
    return merged


