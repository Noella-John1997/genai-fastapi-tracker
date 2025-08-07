import streamlit as st
import pandas as pd

st.set_page_config(page_title="📅 30-Day GenAI + FastAPI Tracker", layout="wide")
st.title("📅 30-Day GenAI + FastAPI Learning Tracker")

# Load the uploaded CSV
@st.cache_data
def load_data():
    return pd.read_csv("30_day_plan.csv")

# Load data only once
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters")
    focus_area = st.multiselect("Focus Area", df['Focus Area'].unique())
    status = st.multiselect("Status", df['Status'].unique())

# Filtered dataframe (for viewing)
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

# Editable full task table with checkboxes
st.markdown("### 📋 All Tasks (Mark ✅ Done or 🚧 In Progress)")

edited_rows = []

# Render the full editable table
for i, row in filtered_df.iterrows():
    col1, col2 = st.columns([0.05, 0.95])
    is_done = row['Status'] == "✅ Done"
    checkbox = col1.checkbox("", value=is_done, key=f"task_{i}")
    task_display = f"**Day {row['Day']}** | 📅 {row['Date']} | 🧠 *{row['Focus Area']}*  \n🔗 [Learning Link]({row['Learning Link']})  \n🛠️ {row['Build Task']}"
    col2.markdown(task_display)
    # Update status in the main DataFrame
    df.at[i, 'Status'] = "✅ Done" if checkbox else "🚧 In Progress"

# Progress breakdown chart
st.markdown("### 📊 Progress Breakdown")
status_counts = df['Status'].value_counts()
st.bar_chart(status_counts)

# Save button
if st.button("💾 Save Progress"):
    df.to_csv("30_day_plan.csv", index=False)
    st.success("Progress saved to file!")
