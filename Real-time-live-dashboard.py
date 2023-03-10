#!/usr/bin/env python
# coding: utf-8

# #### A real-time live dashboard is a web app used to display Key Performance Indicators (KPIs).

# *Requirements*
# - Streamlit: for building the web app/dashboard
# - Time, Numpy: to simulate a live data feed.
# - Pandas: to read the input data source. In this case csv file.

# *User Interface*
# 
# A typical dashboard contains the following basic UI design components:
# - A page title.
# - A top-level filter.
# - KPIs/summary cards.
# - Interactive charts.
# - A data table

# In[1]:


import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# In[ ]:


# dashboard setup
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon = "🤖",
    layout="wide",
)


# In[2]:


dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

# read csv from a URL
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()
df.head()


# In[ ]:


# dashboard title
st.title("Real-Time / Live Data Science Dashboard")


# In[ ]:


# top-level filters
job_filter = st.selectbox("Select the Job", pd.unique(df['job']))


# In[ ]:


# creating a single-element container
placeholder = st.empty()


# In[ ]:


# dataframe filter
df = df[df['job']== job_filter]


# In[ ]:


# near real-time / live feed simulation
for seconds in range(200):
    df["age_new"] = df["age"] * np.random.choice(range(1, 5))
    df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))

    # creating KPIs
    avg_age = np.mean(df["age_new"])

    count_married = int(
        df[(df["marital"] == "married")]["marital"].count()
        + np.random.choice(range(1, 30))
    )
    
    balance = np.mean(df["balance_new"])
    
    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label = "Age ⌛",
            value = round(avg_age),
            delta = round(avg_age)-10,
        )

        kpi2.metric(
            label = "Maried Count 💍",
            value = int(count_married),
            delta = -10 + count_married,
        )

        kpi3.metric(
            label = "A/C Balance $",
            value = f"$ {round(balance,2)} ",
            delta = round(balance / count_married) * 100,
        )
        
        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(
                data_frame=df, y="age_new", x="marital"
            )
            st.write(fig)

        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(
                data_frame=df, x="age_new"
            )
            st.write(fig2)
            
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)

