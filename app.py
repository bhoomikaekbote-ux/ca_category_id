import streamlit as st
import pandas as pd
import json
import plotly.express as px

st.set_page_config(
    page_title="YouTube Category Analytics",
    page_icon="📺",
    layout="wide"
)

# -----------------------
# LOAD DATA
# -----------------------

@st.cache_data
def load_data():

    with open("CA_category_id.json","r") as f:
        data = json.load(f)

    rows = []

    for item in data["items"]:

        rows.append({

            "Category_ID": item["id"],

            "Category":
            item["snippet"]["title"],

            "Assignable":
            item["snippet"]["assignable"],

            "ChannelID":
            item["snippet"]["channelId"]

        })

    return pd.DataFrame(rows)

df = load_data()

# -----------------------
# HEADER
# -----------------------

st.title("📺 YouTube Category Analytics Dashboard")

st.markdown(
"""
Interactive Analytics for Category Mapping
"""
)

# -----------------------
# SIDEBAR
# -----------------------

st.sidebar.header("Filters")

assignable = st.sidebar.multiselect(

    "Assignable",

    df["Assignable"].unique(),

    default=df["Assignable"].unique()

)

filtered = df[
    df["Assignable"].isin(assignable)
]

# -----------------------
# KPI SECTION
# -----------------------

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.metric(
        "Categories",
        len(filtered)
    )

with c2:

    st.metric(
        "Assignable",
        filtered["Assignable"].sum()
    )

with c3:

    st.metric(
        "Non Assignable",
        len(filtered) -
        filtered["Assignable"].sum()
    )

with c4:

    st.metric(
        "Unique Channels",
        filtered["ChannelID"].nunique()
    )

st.divider()

tabs = st.tabs([

    "Category Analytics",

    "Distribution",

    "Insights",

    "Data"

])

# -----------------------
# ANALYTICS
# -----------------------

with tabs[0]:

    fig = px.bar(

        filtered,

        x="Category",

        color="Assignable",

        title="Category Distribution"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig = px.treemap(

        filtered,

        path=["Assignable","Category"],

        title="Category Tree"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------
# DISTRIBUTION
# -----------------------

with tabs[1]:

    pie = px.pie(

        filtered,

        names="Assignable",

        title="Assignable Split"

    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

    hist = px.histogram(

        filtered,

        x="Category_ID",

        title="Category IDs"

    )

    st.plotly_chart(
        hist,
        use_container_width=True
    )

# -----------------------
# INSIGHTS
# -----------------------

with tabs[2]:

    assign_rate = round(

        (
        filtered["Assignable"]
        .sum()

        / len(filtered)

        )*100,

        1

    )

    st.success(

f"""

Total Categories: {len(filtered)}

Assignable Categories:
{assign_rate}%

Top Category:
{filtered['Category'].mode()[0]}

Unique Channel IDs:
{filtered['ChannelID'].nunique()}

"""

)

# -----------------------
# DATA TABLE
# -----------------------

with tabs[3]:

    st.dataframe(
        filtered,
        use_container_width=True
    )
