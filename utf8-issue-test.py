#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd

st.table(pd.DataFrame({"A": ["x"], "B": ["y"]}))

