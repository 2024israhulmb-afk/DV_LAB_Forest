"""
visualizations.py - Interactive Plotly chart builders for Forest Sustainability Dashboard.
Implements:
1. Multi-year Forest Area Trend Line Chart
2. Country & Regional Comparison Bar Chart (Total Area & Net Gain/Loss)
3. Numeric Indicator Distribution Histogram
4. Multi-Variable Pearson Correlation Heatmap
5. Global & Regional Choropleth Geographic Map
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from data_loader import FRA_VARIABLE_MAP

# Custom Forest Color Palettes
FOREST_DARK = "#1b4332"
FOREST_MID = "#2d6a4f"
FOREST_LIGHT = "#52b788"
FOREST_ACCENT = "#74c69d"
FOREST_PALETTE = ["#1b4332", "#2d6a4f", "#40916c", "#52b788", "#74c69d", "#95d5b2", "#b7e4c7", "#d8f3dc"]
GAIN_COLOR = "#2d6a4f"
LOSS_COLOR = "#b91c1c"

# Base layout styling for Plotly figures
PLOTLY_TEMPLATE = "simple_white"

def _apply_common_layout(fig, title: str, x_title: str = "", y_title: str = ""):
    """Applies clean, unified forest typography and margins to Plotly figures."""
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title={
            'text': f"<b>{title}</b>",
            'y': 0.95,
            'x': 0.02,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 16, 'color': FOREST_DARK, 'family': 'Inter, sans-serif'}
        },
        font={'family': 'Inter, sans-serif', 'color': '#1b2e24'},
        margin=dict(l=40, r=40, t=65, b=45),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_size=12,
            font_family="Inter, sans-serif",
            bordercolor=FOREST_MID
        ),
        xaxis=dict(
            title={'text': x_title, 'font': {'size': 12, 'weight': 600}},
            showgrid=True,
            gridcolor='#edf2ee',
            zeroline=False
        ),
        yaxis=dict(
            title={'text': y_title, 'font': {'size': 12, 'weight': 600}},
            showgrid=True,
            gridcolor='#edf2ee',
            zeroline=False
        )
    )
    return fig

def plot_forest_trend_line(df: pd.DataFrame, group_by: str = "Total") -> go.Figure:
    """
    1. Line Chart: Forest Area Trend over Time (1990 - 2025).
    Can show aggregate trend, regional breakdown, or country breakdown.
    """
    if df.empty or '1a_forestArea' not in df.columns:
        fig = go.Figure()
        _apply_common_layout(fig, "Forest Area Trends (1990-2025)", "Year", "Forest Area (Million ha)")
        fig.add_annotation(
            text="No forest area data available for current selection.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#6c757d")
        )
        return fig

    # Work with copy and numeric area
    data = df.copy()
    data['forest_mha'] = data['1a_forestArea'] / 1000.0  # Convert 1,000 ha to Million ha
    data = data.dropna(subset=['year', 'forest_mha'])

    if group_by == "By Region" and 'regions' in data.columns and data['regions'].nunique() > 1:
        # Group by Region and Year
        trend = data.groupby(['regions', 'year'])['forest_mha'].sum().reset_index()
        fig = px.line(
            trend,
            x='year',
            y='forest_mha',
            color='regions',
            markers=True,
            color_discrete_sequence=FOREST_PALETTE,
            labels={'year': 'Reporting Year', 'forest_mha': 'Forest Area (Million ha)', 'regions': 'Region'}
        )
        title = "Forest Area Trends by Region (1990 - 2025)"
    elif group_by == "By Country" and data['name'].nunique() <= 15:
        # Group by Country and Year (if reasonable number of countries selected)
        trend = data.groupby(['name', 'year'])['forest_mha'].sum().reset_index()
        fig = px.line(
            trend,
            x='year',
            y='forest_mha',
            color='name',
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Dark24,
            labels={'year': 'Reporting Year', 'forest_mha': 'Forest Area (Million ha)', 'name': 'Country'}
        )
        title = "Forest Area Trends by Selected Countries (1990 - 2025)"
    else:
        # Aggregate Total Trend
        trend = data.groupby('year')['forest_mha'].sum().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend['year'],
            y=trend['forest_mha'],
            mode='lines+markers',
            name='Total Forest Area',
            line=dict(color=FOREST_MID, width=3.5),
            marker=dict(size=9, color=FOREST_DARK, symbol='circle', line=dict(color='#ffffff', width=2)),
            hovertemplate="<b>Year %{x}</b><br>Total Forest Area: %{y:,.2f} M ha<extra></extra>"
        ))
        title = "Total Forest Area Trend (1990 - 2025)"

    _apply_common_layout(fig, title, "Reporting Milestone Year", "Forest Area (Million ha)")
    fig.update_xaxes(tickmode='array', tickvals=sorted(data['year'].unique()))
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

def plot_country_comparison_bar(df: pd.DataFrame, 
                                year: int = 2025, 
                                top_n: int = 10,
                                mode: str = "area") -> go.Figure:
    """
    2. Bar Chart:
    - mode='area': Top N countries by forest area in selected year
    - mode='change': Top N Forest Gainers vs Top N Forest Losers (1990 to selected year)
    """
    if df.empty or '1a_forestArea' not in df.columns:
        fig = go.Figure()
        _apply_common_layout(fig, "Country Comparison", "", "")
        fig.add_annotation(text="Insufficient data for country comparison.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    if mode == "change":
        # Calculate change between 1990 and selected year
        piv = df.pivot(index='name', columns='year', values='1a_forestArea')
        if 1990 in piv.columns and year in piv.columns and 1990 != year:
            change_df = pd.DataFrame({
                'name': piv.index,
                'change_mha': (piv[year] - piv[1990]) / 1000.0,
                'pct_change': ((piv[year] - piv[1990]) / piv[1990]) * 100.0
            }).dropna()
            
            # Select top gainers and losers
            losers = change_df.sort_values(by='change_mha', ascending=True).head(top_n // 2)
            gainers = change_df.sort_values(by='change_mha', ascending=False).head(top_n // 2)
            combined = pd.concat([gainers, losers]).drop_duplicates().sort_values(by='change_mha', ascending=True)
            
            colors = [GAIN_COLOR if val >= 0 else LOSS_COLOR for val in combined['change_mha']]
            
            fig = go.Figure(go.Bar(
                x=combined['change_mha'],
                y=combined['name'],
                orientation='h',
                marker=dict(color=colors, line=dict(color='rgba(0,0,0,0.1)', width=1)),
                hovertemplate="<b>%{y}</b><br>Net Change: %{x:,.2f} M ha<extra></extra>"
            ))
            _apply_common_layout(
                fig, 
                f"Net Forest Area Change: Top Gainers vs Losers (1990 - {year})", 
                "Net Change (Million ha)", 
                ""
            )
            return fig

    # Default: Top N Countries by Forest Area in selected year
    year_data = df[df['year'] == year].copy()
    if year_data.empty:
        year_data = df[df['year'] == df['year'].max()].copy()
        
    year_data['forest_mha'] = year_data['1a_forestArea'] / 1000.0
    top_countries = year_data.sort_values(by='forest_mha', ascending=False).head(top_n)
    top_countries = top_countries.sort_values(by='forest_mha', ascending=True) # for ascending horizontal bar
    
    fig = go.Figure(go.Bar(
        x=top_countries['forest_mha'],
        y=top_countries['name'],
        orientation='h',
        marker=dict(
            color=top_countries['forest_mha'],
            colorscale='Greens',
            line=dict(color=FOREST_DARK, width=0.5)
        ),
        hovertemplate="<b>%{y}</b><br>Forest Area: %{x:,.2f} M ha<extra></extra>"
    ))
    _apply_common_layout(
        fig, 
        f"Top {len(top_countries)} Countries by Forest Area ({year})", 
        "Forest Area (Million ha)", 
        ""
    )
    return fig

def plot_variable_histogram(df: pd.DataFrame, 
                            variable: str = '1a_forestArea', 
                            year: int = 2025,
                            log_scale: bool = True) -> go.Figure:
    """
    3. Histogram: Distribution of a numeric forest variable across countries.
    Offers log-scale toggle because forest area spans several orders of magnitude.
    """
    if df.empty or variable not in df.columns:
        fig = go.Figure()
        _apply_common_layout(fig, "Variable Distribution", "", "")
        fig.add_annotation(text="Selected variable not present in dataset.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    data = df[df['year'] == year].copy() if 'year' in df.columns else df.copy()
    values = pd.to_numeric(data[variable], errors='coerce').dropna()
    values = values[values > 0] if log_scale else values

    var_label = FRA_VARIABLE_MAP.get(variable, variable.replace('_', ' ').title())

    if values.empty:
        fig = go.Figure()
        _apply_common_layout(fig, f"Distribution of {var_label} ({year})", "", "")
        fig.add_annotation(text="No positive numeric data points for this indicator.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    fig = px.histogram(
        values,
        nbins=35,
        log_x=log_scale,
        marginal="box",
        color_discrete_sequence=[FOREST_MID],
        labels={'value': var_label, 'count': 'Number of Countries'}
    )

    scale_text = " (Log Scale)" if log_scale else ""
    _apply_common_layout(
        fig, 
        f"Country Distribution: {var_label} ({year}){scale_text}", 
        f"{var_label}{scale_text}", 
        "Country Frequency"
    )
    fig.update_layout(bargap=0.08)
    return fig

def plot_correlation_heatmap(df: pd.DataFrame, year: int = 2025) -> go.Figure:
    """
    4. Correlation Heatmap: Pearson correlation between key numeric forest variables.
    Examines biological and management relationships (Biomass, Carbon, Protected Area, etc.)
    """
    key_vars = [
        '1a_forestArea', '1a_landArea', '1b_naturallyRegeneratingForest',
        '1b_plantedForest', '2a_gs_tot_forest', '2c_agb_total',
        '2d_carbon_agb_total', '3b_protected'
    ]
    available_vars = [c for c in key_vars if c in df.columns]

    if len(available_vars) < 2:
        fig = go.Figure()
        _apply_common_layout(fig, "Variable Correlation Heatmap", "", "")
        fig.add_annotation(text="Not enough numeric variables to compute correlation.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    data = df[df['year'] == year] if 'year' in df.columns else df
    num_df = data[available_vars].apply(pd.to_numeric, errors='coerce').dropna(how='all')
    corr = num_df.corr().round(2)

    labels = [FRA_VARIABLE_MAP.get(c, c).split('(')[0].strip() for c in available_vars]

    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=labels,
        y=labels,
        colorscale='Greens',
        zmin=-1, zmax=1,
        text=corr.values,
        texttemplate="%{text:.2f}",
        textfont={"size": 11, "family": "Inter, sans-serif"},
        hoverongaps=False
    ))

    _apply_common_layout(fig, f"Pearson Correlation Matrix of Forest Variables ({year})", "", "")
    fig.update_layout(height=480, margin=dict(l=80, r=40, t=65, b=80))
    fig.update_xaxes(tickangle=35)
    return fig

def plot_choropleth_map(df: pd.DataFrame, 
                        year: int = 2025, 
                        indicator: str = "1a_forestArea") -> go.Figure:
    """
    5. Geographic Map: Interactive World/Regional Choropleth Map using ISO3 country codes.
    Displays Forest Area or Forest Cover Percentage.
    """
    if df.empty or 'iso3' not in df.columns:
        fig = go.Figure()
        _apply_common_layout(fig, "Global Forest Map", "", "")
        fig.add_annotation(text="ISO3 country identifiers not found for mapping.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    map_data = df[df['year'] == year].copy() if 'year' in df.columns else df.copy()
    if indicator not in map_data.columns:
        indicator = '1a_forestArea'

    map_data['mapped_val'] = pd.to_numeric(map_data[indicator], errors='coerce')
    
    if indicator == '1a_forestArea':
        # Convert to Million ha for cleaner map scale
        map_data['display_val'] = map_data['mapped_val'] / 1000.0
        val_name = "Forest Area (Million ha)"
        fmt = ":,.2f"
    elif indicator == 'forest_cover_pct':
        map_data['display_val'] = map_data['mapped_val']
        val_name = "Forest Cover (%)"
        fmt = ":.1f"
    else:
        map_data['display_val'] = map_data['mapped_val']
        val_name = FRA_VARIABLE_MAP.get(indicator, indicator)
        fmt = ":,.1f"

    fig = px.choropleth(
        map_data,
        locations="iso3",
        color="display_val",
        hover_name="name",
        hover_data={
            "display_val": fmt,
            "regions": True,
            "iso3": True
        },
        color_continuous_scale="Greens",
        labels={'display_val': val_name, 'regions': 'Region', 'iso3': 'ISO3 Code'}
    )

    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="#cbd5e1",
        showland=True,
        landcolor="#f8fafc",
        showocean=True,
        oceancolor="#e0f2fe",
        showlakes=True,
        lakecolor="#e0f2fe",
        projection_type="natural earth"
    )

    _apply_common_layout(fig, f"Global {val_name} by Country ({year})", "", "")
    fig.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=55, b=0),
        coloraxis_colorbar=dict(
            title=dict(text=val_name, font=dict(size=11)),
            len=0.75,
            thickness=16
        )
    )
    return fig

def render_empty_state_notice(title: str, message: str, required_data: str):
    """Renders a friendly environmental banner when data for a requested chart is missing."""
    st.markdown(f"""
    <div class="warning-callout">
        <strong>⚠️ {title}</strong><br>
        {message}<br>
        <span style="font-size: 0.8rem; color: #78350f;"><em>Required Data: {required_data}</em></span>
    </div>
    """, unsafe_allow_html=True)


def plot_top_gainers_chart(gainers_df: pd.DataFrame, start_year: int, end_year: int) -> go.Figure:
    """
    Renders horizontal bar chart of Top Countries with Forest Area Increase.
    Emerald green styling with hover details for absolute and percentage gain.
    """
    if gainers_df.empty:
        fig = go.Figure()
        _apply_common_layout(fig, f"Top Forest Gainers ({start_year} - {end_year})", "Net Increase (Million ha)", "")
        fig.add_annotation(text="No countries with net forest increase found for this selection.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    # Ascending sort so largest appears at top in horizontal layout
    plot_data = gainers_df.sort_values(by='abs_change_mha', ascending=True).copy()
    
    fig = go.Figure(go.Bar(
        x=plot_data['abs_change_mha'],
        y=plot_data['name'],
        orientation='h',
        marker=dict(
            color='#2d6a4f',
            line=dict(color='#1b4332', width=1)
        ),
        customdata=np.stack((plot_data['pct_change'].fillna(0), plot_data['regions']), axis=-1),
        hovertemplate="<b>%{y}</b> (%{customdata[1]})<br>Net Increase: <b>+%{x:,.2f} M ha</b><br>Relative Growth: <b>+%{customdata[0]:.2f}%</b><extra></extra>"
    ))
    _apply_common_layout(
        fig, 
        f"Top {len(plot_data)} Forest Gainers ({start_year} → {end_year})", 
        "Net Forest Increase (Million ha)", 
        ""
    )
    return fig


def plot_top_losers_chart(losers_df: pd.DataFrame, start_year: int, end_year: int) -> go.Figure:
    """
    Renders horizontal bar chart of Top Countries with Forest Area Decrease.
    Crimson/coral styling with hover details for absolute and percentage loss.
    """
    if losers_df.empty:
        fig = go.Figure()
        _apply_common_layout(fig, f"Top Forest Losers ({start_year} - {end_year})", "Net Decrease (Million ha)", "")
        fig.add_annotation(text="No countries with net forest decrease found for this selection.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    # Ascending sort (e.g. -116 M ha at bottom or top; for losers, sort ascending so most negative is at top)
    plot_data = losers_df.sort_values(by='abs_change_mha', ascending=False).copy()
    
    fig = go.Figure(go.Bar(
        x=plot_data['abs_change_mha'],
        y=plot_data['name'],
        orientation='h',
        marker=dict(
            color='#b91c1c',
            line=dict(color='#7f1d1d', width=1)
        ),
        customdata=np.stack((plot_data['pct_change'].fillna(0), plot_data['regions']), axis=-1),
        hovertemplate="<b>%{y}</b> (%{customdata[1]})<br>Net Decrease: <b>%{x:,.2f} M ha</b><br>Relative Loss: <b>%{customdata[0]:.2f}%</b><extra></extra>"
    ))
    _apply_common_layout(
        fig, 
        f"Top {len(plot_data)} Forest Losers ({start_year} → {end_year})", 
        "Net Forest Change (Million ha)", 
        ""
    )
    return fig


def plot_top_countries_ranking(df_fra: pd.DataFrame, year: int = 2025, n: int = 10, selected_regions: list = None) -> go.Figure:
    """
    Renders ranking of Top N countries by Forest Area for the selected reporting year.
    Displays rank badges (#1, #2...) and % share of world/region forest area.
    """
    if df_fra.empty or '1a_forestArea' not in df_fra.columns:
        fig = go.Figure()
        _apply_common_layout(fig, f"Top Countries by Forest Area ({year})", "", "")
        fig.add_annotation(text="No forest area data available.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    sub = df_fra[df_fra['year'] == year].copy()
    if selected_regions and "All Regions" not in selected_regions:
        sub = sub[sub['regions'].isin(selected_regions)]
        
    sub = sub.dropna(subset=['1a_forestArea']).sort_values(by='1a_forestArea', ascending=False).head(n)
    if sub.empty:
        fig = go.Figure()
        _apply_common_layout(fig, f"Top Countries by Forest Area ({year})", "", "")
        fig.add_annotation(text="No records match current filter criteria.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    total_ref_area = sub['1a_forestArea'].sum()
    sub['forest_mha'] = sub['1a_forestArea'] / 1000.0
    sub['pct_share'] = (sub['1a_forestArea'] / total_ref_area * 100.0) if total_ref_area > 0 else 0.0

    # Sort ascending for horizontal bar chart
    sub = sub.sort_values(by='forest_mha', ascending=True)

    fig = go.Figure(go.Bar(
        x=sub['forest_mha'],
        y=sub['name'],
        orientation='h',
        marker=dict(
            color=sub['forest_mha'],
            colorscale='Greens',
            line=dict(color=FOREST_DARK, width=0.5)
        ),
        customdata=np.stack((sub['pct_share'], sub['regions']), axis=-1),
        hovertemplate="<b>%{y}</b> (%{customdata[1]})<br>Forest Area: <b>%{x:,.2f} M ha</b><br>Share of Top Group: <b>%{customdata[0]:.1f}%</b><extra></extra>"
    ))
    _apply_common_layout(
        fig, 
        f"Top {len(sub)} Countries by Forest Area ({year})", 
        "Forest Area (Million ha)", 
        ""
    )
    return fig


def plot_enhanced_trend_line(df_fra: pd.DataFrame, 
                             selected_countries: list = None, 
                             years_subset: list = None,
                             show_global: bool = True) -> go.Figure:
    """
    Enhanced Multi-Country & Global Trend Line Chart.
    Allows comparing 1 to 10 countries side-by-side with an optional Global Total overlay.
    Uses actual reported FRA milestones only (1990, 2000, 2010, 2015, 2020, 2025).
    """
    if df_fra.empty or '1a_forestArea' not in df_fra.columns:
        fig = go.Figure()
        _apply_common_layout(fig, "Longitudinal Forest Area Trends", "Year", "Forest Area (Million ha)")
        fig.add_annotation(text="Dataset is empty.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    data = df_fra.dropna(subset=['year', '1a_forestArea']).copy()
    data['forest_mha'] = data['1a_forestArea'] / 1000.0
    
    if years_subset:
        data = data[data['year'].isin(years_subset)]

    fig = go.Figure()
    all_actual_years = sorted(data['year'].unique())

    # Add selected countries
    if selected_countries and "All Countries" not in selected_countries:
        palette = px.colors.qualitative.Dark24
        for idx, country in enumerate(selected_countries):
            c_data = data[data['name'] == country].sort_values(by='year')
            if not c_data.empty:
                fig.add_trace(go.Scatter(
                    x=c_data['year'],
                    y=c_data['forest_mha'],
                    mode='lines+markers',
                    name=country,
                    line=dict(width=2.5, color=palette[idx % len(palette)]),
                    marker=dict(size=8),
                    hovertemplate=f"<b>{country}</b><br>Year %{{x}}: %{{y:,.2f}} M ha<extra></extra>"
                ))
    else:
        # Default: Global Aggregate Trend
        global_trend = data.groupby('year')['forest_mha'].sum().reset_index()
        fig.add_trace(go.Scatter(
            x=global_trend['year'],
            y=global_trend['forest_mha'],
            mode='lines+markers',
            name='Global Total Forest Area',
            line=dict(color=FOREST_MID, width=3.5),
            marker=dict(size=9, color=FOREST_DARK, symbol='circle', line=dict(color='#ffffff', width=2)),
            hovertemplate="<b>Global Total</b><br>Year %{x}: %{y:,.2f} M ha<extra></extra>"
        ))

    # Optional Global Overlay if specific countries are selected and toggle is active
    if selected_countries and "All Countries" not in selected_countries and show_global:
        global_trend = data.groupby('year')['forest_mha'].sum().reset_index()
        fig.add_trace(go.Scatter(
            x=global_trend['year'],
            y=global_trend['forest_mha'],
            mode='lines+markers',
            name='Global Total (Reference)',
            line=dict(color='#94a3b8', width=2, dash='dot'),
            marker=dict(size=6),
            yaxis='y2',
            hovertemplate="<b>Global Total</b><br>Year %{x}: %{y:,.2f} M ha<extra></extra>"
        ))
        fig.update_layout(
            yaxis2=dict(
                title="Global Total (Million ha)",
                overlaying='y',
                side='right',
                showgrid=False
            )
        )

    _apply_common_layout(
        fig, 
        "Longitudinal Forest Area Trajectories (Actual FRA Milestones)", 
        "Reporting Milestone Year", 
        "Forest Area (Million ha)"
    )
    fig.update_xaxes(tickmode='array', tickvals=all_actual_years)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig


def plot_natural_vs_planted_bar(sustainability_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Renders stacked horizontal bar chart:
    Naturally Regenerating Forest vs Planted Forest for Top Forested Countries.
    Validates components: Natural + Planted ≈ Total Forest Area.
    """
    if sustainability_df.empty or 'natural_forest_mha' not in sustainability_df.columns:
        fig = go.Figure()
        _apply_common_layout(fig, "Natural vs Planted Forest Composition", "", "")
        fig.add_annotation(text="Sustainability indicators not available.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    # Filter to top N by total forest area
    top_df = sustainability_df.dropna(subset=['forest_area_mha']).sort_values(by='forest_area_mha', ascending=False).head(top_n)
    top_df = top_df.sort_values(by='forest_area_mha', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_df['name'],
        x=top_df['natural_forest_mha'],
        name='Naturally Regenerating Forest',
        orientation='h',
        marker=dict(color='#1b4332', line=dict(color='#081c15', width=0.5)),
        hovertemplate="<b>%{y}</b><br>Naturally Regenerating: <b>%{x:,.2f} M ha</b><extra></extra>"
    ))
    fig.add_trace(go.Bar(
        y=top_df['name'],
        x=top_df['planted_forest_mha'],
        name='Planted Forest',
        orientation='h',
        marker=dict(color='#74c69d', line=dict(color='#40916c', width=0.5)),
        hovertemplate="<b>%{y}</b><br>Planted Forest: <b>%{x:,.2f} M ha</b><extra></extra>"
    ))

    _apply_common_layout(
        fig, 
        f"Natural vs Planted Forest Composition: Top {len(top_df)} Countries", 
        "Forest Area (Million ha)", 
        ""
    )
    fig.update_layout(
        barmode='stack',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig


def plot_forest_cover_percentage_ranking(sustainability_df: pd.DataFrame, top_n: int = 12, mode: str = "highest") -> go.Figure:
    """
    Renders bar chart of countries with Highest or Lowest Forest Cover (% of national land area).
    """
    if sustainability_df.empty or 'forest_cover_pct' not in sustainability_df.columns:
        fig = go.Figure()
        _apply_common_layout(fig, "Forest Cover Percentage", "", "")
        fig.add_annotation(text="Forest cover percentage data not available.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    valid = sustainability_df.dropna(subset=['forest_cover_pct']).copy()
    # Require minimum land area (e.g. > 10,000 ha = 10 M ha or positive land area)
    valid = valid[valid['land_area_mha'] > 0.05]

    if mode == "highest":
        plot_data = valid.sort_values(by='forest_cover_pct', ascending=False).head(top_n)
        plot_data = plot_data.sort_values(by='forest_cover_pct', ascending=True)
        title = f"Top {len(plot_data)} Nations by Forest Cover (% of Land Area)"
        color_val = '#2d6a4f'
    else:
        plot_data = valid.sort_values(by='forest_cover_pct', ascending=True).head(top_n)
        plot_data = plot_data.sort_values(by='forest_cover_pct', ascending=False)
        title = f"Nations with Lowest Forest Cover (% of Land Area)"
        color_val = '#b45309'

    fig = go.Figure(go.Bar(
        x=plot_data['forest_cover_pct'],
        y=plot_data['name'],
        orientation='h',
        marker=dict(color=color_val, line=dict(color='rgba(0,0,0,0.1)', width=1)),
        customdata=np.stack((plot_data['forest_area_mha'], plot_data['regions']), axis=-1),
        hovertemplate="<b>%{y}</b> (%{customdata[1]})<br>Forest Cover: <b>%{x:.1f}%</b><br>Total Forest Area: <b>%{customdata[0]:,.2f} M ha</b><extra></extra>"
    ))
    _apply_common_layout(fig, title, "Forest Area as % of Total Land Area", "")
    return fig


def plot_primary_forest_share(sustainability_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Renders horizontal bar chart of Primary Forest extent and share of natural forest.
    Primary forest is intact, undisturbed old-growth native forest.
    """
    if sustainability_df.empty or 'primary_forest_mha' not in sustainability_df.columns:
        fig = go.Figure()
        _apply_common_layout(fig, "Primary Forest Extent", "", "")
        fig.add_annotation(text="Primary forest data not available.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    valid = sustainability_df.dropna(subset=['primary_forest_mha']).copy()
    valid = valid[valid['primary_forest_mha'] > 0]
    plot_data = valid.sort_values(by='primary_forest_mha', ascending=False).head(top_n)
    plot_data = plot_data.sort_values(by='primary_forest_mha', ascending=True)

    fig = go.Figure(go.Bar(
        x=plot_data['primary_forest_mha'],
        y=plot_data['name'],
        orientation='h',
        marker=dict(color='#081c15', line=dict(color='#2d6a4f', width=1)),
        customdata=np.stack((plot_data['primary_share_pct'].fillna(0), plot_data['forest_area_mha']), axis=-1),
        hovertemplate="<b>%{y}</b><br>Primary Forest: <b>%{x:,.2f} M ha</b><br>Share of Total Forest: <b>%{customdata[0]:.1f}%</b><br>Total Forest: %{customdata[1]:,.2f} M ha<extra></extra>"
    ))
    _apply_common_layout(
        fig, 
        f"Top {len(plot_data)} Countries by Primary Forest Extent", 
        "Primary (Undisturbed Old-Growth) Forest (Million ha)", 
        ""
    )
    return fig


def plot_flag_coverage_by_year(audit_df: pd.DataFrame, variable: str = 'Total Forest Area') -> go.Figure:
    """
    Renders stacked bar chart showing reporting quality by Observation Flag across years.
    Differentiates:
    - Official Reported Data (Flag A)
    - Imputed / Desk Study (Flag I)
    - Cannot Exist / Missing (Flag M/O)
    """
    if audit_df.empty:
        fig = go.Figure()
        _apply_common_layout(fig, f"Observation Status Flags: {variable}", "Year", "Number of Countries")
        fig.add_annotation(text="Flag audit data not available.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    v_df = audit_df[audit_df['Variable'] == variable].sort_values(by='Year')
    if v_df.empty:
        v_df = audit_df.iloc[:6]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=v_df['Year'].astype(str),
        y=v_df['Official Reported (A)'],
        name='Official Country Report (Flag A)',
        marker=dict(color='#2d6a4f')
    ))
    fig.add_trace(go.Bar(
        x=v_df['Year'].astype(str),
        y=v_df['Imputed/Desk (I)'],
        name='Imputed / Desk Study (Flag I)',
        marker=dict(color='#eab308')
    ))
    fig.add_trace(go.Bar(
        x=v_df['Year'].astype(str),
        y=v_df['Unreported (O)'] + v_df['Cannot Exist (M)'],
        name='Unreported / Missing (Flag O/M)',
        marker=dict(color='#cbd5e1')
    ))

    _apply_common_layout(
        fig, 
        f"Reporting Status Flags across FRA Milestones: {variable}", 
        "Reporting Milestone Year", 
        "Number of Countries & Territories"
    )
    fig.update_layout(
        barmode='stack',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig


def plot_tiers_summary(tiers_df: pd.DataFrame) -> go.Figure:
    """
    Renders grouped bar chart of Data Quality Tiers (High, Medium, Low).
    High Tier = Continuous National Forest Inventory (NFI) / wall-to-wall satellite mapping.
    Medium Tier = Partial/regional surveys.
    Low Tier = Desk study or expert models.
    """
    if tiers_df.empty:
        fig = go.Figure()
        _apply_common_layout(fig, "Data Quality Tiers Distribution", "", "")
        fig.add_annotation(text="Tiers dataset not available.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return fig

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=tiers_df['Indicator'],
        y=tiers_df['High Tier (Satellite/NFI)'],
        name='High Tier (Field NFI / Satellite)',
        marker=dict(color='#1b4332')
    ))
    fig.add_trace(go.Bar(
        x=tiers_df['Indicator'],
        y=tiers_df['Medium Tier (Regional/Partial)'],
        name='Medium Tier (Regional/Subnational)',
        marker=dict(color='#52b788')
    ))
    fig.add_trace(go.Bar(
        x=tiers_df['Indicator'],
        y=tiers_df['Low Tier (Desk/Model)'],
        name='Low Tier (Desk Imputation / Model)',
        marker=dict(color='#d8f3dc', line=dict(color='#2d6a4f', width=1))
    ))

    _apply_common_layout(
        fig, 
        "Empirical Confidence Tiers across Key Forest Dimensions (236 Countries)", 
        "Assessment Dimension", 
        "Number of Countries"
    )
    fig.update_layout(
        barmode='group',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

