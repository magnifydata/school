# school_dashboard.py
import streamlit as st

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="School Dashboard",
    layout="wide"
)

# --- 2. Main Heading with Custom Color ---
st.markdown("<h1 style='text-align: center; color: darkgreen;'>School Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---") # Adds a horizontal rule

# --- 3. Sidebar Navigation Menu ---
# Using st.sidebar.radio to create the menu.
# The first argument is a label for the radio button group.
# The second argument is a list of options.
st.sidebar.title("Menu") # Optional: Add a title to the sidebar itself
selected_option = st.sidebar.radio(
    "Go to:",
    ("School", "Teachers", "Students", "Others")
)

# --- 4. Main Content Area - Display content based on sidebar selection ---
if selected_option == "School":
    st.header("🏫 School Information")
    st.write("This section will display general information about the school.")
    # Add more School-specific content here
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Students", value="1250", delta="50 this year")
    with col2:
        st.metric(label="Average Attendance", value="92%", delta="-1% from last month")
    with col3:
        st.metric(label="Staff Count", value="85", delta="2 new hires")
    st.write("More details about school infrastructure, accreditations, etc., can go here.")

elif selected_option == "Teachers":
    st.header("👩‍🏫 Teacher Management")
    st.write("This section is for managing and viewing teacher data.")
    # Add more Teacher-specific content here
    st.subheader("Teacher Overview")
    st.write("List of teachers, subjects taught, performance metrics, etc.")
    # Example: Placeholder for a teacher list or data input
    if st.button("Add New Teacher"):
        st.success("Teacher addition form would appear here.")

elif selected_option == "Students":
    st.header("🧑‍🎓 Student Insights")
    st.write("This section will focus on student data, performance, and demographics.")
    # Add more Student-specific content here
    st.subheader("Student Performance")
    st.write("Charts for grades, attendance trends, extracurricular activities.")
    # Example: Placeholder for a student search
    student_search = st.text_input("Search for a student by ID or Name:")
    if student_search:
        st.write(f"Displaying results for: {student_search}")

elif selected_option == "Others":
    st.header("⚙️ Other Utilities")
    st.write("This section can contain miscellaneous tools or information.")
    # Add more Other-specific content here
    st.subheader("Settings & Reports")
    if st.checkbox("Enable Advanced Reporting"):
        st.info("Advanced reporting features are now enabled.")
    st.download_button(
        label="Download General School Report (PDF)",
        data="This would be the PDF file content", # Replace with actual file data
        file_name="school_report.pdf",
        mime="application/pdf"
    )

# --- Footer (Optional) ---
st.markdown("---")
st.caption("School Dashboard v0.1 | Developed with Streamlit")


# --- How to run this app ---
# 1. Save this code as a Python file (e.g., school_dashboard.py).
# 2. Open your terminal or command prompt.
# 3. Navigate to the directory where you saved the file.
# 4. Run the command: streamlit run school_dashboard.py
# 5. Your browser will open with the app.
