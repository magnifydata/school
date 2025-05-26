# school_dashboard.py
import streamlit as st

# --- 1. Page Configuration (Optional but good practice) ---
# You can set the page title that appears in the browser tab and other layout options.
# This should be the first Streamlit command in your script.
st.set_page_config(
    page_title="School Dashboard",
    layout="wide"  # Options: "centered" or "wide"
)

# --- 2. Main Heading with Custom Color ---
# We use st.markdown to inject HTML with inline CSS for the color.
# You can also adjust text-align, font-size, etc., here if needed.
st.markdown("<h1 style='text-align: center; color: darkgreen;'>School Dashboard</h1>", unsafe_allow_html=True)

# --- 3. Add some placeholder content below the title ---
st.write("Welcome! This dashboard will provide insights into school data.")
st.markdown("---") # Adds a horizontal rule (a line)

st.subheader("Key Metrics (Coming Soon)")
# You can add columns for layout
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Students", value="N/A", delta="N/A")

with col2:
    st.metric(label="Average Attendance", value="N/A", delta="N/A")

with col3:
    st.metric(label="Staff Count", value="N/A", delta="N/A")

# --- How to run this app ---
# 1. Save this code as a Python file (e.g., school_dashboard.py).
# 2. Open your terminal or command prompt.
# 3. Navigate to the directory where you saved the file.
# 4. Run the command: streamlit run school_dashboard.py
# 5. Your browser will open with the app.
