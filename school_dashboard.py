# school_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import os # To construct file paths robustly

# --- Helper Functions for Loading Data from CSVs ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Gets the directory where the script is located

def load_csv_data(file_name, date_col=None, index_col=None):
    """Loads data from a CSV file located in the same directory as the script."""
    file_path = os.path.join(BASE_DIR, file_name) # File is in the same directory as the script
    try:
        if date_col:
            df = pd.read_csv(file_path, parse_dates=[date_col])
        else:
            df = pd.read_csv(file_path)
        if index_col:
            df = df.set_index(index_col)
        return df
    except FileNotFoundError:
        st.error(f"Error: Data file '{file_name}' not found in the script's directory ('{BASE_DIR}'). Please ensure it exists there.")
        return pd.DataFrame() # Return empty DataFrame on error
    except Exception as e:
        st.error(f"Error loading '{file_name}': {e}")
        return pd.DataFrame()

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="School Dashboard",
    layout="wide"
)

st.markdown("""
    <style>
        div.block-container {padding-top: 1.5rem !important;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: darkgreen; margin-bottom: 0.5rem;'>School Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.title("Menu")
main_options = ("School", "Teachers", "Students", "Others")
selected_main_option = st.sidebar.selectbox("Go to:", main_options, key="main_menu_selectbox")

# --- SCHOOL SECTION ---
if selected_main_option == "School":
    st.header("🏫 School Information")
    st.sidebar.subheader("School Details")
    school_sub_options = ("Financial", "Facilities", "Academic Programs")
    school_sub_option = st.sidebar.selectbox("Select Category:", school_sub_options, key="school_submenu_selectbox")
    st.sidebar.markdown("---")

    if school_sub_option == "Financial":
        st.subheader("💰 Financial Overview")

        today = datetime.date.today()
        default_start_date = today - datetime.timedelta(days=29)
        date_label_col, date_input_col = st.columns([0.3, 0.7])
        with date_label_col:
            st.markdown("<p style='font-weight:bold; margin-top:7px; margin-bottom:0px;'>Date Range for Trends:</p>", unsafe_allow_html=True)
        with date_input_col:
            selected_date_range = st.date_input(
                "Select Date Range for Trends:",
                value=(default_start_date, today),
                min_value=datetime.date(2020, 1, 1),
                max_value=today + datetime.timedelta(days=365),
                key="financial_date_range_selector",
                label_visibility="collapsed"
            )

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric(label="Annual Budget", value="$5,000,000", delta="$200,000 vs LY", delta_color="normal")
        with m_col2:
            st.metric(label="YTD Expenditure", value="$2,350,000", delta="47% of Budget", delta_color="off")
        st.markdown("---")

        if len(selected_date_range) == 2:
            start_date, end_date = selected_date_range
            start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
            end_datetime = datetime.datetime.combine(end_date, datetime.time.max)

            if start_date <= end_date:
                cash_data_full = load_csv_data("cash_on_hand_trend.csv", date_col='Date', index_col='Date')
                fd_data_full = load_csv_data("fixed_deposits_trend.csv", date_col='Date', index_col='Date')
                expenditure_df = load_csv_data("expenditure_breakdown.csv")
                outstanding_df = load_csv_data("outstanding_payments.csv")

                cash_data_filtered = cash_data_full[(cash_data_full.index >= start_datetime) & (cash_data_full.index <= end_datetime)]
                fd_data_filtered = fd_data_full[(fd_data_full.index >= start_datetime) & (fd_data_full.index <= end_datetime)]

                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    st.markdown("###### Cash on Hand Trend")
                    if not cash_data_filtered.empty:
                        st.line_chart(cash_data_filtered['Cash_on_Hand_USD'], height=220)
                    else:
                        st.info("No cash on hand data for selected range or file missing/malformed.")

                    st.markdown("###### Fixed Deposits Value Trend")
                    if not fd_data_filtered.empty:
                        st.line_chart(fd_data_filtered['Fixed_Deposit_Value_USD'], height=220)
                    else:
                        st.info("No fixed deposit data for selected range or file missing/malformed.")

                with chart_col2:
                    st.markdown("###### Expenditure Breakdown")
                    if not expenditure_df.empty and 'Category' in expenditure_df.columns and 'Amount_USD' in expenditure_df.columns:
                        fig_pie = px.pie(expenditure_df, values='Amount_USD', names='Category', hole=0.4)
                        fig_pie.update_traces(textposition='inside', textinfo='percent+label', pull=[0.05]*len(expenditure_df.index))
                        fig_pie.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=235, showlegend=False)
                        st.plotly_chart(fig_pie, use_container_width=True)
                    else:
                        st.info("Expenditure data missing or malformed.")

                    st.markdown("###### Current Outstanding Payments")
                    if not outstanding_df.empty and 'Category' in outstanding_df.columns and 'Amount_Outstanding_USD' in outstanding_df.columns:
                        st.bar_chart(outstanding_df.set_index('Category')['Amount_Outstanding_USD'], height=220)
                    else:
                        st.info("Outstanding payments data missing or malformed.")
            else:
                st.warning("Start date must be before or the same as the end date.")
        else:
            st.info("Select a valid date range (start and end date) to view financial trends.")

    elif school_sub_option == "Facilities":
        st.subheader("🏗️ Facilities Management")
        st.write("Information about school buildings, maintenance, and resources.")
        map_data_df = load_csv_data("facilities_locations.csv") # Example for facilities
        if not map_data_df.empty and 'lat' in map_data_df.columns and 'lon' in map_data_df.columns:
            st.map(map_data_df[['lat', 'lon']])
        else:
            st.info("Facility location data (facilities_locations.csv with 'lat', 'lon' columns) not found or malformed. Displaying placeholder.")
            # Fallback to placeholder map if CSV is missing/wrong
            map_placeholder = pd.DataFrame(np.random.randn(1, 2) / [10, 10] + [37.76, -122.4], columns=['lat', 'lon'])
            st.map(map_placeholder)
        st.write("Classroom availability, lab equipment status, sports facilities.")

    elif school_sub_option == "Academic Programs":
        st.subheader("📚 Academic Programs")
        st.write("Details about courses, curriculum, and academic departments.")
        # Example: load programs from a CSV
        programs_df = load_csv_data("academic_programs.csv")
        if not programs_df.empty and 'Program_Name' in programs_df.columns:
            programs = programs_df['Program_Name'].tolist()
        else:
            programs = ["Computer Science", "Humanities", "Mathematics"] # Fallback
            st.info("Academic programs data (academic_programs.csv with 'Program_Name' column) not found. Using defaults.")

        selected_program = st.selectbox("View Program Details:", programs)
        st.write(f"Showing details for {selected_program}...")
        # You could load more details about the selected_program from the programs_df or another CSV
        st.write("Curriculum outline, head of department, student enrollment numbers, etc.")

# --- TEACHERS SECTION ---
elif selected_main_option == "Teachers":
    st.header("👩‍🏫 Teacher Management")
    st.sidebar.subheader("Teacher Details")
    teacher_sub_options = ("Teacher Profiles", "Analysis", "KPIs", "Performance Logs")
    teacher_sub_option = st.sidebar.selectbox("Select Category:", teacher_sub_options, key="teacher_submenu_selectbox")
    st.sidebar.markdown("---")

    # ... (Teacher content - can also be modified to load data from CSVs)

# --- STUDENTS SECTION ---
elif selected_main_option == "Students":
    st.header("🧑‍🎓 Student Insights")
    st.sidebar.subheader("Student Options")
    student_sub_options = ("Performance Tracking", "Student Search", "Demographics", "Attendance")
    student_sub_option = st.sidebar.selectbox("Select Category:", student_sub_options, key="student_submenu_selectbox")
    st.sidebar.markdown("---")

    # ... (Student content - can also be modified to load data from CSVs)


# --- OTHERS SECTION ---
elif selected_main_option == "Others":
    st.header("⚙️ Other Utilities")
    st.sidebar.subheader("Utilities Menu")
    other_sub_options = ("Settings & Reports", "Event Calendar", "Resource Links")
    other_sub_option = st.sidebar.selectbox("Select Category:", other_sub_options, key="other_submenu_selectbox")
    st.sidebar.markdown("---")

    # ... (Others content)

# --- Footer (Optional) ---
st.markdown("---")
st.caption("School Dashboard v0.8 | Developed with Streamlit")
