import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data if False else lambda f: f
def load_data():
    df = pd.read_csv("data/zomato.csv", encoding="latin-1")
    country = pd.read_excel("data/Country-Code.xlsx")
    df = df.merge(country, on="Country Code", how="left")
    df.columns = df.columns.str.strip()
    df["Average Cost for two"] = pd.to_numeric(df["Average Cost for two"], errors="coerce")
    df["Aggregate rating"] = pd.to_numeric(df["Aggregate rating"], errors="coerce")
    df = df[df["Country"] == "India"].copy()  # Focus on India
    return df


def top_cities_by_restaurants(df, top_n=10):
    city_counts = df["City"].value_counts().head(top_n).reset_index()
    city_counts.columns = ["City", "Restaurant Count"]
    fig = px.bar(
        city_counts, x="City", y="Restaurant Count",
        color="Restaurant Count",
        color_continuous_scale="Oranges",
        title=f"Top {top_n} Cities by Number of Restaurants",
        template="plotly_dark"
    )
    fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
    return fig


def avg_rating_by_city(df, top_n=10):
    rating = (
        df[df["Aggregate rating"] > 0]
        .groupby("City")["Aggregate rating"]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    rating.columns = ["City", "Avg Rating"]
    fig = px.bar(
        rating, x="City", y="Avg Rating",
        color="Avg Rating",
        color_continuous_scale="RdYlGn",
        title=f"Top {top_n} Cities by Average Restaurant Rating",
        template="plotly_dark",
        range_y=[0, 5]
    )
    fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-30)
    return fig


def cuisine_popularity(df, top_n=15):
    cuisines = df["Cuisines"].dropna().str.split(", ").explode()
    top_cuisines = cuisines.value_counts().head(top_n).reset_index()
    top_cuisines.columns = ["Cuisine", "Count"]
    fig = px.bar(
        top_cuisines, x="Count", y="Cuisine",
        orientation="h",
        color="Count",
        color_continuous_scale="Sunset",
        title=f"Top {top_n} Most Popular Cuisines",
        template="plotly_dark"
    )
    fig.update_layout(coloraxis_showscale=False, yaxis={"categoryorder": "total ascending"})
    return fig


def price_vs_rating(df):
    sample = df[(df["Aggregate rating"] > 0) & (df["Average Cost for two"] > 0)].copy()
    sample = sample[sample["Average Cost for two"] < 5000]  # remove outliers
    fig = px.scatter(
        sample, x="Average Cost for two", y="Aggregate rating",
        color="City",
        size_max=8,
        opacity=0.6,
        title="Price vs Rating — Does Expensive Mean Better?",
        labels={"Average Cost for two": "Avg Cost for Two (₹)", "Aggregate rating": "Rating"},
        template="plotly_dark"
    )
    fig.update_traces(marker=dict(size=5))
    return fig


def online_delivery_split(df):
    counts = df["Has Online delivery"].value_counts().reset_index()
    counts.columns = ["Has Online Delivery", "Count"]
    fig = px.pie(
        counts, names="Has Online Delivery", values="Count",
        title="Online Delivery Availability",
        color_discrete_sequence=["#f97316", "#1e293b"],
        template="plotly_dark",
        hole=0.4
    )
    return fig


def table_booking_split(df):
    counts = df["Has Table booking"].value_counts().reset_index()
    counts.columns = ["Has Table Booking", "Count"]
    fig = px.pie(
        counts, names="Has Table Booking", values="Count",
        title="Table Booking Availability",
        color_discrete_sequence=["#f97316", "#1e293b"],
        template="plotly_dark",
        hole=0.4
    )
    return fig


def rating_distribution(df):
    rated = df[df["Aggregate rating"] > 0]
    fig = px.histogram(
        rated, x="Aggregate rating",
        nbins=20,
        color_discrete_sequence=["#f97316"],
        title="Distribution of Restaurant Ratings",
        template="plotly_dark",
        labels={"Aggregate rating": "Rating"}
    )
    fig.update_layout(bargap=0.05)
    return fig


def top_restaurant_chains(df, top_n=10):
    chains = df["Restaurant Name"].value_counts().head(top_n).reset_index()
    chains.columns = ["Restaurant Name", "Outlets"]
    fig = px.bar(
        chains, x="Outlets", y="Restaurant Name",
        orientation="h",
        color="Outlets",
        color_continuous_scale="Blues",
        title=f"Top {top_n} Restaurant Chains by Outlet Count",
        template="plotly_dark"
    )
    fig.update_layout(coloraxis_showscale=False, yaxis={"categoryorder": "total ascending"})
    return fig
