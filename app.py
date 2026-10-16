"""
app.py - Main Streamlit Dashboard for Global Forest Area Change & Sustainability Analysis
Stage 1: Interactive Data Visualization, KPI Monitoring, and Exploratory Diagnostics.
"""

import streamlit as st
import pandas as pd
import numpy as np

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Global Forest Area Change & Sustainability Dashboard",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import custom modules
from styles import get_custom_css, render_header, render_kpi_card
from data_loader import (
    load_fra_years,
    load_intervals,
    load_annual_disturbances,
    load_forest_policy,
    load_degraded_forest,
    load_forest_restoration,
    filter_fra_data,
    calculate_kpis,
    get_dataset_inventory,
    load_raw_dataset,
    FRA_VARIABLE_MAP
)
from visualizations import (
    plot_forest_trend_line,
    plot_country_comparison_bar,
    plot_variable_histogram,
    plot_correlation_heatmap,
    plot_choropleth_map,
    render_empty_state_notice
)

# 1. Inject Custom CSS Stylesheet
st.markdown(get_custom_css(), unsafe_allow_html=True)

# 2. Data Loading with Graceful Fallback
try:
    df_fra = load_fra_years()
except Exception as e:
    st.error(f"Error loading core FRA dataset: {e}")
    df_fra = pd.DataFrame()

# 3. Sidebar Configuration: Navigation & Dynamic Filters
with st.sidebar:
    st.markdown("### 🌲 Navigation")
    nav_option = st.radio(
        "Select Dashboard View:",
        [
            "📌 Overview & Key Insights",
            "📈 Forest Trends & Dynamics",
            "📊 Distribution & Correlations",
            "🗺️ Global Geographic Map",
            "📋 Dataset Diagnostics & Metadata"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 🔍 Filter Controls")
    
    # Region Filter
    available_regions = ["All Regions"]
    if not df_fra.empty and 'regions' in df_fra.columns:
        valid_regs = sorted([str(r) for r in df_fra['regions'].dropna().unique() if str(r).strip()])
        available_regions.extend(valid_regs)
        
    selected_region = st.selectbox("Select Region / Continent:", available_regions, index=0)
    
    # Dynamic Country Filter based on selected region
    available_countries = ["All Countries"]
    if not df_fra.empty and 'name' in df_fra.columns:
        if selected_region != "All Regions":
            c_subset = df_fra[df_fra['regions'] == selected_region]
        else:
            c_subset = df_fra
        valid_countries = sorted([str(c) for c in c_subset['name'].dropna().unique() if str(c).strip()])
        available_countries.extend(valid_countries)
        
    selected_country = st.selectbox("Select Country / Territory:", available_countries, index=0)
    
    # Year Selection
    all_years = [1990, 2000, 2010, 2015, 2020, 2025]
    if not df_fra.empty and 'year' in df_fra.columns:
        present_years = sorted(df_fra['year'].dropna().unique().tolist())
        if present_years:
            all_years = present_years
            
    selected_year = st.select_slider(
        "Target Reporting Year:",
        options=all_years,
        value=all_years[-1] if all_years else 2025
    )
    
    baseline_year = st.selectbox(
        "Baseline Year (for Change Analysis):",
        options=all_years[:-1] if len(all_years) > 1 else [1990],
        index=0
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #52796f; line-height: 1.4;">
            <strong>Course:</strong> Data Visualization Lab<br>
            <strong>Scope:</strong> Stage 1 Architecture<br>
            <strong>Source:</strong> FAO FRA 2025/2026
        </div>
        """,
        unsafe_allow_html=True
    )

# 4. Header Banner
st.markdown(
    render_header(
        title="Global Forest Area Change & Sustainability Dashboard",
        subtitle="Exploring forest trends, degradation, restoration, and sustainability using FAO Forest Resources Assessment datasets.",
        source="FAO Global Forest Resources Assessment (FRA)",
        updated_date="October 16, 2026",
        country_count=df_fra['name'].nunique() if not df_fra.empty else 236
    ),
    unsafe_allow_html=True
)

# 5. Filter Data
regions_filter = [selected_region] if selected_region != "All Regions" else None
countries_filter = [selected_country] if selected_country != "All Countries" else None

filtered_df = filter_fra_data(
    df_fra,
    selected_regions=regions_filter,
    selected_countries=countries_filter
)

# 6. Dynamic KPI Cards
kpis = calculate_kpis(
    df_fra=df_fra,
    selected_year=selected_year,
    baseline_year=baseline_year,
    selected_regions=regions_filter,
    selected_countries=countries_filter
)

# Render KPI Grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    scope_desc = "Territories Filtered" if selected_country != "All Countries" or selected_region != "All Regions" else "Countries & Territories"
    st.markdown(
        render_kpi_card(
            title="🌍 Geographic Coverage",
            value=f"{kpis['countries_count']}",
            subtext=f"{scope_desc} across {kpis['regions_count']} regions",
            trend="Active Filter" if (selected_region != "All Regions" or selected_country != "All Countries") else "Global",
            trend_positive=True
        ),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        render_kpi_card(
            title="📅 Temporal Coverage",
            value=f"{kpis['years_count']} FRA Years",
            subtext=f"Milestones 1990–2025 + 24 annual disturbance yrs",
            trend=f"Target: {selected_year}",
            trend_positive=True
        ),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        render_kpi_card(
            title="🌲 Total Forest Area",
            value=kpis['forest_area_display'],
            subtext=f"Total forested surface in {selected_year}",
            trend="Verified FRA" if kpis['is_reliable'] else "N/A",
            trend_positive=True
        ),
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        render_kpi_card(
            title=f"📉 Net Forest Change ({baseline_year}→{selected_year})",
            value=kpis['change_display'],
            subtext=kpis['change_subtext'] if kpis['change_subtext'] else "Comparative measurement",
            trend="Gain" if kpis['trend_positive'] else "Loss",
            trend_positive=kpis['trend_positive']
        ),
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# 7. Navigation Views Rendering

# ==========================================
# VIEW 1: OVERVIEW & KEY INSIGHTS
# ==========================================
if nav_option == "📌 Overview & Key Insights":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">🌿 Project Overview & Global Baseline</h2>
            <p class="section-desc">Key empirical observations from the Food and Agriculture Organization (FAO) Global Forest Resources Assessment.</p>
        </div>
        <p style="font-size: 0.95rem; line-height: 1.6; color: #2d3748;">
            This interactive dashboard provides evidence-based analysis of global forest ecosystems between <strong>1990 and 2025</strong>. 
            The dataset tracks <strong>236 countries and territories</strong>, evaluating forest area loss, natural regeneration, afforestation, 
            and disturbances. While global forest area has contracted by approximately <strong>203 million hectares (-4.68%)</strong> since 1990, 
            the dynamics reveal significant regional divergence: persistent tropical deforestation in South America and Africa, 
            contrasted with forest expansion in East Asia and Europe through dedicated afforestation initiatives.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1.1, 0.9])
    
    with col_left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        # Line Chart
        fig_line = plot_forest_trend_line(filtered_df, group_by="By Region" if selected_region == "All Regions" else "Total")
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        # Bar Chart
        fig_bar = plot_country_comparison_bar(filtered_df, year=selected_year, top_n=10, mode="area")
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Regional Dynamics Summary Table
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🌐 Regional Forest Area Dynamics Summary (1990 vs 2025)")
    
    if not df_fra.empty:
        reg_df = df_fra.groupby(['regions', 'year'])['1a_forestArea'].sum().unstack()
        if 1990 in reg_df.columns and 2025 in reg_df.columns:
            summary_table = pd.DataFrame({
                'Region': reg_df.index,
                'Forest Area 1990 (M ha)': (reg_df[1990] / 1000.0).round(2),
                'Forest Area 2025 (M ha)': (reg_df[2025] / 1000.0).round(2),
                'Net Change (M ha)': ((reg_df[2025] - reg_df[1990]) / 1000.0).round(2),
                'Relative Change (%)': (((reg_df[2025] - reg_df[1990]) / reg_df[1990]) * 100).round(2)
            }).reset_index(drop=True)
            
            st.dataframe(
                summary_table.style.format({
                    'Forest Area 1990 (M ha)': "{:,.2f}",
                    'Forest Area 2025 (M ha)': "{:,.2f}",
                    'Net Change (M ha)': "{:+,.2f}",
                    'Relative Change (%)': "{:+.2f}%"
                }),
                use_container_width=True
            )
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# VIEW 2: FOREST TRENDS & DYNAMICS
# ==========================================
elif nav_option == "📈 Forest Trends & Dynamics":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">📈 Longitudinal Trends & Country Trajectories</h2>
            <p class="section-desc">Analyze how forest coverage has evolved across milestones and identify the highest forest loss and gain nations.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Controls for line chart
    trend_mode = st.radio(
        "Trend View Aggregation:",
        ["Aggregate Total", "By Region", "By Country (Top selections)"],
        horizontal=True
    )
    group_map = {"Aggregate Total": "Total", "By Region": "By Region", "By Country (Top selections)": "By Country"}
    
    fig_line_detail = plot_forest_trend_line(filtered_df, group_by=group_map[trend_mode])
    st.plotly_chart(fig_line_detail, use_container_width=True)
    
    st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    col_bar_ctrl, col_bar_chart = st.columns([0.35, 0.65])
    with col_bar_ctrl:
        st.markdown("#### Bar Chart Configuration")
        bar_metric = st.selectbox(
            "Comparison Mode:",
            ["Total Forest Area (Top Countries)", "Net Forest Area Change (Gainers vs Losers)"],
            index=1
        )
        bar_count = st.slider("Number of Countries:", min_value=6, max_value=20, value=10, step=2)
        st.info(
            "💡 **Change mode** calculates paired net difference in forest area between 1990 and the selected target year."
        )

    with col_bar_chart:
        chart_mode = "change" if "Change" in bar_metric else "area"
        fig_bar_detail = plot_country_comparison_bar(
            filtered_df,
            year=selected_year,
            top_n=bar_count,
            mode=chart_mode
        )
        st.plotly_chart(fig_bar_detail, use_container_width=True)

    # Interval Rates Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### ⏱️ Average Annual Rates: Afforestation vs Deforestation (Intervals)")
    df_intervals = load_intervals()
    if not df_intervals.empty:
        int_summary = df_intervals.groupby('year')[['1d_expansion', '1d_afforestation', '1d_deforestation']].sum().reset_index()
        int_summary.columns = ['Interval', 'Expansion (1,000 ha/yr)', 'Afforestation (1,000 ha/yr)', 'Deforestation (1,000 ha/yr)']
        st.dataframe(int_summary.style.format({
            'Expansion (1,000 ha/yr)': "{:,.1f}",
            'Afforestation (1,000 ha/yr)': "{:,.1f}",
            'Deforestation (1,000 ha/yr)': "{:,.1f}"
        }), use_container_width=True)
    else:
        render_empty_state_notice("Intervals Dataset Unavailable", "Intervals_2026-10-16.csv could not be loaded.", "Intervals_2026-10-16.csv")
    st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# VIEW 3: DISTRIBUTION & CORRELATIONS
# ==========================================
elif nav_option == "📊 Distribution & Correlations":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">📊 Variable Distribution & Correlation Heatmap</h2>
            <p class="section-desc">Explore statistical distributions of forest metrics and evaluate Pearson correlations between ecosystem variables.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_hist, col_corr = st.columns([0.48, 0.52])
    
    with col_hist:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 📐 Indicator Distribution")
        
        hist_var = st.selectbox(
            "Select Variable for Histogram:",
            list(FRA_VARIABLE_MAP.keys()),
            format_func=lambda x: FRA_VARIABLE_MAP.get(x, x),
            index=0
        )
        use_log = st.checkbox("Logarithmic Scale (Recommended for skewed areas)", value=True)
        
        fig_hist = plot_variable_histogram(filtered_df, variable=hist_var, year=selected_year, log_scale=use_log)
        st.plotly_chart(fig_hist, use_container_width=True)
        st.caption("Distribution shows country-level variation. A marginal boxplot displays the median and quartiles.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_corr:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 🔗 Inter-Variable Correlation Heatmap")
        fig_corr = plot_correlation_heatmap(df_fra, year=selected_year)
        st.plotly_chart(fig_corr, use_container_width=True)
        st.caption("Pearson correlation coefficients calculated across 8 primary biophysical indicators.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Narrative Interpretation
    st.markdown("""
    <div class="info-callout">
        <strong>💡 Key Correlation Takeaways:</strong>
        <ul style="margin: 0.3rem 0 0 1rem; padding: 0;">
            <li><strong>Biomass & Carbon Coupling:</strong> Above-Ground Biomass and Carbon in Biomass exhibit near-perfect correlation (r ≈ 1.00), confirming stoichiometric consistency in FAO estimates.</li>
            <li><strong>Natural Forest Dominance:</strong> Total Forest Area correlates overwhelmingly with Naturally Regenerating Forest (r ≈ 0.99), indicating that natural ecosystems still constitute the vast majority of global canopy.</li>
            <li><strong>Planted Forest Divergence:</strong> Planted forests show lower correlation with total biomass, reflecting younger stand ages and differing wood density profiles.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# VIEW 4: GLOBAL GEOGRAPHIC MAP
# ==========================================
elif nav_option == "🗺️ Global Geographic Map":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">🗺️ Interactive Global Forest Choropleth</h2>
            <p class="section-desc">Geographic distribution of forest resources mapped by ISO3 standard country identifiers.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_map_opt1, col_map_opt2 = st.columns([0.6, 0.4])
    with col_map_opt1:
        map_indicator = st.radio(
            "Select Map Metric:",
            ["Total Forest Area (Million ha)", "Forest Cover Percentage (% of Land Area)"],
            horizontal=True
        )
    with col_map_opt2:
        st.caption(f"Displaying data for reporting year: **{selected_year}**")

    metric_key = '1a_forestArea' if "Area" in map_indicator else 'forest_cover_pct'
    
    fig_map = plot_choropleth_map(filtered_df, year=selected_year, indicator=metric_key)
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Context callout
    st.markdown("""
    <div class="info-callout">
        <strong>🗺️ Cartographic Insights:</strong>
        The five countries with the highest total forest surface are the <strong>Russian Federation, Brazil, Canada, the United States, and China</strong>, 
        collectively holding over 54% of the world's forests. In terms of <em>Forest Cover Percentage</em>, tropical nations like Suriname, Guyana, and Gabon 
        exceed 80% forest canopy.
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# VIEW 5: DATASET DIAGNOSTICS & METADATA
# ==========================================
elif nav_option == "📋 Dataset Diagnostics & Metadata":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">📋 Dataset Diagnostics, Audit & Documentation</h2>
            <p class="section-desc">Comprehensive transparency report detailing row/column counts, missing values, duplicates, and data scopes.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Audited Inventory Table
    st.markdown("### 🗄️ Available Datasets Inventory")
    inv_df = get_dataset_inventory()
    st.dataframe(inv_df, use_container_width=True)
    
    st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    
    # Interactive Raw Dataset Explorer
    st.markdown("### 🔬 Interactive Dataset Explorer")
    dataset_list = inv_df['Dataset'].tolist()
    chosen_file = st.selectbox("Select Dataset to Inspect:", dataset_list, index=0)
    
    raw_df = load_raw_dataset(chosen_file)
    if not raw_df.empty:
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Total Rows", f"{len(raw_df):,}")
        col_m2.metric("Total Columns", f"{len(raw_df.columns):,}")
        col_m3.metric("Duplicate Rows", f"{raw_df.duplicated().sum()}")
        col_m4.metric("Missing Values", f"{raw_df.isna().sum().sum():,} cells")
        
        tab_sample, tab_cols, tab_missing = st.tabs(["📄 Sample Preview", "🏷️ Column Types", "❓ Missing Summary"])
        
        with tab_sample:
            st.dataframe(raw_df.head(15), use_container_width=True)
            
        with tab_cols:
            dtype_df = pd.DataFrame({
                'Column Name': raw_df.columns,
                'Data Type': raw_df.dtypes.astype(str),
                'Non-Null Count': raw_df.notna().sum().values,
                'Null Count': raw_df.isna().sum().values,
                'Null %': (raw_df.isna().sum().values / len(raw_df) * 100).round(1)
            })
            st.dataframe(dtype_df, use_container_width=True)
            
        with tab_missing:
            null_cols = raw_df.isna().sum()
            null_cols = null_cols[null_cols > 0].sort_values(ascending=False)
            if not null_cols.empty:
                st.write("Columns with missing values (Top 20):")
                st.bar_chart(null_cols.head(20))
            else:
                st.success("No missing values found in this dataset!")
    else:
        st.warning(f"Could not load preview for {chosen_file}.")

    # Methodology & Viva Explanations
    st.markdown("""
    <div class="section-card" style="margin-top: 1.5rem;">
        <h3 style="color: #1b4332; margin-top: 0;">🎓 College Viva & Methodology Notes</h3>
        <p style="font-size: 0.9rem; color: #2d3748; line-height: 1.5;">
            <strong>Data Lineage:</strong> Compiled from the official FAO Global Forest Resources Assessment (FRA) 2025/2026 reporting round.<br>
            <strong>Observation Status Codes (Flags):</strong>
            <ul>
                <li><strong>A:</strong> Official reported country data.</li>
                <li><strong>I:</strong> Imputed value, desk study, or FAO expert compilation.</li>
                <li><strong>M:</strong> Missing value (inapplicable or undefined denominator).</li>
                <li><strong>O:</strong> Missing value (unreported).</li>
            </ul>
            <strong>Unit Standardization:</strong>
            All surface areas are published in <code>1,000 hectares (ha)</code>. In this dashboard, KPIs and high-level charts scale to <code>Million hectares (M ha)</code> or <code>Billion hectares (B ha)</code> for visual legibility.
        </p>
    </div>
    """, unsafe_allow_html=True)

# 8. Footer
st.markdown("""
<div class="footer-bar">
    Global Forest Area Change and Forest Sustainability Analysis • College Data Visualization Project (Stage 1)<br>
    Data Source: Food and Agriculture Organization of the United Nations (FAO FRA) • Built with Python, Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
