# basic_test.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Basic Test App")

st.title("Streamlit Basic Test App")

st.write("If you see this, Streamlit is working!")

st.subheader("A simple DataFrame:")
data = {'col1': [1, 2, 3], 'col2': ['A', 'B', 'C']}
df = pd.DataFrame(data)
st.dataframe(df)

st.subheader("A simple chart:")
chart_data = pd.DataFrame(
    np.random.randn(20, 2),
    columns=['a', 'b'])
st.line_chart(chart_data)

st.success("Basic test components loaded successfully!")
