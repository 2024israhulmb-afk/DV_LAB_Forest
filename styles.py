"""
styles.py - Custom Design System and CSS for Forest Sustainability Dashboard
Defines color palette, typography, KPI cards, and responsive layout styles.
"""

def get_custom_css():
    """
    Returns custom CSS styles for the Streamlit dashboard.
    Employs an environmental forest theme:
    - Primary Accents: Deep Forest Green (#1b4332, #2d6a4f, #40916c)
    - Neutral Backgrounds: Off-white & soft mint (#f8faf8, #ffffff, #ebf2ed)
    - Alert & Status: Soft emerald for gains (#2d6a4f), muted coral for losses (#b91c1c)
    """
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #1b2e24;
    }

    /* Top banner / Hero Header */
    .hero-container {
        background: linear-gradient(135deg, #081c15 0%, #1b4332 50%, #2d6a4f 100%);
        color: #ffffff;
        padding: 2.2rem 2.2rem 1.8rem 2.2rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px rgba(27, 67, 50, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.12);
        position: relative;
        overflow: hidden;
    }

    .hero-container::after {
        content: "🌲";
        position: absolute;
        right: 25px;
        bottom: -15px;
        font-size: 8rem;
        opacity: 0.08;
        pointer-events: none;
    }

    .hero-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        font-size: 2.25rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        margin: 0 0 0.4rem 0;
        color: #ffffff !important;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        font-weight: 300;
        color: #d8f3dc;
        margin: 0 0 1.2rem 0;
        line-height: 1.5;
    }

    .hero-meta-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        align-items: center;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.15);
    }

    .meta-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(8px);
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        color: #e8f5e9;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* KPI Cards Styling */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.1rem;
        margin-bottom: 2rem;
    }

    .kpi-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        border: 1px solid #d8f3dc;
        box-shadow: 0 4px 14px rgba(27, 67, 50, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(27, 67, 50, 0.09);
        border-color: #74c69d;
    }

    .kpi-title {
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        color: #52796f;
        margin-bottom: 0.4rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }

    .kpi-value {
        font-family: 'Outfit', 'Inter', sans-serif;
        font-size: 1.95rem;
        font-weight: 700;
        color: #1b4332;
        line-height: 1.1;
        margin-bottom: 0.35rem;
    }

    .kpi-subtext {
        font-size: 0.82rem;
        color: #6c757d;
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }

    .kpi-trend-positive {
        color: #2d6a4f;
        background: #d8f3dc;
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.78rem;
        display: inline-block;
    }

    .kpi-trend-negative {
        color: #b91c1c;
        background: #fee2e2;
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.78rem;
        display: inline-block;
    }

    .kpi-trend-neutral {
        color: #4b5563;
        background: #f3f4f6;
        padding: 0.15rem 0.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.78rem;
        display: inline-block;
    }

    /* Section Card Wrappers */
    .section-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid #e2ece9;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.8rem;
    }

    .section-header {
        border-bottom: 2px solid #ebf2ed;
        padding-bottom: 0.75rem;
        margin-bottom: 1.25rem;
    }

    .section-title {
        font-family: 'Outfit', 'Inter', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #1b4332;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .section-desc {
        font-size: 0.88rem;
        color: #52796f;
        margin: 0.3rem 0 0 0;
    }

    /* Notice and Warning Callouts */
    .info-callout {
        background: #ebf5ee;
        border-left: 4px solid #2d6a4f;
        padding: 0.9rem 1.1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        color: #1b4332;
        margin-bottom: 1rem;
    }

    .warning-callout {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 0.9rem 1.1rem;
        border-radius: 0 8px 8px 0;
        font-size: 0.88rem;
        color: #92400e;
        margin-bottom: 1rem;
    }

    /* Sidebar Styling Tweaks */
    [data-testid="stSidebar"] {
        background-color: #f4f8f5;
        border-right: 1px solid #d8f3dc;
    }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #1b4332;
    }

    /* Footer styling */
    .footer-bar {
        text-align: center;
        padding: 1.8rem 0 1rem 0;
        color: #6c757d;
        font-size: 0.82rem;
        border-top: 1px solid #e2ece9;
        margin-top: 3rem;
    }
    </style>
    """

def render_header(title, subtitle, source, updated_date=None, country_count=236):
    """Generates the HTML banner for the top of the dashboard."""
    date_badge = f'<span class="meta-badge">📅 Dataset Release: {updated_date}</span>' if updated_date else ''
    
    return f"""
    <div class="hero-container">
        <h1 class="hero-title">{title}</h1>
        <div class="hero-subtitle">{subtitle}</div>
        <div class="hero-meta-bar">
            <span class="meta-badge">📊 Data Source: {source}</span>
            <span class="meta-badge">🌍 Coverage: {country_count} Countries & Territories</span>
            {date_badge}
            <span class="meta-badge">🔬 Stage 1: Baseline Architecture</span>
        </div>
    </div>
    """

def render_kpi_card(title, value, subtext="", trend=None, trend_positive=True):
    """
    Renders an HTML card for a single KPI.
    trend can be e.g. "+3.4%" or "-5.2%"
    trend_positive indicates if green or red styling should be applied.
    """
    trend_html = ""
    if trend:
        if trend == "Not available" or trend == "N/A":
            trend_html = f'<span class="kpi-trend-neutral">{trend}</span>'
        elif trend_positive:
            trend_html = f'<span class="kpi-trend-positive">{trend}</span>'
        else:
            trend_html = f'<span class="kpi-trend-negative">{trend}</span>'

    return f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-subtext">
            {trend_html}
            <span>{subtext}</span>
        </div>
    </div>
    """
