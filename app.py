import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Indian Skincare Demand Intelligence",
    page_icon="🧴",
    layout="wide"
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Serif+Display&display=swap');

/* Force light background everywhere */
.stApp { background-color: #F7F5F0 !important; }
section[data-testid="stSidebar"] { background-color: #F7F5F0 !important; }

/* Global text */
html, body, .stApp, .stMarkdown, p, span, div {
    font-family: 'DM Sans', sans-serif;
    color: #1C1C1E;
}

/* Tab text fix */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 4px 4px 0 0;
    padding: 8px 16px;
    color: #6B7280 !important;
    font-weight: 500;
    font-size: 0.9rem;
}
.stTabs [aria-selected="true"] {
    background: transparent;
    color: #1C1C1E !important;
    border-bottom: 2px solid #D4845A;
    font-weight: 600;
}
.stTabs [data-baseweb="tab"] p {
    color: inherit !important;
    font-size: 0.9rem !important;
}

[data-baseweb="menu"] { background-color: #FFFFFF !important; }
[data-baseweb="menu"] li { color: #1C1C1E !important; }
[data-baseweb="option"] { color: #1C1C1E !important; background-color: #FFFFFF !important; }
[data-baseweb="select"] { background-color: #FFFFFF !important; }
[data-baseweb="popover"] { background-color: #FFFFFF !important; }
[role="option"] { color: #1C1C1E !important; background-color: #FFFFFF !important; }
[role="listbox"] { background-color: #FFFFFF !important; }


/* Selectbox and multiselect */
.stMultiSelect span { color: #1C1C1E !important; }

/* Metric cards */
.kpi-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    border-left: 3px solid #D4845A;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 1.9rem;
    font-weight: 700;
    color: #1C1C1E;
    line-height: 1.1;
    font-family: 'DM Serif Display', serif;
}
.kpi-label {
    font-size: 0.72rem;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-top: 4px;
}

/* Section headers */
.eyebrow {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #D4845A;
    margin-bottom: 2px;
}
.section-h {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    color: #1C1C1E;
    margin-bottom: 12px;
    line-height: 1.25;
}
            
/* Selectbox fix */
[data-baseweb="select"] div {
    background-color: #FFFFFF !important;
    color: #1C1C1E !important;
}
[data-baseweb="select"] span {
    color: #1C1C1E !important;
}
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #1C1C1E !important;
}
/* Selectbox arrow */
[data-baseweb="select"] svg {
    fill: #1C1C1E !important;
    color: #1C1C1E !important;
}

/* Hero */
.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #1C1C1E;
    line-height: 1.15;
    margin-bottom: 4px;
}
.hero-sub {
    font-size: 0.95rem;
    color: #6B7280;
    font-weight: 300;
    margin-bottom: 1.5rem;
}

/* Insight box */
.insight {
    background: #FEF6EF;
    border-left: 3px solid #D4845A;
    border-radius: 0 6px 6px 0;
    padding: 0.85rem 1rem;
    font-size: 0.86rem;
    color: #374151;
    margin-top: 12px;
    line-height: 1.55;
}

hr.divider {
    border: none;
    border-top: 1px solid #E5E7EB;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Plotly base template ──────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    plot_bgcolor='#FFFFFF',
    paper_bgcolor='#F7F5F0',
    font=dict(color='#1C1C1E', size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        font=dict(color='#1C1C1E', size=11),
        bgcolor='rgba(0,0,0,0)',
        orientation='h',
        yanchor='bottom', y=1.02,
        xanchor='left', x=0
    ),
    xaxis=dict(
        color='#1C1C1E',
        tickfont=dict(color='#1C1C1E', size=12),
        title_font=dict(color='#1C1C1E', size=13),
        gridcolor='#F3F4F6',
        showgrid=False,
        linecolor='#E5E7EB'
    ),
    yaxis=dict(
        color='#1C1C1E',
        tickfont=dict(color='#1C1C1E', size=12),
        title_font=dict(color='#1C1C1E', size=13),
        gridcolor='#EBEBEB',
        showgrid=True,
        linecolor='#E5E7EB'
    )
)

# ── Brand colours ─────────────────────────────────────────────────────────────
BRAND_COLORS = {
    'Minimalist':              '#1A1A2E',
    'Foxtale':                 '#D4845A',
    'Dot and Key':             '#4A90C4',
    'Plum':                    '#7B5EA7',
    'Pilgrim':                 '#D64045',
    'Lakme':                   '#E6A817',
    'Himalaya Wellness Company': '#3A7D44',
    'Cetaphil':                '#7D8FA3'
}

INGR_COLORS = px.colors.qualitative.Safe

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    trends = pd.read_excel('skincare_trends_master (1).xlsx', sheet_name='All Terms')
    trends['Time'] = pd.to_datetime(trends['Time'])
    trends = trends.set_index('Time')
    nykaa = pd.read_excel('nykaa_data.xlsx')
    return trends, nykaa

trends_df, nykaa_df = load_data()

INGREDIENTS = [c for c in ['niacinamide','retinol','hyaluronic acid','Vitamin C',
               'kojic acid','salicylic acid','tranexamic acid','ceramides','rice water']
               if c in trends_df.columns]

BRANDS = [c for c in ['Minimalist','Foxtale','Dot and Key','Plum','Pilgrim',
                       'Lakme','Himalaya Wellness Company','Cetaphil']
          if c in trends_df.columns]

CAT_TERM = {'Face Wash':'face wash','Sunscreen':'sunscreen',
            'Toner':'toner','Face Serum':'face serum'}

# ── Pre-compute growth ────────────────────────────────────────────────────────
def growth_pct(df, cols):
    f = df[cols].iloc[:12].mean()
    l = df[cols].iloc[-12:].mean()
    g = ((l - f) / f * 100)
    return g

brand_growth = growth_pct(trends_df, BRANDS)
ingr_growth  = growth_pct(trends_df, INGREDIENTS)

brand_growth_finite = brand_growth.replace([float('inf'), float('-inf')], float('nan'))
ingr_growth_finite  = ingr_growth.replace([float('inf'), float('-inf')], float('nan'))

fastest_brand = brand_growth_finite.idxmax()
fastest_brand_val = int(brand_growth_finite.max())
declining_count = int((brand_growth < 0).sum())
fastest_ingr = ingr_growth_finite.idxmax()
fastest_ingr_val = int(ingr_growth_finite.max())
total_skus = int(nykaa_df['Num_SKUs'].sum())

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Indian Skincare Demand Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Mapping consumer search signals to brand supply across 8 Indian skincare brands &nbsp;·&nbsp; 2021 – 2026</div>', unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
for col, val, label in [
    (c1, f"{fastest_brand_val}%", f"Fastest brand growth · {fastest_brand}"),
    (c2, str(declining_count),    "Legacy brands declining in search"),
    (c3, f"{fastest_ingr_val}%",  f"Fastest ingredient · {fastest_ingr}"),
    (c4, str(total_skus),         "Total SKUs analysed across 8 brands"),
]:
    with col:
        st.markdown(f'''<div class="kpi-card">
            <div class="kpi-value">{val}</div>
            <div class="kpi-label">{label}</div>
        </div>''', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Ingredient Trends",
    "Brand Search Growth",
    "Demand vs Supply Gap",
    "Price Positioning"
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — INGREDIENT TRENDS
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="eyebrow">Search demand · 2021 – 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">Which ingredients are Indian consumers searching for?</div>', unsafe_allow_html=True)

    selected = st.multiselect(
        "Select ingredients",
        options=INGREDIENTS,
        default=['niacinamide','Vitamin C','kojic acid','retinol']
    )

    if selected:
        melt = trends_df[selected].reset_index().melt(
            id_vars='Time', var_name='Ingredient', value_name='Search Index'
        )
        fig1 = px.line(melt, x='Time', y='Search Index', color='Ingredient',
                       color_discrete_sequence=INGR_COLORS)
        fig1.update_traces(line_width=2)
        fig1.update_layout(**PLOT_LAYOUT)
        fig1.update_layout(height=380)
        fig1.update_layout(legend_title_text='')
        st.plotly_chart(fig1, use_container_width=True)

        g_table = pd.DataFrame({
            'Ingredient': INGREDIENTS,
            'Mean volume': trends_df[INGREDIENTS].mean().round(1).values,
            '5-year growth (%)': ingr_growth.round(1).values
        }).sort_values('5-year growth (%)', ascending=False).reset_index(drop=True)
        g_table['5-year growth (%)'] = g_table['5-year growth (%)'].apply(
            lambda x: '∞ (new)' if x == float('inf') else f"{x:+.1f}%"
        )
        st.dataframe(g_table, use_container_width=True, hide_index=True)

        st.markdown('''<div class="insight">
            <strong>Key insight —</strong> Kojic acid (+391%) and niacinamide (+308%) are the 
            fastest-growing ingredients, both targeting hyperpigmentation — the dominant Indian 
            skincare concern. Vitamin C leads in raw volume but is maturing (+49%). Brands that 
            built ingredient portfolios around niacinamide early are riding the growth wave.
        </div>''', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — BRAND SEARCH GROWTH
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="eyebrow">Brand awareness · 2021 – 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">Who is winning and losing consumer mindshare?</div>', unsafe_allow_html=True)

    bg_df = pd.DataFrame({
        'Brand': BRANDS,
        'Growth': [brand_growth[b] for b in BRANDS],
        'Mean volume': [round(trends_df[b].mean(), 1) for b in BRANDS]
    })
    bg_df['Plot'] = bg_df['Growth'].replace(float('inf'), 1500)
    bg_df['Label'] = bg_df['Growth'].apply(
        lambda x: '∞  new brand' if x == float('inf') else f"{x:+.0f}%"
    )
    bg_df['Color'] = bg_df['Plot'].apply(lambda x: '#D4845A' if x >= 0 else '#D64045')
    bg_df = bg_df.sort_values('Plot', ascending=True)

    fig2 = go.Figure(go.Bar(
        x=bg_df['Plot'], y=bg_df['Brand'],
        orientation='h',
        marker_color=bg_df['Color'],
        text=bg_df['Label'],
        textposition='outside',
        textfont=dict(color='#1C1C1E', size=12),
        cliponaxis=False
    ))
    fig2.update_layout(**PLOT_LAYOUT)
    fig2.update_layout(
        height=380,
        xaxis=dict(showticklabels=False, showgrid=False, title='', zeroline=True,
                   zerolinecolor='#D1D5DB', color='#1C1C1E'),
        yaxis=dict(showgrid=False, title='', tickfont=dict(color='#1C1C1E', size=12)),
        margin=dict(l=10, r=140, t=20, b=10)
    )
    st.plotly_chart(fig2, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('''<div class="insight">
            <strong>D2C explosion —</strong> Dot & Key (+1273%), Pilgrim (+670%), 
            Minimalist (+275%) all grew dramatically — driven by ingredient education, 
            digital marketing, and Nykaa as a launch platform.
        </div>''', unsafe_allow_html=True)
    with col_b:
        st.markdown('''<div class="insight">
            <strong>Legacy decline —</strong> Lakme (-34%) and Himalaya (-85%) are losing 
            consumer mindshare despite dominant offline distribution — a structural shift 
            in where Indian skincare consumers are paying attention.
        </div>''', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — DEMAND VS SUPPLY GAP
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="eyebrow">Strategic gap analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">Where does demand outpace brand supply?</div>', unsafe_allow_html=True)

    cat_demand = {}
    for cat, term in CAT_TERM.items():
        if term in trends_df.columns:
            f = trends_df[term].iloc[:12].mean()
            l = trends_df[term].iloc[-12:].mean()
            cat_demand[cat] = round(((l - f) / f * 100), 1) if f > 0 else 0

    gap_rows = []
    for _, row in nykaa_df.iterrows():
        gap_rows.append({
            'Brand':    row['Brand'],
            'Category': row['Category'],
            'SKUs':     row['Num_SKUs'],
            'Reviews':  row['Num_Reviews (Avg)'] if pd.notna(row['Num_Reviews (Avg)']) else 10,
            'Demand Growth': cat_demand.get(row['Category'], 0)
        })
    gap_df = pd.DataFrame(gap_rows)

    cat_filter = st.selectbox("Filter by category", ['All'] + list(CAT_TERM.keys()))
    plot_gap = gap_df if cat_filter == 'All' else gap_df[gap_df['Category'] == cat_filter]

    fig3 = px.scatter(
        plot_gap, x='Demand Growth', y='SKUs',
        size='Reviews', color='Brand',
        color_discrete_map=BRAND_COLORS,
        hover_data=['Category','Reviews'],
        text='Brand', size_max=55
    )
    fig3.update_traces(
        textposition='top center',
        textfont=dict(color='#1C1C1E', size=10),
        marker=dict(opacity=0.85, line=dict(width=1, color='white'))
    )
    mean_x = plot_gap['Demand Growth'].mean()
    mean_y = plot_gap['SKUs'].mean()
    fig3.add_vline(x=mean_x, line_dash='dash', line_color='#D1D5DB', line_width=1)
    fig3.add_hline(y=mean_y, line_dash='dash', line_color='#D1D5DB', line_width=1)

    fig3.update_layout(**PLOT_LAYOUT)
    fig3.update_layout(
        height=480,
        xaxis=dict(title='Category demand growth (%)', color='#1C1C1E',
                   tickfont=dict(color='#4B5563'), title_font=dict(color='#4B5563')),
        yaxis=dict(title='Number of SKUs on Nykaa', color='#1C1C1E',
                   tickfont=dict(color='#4B5563'), title_font=dict(color='#4B5563')),
        showlegend=True,
        legend=dict(font=dict(color='#1C1C1E', size=11), bgcolor='rgba(0,0,0,0)',
                    orientation='v', yanchor='top', y=1, xanchor='left', x=1.01)
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('''<div class="insight">
        <strong>How to read this —</strong> Bottom-right quadrant = high demand growth + low SKU 
        supply = strategic gap. Brands sitting there are missing high-growth categories. 
        Bubble size = average reviews (consumer traction). Dashed lines show category averages.
    </div>''', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — PRICE POSITIONING
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="eyebrow">Competitive pricing · Nykaa 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">How are brands positioned across price tiers?</div>', unsafe_allow_html=True)

    fig4 = px.strip(
        nykaa_df, x='BestSeller_Price', y='Category',
        color='Brand', color_discrete_map=BRAND_COLORS,
        hover_data=['Num_SKUs','Avg_Rating'],
        stripmode='overlay'
    )
    fig4.update_traces(marker=dict(size=13, opacity=0.85,
                                   line=dict(width=1, color='white')))
    fig4.update_layout(**PLOT_LAYOUT)
    fig4.update_layout(
        height=380,
        xaxis=dict(title='Bestseller price (₹)', color='#1C1C1E',
                   tickfont=dict(color='#4B5563'), title_font=dict(color='#4B5563')),
        yaxis=dict(title='', color='#1C1C1E',
                   tickfont=dict(color='#1C1C1E', size=12)),
        legend=dict(font=dict(color='#1C1C1E', size=11), bgcolor='rgba(0,0,0,0)',
                    orientation='v', yanchor='top', y=1, xanchor='left', x=1.01)
    )
    st.plotly_chart(fig4, use_container_width=True)

    price_summary = nykaa_df.groupby('Brand').agg(
        Avg_price=('BestSeller_Price','mean'),
        Min_price=('Price_Min','min'),
        Max_price=('Price_Max','max')
    ).round(0).sort_values('Avg_price', ascending=False)
    price_summary.columns = ['Avg bestseller (₹)', 'Min price (₹)', 'Max price (₹)']
    st.dataframe(price_summary, use_container_width=True)

    st.markdown('''<div class="insight">
        <strong>Key insight —</strong> D2C brands (Foxtale ₹407, Minimalist ₹358) price 
        surprisingly close to legacy brands (Lakme ₹325, Himalaya ₹310) — competing on 
        value and ingredient quality, not premium positioning. Cetaphil (₹923) operates 
        in a separate tier entirely, anchored by dermatologist trust rather than price competition.
    </div>''', unsafe_allow_html=True)