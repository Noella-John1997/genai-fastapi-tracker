import streamlit as st
import pandas as pd

st.set_page_config(page_title="30-Day GenAI + FastAPI Tracker", layout="wide")
st.title("📅 30-Day GenAI + FastAPI Learning Tracker")

# Load CSV data only once
@st.cache_data
def load_data():
    return pd.read_csv("30_day_plan.csv")

# Initialize session state
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    focus_area = st.multiselect("Focus Area", df['Focus Area'].unique())
    status = st.multiselect("Status", df['Status'].unique())

# Apply filters
filtered_df = df.copy()
if focus_area:
    filtered_df = filtered_df[filtered_df["Focus Area"].isin(focus_area)]
if status:
    filtered_df = filtered_df[filtered_df["Status"].isin(status)]

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Tasks", len(df))
col2.metric("✅ Completed", (df['Status'] == '✅ Done').sum())
col3.metric("🚧 In Progress", (df['Status'] == '🚧 In Progress').sum())

# Editable task list
st.markdown("### ✅ Mark Tasks as Done / In Progress")

# For each row, show checkbox and update status
for i, row in filtered_df.iterrows():
    task_label = f'**Day {row["Day"]}** - {row["Activity"]} ({row["Focus Area"]})'
    checked = row["Status"] == "✅ Done"
    checkbox = st.checkbox(task_label, value=checked, key=f"task_{i}")

    # Update status in the main df
    original_index = row.name  # Index in the original df
    st.session_state.df.at[original_index, "Status"] = "✅ Done" if checkbox else "🚧 In Progress"

# Progress chart
st.markdown("### 📊 Progress Breakdown")
status_counts = st.session_state.df['Status'].value_counts()
st.bar_chart(status_counts)

# Save button
if st.button("💾 Save Progress"):
    st.session_state.df.to_csv("30_day_plan.csv", index=False)
    st.success("Progress saved successfully!")
