# school_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime  # For date operations
import plotly.express as px # For Pie Chart

# --- Helper Function for Financial Data Generation ---
def generate_financial_data(start_date, end_date):
    """Generates sample financial data for the given date range."""
    num_days = (end_date - start_date).days + 1
    if num_days <= 0:
        dates = pd.to_datetime([start_date]) # Use start_date if range is invalid
        num_days = 1
    else:
        dates = pd.date_range(start_date, end_date, freq='D')

    # Cash on Hand
    initial_cash = 250000
    cash_fluctuations = np.random.randint(-10000, 10000, size=len(dates))
    cash_on_hand_trend = initial_cash + np.cumsum(cash_fluctuations)
    cash_data = pd.DataFrame({'Date': dates, 'Cash on Hand ($)': cash_on_hand_trend}).set_index('Date')

    # Fixed Deposits (simplified: total value of FDs)
    initial_fd_value = 1000000
    fd_growth_rate_daily = np.random.uniform(0.00005, 0.00015, size=len(dates)) # Small daily interest
    fd_value_trend = initial_fd_value * np.cumprod(1 + fd_growth_rate_daily)
    fd_data = pd.DataFrame({'Date': dates, 'Fixed Deposit Value ($)': fd_value_trend}).set_index('Date')

    # Outstanding Payments (snapshot for the end_date)
    outstanding_categories = ["Tuition Fees", "Activity Fees", "Transport Fees", "Other Dues"]
    outstanding_amounts = np.random.randint(5000, 75000, size=len(outstanding_categories))
    outstanding_df = pd.DataFrame({
        'Category': outstanding_categories,
        'Amount Outstanding ($)': outstanding_amounts
    })

    # Expenditure Breakdown (snapshot for the current period view)
    exp_categories = ["Salaries", "Utilities", "Supplies", "Maintenance", "Academics", "Admin"]
    exp_amounts = np.random.randint(20000, 150000, size=len(exp_categories))
    expenditure_breakdown_df = pd.DataFrame({
        'Category': exp_categories,
        'Amount ($)': exp_amounts
    })

    return cash_data, fd_data, outstanding_df, expenditure_breakdown_df

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="School Dashboard",
    layout="wide"
)

# Attempt to reduce top padding of the main content area
st.markdown("""
    <style>
        div.block-container {
            padding-top: 1.5rem !important; /* Adjust this value as needed */
        }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Main Heading with Custom Color and reduced margin ---
st.markdown("<h1 style='text-align: center; color: darkgreen; margin-bottom: 0.5rem;'>School Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---") # Adds a horizontal rule

# --- 3. Sidebar Navigation Menu ---
st.sidebar.title("Menu")
main_options = ("School", "Teachers", "Students", "Others")
selected_main_option = st.sidebar.selectbox(
    "Go to:",
    main_options,
    key="main_menu_selectbox"
)

# --- 4. Main Content Area - Display content based on sidebar selection ---

# --- SCHOOL SECTION ---
if selected_main_option == "School":
    st.header("🏫 School Information")

    st.sidebar.subheader("School Details")
    school_sub_options = ("Financial", "Facilities", "Academic Programs")
    school_sub_option = st.sidebar.selectbox(
        "Select Category:",
        school_sub_options,
        key="school_submenu_selectbox"
    )
    st.sidebar.markdown("---")

    if school_sub_option == "Financial":
        st.subheader("💰 Financial Overview")
        # Removed st.write("This section displays...") for compactness

        # Date Range Selector - Placed prominently at the top of this section
        today = datetime.date.today()
        default_start_date = today - datetime.timedelta(days=29) # Default to last 30 days

        date_label_col, date_input_col = st.columns([0.3, 0.7]) # Adjust ratio as needed
        with date_label_col:
            st.markdown("<p style='font-weight:bold; margin-top:7px; margin-bottom:0px;'>Date Range for Trends:</p>", unsafe_allow_html=True)
        with date_input_col:
            selected_date_range = st.date_input(
                "Select Date Range for Trends:", # Actual label hidden
                value=(default_start_date, today),
                min_value=datetime.date(2020, 1, 1),
                max_value=today + datetime.timedelta(days=365),
                key="financial_date_range_selector",
                label_visibility="collapsed" # Hides the default Streamlit label
            )
        # st.markdown("---") # Separator after date input, can be removed if too much space

        # Metrics
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric(label="Annual Budget", value="$5,000,000", delta="$200,000 vs LY", delta_color="normal")
        with m_col2:
            st.metric(label="YTD Expenditure", value="$2,350,000", delta="47% of Budget", delta_color="off") # "off" for neutral display

        st.markdown("---") # Separator after metrics

        if len(selected_date_range) == 2:
            start_date, end_date = selected_date_range
            if start_date <= end_date:
                cash_data, fd_data, outstanding_df, expenditure_df = generate_financial_data(start_date, end_date)

                # Charts in two columns
                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    st.markdown("###### Cash on Hand Trend")
                    st.line_chart(cash_data['Cash on Hand ($)'], height=220)

                    st.markdown("###### Fixed Deposits Value Trend")
                    st.line_chart(fd_data['Fixed Deposit Value ($)'], height=220)

                with chart_col2:
                    st.markdown("###### Expenditure Breakdown") # External title for consistency
                    if not expenditure_df.empty:
                        fig_pie = px.pie(expenditure_df,
                                         values='Amount ($)',
                                         names='Category',
                                         hole=0.4, # Creates a donut chart
                                         # title="Expenditure Breakdown" # Title can be here or above
                                         )
                        fig_pie.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05]*len(expenditure_df.index))
                        fig_pie.update_layout(
                            margin=dict(l=10, r=10, t=30, b=10), # Adjusted margins
                            height=235, # Slightly more height for pie
                            showlegend=False, # Legend hidden as info is on slices
                            # title_x=0.5, title_font_size=14 # If using Plotly title
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.info("No expenditure data to display.")

                    st.markdown("###### Current Outstanding Payments")
                    if not outstanding_df.empty:
                        st.bar_chart(outstanding_df.set_index('Category')['Amount Outstanding ($)'], height=220)
                    else:
                        st.info("No outstanding payments data.")
            else:
                st.warning("Start date must be before or the same as the end date.")
        else:
            st.info("Select a valid date range (start and end date) to view financial trends.")


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
        selected_program = st.selectbox("View Program Details:", programs)
        st.write(f"Showing details for {selected_program}...")
        st.write("Curriculum outline, head of department, student enrollment numbers, etc.")

# --- TEACHERS SECTION ---
elif selected_main_option == "Teachers":
    st.header("👩‍🏫 Teacher Management")
    st.sidebar.subheader("Teacher Details")
    teacher_sub_options = ("Teacher Profiles", "Analysis", "KPIs", "Performance Logs")
    teacher_sub_option = st.sidebar.selectbox(
        "Select Category:",
        teacher_sub_options,
        key="teacher_submenu_selectbox"
    )
    st.sidebar.markdown("---")

    if teacher_sub_option == "Teacher Profiles":
        st.subheader("👤 Teacher Profiles")
        st.write("View and manage individual teacher profiles.")
        teacher_names = ["Dr. Alice Smith", "Mr. Bob Johnson", "Ms. Carol Williams"]
        selected_teacher = st.selectbox("Select Teacher:", teacher_names)
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
    st.sidebar.subheader("Student Options")
    student_sub_options = ("Performance Tracking", "Student Search", "Demographics", "Attendance")
    student_sub_option = st.sidebar.selectbox(
        "Select Category:",
        student_sub_options,
        key="student_submenu_selectbox"
    )
    st.sidebar.markdown("---")

    if student_sub_option == "Performance Tracking":
        st.subheader("📈 Student Performance")
        st.write("Charts for grades, progress over time, and subject-wise performance.")
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
            st.write(f"Student ID: [ID for {student_search_query}]")
            st.write(f"Name: {student_search_query}")
            st.write(f"Grade: [Grade]")
            st.write(f"Contact: [Contact Info]")
        else:
            st.info("Enter a student ID or name to search.")

    elif student_sub_option == "Demographics":
        st.subheader("📊 Student Demographics")
        st.write("Overview of student population, diversity, and enrollment statistics.")
        demo_data = pd.DataFrame({
            'Grade Level': ['Grade 9', 'Grade 10', 'Grade 11', 'Grade 12'],
            'Number of Students': [120, 110, 100, 90]
        })
        st.area_chart(demo_data.set_index('Grade Level'))
        st.write("Breakdown by age, gender, region, etc.")

    elif student_sub_option == "Attendance":
        st.subheader("📅 Attendance Records")
        st.write("Track student attendance, view trends, and generate reports.")
        st.metric(label="Overall Attendance Rate", value="93%", delta="1% from last month")
        st.write("Daily/Weekly attendance logs, absenteeism alerts.")
        st.selectbox("Select Class for Attendance View:", ["Class A", "Class B", "Class C"])
        st.write("Displaying attendance for selected class...")

# --- OTHERS SECTION ---
elif selected_main_option == "Others":
    st.header("⚙️ Other Utilities")
    st.sidebar.subheader("Utilities Menu")
    other_sub_options = ("Settings & Reports", "Event Calendar", "Resource Links")
    other_sub_option = st.sidebar.selectbox(
        "Select Category:",
        other_sub_options,
        key="other_submenu_selectbox"
    )
    st.sidebar.markdown("---")

    if other_sub_option == "Settings & Reports":
        st.subheader("🔧 Settings & General Reports")
        if st.checkbox("Enable Advanced Reporting Features", key="adv_reporting_cb"):
            st.info("Advanced reporting features are now enabled.")
        else:
            st.info("Advanced reporting features are disabled.")

        st.download_button(
            label="Download General School Report (PDF)",
            data="This would be the PDF file content if generated.",
            file_name="school_report.pdf",
            mime="application/pdf"
        )
        st.write("More settings like notification preferences, user roles (future).")

    elif other_sub_option == "Event Calendar":
        st.subheader("🗓️ School Event Calendar")
        st.write("View upcoming school events, holidays, and important dates.")
        st.date_input("Select a date to view events:", datetime.date.today(), key="event_calendar_date")
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
st.caption("School Dashboard v0.6 | Developed with Streamlit")
