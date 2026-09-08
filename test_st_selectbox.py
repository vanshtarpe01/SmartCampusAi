import streamlit as st
import pandas as pd
import numpy as np

# This reproduces the issue if we have NaN in selectbox
options = ["SC-1", np.nan, "SC-2"]
# st.selectbox("Test", options=options) # If you type, it crashes
