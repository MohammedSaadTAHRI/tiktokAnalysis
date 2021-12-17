"""Tiktok analysis, By Mohammed Saad TAHRI
An app to visualze tiktok data."""
from pathlib import Path
import subprocess
import sys

import streamlit as st  # Import base streamlit dependency
import pandas as pd  # Import pandas to load the analytics data
import plotly.express as px  # Import plotly for viz

import tiktokanalysis

DATA_PATH = Path("tiktokanalysis/data/tiktokdata.csv")

st.set_page_config(layout="wide")  # Set page width to wide

# Create sidebar
st.sidebar.markdown(
    "<div><img src='https://png2png.com/wp-content/uploads/2021/08/Tiktok-logo-png.png' width=100 /><h1 style='display:inline-block'>Tiktok Analytics</h1></div>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "This dashboard allows you to analyse trending 📈 tiktoks using Python and Streamlit."
)
st.sidebar.markdown(
    "To get started <ol><li>Enter the <i>hashtag</i> you wish to analyse</li> <li>Hit <i>Get Data</i>.</li> <li>Get analyzing</li></ol>",
    unsafe_allow_html=True,
)

st.header("Analytics Dashboard")
with st.form("hashtag_search"):
    hashtag = st.text_input("Search for a hashtag here", value="")
    submitted = st.form_submit_button("Get Data")
    if submitted:
        data_status = subprocess.run([sys.executable, str(Path("tiktokanalysis/tiktok.py")), f"'{hashtag}'"])
        if data_status.returncode:
            raise Exception("Could not get the data from the API, Please try again.")
        df = pd.read_csv(DATA_PATH)
        fig = px.histogram(
            df, x="desc", hover_data=["desc"], y="stats_diggCount", height=300
        )
        st.plotly_chart(fig, use_container_width=True)

        left_col, right_col = st.columns(2)

        scatter1 = px.scatter(
            df,
            x="stats_shareCount",
            y="stats_commentCount",
            hover_data=["desc"],
            size="stats_playCount",
            color="stats_playCount",
        )
        left_col.plotly_chart(scatter1, use_container_width=True)

        scatter2 = px.scatter(
            df,
            x="authorStats_videoCount",
            y="authorStats_heartCount",
            hover_data=["author_nickname"],
            size="authorStats_followerCount",
            color="authorStats_followerCount",
        )
        right_col.plotly_chart(scatter2, use_container_width=True)

        # Show tabular dataframe in streamlit
        st.dataframe(df)