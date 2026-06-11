import streamlit as st
import pandas as pd
from analysis import (
    load_data,
    top_cities_by_restaurants,
    avg_rating_by_city,
    cuisine_popularity,
    price_vs_rating,
    online_delivery_split,
    table_booking_split,
    rating_distribution,
    top_restaurant_chains,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato EDA Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .main { background-color: #0f172a; }

    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #f97316;
        margin: 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 4px;
    }
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #f1f5f9;
        border-left: 4px solid #f97316;
        padding-left: 12px;
        margin: 32px 0 16px 0;
    }
    .insight-box {
        background: #1e293b;
        border-left: 3px solid #f97316;
        border-radius: 6px;
        padding: 14px 18px;
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/7/75/Zomato_logo.png", width=160)
st.sidebar.markdown("## Filters")

all_cities = sorted(df["City"].dropna().unique())
selected_cities = st.sidebar.multiselect(
    "Select Cities", options=all_cities,
    default=all_cities[:10],
    help="Filter the dashboard by city"
)

rating_range = st.sidebar.slider(
    "Minimum Rating", min_value=0.0, max_value=5.0,
    value=0.0, step=0.5
)

has_delivery = st.sidebar.checkbox("Online Delivery Only", value=False)
has_booking = st.sidebar.checkbox("Table Booking Only", value=False)

# Apply filters
filtered = df.copy()
if selected_cities:
    filtered = filtered[filtered["City"].isin(selected_cities)]
if rating_range > 0:
    filtered = filtered[filtered["Aggregate rating"] >= rating_range]
if has_delivery:
    filtered = filtered[filtered["Has Online delivery"] == "Yes"]
if has_booking:
    filtered = filtered[filtered["Has Table booking"] == "Yes"]

st.sidebar.markdown(f"**{len(filtered):,}** restaurants match filters")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🍽️ Zomato India — EDA Dashboard")
st.markdown("An exploratory analysis of restaurant trends, cuisines, and ratings across Indian cities.")
st.markdown("---")

# ── KPI cards ─────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{len(filtered):,}</p>
        <p class="metric-label">Total Restaurants</p>
    </div>""", unsafe_allow_html=True)

with col2:
    avg_r = filtered[filtered["Aggregate rating"] > 0]["Aggregate rating"].mean()
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{avg_r:.2f} ⭐</p>
        <p class="metric-label">Avg Rating</p>
    </div>""", unsafe_allow_html=True)

with col3:
    delivery_pct = (filtered["Has Online delivery"] == "Yes").mean() * 100
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{delivery_pct:.1f}%</p>
        <p class="metric-label">Online Delivery</p>
    </div>""", unsafe_allow_html=True)

with col4:
    num_cities = filtered["City"].nunique()
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-value">{num_cities}</p>
        <p class="metric-label">Cities Covered</p>
    </div>""", unsafe_allow_html=True)

# ── Section 1: City Analysis ──────────────────────────────────────────────────
st.markdown('<p class="section-header">📍 City-wise Restaurant Analysis</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(top_cities_by_restaurants(filtered), use_container_width=True)
with col2:
    st.plotly_chart(avg_rating_by_city(filtered), use_container_width=True)

st.markdown("""
<div class="insight-box">
💡 <strong>Insight:</strong> New Delhi dominates in restaurant count, but smaller cities like Panchkula
often outperform metros in average ratings — suggesting quality over quantity.
</div>""", unsafe_allow_html=True)

# ── Section 2: Cuisines ───────────────────────────────────────────────────────
st.markdown('<p class="section-header">🍜 Cuisine Popularity</p>', unsafe_allow_html=True)
st.plotly_chart(cuisine_popularity(filtered), use_container_width=True)
st.markdown("""
<div class="insight-box">
💡 <strong>Insight:</strong> North Indian and Chinese cuisines dominate the Indian food market,
while Continental and Fast Food are rising due to urbanisation.
</div>""", unsafe_allow_html=True)

# ── Section 3: Price vs Rating ────────────────────────────────────────────────
st.markdown('<p class="section-header">💰 Does Price Predict Rating?</p>', unsafe_allow_html=True)
st.plotly_chart(price_vs_rating(filtered), use_container_width=True)
st.markdown("""
<div class="insight-box">
💡 <strong>Insight:</strong> There is weak positive correlation between price and rating — 
premium restaurants tend to rate slightly higher, but many budget restaurants hold strong ratings too.
</div>""", unsafe_allow_html=True)

# ── Section 4: Ratings Distribution ──────────────────────────────────────────
st.markdown('<p class="section-header">⭐ Rating Distribution</p>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    st.plotly_chart(rating_distribution(filtered), use_container_width=True)
with col2:
    st.markdown("#### Rating Breakdown")
    bins = [0, 2, 3, 4, 4.5, 5]
    labels = ["Poor (0–2)", "Average (2–3)", "Good (3–4)", "Very Good (4–4.5)", "Excellent (4.5–5)"]
    rated = filtered[filtered["Aggregate rating"] > 0].copy()
    rated["Rating Band"] = pd.cut(rated["Aggregate rating"], bins=bins, labels=labels)
    band_counts = rated["Rating Band"].value_counts().sort_index()
    for label, count in band_counts.items():
        pct = count / len(rated) * 100
        st.markdown(f"**{label}** — {count:,} ({pct:.1f}%)")

# ── Section 5: Delivery & Booking ─────────────────────────────────────────────
st.markdown('<p class="section-header">🛵 Delivery & Booking Trends</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(online_delivery_split(filtered), use_container_width=True)
with col2:
    st.plotly_chart(table_booking_split(filtered), use_container_width=True)

# ── Section 6: Top Chains ─────────────────────────────────────────────────────
st.markdown('<p class="section-header">🏆 Top Restaurant Chains</p>', unsafe_allow_html=True)
st.plotly_chart(top_restaurant_chains(filtered), use_container_width=True)
st.markdown("""
<div class="insight-box">
💡 <strong>Insight:</strong> Cafe Coffee Day and Domino's Pizza are the most widely distributed chains,
reflecting the growth of QSR (Quick Service Restaurant) culture in India.
</div>""", unsafe_allow_html=True)

# ── Raw Data ──────────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📄 View Raw Data"):
    st.dataframe(
        filtered[["Restaurant Name", "City", "Cuisines", "Aggregate rating",
                  "Average Cost for two", "Has Online delivery", "Has Table booking"]].head(200),
        use_container_width=True
    )

st.markdown("""
<br>
<center style="color:#475569; font-size:0.8rem;">
Built with ❤️ using Streamlit & Plotly &nbsp;|&nbsp; Data: Zomato via Kaggle
</center>
""", unsafe_allow_html=True)
