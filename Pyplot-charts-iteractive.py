#!/usr/bin/env python
# coding: utf-8

# ### A simple figure with st.pyplot!

# #### Create a basic Matplotlib chart

# In[ ]:


import streamlit as st
import matplotlib.pyplot as plt

# dashboard setup
st.set_page_config(
    page_title="Chart Interactive",
    page_icon = "🤖",
    layout="wide",
)

# create your figure and get the figure object returned
fig = plt.figure()
plt.plot([1,2,3,4,5])

st.pyplot(fig)


# #### Make the chart interactive

# In[ ]:


import mpld3
import streamlit.components.v1 as components

# create your figure and get the figure object return
fig = plt.figure()
plt.plot([1,2,3,4,5])

fig_html = mpld3.fig_to_html(fig)
components.html(fig_html, height=600)


# ### Advanced example

# #### Render the graph statically

# In[ ]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3
import streamlit as st
from mpld3 import plugins

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

# How to set the graph size
two_subplot_fig = plt.figure(figsize=(6,6))
plt.subplot(211)
plt.plot(t1, f(t1), color='tab:blue', marker=',')
plt.plot(t2, f(t2), color='black', marker='.')

plt.subplot(212)
plt.plot(t2, np.cos(2*np.pi*t2), color='tab:orange', linestyle='--', marker='.')

st.pyplot(two_subplot_fig)


# #### Make the graph interactive with mpld3

# In[ ]:


fig_html = mpld3.fig_to_html(two_subplot_fig)
components.html(fig_html, height=600)


# #### Add tooltips for wvwn more interactivity

# In[ ]:


# Define some css to control our custom labels
css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #ffffff;
  background-color: #000000;
}
td
{
  background-color: #cccccc;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
"""

for axes in two_subplot_fig.axes:
    for line in axes.get_lines():
        # get the x and y coords
        xy_data = line.get_xydata()
        labels = []
        for x, y in xy_data:
            # Create a label for each point with the x and y coords
            html_label = f'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> </thead> <tbody> <tr> <th>x</th> <td>{x}</td> </tr> <tr> <th>y</th> <td>{y}</td> </tr> </tbody> </table>'
            labels.append(html_label)
        # Create the tooltip with the labels (x and y coords) and attach it to each line with the css specified
        tooltip = plugins.PointHTMLTooltip(line, labels, css=css)
        # Since this is a separate plugin, you have to connect it
        plugins.connect(two_subplot_fig, tooltip)
        
fig_html = mpld3.fig_to_html(two_subplot_fig)
components.html(fig_html, height=600)


# *Note: mpld3 limitations*
# 1. Complex charts sometimes don't render properly.
# 2. Dark mode isn't supported.
# 3. 3D charts don't render properly.
# 4. You need markers for tooltips.
# 5. Some markers don't work (examples: none or '+').
