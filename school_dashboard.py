# school_dashboard.py
import streamlit as st
import pandas as pd # For potential data display later
import numpy as np  # For potential data display later

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
    key="main_menu"
)

# --- 4. Main Content Area - Display content based on sidebar selection ---

# --- SCHOOL SECTION ---
if selected_main_option == "School":
    st.header("🏫 School Information")

    st.sidebar.markdown("---")
    st.sidebar.subheader("School Details")
    school_sub_option = st.sidebar.radio(
        "Select Category:",
        ("Financial", "Facilities", "Academic Programs"),
        key="school_submenu"
    )
    st.sidebar.markdown("---")

    if school_sub_option == "Financial":
        st.subheader("💰 Financial Overview")
        st.write("This section displays financial data, budgets, and expenditure.")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Annual Budget", value="$5,000,000", delta="$200,000 from last year")
        with col2:
            st.metric(label="Current Expenditure", value="$2,350,000", delta="47% of budget")
        st.write("More detailed financial reports, income sources, etc.")

    elif school_sub_option == "Facilities":
        st.subheader("🏗️ Facilities Management")
        st.write("Information about school buildings, maintenance, and resources.")
        # Example: Placeholder for a map. You'd need to provide actual data.
        # Create a dummy DataFrame for the map
        map_data = pd.DataFrame(
            np.random.randn(1, 2) / [10, 10] + [37.76, -122.4], # Example coordinates (San Francisco)
            columns=['lat', 'lon'])
        st.map(map_data)
        st.write("Classroom availability, lab equipment status, sports facilities.")

    elif school_sub_option == "Academic Programs":
        st.subheader("📚 Academic Programs")
        st.write("Details about courses, curriculum, and academic departments.")
        programs = ["Computer Science", "Humanities", "Mathematics", "Physical Education", "Arts"]
        selected_program = st.selectbox("View Program Details:", programs)
        st.write(f"Showing details for {selected_program}...")
        st.write("Curriculum outline, head of department, student enrollment numbers, etc.")

# --- TEACHERS SECTION ---
elif selected_main_option == "Teachers":
    st.header("👩‍🏫 Teacher Management") # Main area header for Teachers

    # --- Teachers Sub-Menu (conditionally shown in the sidebar) ---
    st.sidebar.markdown("---")
    st.sidebar.subheader("Teacher Details")
    teacher_sub_option = st.sidebar.radio(
        "Select Category:",
        ("Teacher Profiles", "Analysis", "KPIs", "Performance Logs"),
        key="teacher_submenu"
    )
    st.sidebar.markdown("---")

    # --- Display content based on Teacher sub-menu selection (in the main area) ---
    if teacher_sub_option == "Teacher Profiles":
        st.subheader("👤 Teacher Profiles")
        st.write("View and manage individual teacher profiles.")
        # Placeholder for teacher profiles
        teacher_names = ["Dr. Alice Smith", "Mr. Bob Johnson", "Ms. Carol Williams"]
        selected_teacher = st.selectbox("Select Teacher:", teacher_names)
        st.write(f"Displaying profile for {selected_teacher}:")
        st.write(f"- Subject: [Subject for {selected_teacher}]")
        st.write(f"- Years of Service: [Years for {selected_teacher}]")
        st.button(f"Edit Profile for {selected_teacher}")

    elif teacher_sub_option == "Analysis":
        st.subheader("📊 Teacher Data Analysis")
        st.write("Analyze aggregated teacher data, trends, and statistics.")
        # Placeholder for analysis charts
        st.write("Charts showing teacher distribution by department, experience level, qualifications, etc.")
        # Example dummy chart
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Experience (Yrs)', 'Student Satisfaction (Avg)', 'Publications']
        )
        st.line_chart(chart_data[['Experience (Yrs)', 'Student Satisfaction (Avg)']])


    elif teacher_sub_option == "KPIs":
        st.subheader("🎯 Key Performance Indicators (KPIs)")
        st.write("Track teacher-specific KPIs.")
        # Placeholder for KPIs
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        with kpi_col1:
            st.metric(label="Avg. Class Rating", value="4.5/5", delta="0.1")
        with kpi_col2:
            st.metric(label="Student Pass Rate", value="88%", delta="-2%")
        with kpi_col3:
            st.metric(label="Professional Dev. Hours", value="40 Hrs", delta="5 Hrs")
        st.write("More KPIs related to student engagement, curriculum development, etc.")

    elif teacher_sub_option == "Performance Logs":
        st.subheader("📝 Performance Logs")
        st.write("Maintain and review teacher performance logs and appraisals.")
        # Placeholder for performance logs
        st.text_area("Enter New Log Entry:", "Date: [YYYY-MM-DD]\nObserver: [Name]\nFeedback: [Details]")
        st.button("Save Log Entry")
        st.write("---")
        st.write("Recent Log Entries:")
        st.dataframe({
            'Date': ['2023-10-15', '2023-09-01'],
            'Teacher': ['Dr. Alice Smith', 'Mr. Bob Johnson'],
            'Summary': ['Excellent student engagement observed.', 'Constructive feedback on lesson pacing.']
        })


# --- STUDENTS SECTION ---
elif selected_main_option == "Students":
    st.header("🧑‍🎓 Student Insights")
    st.write("This section will focus on student data, performance, and demographics.")
    # We can add a sub-menu for students later if needed
    st.subheader("Student Performance")
    st.write("Charts for grades, attendance trends, extracurricular activities.")
    student_search = st.text_input("Search for a student by ID or Name:")
    if student_search:
        st.write(f"Displaying results for: {student_search}")

# --- OTHERS SECTION ---
elif selected_main_option == "Others":
    st.header("⚙️ Other Utilities")
    st.write("This section can contain miscellaneous tools or information.")
    # We can add a sub-menu for others later if needed
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
st.caption("School Dashboard v0.3 | Developed with Streamlit")
