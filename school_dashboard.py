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
main_options = ("School", "Teachers", "Students", "Others")
selected_main_option = st.sidebar.selectbox(
    "Go to:",
    main_options,
    key="main_menu_selectbox" # Changed from radio to selectbox
)

# --- 4. Main Content Area - Display content based on sidebar selection ---

# --- SCHOOL SECTION ---
if selected_main_option == "School":
    st.header("🏫 School Information")

    # School Sub-Menu (conditionally shown in the sidebar with selectbox)
    st.sidebar.markdown("---")
    st.sidebar.subheader("School Details")
    school_sub_options = ("Financial", "Facilities", "Academic Programs")
    school_sub_option = st.sidebar.selectbox(
        "Select Category:",
        school_sub_options,
        key="school_submenu_selectbox" # Changed from radio to selectbox
    )
    st.sidebar.markdown("---")

    # Display content based on School sub-menu selection
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
        map_data = pd.DataFrame(
            np.random.randn(1, 2) / [10, 10] + [37.76, -122.4], # Example coordinates
            columns=['lat', 'lon'])
        st.map(map_data)
        st.write("Classroom availability, lab equipment status, sports facilities.")

    elif school_sub_option == "Academic Programs":
        st.subheader("📚 Academic Programs")
        st.write("Details about courses, curriculum, and academic departments.")
        programs = ["Computer Science", "Humanities", "Mathematics", "Physical Education", "Arts"]
        selected_program = st.selectbox("View Program Details:", programs) # This selectbox is in the main area
        st.write(f"Showing details for {selected_program}...")
        st.write("Curriculum outline, head of department, student enrollment numbers, etc.")

# --- TEACHERS SECTION ---
elif selected_main_option == "Teachers":
    st.header("👩‍🏫 Teacher Management")

    # Teachers Sub-Menu (conditionally shown in the sidebar with selectbox)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Teacher Details")
    teacher_sub_options = ("Teacher Profiles", "Analysis", "KPIs", "Performance Logs")
    teacher_sub_option = st.sidebar.selectbox(
        "Select Category:",
        teacher_sub_options,
        key="teacher_submenu_selectbox" # Changed from radio to selectbox
    )
    st.sidebar.markdown("---")

    # Display content based on Teacher sub-menu selection
    if teacher_sub_option == "Teacher Profiles":
        st.subheader("👤 Teacher Profiles")
        st.write("View and manage individual teacher profiles.")
        teacher_names = ["Dr. Alice Smith", "Mr. Bob Johnson", "Ms. Carol Williams"]
        selected_teacher = st.selectbox("Select Teacher:", teacher_names) # Main area selectbox
        st.write(f"Displaying profile for {selected_teacher}:")
        st.write(f"- Subject: [Subject for {selected_teacher}]")
        st.write(f"- Years of Service: [Years for {selected_teacher}]")
        st.button(f"Edit Profile for {selected_teacher}")

    elif teacher_sub_option == "Analysis":
        st.subheader("📊 Teacher Data Analysis")
        st.write("Analyze aggregated teacher data, trends, and statistics.")
        st.write("Charts showing teacher distribution by department, experience level, qualifications, etc.")
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Experience (Yrs)', 'Student Satisfaction (Avg)', 'Publications']
        )
        st.line_chart(chart_data[['Experience (Yrs)', 'Student Satisfaction (Avg)']])

    elif teacher_sub_option == "KPIs":
        st.subheader("🎯 Key Performance Indicators (KPIs)")
        st.write("Track teacher-specific KPIs.")
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

    # Students Sub-Menu (conditionally shown in the sidebar with selectbox)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Student Options")
    student_sub_options = ("Performance Tracking", "Student Search", "Demographics", "Attendance")
    student_sub_option = st.sidebar.selectbox(
        "Select Category:",
        student_sub_options,
        key="student_submenu_selectbox"
    )
    st.sidebar.markdown("---")

    # Display content based on Student sub-menu selection
    if student_sub_option == "Performance Tracking":
        st.subheader("📈 Student Performance")
        st.write("Charts for grades, progress over time, and subject-wise performance.")
        # Placeholder for performance charts
        perf_data = pd.DataFrame({
            'Subject': ['Math', 'Science', 'English', 'History'],
            'Average Score': [85, 78, 92, 80]
        })
        st.bar_chart(perf_data.set_index('Subject'))
        st.write("Detailed reports on individual student achievements and areas for improvement.")

    elif student_sub_option == "Student Search":
        st.subheader("🔍 Student Search")
        student_search_query = st.text_input("Search for a student by ID or Name:", key="student_search_input")
        if student_search_query:
            st.write(f"Displaying results for: {student_search_query}")
            # Placeholder for search results
            st.write(f"Student ID: [ID for {student_search_query}]")
            st.write(f"Name: {student_search_query}")
            st.write(f"Grade: [Grade]")
            st.write(f"Contact: [Contact Info]")
        else:
            st.info("Enter a student ID or name to search.")

    elif student_sub_option == "Demographics":
        st.subheader("📊 Student Demographics")
        st.write("Overview of student population, diversity, and enrollment statistics.")
        # Placeholder for demographics charts
        demo_data = pd.DataFrame({
            'Grade Level': ['Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'],
            'Number of Students': [120, 110, 100, 90]
        })
        st.area_chart(demo_data.set_index('Grade Level'))
        st.write("Breakdown by age, gender, region, etc.")

    elif student_sub_option == "Attendance":
        st.subheader("📅 Attendance Records")
        st.write("Track student attendance, view trends, and generate reports.")
        # Placeholder for attendance data
        st.metric(label="Overall Attendance Rate", value="93%", delta="1% from last month")
        st.write("Daily/Weekly attendance logs, absenteeism alerts.")
        st.selectbox("Select Class for Attendance View:", ["Class A", "Class B", "Class C"])
        st.write("Displaying attendance for selected class...")


# --- OTHERS SECTION ---
elif selected_main_option == "Others":
    st.header("⚙️ Other Utilities")

    # Others Sub-Menu (conditionally shown in the sidebar with selectbox)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Utilities Menu")
    other_sub_options = ("Settings & Reports", "Event Calendar", "Resource Links")
    other_sub_option = st.sidebar.selectbox(
        "Select Category:",
        other_sub_options,
        key="other_submenu_selectbox"
    )
    st.sidebar.markdown("---")

    # Display content based on Other sub-menu selection
    if other_sub_option == "Settings & Reports":
        st.subheader("🔧 Settings & General Reports")
        if st.checkbox("Enable Advanced Reporting Features", key="adv_reporting_cb"):
            st.info("Advanced reporting features are now enabled.")
        else:
            st.info("Advanced reporting features are disabled.")

        st.download_button(
            label="Download General School Report (PDF)",
            data="This would be the PDF file content if generated.", # Placeholder data
            file_name="school_report.pdf",
            mime="application/pdf"
        )
        st.write("More settings like notification preferences, user roles (future).")

    elif other_sub_option == "Event Calendar":
        st.subheader("🗓️ School Event Calendar")
        st.write("View upcoming school events, holidays, and important dates.")
        # Placeholder for a calendar - could integrate with a calendar library or API
        st.date_input("Select a date to view events:", pd.to_datetime("today"))
        st.write("List of events for the selected date...")
        st.write("- School Assembly")
        st.write("- Parent-Teacher Meeting Sign-ups Open")

    elif other_sub_option == "Resource Links":
        st.subheader("🔗 Useful Resource Links")
        st.write("Quick links to important external or internal resources.")
        st.markdown("- [School Website](http://example.com)")
        st.markdown("- [Online Learning Portal](http://example.com/moodle)")
        st.markdown("- [Staff Directory](http://example.com/staff)")

# --- Footer (Optional) ---
st.markdown("---")
st.caption("School Dashboard v0.4 | Developed with Streamlit") # Corrected typo
