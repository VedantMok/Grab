from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Grab Executive Dashboard", page_icon="🟢", layout="wide", initial_sidebar_state="collapsed")
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = "grab_superapp_synthetic.csv"
GRAB_GREEN = "#00B14F"
GRAB_GREEN_SOFT = "#EAF8F0"
GRAB_TEXT = "#143524"
GRAB_BORDER = "#DCEEE3"
BG = "#F7FBF8"
CARD = "#FFFFFF"
TEAL = "#0EA5A4"
AMBER = "#F59E0B"
RED = "#E5484D"

st.markdown(f"""
<style>
.stApp {{background:{BG}; color:{GRAB_TEXT};}}
.block-container {{padding-top:1rem; padding-bottom:1.5rem; max-width:95%;}}
[data-testid="stSidebar"] {{display:none;}}
header[data-testid="stHeader"] {{background:transparent;}}
.main-title {{background:#fff; border:1px solid {GRAB_BORDER}; border-radius:18px; padding:1rem 1.15rem; margin-bottom:.9rem; box-shadow:0 6px 20px rgba(0,0,0,.03);}}
.main-title h1 {{margin:0; font-size:1.8rem; color:{GRAB_TEXT};}}
.main-title p {{margin:.25rem 0 0 0; color:#587262; font-size:.92rem;}}
.metric-card {{background:{CARD}; border:1px solid {GRAB_BORDER}; border-radius:16px; padding:.95rem 1rem; box-shadow:0 6px 18px rgba(0,0,0,.03);}}
.metric-label {{font-size:.75rem; text-transform:uppercase; letter-spacing:.08em; color:#5E7868; margin-bottom:.2rem;}}
.metric-value {{font-size:1.8rem; font-weight:800; color:{GRAB_TEXT}; line-height:1.05;}}
.metric-note {{font-size:.8rem; color:#617B6C; margin-top:.3rem;}}
.section-card {{background:{CARD}; border:1px solid {GRAB_BORDER}; border-radius:16px; padding:.95rem 1rem .8rem 1rem; margin-bottom:.8rem; box-shadow:0 6px 18px rgba(0,0,0,.03);}}
.section-title {{font-size:1rem; font-weight:800; color:{GRAB_TEXT}; margin-bottom:.45rem;}}
.section-sub {{font-size:.84rem; color:#607A6A; margin-bottom:.65rem;}}
.problem-head {{background:#fff; border:1px solid {GRAB_BORDER}; border-left:6px solid {GRAB_GREEN}; border-radius:16px; padding:.9rem 1rem; margin-bottom:.85rem;}}
.problem-head.ps2 {{border-left-color:{TEAL};}}
.problem-head.ps3 {{border-left-color:{AMBER};}}
.problem-head h2 {{margin:0; font-size:1.1rem; color:{GRAB_TEXT};}}
.problem-head p {{margin:.3rem 0 0 0; color:#5F7869; font-size:.9rem;}}
.action-box {{background:#fff; border:1px solid {GRAB_BORDER}; border-radius:14px; padding:.9rem 1rem; margin-bottom:.65rem;}}
.action-box.green {{border-left:5px solid {GRAB_GREEN};}}
.action-box.amber {{border-left:5px solid {AMBER};}}
.action-box.red {{border-left:5px solid {RED};}}
.action-box h4 {{margin:0 0 .25rem 0; color:{GRAB_TEXT}; font-size:.98rem;}}
.action-box p {{margin:.22rem 0; font-size:.84rem; color:#5F7869;}}
.small-label {{font-size:.76rem; color:#617B6C; text-transform:uppercase; letter-spacing:.08em; margin-bottom:.2rem;}}
.stTabs [data-baseweb="tab-list"] {{gap:.35rem;}}
.stTabs [data-baseweb="tab"] {{background:#fff; border:1px solid {GRAB_BORDER}; border-radius:12px 12px 0 0; padding:.55rem .9rem;}}
.stTabs [aria-selected="true"] {{color:{GRAB_GREEN} !important; border-bottom:2px solid {GRAB_GREEN} !important;}}
div[data-baseweb="select"] > div, div[data-baseweb="base-input"] > div {{border-color:{GRAB_BORDER} !important;}}
</style>
""", unsafe_allow_html=True)

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


def prep_bar(df, group_col, value_col, agg='mean', pct=False, sort_desc=True):
    out = df.groupby(group_col)[value_col].agg(agg).reset_index()
    if pct:
        out[value_col] = out[value_col] * 100
    out = out.sort_values(value_col, ascending=not sort_desc).set_index(group_col)
    return out


def prep_two_metric(df, group_col, m1, m2, pct_cols=None):
    out = df.groupby(group_col).agg({m1:'mean', m2:'mean'}).reset_index()
    pct_cols = pct_cols or []
    for c in pct_cols:
        if c in out.columns:
            out[c] = out[c] * 100
    return out.set_index(group_col)


def styled_top(df, cols, n=12, by=None, asc=False):
    out = df[cols].copy()
    if by is not None:
        out = out.sort_values(by, ascending=asc)
    return out.head(n)


def master_ps1(view):
    c1,c2,c3,c4,c5 = st.columns(5)
    kpi_card(c1,'Bad booking rate',f"{view['bad_booking_label'].mean()*100:.1f}%",'Bookings likely to fail or delay')
    kpi_card(c2,'Avg ETA gap',f"{view['eta_gap_min'].mean():.1f} min",'Promised vs actual')
    kpi_card(c3,'High-risk driver exposure',f"{(view['assigned_driver_tier']=='High-Risk').mean()*100:.1f}%",'Share matched to weak drivers')
    kpi_card(c4,'Complaint load',f"{view['complaint_count_90d'].mean():.1f}",'Average complaints over 90d')
    kpi_card(c5,'Trust score',f"{view['trust_score'].mean():.1f}",'Higher is better')

    a,b = st.columns([1,1])
    with a:
        section_open('Risk map','Master view of where booking failure is concentrated.')
        st.bar_chart(prep_bar(view,'country','bad_booking_label',pct=True))
        section_close()
        section_open('Driver tier pressure','Reliability tier mix across the filtered population.')
        st.bar_chart(view['assigned_driver_tier'].value_counts().to_frame('Customers'))
        section_close()
    with b:
        section_open('ETA realism','Average promised versus actual arrival by country.')
        eta = view.groupby('country')[['avg_eta_promised_min','avg_eta_actual_min']].mean().round(1)
        st.line_chart(eta)
        section_close()
        section_open('High-risk queue','Priority customers needing intervention now.')
        q = styled_top(view,['customer_id','country','assigned_driver_tier','booking_risk_score','eta_gap_min','clv_12m_usd'],12,['booking_risk_score','clv_12m_usd'])
        st.dataframe(q, use_container_width=True, hide_index=True)
        section_close()

    x,y = st.columns([1.15,.85])
    with x:
        section_open('Context drivers','Risk rises when low-supply exposure and ETA gap both increase.')
        sc = view[['low_supply_zone_share','eta_gap_min','booking_risk_score']].copy()
        st.scatter_chart(sc, x='low_supply_zone_share', y='booking_risk_score', size='eta_gap_min')
        section_close()
    with y:
        st.markdown(f"""
        <div class='action-box green'><h4>Decision priority</h4><p>Auto-reassign high-value riders when booking risk exceeds 70.</p><p>Why: this group combines high trust-loss risk and high value.</p></div>
        <div class='action-box amber'><h4>Operations priority</h4><p>Send targeted incentives into low-supply rush-hour zones.</p><p>Why: supply imbalance is driving avoidable delay and cancellation exposure.</p></div>
        <div class='action-box red'><h4>Control priority</h4><p>Escalate High-Risk driver tier for warning, reduced visibility, or review.</p><p>Why: complaints and failure rates are already elevated.</p></div>
        """, unsafe_allow_html=True)


def descriptive_ps1(view):
    a,b = st.columns(2)
    with a:
        section_open('Failed booking by country','Current distribution of booking failures.')
        st.bar_chart(prep_bar(view,'country','bad_booking_label',pct=True))
        section_close()
        section_open('Driver tier distribution','How exposure is split across reliability buckets.')
        st.bar_chart(view['assigned_driver_tier'].value_counts().to_frame('Customers'))
        section_close()
    with b:
        section_open('Complaints by driver tier','Average complaint load by reliability tier.')
        st.bar_chart(prep_bar(view,'assigned_driver_tier','complaint_count_90d'))
        section_close()
        section_open('ETA gap by country','Operational pain point by market.')
        st.bar_chart(prep_bar(view,'country','eta_gap_min'))
        section_close()

    c,d = st.columns(2)
    with c:
        section_open('Rush-hour exposure','Who is booking in harder operating windows.')
        st.bar_chart(prep_bar(view,'country','rush_hour_share',pct=True))
        section_close()
    with d:
        section_open('Low-supply zone exposure','Share of users exposed to thin supply conditions.')
        st.bar_chart(prep_bar(view,'country','low_supply_zone_share',pct=True))
        section_close()


def diagnostic_ps1(view):
    a,b = st.columns(2)
    with a:
        section_open('Risk drivers by tier','Booking risk and failure move with driver quality.')
        diag = view.groupby('assigned_driver_tier')[['booking_risk_score','failed_booking_rate_90d','eta_gap_min']].mean().round(2)
        st.bar_chart(diag)
        section_close()
    with b:
        section_open('Customer value exposure','High-value customers should face lower failure risk, not higher.')
        val = view.groupby('customer_value_tier')[['bad_booking_label','booking_risk_score','trust_score']].mean().round(2)
        val['bad_booking_label'] = val['bad_booking_label']*100
        st.bar_chart(val)
        section_close()

    c,d = st.columns(2)
    with c:
        section_open('Supply vs failure','Higher low-supply exposure aligns with higher failed booking rate.')
        bins = pd.cut(view['low_supply_zone_share'], bins=[0,0.2,0.35,0.5,1], labels=['Very low','Low','Medium','High'])
        grp = view.groupby(bins)['bad_booking_label'].mean().mul(100).to_frame('Bad booking %')
        st.bar_chart(grp)
        section_close()
    with d:
        section_open('ETA miss vs trust','Wider ETA miss erodes trust directly.')
        sc = view[['eta_gap_min','trust_score','refund_delay_days_avg']].copy()
        st.scatter_chart(sc, x='eta_gap_min', y='trust_score', size='refund_delay_days_avg')
        section_close()


def predictive_ps1(view):
    a,b = st.columns(2)
    with a:
        section_open('Booking risk distribution','Portfolio spread of predicted booking risk.')
        risk_band = pd.cut(view['booking_risk_score'], bins=[0,40,55,70,100], labels=['Low','Medium','High','Critical'])
        st.bar_chart(risk_band.value_counts().sort_index().to_frame('Customers'))
        section_close()
        section_open('Future failure candidates','Customers most likely to experience the next broken booking.')
        pred = styled_top(view,['customer_id','country','booking_risk_score','failed_booking_rate_90d','assigned_driver_tier','customer_value_tier'],15,'booking_risk_score')
        st.dataframe(pred, use_container_width=True, hide_index=True)
        section_close()
    with b:
        section_open('Risk by operational context','Predicted risk by rush-hour and late-night exposure.')
        ctx = view.copy()
        ctx['rush_band'] = pd.cut(ctx['rush_hour_share'], bins=[0,0.25,0.45,1], labels=['Low','Medium','High'])
        out = ctx.groupby('rush_band')[['booking_risk_score','bad_booking_label']].mean().round(2)
        out['bad_booking_label'] = out['bad_booking_label']*100
        st.line_chart(out)
        section_close()
        section_open('High-risk value pool','How much CLV sits inside the high-risk bucket.')
        value = view.assign(risk_band=risk_band).groupby('risk_band')['clv_12m_usd'].mean().round(0).to_frame('Avg CLV')
        st.bar_chart(value)
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
        action = styled_top(view[['customer_id','country','customer_value_tier','booking_risk_score','assigned_driver_tier','recommended_action','clv_12m_usd']], ['customer_id','country','customer_value_tier','booking_risk_score','assigned_driver_tier','recommended_action','clv_12m_usd'], 15, ['booking_risk_score','clv_12m_usd'])
        st.dataframe(action, use_container_width=True, hide_index=True)
        section_close()
        section_open('Expected effect by action type','Where the largest recoverable value sits.')
        eff = view.groupby('recommended_action')[['clv_12m_usd','trust_score']].mean().round(1).sort_values('clv_12m_usd', ascending=False).head(8)
        st.bar_chart(eff)
        section_close()


def master_ps2(view):
    c1,c2,c3,c4,c5 = st.columns(5)
    kpi_card(c1,'Single-service share',f"{(view['services_used_count']<=1).mean()*100:.1f}%",'Users not acting like super-app customers')
    kpi_card(c2,'3+ services share',f"{(view['services_used_count']>=3).mean()*100:.1f}%",'Higher ecosystem depth')
    kpi_card(c3,'Cross-sell propensity',f"{view['cross_sell_propensity'].mean():.1f}",'Likelihood of next-service adoption')
    kpi_card(c4,'Churn risk',f"{view['churn_risk_score'].mean():.1f}",'Portfolio average')
    kpi_card(c5,'12m CLV',f"${view['clv_12m_usd'].mean():.0f}",'Average customer value')

    a,b = st.columns(2)
    with a:
        section_open('Segment command view','Current shape of the customer base.')
        st.bar_chart(view['superapp_segment'].value_counts().to_frame('Customers'))
        section_close()
        section_open('Service depth by country','How multi-service behavior differs by market.')
        st.bar_chart(prep_bar(view,'country','services_used_count'))
        section_close()
    with b:
        section_open('Cross-sell vs churn','Master relationship between growth and churn pressure.')
        sc = view[['cross_sell_propensity','churn_risk_score','clv_12m_usd']].copy()
        st.scatter_chart(sc, x='cross_sell_propensity', y='churn_risk_score', size='clv_12m_usd')
        section_close()
        section_open('Top next-service routes','Most frequent next service opportunities.')
        flow = view.groupby(['primary_service','next_best_service']).size().reset_index(name='Customers').sort_values('Customers', ascending=False)
        st.dataframe(flow.head(12), use_container_width=True, hide_index=True)
        section_close()

    x,y = st.columns([1.1,.9])
    with x:
        section_open('Value at risk','Higher churn pressure combined with low service depth is the key growth gap.')
        seg = view.groupby('superapp_segment')[['services_used_count','churn_risk_score','clv_12m_usd']].mean().round(1)
        st.bar_chart(seg)
        section_close()
    with y:
        st.markdown(f"""
        <div class='action-box green'><h4>Growth priority</h4><p>Cross-sell only where consent and high propensity both exist.</p><p>Why: this improves conversion without creating compliance waste.</p></div>
        <div class='action-box amber'><h4>Retention priority</h4><p>Re-activate fading single-service users before inactivity hardens into churn.</p><p>Why: recency and narrow usage are early warning signs.</p></div>
        <div class='action-box red'><h4>Value protection</h4><p>Protect power users with bundles and priority support.</p><p>Why: they carry the strongest lifetime value and ecosystem habit.</p></div>
        """, unsafe_allow_html=True)


def descriptive_ps2(view):
    a,b = st.columns(2)
    with a:
        section_open('Super-app segment split','Current distribution of customer profiles.')
        st.bar_chart(view['superapp_segment'].value_counts().to_frame('Customers'))
        section_close()
        section_open('Primary service split','Where users currently anchor.')
        st.bar_chart(view['primary_service'].value_counts().to_frame('Customers'))
        section_close()
    with b:
        section_open('Service depth distribution','How many services customers use today.')
        depth = view['services_used_count'].value_counts().sort_index().to_frame('Customers')
        st.bar_chart(depth)
        section_close()
        section_open('Customer value tier mix','Value segmentation of the current base.')
        st.bar_chart(view['customer_value_tier'].value_counts().to_frame('Customers'))
        section_close()

    c,d = st.columns(2)
    with c:
        section_open('Country service depth','Average services used by market.')
        st.bar_chart(prep_bar(view,'country','services_used_count'))
        section_close()
    with d:
        section_open('Promotion response by segment','Which segments react most to offers.')
        st.bar_chart(prep_bar(view,'superapp_segment','promo_response_rate',pct=True))
        section_close()


def diagnostic_ps2(view):
    a,b = st.columns(2)
    with a:
        section_open('Recency and churn','Dormancy explains much of the churn signal.')
        rec = view.groupby('superapp_segment')[['recency_days','churn_risk_score']].mean().round(1)
        st.bar_chart(rec)
        section_close()
    with b:
        section_open('Consent and cross-sell','Valid contact rights shape who should be targeted.')
        consent = view.groupby('pdpa_contact_ok')[['cross_sell_propensity','churn_risk_score']].mean().round(1)
        consent.index = ['No consent','Consent'] if len(consent.index)==2 else consent.index
        st.bar_chart(consent)
        section_close()

    c,d = st.columns(2)
    with c:
        section_open('Value versus service depth','More service usage generally aligns with stronger value.')
        sc = view[['services_used_count','clv_12m_usd','churn_risk_score']].copy()
        st.scatter_chart(sc, x='services_used_count', y='clv_12m_usd', size='churn_risk_score')
        section_close()
    with d:
        section_open('Segment scorecard','Where churn, cross-sell, and CLV diverge most.')
        score = view.groupby('superapp_segment')[['cross_sell_propensity','churn_risk_score','clv_12m_usd','services_used_count']].mean().round(1)
        st.dataframe(score, use_container_width=True)
        section_close()


def predictive_ps2(view):
    a,b = st.columns(2)
    with a:
        section_open('Churn risk bands','Share of users by predicted churn intensity.')
        bands = pd.cut(view['churn_risk_score'], bins=[0,35,50,65,100], labels=['Low','Medium','High','Critical'])
        st.bar_chart(bands.value_counts().sort_index().to_frame('Customers'))
        section_close()
        section_open('Top churn candidates','Users likely to leave in the next 30 days.')
        top = styled_top(view,['customer_id','country','superapp_segment','churn_risk_score','recency_days','services_used_count','clv_12m_usd'],15,'churn_risk_score')
        st.dataframe(top, use_container_width=True, hide_index=True)
        section_close()
    with b:
        section_open('Cross-sell bands','How many users are realistically ready for the next service.')
        cb = pd.cut(view['cross_sell_propensity'], bins=[0,40,55,70,100], labels=['Low','Medium','High','Priority'])
        st.bar_chart(cb.value_counts().sort_index().to_frame('Customers'))
        section_close()
        section_open('Next-best service by primary anchor','Predicted growth path from the current main service.')
        nxt = view.groupby(['primary_service','next_best_service']).size().reset_index(name='Customers').sort_values('Customers', ascending=False)
        st.dataframe(nxt.head(15), use_container_width=True, hide_index=True)
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
        q = styled_top(view,['customer_id','country','superapp_segment','next_best_service','cross_sell_propensity','churn_risk_score','recommended_action','clv_12m_usd'],15,['cross_sell_propensity','clv_12m_usd'])
        st.dataframe(q, use_container_width=True, hide_index=True)
        section_close()
        section_open('Action value by segment','Where the most recoverable or expandable value sits.')
        act = view.groupby('superapp_segment')[['clv_12m_usd','cross_sell_propensity','churn_risk_score']].mean().round(1)
        st.bar_chart(act)
        section_close()


def master_ps3(view):
    c1,c2,c3,c4,c5 = st.columns(5)
    kpi_card(c1,'Avg surge',f"{view['avg_surge_multiplier'].mean():.2f}x",'Average multiplier')
    kpi_card(c2,'Extreme surge exposure',f"{view['extreme_surge_exposure_rate'].mean()*100:.1f}%",'Exposure to sharp spikes')
    kpi_card(c3,'Abnormal charge flags',f"{view['abnormal_charge_flags_90d'].mean():.1f}",'Potential billing anomalies')
    kpi_card(c4,'Fairness score',f"{view['fare_fairness_score'].mean():.1f}",'Higher is better')
    kpi_card(c5,'Refund recovery',f"{view['proactive_refund_rate'].mean()*100:.1f}%",'Proactive service recovery')

    a,b = st.columns(2)
    with a:
        section_open('Fairness by segment','Master view of who experiences pricing strain.')
        st.bar_chart(prep_bar(view,'price_sensitivity_segment','fare_fairness_score'))
        section_close()
        section_open('Surge by country','Current pricing intensity by market.')
        st.bar_chart(prep_bar(view,'country','avg_surge_multiplier'))
        section_close()
    with b:
        section_open('Shock versus fairness','Pricing trust weakens as shock and anomaly exposure rise.')
        sc = view[['avg_surge_multiplier','fare_fairness_score','abnormal_charge_flags_90d']].copy()
        st.scatter_chart(sc, x='avg_surge_multiplier', y='fare_fairness_score', size='abnormal_charge_flags_90d')
        section_close()
        section_open('Pricing review queue','Users most likely to feel overcharged or churn after a shock.')
        q = styled_top(view,['customer_id','country','price_sensitivity_segment','avg_surge_multiplier','abnormal_charge_flags_90d','fare_fairness_score','churn_risk_score'],12,['abnormal_charge_flags_90d','churn_risk_score'])
        st.dataframe(q, use_container_width=True, hide_index=True)
        section_close()

    x,y = st.columns([1.1,.9])
    with x:
        section_open('Policy comparison','Sensitivity segment, elasticity, and recommended cap together.')
        policy = view.groupby('price_sensitivity_segment')[['avg_surge_multiplier','price_elasticity_score','surge_cap_recommendation','fare_fairness_score']].mean().round(2)
        st.bar_chart(policy)
        section_close()
    with y:
        st.markdown(f"""
        <div class='action-box green'><h4>Pricing guardrail</h4><p>Cap surge at 1.5x for highly sensitive users.</p><p>Why: fairness erosion and churn risk are highest here.</p></div>
        <div class='action-box amber'><h4>Recovery rule</h4><p>Trigger proactive refund review for repeated abnormal charge flags.</p><p>Why: this reduces reputational and regulatory exposure.</p></div>
        <div class='action-box red'><h4>Premium logic</h4><p>Allow higher surge only where convenience-first segments receive service assurance.</p><p>Why: higher price without reliability becomes hard to defend.</p></div>
        """, unsafe_allow_html=True)


def descriptive_ps3(view):
    a,b = st.columns(2)
    with a:
        section_open('Price sensitivity mix','Current customer split by price sensitivity.')
        st.bar_chart(view['price_sensitivity_segment'].value_counts().to_frame('Customers'))
        section_close()
        section_open('Waiting fee burden','Average waiting-fee count by country.')
        st.bar_chart(prep_bar(view,'country','waiting_fee_count_90d'))
        section_close()
    with b:
        section_open('Fairness by country','Market-level perception of pricing fairness.')
        st.bar_chart(prep_bar(view,'country','fare_fairness_score'))
        section_close()
        section_open('Abnormal charges by segment','Where charge anomalies cluster.')
        st.bar_chart(prep_bar(view,'price_sensitivity_segment','abnormal_charge_flags_90d'))
        section_close()

    c,d = st.columns(2)
    with c:
        section_open('Surge intensity distribution','Current pricing pressure across user segments.')
        st.bar_chart(prep_bar(view,'price_sensitivity_segment','avg_surge_multiplier'))
        section_close()
    with d:
        section_open('Refund recovery by segment','Where proactive recovery is currently concentrated.')
        st.bar_chart(prep_bar(view,'price_sensitivity_segment','proactive_refund_rate',pct=True))
        section_close()


def diagnostic_ps3(view):
    a,b = st.columns(2)
    with a:
        section_open('Shock drivers','Surge, hidden fees, and anomalies jointly reduce fairness.')
        diag = view[['avg_surge_multiplier','waiting_fee_count_90d','abnormal_charge_flags_90d','fare_fairness_score']].corr().round(2)
        st.dataframe(diag, use_container_width=True)
        section_close()
    with b:
        section_open('Elasticity by segment','Demand response changes by customer sensitivity.')
        st.bar_chart(prep_bar(view,'price_sensitivity_segment','price_elasticity_score'))
        section_close()

    c,d = st.columns(2)
    with c:
        section_open('Fairness versus churn','Lower fairness tends to align with higher churn pressure.')
        sc = view[['fare_fairness_score','churn_risk_score','avg_surge_multiplier']].copy()
        st.scatter_chart(sc, x='fare_fairness_score', y='churn_risk_score', size='avg_surge_multiplier')
        section_close()
    with d:
        section_open('Abnormal charge impact','Users with repeated flags see materially weaker fairness.')
        bins = pd.cut(view['abnormal_charge_flags_90d'], bins=[-1,0,2,4,20], labels=['None','Low','Medium','High'])
        grp = view.groupby(bins)[['fare_fairness_score','churn_risk_score']].mean().round(1)
        st.bar_chart(grp)
        section_close()


def predictive_ps3(view):
    a,b = st.columns(2)
    with a:
        section_open('Fairness risk bands','How many users fall into weak pricing-trust conditions.')
        bands = pd.cut(view['fare_fairness_score'], bins=[0,45,60,75,100], labels=['Critical','High risk','Watch','Healthy'])
        st.bar_chart(bands.value_counts().sort_index().to_frame('Customers'))
        section_close()
        section_open('Pricing risk candidates','Users most likely to react negatively to pricing shock.')
        top = styled_top(view,['customer_id','country','price_sensitivity_segment','avg_surge_multiplier','abnormal_charge_flags_90d','fare_fairness_score','churn_risk_score'],15,['fare_fairness_score','churn_risk_score'],asc=[True,False] if False else False)
        top = view[['customer_id','country','price_sensitivity_segment','avg_surge_multiplier','abnormal_charge_flags_90d','fare_fairness_score','churn_risk_score']].sort_values(['fare_fairness_score','churn_risk_score'], ascending=[True,False]).head(15)
        st.dataframe(top, use_container_width=True, hide_index=True)
        section_close()
    with b:
        section_open('Cap recommendation by segment','Predicted pricing guardrails from elasticity and fairness signals.')
        cap = view.groupby('price_sensitivity_segment')[['surge_cap_recommendation','avg_surge_multiplier','churn_risk_score']].mean().round(2)
        st.line_chart(cap)
        section_close()
        section_open('Exposure ladder','How extreme surge exposure escalates by segment.')
        ex = view.groupby('price_sensitivity_segment')[['extreme_surge_exposure_rate','proactive_refund_rate']].mean().mul(100).round(1)
        st.bar_chart(ex)
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
        q = view[['customer_id','country','price_sensitivity_segment','avg_surge_multiplier','abnormal_charge_flags_90d','surge_cap_recommendation','recommended_action']].sort_values(['abnormal_charge_flags_90d','avg_surge_multiplier'], ascending=[False,False]).head(15)
        st.dataframe(q, use_container_width=True, hide_index=True)
        section_close()
        section_open('Policy value view','Where fairness recovery protects the most value.')
        pol = view.groupby('price_sensitivity_segment')[['clv_12m_usd','fare_fairness_score','churn_risk_score']].mean().round(1)
        st.bar_chart(pol)
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
