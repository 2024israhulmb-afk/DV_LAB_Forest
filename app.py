"""
app.py - Global Forest Area Change & Sustainability Dashboard
Stage 2: Advanced Forest Data Analysis, Period Change Insights, Country Rankings,
Sustainability Indicators, and Comprehensive Data Quality Diagnostics.
"""

import streamlit as st
import pandas as pd
import numpy as np

# 1. Set Streamlit Page Configuration
st.set_page_config(
    page_title="Global Forest Area Change & Sustainability Dashboard",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Import custom modules
from styles import get_custom_css, render_header, render_kpi_card
from data_loader import (
    load_fra_years,
    load_intervals,
    load_annual_disturbances,
    load_forest_policy,
    load_degraded_forest,
    load_forest_restoration,
    load_tiers,
    load_ndp,
    load_nwfp,
    filter_fra_data,
    calculate_kpis,
    calculate_period_change,
    get_top_gainers,
    get_top_losers,
    get_top_countries_by_area,
    get_sustainability_metrics,
    get_flag_audit_report,
    get_tiers_report,
    get_policy_adoption_report,
    get_dataset_inventory,
    load_raw_dataset,
    FRA_VARIABLE_MAP,
    DISTURBANCE_INDICATORS_MAP,
    get_disturbance_time_series,
    get_top_disturbance_countries,
    get_disturbance_kpis,
    get_degradation_profile,
    get_restoration_profile,
    get_cross_topic_synthesis,
    get_statistical_distribution_metrics,
    calculate_correlation_matrix,
    get_regional_comparison_metrics,
    get_interval_dynamics_summary,
    get_country_forest_profile,
    get_research_question_findings
)
from visualizations import (
    plot_forest_trend_line,
    plot_country_comparison_bar,
    plot_variable_histogram,
    plot_correlation_heatmap,
    plot_choropleth_map,
    plot_top_gainers_chart,
    plot_top_losers_chart,
    plot_top_countries_ranking,
    plot_enhanced_trend_line,
    plot_natural_vs_planted_bar,
    plot_forest_cover_percentage_ranking,
    plot_primary_forest_share,
    plot_flag_coverage_by_year,
    plot_tiers_summary,
    render_empty_state_notice,
    plot_disturbance_time_series,
    plot_disturbance_country_ranking,
    plot_disturbance_category_breakdown,
    plot_degradation_governance_charts,
    plot_degradation_methods_bar,
    plot_restoration_commitments_by_region,
    plot_cross_topic_scatter,
    plot_country_forest_distribution_histogram,
    plot_forest_area_outliers_box,
    plot_statistical_correlation_heatmap,
    plot_regional_comparison_bar,
    plot_interval_rates_comparison,
    plot_country_profile_trend,
    plot_country_natural_vs_planted_donut,
    plot_research_q1_global_trajectory,
    plot_research_q4_regional_shares
)

# 3. Inject Custom CSS Stylesheet
st.markdown(get_custom_css(), unsafe_allow_html=True)

# 4. Data Loading with Graceful Fallback
try:
    df_fra = load_fra_years()
except Exception as e:
    st.error(f"Error loading core FRA dataset: {e}")
    df_fra = pd.DataFrame()

try:
    df_intervals = load_intervals()
except Exception:
    df_intervals = pd.DataFrame()

try:
    df_deg = load_degraded_forest()
except Exception:
    df_deg = pd.DataFrame()

try:
    df_rest = load_forest_restoration()
except Exception:
    df_rest = pd.DataFrame()

try:
    df_pol = load_forest_policy()
except Exception:
    df_pol = pd.DataFrame()

try:
    df_tiers = load_tiers()
except Exception:
    df_tiers = pd.DataFrame()

try:
    df_nwfp = load_nwfp()
except Exception:
    df_nwfp = pd.DataFrame()

# 5. Sidebar Configuration: Navigation & Dynamic Filters
with st.sidebar:
    st.markdown("### 🌲 Navigation")
    nav_option = st.radio(
        "Select Dashboard View:",
        [
            "📌 Overview & Key Insights",
            "🔄 Forest Change Insights",
            "🏆 Country Rankings & Comparisons",
            "📈 Multi-Country Trend Analysis",
            "🌱 Forest Sustainability Indicators",
            "🗺️ Global Geographic Map",
            "📋 Data Quality & Diagnostics",
            "🔬 Research Questions & Key Findings"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 🔍 Global Filter Controls")
    
    # Reset filters button
    if st.button("🔄 Reset Global Filters", use_container_width=True):
        st.session_state['sel_region'] = "All Regions"
        st.session_state['sel_country'] = "All Countries"
        st.session_state['sel_year'] = 2025
        st.session_state['sel_baseline'] = 1990
        st.rerun()

    # Region Filter
    available_regions = ["All Regions"]
    if not df_fra.empty and 'regions' in df_fra.columns:
        valid_regs = sorted([str(r) for r in df_fra['regions'].dropna().unique() if str(r).strip()])
        available_regions.extend(valid_regs)
        
    selected_region = st.selectbox(
        "Select Region / Continent:", 
        available_regions, 
        index=0,
        key='sel_region'
    )
    
    # Dynamic Country Filter based on selected region
    available_countries = ["All Countries"]
    if not df_fra.empty and 'name' in df_fra.columns:
        if selected_region != "All Regions":
            c_subset = df_fra[df_fra['regions'] == selected_region]
        else:
            c_subset = df_fra
        valid_countries = sorted([str(c) for c in c_subset['name'].dropna().unique() if str(c).strip()])
        available_countries.extend(valid_countries)
        
    selected_country = st.selectbox(
        "Select Country / Territory:", 
        available_countries, 
        index=0,
        key='sel_country'
    )
    
    # Year Selection (Actual FRA Milestone Years only)
    all_actual_years = [1990, 2000, 2010, 2015, 2020, 2025]
    if not df_fra.empty and 'year' in df_fra.columns:
        present_years = sorted(df_fra['year'].dropna().unique().tolist())
        if present_years:
            all_actual_years = present_years
            
    selected_year = st.select_slider(
        "Target Reporting Year:",
        options=all_actual_years,
        value=all_actual_years[-1] if all_actual_years else 2025,
        key='sel_year'
    )
    
    baseline_year = st.selectbox(
        "Baseline Year (for Change Analysis):",
        options=all_actual_years[:-1] if len(all_actual_years) > 1 else [1990],
        index=0,
        key='sel_baseline'
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #52796f; line-height: 1.4;">
            <strong>Course:</strong> Data Visualization Lab<br>
            <strong>Scope:</strong> Stage 2 Advanced Analytics<br>
            <strong>Standard Unit:</strong> 1 M ha = 1,000,000 ha<br>
            <strong>Data Source:</strong> FAO FRA 2025/2026
        </div>
        """,
        unsafe_allow_html=True
    )

# 6. Header Banner
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

# 7. Apply Filter Data
regions_filter = [selected_region] if selected_region != "All Regions" else None
countries_filter = [selected_country] if selected_country != "All Countries" else None

filtered_df = filter_fra_data(
    df_fra,
    selected_regions=regions_filter,
    selected_countries=countries_filter
)

# 8. Dynamic KPI Cards
kpis = calculate_kpis(
    df_fra=df_fra,
    selected_year=selected_year,
    baseline_year=baseline_year,
    selected_regions=regions_filter,
    selected_countries=countries_filter
)

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
            value=f"{kpis['years_count']} FRA Milestones",
            subtext=f"Reported 1990–2025 (no synthetic data)",
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


# ==============================================================================
# VIEW 1: OVERVIEW & KEY INSIGHTS
# ==============================================================================
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
        fig_line = plot_forest_trend_line(filtered_df, group_by="By Region" if selected_region == "All Regions" else "Total")
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
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


# ==============================================================================
# VIEW 2: FOREST CHANGE INSIGHTS (NEW STAGE 2 DEDICATED PAGE)
# ==============================================================================
elif nav_option == "🔄 Forest Change Insights":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">🔄 Forest Change Insights (Period-to-Period Analysis)</h2>
            <p class="section-desc">Evaluate net forest-area changes, annual change rates, and country-level increases and decreases between any two FRA reporting milestones.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Period Selection Controls
    col_p1, col_p2, col_p3 = st.columns([0.3, 0.3, 0.4])
    with col_p1:
        start_yr = st.selectbox(
            "Starting Reporting Year:",
            options=all_actual_years[:-1],
            index=0,
            key='change_start_yr'
        )
    with col_p2:
        valid_end_years = [y for y in all_actual_years if y > start_yr]
        end_yr = st.selectbox(
            "Ending Reporting Year:",
            options=valid_end_years if valid_end_years else [all_actual_years[-1]],
            index=len(valid_end_years)-1 if valid_end_years else 0,
            key='change_end_yr'
        )
    with col_p3:
        st.markdown(f"""
        <div style="background: #f1f8f4; border: 1px solid #d8f3dc; padding: 0.75rem 1rem; border-radius: 10px; margin-top: 0.3rem;">
            <strong>Selected Period:</strong> {start_yr} → {end_yr} ({end_yr - start_yr} Years)<br>
            <span style="font-size: 0.82rem; color: #52796f;">Filtered Region: <strong>{selected_region}</strong> | Filtered Country: <strong>{selected_country}</strong></span>
        </div>
        """, unsafe_allow_html=True)

    # Execute period change calculation
    change_df, period_summary = calculate_period_change(
        df_fra=df_fra,
        start_year=start_yr,
        end_year=end_yr,
        selected_regions=regions_filter,
        selected_countries=countries_filter
    )

    if not period_summary['is_valid']:
        st.error(f"⚠️ {period_summary['error_msg']}")
    else:
        # Period KPI Cards
        st.markdown("#### 📊 Period Performance Summary")
        pk1, pk2, pk3, pk4 = st.columns(4)
        
        with pk1:
            st.markdown(
                render_kpi_card(
                    title="🌐 Period Net Change",
                    value=f"{'+' if period_summary['net_change_mha'] > 0 else ''}{period_summary['net_change_mha']:,.2f} M ha",
                    subtext=f"{'+' if period_summary['pct_change'] > 0 else ''}{period_summary['pct_change']:.2f}% overall",
                    trend="Net Expansion" if period_summary['net_change_mha'] >= 0 else "Net Deforestation",
                    trend_positive=period_summary['net_change_mha'] >= 0
                ),
                unsafe_allow_html=True
            )
            
        with pk2:
            st.markdown(
                render_kpi_card(
                    title="⏱️ Average Annual Rate",
                    value=f"{'+' if period_summary['annual_rate_mha'] > 0 else ''}{period_summary['annual_rate_mha']:,.2f} M ha/yr",
                    subtext=f"Annualized rate over {period_summary['years_diff']} years",
                    trend=f"{period_summary['years_diff']} yrs span",
                    trend_positive=period_summary['annual_rate_mha'] >= 0
                ),
                unsafe_allow_html=True
            )
            
        with pk3:
            st.markdown(
                render_kpi_card(
                    title="🌲 Expanding Nations",
                    value=f"{period_summary['gainers_count']} Countries",
                    subtext=f"Out of {period_summary['countries_evaluated']} evaluated nations",
                    trend="Forest Gainers",
                    trend_positive=True
                ),
                unsafe_allow_html=True
            )
            
        with pk4:
            st.markdown(
                render_kpi_card(
                    title="🪓 Declining Nations",
                    value=f"{period_summary['losers_count']} Countries",
                    subtext=f"{period_summary['stable_count']} nations remained stable",
                    trend="Forest Losers",
                    trend_positive=False
                ),
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Gainers and Losers Side-by-Side Charts
        col_gain, col_lose = st.columns(2)
        top_gainers = get_top_gainers(change_df, n=10)
        top_losers = get_top_losers(change_df, n=10)

        with col_gain:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            fig_gain = plot_top_gainers_chart(top_gainers, start_yr, end_yr)
            st.plotly_chart(fig_gain, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_lose:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            fig_lose = plot_top_losers_chart(top_losers, start_yr, end_yr)
            st.plotly_chart(fig_lose, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Scientific Methodology Callout: Net Forest Area Change vs Gross Deforestation
        st.markdown("""
        <div class="info-callout">
            <strong>🎓 Scientific Distinction: Net Forest-Area Change vs Gross Deforestation & Tree-Cover Loss</strong>
            <ul style="margin: 0.3rem 0 0 1.2rem; padding: 0; line-height: 1.5;">
                <li><strong>Net Forest-Area Change:</strong> Defined by FAO as the mathematical sum of all forest expansions (natural regeneration + planted afforestation) <em>minus</em> all forest losses (deforestation). A country with high gross deforestation can still report a positive net change if its tree-planting programs exceed forest clearing (e.g. China).</li>
                <li><strong>Gross Deforestation:</strong> Refers strictly to the permanent conversion of forest land to another land use (e.g. agriculture, infrastructure).</li>
                <li><strong>Satellite Tree-Cover Loss:</strong> Frequently reported by remote-sensing platforms (e.g. Global Forest Watch). It detects canopy disturbance regardless of whether it is permanent deforestation, planned forestry harvesting, wildfire, or disease dieback where the land remains classified as forest.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Detailed Period Change Data Table & Download Option
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Complete Period Change Data Table")
        
        # Search & Filter within results
        search_query = st.text_input("🔍 Search country name in results:", "", key='table_search')
        display_df = change_df.copy()
        if search_query:
            display_df = display_df[display_df['name'].str.contains(search_query, case=False, na=False)]
            
        formatted_table = display_df[[
            'name', 'regions', 'start_area_mha', 'end_area_mha', 
            'abs_change_mha', 'pct_change', 'annual_rate_mha', 'direction'
        ]].rename(columns={
            'name': 'Country / Territory',
            'regions': 'Region',
            'start_area_mha': f'Forest Area {start_yr} (M ha)',
            'end_area_mha': f'Forest Area {end_yr} (M ha)',
            'abs_change_mha': 'Net Change (M ha)',
            'pct_change': 'Relative Change (%)',
            'annual_rate_mha': 'Annual Rate (M ha/yr)',
            'direction': 'Trend'
        })

        st.dataframe(
            formatted_table.style.format({
                f'Forest Area {start_yr} (M ha)': "{:,.2f}",
                f'Forest Area {end_yr} (M ha)': "{:,.2f}",
                'Net Change (M ha)': "{:+,.2f}",
                'Relative Change (%)': "{:+.2f}%",
                'Annual Rate (M ha/yr)': "{:+,.3f}"
            }),
            use_container_width=True
        )

        # CSV Download Button
        csv_data = change_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Download Filtered Period Change Analysis ({start_yr} - {end_yr}) as CSV",
            data=csv_data,
            file_name=f"forest_change_{start_yr}_{end_yr}_{selected_region.replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# VIEW 3: COUNTRY RANKINGS & COMPARISONS (NEW STAGE 2 PAGE)
# ==============================================================================
elif nav_option == "🏆 Country Rankings & Comparisons":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">🏆 Country Rankings & Comparative Performance</h2>
            <p class="section-desc">Explore the largest national forest reserves, fastest forest expanding nations, and nations with steepest forest decline.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ranking_mode = st.radio(
        "Select Ranking Dimension:",
        [
            f"🌲 Top Countries by Total Forest Area ({selected_year})",
            f"📈 Top Countries by Forest Area Increase ({baseline_year} → {selected_year})",
            f"📉 Top Countries by Forest Area Decrease ({baseline_year} → {selected_year})"
        ],
        horizontal=True
    )
    
    rank_count = st.slider("Select Number of Countries to Rank:", min_value=5, max_value=25, value=10, step=5)

    if "Total Forest Area" in ranking_mode:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        fig_rank_area = plot_top_countries_ranking(
            df_fra, 
            year=selected_year, 
            n=rank_count, 
            selected_regions=regions_filter
        )
        st.plotly_chart(fig_rank_area, use_container_width=True)
        
        # Display corresponding ranking table
        top_area_df = get_top_countries_by_area(df_fra, year=selected_year, n=rank_count, selected_regions=regions_filter)
        st.markdown(f"#### 📊 Top {rank_count} Forested Nations Data Summary ({selected_year})")
        st.dataframe(
            top_area_df[['name', 'regions', 'forest_area_mha', 'share_of_total_pct']].rename(columns={
                'name': 'Country',
                'regions': 'Region',
                'forest_area_mha': f'Forest Area {selected_year} (M ha)',
                'share_of_total_pct': 'Share of Evaluated Total (%)'
            }).style.format({
                f'Forest Area {selected_year} (M ha)': "{:,.2f}",
                'Share of Evaluated Total (%)': "{:.2f}%"
            }),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    elif "Increase" in ranking_mode:
        chg_data, _ = calculate_period_change(df_fra, baseline_year, selected_year, regions_filter)
        gainers = get_top_gainers(chg_data, n=rank_count)
        
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        fig_rank_gain = plot_top_gainers_chart(gainers, baseline_year, selected_year)
        st.plotly_chart(fig_rank_gain, use_container_width=True)
        
        st.markdown(f"#### 📈 Top {len(gainers)} Forest Expanding Nations Data ({baseline_year} → {selected_year})")
        st.dataframe(
            gainers[['name', 'regions', 'start_area_mha', 'end_area_mha', 'abs_change_mha', 'pct_change']].rename(columns={
                'name': 'Country',
                'regions': 'Region',
                'start_area_mha': f'Forest {baseline_year} (M ha)',
                'end_area_mha': f'Forest {selected_year} (M ha)',
                'abs_change_mha': 'Net Increase (M ha)',
                'pct_change': 'Relative Growth (%)'
            }).style.format({
                f'Forest {baseline_year} (M ha)': "{:,.2f}",
                f'Forest {selected_year} (M ha)': "{:,.2f}",
                'Net Increase (M ha)': "{:+,.2f}",
                'Relative Growth (%)': "{:+.2f}%"
            }),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else: # Decrease
        chg_data, _ = calculate_period_change(df_fra, baseline_year, selected_year, regions_filter)
        losers = get_top_losers(chg_data, n=rank_count)
        
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        fig_rank_lose = plot_top_losers_chart(losers, baseline_year, selected_year)
        st.plotly_chart(fig_rank_lose, use_container_width=True)
        
        st.markdown(f"#### 📉 Top {len(losers)} Forest Decreasing Nations Data ({baseline_year} → {selected_year})")
        st.dataframe(
            losers[['name', 'regions', 'start_area_mha', 'end_area_mha', 'abs_change_mha', 'pct_change']].rename(columns={
                'name': 'Country',
                'regions': 'Region',
                'start_area_mha': f'Forest {baseline_year} (M ha)',
                'end_area_mha': f'Forest {selected_year} (M ha)',
                'abs_change_mha': 'Net Decrease (M ha)',
                'pct_change': 'Relative Loss (%)'
            }).style.format({
                f'Forest {baseline_year} (M ha)': "{:,.2f}",
                f'Forest {selected_year} (M ha)': "{:,.2f}",
                'Net Decrease (M ha)': "{:,.2f}",
                'Relative Loss (%)': "{:.2f}%"
            }),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# VIEW 4: MULTI-COUNTRY TREND ANALYSIS (ENHANCED STAGE 2 PAGE)
# ==============================================================================
elif nav_option == "📈 Multi-Country Trend Analysis":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">📈 Longitudinal Multi-Country Trajectory Explorer</h2>
            <p class="section-desc">Compare the historical forest area trajectories of selected countries across actual FAO milestone years (1990–2025).</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_t1, col_t2 = st.columns([0.65, 0.35])
    with col_t1:
        default_comparison_countries = ["Brazil", "China", "Russian Federation", "United States of America", "Indonesia", "Democratic Republic of the Congo"]
        all_c_list = sorted(df_fra['name'].dropna().unique().tolist())
        selected_multi_countries = st.multiselect(
            "Select Countries to Compare (2 to 10 recommended):",
            options=all_c_list,
            default=[c for c in default_comparison_countries if c in all_c_list]
        )
    with col_t2:
        selected_year_subset = st.multiselect(
            "Select Actual FRA Milestone Years:",
            options=all_actual_years,
            default=all_actual_years
        )
        show_global_trace = st.checkbox("Overlay Global Total (Secondary Axis)", value=False)

    if not selected_year_subset:
        st.warning("Please select at least one reporting year milestone.")
    else:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        fig_multi = plot_enhanced_trend_line(
            df_fra,
            selected_countries=selected_multi_countries,
            years_subset=selected_year_subset,
            show_global=show_global_trace
        )
        st.plotly_chart(fig_multi, use_container_width=True)
        st.caption("ℹ️ Only actual reported FRA milestone observations are plotted. No artificial or interpolated annual observations are introduced.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Interval Rates Table
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### ⏱️ Integrated Reporting Intervals: Annual Rates of Expansion vs Deforestation")
    df_intervals = load_intervals()
    if not df_intervals.empty:
        int_summary = df_intervals.groupby('year')[['1d_expansion', '1d_afforestation', '1d_deforestation']].sum().reset_index()
        int_summary.columns = ['Reporting Interval', 'Total Expansion (1,000 ha/yr)', 'Afforestation (1,000 ha/yr)', 'Deforestation (1,000 ha/yr)']
        int_summary['Net Interval Rate (1,000 ha/yr)'] = int_summary['Total Expansion (1,000 ha/yr)'] - int_summary['Deforestation (1,000 ha/yr)']
        st.dataframe(int_summary.style.format({
            'Total Expansion (1,000 ha/yr)': "{:,.1f}",
            'Afforestation (1,000 ha/yr)': "{:,.1f}",
            'Deforestation (1,000 ha/yr)': "{:,.1f}",
            'Net Interval Rate (1,000 ha/yr)': "{:+,.1f}"
        }), use_container_width=True)
    else:
        render_empty_state_notice("Intervals Dataset Unavailable", "Intervals_2026-10-16.csv could not be loaded.", "Intervals_2026-10-16.csv")
    st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# VIEW 5: FOREST SUSTAINABILITY INDICATORS (NEW STAGE 2 PAGE)
# ==============================================================================
elif nav_option == "🌱 Forest Sustainability Indicators":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">🌱 Forest Sustainability & Ecosystem Integrity Indicators</h2>
            <p class="section-desc">Assess forest cover density, primary forest preservation, natural vs planted forest composition, and SFM policy governance.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    sust_df = get_sustainability_metrics(
        df_fra, 
        year=selected_year, 
        selected_regions=regions_filter, 
        selected_countries=countries_filter
    )

    tab_comp, tab_cover, tab_prim, tab_policy = st.tabs([
        "🌲 Natural vs Planted Forests", 
        "📐 Forest Cover % of Land", 
        "🏛️ Primary Old-Growth Forests",
        "📜 Forest Governance & Policy"
    ])

    with tab_comp:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"#### 🌲 Naturally Regenerating vs Planted Forests ({selected_year})")
        st.write(
            "FAO classifies all forests into two primary non-overlapping structural classes: "
            "**Naturally Regenerating Forest** (forest predominantly composed of trees established through natural regeneration) and "
            "**Planted Forest** (forest predominantly composed of trees established through planting and/or deliberate seeding). "
            "Together, these two categories sum to Total Forest Area without double-counting."
        )
        fig_comp = plot_natural_vs_planted_bar(sust_df, top_n=12)
        st.plotly_chart(fig_comp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_cover:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"#### 📐 Forest Area as a Percentage of Land Area ({selected_year})")
        st.write(
            "Globally, forests cover approximately **31% of the world's total land area**. "
            "However, national cover ranges from below 1% in hyper-arid countries to over 80% in tropical nations."
        )
        col_cov_hi, col_cov_lo = st.columns(2)
        with col_cov_hi:
            fig_cov_hi = plot_forest_cover_percentage_ranking(sust_df, top_n=10, mode="highest")
            st.plotly_chart(fig_cov_hi, use_container_width=True)
        with col_cov_lo:
            fig_cov_lo = plot_forest_cover_percentage_ranking(sust_df, top_n=10, mode="lowest")
            st.plotly_chart(fig_cov_lo, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_prim:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(f"#### 🏛️ Primary (Old-Growth) Forest Extent ({selected_year})")
        st.write(
            "**Primary forests** are naturally regenerated forests of native species where there are no clearly visible indications of human activities "
            "and ecological processes are not significantly disturbed. Primary forest is a sub-category of Naturally Regenerating Forest."
        )
        fig_prim = plot_primary_forest_share(sust_df, top_n=12)
        st.plotly_chart(fig_prim, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_policy:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("#### 📜 Sustainable Forest Management (SFM) Governance Adoption")
        st.write(
            "Integration from `ForestPolicy_2026-10-16.csv`: Documents institutional frameworks supporting sustainable forest management."
        )
        pol_report = get_policy_adoption_report()
        if not pol_report.empty:
            st.dataframe(pol_report, use_container_width=True)
            st.info(
                "💡 Over **81% of evaluated countries (192 nations)** have national policies supporting Sustainable Forest Management, "
                "and **84% (199 nations)** have enacted dedicated national forest legislation."
            )
        else:
            render_empty_state_notice("Policy Dataset Unavailable", "ForestPolicy_2026-10-16.csv could not be loaded.", "ForestPolicy_2026-10-16.csv")
        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# VIEW 6: GLOBAL GEOGRAPHIC MAP
# ==============================================================================
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


# ==============================================================================
# VIEW 7: DATA QUALITY & DIAGNOSTICS (ENHANCED STAGE 2 PAGE)
# ==============================================================================
elif nav_option == "📋 Data Quality & Diagnostics":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">📋 Comprehensive Data Quality, Audit & Methodological Diagnostics</h2>
            <p class="section-desc">Transparent reporting on dataset dimensions, observation status flags, data confidence tiers, missingness, and methodology.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Audited Inventory Table
    st.markdown("### 🗄️ Available Datasets Inventory (Dimensions & Column Breakdown)")
    inv_df = get_dataset_inventory()
    st.dataframe(inv_df, use_container_width=True)
    
    st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # Observation Status Flags Audit
    st.markdown("### 🚩 Observation Status Flags Audit across FRA Reporting Milestones")
    st.write(
        "FAO reports data quality through observation flags. It is vital to preserve the distinction between **officially reported values (Flag A)**, "
        "**imputed / desk study estimates (Flag I)**, and **unreported missing values (Flag O/M)**. "
        "Missing values are preserved as nulls and never fabricated as zero."
    )
    
    flag_audit_df = get_flag_audit_report(df_fra)
    if not flag_audit_df.empty:
        var_choice = st.selectbox(
            "Select Variable to Audit Flags:",
            options=flag_audit_df['Variable'].unique(),
            index=0
        )
        fig_flag = plot_flag_coverage_by_year(flag_audit_df, variable=var_choice)
        st.plotly_chart(fig_flag, use_container_width=True)
        
        # Table of flags
        st.dataframe(flag_audit_df[flag_audit_df['Variable'] == var_choice], use_container_width=True)

    st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 1.5rem 0;'>", unsafe_allow_html=True)

    # Tiers Analysis Integration
    st.markdown("### 🏅 Empirical Confidence Tiers (from Tiers_2026-10-16.csv)")
    st.write(
        "FAO assigns confidence tiers based on the source data strength: "
        "**Tier 3 (High):** Based on recent National Forest Inventories (NFI) or wall-to-wall satellite remote sensing; "
        "**Tier 2 (Medium):** Based on partial or older inventory surveys; "
        "**Tier 1 (Low):** Based on expert models or desk study extrapolations."
    )
    tiers_report = get_tiers_report()
    if not tiers_report.empty:
        fig_tiers = plot_tiers_summary(tiers_report)
        st.plotly_chart(fig_tiers, use_container_width=True)
        st.dataframe(tiers_report, use_container_width=True)
    else:
        render_empty_state_notice("Tiers Dataset Unavailable", "Tiers_2026-10-16.csv could not be loaded.", "Tiers_2026-10-16.csv")

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
        col_m4.metric("Missing Cells", f"{raw_df.isna().sum().sum():,} cells")
        
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


# ==============================================================================
# VIEW 8: RESEARCH QUESTIONS & KEY FINDINGS (STAGE 3)
# ==============================================================================
elif nav_option == "🔬 Research Questions & Key Findings":
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <h2 class="section-title">🔬 Research Questions, Statistical Analysis & Country Validation</h2>
            <p class="section-desc">Empirical investigation of core FAO FRA research questions, statistical dispersion, outlier diagnostics, and granular multi-dataset country profiling.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_rq, tab_stats, tab_profile, tab_export = st.tabs([
        "❓ 8 Core Research Questions",
        "📐 Statistical Analysis & Outliers",
        "🌲 Country Forest Profile",
        "📑 Summary Report & Downloads"
    ])

    # --------------------------------------------------------------------------
    # TAB 1: 8 CORE RESEARCH QUESTIONS
    # --------------------------------------------------------------------------
    with tab_rq:
        st.markdown("""
        <div class="info-callout">
            <strong>Methodological Note on FAO FRA Data:</strong>
            Findings are generated dynamically from official FAO Forest Resources Assessment datasets.
            Calculations strictly adhere to official definitions: <strong>Net Forest-Area Change</strong> represents the algebraic sum 
            of forest losses, afforestation, and natural expansion, and is <em>not</em> equivalent to gross deforestation or satellite tree-cover canopy loss.
        </div>
        """, unsafe_allow_html=True)

        findings = get_research_question_findings(
            df_fra=df_fra,
            df_intervals=df_intervals,
            df_deg=df_deg,
            df_rest=df_rest,
            df_pol=df_pol,
            df_tiers=df_tiers,
            start_year=baseline_year,
            end_year=selected_year,
            selected_regions=regions_filter
        )

        # --- Q1 ---
        q1 = findings['Q1']
        st.markdown(f"""
        <div class="rq-card">
            <span class="rq-badge">Research Question 1</span>
            <span class="stat-pill">📅 {q1['reporting_period']}</span>
            <h3 class="rq-title">{q1['question']}</h3>
            <div class="formula-callout"><strong>Formula Applied:</strong> {q1['calculation_used']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_q1_m1, col_q1_m2, col_q1_m3, col_q1_m4 = st.columns(4)
        if q1['summary']['is_valid']:
            col_q1_m1.metric("1990 Forest Extent", f"{q1['summary']['total_start_mha']:,.1f} M ha")
            col_q1_m2.metric("2025 Forest Extent", f"{q1['summary']['total_end_mha']:,.1f} M ha")
            col_q1_m3.metric("Net Change (1990→2025)", f"{q1['summary']['net_change_mha']:,.1f} M ha", f"{q1['summary']['pct_change']:.2f}%")
            col_q1_m4.metric("Annualized Rate", f"{q1['summary']['annual_rate_mha']:,.2f} M ha/yr")

        fig_q1 = plot_research_q1_global_trajectory(df_fra)
        st.plotly_chart(fig_q1, use_container_width=True)
        st.markdown(f'<div class="finding-callout"><strong>Data-Driven Finding:</strong> {q1["interpretation"]}</div>', unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 2rem 0;'>", unsafe_allow_html=True)

        # --- Q2 ---
        q2 = findings['Q2']
        st.markdown(f"""
        <div class="rq-card">
            <span class="rq-badge">Research Question 2</span>
            <span class="stat-pill">📅 {q2['reporting_period']}</span>
            <h3 class="rq-title">{q2['question']}</h3>
            <div class="formula-callout"><strong>Formula Applied:</strong> {q2['calculation_used']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_q2_c, col_q2_t = st.columns([0.55, 0.45])
        with col_q2_c:
            fig_q2 = plot_top_countries_ranking(df_fra, year=2025, n=10, selected_regions=regions_filter)
            st.plotly_chart(fig_q2, use_container_width=True)
        with col_q2_t:
            if 'data_table' in q2 and not q2['data_table'].empty:
                st.dataframe(
                    q2['data_table'].style.format({
                        'Forest Area 2025 (M ha)': "{:,.2f}",
                        'Global Share (%)': "{:.2f}%"
                    }),
                    use_container_width=True
                )
        st.markdown(f'<div class="finding-callout"><strong>Data-Driven Finding:</strong> {q2["interpretation"]}</div>', unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 2rem 0;'>", unsafe_allow_html=True)

        # --- Q3 ---
        q3 = findings['Q3']
        st.markdown(f"""
        <div class="rq-card">
            <span class="rq-badge">Research Question 3</span>
            <span class="stat-pill">📅 {q3['reporting_period']}</span>
            <h3 class="rq-title">{q3['question']}</h3>
            <div class="formula-callout"><strong>Formula Applied:</strong> {q3['calculation_used']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_q3_g, col_q3_l = st.columns(2)
        with col_q3_g:
            st.markdown(f"#### 📈 Top Forest Expanding Nations ({baseline_year}→{selected_year})")
            if 'gainers_table' in q3 and not q3['gainers_table'].empty:
                st.dataframe(
                    q3['gainers_table'].style.format({
                        'Increase (M ha)': "{:+,.2f}",
                        'Relative Growth (%)': "{:+.2f}%"
                    }),
                    use_container_width=True
                )
        with col_q3_l:
            st.markdown(f"#### 📉 Top Forest Decreasing Nations ({baseline_year}→{selected_year})")
            if 'losers_table' in q3 and not q3['losers_table'].empty:
                st.dataframe(
                    q3['losers_table'].style.format({
                        'Decrease (M ha)': "{:,.2f}",
                        'Relative Loss (%)': "{:.2f}%"
                    }),
                    use_container_width=True
                )
        st.markdown(f'<div class="finding-callout"><strong>Data-Driven Finding:</strong> {q3["interpretation"]}</div>', unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 2rem 0;'>", unsafe_allow_html=True)

        # --- Q4 ---
        q4 = findings['Q4']
        st.markdown(f"""
        <div class="rq-card">
            <span class="rq-badge">Research Question 4</span>
            <span class="stat-pill">📅 {q4['reporting_period']}</span>
            <h3 class="rq-title">{q4['question']}</h3>
            <div class="formula-callout"><strong>Formula Applied:</strong> {q4['calculation_used']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_q4_1, col_q4_2 = st.columns(2)
        with col_q4_1:
            fig_q4_share = plot_research_q4_regional_shares(q4['regional_table'], end_year=2025)
            st.plotly_chart(fig_q4_share, use_container_width=True)
        with col_q4_2:
            fig_q4_bar = plot_regional_comparison_bar(q4['regional_table'], start_year=1990, end_year=2025)
            st.plotly_chart(fig_q4_bar, use_container_width=True)

        if not q4['regional_table'].empty:
            st.dataframe(
                q4['regional_table'].style.format({
                    'Forest Area 1990 (M ha)': "{:,.1f}",
                    'Forest Area 2025 (M ha)': "{:,.1f}",
                    'Net Change (M ha)': "{:+,.1f}",
                    'Relative Change (%)': "{:+.2f}%",
                    'Annual Rate (M ha/yr)': "{:+,.3f}",
                    'Total Land Area (M ha)': "{:,.1f}",
                    'Forest Cover (% Land)': "{:.1f}%",
                    'Share of Global Forest 2025 (%)': "{:.1f}%"
                }),
                use_container_width=True
            )
        st.markdown(f'<div class="finding-callout"><strong>Data-Driven Finding:</strong> {q4["interpretation"]}</div>', unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 2rem 0;'>", unsafe_allow_html=True)

        # --- Q5 ---
        q5 = findings['Q5']
        st.markdown(f"""
        <div class="rq-card">
            <span class="rq-badge">Research Question 5</span>
            <span class="stat-pill">📅 {q5['reporting_period']}</span>
            <h3 class="rq-title">{q5['question']}</h3>
            <div class="formula-callout"><strong>Formula Applied:</strong> {q5['calculation_used']}</div>
        </div>
        """, unsafe_allow_html=True)

        fig_q5 = plot_interval_rates_comparison(df_intervals)
        st.plotly_chart(fig_q5, use_container_width=True)
        if not q5['intervals_table'].empty:
            st.dataframe(q5['intervals_table'], use_container_width=True)
        st.markdown(f'<div class="finding-callout"><strong>Data-Driven Finding:</strong> {q5["interpretation"]}</div>', unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 2rem 0;'>", unsafe_allow_html=True)

        # --- Q6 ---
        q6 = findings['Q6']
        st.markdown(f"""
        <div class="rq-card">
            <span class="rq-badge">Research Question 6</span>
            <span class="stat-pill">📅 {q6['reporting_period']}</span>
            <h3 class="rq-title">{q6['question']}</h3>
            <div class="formula-callout"><strong>Formula Applied:</strong> {q6['calculation_used']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_q6_k1, col_q6_k2, col_q6_k3, col_q6_k4 = st.columns(4)
        col_q6_k1.metric("Naturally Regenerating Total", f"{q6['natural_total_mha']:,.1f} M ha")
        col_q6_k2.metric("Planted Forest Total", f"{q6['planted_total_mha']:,.1f} M ha")
        col_q6_k3.metric("Natural Forest Share", f"{q6['natural_share_pct']:.1f}%")
        col_q6_k4.metric("Planted Forest Share", f"{q6['planted_share_pct']:.1f}%")

        sust_df_q6 = get_sustainability_metrics(df_fra, year=2025, selected_regions=regions_filter)
        fig_q6 = plot_natural_vs_planted_bar(sust_df_q6, top_n=12)
        st.plotly_chart(fig_q6, use_container_width=True)
        st.markdown(f'<div class="finding-callout"><strong>Data-Driven Finding:</strong> {q6["interpretation"]}</div>', unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 2rem 0;'>", unsafe_allow_html=True)

        # --- Q7 ---
        q7 = findings['Q7']
        st.markdown(f"""
        <div class="rq-card">
            <span class="rq-badge">Research Question 7</span>
            <span class="stat-pill">📅 {q7['reporting_period']}</span>
            <h3 class="rq-title">{q7['question']}</h3>
            <div class="formula-callout"><strong>Formula Applied:</strong> {q7['calculation_used']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_q7_1, col_q7_2 = st.columns(2)
        with col_q7_1:
            flag_audit_q7 = get_flag_audit_report(df_fra)
            if not flag_audit_q7.empty:
                fig_q7_flags = plot_flag_coverage_by_year(flag_audit_q7, variable="Total Forest Area")
                st.plotly_chart(fig_q7_flags, use_container_width=True)
        with col_q7_2:
            if not q7['tiers_summary'].empty:
                fig_q7_tiers = plot_tiers_summary(q7['tiers_summary'])
                st.plotly_chart(fig_q7_tiers, use_container_width=True)
        st.markdown(f'<div class="finding-callout"><strong>Data-Driven Finding:</strong> {q7["interpretation"]}</div>', unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 2rem 0;'>", unsafe_allow_html=True)

        # --- Q8 ---
        q8 = findings['Q8']
        st.markdown(f"""
        <div class="rq-card">
            <span class="rq-badge">Research Question 8</span>
            <span class="stat-pill">📅 {q8['reporting_period']}</span>
            <h3 class="rq-title">{q8['question']}</h3>
            <div class="formula-callout"><strong>Formula Applied:</strong> {q8['calculation_used']}</div>
        </div>
        """, unsafe_allow_html=True)

        col_q8_1, col_q8_2 = st.columns([0.45, 0.55])
        with col_q8_1:
            if not q8['policy_summary'].empty:
                st.markdown("#### 📜 Sustainable Forest Management Policy Adoption")
                st.dataframe(q8['policy_summary'], use_container_width=True)
        with col_q8_2:
            st.markdown("#### 🤝 National Restoration Commitments by Region")
            fig_q8_rest = plot_restoration_commitments_by_region(df_rest)
            st.plotly_chart(fig_q8_rest, use_container_width=True)
        st.markdown(f'<div class="finding-callout"><strong>Data-Driven Finding:</strong> {q8["interpretation"]}</div>', unsafe_allow_html=True)


    # --------------------------------------------------------------------------
    # TAB 2: STATISTICAL ANALYSIS & OUTLIERS
    # --------------------------------------------------------------------------
    with tab_stats:
        st.markdown("### 📐 Statistical Analysis, Skewness, Outlier & Correlation Diagnostics")
        st.write(
            "Rigorous exploratory data analysis (EDA) evaluating the dispersion, asymmetry, parametric vs non-parametric statistics, "
            "and linear relationships of forest indicators across the 236 evaluated countries and territories."
        )

        # 1. Period-to-Period Statistical Change Calculator
        st.markdown("#### 1. Period Percentage & Annualized Change Calculator")
        col_s_y1, col_s_y2 = st.columns(2)
        with col_s_y1:
            stat_start_yr = st.selectbox("Start Milestone:", all_actual_years[:-1], index=0, key='stat_start_yr')
        with col_s_y2:
            stat_valid_end = [y for y in all_actual_years if y > stat_start_yr]
            stat_end_yr = st.selectbox("End Milestone:", stat_valid_end if stat_valid_end else [all_actual_years[-1]], index=len(stat_valid_end)-1 if stat_valid_end else 0, key='stat_end_yr')

        _, stat_chg = calculate_period_change(df_fra, stat_start_yr, stat_end_yr, regions_filter)
        if stat_chg['is_valid']:
            col_sc1, col_sc2, col_sc3, col_sc4 = st.columns(4)
            col_sc1.metric(f"Net Change ({stat_start_yr}→{stat_end_yr})", f"{stat_chg['net_change_mha']:+,.1f} M ha")
            col_sc2.metric("Relative Percentage Change", f"{stat_chg['pct_change']:+.2f}%")
            col_sc3.metric("Annualized Change Rate", f"{stat_chg['annual_rate_mha']:+,.3f} M ha/yr")
            col_sc4.metric("Expanding vs Declining", f"{stat_chg['gainers_count']} Gain / {stat_chg['losers_count']} Loss")
        else:
            st.warning(stat_chg.get('error_msg', 'Unable to compute period change.'))

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # 2. Distribution & Skewness
        st.markdown("#### 2. Country Forest Area Frequency Distribution & Skewness")
        stat_dist_year = st.select_slider("Target Year for Distribution:", options=all_actual_years, value=selected_year, key='stat_dist_yr')
        dist_metrics = get_statistical_distribution_metrics(df_fra, year=stat_dist_year, selected_regions=regions_filter)

        col_opt_hist, _ = st.columns([0.4, 0.6])
        with col_opt_hist:
            scale_choice = st.radio("X-Axis Scaling:", ["Logarithmic Scale (Recommended for Skewed Data)", "Linear Scale"], horizontal=True, key='hist_scale')
        use_log = "Logarithmic" in scale_choice

        fig_hist = plot_country_forest_distribution_histogram(dist_metrics, log_scale=use_log)
        st.plotly_chart(fig_hist, use_container_width=True)

        if dist_metrics['is_valid']:
            col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns(5)
            col_d1.metric("Evaluated Nations", f"{dist_metrics['count']}")
            col_d2.metric("Mean Area", f"{dist_metrics['mean_mha']:,.2f} M ha")
            col_d3.metric("Median Area", f"{dist_metrics['median_mha']:,.2f} M ha")
            col_d4.metric("Std Deviation", f"{dist_metrics['std_mha']:,.2f} M ha")
            col_d5.metric("Fisher-Pearson Skewness", f"{dist_metrics['skewness']:+.2f}")

            st.markdown(f"""
            <div class="info-callout">
                <strong>💡 Distribution Insights:</strong>
                The distribution displays extreme <strong>positive (right) skewness ({dist_metrics['skewness']:+.2f})</strong>. 
                The parametric Mean (<strong>{dist_metrics['mean_mha']:,.2f} M ha</strong>) is over <strong>{dist_metrics['mean_mha'] / max(0.01, dist_metrics['median_mha']):.1f} times higher</strong> 
                than the non-parametric Median (<strong>{dist_metrics['median_mha']:,.2f} M ha</strong>), proving that a small handful of mega-forest nations pull the arithmetic average up dramatically. 
                For skewed ecological data, the <em>Median</em> and <em>Interquartile Range (IQR)</em> are the scientifically appropriate central tendency metrics.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # 3. Outlier Analysis (Tukey Boxplot)
        st.markdown("#### 3. Dispersion, Interquartile Range (IQR) & Outlier Analysis")
        fig_box = plot_forest_area_outliers_box(dist_metrics)
        st.plotly_chart(fig_box, use_container_width=True)

        if dist_metrics['is_valid']:
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            col_b1.metric("25th Percentile (Q1)", f"{dist_metrics['q25_mha']:,.2f} M ha")
            col_b2.metric("75th Percentile (Q3)", f"{dist_metrics['q75_mha']:,.2f} M ha")
            col_b3.metric("Interquartile Range (IQR)", f"{dist_metrics['iqr_mha']:,.2f} M ha")
            col_b4.metric("Upper Outlier Fence (Q3+1.5×IQR)", f"{dist_metrics['upper_fence_mha']:,.2f} M ha")

            with st.expander(f"🔍 View Identified Outlier Countries ({dist_metrics['outliers_count']} Nations with Forest Area > {dist_metrics['upper_fence_mha']:,.1f} M ha)"):
                st.dataframe(
                    dist_metrics['outliers_df'].rename(columns={'name': 'Country', 'regions': 'Region', 'forest_area_mha': f'Forest Area {stat_dist_year} (M ha)'}).style.format({
                        f'Forest Area {stat_dist_year} (M ha)': "{:,.2f}"
                    }),
                    use_container_width=True
                )

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # 4. Correlation Heatmap
        st.markdown("#### 4. Pearson Correlation Matrix of Validated Continuous Forest Indicators")
        st.write(
            "Excludes text identifiers (iso3, name), categorical codes, and data-flag columns (*_flag). "
            "Excludes constant zero-variance indicators and handles missing values safely through pairwise observation deletion without fabricating zeros."
        )

        all_valid_cand = [
            '1a_forestArea', '1a_landArea', '1a_otherWoodedLand', 
            '1b_naturallyRegeneratingForest', '1b_plantedForest', '1b_primary',
            '2a_gs_tot_forest', '2c_agb_total', '2c_bgb_total', '2d_carbon_agb_total',
            '3a_tot_biodiv', '3b_protected'
        ]
        
        selected_corr_keys = st.multiselect(
            "Select Numerical Indicators to Correlate:",
            options=all_valid_cand,
            default=['1a_forestArea', '1a_landArea', '1a_otherWoodedLand', '1b_naturallyRegeneratingForest', '1b_plantedForest', '1b_primary', '2a_gs_tot_forest', '2c_agb_total']
        )
        
        corr_matrix, _ = calculate_correlation_matrix(df_fra, year=selected_year, selected_keys=selected_corr_keys)
        fig_corr = plot_statistical_correlation_heatmap(corr_matrix)
        st.plotly_chart(fig_corr, use_container_width=True)

        st.markdown("""
        <div class="warning-callout">
            <strong>⚠️ Scientific Caution on Correlation:</strong>
            Strong statistical correlation (e.g. between <em>Forest Area</em> and <em>Naturally Regenerating Forest</em>, $r \approx 0.99$, 
            or between <em>Growing Stock</em> and <em>Above-Ground Biomass</em>, $r > 0.95$) reflects biophysical scaling relationships. 
            Correlation does <strong>not</strong> imply causality, nor does it establish environmental relationships with climate, rainfall, 
            or economic variables unless those specific covariates are explicitly present in the data.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 1.5rem 0;'>", unsafe_allow_html=True)

        # 5. Interval Rates Dynamics
        st.markdown("#### 5. Reporting Interval Dynamics: Annual Rates of Deforestation vs Expansion")
        fig_int = plot_interval_rates_comparison(df_intervals)
        st.plotly_chart(fig_int, use_container_width=True)
        int_summary_stats = get_interval_dynamics_summary(df_intervals)
        if not int_summary_stats['summary_table'].empty:
            st.dataframe(int_summary_stats['summary_table'], use_container_width=True)


    # --------------------------------------------------------------------------
    # TAB 3: COUNTRY FOREST PROFILE
    # --------------------------------------------------------------------------
    with tab_profile:
        st.markdown("### 🌲 Comprehensive Country Forest Profile Explorer")
        st.write(
            "Select any country or territory to inspect its complete multi-dataset record across FAO FRA reporting milestones, "
            "forest structural composition, intervals rates, qualitative degradation definitions, restoration commitments, "
            "Non-Wood Forest Products (NWFP), forest policy legislation, observation status flags, and data quality tiers."
        )

        all_countries_profile = sorted(df_fra['name'].dropna().unique().tolist())
        default_idx = 0
        preferred_defaults = ["Brazil", "Canada", "China", "India", "United States of America", "Democratic Republic of the Congo", "Russian Federation", "Indonesia"]
        if selected_country != "All Countries" and selected_country in all_countries_profile:
            default_idx = all_countries_profile.index(selected_country)
        else:
            for pref in preferred_defaults:
                if pref in all_countries_profile:
                    default_idx = all_countries_profile.index(pref)
                    break

        prof_country = st.selectbox(
            "Select Country / Territory to Profile:",
            options=all_countries_profile,
            index=default_idx,
            key='prof_country_picker'
        )

        profile = get_country_forest_profile(
            country_name=prof_country,
            df_fra=df_fra,
            df_intervals=df_intervals,
            df_deg=df_deg,
            df_rest=df_rest,
            df_pol=df_pol,
            df_nwfp=df_nwfp,
            df_tiers=df_tiers,
            start_year=baseline_year,
            end_year=selected_year
        )

        if profile['found']:
            # Country Hero Header
            st.markdown(f"""
            <div class="hero-container" style="padding: 1.5rem 1.8rem; margin-bottom: 1.5rem;">
                <h2 class="hero-title" style="font-size: 1.8rem;">{profile['name']}</h2>
                <div class="hero-subtitle" style="margin-bottom: 0.6rem;">Regional Allocation: <strong>{profile['region']}</strong> (Subregion: {profile['subregion']})</div>
                <div class="hero-meta-bar" style="padding-top: 0.5rem;">
                    <span class="meta-badge">🏷️ ISO3: {profile['iso3']}</span>
                    <span class="meta-badge">📅 Milestones: 1990–2025</span>
                    <span class="meta-badge">🌲 Forest Status Tier: {profile['tiers'].get('forest_area_status', 'Not reported')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Profile KPIs
            col_pk1, col_pk2, col_pk3, col_pk4 = st.columns(4)
            latest_s = profile.get('latest_sustainability', {})
            tot_f_disp = f"{latest_s.get('total_forest_mha'):,.2f} M ha" if latest_s.get('total_forest_mha') is not None else "Not reported"
            cov_disp = f"{latest_s.get('forest_cover_pct'):.1f}%" if latest_s.get('forest_cover_pct') is not None else "Not reported"
            nat_disp = f"{latest_s.get('natural_share_pct'):.1f}%" if latest_s.get('natural_share_pct') is not None else "Not reported"
            plant_disp = f"{latest_s.get('planted_share_pct'):.1f}%" if latest_s.get('planted_share_pct') is not None else "Not reported"

            col_pk1.metric(f"Total Forest ({latest_s.get('year', 2025)})", tot_f_disp)
            col_pk2.metric("Forest Cover (% of Land)", cov_disp)
            col_pk3.metric("Naturally Regenerating Share", nat_disp)
            col_pk4.metric("Planted Forest Share", plant_disp)

            col_prof_l, col_prof_r = st.columns([0.65, 0.35])
            with col_prof_l:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                fig_prof_trend = plot_country_profile_trend(profile)
                st.plotly_chart(fig_prof_trend, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_prof_r:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                fig_prof_donut = plot_country_natural_vs_planted_donut(profile)
                st.plotly_chart(fig_prof_donut, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Milestone Historical Table
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(f"#### 📅 Reported Milestone Observations for {profile['name']} (No Synthetic Interpolation)")
            if not profile['milestones_df'].empty:
                st.dataframe(profile['milestones_df'].fillna("-"), use_container_width=True)
            else:
                st.info("No milestone observations found.")
            st.markdown('</div>', unsafe_allow_html=True)

            # Selected Period Performance
            pchg = profile.get('period_change', {})
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(f"#### ⏱️ Selected Period Performance ({baseline_year} → {selected_year})")
            if pchg.get('is_available'):
                col_pc1, col_pc2, col_pc3, col_pc4 = st.columns(4)
                col_pc1.metric(f"Forest in {baseline_year}", f"{pchg['start_forest_mha']:,.2f} M ha")
                col_pc2.metric(f"Forest in {selected_year}", f"{pchg['end_forest_mha']:,.2f} M ha")
                col_pc3.metric("Net Period Change", f"{pchg['abs_change_mha']:+,.2f} M ha")
                pct_str = f"{pchg['pct_change']:+.2f}%" if pchg.get('pct_change') is not None else "N/A"
                col_pc4.metric("Relative Percentage Change", pct_str, f"{pchg['annual_rate_mha_yr']:+,.4f} M ha/yr")
            else:
                st.info(pchg.get('message', 'Period change not available.'))
            st.markdown('</div>', unsafe_allow_html=True)

            # Interval Rates for Country
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(f"#### 📊 Annual Change Rates Across Reporting Intervals (from Intervals_2026-10-16.csv)")
            if not profile['intervals_df'].empty:
                st.dataframe(profile['intervals_df'].fillna("Not reported"), use_container_width=True)
                st.caption("ℹ️ Units are expressed in 1,000 hectares per year (1,000 ha/yr).")
            else:
                st.info(f"No interval rate records reported for {profile['name']}.")
            st.markdown('</div>', unsafe_allow_html=True)

            # Four Profile Cards: Degradation, Restoration, NWFP, Policy
            col_card_1, col_card_2 = st.columns(2)
            with col_card_1:
                # Degradation
                deg = profile.get('degradation', {})
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("#### 🍂 Forest Degradation Monitoring")
                st.markdown(f"- **National Definition:** {deg.get('has_definition', 'Not reported')}")
                st.markdown(f"- **Definition Details:** {deg.get('definition_text', 'Not reported')}")
                st.markdown(f"- **Criteria Applied:** {deg.get('criteria', 'Not reported')}")
                st.markdown(f"- **Monitors Degradation:** {deg.get('monitors', 'Not reported')}")
                st.markdown(f"- **Methods Applied:** {deg.get('methods', 'Not reported')}")
                st.markdown(f"- **Monitoring Scale:** {deg.get('scale', 'Not reported')}")
                st.markdown(f"- **Latest Assessment Year:** {deg.get('assessment_year', 'Not reported')}")
                st.markdown(f"- **Degraded Forest Area Reported:** {deg.get('degraded_area_reported', 'Not reported')}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Non-Wood Forest Products
                nwfp_items = profile.get('nwfp_products', [])
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("#### 🍄 Top Non-Wood Forest Products (NWFP)")
                if nwfp_items:
                    st.dataframe(pd.DataFrame(nwfp_items), use_container_width=True)
                else:
                    st.info(f"No specific NWFP products reported for {profile['name']}.")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_card_2:
                # Restoration
                rest = profile.get('restoration', {})
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("#### 🌱 Forest Restoration Commitments")
                st.markdown(f"- **Formal Commitment:** {rest.get('commitment', 'Not reported')}")
                st.markdown(f"- **Legal Mandate:** {rest.get('law_mandate', 'Not reported')}")
                st.markdown(f"- **National Definition:** {rest.get('definition', 'Not reported')}")
                st.markdown(f"- **Areas in Need of Restoration:** {rest.get('areas_in_need', 'Not reported')}")
                st.markdown(f"- **Restoration Targets:** {rest.get('targets', 'Not reported')}")
                st.markdown(f"- **Hectares Restored to Date:** {rest.get('ha_restored', 'Not reported')}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Policy & Governance
                pol = profile.get('policy', {})
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown("#### 📜 Forest Governance & Policy Framework")
                st.markdown(f"- **National SFM Policy:** {pol.get('national_policy_sfm', 'Not reported')}")
                st.markdown(f"- **Sub-National SFM Policy:** {pol.get('subnational_policy_sfm', 'Not reported')}")
                st.markdown(f"- **National SFM Legislation:** {pol.get('national_legislation_sfm', 'Not reported')}")
                st.markdown(f"- **Stakeholder Participation Platform:** {pol.get('stakeholder_platform', 'Not reported')}")
                st.markdown(f"- **Wood Traceability System:** {pol.get('traceability_system', 'Not reported')}")
                st.markdown('</div>', unsafe_allow_html=True)

            # Tiers Confidence
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(f"#### 🏅 Data Confidence Tiers (from Tiers_2026-10-16.csv)")
            tiers = profile.get('tiers', {})
            col_t1, col_t2, col_t3, col_t4 = st.columns(4)
            col_t1.metric("Forest Area Status Tier", tiers.get('forest_area_status', 'Not reported'))
            col_t2.metric("Forest Area Trend Tier", tiers.get('forest_area_trend', 'Not reported'))
            col_t3.metric("Growing Stock Tier", tiers.get('growing_stock_status', 'Not reported'))
            col_t4.metric("Biomass Status Tier", tiers.get('biomass_status', 'Not reported'))
            st.markdown('</div>', unsafe_allow_html=True)


    # --------------------------------------------------------------------------
    # TAB 4: SUMMARY REPORT & DOWNLOADS
    # --------------------------------------------------------------------------
    with tab_export:
        st.markdown("### 📑 Downloadable Research Synthesis Report & Filtered Datasets")
        st.write(
            "Export tailored research artifacts, including a synthesized methodology and findings report, "
            "as well as filtered research tables in CSV format for offline statistical modeling and verification."
        )

        # Generate Synthesis Markdown Report
        report_findings = get_research_question_findings(df_fra, df_intervals, df_deg, df_rest, df_pol, df_tiers, baseline_year, selected_year, regions_filter)
        dist_export = get_statistical_distribution_metrics(df_fra, selected_year, regions_filter)
        reg_export = get_regional_comparison_metrics(df_fra, 1990, 2025)
        int_export = get_interval_dynamics_summary(df_intervals)

        summary_report_text = f"""# GLOBAL FOREST RESOURCES ASSESSMENT (FRA) RESEARCH SUMMARY REPORT
**Generated:** 2026-10-23
**Scope:** Stage 3: Research Insights, Statistical Analysis & Country Validation
**Data Source:** Food and Agriculture Organization of the United Nations (FAO FRA) Official Release (October 16, 2026)

---

## 1. Active Evaluation Scope & Filters
- **Geographic Filter:** Region: {selected_region} | Country: {selected_country}
- **Milestone Period:** Baseline: {baseline_year} → Target Year: {selected_year}
- **Countries Evaluated:** {kpis['countries_count']} Countries & Territories
- **Total Forest Area in {selected_year}:** {kpis['forest_area_display']}
- **Net Change ({baseline_year}→{selected_year}):** {kpis['change_display']} ({kpis['change_subtext']})

---

## 2. Answers to the 8 Core Research Questions

### Q1. Global Forest Area Change (1990–2025)
- **Formula:** ΔArea = Area_2025 - Area_1990; %Δ = (ΔArea / Area_1990) * 100
- **Empirical Finding:** {report_findings['Q1']['interpretation']}

### Q2. Countries with Largest Forest Areas (2025)
- **Formula:** Share % = (Country Area / Global Total Area) * 100
- **Empirical Finding:** {report_findings['Q2']['interpretation']}

### Q3. Largest Absolute Increases and Decreases ({baseline_year}→{selected_year})
- **Formula:** Absolute Change = Area_{selected_year} - Area_{baseline_year}
- **Empirical Finding:** {report_findings['Q3']['interpretation']}

### Q4. Forest Area Differences Across the Six FAO Regions
- **Formula:** Regional Total = Sum of Countries in Region; Cover % = Forest Area / Land Area * 100
- **Empirical Finding:** {report_findings['Q4']['interpretation']}

### Q5. Expansion, Afforestation and Deforestation Rates Across Intervals
- **Formula:** Annual Rate = Reported Interval Average (1,000 ha/year)
- **Empirical Finding:** {report_findings['Q5']['interpretation']}

### Q6. Naturally Regenerating vs. Planted Forests
- **Formula:** Naturally Regenerating Share % + Planted Forest Share % ≈ 100% (No Double Counting)
- **Empirical Finding:** {report_findings['Q6']['interpretation']}

### Q7. Completeness and Reliability of Observations
- **Formula:** Official Flag A % = Count(Flag A) / Total Nations * 100; Tier 3 High % = Count(Tier 3) / Total * 100
- **Empirical Finding:** {report_findings['Q7']['interpretation']}

### Q8. Forest Restoration and Policy Governance Indicators
- **Formula:** Adoption Rate % = Count(Indicator == 'Yes') / Total Evaluated * 100
- **Empirical Finding:** {report_findings['Q8']['interpretation']}

---

## 3. Parametric & Non-Parametric Distribution Statistics ({selected_year})
- **Count:** {dist_export.get('count', 0)} nations
- **Mean Area:** {dist_export.get('mean_mha', 0):,.2f} M ha
- **Median Area:** {dist_export.get('median_mha', 0):,.2f} M ha
- **Standard Deviation:** {dist_export.get('std_mha', 0):,.2f} M ha
- **Interquartile Range (IQR):** {dist_export.get('iqr_mha', 0):,.2f} M ha (Q1: {dist_export.get('q25_mha', 0):,.2f} M ha, Q3: {dist_export.get('q75_mha', 0):,.2f} M ha)
- **Tukey Upper Outlier Fence:** {dist_export.get('upper_fence_mha', 0):,.2f} M ha
- **Fisher-Pearson Skewness:** {dist_export.get('skewness', 0):+.2f} (Extreme right-skewness)

---

## 4. Scientific Methodology Caveats & Definitions
1. **Net Forest-Area Change vs. Gross Deforestation:** Net forest-area change is the algebraic sum of gross forest reduction, afforestation, and natural expansion. A net loss does not equal gross deforestation alone.
2. **Deforestation Definition:** Under FAO FRA, deforestation is the conversion of forest to other land use or long-term reduction of tree canopy cover below 10%. It does not include temporary canopy loss in forests managed for timber where regeneration occurs.
3. **Satellite Tree-Cover Loss Distinction:** Satellite-detected tree-cover loss (e.g. Global Forest Watch) measures annual canopy clearance irrespective of land-use change, including forestry harvesting and fires. FAO FRA measures legal and administrative land-use status.
4. **Data Reliability Flags & Tiers:** Tier 1 represents expert models and desk extrapolations; Tier 2 represents partial field inventories; Tier 3 represents wall-to-wall satellite remote sensing and national field sample inventories.
"""

        col_d_rep, _ = st.columns([0.4, 0.6])
        with col_d_rep:
            st.download_button(
                label="📥 Download Research Summary Report (.md)",
                data=summary_report_text,
                file_name=f"forest_research_summary_report_{selected_year}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with st.expander("📄 Preview Generated Research Summary Report"):
            st.markdown(summary_report_text)

        st.markdown("<hr style='border: 1px solid #ebf2ed; margin: 1.5rem 0;'>", unsafe_allow_html=True)

        st.markdown("#### 📊 Download Filtered Research Tables (CSV Format)")
        col_csv1, col_csv2, col_csv3, col_csv4 = st.columns(4)

        with col_csv1:
            if not reg_export.empty:
                csv_reg = reg_export.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Regional Dynamics CSV",
                    data=csv_reg,
                    file_name="regional_forest_dynamics_1990_2025.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        with col_csv2:
            if not int_export['summary_table'].empty:
                csv_int = int_export['summary_table'].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Interval Rates CSV",
                    data=csv_int,
                    file_name="reporting_intervals_annual_rates.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        with col_csv3:
            if not dist_export['outliers_df'].empty:
                csv_out = dist_export['outliers_df'].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Outlier Nations CSV",
                    data=csv_out,
                    file_name=f"forest_area_outliers_{selected_year}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        with col_csv4:
            if profile['found'] and not profile['milestones_df'].empty:
                csv_prof = profile['milestones_df'].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"📥 {profile['name']} Profile CSV",
                    data=csv_prof,
                    file_name=f"{profile['name'].replace(' ', '_')}_milestones.csv",
                    mime="text/csv",
                    use_container_width=True
                )


# 9. Footer
st.markdown("""
<div class="footer-bar">
    Global Forest Area Change and Forest Sustainability Analysis • College Data Visualization Project (Stage 3)<br>
    Data Source: Food and Agriculture Organization of the United Nations (FAO FRA) • Built with Python, Streamlit & Plotly
</div>
""", unsafe_allow_html=True)

