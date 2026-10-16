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
    get_cross_topic_synthesis
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
    plot_cross_topic_scatter
)

# 3. Inject Custom CSS Stylesheet
st.markdown(get_custom_css(), unsafe_allow_html=True)

# 4. Data Loading with Graceful Fallback
try:
    df_fra = load_fra_years()
except Exception as e:
    st.error(f"Error loading core FRA dataset: {e}")
    df_fra = pd.DataFrame()

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
            "📋 Data Quality & Diagnostics"
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

# 9. Footer
st.markdown("""
<div class="footer-bar">
    Global Forest Area Change and Forest Sustainability Analysis • College Data Visualization Project (Stage 2)<br>
    Data Source: Food and Agriculture Organization of the United Nations (FAO FRA) • Built with Python, Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
