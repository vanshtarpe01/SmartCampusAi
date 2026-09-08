import streamlit as st
import pandas as pd

st.dataframe(pd.DataFrame({'A': [1]}), use_container_width=True)
st.button("Test", use_container_width=True)
