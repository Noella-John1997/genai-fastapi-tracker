import streamlit as st
import pandas as pd

# Set page layout
st.set_page_config(page_title="30-Day GenAI + FastAPI Tracker", layout="wide")
st.title("📅 30-Day GenAI + FastAPI Learning Tracker")

# Load data from CSV
@st.cache_data
def load_data():
    return pd.read_csv("30_day_plan.csv")

df = load_data()

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

# Display metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Tasks", len(df))
col2.metric("✅ Completed", (df['Status'] == '✅ Done').sum())
col3.metric("🚧 In Progress", (df['Status'] == '🚧 In Progress').sum())

# Display task checkboxes to mark/unmark completion
st.markdown("### 📋 Task List (Mark tasks as ✅ Done)")

for i, row in filtered_df.iterrows():
    task_label = f"**Day {row['Day']}** - {row['Build Task']} ({row['Focus Area']})"
    checked = row["Status"] == "✅ Done"
    checkbox = st.checkbox(task_label, value=checked, key=f"task_{row.name}")
    
    # Update main DataFrame with new status
    df.at[row.name, "Status"] = "✅ Done" if checkbox else "🚧 In Progress"

# Progress breakdown chart
st.markdown("### 📊 Progress Breakdown")
status_counts = df['Status'].value_counts()
st.bar_chart(status_counts)

# Save button (optional)
if st.button("💾 Save Progress"):
    df.to_csv("30_day_plan.csv", index=False)
    st.success("Progress saved!")
