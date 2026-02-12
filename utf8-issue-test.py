#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from datetime import datetime


def build_comparison_table(results, gleif_vars, manager_vars):

    rows = []

    for feature, score in results:

        key = FEATURE_KEY_MAP.get(feature)

        manager_value = manager_vars.get(key) if key else None
        gleif_value = gleif_vars.get(key) if key else None

        # fallback inteligente para Legal Form
        if feature == "Legal Form" and not gleif_value:
            gleif_value = gleif_vars.get("legal_form_other")

        rows.append({
            "Feature": feature,
            "LEI Manager": manager_value,
            "GLEIF Candidate": gleif_value,
            "Score": score
        })

    df = pd.DataFrame(rows)

    df = df.astype(str)

    styled_df = df.style.apply(
        lambda row: [
            "",
            "",
            "",
            score_color(row["Feature"], float(row["Score"]))
        ],
        axis=1
    )

    return styled_df

def score_color(feature, value):
    if value is None:
        return ""

    if feature == "Date (delta)":
        if value <= 7:
            return "background-color: #c6efce"   # verde
        elif value <= 30:
            return "background-color: #ffeb9c"   # amarelo
        else:
            return "background-color: #ffc7ce"   # vermelho
    else:
        if value >= 90:
            return "background-color: #c6efce"
        elif value >= 70:
            return "background-color: #ffeb9c"
        else:
            return "background-color: #ffc7ce"



results = [
    ("RegistrationID", 100),
    ("Legal Name", 92),
    ("Date (delta)", 3),
    ("Address", 85),
    ("Legal Form", 90),
]
gleif_vars = {
    "reg_id": "5493001KJTIIGC8Y1R12",
    "legal_name": "ACME INDUSTRIES LTD",
    "date": datetime(2020, 5, 20),
    "address": "123 Baker Street, London",
    "legal_form": "Limited Company",
    "legal_form_other": None,
}

manager_vars = {
    "reg_id": "5493001KJTIIGC8Y1R12",
    "legal_name": "ACME INDUSTRIES LIMITED",
    "date": datetime(2020, 5, 23),
    "address": "123 Baker St., London",
    "legal_form": "Ltd",
}
FEATURE_KEY_MAP = {
    "RegistrationID": "reg_id",
    "Legal Name": "legal_name",
    "Date (delta)": "date",
    "Address": "address",
    "Legal Form": "legal_form",
}

df = build_comparison_table(
    results,
    gleif_vars,
    manager_vars
)
if st.button("press for graph"):
    st.dataframe(df, use_container_width=True)

