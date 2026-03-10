from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Grab Decision Studio", page_icon="🟢", layout="wide", initial_sidebar_state="collapsed")
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = "grab_superapp_synthetic.csv"
GRAB_GREEN = "#00B14F"
GRAB_GREEN_2 = "#02C75A"
GRAB_GREEN_SOFT = "#E9FFF2"
GRAB_TEXT = "#103121"
GRAB_BORDER = "#D9F2E3"
AMBER = "#F59E0B"
RED = "#E5484D"
TEAL = "#0EA5A4"
BG = "#F7FBF8"
CARD = "#FFFFFF"

st.markdown(f"""
<style>
:root {{
  --grab-green: {GRAB_GREEN};
  --grab-green-2: {GRAB_GREEN_2};
  --grab-soft: {GRAB_GREEN_SOFT};
  --grab-text: {GRAB_TEXT};
  --grab-border: {GRAB_BORDER};
  --bg: {BG};
  --card: {CARD};
  --amber: {AMBER};
  --red: {RED};
  --teal: {TEAL};
}}
.stApp {{background: var(--bg); color: var(--grab-text);}}
.block-container {{padding-top: 1rem; padding-bottom: 2rem; max-width: 94%;}}
[data-testid="stSidebar"] {{display:none;}}
.hero {{background: linear-gradient(135deg, #ffffff 0%, #f1fff7 100%); border:1px solid var(--grab-border); border-radius:22px; padding: 1.1rem 1.2rem; box-shadow: 0 8px 30px rgba(0,177,79,0.06); margin-bottom: 0.9rem;}}
.hero h1 {{font-size: 2rem; line-height: 1.05; margin: 0; color: var(--grab-text);}}
.hero p {{margin: .35rem 0 0 0; color: #466657; font-size: .96rem;}}
.tagrow {{display:flex; flex-wrap:wrap; gap:.5rem; margin-top:.75rem;}}
.tag {{background:#fff; border:1px solid var(--grab-border); color:#24543d; padding:.28rem .65rem; border-radius:999px; font-size:.78rem;}}
.metric-card {{background: var(--card); border:1px solid var(--grab-border); border-radius:18px; padding: .95rem 1rem; box-shadow: 0 8px 20px rgba(0,0,0,0.03);}}
.metric-label {{font-size:.76rem; text-transform:uppercase; letter-spacing:.08em; color:#567866; margin-bottom:.25rem;}}
.metric-value {{font-size:1.9rem; font-weight:800; color: var(--grab-text); line-height:1;}}
.metric-note {{font-size:.8rem; color:#5f7e6c; margin-top:.35rem;}}
.section-card {{background: var(--card); border:1px solid var(--grab-border); border-radius:18px; padding: 1rem 1rem .8rem 1rem; margin-bottom: .85rem; box-shadow: 0 8px 24px rgba(0,0,0,0.03);}}
.section-title {{font-weight: 800; font-size:1.05rem; color: var(--grab-text); margin-bottom:.5rem;}}
.section-sub {{color:#557663; font-size:.85rem; margin-top:-.15rem; margin-bottom:.7rem;}}
.problem-banner {{border-radius:16px; padding:.9rem 1rem; margin-bottom:.85rem; border-left:6px solid var(--grab-green); background:#ffffff; border:1px solid var(--grab-border);}}
.problem-banner.ps2 {{border-left-color: var(--teal);}}
.problem-banner.ps3 {{border-left-color: var(--amber);}}
.problem-banner h3 {{margin:0; font-size:1.1rem; color: var(--grab-text);}}
.problem-banner p {{margin:.35rem 0 0 0; color:#577565; font-size:.9rem;}}
.cue {{display:inline-block; padding:.22rem .5rem; border-radius:999px; font-size:.75rem; font-weight:700;}}
.cue-green {{background:#E9FFF2; color:#13733A; border:1px solid #BAECCF;}}
.cue-amber {{background:#FFF7E7; color:#9A6500; border:1px solid #F1D496;}}
.cue-red {{background:#FFF0F1; color:#B4232C; border:1px solid #F2C7CB;}}
.cue-teal {{background:#EBFEFD; color:#0F6E6B; border:1px solid #B4EBE8;}}
.action-card {{border-radius:16px; padding:.95rem 1rem; margin-bottom:.7rem; border:1px solid var(--grab-border); background:#fff;}}
.action-card.act {{border-left:5px solid var(--grab-green);}}
.action-card.watch {{border-left:5px solid var(--amber);}}
.action-card.risk {{border-left:5px solid var(--red);}}
.action-title {{font-weight:800; color:var(--grab-text); margin-bottom:.25rem;}}
.action-meta {{font-size:.82rem; color:#5A7A68; margin-bottom:.35rem;}}
.small-note {{font-size:.8rem; color:#5F7E6C;}}
hr.soft {{border:none; height:1px; background:#E5F4EB; margin:.65rem 0 .8rem 0;}}
div[data-testid="stTabs"] button {{padding-top:.55rem; padding-bottom:.55rem;}}
div[data-testid="stTabs"] button[aria-selected="true"] {{color: var(--grab-green) !important; border-bottom-color: var(--grab-green) !important;}}
div[data-testid="stMetric"] {{background:#fff; border:1px solid var(--grab-border); border-radius:16px; padding:.3rem .6rem;}}
div[data-baseweb="select"] > div, div[data-baseweb="base-input"] > div {{border-color: var(--grab-border) !important;}}
</style>
""", unsafe_allow_html=True)


def load_data(uploaded=None):
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv(BASE_DIR / DATA_FILE)
    for c in df.columns:
        if df[c].dtype == 'object':
            df[c] = df[c].fillna('Unknown').astype(str)
    return df


def apply_theme(fig, title=""):
    fig.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        margin=dict(l=20, r=20, t=60, b=20),
        title=title,
        font=dict(color=GRAB_TEXT, size=13),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig


def kpi_card(col, label, value, note):
    col.markdown(f"""
    <div class='metric-card'>
      <div class='metric-label'>{label}</div>
      <div class='metric-value'>{value}</div>
      <div class='metric-note'>{note}</div>
    </div>
    """, unsafe_allow_html=True)


def small_cue(score, high, med, reverse=False):
    if reverse:
        if score <= high:
            return "cue-green", "Healthy"
        if score <= med:
            return "cue-amber", "Watch"
        return "cue-red", "Action"
    if score >= high:
        return "cue-red", "Action"
    if score >= med:
        return "cue-amber", "Watch"
    return "cue-green", "Healthy"


def header():
    st.markdown("""
    <div class='hero'>
      <h1>Grab Decision Studio</h1>
      <p>Problem-led decision dashboard for Driver Trust, Super-App Growth, and Pricing Fairness.</p>
      <div class='tagrow'>
        <div class='tag'>Problem-first navigation</div>
        <div class='tag'>Hidden filters</div>
        <div class='tag'>Dynamic action cues</div>
        <div class='tag'>Stakeholder-friendly analytics</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def filter_panel(df):
    with st.expander("Refine view", expanded=False):
        c1, c2, c3 = st.columns(3)
        countries = c1.multiselect("Country", sorted(df['country'].dropna().unique()), default=sorted(df['country'].dropna().unique()))
        segments = c2.multiselect("Customer segment", sorted(df['superapp_segment'].dropna().unique()), default=sorted(df['superapp_segment'].dropna().unique()))
        value_tiers = c3.multiselect("Value tier", sorted(df['customer_value_tier'].dropna().unique()), default=sorted(df['customer_value_tier'].dropna().unique()))
        c4, c5, c6 = st.columns(3)
        driver_tiers = c4.multiselect("Driver tier", sorted(df['assigned_driver_tier'].dropna().unique()), default=sorted(df['assigned_driver_tier'].dropna().unique()))
        price_segs = c5.multiselect("Price sensitivity", sorted(df['price_sensitivity_segment'].dropna().unique()), default=sorted(df['price_sensitivity_segment'].dropna().unique()))
        primary = c6.multiselect("Primary service", sorted(df['primary_service'].dropna().unique()), default=sorted(df['primary_service'].dropna().unique()))
    view = df[
        df['country'].isin(countries)
        & df['superapp_segment'].isin(segments)
        & df['customer_value_tier'].isin(value_tiers)
        & df['assigned_driver_tier'].isin(driver_tiers)
        & df['price_sensitivity_segment'].isin(price_segs)
        & df['primary_service'].isin(primary)
    ].copy()
    return view


def ps1_page(view):
    st.markdown("""
    <div class='problem-banner'>
      <h3>PS1 · Driver Trust and Failed Bookings</h3>
      <p>Focus: identify where bookings are likely to fail, explain why it happens, and show what operational action should trigger before trust is lost.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    bad_rate = view['bad_booking_label'].mean()*100
    eta_gap = view['eta_gap_min'].mean()
    hi_driver = (view['assigned_driver_tier']=='High-Risk').mean()*100
    trust = view['trust_score'].mean()
    kpi_card(c1, 'Bad booking rate', f'{bad_rate:.1f}%', 'Bookings likely to fail or delay')
    kpi_card(c2, 'Avg ETA gap', f'{eta_gap:.1f} min', 'Promised vs actual arrival')
    kpi_card(c3, 'High-risk driver exposure', f'{hi_driver:.1f}%', 'Customer share exposed to risky drivers')
    kpi_card(c4, 'Trust score', f'{trust:.1f}', 'Higher is better')

    w1, w2 = st.columns([1.05, .95])
    with w1:
        st.markdown("<div class='section-card'><div class='section-title'>What is happening</div><div class='section-sub'>Bad bookings are concentrated where driver quality and operating conditions combine poorly.</div>", unsafe_allow_html=True)
        risk_country = view.groupby('country').agg(Bad_Booking_Rate=('bad_booking_label','mean'), ETA_Gap=('eta_gap_min','mean')).reset_index()
        risk_country['Bad_Booking_Rate'] = (risk_country['Bad_Booking_Rate']*100).round(1)
        fig = px.bar(risk_country.sort_values('Bad_Booking_Rate', ascending=False), x='country', y='Bad_Booking_Rate', color='ETA_Gap', color_continuous_scale=['#DFF7EA', GRAB_GREEN])
        fig.update_layout(coloraxis_colorbar_title='ETA gap')
        st.plotly_chart(apply_theme(fig, 'Bad booking rate by country'), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with w2:
        st.markdown("<div class='section-card'><div class='section-title'>Why it is happening</div><div class='section-sub'>Late-night demand, low-supply zones, and weaker driver tiers raise failure risk together.</div>", unsafe_allow_html=True)
        fig = px.scatter(
            view,
            x='low_supply_zone_share', y='booking_risk_score', size='complaint_count_90d',
            color='assigned_driver_tier', hover_data=['country','customer_id','eta_gap_min'],
            color_discrete_map={'Reliable':GRAB_GREEN, 'Average':TEAL, 'High-Risk':RED}
        )
        st.plotly_chart(apply_theme(fig, 'Booking risk vs low-supply exposure'), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    w3, w4 = st.columns([1,1])
    with w3:
        st.markdown("<div class='section-card'><div class='section-title'>What is likely next</div><div class='section-sub'>These combinations point to users most likely to face another broken booking.</div>", unsafe_allow_html=True)
        top_risk = view.sort_values(['booking_risk_score','clv_12m_usd'], ascending=[False, False]).head(12)
        st.dataframe(top_risk[['customer_id','country','assigned_driver_tier','booking_risk_score','eta_gap_min','failed_booking_rate_90d','clv_12m_usd']], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with w4:
        st.markdown("<div class='section-card'><div class='section-title'>What we should do</div><div class='section-sub'>Prescriptive logic is shown as action cards so the reason behind each move is visible.</div>", unsafe_allow_html=True)
        high_value = view[(view['booking_risk_score']>=70) & (view['customer_value_tier']=='High-Value')]
        zone_ops = view[(view['low_supply_zone_share']>=0.45) & (view['rush_hour_share']>=0.45)]
        driver_watch = view[view['assigned_driver_tier']=='High-Risk']
        st.markdown(f"<div class='action-card act'><div class='action-title'>Protect high-value riders first</div><div class='action-meta'>Who: {len(high_value)} high-value users with booking risk ≥ 70</div>Why: these riders combine high CLV with high trust-loss exposure.<hr class='soft'><b>Decision:</b> force reliable-driver assignment and auto-compensation trigger.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card watch'><div class='action-title'>Rebalance supply by zone and time</div><div class='action-meta'>Where: {len(zone_ops)} riders cluster in high rush-hour and low-supply conditions</div>Why: this is where delay risk compounds fastest.<hr class='soft'><b>Decision:</b> push driver incentives and tighter dispatch rules in these windows.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card risk'><div class='action-title'>Escalate risky driver pool</div><div class='action-meta'>Who: {len(driver_watch)} users matched to High-Risk driver tier</div>Why: cancellations, complaints, and ETA miss rates are already elevated.<hr class='soft'><b>Decision:</b> warning queue, reduced visibility, or temporary suspension review.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def ps2_page(view):
    st.markdown("""
    <div class='problem-banner ps2'>
      <h3>PS2 · Super-App Growth and Single-Service Dependency</h3>
      <p>Focus: show where Grab is stuck as a one-service app, why customers fail to expand, and which cross-sell or retention move should be made next.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    single_service = (view['services_used_count']<=1).mean()*100
    multi_service = (view['services_used_count']>=3).mean()*100
    churn = view['churn_30d_label'].mean()*100
    xprop = view['cross_sell_propensity'].mean()
    kpi_card(c1, 'Single-service share', f'{single_service:.1f}%', 'Users not acting like super-app customers')
    kpi_card(c2, '3+ services share', f'{multi_service:.1f}%', 'Higher ecosystem depth')
    kpi_card(c3, '30d churn risk', f'{churn:.1f}%', 'Users likely to go dormant soon')
    kpi_card(c4, 'Cross-sell propensity', f'{xprop:.1f}', 'Higher means better next-service adoption odds')

    a, b = st.columns([1.02, .98])
    with a:
        st.markdown("<div class='section-card'><div class='section-title'>What is happening</div><div class='section-sub'>The user base is fragmented into service specialists rather than broad ecosystem users.</div>", unsafe_allow_html=True)
        seg = view['superapp_segment'].value_counts().reset_index()
        seg.columns = ['segment','customers']
        fig = px.treemap(seg, path=['segment'], values='customers', color='customers', color_continuous_scale=['#E8FBF0', GRAB_GREEN])
        st.plotly_chart(apply_theme(fig, 'Customer base by super-app segment'), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='section-card'><div class='section-title'>Why it is happening</div><div class='section-sub'>Usage depth, recency, and consent determine whether cross-sell is realistic or wasteful.</div>", unsafe_allow_html=True)
        fig = px.scatter(
            view,
            x='services_used_count', y='cross_sell_propensity', size='clv_12m_usd',
            color='pdpa_contact_ok', symbol='customer_value_tier',
            hover_data=['customer_id','primary_service','next_best_service','recency_days'],
            color_continuous_scale=['#B8EFD0', GRAB_GREEN]
        )
        st.plotly_chart(apply_theme(fig, 'Cross-sell propensity by service depth'), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c, d = st.columns([1,1])
    with c:
        st.markdown("<div class='section-card'><div class='section-title'>What is likely next</div><div class='section-sub'>These are the natural next-service opportunities supported by the data.</div>", unsafe_allow_html=True)
        flow = view.groupby(['primary_service','next_best_service']).size().reset_index(name='count')
        if len(flow) > 0:
            labels = pd.Index(flow['primary_service'].tolist() + flow['next_best_service'].tolist()).unique().tolist()
            src = [labels.index(x) for x in flow['primary_service']]
            tgt = [labels.index(x) for x in flow['next_best_service']]
            fig = go.Figure(data=[go.Sankey(
                node=dict(label=labels, pad=16, thickness=18, color=['#B8EFD0']*len(labels)),
                link=dict(source=src, target=tgt, value=flow['count'], color='rgba(0,177,79,0.22)')
            )])
            st.plotly_chart(apply_theme(fig, 'Likely next-service journeys'), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with d:
        st.markdown("<div class='section-card'><div class='section-title'>What we should do</div><div class='section-sub'>Recommendations stay understandable by separating target, trigger, action, and business logic.</div>", unsafe_allow_html=True)
        cross_sell = view[(view['cross_sell_propensity']>=65) & (view['pdpa_contact_ok']==1) & (view['churn_risk_score']<58)]
        fading = view[view['superapp_segment']=='At-Risk Single-App User']
        power = view[view['superapp_segment']=='Power User']
        st.markdown(f"<div class='action-card act'><div class='action-title'>Cross-sell only where consent and likelihood both exist</div><div class='action-meta'>Who: {len(cross_sell)} users with high propensity and valid contact consent</div>Why: these are persuadable without creating compliance noise.<hr class='soft'><b>Decision:</b> recommend their next-best service, not a generic discount blast.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card risk'><div class='action-title'>Stop single-service users from fading out</div><div class='action-meta'>Who: {len(fading)} at-risk single-app users</div>Why: recency and narrow usage make quiet churn likely.<hr class='soft'><b>Decision:</b> send a primary-service reactivation message tied to their known habit.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card watch'><div class='action-title'>Protect ecosystem leaders</div><div class='action-meta'>Who: {len(power)} power users across multiple services</div>Why: they already carry the strongest value and habit formation.<hr class='soft'><b>Decision:</b> route them into loyalty bundles, priority support, and finance upsell.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'><div class='section-title'>Refined segment table</div><div class='section-sub'>A stakeholder can scan this once and immediately see where growth, churn, and next best action differ by segment.</div>", unsafe_allow_html=True)
    segtbl = view.groupby('superapp_segment').agg(
        Customers=('customer_id','count'),
        Avg_Services=('services_used_count','mean'),
        Churn_Risk=('churn_risk_score','mean'),
        Cross_Sell=('cross_sell_propensity','mean'),
        Avg_CLV=('clv_12m_usd','mean')
    ).round(1).sort_values('Avg_CLV', ascending=False).reset_index()
    st.dataframe(segtbl, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def ps3_page(view):
    st.markdown("""
    <div class='problem-banner ps3'>
      <h3>PS3 · Pricing Fairness, Surge Shock, and Hidden Fees</h3>
      <p>Focus: highlight where fare trust breaks, explain which customer groups are price-sensitive, and show how pricing rules should change to protect revenue and reputation together.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    surge = view['avg_surge_multiplier'].mean()
    extreme = view['extreme_surge_exposure_rate'].mean()*100
    abnormal = view['abnormal_charge_flags_90d'].mean()
    fairness = view['fare_fairness_score'].mean()
    kpi_card(c1, 'Avg surge multiplier', f'{surge:.2f}x', 'Average charged intensity')
    kpi_card(c2, 'Extreme surge exposure', f'{extreme:.1f}%', 'User share exposed to sharp fare spikes')
    kpi_card(c3, 'Abnormal charge flags', f'{abnormal:.1f}', 'Suspected billing or pricing anomalies')
    kpi_card(c4, 'Fare fairness score', f'{fairness:.1f}', 'Higher means clearer and fairer pricing')

    a, b = st.columns([1,1])
    with a:
        st.markdown("<div class='section-card'><div class='section-title'>What is happening</div><div class='section-sub'>Pricing stress is not uniform; it concentrates in sensitive segments and high-friction contexts.</div>", unsafe_allow_html=True)
        fair = view.groupby('price_sensitivity_segment').agg(Fairness=('fare_fairness_score','mean'), Surge=('avg_surge_multiplier','mean')).reset_index().round(2)
        fig = px.bar(fair, x='price_sensitivity_segment', y='Fairness', color='Surge', color_continuous_scale=['#FFF5D8', '#F2B53C'])
        st.plotly_chart(apply_theme(fig, 'Fairness by price sensitivity segment'), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='section-card'><div class='section-title'>Why it is happening</div><div class='section-sub'>High surge, waiting fees, and abnormal charges reduce perceived fairness and future trust.</div>", unsafe_allow_html=True)
        fig = px.scatter(
            view,
            x='avg_surge_multiplier', y='fare_fairness_score', size='abnormal_charge_flags_90d',
            color='price_sensitivity_segment', hover_data=['customer_id','country','surge_cap_recommendation'],
            color_discrete_map={'Highly Sensitive':RED, 'Moderately Sensitive':AMBER, 'Convenience-First':GRAB_GREEN}
        )
        st.plotly_chart(apply_theme(fig, 'Surge intensity vs fairness'), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c, d = st.columns([1,1])
    with c:
        st.markdown("<div class='section-card'><div class='section-title'>What is likely next</div><div class='section-sub'>Without intervention, price shock feeds churn in the most sensitive cohorts.</div>", unsafe_allow_html=True)
        tbl = view.sort_values(['abnormal_charge_flags_90d','churn_risk_score'], ascending=[False, False]).head(12)
        st.dataframe(tbl[['customer_id','country','price_sensitivity_segment','avg_surge_multiplier','abnormal_charge_flags_90d','fare_fairness_score','churn_risk_score']], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with d:
        st.markdown("<div class='section-card'><div class='section-title'>What we should do</div><div class='section-sub'>Actions are linked directly to fairness signals so the stakeholder sees the logic behind each move.</div>", unsafe_allow_html=True)
        sensitive = view[(view['price_sensitivity_segment']=='Highly Sensitive') & (view['avg_surge_multiplier']>=1.5)]
        abnormal_pool = view[view['abnormal_charge_flags_90d']>=3]
        convenience = view[(view['price_sensitivity_segment']=='Convenience-First') & (view['avg_surge_multiplier']>=1.7)]
        st.markdown(f"<div class='action-card act'><div class='action-title'>Cap fares for highly sensitive users</div><div class='action-meta'>Who: {len(sensitive)} users with sensitivity + surge above 1.5x</div>Why: this is the group most likely to perceive the fare as exploitative.<hr class='soft'><b>Decision:</b> enforce surge cap, show full fare upfront, and surface cheaper alternatives.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card risk'><div class='action-title'>Automate charge review and proactive refund</div><div class='action-meta'>Who: {len(abnormal_pool)} users with 3+ abnormal charge flags</div>Why: unexplained anomalies are a reputational and regulatory risk.<hr class='soft'><b>Decision:</b> trigger refund review and classify driver behaviour as normal, suspicious, or abusive.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card watch'><div class='action-title'>Use premium pricing only where service value is defensible</div><div class='action-meta'>Who: {len(convenience)} convenience-first users with high surge tolerance</div>Why: higher prices work only when speed and reliability stay strong.<hr class='soft'><b>Decision:</b> allow higher surge but pair it with service guarantee messaging.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'><div class='section-title'>Pricing rulebook view</div><div class='section-sub'>This turns analytical outputs into a simple policy table a non-technical stakeholder can approve.</div>", unsafe_allow_html=True)
    rulebook = view.groupby('price_sensitivity_segment').agg(
        Customers=('customer_id','count'),
        Avg_Surge=('avg_surge_multiplier','mean'),
        Avg_Fairness=('fare_fairness_score','mean'),
        Avg_Elasticity=('price_elasticity_score','mean'),
        Recommended_Cap=('surge_cap_recommendation','mean')
    ).round(2).reset_index()
    st.dataframe(rulebook, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def overview_page(view):
    st.markdown("<div class='section-card'><div class='section-title'>Executive lens</div><div class='section-sub'>This page gives one-glance orientation before a stakeholder enters the three problem areas.</div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, 'Customers', f"{len(view):,}", 'Filtered audience')
    kpi_card(c2, 'Avg trust', f"{view['trust_score'].mean():.1f}", 'Trust after booking and pricing experience')
    kpi_card(c3, 'Avg CLV', f"${view['clv_12m_usd'].mean():.0f}", '12-month value')
    kpi_card(c4, 'Churn risk', f"{view['churn_risk_score'].mean():.1f}", 'Portfolio risk')
    kpi_card(c5, 'Avg fairness', f"{view['fare_fairness_score'].mean():.1f}", 'Pricing transparency')

    s1, s2 = st.columns([1.05, .95])
    with s1:
        risk = pd.DataFrame({
            'Problem':['PS1 Driver Trust','PS2 Super-App Growth','PS3 Pricing Fairness'],
            'Severity':[view['booking_risk_score'].mean(), view['churn_risk_score'].mean(), 100-view['fare_fairness_score'].mean()],
            'Decision urgency':[view['bad_booking_label'].mean()*100, view['churn_30d_label'].mean()*100, view['abnormal_charge_flags_90d'].mean()*18]
        }).round(1)
        fig = px.scatter(risk, x='Severity', y='Decision urgency', size='Severity', color='Problem', text='Problem',
                         color_discrete_map={'PS1 Driver Trust':GRAB_GREEN,'PS2 Super-App Growth':TEAL,'PS3 Pricing Fairness':AMBER})
        fig.update_traces(textposition='top center')
        st.plotly_chart(apply_theme(fig, 'Portfolio view: severity vs urgency'), use_container_width=True)
    with s2:
        actions = view['recommended_action'].value_counts().reset_index().head(6)
        actions.columns = ['Action','Customers']
        fig = px.bar(actions, x='Customers', y='Action', orientation='h', color='Customers', color_continuous_scale=['#E8FBF0', GRAB_GREEN])
        st.plotly_chart(apply_theme(fig, 'Most common recommended actions'), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'><div class='section-title'>Decision cues</div><div class='section-sub'>These cues help a stakeholder know what matters before they read charts.</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    cues = [
        ('PS1 · Action now', 'High booking risk, weak driver tier, and high-value users overlap.', 'cue-red'),
        ('PS2 · Growth lever', 'Cross-sell is most defensible where consent, low churn, and high propensity all align.', 'cue-teal'),
        ('PS3 · Regulatory watch', 'High surge plus low fairness is not just a UX issue; it can become a policy issue.', 'cue-amber'),
    ]
    for col, (title, text, cueclass) in zip(cols, cues):
        col.markdown(f"<div class='action-card'><span class='cue {cueclass}'>{title}</span><div class='action-meta' style='margin-top:.45rem'>{text}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


uploaded = st.file_uploader('Upload Grab CSV', type=['csv'])
df = load_data(uploaded)
header()
view = filter_panel(df)

if len(view) == 0:
    st.warning('No rows match the selected filters.')
    st.stop()

nav = st.tabs(['Overview','PS1 Driver Trust','PS2 Super-App Growth','PS3 Pricing Fairness'])
with nav[0]:
    overview_page(view)
with nav[1]:
    ps1_page(view)
with nav[2]:
    ps2_page(view)
with nav[3]:
    ps3_page(view)

st.caption('Grab Decision Studio · hidden filters · problem-led navigation · action-oriented prescriptive view')
