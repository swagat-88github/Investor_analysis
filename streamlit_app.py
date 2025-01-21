import streamlit_app as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("startup_cleaned.csv")
st.sidebar.title("Startup Funding Analysis")
options=st.sidebar.selectbox("Select one",["Overall Analysis","Startup","Investor"])