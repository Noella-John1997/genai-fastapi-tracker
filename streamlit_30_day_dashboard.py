
import streamlit as st
import pandas as pd

st.set_page_config(page_title="30-Day GenAI + FastAPI Tracker", layout="wide")
st.title("📅 30-Day GenAI + FastAPI Learning Tracker")

@st.cache_data
def load_data():
    return pd.read_csv("30_day_plan.csv")

df = load_data()

with st.sidebar:
    st.header("🔍 Filters")
    focus_area = st.multiselect("Focus Area", df['Focus Area'].unique())
    status = st.multiselect("Status", df['Status'].unique())

filtered_df = df.copy()
if focus_area:
    filtered_df = filtered_df[filtered_df["Focus Area"].isin(focus_area)]
if status:
    filtered_df = filtered_df[filtered_df["Status"].isin(status)]

col1, col2, col3 = st.columns(3)
col1.metric("Total Tasks", len(df))
col2.metric("✅ Completed", (df['Status'] == '✅ Done').sum())
col3.metric("🚧 In Progress", (df['Status'] == '🚧 In Progress').sum())

st.markdown("### 📋 Task List")
st.dataframe(filtered_df, use_container_width=True)

status_counts = df['Status'].value_counts()
st.markdown("### 📊 Progress Breakdown")
st.bar_chart(status_counts)
