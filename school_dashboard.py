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
st.sidebar.title("Menu")
selected_main_option = st.sidebar.radio(
    "Go to:",
    ("School", "Teachers", "Students", "Others"),
    key="main_menu" # Adding a key for clarity if we add more radio groups
)

# --- 4. Main Content Area - Display content based on sidebar selection ---

# --- SCHOOL SECTION ---
if selected_main_option == "School":
    st.header("🏫 School Information") # Main area header for School

    # --- School Sub-Menu (conditionally shown in the sidebar) ---
    st.sidebar.markdown("---") # Optional separator
    st.sidebar.subheader("School Details")
    school_sub_option = st.sidebar.radio(
        "Select Category:",
        ("Financial", "Facilities", "Academic Programs"), # Added "Academic Programs" as the 3rd option
        key="school_submenu"
    )
    st.sidebar.markdown("---") # Optional separator

    # --- Display content based on School sub-menu selection (in the main area) ---
    if school_sub_option == "Financial":
        st.subheader("💰 Financial Overview")
        st.write("This section displays financial data, budgets, and expenditure.")
        # Placeholder for financial metrics or charts
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Annual Budget", value="$5,000,000", delta="$200,000 from last year")
        with col2:
            st.metric(label="Current Expenditure", value="$2,350,000", delta="47% of budget")
        st.write("More detailed financial reports, income sources, etc.")

    elif school_sub_option == "Facilities":
        st.subheader("🏗️ Facilities Management")
        st.write("Information about school buildings, maintenance, and resources.")
        # Placeholder for facilities info
        st.map(data=None) # Example: Could show a map of school buildings if you have lat/lon data
        st.write("Classroom availability, lab equipment status, sports facilities.")

    elif school_sub_option == "Academic Programs":
        st.subheader("📚 Academic Programs")
        st.write("Details about courses, curriculum, and academic departments.")
        # Placeholder for academic program info
        programs = ["Computer Science", "Humanities", "Mathematics", "Physical Education", "Arts"]
        selected_program = st.selectbox("View Program Details:", programs)
        st.write(f"Showing details for {selected_program}...")
        st.write("Curriculum outline, head of department, student enrollment numbers, etc.")

# --- TEACHERS SECTION ---
elif selected_main_option == "Teachers":
    st.header("👩‍🏫 Teacher Management")
    st.write("This section is for managing and viewing teacher data.")
    st.subheader("Teacher Overview")
    st.write("List of teachers, subjects taught, performance metrics, etc.")
    if st.button("Add New Teacher"):
        st.success("Teacher addition form would appear here.")

# --- STUDENTS SECTION ---
elif selected_main_option == "Students":
    st.header("🧑‍🎓 Student Insights")
    st.write("This section will focus on student data, performance, and demographics.")
    st.subheader("Student Performance")
    st.write("Charts for grades, attendance trends, extracurricular activities.")
    student_search = st.text_input("Search for a student by ID or Name:")
    if student_search:
        st.write(f"Displaying results for: {student_search}")

# --- OTHERS SECTION ---
elif selected_main_option == "Others":
    st.header("⚙️ Other Utilities")
    st.write("This section can contain miscellaneous tools or information.")
    st.subheader("Settings & Reports")
    if st.checkbox("Enable Advanced Reporting"):
        st.info("Advanced reporting features are now enabled.")
    st.download_button(
        label="Download General School Report (PDF)",
        data="This would be the PDF file content",
        file_name="school_report.pdf",
        mime="application/pdf"
    )

# --- Footer (Optional) ---
st.markdown("---")
st.caption("School Dashboard v0.2 | Developed with Streamlit")

# --- How to run this app ---
# 1. Save this code as a Python file (e.g., school_dashboard.py).
# 2. Open your terminal or command prompt.
# 3. Navigate to the directory where you saved the file.
# 4. Run the command: streamlit run school_dashboard.py
# 5. Your browser will open with the app.
