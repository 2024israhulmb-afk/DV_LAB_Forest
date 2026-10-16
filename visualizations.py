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
