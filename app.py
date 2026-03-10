from pathlib import Path
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

st.set_page_config(page_title="Grab Decision Studio", page_icon="🟢", layout="wide", initial_sidebar_state="collapsed")
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = "grab_superapp_synthetic.csv"
GRAB_GREEN = "#00B14F"
GRAB_GREEN_2 = "#02C75A"
GRAB_SOFT = "#E9FFF2"
GRAB_TEXT = "#103121"
GRAB_BORDER = "#D9F2E3"
BG = "#F7FBF8"
AMBER = "#F59E0B"
RED = "#E5484D"
TEAL = "#0EA5A4"

st.markdown(f"""
<style>
.stApp {{background:{BG}; color:{GRAB_TEXT};}}
.block-container {{padding-top:1rem; padding-bottom:2rem; max-width:94%;}}
[data-testid="stSidebar"] {{display:none;}}
.hero {{background:linear-gradient(135deg,#ffffff 0%,#f1fff7 100%); border:1px solid {GRAB_BORDER}; border-radius:22px; padding:1.1rem 1.2rem; box-shadow:0 8px 30px rgba(0,177,79,.06); margin-bottom:.9rem;}}
.hero h1 {{font-size:2rem; line-height:1.05; margin:0; color:{GRAB_TEXT};}}
.hero p {{margin:.35rem 0 0 0; color:#466657; font-size:.96rem;}}
.tagrow {{display:flex; flex-wrap:wrap; gap:.5rem; margin-top:.75rem;}}
.tag {{background:#fff; border:1px solid {GRAB_BORDER}; color:#24543d; padding:.28rem .65rem; border-radius:999px; font-size:.78rem;}}
.metric-card {{background:#fff; border:1px solid {GRAB_BORDER}; border-radius:18px; padding:.95rem 1rem; box-shadow:0 8px 20px rgba(0,0,0,.03);}}
.metric-label {{font-size:.76rem; text-transform:uppercase; letter-spacing:.08em; color:#567866; margin-bottom:.25rem;}}
.metric-value {{font-size:1.9rem; font-weight:800; color:{GRAB_TEXT}; line-height:1;}}
.metric-note {{font-size:.8rem; color:#5f7e6c; margin-top:.35rem;}}
.section-card {{background:#fff; border:1px solid {GRAB_BORDER}; border-radius:18px; padding:1rem 1rem .8rem 1rem; margin-bottom:.85rem; box-shadow:0 8px 24px rgba(0,0,0,.03);}}
.section-title {{font-weight:800; font-size:1.05rem; color:{GRAB_TEXT}; margin-bottom:.45rem;}}
.section-sub {{color:#557663; font-size:.85rem; margin-top:-.1rem; margin-bottom:.7rem;}}
.problem-banner {{border-radius:16px; padding:.9rem 1rem; margin-bottom:.85rem; border-left:6px solid {GRAB_GREEN}; background:#fff; border:1px solid {GRAB_BORDER};}}
.problem-banner.ps2 {{border-left-color:{TEAL};}}
.problem-banner.ps3 {{border-left-color:{AMBER};}}
.problem-banner h3 {{margin:0; font-size:1.1rem; color:{GRAB_TEXT};}}
.problem-banner p {{margin:.35rem 0 0 0; color:#577565; font-size:.9rem;}}
.action-card {{border-radius:16px; padding:.95rem 1rem; margin-bottom:.7rem; border:1px solid {GRAB_BORDER}; background:#fff;}}
.action-card.act {{border-left:5px solid {GRAB_GREEN};}}
.action-card.watch {{border-left:5px solid {AMBER};}}
.action-card.risk {{border-left:5px solid {RED};}}
.action-title {{font-weight:800; color:{GRAB_TEXT}; margin-bottom:.25rem;}}
.action-meta {{font-size:.82rem; color:#5A7A68; margin-bottom:.35rem;}}
.small-note {{font-size:.8rem; color:#5F7E6C;}}
hr.soft {{border:none; height:1px; background:#E5F4EB; margin:.65rem 0 .8rem 0;}}
div[data-testid="stTabs"] button[aria-selected="true"] {{color:{GRAB_GREEN} !important; border-bottom-color:{GRAB_GREEN} !important;}}
div[data-baseweb="select"] > div, div[data-baseweb="base-input"] > div {{border-color:{GRAB_BORDER} !important;}}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(uploaded=None):
    path = BASE_DIR / DATA_FILE
    df = pd.read_csv(uploaded) if uploaded is not None else pd.read_csv(path)
    for c in df.columns:
        if df[c].dtype == 'object':
            df[c] = df[c].fillna('Unknown').astype(str)
    return df


def header():
    st.markdown("""
    <div class='hero'>
      <h1>Grab Decision Studio</h1>
      <p>Problem-led dashboard for Driver Trust, Super-App Growth, and Pricing Fairness.</p>
      <div class='tagrow'>
        <div class='tag'>Grab-inspired theme</div>
        <div class='tag'>Hidden filters</div>
        <div class='tag'>Business-readable analytics</div>
        <div class='tag'>Decision cues</div>
      </div>
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
    return df[
        df['country'].isin(countries)
        & df['superapp_segment'].isin(segments)
        & df['customer_value_tier'].isin(value_tiers)
        & df['assigned_driver_tier'].isin(driver_tiers)
        & df['price_sensitivity_segment'].isin(price_segs)
        & df['primary_service'].isin(primary)
    ].copy()


def alt_scatter(data, x, y, color, size=None, tooltip=None, height=330, color_domain=None, color_range=None):
    enc = {
        'x': alt.X(f'{x}:Q', title=x.replace('_', ' ').title()),
        'y': alt.Y(f'{y}:Q', title=y.replace('_', ' ').title()),
        'tooltip': tooltip or list(data.columns[:5])
    }
    if size:
        enc['size'] = alt.Size(f'{size}:Q', title=size.replace('_', ' ').title())
    if color_domain and color_range:
        enc['color'] = alt.Color(f'{color}:N', scale=alt.Scale(domain=color_domain, range=color_range), title=color.replace('_', ' ').title())
    else:
        enc['color'] = alt.Color(f'{color}:N', title=color.replace('_', ' ').title())
    return alt.Chart(data).mark_circle(opacity=0.78).encode(**enc).properties(height=height)


def overview_page(view):
    st.markdown("<div class='section-card'><div class='section-title'>Executive lens</div><div class='section-sub'>A one-glance summary before entering the three problem areas.</div>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    kpi_card(c1, 'Customers', f"{len(view):,}", 'Filtered audience')
    kpi_card(c2, 'Avg trust', f"{view['trust_score'].mean():.1f}", 'Booking and pricing trust')
    kpi_card(c3, 'Avg CLV', f"${view['clv_12m_usd'].mean():.0f}", '12-month value')
    kpi_card(c4, 'Avg churn risk', f"{view['churn_risk_score'].mean():.1f}", 'Portfolio risk level')
    kpi_card(c5, 'Avg fairness', f"{view['fare_fairness_score'].mean():.1f}", 'Pricing clarity and fairness')

    left, right = st.columns([1.05, .95])
    with left:
        risk = pd.DataFrame({
            'Problem':['PS1 Driver Trust','PS2 Super-App Growth','PS3 Pricing Fairness'],
            'Severity':[view['booking_risk_score'].mean(), view['churn_risk_score'].mean(), 100-view['fare_fairness_score'].mean()],
            'Urgency':[view['bad_booking_label'].mean()*100, view['churn_30d_label'].mean()*100, view['abnormal_charge_flags_90d'].mean()*18]
        }).round(1).set_index('Problem')
        st.bar_chart(risk, color=[GRAB_GREEN, TEAL])
    with right:
        actions = view['recommended_action'].value_counts().head(6).to_frame('Customers')
        st.bar_chart(actions, color=GRAB_GREEN)

    st.markdown("<hr class='soft'>", unsafe_allow_html=True)
    cue1, cue2, cue3 = st.columns(3)
    cue1.markdown("<div class='action-card risk'><div class='action-title'>PS1 · Act now</div><div class='action-meta'>High booking risk overlapping with high-value riders needs immediate protection.</div></div>", unsafe_allow_html=True)
    cue2.markdown("<div class='action-card act'><div class='action-title'>PS2 · Growth lever</div><div class='action-meta'>Cross-sell should target users with consent, low churn pressure, and strong next-service fit.</div></div>", unsafe_allow_html=True)
    cue3.markdown("<div class='action-card watch'><div class='action-title'>PS3 · Regulatory watch</div><div class='action-meta'>High surge plus low fairness is a policy and reputation risk, not just a UX issue.</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def ps1_page(view):
    st.markdown("""
    <div class='problem-banner'>
      <h3>PS1 · Driver Trust and Failed Bookings</h3>
      <p>Identify where bookings are likely to fail, why those failures happen, and what operational move should trigger before trust is lost.</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, 'Bad booking rate', f"{view['bad_booking_label'].mean()*100:.1f}%", 'Likely failed or delayed bookings')
    kpi_card(c2, 'Avg ETA gap', f"{view['eta_gap_min'].mean():.1f} min", 'Promised vs actual arrival')
    kpi_card(c3, 'High-risk driver exposure', f"{(view['assigned_driver_tier']=='High-Risk').mean()*100:.1f}%", 'Users exposed to weak drivers')
    kpi_card(c4, 'Trust score', f"{view['trust_score'].mean():.1f}", 'Higher is better')

    a, b = st.columns([1.05, .95])
    with a:
        st.markdown("<div class='section-card'><div class='section-title'>What is happening</div><div class='section-sub'>Bad bookings are concentrated where driver quality and operating context both weaken.</div>", unsafe_allow_html=True)
        risk_country = view.groupby('country').agg(Bad_Booking_Rate=('bad_booking_label','mean')).mul(100).round(1).sort_values('Bad_Booking_Rate', ascending=False)
        st.bar_chart(risk_country, color=GRAB_GREEN)
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='section-card'><div class='section-title'>Why it is happening</div><div class='section-sub'>Low supply, late hours, and driver quality combine to raise booking risk.</div>", unsafe_allow_html=True)
        sc = alt_scatter(view, 'low_supply_zone_share', 'booking_risk_score', 'assigned_driver_tier', size='complaint_count_90d', tooltip=['customer_id','country','eta_gap_min','assigned_driver_tier'], color_domain=['Reliable','Average','High-Risk'], color_range=[GRAB_GREEN, TEAL, RED])
        st.altair_chart(sc, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c, d = st.columns(2)
    with c:
        st.markdown("<div class='section-card'><div class='section-title'>What is likely next</div><div class='section-sub'>These users are most likely to experience another broken booking.</div>", unsafe_allow_html=True)
        top_risk = view.sort_values(['booking_risk_score','clv_12m_usd'], ascending=[False, False]).head(12)
        st.dataframe(top_risk[['customer_id','country','assigned_driver_tier','booking_risk_score','eta_gap_min','failed_booking_rate_90d','clv_12m_usd']], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with d:
        st.markdown("<div class='section-card'><div class='section-title'>What we should do</div><div class='section-sub'>Decision cards make the trigger and the reason explicit.</div>", unsafe_allow_html=True)
        high_value = view[(view['booking_risk_score']>=70) & (view['customer_value_tier']=='High-Value')]
        zone_ops = view[(view['low_supply_zone_share']>=0.45) & (view['rush_hour_share']>=0.45)]
        driver_watch = view[view['assigned_driver_tier']=='High-Risk']
        st.markdown(f"<div class='action-card act'><div class='action-title'>Protect high-value riders first</div><div class='action-meta'>Who: {len(high_value)} high-value users with booking risk ≥ 70</div>Why: high CLV and high trust-loss risk overlap here.<hr class='soft'><b>Decision:</b> force reliable-driver assignment and auto-compensation trigger.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card watch'><div class='action-title'>Rebalance supply by zone and time</div><div class='action-meta'>Where: {len(zone_ops)} riders cluster in high rush-hour and low-supply conditions</div>Why: this is where delay risk compounds fastest.<hr class='soft'><b>Decision:</b> push driver incentives and tighter dispatch rules in these windows.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card risk'><div class='action-title'>Escalate risky driver pool</div><div class='action-meta'>Who: {len(driver_watch)} users matched to High-Risk driver tier</div>Why: cancellations and complaints are already elevated.<hr class='soft'><b>Decision:</b> warning queue, reduced visibility, or suspension review.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def ps2_page(view):
    st.markdown("""
    <div class='problem-banner ps2'>
      <h3>PS2 · Super-App Growth and Single-Service Dependency</h3>
      <p>Show where Grab behaves like a one-service app, why customers fail to expand, and which cross-sell or retention move should be made next.</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, 'Single-service share', f"{(view['services_used_count']<=1).mean()*100:.1f}%", 'Users not behaving like super-app customers')
    kpi_card(c2, '3+ services share', f"{(view['services_used_count']>=3).mean()*100:.1f}%", 'Deeper ecosystem engagement')
    kpi_card(c3, '30d churn rate', f"{view['churn_30d_label'].mean()*100:.1f}%", 'Users likely to go dormant soon')
    kpi_card(c4, 'Cross-sell propensity', f"{view['cross_sell_propensity'].mean():.1f}", 'Higher means stronger next-service odds')

    a, b = st.columns([1.02, .98])
    with a:
        st.markdown("<div class='section-card'><div class='section-title'>What is happening</div><div class='section-sub'>The customer base is fragmented into specialists rather than broad ecosystem users.</div>", unsafe_allow_html=True)
        seg = view['superapp_segment'].value_counts().to_frame('Customers')
        st.bar_chart(seg, color=GRAB_GREEN)
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='section-card'><div class='section-title'>Why it is happening</div><div class='section-sub'>Usage depth, recency, and consent determine whether cross-sell is realistic.</div>", unsafe_allow_html=True)
        sc = alt_scatter(view, 'services_used_count', 'cross_sell_propensity', 'customer_value_tier', size='clv_12m_usd', tooltip=['customer_id','primary_service','next_best_service','recency_days','pdpa_contact_ok'], color_domain=['High-Value','Mid-Value','Low-Value'], color_range=[GRAB_GREEN, TEAL, AMBER])
        st.altair_chart(sc, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c, d = st.columns(2)
    with c:
        st.markdown("<div class='section-card'><div class='section-title'>What is likely next</div><div class='section-sub'>This table shows the strongest next-service movements to target.</div>", unsafe_allow_html=True)
        flow = view.groupby(['primary_service','next_best_service']).size().reset_index(name='Customers').sort_values('Customers', ascending=False)
        st.dataframe(flow.head(15), use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with d:
        st.markdown("<div class='section-card'><div class='section-title'>What we should do</div><div class='section-sub'>Recommendations separate who, why, and action so they are easy to approve.</div>", unsafe_allow_html=True)
        cross_sell = view[(view['cross_sell_propensity']>=65) & (view['pdpa_contact_ok']==1) & (view['churn_risk_score']<58)]
        fading = view[view['superapp_segment']=='At-Risk Single-App User']
        power = view[view['superapp_segment']=='Power User']
        st.markdown(f"<div class='action-card act'><div class='action-title'>Cross-sell only where consent and likelihood both exist</div><div class='action-meta'>Who: {len(cross_sell)} users with high propensity and valid contact consent</div>Why: these are persuadable without creating compliance noise.<hr class='soft'><b>Decision:</b> recommend their next-best service, not a generic discount blast.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card risk'><div class='action-title'>Stop single-service users from fading out</div><div class='action-meta'>Who: {len(fading)} at-risk single-app users</div>Why: recency and narrow usage make quiet churn likely.<hr class='soft'><b>Decision:</b> send a primary-service reactivation message tied to their known habit.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card watch'><div class='action-title'>Protect ecosystem leaders</div><div class='action-meta'>Who: {len(power)} power users</div>Why: they carry the strongest value and habit formation.<hr class='soft'><b>Decision:</b> route them into loyalty bundles, priority support, and finance upsell.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'><div class='section-title'>Refined segment table</div><div class='section-sub'>A clean summary of growth, churn, and recommended direction by segment.</div>", unsafe_allow_html=True)
    segtbl = view.groupby('superapp_segment').agg(Customers=('customer_id','count'), Avg_Services=('services_used_count','mean'), Churn_Risk=('churn_risk_score','mean'), Cross_Sell=('cross_sell_propensity','mean'), Avg_CLV=('clv_12m_usd','mean')).round(1).sort_values('Avg_CLV', ascending=False).reset_index()
    st.dataframe(segtbl, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def ps3_page(view):
    st.markdown("""
    <div class='problem-banner ps3'>
      <h3>PS3 · Pricing Fairness, Surge Shock, and Hidden Fees</h3>
      <p>Highlight where fare trust breaks, which groups are most price-sensitive, and how pricing rules should change to protect revenue and reputation together.</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, 'Avg surge multiplier', f"{view['avg_surge_multiplier'].mean():.2f}x", 'Average charged intensity')
    kpi_card(c2, 'Extreme surge exposure', f"{view['extreme_surge_exposure_rate'].mean()*100:.1f}%", 'Exposure to sharp fare spikes')
    kpi_card(c3, 'Abnormal charge flags', f"{view['abnormal_charge_flags_90d'].mean():.1f}", 'Potential pricing anomalies')
    kpi_card(c4, 'Fare fairness score', f"{view['fare_fairness_score'].mean():.1f}", 'Higher means clearer pricing')

    a, b = st.columns(2)
    with a:
        st.markdown("<div class='section-card'><div class='section-title'>What is happening</div><div class='section-sub'>Pricing pressure is not uniform; it concentrates in sensitive segments.</div>", unsafe_allow_html=True)
        fair = view.groupby('price_sensitivity_segment').agg(Fairness=('fare_fairness_score','mean')).round(1)
        st.bar_chart(fair, color=AMBER)
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='section-card'><div class='section-title'>Why it is happening</div><div class='section-sub'>Higher surge, waiting fees, and abnormal charges reduce perceived fairness.</div>", unsafe_allow_html=True)
        sc = alt_scatter(view, 'avg_surge_multiplier', 'fare_fairness_score', 'price_sensitivity_segment', size='abnormal_charge_flags_90d', tooltip=['customer_id','country','surge_cap_recommendation','waiting_fee_count_90d'], color_domain=['Highly Sensitive','Moderately Sensitive','Convenience-First'], color_range=[RED, AMBER, GRAB_GREEN])
        st.altair_chart(sc, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c, d = st.columns(2)
    with c:
        st.markdown("<div class='section-card'><div class='section-title'>What is likely next</div><div class='section-sub'>Without intervention, price shock feeds churn in the most sensitive users.</div>", unsafe_allow_html=True)
        tbl = view.sort_values(['abnormal_charge_flags_90d','churn_risk_score'], ascending=[False, False]).head(12)
        st.dataframe(tbl[['customer_id','country','price_sensitivity_segment','avg_surge_multiplier','abnormal_charge_flags_90d','fare_fairness_score','churn_risk_score']], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with d:
        st.markdown("<div class='section-card'><div class='section-title'>What we should do</div><div class='section-sub'>Pricing decisions are shown as simple policy actions.</div>", unsafe_allow_html=True)
        sensitive = view[(view['price_sensitivity_segment']=='Highly Sensitive') & (view['avg_surge_multiplier']>=1.5)]
        abnormal_pool = view[view['abnormal_charge_flags_90d']>=3]
        convenience = view[(view['price_sensitivity_segment']=='Convenience-First') & (view['avg_surge_multiplier']>=1.7)]
        st.markdown(f"<div class='action-card act'><div class='action-title'>Cap fares for highly sensitive users</div><div class='action-meta'>Who: {len(sensitive)} users with sensitivity and surge above 1.5x</div>Why: this group is most likely to perceive the fare as unfair.<hr class='soft'><b>Decision:</b> enforce surge cap, show full fare upfront, and surface cheaper alternatives.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card risk'><div class='action-title'>Automate charge review and proactive refund</div><div class='action-meta'>Who: {len(abnormal_pool)} users with 3+ abnormal charge flags</div>Why: anomalies create both trust and regulatory risk.<hr class='soft'><b>Decision:</b> trigger refund review and classify behaviour as normal, suspicious, or abusive.</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='action-card watch'><div class='action-title'>Use premium pricing only where value is defensible</div><div class='action-meta'>Who: {len(convenience)} convenience-first users with high surge tolerance</div>Why: higher prices work only when service reliability stays strong.<hr class='soft'><b>Decision:</b> allow higher surge only with service guarantee messaging.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'><div class='section-title'>Pricing rulebook view</div><div class='section-sub'>A policy table a non-technical stakeholder can review quickly.</div>", unsafe_allow_html=True)
    rulebook = view.groupby('price_sensitivity_segment').agg(Customers=('customer_id','count'), Avg_Surge=('avg_surge_multiplier','mean'), Avg_Fairness=('fare_fairness_score','mean'), Avg_Elasticity=('price_elasticity_score','mean'), Recommended_Cap=('surge_cap_recommendation','mean')).round(2).reset_index()
    st.dataframe(rulebook, use_container_width=True, hide_index=True)
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

st.caption('Grab Decision Studio · Altair + Streamlit-native charts · no Plotly dependency')
