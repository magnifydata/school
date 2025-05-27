# dashboard_intermediate_test.py
import streamlit as st
import pandas as pd
import numpy as np # Though not directly used in this simplified version, good to keep if expanding
import datetime
import plotly.express as px
import os

st.set_page_config(page_title="Intermediate Dashboard", layout="wide")

st.markdown("""
    <style>
        div.block-container {padding-top: 1.5rem !important;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: darkgreen; margin-bottom: 0.5rem;'>Intermediate School Dashboard</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Helper Function for Loading Data from CSVs ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_csv_data(file_name, date_col=None, index_col=None):
    file_path = os.path.join(BASE_DIR, file_name)
    try:
        if date_col:
            df = pd.read_csv(file_path, parse_dates=[date_col])
        else:
            df = pd.read_csv(file_path)
        if index_col:
            df = df.set_index(index_col)
        return df
    except FileNotFoundError:
        st.error(f"Error: Data file '{file_name}' not found in '{BASE_DIR}'. Please create it or check the path.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading '{file_name}': {e}")
        return pd.DataFrame()

# --- Sidebar ---
st.sidebar.title("Menu")
selected_main_option = st.sidebar.selectbox(
    "Go to:",
    ("School", "Teachers"), # Simplified menu for now
    key="main_menu_selectbox"
)

# --- Main Content ---
if selected_main_option == "School":
    st.header("🏫 School Information")
    st.sidebar.subheader("School Details")
    school_sub_option = st.sidebar.selectbox(
        "Select Category:",
        ("Financial", "Facilities"), # Simplified sub-menu
        key="school_submenu_selectbox"
    )
    st.sidebar.markdown("---")


    if school_sub_option == "Financial":
        st.subheader("💰 Financial Overview")

        # --- CSV Files Information ---
        # Expected CSVs in the same directory as this script:
        # 1. cash_on_hand_trend.csv
        #    Example:
        #    Date,Cash_on_Hand_USD
        #    2023-09-01,230000
        #    2023-10-01,245000
        #    ...
        # 2. expenditure_breakdown.csv
        #    Example:
        #    Category,Amount_USD
        #    Salaries,125000
        #    Utilities,28000
        #    ...

        # Adjust these defaults to match your actual data's date range for testing
        # Your data is for May 2024
        data_start_date = datetime.date(2024, 5, 21)
        data_end_date = datetime.date(2024, 5, 27) # Or a bit later if you might add more data

        # Sensible default selection for the date picker
        default_picker_start = data_start_date
        default_picker_end = data_end_date # or min(data_end_date, datetime.date.today()) if you want it to not go past today by default

        # Min and Max for the calendar itself
        calendar_min_date = datetime.date(2024, 1, 1) # Allow selection from start of 2024
        calendar_max_date = datetime.date(2025, 12, 31) # Allow selection well into the future

        selected_date_range = st.date_input(
            "Select Date Range for Trends:",
            value=(default_picker_start, default_picker_end), # Default to cover your May 2024 data
            min_value=calendar_min_date,    # Earliest date selectable in calendar
            max_value=calendar_max_date,    # Latest date selectable in calendar
            key="financial_date_range_selector"
        )

        st.markdown("---")

        if len(selected_date_range) == 2:
            start_date, end_date = selected_date_range
            start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
            end_datetime = datetime.datetime.combine(end_date, datetime.time.max)

            # --- DEBUG PRINTS FOR DATE RANGE ---
            print(f"DEBUG: Selected Start Date (from picker): {start_date}, Filter Start Datetime: {start_datetime}")
            print(f"DEBUG: Selected End Date (from picker): {end_date}, Filter End Datetime: {end_datetime}")
            # --- END DEBUG ---

            if start_date <= end_date:
                cash_data_full = load_csv_data("cash_on_hand_trend.csv", date_col='Date', index_col='Date')
                expenditure_df = load_csv_data("expenditure_breakdown.csv")

                # --- DEBUG PRINTS FOR cash_data_full ---
                if not cash_data_full.empty:
                    print("\nDEBUG: cash_data_full (raw loaded data) head:")
                    print(cash_data_full.head())
                    print(f"DEBUG: cash_data_full index type: {type(cash_data_full.index)}")
                    if not cash_data_full.index.empty:
                         print(f"DEBUG: cash_data_full first index value: {cash_data_full.index[0]}, type: {type(cash_data_full.index[0])}")
                         print(f"DEBUG: cash_data_full last index value: {cash_data_full.index[-1]}, type: {type(cash_data_full.index[-1])}")
                    print(f"DEBUG: cash_data_full columns: {cash_data_full.columns.tolist()}")
                    print(f"DEBUG: cash_data_full shape: {cash_data_full.shape}")
                else:
                    print("DEBUG: cash_data_full is EMPTY after loading (File not found or empty).")
                # --- END DEBUG ---

                cash_data_filtered = pd.DataFrame() # Initialize
                if not cash_data_full.empty:
                     # Ensure the index is indeed datetime before filtering
                     if pd.api.types.is_datetime64_any_dtype(cash_data_full.index):
                        cash_data_filtered = cash_data_full[
                            (cash_data_full.index >= start_datetime) &
                            (cash_data_full.index <= end_datetime)
                        ]
                     else:
                        print("DEBUG: cash_data_full.index is NOT datetime. Filtering might fail or be incorrect.")


                # --- DEBUG PRINTS FOR cash_data_filtered ---
                if not cash_data_filtered.empty:
                    print("\nDEBUG: cash_data_filtered (after date range filter) head:")
                    print(cash_data_filtered.head())
                    print(f"DEBUG: cash_data_filtered shape: {cash_data_filtered.shape}")

                else:
                    print("DEBUG: cash_data_filtered is EMPTY after filtering.")
                    if not cash_data_full.empty and not pd.api.types.is_datetime64_any_dtype(cash_data_full.index):
                        print("      Reason: cash_data_full index was not datetime type.")
                    elif not cash_data_full.empty:
                        print("      Reason: No data within the selected date range or other filtering issue.")

                # --- END DEBUG ---


                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    st.markdown("###### Cash on Hand Trend (Streamlit Chart)")
                    # Check if 'Cash_on_Hand_USD' column exists in the *filtered* data
                    if not cash_data_filtered.empty and 'Cash_on_Hand_USD' in cash_data_filtered.columns:
                        st.line_chart(cash_data_filtered['Cash_on_Hand_USD'], height=250)
                    elif cash_data_full.empty : # If file wasn't loaded at all
                        st.warning("Cash data file ('cash_on_hand_trend.csv') missing or empty.")
                    else: # File loaded, but filtered data is empty or column missing
                        st.info("No cash on hand data for selected range or 'Cash_on_Hand_USD' column missing.")
                        # More specific debug info in UI (optional, can remove after fixing)
                        if not cash_data_full.empty and 'Cash_on_Hand_USD' not in cash_data_full.columns:
                            st.caption(f"Debug Hint: 'Cash_on_Hand_USD' column NOT FOUND in loaded CSV. Available columns: {cash_data_full.columns.tolist()}")
                        elif not cash_data_full.empty and cash_data_filtered.empty:
                            st.caption("Debug Hint: CSV loaded, but NO DATA matched the selected date range after filtering.")
                        elif not cash_data_filtered.empty and 'Cash_on_Hand_USD' not in cash_data_filtered.columns:
                             st.caption(f"Debug Hint: Filtered data exists, but 'Cash_on_Hand_USD' column NOT FOUND in it. Available columns: {cash_data_filtered.columns.tolist()}")


                with chart_col2:
                    st.markdown("###### Expenditure Breakdown (Plotly Chart)")
                    if not expenditure_df.empty and 'Category' in expenditure_df.columns and 'Amount_USD' in expenditure_df.columns:
                        try:
                            fig_pie = px.pie(expenditure_df,
                                             values='Amount_USD',
                                             names='Category',
                                             hole=0.4,
                                             title="Expenditure")
                            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                            fig_pie.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=280, showlegend=False, title_x=0.5)
                            st.plotly_chart(fig_pie, use_container_width=True)
                        except Exception as e:
                            st.error(f"Error creating pie chart: {e}")
                    elif expenditure_df.empty:
                         st.warning("Expenditure data file ('expenditure_breakdown.csv') missing or empty.")
                    else:
                        st.info("Expenditure data malformed (missing 'Category' or 'Amount_USD' columns).")
            else:
                st.warning("Start date must be before or the same as the end date.")
        else:
            st.info("Select a valid date range (start and end date) to view financial trends.")

    elif school_sub_option == "Facilities":
        st.subheader("🏗️ Facilities (Placeholder)")
        st.write("Facilities information would go here.")

elif selected_main_option == "Teachers":
    st.header("👩‍🏫 Teacher Management (Placeholder)")
    st.write("Teacher related content would go here.")


st.markdown("---")
st.caption("Intermediate Dashboard Test | v0.1.debug")
