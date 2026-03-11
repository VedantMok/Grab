from pathlib import Path
import pandas as pd
import numpy as np
import altair as alt
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Grab Executive Dashboard", page_icon="🟢", layout="wide", initial_sidebar_state="collapsed")
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = "grab_superapp_synthetic.csv"

GRAB_GREEN = "#00B14F"
GRAB_GREEN_DARK = "#0B6B3A"
GRAB_GREEN_SOFT = "#EAF8F0"
GRAB_TEXT = "#143524"
GRAB_BORDER = "#DCEEE3"
BG = "#F7FBF8"
CARD = "#FFFFFF"
TEAL = "#0EA5A4"
AMBER = "#F59E0B"
RED = "#E5484D"
GRAY = "#6B7C72"

st.markdown(f"""
<style>
.stApp {{background:{BG}; color:{GRAB_TEXT};}}
.block-container {{padding-top:1rem; padding-bottom:1.4rem; max-width:95%;}}
[data-testid="stSidebar"] {{display:none;}}
header[data-testid="stHeader"] {{background:transparent;}}
.main-title {{background:#fff; border:1px solid {GRAB_BORDER}; border-radius:18px; padding:1rem 1.15rem; margin-bottom:.9rem; box-shadow:0 6px 18px rgba(0,0,0,.03);}}
.main-title h1 {{margin:0; font-size:1.85rem; color:{GRAB_TEXT};}}
.main-title p {{margin:.25rem 0 0 0; color:#587262; font-size:.92rem;}}
.metric-card {{background:{CARD}; border:1px solid {GRAB_BORDER}; border-radius:16px; padding:.9rem 1rem; box-shadow:0 6px 16px rgba(0,0,0,.03);}}
.metric-label {{font-size:.74rem; text-transform:uppercase; letter-spacing:.08em; color:#5E7868; margin-bottom:.2rem;}}
.metric-value {{font-size:1.8rem; font-weight:800; color:{GRAB_TEXT}; line-height:1.02;}}
.metric-note {{font-size:.8rem; color:#617B6C; margin-top:.28rem;}}
.section-card {{background:#fff; border:1px solid {GRAB_BORDER}; border-radius:16px; padding:.92rem 1rem .72rem 1rem; margin-bottom:.78rem; box-shadow:0 6px 18px rgba(0,0,0,.03);}}
.section-title {{font-size:1rem; font-weight:800; color:{GRAB_TEXT}; margin-bottom:.42rem;}}
.section-sub {{font-size:.84rem; color:#607A6A; margin-bottom:.62rem;}}
.problem-head {{background:#fff; border:1px solid {GRAB_BORDER}; border-left:6px solid {GRAB_GREEN}; border-radius:16px; padding:.9rem 1rem; margin-bottom:.82rem;}}
.problem-head.ps2 {{border-left-color:{TEAL};}}
.problem-head.ps3 {{border-left-color:{AMBER};}}
.problem-head h2 {{margin:0; font-size:1.08rem; color:{GRAB_TEXT};}}
.problem-head p {{margin:.28rem 0 0 0; color:#5F7869; font-size:.9rem;}}
.action-box {{background:#fff; border:1px solid {GRAB_BORDER}; border-radius:14px; padding:.88rem 1rem; margin-bottom:.62rem;}}
.action-box.green {{border-left:5px solid {GRAB_GREEN};}}
.action-box.amber {{border-left:5px solid {AMBER};}}
.action-box.red {{border-left:5px solid {RED};}}
.action-box h4 {{margin:0 0 .22rem 0; color:{GRAB_TEXT}; font-size:.98rem;}}
.action-box p {{margin:.2rem 0; font-size:.84rem; color:#5F7869;}}
.stTabs [data-baseweb="tab-list"] {{gap:.35rem;}}
.stTabs [data-baseweb="tab"] {{background:#fff; border:1px solid {GRAB_BORDER}; border-radius:12px 12px 0 0; padding:.55rem .9rem;}}
.stTabs [aria-selected="true"] {{color:{GRAB_GREEN} !important; border-bottom:2px solid {GRAB_GREEN} !important;}}
div[data-baseweb="select"] > div, div[data-baseweb="base-input"] > div {{border-color:{GRAB_BORDER} !important;}}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.phone-stage {
    background: linear-gradient(180deg, #FCFFFD 0%, #F3FBF6 100%);
    border: 1px solid #DCEEE3;
    border-radius: 22px;
    padding: 1rem 1rem .85rem 1rem;
    box-shadow: 0 10px 24px rgba(0,0,0,.04);
    margin-bottom: .7rem;
}
.phone-shell {
    width: 372px;
    max-width: 100%;
    margin: 0 auto;
    background: #0B1115;
    border-radius: 42px;
    padding: 10px;
    box-shadow: 0 26px 60px rgba(20,53,36,.18), 0 6px 16px rgba(0,0,0,.12);
}
.phone-body {
    background: #F6FBF8;
    border-radius: 32px;
    overflow: hidden;
    min-height: 690px;
    position: relative;
}
.phone-notch {
    width: 124px;
    height: 30px;
    background: #0B1115;
    border-radius: 0 0 18px 18px;
    margin: 0 auto 6px auto;
}
.phone-status {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: .45rem .95rem .1rem .95rem;
    color: #173B2A;
    font-size: .72rem;
    font-weight: 700;
}
.phone-header {
    padding: .55rem 1rem .85rem 1rem;
    background: linear-gradient(180deg, #EEFBF3 0%, #F7FBF8 100%);
}
.phone-brand { color: #00B14F; font-weight: 900; letter-spacing: .02em; font-size: 1rem; }
.phone-screen-title { margin-top: .18rem; color: #143524; font-size: 1.1rem; font-weight: 800; }
.phone-subtitle { margin-top: .15rem; color: #5D7768; font-size: .78rem; }
.phone-map {
    margin: .85rem 1rem .85rem 1rem;
    border-radius: 22px;
    padding: .95rem;
    min-height: 120px;
    background: linear-gradient(135deg, #D7F7E4 0%, #EFFAF4 55%, #FFFFFF 100%);
    border: 1px solid #DCEEE3;
}
.phone-route {
    display: inline-block;
    background: rgba(255,255,255,.9);
    border: 1px solid #DCEEE3;
    border-radius: 16px;
    padding: .7rem .85rem;
    color: #143524;
    box-shadow: 0 6px 14px rgba(0,0,0,.04);
}
.phone-route span { display: block; color: #6A8375; font-size: .72rem; margin-bottom: .18rem; }
.phone-route strong { font-size: .9rem; }
.phone-panel {
    background: #FFFFFF;
    margin: 0 1rem .78rem 1rem;
    border: 1px solid #DCEEE3;
    border-radius: 20px;
    padding: .92rem .95rem;
    box-shadow: 0 8px 18px rgba(0,0,0,.04);
}
.phone-panel.soft { background: #F8FCFA; }
.phone-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: .7rem;
    color: #143524;
    font-weight: 700;
    font-size: .86rem;
}
.phone-copy { color: #5E7868; font-size: .78rem; line-height: 1.5; margin-top: .45rem; }
.phone-banner { border-radius: 14px; padding: .68rem .78rem; font-size: .76rem; font-weight: 700; margin-top: .75rem; }
.phone-banner.warn { background: #FFF6E8; color: #9A5F00; border: 1px solid #F8E1BA; }
.phone-banner.success { background: #EAF8F0; color: #0B6B3A; border: 1px solid #CDEED9; }
.phone-chip { display: inline-block; padding: .28rem .58rem; border-radius: 999px; font-size: .67rem; font-weight: 800; letter-spacing: .01em; }
.phone-chip.neutral { color: #476555; background: #EEF5F1; border: 1px solid #DFECE5; }
.phone-chip.warn { color: #9A5F00; background: #FFF6E8; border: 1px solid #F8E1BA; }
.phone-chip.success { color: #0B6B3A; background: #EAF8F0; border: 1px solid #CDEED9; }
.phone-chip.danger { color: #B02C31; background: #FFF0F0; border: 1px solid #F7D5D7; }
.phone-price { color: #143524; font-size: 1.2rem; font-weight: 900; }
.phone-mini-kpis { display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; margin-top: .8rem; }
.phone-kpi { background: #F8FCFA; border: 1px solid #E3F1E9; border-radius: 16px; padding: .68rem .72rem; }
.phone-kpi span { display: block; color: #6A8375; font-size: .68rem; margin-bottom: .18rem; }
.phone-kpi strong { color: #143524; font-size: .95rem; }
.phone-cta { margin: .2rem 1rem 1rem 1rem; background: #00B14F; color: #FFFFFF; text-align: center; border-radius: 16px; padding: .88rem 1rem; font-size: .88rem; font-weight: 800; box-shadow: 0 10px 18px rgba(0,177,79,.18); }
.phone-cta.muted { background: #DFF2E7; color: #0B6B3A; box-shadow: none; }
.phone-service-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .55rem; margin-top: .78rem; }
.phone-service { background: #F8FCFA; border: 1px solid #E3F1E9; border-radius: 16px; padding: .65rem .2rem; text-align: center; color: #143524; font-size: .72rem; font-weight: 800; }
.phone-service.active { background: linear-gradient(180deg, #EAF8F0 0%, #F4FBF7 100%); border-color: #BFE7CF; color: #0B6B3A; }
.phone-offer { margin-top: .7rem; background: linear-gradient(135deg, #143524 0%, #0B6B3A 100%); color: #FFFFFF; border-radius: 18px; padding: .9rem .95rem; }
.phone-offer small { display: block; opacity: .78; margin-bottom: .22rem; }
.phone-offer strong { display: block; font-size: 1rem; margin-bottom: .22rem; }
.phone-fare-line { display: flex; justify-content: space-between; align-items: center; color: #143524; font-size: .78rem; padding: .36rem 0; border-bottom: 1px dashed #E3EEE8; }
.phone-fare-line:last-child { border-bottom: none; }
.impact-card { background: #FFFFFF; border: 1px solid #DCEEE3; border-radius: 18px; padding: .9rem 1rem; margin-bottom: .72rem; box-shadow: 0 8px 18px rgba(0,0,0,.03); }
.impact-label { color: #607A6A; font-size: .74rem; text-transform: uppercase; letter-spacing: .08em; }
.impact-values { display: flex; justify-content: space-between; align-items: flex-end; gap: .8rem; margin-top: .48rem; }
.impact-current, .impact-best { color: #143524; font-size: 1.1rem; font-weight: 800; }
.impact-sub { color: #6A8375; font-size: .69rem; margin-top: .08rem; }
.impact-delta { font-size: .82rem; font-weight: 800; margin-top: .32rem; }
.impact-delta.good { color: #0B6B3A; }
.impact-delta.bad { color: #E5484D; }
.sim-note { background: #F8FCFA; border: 1px solid #E3F1E9; border-radius: 16px; padding: .85rem .95rem; margin-bottom: .72rem; color: #567061; font-size: .82rem; line-height: 1.55; }
.sim-note strong { color: #143524; }
</style>
""", unsafe_allow_html=True)

alt.theme.enable("default")

@st.cache_data
def load_data(uploaded=None):
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        path = BASE_DIR / DATA_FILE
        if not path.exists():
            return None
        df = pd.read_csv(path)
    for c in df.columns:
        if df[c].dtype == 'object':
            df[c] = df[c].fillna('Unknown').astype(str)
    return df


def header():
    st.markdown("""
    <div class='main-title'>
      <h1>Grab Executive Dashboard</h1>
      <p>Problem-led analytical views for Driver Trust, Super-App Growth, and Pricing Fairness.</p>
    </div>
    """, unsafe_allow_html=True)


def kpi_card(col, label, value, note):
    col.markdown(f"""
    <div class='metric-card'>
      <div class='metric-label'>{label}</div>
      <div class='metric-value'>{value}</div>
      <div class='metric-note'>{note}</div>
    </div>
    """, unsafe_allow_html=True)


def section_open(title, subtitle):
    st.markdown(f"<div class='section-card'><div class='section-title'>{title}</div><div class='section-sub'>{subtitle}</div>", unsafe_allow_html=True)


def section_close():
    st.markdown("</div>", unsafe_allow_html=True)


def problem_head(title, text, cls=''):
    st.markdown(f"<div class='problem-head {cls}'><h2>{title}</h2><p>{text}</p></div>", unsafe_allow_html=True)


def filter_panel(df):
    with st.expander("Filters", expanded=False):
        c1, c2, c3 = st.columns(3)
        countries = c1.multiselect("Country", sorted(df['country'].dropna().unique()), default=sorted(df['country'].dropna().unique()))
        value_tier = c2.multiselect("Value tier", sorted(df['customer_value_tier'].dropna().unique()), default=sorted(df['customer_value_tier'].dropna().unique()))
        super_seg = c3.multiselect("Super-app segment", sorted(df['superapp_segment'].dropna().unique()), default=sorted(df['superapp_segment'].dropna().unique()))
        c4, c5, c6 = st.columns(3)
        driver_tier = c4.multiselect("Driver tier", sorted(df['assigned_driver_tier'].dropna().unique()), default=sorted(df['assigned_driver_tier'].dropna().unique()))
        price_seg = c5.multiselect("Price sensitivity", sorted(df['price_sensitivity_segment'].dropna().unique()), default=sorted(df['price_sensitivity_segment'].dropna().unique()))
        primary = c6.multiselect("Primary service", sorted(df['primary_service'].dropna().unique()), default=sorted(df['primary_service'].dropna().unique()))
    view = df[
        df['country'].isin(countries)
        & df['customer_value_tier'].isin(value_tier)
        & df['superapp_segment'].isin(super_seg)
        & df['assigned_driver_tier'].isin(driver_tier)
        & df['price_sensitivity_segment'].isin(price_seg)
        & df['primary_service'].isin(primary)
    ].copy()
    return view


def apply_chart_style(chart):
    return chart.configure_view(stroke=None).configure_axis(
        labelColor=GRAB_TEXT,
        titleColor=GRAB_TEXT,
        gridColor="#E8F1EC",
        domainColor="#D7E7DE",
        tickColor="#D7E7DE"
    ).configure_legend(labelColor=GRAB_TEXT, titleColor=GRAB_TEXT).configure_title(color=GRAB_TEXT)


def with_optional_title(chart, title=None, height=300):
    chart = apply_chart_style(chart).properties(height=height)
    if title:
        chart = chart.properties(title=title)
    return chart


def bar_chart(df, x, y, title=None, color=GRAB_GREEN, sort='-y', x_type='N', y_title=None, tooltip=None):
    tooltip = tooltip or [x, y]
    chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4, color=color).encode(
        x=alt.X(f'{x}:{x_type}', sort=sort, title=x.replace('_',' ').title()),
        y=alt.Y(f'{y}:Q', title=y_title or y.replace('_',' ').title()),
        tooltip=tooltip
    )
    return with_optional_title(chart, title)


def grouped_bar(df, x, y, color_field, title=None, palette=None, x_type='N'):
    scale = alt.Scale(range=palette) if palette else alt.Undefined
    chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3).encode(
        x=alt.X(f'{x}:{x_type}', title=x.replace('_',' ').title()),
        y=alt.Y(f'{y}:Q', title=y.replace('_',' ').title()),
        color=alt.Color(f'{color_field}:N', scale=scale, title=color_field.replace('_',' ').title()),
        xOffset=f'{color_field}:N',
        tooltip=[x, color_field, y]
    )
    return with_optional_title(chart, title)


def line_chart(df, x, y, color_field=None, title=None, palette=None, x_type='N'):
    enc = {
        'x': alt.X(f'{x}:{x_type}', title=x.replace('_',' ').title()),
        'y': alt.Y(f'{y}:Q', title=y.replace('_',' ').title()),
        'tooltip': [x, y]
    }
    if color_field:
        scale = alt.Scale(range=palette) if palette else alt.Undefined
        enc['color'] = alt.Color(f'{color_field}:N', scale=scale, title=color_field.replace('_',' ').title())
        enc['tooltip'] = [x, color_field, y]
    chart = alt.Chart(df).mark_line(point=True, strokeWidth=3).encode(**enc)
    return with_optional_title(chart, title)


def scatter_chart(df, x, y, size=None, color_field=None, title=None, palette=None, tooltip=None):
    enc = {
        'x': alt.X(f'{x}:Q', title=x.replace('_',' ').title()),
        'y': alt.Y(f'{y}:Q', title=y.replace('_',' ').title())
    }
    if size:
        enc['size'] = alt.Size(f'{size}:Q', title=size.replace('_',' ').title())
    if color_field:
        scale = alt.Scale(range=palette) if palette else alt.Undefined
        enc['color'] = alt.Color(f'{color_field}:N', scale=scale, title=color_field.replace('_',' ').title())
    enc['tooltip'] = tooltip or [x, y]
    chart = alt.Chart(df).mark_circle(opacity=0.78, stroke='white', strokeWidth=0.7).encode(**enc)
    return with_optional_title(chart, title)


def heatmap_chart(df, x, y, color, title=None, scheme='greens'):
    chart = alt.Chart(df).mark_rect().encode(
        x=alt.X(f'{x}:N', title=x.replace('_',' ').title()),
        y=alt.Y(f'{y}:N', title=y.replace('_',' ').title()),
        color=alt.Color(f'{color}:Q', scale=alt.Scale(scheme=scheme), title=color.replace('_',' ').title()),
        tooltip=[x, y, color]
    )
    text = alt.Chart(df).mark_text(fontSize=11, color=GRAB_TEXT).encode(
        x=f'{x}:N', y=f'{y}:N', text=alt.Text(f'{color}:Q', format='.1f')
    )
    return with_optional_title(chart + text, title, height=260)


def band_counts(series, bins, labels, name='Band'):
    out = pd.cut(series, bins=bins, labels=labels, include_lowest=True).value_counts().sort_index().reset_index()
    out.columns = [name, 'Customers']
    return out


def top_rows(df, cols, sort_cols, ascending, n=12):
    return df[cols].sort_values(sort_cols, ascending=ascending).head(n)






def render_story_demo(key, payload, height=800):
    metrics_html = ''.join(
        f"<div class='story-metric'><span>{m['label']}</span><strong data-current='{m['current']}' data-improved='{m['improved']}'>{m['current']}</strong><small data-current='{m['current_note']}' data-improved='{m['improved_note']}'>{m['current_note']}</small></div>"
        for m in payload['metrics']
    )
    data = json.dumps({
        'current_title': payload['current_title'],
        'improved_title': payload['improved_title'],
        'current_text': payload['current_text'],
        'improved_text': payload['improved_text'],
        'current_status': payload['current_status'],
        'improved_status': payload['improved_status'],
        'interval_ms': payload.get('interval_ms', 3200),
    })
    html = f"""
    <html><head><meta name='viewport' content='width=device-width, initial-scale=1' />
    <style>
    * {{ box-sizing:border-box; font-family: Inter, -apple-system, BlinkMacSystemFont, sans-serif; }}
    body {{ margin:0; background:transparent; }}
    .story-shell {{ background:linear-gradient(180deg,#FCFFFD 0%,#F3FBF6 100%); border:1px solid #DCEEE3; border-radius:24px; padding:16px; box-shadow:0 10px 24px rgba(0,0,0,.04); }}
    .story-grid {{ display:grid; grid-template-columns:392px 1fr; gap:18px; align-items:start; }}
    .phone-shell {{ width:372px; max-width:100%; margin:0 auto; background:#0B1115; border-radius:42px; padding:10px; box-shadow:0 26px 60px rgba(20,53,36,.18), 0 6px 16px rgba(0,0,0,.12); }}
    .phone-notch {{ width:124px; height:30px; background:#0B1115; border-radius:0 0 18px 18px; margin:0 auto 6px auto; }}
    .phone-body {{ background:#F6FBF8; border-radius:32px; overflow:hidden; min-height:690px; position:relative; }}
    .screen {{ position:absolute; inset:0; opacity:0; transform:translateX(22px) scale(.986); transition:opacity .75s cubic-bezier(.22,1,.36,1), transform .75s cubic-bezier(.22,1,.36,1); }}
    .screen.active {{ opacity:1; transform:translateX(0) scale(1); }}
    .story-panel {{ background:#FFFFFF; border:1px solid #DCEEE3; border-radius:20px; padding:16px; min-height:710px; box-shadow:0 8px 18px rgba(0,0,0,.03); display:flex; flex-direction:column; }}
    .story-top {{ display:flex; justify-content:space-between; align-items:center; gap:10px; }}
    .story-kicker {{ color:#607A6A; font-size:.74rem; text-transform:uppercase; letter-spacing:.08em; }}
    .story-live {{ color:#0B6B3A; background:#EAF8F0; border:1px solid #CDEED9; border-radius:999px; padding:.32rem .65rem; font-size:.68rem; font-weight:800; }}
    .story-live.paused {{ color:#6A8375; background:#F3F7F5; border-color:#E1ECE6; }}
    .story-title {{ color:#143524; font-weight:800; font-size:1.16rem; margin-top:.55rem; }}
    .story-text {{ color:#5C7667; font-size:.85rem; line-height:1.62; margin-top:.35rem; min-height:88px; }}
    .story-status {{ margin-top:.8rem; border-radius:16px; padding:.82rem .9rem; font-size:.81rem; font-weight:700; transition:all .45s ease; }}
    .story-status.current {{ background:#FFF6E8; color:#9A5F00; border:1px solid #F8E1BA; }}
    .story-status.improved {{ background:#EAF8F0; color:#0B6B3A; border:1px solid #CDEED9; }}
    .story-progress {{ width:100%; height:6px; background:#EDF4F0; border-radius:999px; overflow:hidden; margin-top:.75rem; }}
    .story-progress-bar {{ width:100%; height:100%; transform-origin:left center; background:linear-gradient(90deg,#00B14F 0%, #54D98B 100%); animation:storyProgress linear infinite; }}
    .story-progress-bar.paused {{ animation-play-state:paused; }}
    .story-dots {{ display:flex; gap:.35rem; margin-top:.6rem; }}
    .story-dot {{ width:8px; height:8px; border-radius:999px; background:#D1E4D9; transition:all .35s ease; }}
    .story-dot.active {{ width:20px; background:#00B14F; }}
    .story-metrics {{ display:grid; grid-template-columns:1fr; gap:.72rem; margin-top:.95rem; }}
    .story-metric {{ background:#F8FCFA; border:1px solid #E3F1E9; border-radius:16px; padding:.82rem .9rem; transition:transform .35s ease, box-shadow .35s ease, border-color .35s ease; }}
    .story-metric.active {{ transform:translateY(-2px); box-shadow:0 8px 18px rgba(0,177,79,.08); border-color:#BFE7CF; }}
    .story-metric span {{ display:block; color:#607A6A; font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; }}
    .story-metric strong {{ display:block; color:#143524; font-size:1.16rem; margin-top:.23rem; }}
    .story-metric small {{ display:block; color:#6A8375; margin-top:.22rem; font-size:.74rem; line-height:1.45; }}
    .story-actions {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:.55rem; margin-top:auto; padding-top:1rem; }}
    .story-btn {{ border:none; border-radius:14px; padding:.82rem .85rem; font-weight:800; cursor:pointer; }}
    .story-btn.secondary {{ background:#EFF5F1; color:#244334; }} .story-btn.primary {{ background:#00B14F; color:#fff; }} .story-btn.ghost {{ background:#fff; color:#244334; border:1px solid #DCEEE3; }}
    .phone-status {{ display:flex; justify-content:space-between; align-items:center; padding:.45rem .95rem .1rem .95rem; color:#173B2A; font-size:.72rem; font-weight:700; }}
    .phone-header {{ padding:.55rem 1rem .85rem 1rem; background:linear-gradient(180deg,#EEFBF3 0%,#F7FBF8 100%); }}
    .phone-brand {{ color:#00B14F; font-weight:900; letter-spacing:.02em; font-size:1rem; }} .phone-screen-title {{ margin-top:.18rem; color:#143524; font-size:1.1rem; font-weight:800; }} .phone-subtitle {{ margin-top:.15rem; color:#5D7768; font-size:.78rem; }}
    .phone-map {{ margin:.85rem 1rem .85rem 1rem; border-radius:22px; padding:.95rem; min-height:120px; background:linear-gradient(135deg,#D7F7E4 0%,#EFFAF4 55%,#FFFFFF 100%); border:1px solid #DCEEE3; }}
    .phone-route {{ display:inline-block; background:rgba(255,255,255,.9); border:1px solid #DCEEE3; border-radius:16px; padding:.7rem .85rem; color:#143524; box-shadow:0 6px 14px rgba(0,0,0,.04); }}
    .phone-route span {{ display:block; color:#6A8375; font-size:.72rem; margin-bottom:.18rem; }} .phone-route strong {{ font-size:.9rem; }}
    .phone-panel {{ background:#FFFFFF; margin:0 1rem .78rem 1rem; border:1px solid #DCEEE3; border-radius:20px; padding:.92rem .95rem; box-shadow:0 8px 18px rgba(0,0,0,.04); }} .phone-panel.soft {{ background:#F8FCFA; }}
    .phone-row {{ display:flex; justify-content:space-between; align-items:center; gap:.7rem; color:#143524; font-weight:700; font-size:.86rem; }} .phone-copy {{ color:#5E7868; font-size:.78rem; line-height:1.5; margin-top:.45rem; }}
    .phone-banner {{ border-radius:14px; padding:.68rem .78rem; font-size:.76rem; font-weight:700; margin-top:.75rem; }} .phone-banner.warn {{ background:#FFF6E8; color:#9A5F00; border:1px solid #F8E1BA; }} .phone-banner.success {{ background:#EAF8F0; color:#0B6B3A; border:1px solid #CDEED9; }}
    .phone-chip {{ display:inline-block; padding:.28rem .58rem; border-radius:999px; font-size:.67rem; font-weight:800; letter-spacing:.01em; }} .phone-chip.neutral {{ color:#476555; background:#EEF5F1; border:1px solid #DFECE5; }} .phone-chip.warn {{ color:#9A5F00; background:#FFF6E8; border:1px solid #F8E1BA; }} .phone-chip.success {{ color:#0B6B3A; background:#EAF8F0; border:1px solid #CDEED9; }} .phone-chip.danger {{ color:#B02C31; background:#FFF0F0; border:1px solid #F7D5D7; }}
    .phone-price {{ color:#143524; font-size:1.2rem; font-weight:900; }} .phone-mini-kpis {{ display:grid; grid-template-columns:1fr 1fr; gap:.6rem; margin-top:.8rem; }} .phone-kpi {{ background:#F8FCFA; border:1px solid #E3F1E9; border-radius:16px; padding:.68rem .72rem; }} .phone-kpi span {{ display:block; color:#6A8375; font-size:.68rem; margin-bottom:.18rem; }} .phone-kpi strong {{ color:#143524; font-size:.95rem; }}
    .phone-cta {{ margin:.2rem 1rem 1rem 1rem; background:#00B14F; color:#FFFFFF; text-align:center; border-radius:16px; padding:.88rem 1rem; font-size:.88rem; font-weight:800; box-shadow:0 10px 18px rgba(0,177,79,.18); }} .phone-cta.muted {{ background:#DFF2E7; color:#0B6B3A; box-shadow:none; }}
    .phone-service-grid {{ display:grid; grid-template-columns:repeat(4,1fr); gap:.55rem; margin-top:.78rem; }} .phone-service {{ background:#F8FCFA; border:1px solid #E3F1E9; border-radius:16px; padding:.65rem .2rem; text-align:center; color:#143524; font-size:.72rem; font-weight:800; }} .phone-service.active {{ background:linear-gradient(180deg,#EAF8F0 0%,#F4FBF7 100%); border-color:#BFE7CF; color:#0B6B3A; }}
    .phone-offer {{ margin-top:.7rem; background:linear-gradient(135deg,#143524 0%,#0B6B3A 100%); color:#FFFFFF; border-radius:18px; padding:.9rem .95rem; }} .phone-offer small {{ display:block; opacity:.78; margin-bottom:.22rem; }} .phone-offer strong {{ display:block; font-size:1rem; margin-bottom:.22rem; }}
    .phone-fare-line {{ display:flex; justify-content:space-between; align-items:center; color:#143524; font-size:.78rem; padding:.36rem 0; border-bottom:1px dashed #E3EEE8; }} .phone-fare-line:last-child {{ border-bottom:none; }}
    @keyframes storyProgress {{ from {{ transform:scaleX(0); }} to {{ transform:scaleX(1); }} }} @media (max-width:920px) {{ .story-grid {{ grid-template-columns:1fr; }} .story-panel {{ min-height:auto; }} }}
    </style></head><body>
    <div class='story-shell' id='root_{key}'><div class='story-grid'><div><div class='phone-shell'><div class='phone-notch'></div><div class='phone-body'><div class='screen active' id='{key}_current'>{payload['current_screen']}</div><div class='screen' id='{key}_improved'>{payload['improved_screen']}</div></div></div></div><div class='story-panel'><div class='story-top'><div class='story-kicker'>{payload['kicker']}</div><div class='story-live' id='{key}_live'>Live story</div></div><div class='story-title' id='{key}_title'>{payload['current_title']}</div><div class='story-text' id='{key}_text'>{payload['current_text']}</div><div class='story-status current' id='{key}_status'>{payload['current_status']}</div><div class='story-progress'><div class='story-progress-bar' id='{key}_progress'></div></div><div class='story-dots'><div class='story-dot active' id='{key}_dot_c'></div><div class='story-dot' id='{key}_dot_i'></div></div><div class='story-metrics'>{metrics_html}</div><div class='story-actions'><button class='story-btn secondary' id='{key}_btn_c'>Current state</button><button class='story-btn primary' id='{key}_btn_i'>Best case</button><button class='story-btn ghost' id='{key}_btn_l'>Pause</button></div></div></div></div>
    <script>
    const data = {data};
    const currentScreen = document.getElementById('{key}_current');
    const improvedScreen = document.getElementById('{key}_improved');
    const titleEl = document.getElementById('{key}_title');
    const textEl = document.getElementById('{key}_text');
    const statusEl = document.getElementById('{key}_status');
    const liveEl = document.getElementById('{key}_live');
    const progressEl = document.getElementById('{key}_progress');
    const dotC = document.getElementById('{key}_dot_c');
    const dotI = document.getElementById('{key}_dot_i');
    const metricCards = Array.from(document.querySelectorAll('#root_{key} .story-metric'));
    const metricValues = Array.from(document.querySelectorAll('#root_{key} .story-metric strong'));
    const metricNotes = Array.from(document.querySelectorAll('#root_{key} .story-metric small'));
    let state = 'current'; let looping = true; let timer = null;
    function refreshProgress() {{ progressEl.style.animation='none'; void progressEl.offsetWidth; progressEl.style.animation=`storyProgress ${{data.interval_ms}}ms linear infinite`; progressEl.classList.toggle('paused', !looping); }}
    function setState(next) {{ const improved = next==='improved'; state=next; currentScreen.classList.toggle('active', !improved); improvedScreen.classList.toggle('active', improved); titleEl.textContent = improved ? data.improved_title : data.current_title; textEl.textContent = improved ? data.improved_text : data.current_text; statusEl.textContent = improved ? data.improved_status : data.current_status; statusEl.className = 'story-status ' + (improved ? 'improved' : 'current'); dotC.classList.toggle('active', !improved); dotI.classList.toggle('active', improved); metricCards.forEach((el, idx)=> el.classList.toggle('active', improved && idx===0)); metricValues.forEach(el=>el.textContent = improved ? el.dataset.improved : el.dataset.current); metricNotes.forEach(el=>el.textContent = improved ? el.dataset.improved : el.dataset.current); refreshProgress(); }}
    function startLoop() {{ if (timer) clearInterval(timer); if (!looping) return; timer = setInterval(()=>setState(state==='current' ? 'improved' : 'current'), data.interval_ms); }}
    document.getElementById('{key}_btn_c').onclick=()=>setState('current');
    document.getElementById('{key}_btn_i').onclick=()=>setState('improved');
    document.getElementById('{key}_btn_l').onclick=()=>{{ looping=!looping; document.getElementById('{key}_btn_l').textContent = looping ? 'Pause' : 'Resume'; liveEl.textContent = looping ? 'Live story' : 'Manual mode'; liveEl.classList.toggle('paused', !looping); refreshProgress(); startLoop(); }};
    setState('current'); startLoop();
    </script></body></html>
    """
    components.html(html, height=height, scrolling=False)


def clamp(value, low, high):
    return max(low, min(high, value))


def fmt_metric(value, suffix='', decimals=1):
    return f"{float(value):,.{decimals}f}{suffix}"


def first_mode(series, fallback='Selected market'):
    series = series.dropna()
    return fallback if series.empty else str(series.mode().iloc[0])


def top_group(df, group_col, value_col, fallback='Selected market'):
    if df.empty:
        return fallback
    grp = df.groupby(group_col, as_index=False)[value_col].mean().sort_values(value_col, ascending=False)
    return fallback if grp.empty else str(grp.iloc[0][group_col])


def impact_card(label, current, improved, note, higher_is_better=True, suffix='', decimals=1):
    delta = float(improved) - float(current)
    good = delta >= 0 if higher_is_better else delta <= 0
    cls = 'good' if good else 'bad'
    if abs(delta) < 1e-9:
        delta_text = 'No change'
    else:
        arrow = '▲' if delta > 0 else '▼'
        delta_text = f"{arrow} {fmt_metric(abs(delta), suffix=suffix, decimals=decimals)}"
    st.markdown(f"""
        <div class='impact-card'>
            <div class='impact-label'>{label}</div>
            <div class='impact-values'>
                <div>
                    <div class='impact-current'>{fmt_metric(current, suffix=suffix, decimals=decimals)}</div>
                    <div class='impact-sub'>Current</div>
                </div>
                <div style='text-align:right'>
                    <div class='impact-best'>{fmt_metric(improved, suffix=suffix, decimals=decimals)}</div>
                    <div class='impact-sub'>Best case</div>
                </div>
            </div>
            <div class='impact-delta {cls}'>{delta_text}</div>
            <div class='impact-sub'>{note}</div>
        </div>
    """, unsafe_allow_html=True)


def render_phone(screen_html):
    st.markdown(f"""
        <div class='phone-stage'>
            <div class='phone-shell'>
                <div class='phone-notch'></div>
                <div class='phone-body'>{screen_html}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def phone_state_buttons(key):
    if key not in st.session_state:
        st.session_state[key] = 'current'
    c1, c2 = st.columns(2)
    cur_label = '● Current experience' if st.session_state[key] == 'current' else 'Current experience'
    imp_label = '● Improved experience' if st.session_state[key] == 'improved' else 'Improved experience'
    with c1:
        if st.button(cur_label, key=f'{key}_current', use_container_width=True):
            st.session_state[key] = 'current'
            st.rerun()
    with c2:
        if st.button(imp_label, key=f'{key}_improved', use_container_width=True):
            st.session_state[key] = 'improved'
            st.rerun()
    return st.session_state[key]



def master_ps1(view):
    c1,c2,c3,c4,c5 = st.columns(5)
    kpi_card(c1,'Bad booking rate',f"{view['bad_booking_label'].mean()*100:.1f}%",'Bookings likely to fail or delay')
    kpi_card(c2,'Avg ETA gap',f"{view['eta_gap_min'].mean():.1f} min",'Promised vs actual')
    kpi_card(c3,'High-risk driver exposure',f"{(view['assigned_driver_tier']=='High-Risk').mean()*100:.1f}%",'Share matched to weak drivers')
    kpi_card(c4,'Complaint load',f"{view['complaint_count_90d'].mean():.1f}",'Average complaints over 90d')
    kpi_card(c5,'Trust score',f"{view['trust_score'].mean():.1f}",'Higher is better')

    current_bad = float(view['bad_booking_label'].mean() * 100)
    current_eta = float(view['eta_gap_min'].mean())
    current_trust = float(view['trust_score'].mean())
    current_high_risk = float((view['assigned_driver_tier'] == 'High-Risk').mean() * 100)
    current_low_supply = float(view['low_supply_zone_share'].mean() * 100)
    current_rush = float(view['rush_hour_share'].mean() * 100)
    focus_country = top_group(view, 'country', 'bad_booking_label', 'Selected market')
    focus_tier = first_mode(view['assigned_driver_tier'], 'Standard')

    booking_lift = min(0.38, 0.16 + (current_high_risk / 100) * 0.14 + (current_low_supply / 100) * 0.10)
    eta_lift = min(0.34, 0.10 + (current_low_supply / 100) * 0.14 + (current_rush / 100) * 0.08)
    improved_bad = clamp(current_bad * (1 - booking_lift), 2.0, current_bad)
    improved_eta = clamp(current_eta * (1 - eta_lift), 1.0, current_eta)
    improved_trust = clamp(current_trust + max(0, current_bad - improved_bad) * 0.55 + max(0, current_eta - improved_eta) * 1.80 + 3.0, current_trust, 100.0)

    eta_now = max(4, int(round(7 + current_eta)))
    eta_best = max(3, int(round(eta_now - max(1, current_eta * 0.55))))
    recovery_credit = int(round(min(25, 8 + current_bad / 2)))
    issue_count = int((view['booking_risk_score'] >= 70).sum())
    state = st.session_state.get('ps1_demo_state', 'current')

    problem_screen = f"""
    <div class='phone-status'><span>9:41</span><span>5G 92%</span></div>
    <div class='phone-header'>
        <div class='phone-brand'>Grab</div>
        <div class='phone-screen-title'>Book ride</div>
        <div class='phone-subtitle'>{focus_country} · Airport trip</div>
    </div>
    <div class='phone-map'>
        <div class='phone-route'><span>Pickup</span><strong>Home</strong><span style='margin-top:.45rem'>Drop-off</span><strong>Airport T1</strong></div>
        <div style='margin-top:.7rem'><span class='phone-chip warn'>Low supply in your zone</span></div>
    </div>
    <div class='phone-panel'>
        <div class='phone-row'><span>JustGrab</span><span class='phone-price'>{eta_now} min</span></div>
        <div class='phone-banner warn'>Driver changed again. Similar bookings in this context fail or break trust {current_bad:.1f}% of the time.</div>
        <div class='phone-mini-kpis'>
            <div class='phone-kpi'><span>ETA miss</span><strong>{current_eta:.1f} min</strong></div>
            <div class='phone-kpi'><span>Trust</span><strong>{current_trust:.0f}/100</strong></div>
        </div>
    </div>
    <div class='phone-panel soft'>
        <div class='phone-row'><span>What the customer sees</span><span class='phone-chip danger'>Uncertain</span></div>
        <div class='phone-copy'>Matched to {focus_tier} supply, delayed ETAs, and no clear recovery promise if the booking fails.</div>
        <div class='phone-copy'><strong>{issue_count}</strong> customers in the current filtered portfolio are already above the risk threshold.</div>
    </div>
    <div class='phone-cta muted'>Retry booking</div>
    """

    improved_screen = f"""
    <div class='phone-status'><span>9:41</span><span>5G 92%</span></div>
    <div class='phone-header'>
        <div class='phone-brand'>Grab</div>
        <div class='phone-screen-title'>Protected ride</div>
        <div class='phone-subtitle'>{focus_country} · Reliable-driver override applied</div>
    </div>
    <div class='phone-map'>
        <div class='phone-route'><span>Pickup</span><strong>Home</strong><span style='margin-top:.45rem'>Drop-off</span><strong>Airport T1</strong></div>
        <div style='margin-top:.7rem'><span class='phone-chip success'>ETA locked</span> <span class='phone-chip success'>Recovery ready</span></div>
    </div>
    <div class='phone-panel'>
        <div class='phone-row'><span>Reliable Driver Match</span><span class='phone-price'>{eta_best} min</span></div>
        <div class='phone-banner success'>High-risk dispatch removed. If your driver is late, a ${recovery_credit} service credit is already protected.</div>
        <div class='phone-mini-kpis'>
            <div class='phone-kpi'><span>Bad booking risk</span><strong>{improved_bad:.1f}%</strong></div>
            <div class='phone-kpi'><span>Trust</span><strong>{improved_trust:.0f}/100</strong></div>
        </div>
    </div>
    <div class='phone-panel soft'>
        <div class='phone-row'><span>What improved</span><span class='phone-chip success'>Stable</span></div>
        <div class='phone-copy'>Reliable-driver override, tighter dispatch in low-supply zones, and automatic recovery messaging remove the uncertainty from the ride-booking moment.</div>
    </div>
    <div class='phone-cta'>Confirm protected ride</div>
    """

    story_payload = {
        'kicker': 'Customer app demo · Driver Trust',
        'current_title': 'Current experience: booking feels fragile',
        'current_text': 'The booking flow feels uncertain because the customer sees low-supply friction, weaker dispatch quality, and no visible promise that Grab will recover the experience if it breaks.',
        'current_status': 'Why it feels bad: the app surfaces demand pressure before reassurance.',
        'improved_title': 'Best case: the ride is protected inside the journey',
        'improved_text': 'The app now behaves like a real product fix: stronger driver matching, a believable ETA, and automatic recovery all appear naturally inside the ride-booking flow.',
        'improved_status': 'What changed: reliable-driver override, tighter zone dispatch, and built-in recovery improve trust before checkout.',
        'interval_ms': 3200,
        'metrics': [
            {'label': 'Bad booking rate', 'current': f'{current_bad:.1f}%', 'improved': f'{improved_bad:.1f}%', 'current_note': 'Broken-booking exposure today.', 'improved_note': 'Lower after safer matching and dispatch.'},
            {'label': 'ETA gap', 'current': f'{current_eta:.1f} min', 'improved': f'{improved_eta:.1f} min', 'current_note': 'Promised versus actual arrival gap.', 'improved_note': 'Narrower after operational correction.'},
            {'label': 'Trust score', 'current': f'{current_trust:.0f}/100', 'improved': f'{improved_trust:.0f}/100', 'current_note': 'Customer confidence in the booking flow.', 'improved_note': 'Higher once reliability and recovery are visible.'},
        ],
        'current_screen': problem_screen,
        'improved_screen': improved_screen,
    }
    render_story_demo('ps1_story', story_payload, height=800)

    a,b = st.columns(2)
    with a:
        section_open('Risk map','Master view of where booking failure is concentrated.')
        rc = view.groupby('country', as_index=False)['bad_booking_label'].mean()
        rc['bad_booking_pct'] = rc['bad_booking_label']*100
        st.altair_chart(bar_chart(rc, 'country', 'bad_booking_pct', color=GRAB_GREEN, y_title='Bad booking %'), use_container_width=True)
        section_close()
        section_open('Tier and trust profile','Driver reliability mix and resulting trust effect.')
        dt = view.groupby('assigned_driver_tier', as_index=False).agg(customers=('customer_id','count'), trust_score=('trust_score','mean'))
        st.altair_chart(grouped_bar(dt.melt('assigned_driver_tier', var_name='Metric', value_name='Value'), 'assigned_driver_tier', 'Value', 'Metric', palette=[GRAB_GREEN, TEAL]), use_container_width=True)
        section_close()
    with b:
        section_open('ETA realism','Average promised versus actual arrival by country.')
        eta = view.groupby('country', as_index=False)[['avg_eta_promised_min','avg_eta_actual_min']].mean().melt('country', var_name='Metric', value_name='Minutes')
        st.altair_chart(grouped_bar(eta, 'country', 'Minutes', 'Metric', palette=[GRAB_GREEN, AMBER]), use_container_width=True)
        section_close()
        section_open('High-risk queue','Priority customers needing intervention now.')
        q = top_rows(view, ['customer_id','country','assigned_driver_tier','booking_risk_score','eta_gap_min','clv_12m_usd'], ['booking_risk_score','clv_12m_usd'], [False, False], 12)
        st.dataframe(q, use_container_width=True, hide_index=True)
        section_close()

    x,y = st.columns([1.15,.85])
    with x:
        section_open('Context drivers','Risk rises when low-supply exposure and ETA gap both increase.')
        st.altair_chart(scatter_chart(view, 'low_supply_zone_share', 'booking_risk_score', size='eta_gap_min', color_field='assigned_driver_tier', palette=[GRAB_GREEN, TEAL, RED], tooltip=['customer_id','country','low_supply_zone_share','eta_gap_min','booking_risk_score','assigned_driver_tier']), use_container_width=True)
        section_close()
    with y:
        st.markdown(f"""
        <div class='action-box green'><h4>Decision priority</h4><p>Auto-reassign high-value customers when booking risk exceeds 70.</p><p>Why this group combines high trust-loss risk and high value.</p></div>
        <div class='action-box amber'><h4>Operations priority</h4><p>Send targeted incentives into low-supply rush-hour zones.</p><p>Why supply imbalance is driving avoidable delay and cancellation exposure.</p></div>
        <div class='action-box red'><h4>Control priority</h4><p>Escalate High-Risk driver tier for warning, reduced visibility, or review.</p><p>Why complaints and failure rates are already elevated.</p></div>
        """, unsafe_allow_html=True)


def descriptive_ps1(view):
    a,b = st.columns(2)
    with a:
        section_open('Failed booking by country','Current distribution of booking failures.')
        rc = view.groupby('country', as_index=False)['bad_booking_label'].mean(); rc['bad_booking_pct']=rc['bad_booking_label']*100
        st.altair_chart(bar_chart(rc,'country','bad_booking_pct',color=GRAB_GREEN,y_title='Bad booking %'), use_container_width=True)
        section_close()
        section_open('Driver tier distribution','How exposure is split across reliability buckets.')
        dt = view['assigned_driver_tier'].value_counts().reset_index(); dt.columns=['assigned_driver_tier','Customers']
        st.altair_chart(bar_chart(dt,'assigned_driver_tier','Customers',color=TEAL), use_container_width=True)
        section_close()
    with b:
        section_open('Complaints by driver tier','Average complaint load by reliability tier.')
        comp = view.groupby('assigned_driver_tier', as_index=False)['complaint_count_90d'].mean()
        st.altair_chart(bar_chart(comp,'assigned_driver_tier','complaint_count_90d',color=AMBER), use_container_width=True)
        section_close()
        section_open('ETA gap by country','Operational pain point by market.')
        eg = view.groupby('country', as_index=False)['eta_gap_min'].mean()
        st.altair_chart(bar_chart(eg,'country','eta_gap_min',color=RED), use_container_width=True)
        section_close()
    c,d = st.columns(2)
    with c:
        section_open('Rush-hour exposure','Who is booking in harder operating windows.')
        rh = view.groupby('country', as_index=False)['rush_hour_share'].mean(); rh['rush_hour_pct']=rh['rush_hour_share']*100
        st.altair_chart(bar_chart(rh,'country','rush_hour_pct',color=GRAB_GREEN,y_title='Rush-hour %'), use_container_width=True)
        section_close()
    with d:
        section_open('Low-supply exposure','Share of users exposed to thin supply conditions.')
        ls = view.groupby('country', as_index=False)['low_supply_zone_share'].mean(); ls['low_supply_pct']=ls['low_supply_zone_share']*100
        st.altair_chart(bar_chart(ls,'country','low_supply_pct',color=TEAL,y_title='Low-supply %'), use_container_width=True)
        section_close()


def diagnostic_ps1(view):
    a,b = st.columns(2)
    with a:
        section_open('Risk drivers by tier','Booking risk and failure move with driver quality.')
        diag = view.groupby('assigned_driver_tier', as_index=False)[['booking_risk_score','failed_booking_rate_90d','eta_gap_min']].mean().melt('assigned_driver_tier', var_name='Metric', value_name='Value')
        diag.loc[diag['Metric']=='failed_booking_rate_90d','Value'] *= 100
        st.altair_chart(grouped_bar(diag,'assigned_driver_tier','Value','Metric',palette=[GRAB_GREEN,TEAL,RED]), use_container_width=True)
        section_close()
    with b:
        section_open('Customer value exposure','High-value customers should face lower failure risk, not higher.')
        val = view.groupby('customer_value_tier', as_index=False)[['bad_booking_label','booking_risk_score','trust_score']].mean()
        val['bad_booking_label'] *= 100
        melt = val.melt('customer_value_tier', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(melt,'customer_value_tier','Value','Metric',palette=[RED,TEAL,GRAB_GREEN]), use_container_width=True)
        section_close()
    c,d = st.columns(2)
    with c:
        section_open('Supply vs failure','Higher low-supply exposure aligns with higher failed booking rate.')
        tmp = view.copy()
        tmp['supply_band'] = pd.cut(tmp['low_supply_zone_share'], bins=[0,0.2,0.35,0.5,1], labels=['Very low','Low','Medium','High'], include_lowest=True)
        grp = tmp.groupby('supply_band', as_index=False)['bad_booking_label'].mean(); grp['bad_booking_pct']=grp['bad_booking_label']*100
        st.altair_chart(bar_chart(grp,'supply_band','bad_booking_pct',color=AMBER,y_title='Bad booking %'), use_container_width=True)
        section_close()
    with d:
        section_open('ETA miss vs trust','Wider ETA miss erodes trust directly.')
        st.altair_chart(scatter_chart(view,'eta_gap_min','trust_score',size='refund_delay_days_avg',color_field='assigned_driver_tier',palette=[GRAB_GREEN,TEAL,RED],tooltip=['customer_id','eta_gap_min','trust_score','refund_delay_days_avg','assigned_driver_tier']), use_container_width=True)
        section_close()


def predictive_ps1(view):
    a,b = st.columns(2)
    with a:
        section_open('Booking risk distribution','Portfolio spread of predicted booking risk.')
        rb = band_counts(view['booking_risk_score'], [0,40,55,70,100], ['Low','Medium','High','Critical'], 'Risk band')
        st.altair_chart(bar_chart(rb,'Risk band','Customers',color=GRAB_GREEN), use_container_width=True)
        section_close()
        section_open('Future failure candidates','Customers most likely to experience the next broken booking.')
        pred = top_rows(view,['customer_id','country','booking_risk_score','failed_booking_rate_90d','assigned_driver_tier','customer_value_tier'],['booking_risk_score'],[False],15)
        st.dataframe(pred, use_container_width=True, hide_index=True)
        section_close()
    with b:
        section_open('Risk by operational context','Predicted risk by rush-hour and late-night exposure.')
        tmp = view.copy(); tmp['rush_band'] = pd.cut(tmp['rush_hour_share'], bins=[0,0.25,0.45,1], labels=['Low','Medium','High'], include_lowest=True)
        out = tmp.groupby('rush_band', as_index=False)[['booking_risk_score','bad_booking_label']].mean()
        out['bad_booking_pct']=out['bad_booking_label']*100
        melt = out.melt('rush_band', value_vars=['booking_risk_score','bad_booking_pct'], var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(melt,'rush_band','Value','Metric',palette=[TEAL,RED]), use_container_width=True)
        section_close()
        section_open('High-risk value pool','How much CLV sits inside the high-risk bucket.')
        tmp2 = view.copy(); tmp2['risk_band']=pd.cut(tmp2['booking_risk_score'], bins=[0,40,55,70,100], labels=['Low','Medium','High','Critical'], include_lowest=True)
        value = tmp2.groupby('risk_band', as_index=False)['clv_12m_usd'].mean()
        st.altair_chart(bar_chart(value,'risk_band','clv_12m_usd',color=GRAB_GREEN_DARK,y_title='Avg CLV'), use_container_width=True)
        section_close()


def prescriptive_ps1(view):
    high_value = view[(view['booking_risk_score']>=70) & (view['customer_value_tier']=='High-Value')]
    zone_ops = view[(view['low_supply_zone_share']>=0.45) & (view['rush_hour_share']>=0.45)]
    driver_watch = view[view['assigned_driver_tier']=='High-Risk']
    a,b = st.columns([.95,1.05])
    with a:
        st.markdown(f"""
        <div class='action-box green'><h4>Reliable-driver override</h4><p>Target group: {len(high_value)} high-value customers with booking risk above 70.</p><p>Action: force assignment to Reliable tier and auto-enable service recovery.</p></div>
        <div class='action-box amber'><h4>Zone incentive trigger</h4><p>Target group: {len(zone_ops)} bookings in high rush-hour and low-supply conditions.</p><p>Action: deploy localized supply incentives and stricter dispatch rules.</p></div>
        <div class='action-box red'><h4>Driver accountability review</h4><p>Target group: {len(driver_watch)} High-Risk tier exposures.</p><p>Action: warning queue, limited visibility, or suspension review.</p></div>
        """, unsafe_allow_html=True)
    with b:
        section_open('Actionable queue','Prescriptive queue sorted by business importance.')
        action = top_rows(view,['customer_id','country','customer_value_tier','booking_risk_score','assigned_driver_tier','recommended_action','clv_12m_usd'],['booking_risk_score','clv_12m_usd'],[False,False],15)
        st.dataframe(action, use_container_width=True, hide_index=True)
        section_close()
        section_open('Expected effect by action type','Where the largest recoverable value sits.')
        eff = view.groupby('recommended_action', as_index=False)[['clv_12m_usd','trust_score']].mean().sort_values('clv_12m_usd', ascending=False).head(8).melt('recommended_action', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(eff,'recommended_action','Value','Metric',palette=[GRAB_GREEN,TEAL]), use_container_width=True)
        section_close()



def master_ps2(view):
    c1,c2,c3,c4,c5 = st.columns(5)
    kpi_card(c1,'Single-service share',f"{(view['services_used_count']<=1).mean()*100:.1f}%",'Users not acting like super-app customers')
    kpi_card(c2,'3+ services share',f"{(view['services_used_count']>=3).mean()*100:.1f}%",'Higher ecosystem depth')
    kpi_card(c3,'Cross-sell propensity',f"{view['cross_sell_propensity'].mean():.1f}",'Likelihood of next-service adoption')
    kpi_card(c4,'Churn risk',f"{view['churn_risk_score'].mean():.1f}",'Portfolio average')
    kpi_card(c5,'12m CLV',f"${view['clv_12m_usd'].mean():.0f}",'Average customer value')

    single_share = float((view['services_used_count'] <= 1).mean() * 100)
    service_depth = float(view['services_used_count'].mean())
    crosssell = float(view['cross_sell_propensity'].mean())
    churn = float(view['churn_risk_score'].mean())
    consent = float(view['pdpa_contact_ok'].mean() * 100)
    promo = float(view['promo_response_rate'].mean() * 100)
    primary_service = first_mode(view['primary_service'], 'Grab')
    next_best = first_mode(view['next_best_service'], 'GrabUnlimited')
    focus_segment = first_mode(view['superapp_segment'], 'At-Risk Single-App User')

    improved_single = clamp(single_share * (1 - min(0.30, 0.12 + crosssell / 250 + consent / 500)), 8.0, single_share)
    improved_cross = clamp(crosssell + 10 + promo / 10 + max(0, 2 - service_depth) * 4, crosssell, 100.0)
    improved_churn = clamp(churn - (8 + consent / 25 + max(0, 2 - service_depth) * 5), 8.0, churn)
    improved_depth = clamp(service_depth + 0.65, service_depth, 4.0)

    bundle_save = int(round(8 + improved_cross / 10))
    points_boost = int(round(2 + improved_depth))
    state = st.session_state.get('ps2_demo_state', 'current')

    problem_screen = f"""
    <div class='phone-status'><span>9:41</span><span>5G 92%</span></div>
    <div class='phone-header'>
        <div class='phone-brand'>Grab</div>
        <div class='phone-screen-title'>Home</div>
        <div class='phone-subtitle'>Customer mostly anchored in {primary_service}</div>
    </div>
    <div class='phone-panel'>
        <div class='phone-row'><span>Services</span><span class='phone-chip neutral'>Generic home</span></div>
        <div class='phone-service-grid'>
            <div class='phone-service active'>{primary_service}</div>
            <div class='phone-service'>Mart</div>
            <div class='phone-service'>Ride</div>
            <div class='phone-service'>Pay</div>
        </div>
    </div>
    <div class='phone-panel'>
        <div class='phone-row'><span>Offer shown today</span><span class='phone-chip warn'>Low relevance</span></div>
        <div class='phone-copy'>The user sees a broad discount, but there is no clear next-best-service journey even though churn pressure is {churn:.1f} and single-service dependency is still {single_share:.1f}%.</div>
        <div class='phone-mini-kpis'>
            <div class='phone-kpi'><span>Services used</span><strong>{service_depth:.1f}</strong></div>
            <div class='phone-kpi'><span>Cross-sell</span><strong>{crosssell:.0f}/100</strong></div>
        </div>
    </div>
    <div class='phone-panel soft'>
        <div class='phone-row'><span>Why growth stalls</span><span class='phone-chip danger'>Friction</span></div>
        <div class='phone-copy'>The customer is treated like everyone else, instead of being nudged toward {next_best} when the data already suggests that route.</div>
    </div>
    <div class='phone-cta muted'>Browse offers</div>
    """

    improved_screen = f"""
    <div class='phone-status'><span>9:41</span><span>5G 92%</span></div>
    <div class='phone-header'>
        <div class='phone-brand'>Grab</div>
        <div class='phone-screen-title'>For you</div>
        <div class='phone-subtitle'>Next-best-service offer shown only where consent and propensity are strong</div>
    </div>
    <div class='phone-panel'>
        <div class='phone-row'><span>Personalised growth card</span><span class='phone-chip success'>Best next step</span></div>
        <div class='phone-offer'><small>Based on your {primary_service} habits</small><strong>Try {next_best}</strong>Save {bundle_save}% with a curated bundle and earn {points_boost}x points on your next order.</div>
        <div class='phone-mini-kpis'>
            <div class='phone-kpi'><span>Cross-sell</span><strong>{improved_cross:.0f}/100</strong></div>
            <div class='phone-kpi'><span>Depth</span><strong>{improved_depth:.1f}</strong></div>
        </div>
    </div>
    <div class='phone-panel soft'>
        <div class='phone-row'><span>What improved</span><span class='phone-chip success'>Relevant</span></div>
        <div class='phone-copy'>The app now shows a consent-safe, next-best-service path instead of a generic promo. That makes the home screen feel smarter and increases the chance of a second habit forming.</div>
    </div>
    <div class='phone-cta'>Unlock my bundle</div>
    """

    story_payload = {
        'kicker': 'Customer app demo · Super-App Growth',
        'current_title': 'Current experience: the home feed feels generic',
        'current_text': 'The customer opens Grab and sees a broad offer, but nothing in the app naturally guides them toward the most relevant next service or a deeper ecosystem habit.',
        'current_status': 'Why it feels weak: the experience looks promotional, not personal.',
        'improved_title': 'Best case: the app feels like a smart personal assistant',
        'improved_text': 'The improved home feed makes discovery feel native to the product, surfacing the right next service at the right time instead of pushing a generic discount.',
        'improved_status': 'What changed: consent-safe next-best-service logic turns the home screen into the intervention itself.',
        'interval_ms': 3200,
        'metrics': [
            {'label': 'Single-service share', 'current': f'{single_share:.1f}%', 'improved': f'{improved_single:.1f}%', 'current_note': 'Customers still behaving like one-service users.', 'improved_note': 'Lower once the app encourages the next habit.'},
            {'label': 'Cross-sell propensity', 'current': f'{crosssell:.0f}/100', 'improved': f'{improved_cross:.0f}/100', 'current_note': 'Likelihood of next-service adoption today.', 'improved_note': 'Higher with relevant in-app discovery.'},
            {'label': 'Churn risk', 'current': f'{churn:.1f}', 'improved': f'{improved_churn:.1f}', 'current_note': 'Drop-off pressure across the portfolio.', 'improved_note': 'Lower when depth and relevance improve.'},
        ],
        'current_screen': problem_screen,
        'improved_screen': improved_screen,
    }
    render_story_demo('ps2_story', story_payload, height=800)

    a,b = st.columns(2)
    with a:
        section_open('Segment command view','Current shape of the customer base.')
        seg = view['superapp_segment'].value_counts().reset_index(); seg.columns=['superapp_segment','Customers']
        st.altair_chart(bar_chart(seg,'superapp_segment','Customers',color=GRAB_GREEN), use_container_width=True)
        section_close()
        section_open('Service depth by country','How multi-service behavior differs by market.')
        depth = view.groupby('country', as_index=False)['services_used_count'].mean()
        st.altair_chart(bar_chart(depth,'country','services_used_count',color=TEAL), use_container_width=True)
        section_close()
    with b:
        section_open('Cross-sell vs churn','Master relationship between growth and churn pressure.')
        st.altair_chart(scatter_chart(view,'cross_sell_propensity','churn_risk_score',size='clv_12m_usd',color_field='customer_value_tier',palette=[GRAB_GREEN,TEAL,AMBER],tooltip=['customer_id','cross_sell_propensity','churn_risk_score','clv_12m_usd','customer_value_tier']), use_container_width=True)
        section_close()
        section_open('Top next-service routes','Most frequent next service opportunities.')
        flow = view.groupby(['primary_service','next_best_service'], as_index=False).size().rename(columns={'size':'Customers'}).sort_values('Customers', ascending=False)
        st.dataframe(flow.head(12), use_container_width=True, hide_index=True)
        section_close()

    x,y = st.columns([1.1,.9])
    with x:
        section_open('Value at risk','Higher churn pressure combined with low service depth is the key growth gap.')
        seg2 = view.groupby('superapp_segment', as_index=False)[['services_used_count','churn_risk_score','clv_12m_usd']].mean().melt('superapp_segment', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(seg2,'superapp_segment','Value','Metric',palette=[GRAB_GREEN,RED,TEAL]), use_container_width=True)
        section_close()
    with y:
        st.markdown(f"""
        <div class='action-box green'><h4>Growth priority</h4><p>Cross-sell only where consent and high propensity both exist.</p><p>Why this improves conversion without creating compliance waste.</p></div>
        <div class='action-box amber'><h4>Retention priority</h4><p>Re-activate fading single-service users before inactivity hardens into churn.</p><p>Why recency and narrow usage are early warning signs.</p></div>
        <div class='action-box red'><h4>Value protection</h4><p>Protect power users with bundles and priority support.</p><p>Why they carry the strongest lifetime value and ecosystem habit.</p></div>
        """, unsafe_allow_html=True)


def descriptive_ps2(view):
    a,b = st.columns(2)
    with a:
        section_open('Super-app segment split','Current distribution of customer profiles.')
        seg = view['superapp_segment'].value_counts().reset_index(); seg.columns=['superapp_segment','Customers']
        st.altair_chart(bar_chart(seg,'superapp_segment','Customers',color=GRAB_GREEN), use_container_width=True)
        section_close()
        section_open('Primary service split','Where users currently anchor.')
        pri = view['primary_service'].value_counts().reset_index(); pri.columns=['primary_service','Customers']
        st.altair_chart(bar_chart(pri,'primary_service','Customers',color=TEAL), use_container_width=True)
        section_close()
    with b:
        section_open('Service depth distribution','How many services customers use today.')
        depth = view['services_used_count'].value_counts().sort_index().reset_index(); depth.columns=['services_used_count','Customers']
        st.altair_chart(bar_chart(depth,'services_used_count','Customers',color=AMBER,x_type='Q'), use_container_width=True)
        section_close()
        section_open('Customer value tier mix','Value segmentation of the current base.')
        vt = view['customer_value_tier'].value_counts().reset_index(); vt.columns=['customer_value_tier','Customers']
        st.altair_chart(bar_chart(vt,'customer_value_tier','Customers',color=GRAB_GREEN_DARK), use_container_width=True)
        section_close()
    c,d = st.columns(2)
    with c:
        section_open('Country service depth','Average services used by market.')
        cs = view.groupby('country', as_index=False)['services_used_count'].mean()
        st.altair_chart(bar_chart(cs,'country','services_used_count',color=GRAB_GREEN), use_container_width=True)
        section_close()
    with d:
        section_open('Promotion response by segment','Which segments react most to offers.')
        promo = view.groupby('superapp_segment', as_index=False)['promo_response_rate'].mean(); promo['promo_pct']=promo['promo_response_rate']*100
        st.altair_chart(bar_chart(promo,'superapp_segment','promo_pct',color=AMBER,y_title='Promo response %'), use_container_width=True)
        section_close()


def diagnostic_ps2(view):
    a,b = st.columns(2)
    with a:
        section_open('Recency and churn','Dormancy explains much of the churn signal.')
        rec = view.groupby('superapp_segment', as_index=False)[['recency_days','churn_risk_score']].mean().melt('superapp_segment', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(rec,'superapp_segment','Value','Metric',palette=[AMBER,RED]), use_container_width=True)
        section_close()
    with b:
        section_open('Consent and cross-sell','Valid contact rights shape who should be targeted.')
        consent = view.groupby('pdpa_contact_ok', as_index=False)[['cross_sell_propensity','churn_risk_score']].mean()
        consent['Consent'] = consent['pdpa_contact_ok'].map({0:'No consent',1:'Consent'})
        cm = consent.melt('Consent', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(cm,'Consent','Value','Metric',palette=[GRAB_GREEN,RED]), use_container_width=True)
        section_close()
    c,d = st.columns(2)
    with c:
        section_open('Value versus service depth','More service usage generally aligns with stronger value.')
        st.altair_chart(scatter_chart(view,'services_used_count','clv_12m_usd',size='churn_risk_score',color_field='superapp_segment',tooltip=['customer_id','services_used_count','clv_12m_usd','churn_risk_score','superapp_segment']), use_container_width=True)
        section_close()
    with d:
        section_open('Segment scorecard','Where churn, cross-sell, and CLV diverge most.')
        score = view.groupby('superapp_segment', as_index=False)[['cross_sell_propensity','churn_risk_score','clv_12m_usd','services_used_count']].mean().round(1)
        st.dataframe(score, use_container_width=True, hide_index=True)
        section_close()


def predictive_ps2(view):
    a,b = st.columns(2)
    with a:
        section_open('Churn risk bands','Share of users by predicted churn intensity.')
        bands = band_counts(view['churn_risk_score'], [0,35,50,65,100], ['Low','Medium','High','Critical'], 'Churn band')
        st.altair_chart(bar_chart(bands,'Churn band','Customers',color=RED), use_container_width=True)
        section_close()
        section_open('Top churn candidates','Users likely to leave in the next 30 days.')
        top = top_rows(view,['customer_id','country','superapp_segment','churn_risk_score','recency_days','services_used_count','clv_12m_usd'],['churn_risk_score','recency_days'],[False,False],15)
        st.dataframe(top, use_container_width=True, hide_index=True)
        section_close()
    with b:
        section_open('Cross-sell bands','How many users are realistically ready for the next service.')
        cb = band_counts(view['cross_sell_propensity'], [0,40,55,70,100], ['Low','Medium','High','Priority'], 'Cross-sell band')
        st.altair_chart(bar_chart(cb,'Cross-sell band','Customers',color=GRAB_GREEN), use_container_width=True)
        section_close()
        section_open('Next-best service by primary anchor','Predicted growth path from the current main service.')
        nxt = view.groupby(['primary_service','next_best_service'], as_index=False).size().rename(columns={'size':'Customers'}).sort_values('Customers', ascending=False)
        heat = nxt.copy(); heat['pair'] = heat['Customers']
        st.altair_chart(heatmap_chart(heat,'primary_service','next_best_service','pair',scheme='tealblues'), use_container_width=True)
        section_close()


def prescriptive_ps2(view):
    cross_sell = view[(view['cross_sell_propensity']>=65) & (view['pdpa_contact_ok']==1) & (view['churn_risk_score']<58)]
    fading = view[view['superapp_segment']=='At-Risk Single-App User']
    power = view[view['superapp_segment']=='Power User']
    a,b = st.columns([.95,1.05])
    with a:
        st.markdown(f"""
        <div class='action-box green'><h4>Consent-safe cross-sell</h4><p>Target group: {len(cross_sell)} users with strong next-service propensity and valid contact rights.</p><p>Action: push next-best-service offer instead of a generic discount.</p></div>
        <div class='action-box amber'><h4>Fading-user rescue</h4><p>Target group: {len(fading)} at-risk single-app users.</p><p>Action: send primary-service reactivation tied to the user’s known habit.</p></div>
        <div class='action-box red'><h4>Power-user protection</h4><p>Target group: {len(power)} high-depth customers.</p><p>Action: bundle benefits, priority support, and finance upsell.</p></div>
        """, unsafe_allow_html=True)
    with b:
        section_open('Action queue','Who should be targeted first and why.')
        q = top_rows(view,['customer_id','country','superapp_segment','next_best_service','cross_sell_propensity','churn_risk_score','recommended_action','clv_12m_usd'],['cross_sell_propensity','clv_12m_usd'],[False,False],15)
        st.dataframe(q, use_container_width=True, hide_index=True)
        section_close()
        section_open('Action value by segment','Where the most recoverable or expandable value sits.')
        act = view.groupby('superapp_segment', as_index=False)[['clv_12m_usd','cross_sell_propensity','churn_risk_score']].mean().melt('superapp_segment', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(act,'superapp_segment','Value','Metric',palette=[TEAL,GRAB_GREEN,RED]), use_container_width=True)
        section_close()



def master_ps3(view):
    c1,c2,c3,c4,c5 = st.columns(5)
    kpi_card(c1,'Avg surge',f"{view['avg_surge_multiplier'].mean():.2f}x",'Average multiplier')
    kpi_card(c2,'Extreme surge exposure',f"{view['extreme_surge_exposure_rate'].mean()*100:.1f}%",'Exposure to sharp spikes')
    kpi_card(c3,'Abnormal charge flags',f"{view['abnormal_charge_flags_90d'].mean():.1f}",'Potential billing anomalies')
    kpi_card(c4,'Fairness score',f"{view['fare_fairness_score'].mean():.1f}",'Higher is better')
    kpi_card(c5,'Refund recovery',f"{view['proactive_refund_rate'].mean()*100:.1f}%",'Proactive service recovery')

    surge = float(view['avg_surge_multiplier'].mean())
    extreme = float(view['extreme_surge_exposure_rate'].mean() * 100)
    abnormal = float(view['abnormal_charge_flags_90d'].mean())
    fairness = float(view['fare_fairness_score'].mean())
    refund = float(view['proactive_refund_rate'].mean() * 100)
    sensitivity = first_mode(view['price_sensitivity_segment'], 'Highly Sensitive')
    cap_now = float(pd.to_numeric(view['surge_cap_recommendation'], errors='coerce').dropna().mean()) if not pd.to_numeric(view['surge_cap_recommendation'], errors='coerce').dropna().empty else 1.50

    improved_surge = clamp(min(1.50, cap_now, surge - 0.12 if surge > 1.50 else surge), 1.10, surge)
    improved_fairness = clamp(fairness + max(0, surge - improved_surge) * 24 + min(abnormal, 4) * 1.5 + 5.0, fairness, 100.0)
    improved_abnormal = clamp(abnormal - 0.9, 0.0, abnormal)
    improved_refund = clamp(refund + 18.0, refund, 100.0)

    base_fare = 11.80
    current_total = base_fare * surge + 0.65 * abnormal + 1.30
    improved_total = base_fare * improved_surge + 0.90
    save_amount = max(0.5, current_total - improved_total)
    state = st.session_state.get('ps3_demo_state', 'current')

    problem_screen = f"""
    <div class='phone-status'><span>9:41</span><span>5G 92%</span></div>
    <div class='phone-header'>
        <div class='phone-brand'>Grab</div>
        <div class='phone-screen-title'>Fare estimate</div>
        <div class='phone-subtitle'>{sensitivity} customer · price check before booking</div>
    </div>
    <div class='phone-panel'>
        <div class='phone-row'><span>Ride total</span><span class='phone-price'>${current_total:.2f}</span></div>
        <div class='phone-banner warn'>Surge is {surge:.2f}x right now. Some extras may still change after the trip.</div>
        <div class='phone-fare-line'><span>Base fare</span><span>${base_fare:.2f}</span></div>
        <div class='phone-fare-line'><span>Surge multiplier</span><span>{surge:.2f}x</span></div>
        <div class='phone-fare-line'><span>Other fees</span><span>Calculated later</span></div>
    </div>
    <div class='phone-panel soft'>
        <div class='phone-row'><span>What the customer feels</span><span class='phone-chip danger'>Unfair</span></div>
        <div class='phone-copy'>Fairness score is only {fairness:.1f}/100 while abnormal charge flags average {abnormal:.1f}. The customer sees a high price, but not a strong explanation or recovery promise.</div>
        <div class='phone-mini-kpis'>
            <div class='phone-kpi'><span>Extreme surge</span><strong>{extreme:.1f}%</strong></div>
            <div class='phone-kpi'><span>Refund recovery</span><strong>{refund:.0f}%</strong></div>
        </div>
    </div>
    <div class='phone-cta muted'>Review fare</div>
    """

    improved_screen = f"""
    <div class='phone-status'><span>9:41</span><span>5G 92%</span></div>
    <div class='phone-header'>
        <div class='phone-brand'>Grab</div>
        <div class='phone-screen-title'>Protected pricing</div>
        <div class='phone-subtitle'>Fairness guardrail applied for sensitive customers</div>
    </div>
    <div class='phone-panel'>
        <div class='phone-row'><span>Ride total</span><span class='phone-price'>${improved_total:.2f}</span></div>
        <div class='phone-banner success'>Surge capped at {improved_surge:.2f}x, full fare shown up front, and refund review is triggered automatically if anything looks abnormal.</div>
        <div class='phone-fare-line'><span>Base fare</span><span>${base_fare:.2f}</span></div>
        <div class='phone-fare-line'><span>Capped surge</span><span>{improved_surge:.2f}x</span></div>
        <div class='phone-fare-line'><span>Protection</span><span>Refund eligible</span></div>
    </div>
    <div class='phone-panel soft'>
        <div class='phone-row'><span>What improved</span><span class='phone-chip success'>Transparent</span></div>
        <div class='phone-copy'>The app now explains the fare clearly, caps surge for sensitive users, and shows a cheaper alternative timing option that saves about ${save_amount:.2f}.</div>
        <div class='phone-mini-kpis'>
            <div class='phone-kpi'><span>Fairness</span><strong>{improved_fairness:.0f}/100</strong></div>
            <div class='phone-kpi'><span>Refund recovery</span><strong>{improved_refund:.0f}%</strong></div>
        </div>
    </div>
    <div class='phone-cta'>Book with fare protection</div>
    """

    story_payload = {
        'kicker': 'Customer app demo · Pricing Fairness',
        'current_title': 'Current experience: pricing feels like a shock',
        'current_text': 'The customer sees a high fare with limited explanation, unclear fee logic, and weak confidence that Grab will correct abnormal charges quickly.',
        'current_status': 'Why it feels unfair: price shock appears before trust protection appears.',
        'improved_title': 'Best case: the checkout explains and protects the fare',
        'improved_text': 'The improved flow makes pricing feel native and trustworthy by capping the shock, clarifying the fare, and making refund protection visible before confirmation.',
        'improved_status': 'What changed: surge guardrails and proactive refund logic turn a stressful fare screen into a confident checkout.',
        'interval_ms': 3200,
        'metrics': [
            {'label': 'Avg surge', 'current': f'{surge:.2f}x', 'improved': f'{improved_surge:.2f}x', 'current_note': 'Pricing pressure the customer sees now.', 'improved_note': 'Lower after the fairness guardrail.'},
            {'label': 'Fairness score', 'current': f'{fairness:.0f}/100', 'improved': f'{improved_fairness:.0f}/100', 'current_note': 'Trust in the fare experience today.', 'improved_note': 'Higher with clearer fare logic and recovery.'},
            {'label': 'Abnormal charge flags', 'current': f'{abnormal:.1f}', 'improved': f'{improved_abnormal:.1f}', 'current_note': 'Customers exposed to billing doubt.', 'improved_note': 'Lower with proactive review and refund triggers.'},
        ],
        'current_screen': problem_screen,
        'improved_screen': improved_screen,
    }
    render_story_demo('ps3_story', story_payload, height=800)

    a,b = st.columns(2)
    with a:
        section_open('Fairness by segment','Master view of who experiences pricing strain.')
        fair = view.groupby('price_sensitivity_segment', as_index=False)['fare_fairness_score'].mean()
        st.altair_chart(bar_chart(fair,'price_sensitivity_segment','fare_fairness_score',color=GRAB_GREEN), use_container_width=True)
        section_close()
        section_open('Surge by country','Current pricing intensity by market.')
        sur = view.groupby('country', as_index=False)['avg_surge_multiplier'].mean()
        st.altair_chart(bar_chart(sur,'country','avg_surge_multiplier',color=AMBER), use_container_width=True)
        section_close()
    with b:
        section_open('Shock versus fairness','Pricing trust weakens as shock and anomaly exposure rise.')
        st.altair_chart(scatter_chart(view,'avg_surge_multiplier','fare_fairness_score',size='abnormal_charge_flags_90d',color_field='price_sensitivity_segment',palette=[RED,AMBER,GRAB_GREEN],tooltip=['customer_id','avg_surge_multiplier','fare_fairness_score','abnormal_charge_flags_90d','price_sensitivity_segment']), use_container_width=True)
        section_close()
        section_open('Pricing review queue','Users most likely to feel overcharged or churn after a shock.')
        q = top_rows(view, ['customer_id','country','price_sensitivity_segment','avg_surge_multiplier','abnormal_charge_flags_90d','fare_fairness_score','churn_risk_score'], ['abnormal_charge_flags_90d','churn_risk_score'], [False, False], 12)
        st.dataframe(q, use_container_width=True, hide_index=True)
        section_close()

    x,y = st.columns([1.1,.9])
    with x:
        section_open('Policy comparison','Sensitivity segment, elasticity, and recommended cap together.')
        policy = view.groupby('price_sensitivity_segment', as_index=False)[['avg_surge_multiplier','price_elasticity_score','surge_cap_recommendation','fare_fairness_score']].mean().melt('price_sensitivity_segment', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(policy,'price_sensitivity_segment','Value','Metric',palette=[AMBER,RED,TEAL,GRAB_GREEN]), use_container_width=True)
        section_close()
    with y:
        st.markdown(f"""
        <div class='action-box green'><h4>Pricing guardrail</h4><p>Cap surge at 1.5x for highly sensitive users.</p><p>Why fairness erosion and churn risk are highest here.</p></div>
        <div class='action-box amber'><h4>Recovery rule</h4><p>Trigger proactive refund review for repeated abnormal charge flags.</p><p>Why this reduces reputational and regulatory exposure.</p></div>
        <div class='action-box red'><h4>Premium logic</h4><p>Allow higher surge only where convenience-first segments receive service assurance.</p><p>Why higher price without reliability becomes hard to defend.</p></div>
        """, unsafe_allow_html=True)


def descriptive_ps3(view):
    a,b = st.columns(2)
    with a:
        section_open('Price sensitivity mix','Current customer split by price sensitivity.')
        ps = view['price_sensitivity_segment'].value_counts().reset_index(); ps.columns=['price_sensitivity_segment','Customers']
        st.altair_chart(bar_chart(ps,'price_sensitivity_segment','Customers',color=AMBER), use_container_width=True)
        section_close()
        section_open('Waiting fee burden','Average waiting-fee count by country.')
        wf = view.groupby('country', as_index=False)['waiting_fee_count_90d'].mean()
        st.altair_chart(bar_chart(wf,'country','waiting_fee_count_90d',color=RED), use_container_width=True)
        section_close()
    with b:
        section_open('Fairness by country','Market-level perception of pricing fairness.')
        ff = view.groupby('country', as_index=False)['fare_fairness_score'].mean()
        st.altair_chart(bar_chart(ff,'country','fare_fairness_score',color=GRAB_GREEN), use_container_width=True)
        section_close()
        section_open('Abnormal charges by segment','Where charge anomalies cluster.')
        ab = view.groupby('price_sensitivity_segment', as_index=False)['abnormal_charge_flags_90d'].mean()
        st.altair_chart(bar_chart(ab,'price_sensitivity_segment','abnormal_charge_flags_90d',color=TEAL), use_container_width=True)
        section_close()
    c,d = st.columns(2)
    with c:
        section_open('Surge intensity distribution','Current pricing pressure across user segments.')
        su = view.groupby('price_sensitivity_segment', as_index=False)['avg_surge_multiplier'].mean()
        st.altair_chart(bar_chart(su,'price_sensitivity_segment','avg_surge_multiplier',color=AMBER), use_container_width=True)
        section_close()
    with d:
        section_open('Refund recovery by segment','Where proactive recovery is currently concentrated.')
        rr = view.groupby('price_sensitivity_segment', as_index=False)['proactive_refund_rate'].mean(); rr['refund_pct']=rr['proactive_refund_rate']*100
        st.altair_chart(bar_chart(rr,'price_sensitivity_segment','refund_pct',color=GRAB_GREEN_DARK,y_title='Refund %'), use_container_width=True)
        section_close()


def diagnostic_ps3(view):
    a,b = st.columns(2)
    with a:
        section_open('Correlation view','Surge, hidden fees, and anomalies jointly reduce fairness.')
        corr = view[['avg_surge_multiplier','waiting_fee_count_90d','abnormal_charge_flags_90d','fare_fairness_score','churn_risk_score']].corr().reset_index().melt('index', var_name='metric_2', value_name='correlation')
        corr = corr.rename(columns={'index':'metric_1'})
        st.altair_chart(heatmap_chart(corr,'metric_1','metric_2','correlation',scheme='redyellowgreen'), use_container_width=True)
        section_close()
    with b:
        section_open('Elasticity by segment','Demand response changes by customer sensitivity.')
        el = view.groupby('price_sensitivity_segment', as_index=False)['price_elasticity_score'].mean()
        st.altair_chart(bar_chart(el,'price_sensitivity_segment','price_elasticity_score',color=RED), use_container_width=True)
        section_close()
    c,d = st.columns(2)
    with c:
        section_open('Fairness versus churn','Lower fairness tends to align with higher churn pressure.')
        st.altair_chart(scatter_chart(view,'fare_fairness_score','churn_risk_score',size='avg_surge_multiplier',color_field='price_sensitivity_segment',palette=[RED,AMBER,GRAB_GREEN],tooltip=['customer_id','fare_fairness_score','churn_risk_score','avg_surge_multiplier','price_sensitivity_segment']), use_container_width=True)
        section_close()
    with d:
        section_open('Abnormal charge impact','Users with repeated flags see materially weaker fairness.')
        tmp = view.copy(); tmp['flag_band'] = pd.cut(tmp['abnormal_charge_flags_90d'], bins=[-1,0,2,4,20], labels=['None','Low','Medium','High'])
        grp = tmp.groupby('flag_band', as_index=False)[['fare_fairness_score','churn_risk_score']].mean().melt('flag_band', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(grp,'flag_band','Value','Metric',palette=[GRAB_GREEN,RED]), use_container_width=True)
        section_close()


def predictive_ps3(view):
    a,b = st.columns(2)
    with a:
        section_open('Fairness risk bands','How many users fall into weak pricing-trust conditions.')
        bands = band_counts(view['fare_fairness_score'], [0,45,60,75,100], ['Critical','High risk','Watch','Healthy'], 'Fairness band')
        st.altair_chart(bar_chart(bands,'Fairness band','Customers',color=RED), use_container_width=True)
        section_close()
        section_open('Pricing risk candidates','Users most likely to react negatively to pricing shock.')
        top = top_rows(view,['customer_id','country','price_sensitivity_segment','avg_surge_multiplier','abnormal_charge_flags_90d','fare_fairness_score','churn_risk_score'],['fare_fairness_score','churn_risk_score'],[True,False],15)
        st.dataframe(top, use_container_width=True, hide_index=True)
        section_close()
    with b:
        section_open('Cap recommendation by segment','Predicted pricing guardrails from elasticity and fairness signals.')
        cap = view.groupby('price_sensitivity_segment', as_index=False)[['surge_cap_recommendation','avg_surge_multiplier','churn_risk_score']].mean().melt('price_sensitivity_segment', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(cap,'price_sensitivity_segment','Value','Metric',palette=[GRAB_GREEN,AMBER,RED]), use_container_width=True)
        section_close()
        section_open('Exposure ladder','How extreme surge exposure escalates by segment.')
        ex = view.groupby('price_sensitivity_segment', as_index=False)[['extreme_surge_exposure_rate','proactive_refund_rate']].mean()
        ex['extreme_surge_pct'] = ex['extreme_surge_exposure_rate']*100
        ex['refund_pct'] = ex['proactive_refund_rate']*100
        em = ex[['price_sensitivity_segment','extreme_surge_pct','refund_pct']].melt('price_sensitivity_segment', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(em,'price_sensitivity_segment','Value','Metric',palette=[AMBER,GRAB_GREEN]), use_container_width=True)
        section_close()


def prescriptive_ps3(view):
    sensitive = view[(view['price_sensitivity_segment']=='Highly Sensitive') & (view['avg_surge_multiplier']>=1.5)]
    abnormal_pool = view[view['abnormal_charge_flags_90d']>=3]
    convenience = view[(view['price_sensitivity_segment']=='Convenience-First') & (view['avg_surge_multiplier']>=1.7)]
    a,b = st.columns([.95,1.05])
    with a:
        st.markdown(f"""
        <div class='action-box green'><h4>Surge cap enforcement</h4><p>Target group: {len(sensitive)} highly sensitive users facing surge above 1.5x.</p><p>Action: cap price, show full fare up front, and display cheaper alternatives.</p></div>
        <div class='action-box amber'><h4>Abnormal charge recovery</h4><p>Target group: {len(abnormal_pool)} users with repeated charge anomalies.</p><p>Action: trigger review and proactive refund before complaint escalation.</p></div>
        <div class='action-box red'><h4>Premium pricing control</h4><p>Target group: {len(convenience)} convenience-first users with higher tolerance.</p><p>Action: allow higher surge only with service guarantee messaging.</p></div>
        """, unsafe_allow_html=True)
    with b:
        section_open('Pricing action queue','Who requires intervention first.')
        q = top_rows(view,['customer_id','country','price_sensitivity_segment','avg_surge_multiplier','abnormal_charge_flags_90d','surge_cap_recommendation','recommended_action'],['abnormal_charge_flags_90d','avg_surge_multiplier'],[False,False],15)
        st.dataframe(q, use_container_width=True, hide_index=True)
        section_close()
        section_open('Policy value view','Where fairness recovery protects the most value.')
        pol = view.groupby('price_sensitivity_segment', as_index=False)[['clv_12m_usd','fare_fairness_score','churn_risk_score']].mean().melt('price_sensitivity_segment', var_name='Metric', value_name='Value')
        st.altair_chart(grouped_bar(pol,'price_sensitivity_segment','Value','Metric',palette=[TEAL,GRAB_GREEN,RED]), use_container_width=True)
        section_close()


def render_problem(title, text, cls, funcs):
    problem_head(title, text, cls)
    subtabs = st.tabs(['Master','Descriptive','Diagnostic','Predictive','Prescriptive'])
    with subtabs[0]: funcs[0]()
    with subtabs[1]: funcs[1]()
    with subtabs[2]: funcs[2]()
    with subtabs[3]: funcs[3]()
    with subtabs[4]: funcs[4]()

uploaded = st.file_uploader('Upload CSV', type=['csv'])
df = load_data(uploaded)
header()

if df is None:
    st.warning('Dataset not found. Upload grab_superapp_synthetic.csv or place it beside app.py in the repo root.')
    st.stop()

view = filter_panel(df)
if len(view) == 0:
    st.warning('No rows match the selected filters.')
    st.stop()

main_tabs = st.tabs(['PS1 Driver Trust','PS2 Super-App Growth','PS3 Pricing Fairness'])
with main_tabs[0]:
    render_problem(
        'PS1 · Driver Trust and Failed Bookings',
        'Separate master, descriptive, diagnostic, predictive, and prescriptive views for booking failures, ETA misses, and driver reliability.',
        '',
        [lambda: master_ps1(view), lambda: descriptive_ps1(view), lambda: diagnostic_ps1(view), lambda: predictive_ps1(view), lambda: prescriptive_ps1(view)]
    )
with main_tabs[1]:
    render_problem(
        'PS2 · Super-App Growth and Single-Service Dependency',
        'Separate analytical views for adoption depth, churn exposure, next-best service opportunities, and intervention design.',
        'ps2',
        [lambda: master_ps2(view), lambda: descriptive_ps2(view), lambda: diagnostic_ps2(view), lambda: predictive_ps2(view), lambda: prescriptive_ps2(view)]
    )
with main_tabs[2]:
    render_problem(
        'PS3 · Pricing Fairness, Surge Shock, and Hidden Fees',
        'Separate analytical views for pricing intensity, fairness breakdown, anomaly detection, and pricing policy actions.',
        'ps3',
        [lambda: master_ps3(view), lambda: descriptive_ps3(view), lambda: diagnostic_ps3(view), lambda: predictive_ps3(view), lambda: prescriptive_ps3(view)]
    )
