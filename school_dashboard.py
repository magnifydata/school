# dashboard_intermediate_test.py
import streamlit as st
import pandas as pd
import numpy as np
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
    st.sidebar.subheader("School Details") # Moved subheader here for direct association
    school_sub_option = st.sidebar.selectbox(
        "Select Category:",
        ("Financial", "Facilities"), # Simplified sub-menu
        key="school_submenu_selectbox"
    )
    st.sidebar.markdown("---")


    if school_sub_option == "Financial":
        st.subheader("💰 Financial Overview")

        # --- Sample CSV Files (Create these in the same directory as the script) ---
        # 1. cash_on_hand_trend.csv
        # Date,Cash_on_Hand_USD
        # 2023-10-01,245000
        # 2023-10-02,248000
        # 2023-10-15,265000

        # 2. expenditure_breakdown.csv
        # Category,Amount_USD
        # Salaries,125000
        # Utilities,28000
        # Supplies,45000

        today = datetime.date.today()
        default_start_date = today - datetime.timedelta(days=29)

        # Date Range Selector (Simplified layout for now)
        selected_date_range = st.date_input(
            "Select Date Range for Trends:",
            value=(default_start_date, today),
            min_value=datetime.date(2023, 1, 1), # Adjust if your data is older
            max_value=today + datetime.timedelta(days=365),
            key="financial_date_range_selector"
        )

        st.markdown("---")

        if len(selected_date_range) == 2:
            start_date, end_date = selected_date_range
            start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
            end_datetime = datetime.datetime.combine(end_date, datetime.time.max)

            if start_date <= end_date:
                # Load data
                cash_data_full = load_csv_data("cash_on_hand_trend.csv", date_col='Date', index_col='Date')
                expenditure_df = load_csv_data("expenditure_breakdown.csv")

                # Filter trend data
                cash_data_filtered = pd.DataFrame() # Initialize
                if not cash_data_full.empty:
                     cash_data_filtered = cash_data_full[(cash_data_full.index >= start_datetime) & (cash_data_full.index <= end_datetime)]


                chart_col1, chart_col2 = st.columns(2)

                with chart_col1:
                    st.markdown("###### Cash on Hand Trend (Streamlit Chart)")
                    if not cash_data_filtered.empty and 'Cash_on_Hand_USD' in cash_data_filtered.columns:
                        st.line_chart(cash_data_filtered['Cash_on_Hand_USD'], height=250)
                    elif cash_data_full.empty : # If file wasn't loaded at all
                        st.warning("Cash data file ('cash_on_hand_trend.csv') missing or empty.")
                    else: # File loaded, but no data in range or column missing
                        st.info("No cash on hand data for selected range or 'Cash_on_Hand_USD' column missing.")


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
st.caption("Intermediate Dashboard Test | v0.1")
