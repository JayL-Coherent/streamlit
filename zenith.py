import pandas as pd
import numpy as np
import json
import requests
import streamlit as st
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots

def callSparkEngine(claimsRatio, derisking, expenses, lapse, newBusiness, profitImprovement):
    
    url = "https://excel.sit.coherent.global/coherent/api/v3/folders/Jay_Testing/services/ORSA_Sandbox_V4/Execute"
    payload = json.dumps({
      "request_data": {
        "inputs": {
          "ClaimsRatio": claimsRatio,
          "Desrisking": derisking,
          "Expenses": expenses,
          "Lapse": lapse,
          "NewBusiness": newBusiness,
          "ProfitabilityImprovements": profitImprovement,
          "INCOME_STATEMENT": {
            "FileName": ""
          },
          "BALANCE_SHEET": {
            "FileName": ""
          }
        }
      },
      "request_meta": {
        "source_system": "SPARK",
        "correlation_id": "",
        "requested_output": "",
        "service_category": "",
        "compiler_type": "NodeGen"
      }
    })
    headers = {
      'Content-Type': 'application/json',
      'x-tenant-name': 'coherent',
      'SecretKey': 'a929e726-6cd7-41e6-ad23-f0708324aee5'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response

st.title("Zenith ORZA Model")

    
with st.form("My Form"):

    claimsRatio = st.number_input('Claims Ratio: ', 0.0)
    expenses = st.number_input('Expenses: ', 0.0)
    lapse = st.number_input('Lapse: ', 0.0)
    newBusiness = st.number_input('New Business: ', 0.0)
    profitImprovement = st.radio('Profitability Improvements: ', ('Yes', 'No'))
    derisking = st.radio('Derisking: ', ('Yes', 'No'))
    submitted = st.form_submit_button("Submit")
    
   
if submitted:
    
    response = callSparkEngine(claimsRatio, derisking, expenses, lapse, newBusiness, profitImprovement)
    
    balanceSheetTable = pd.DataFrame(json.loads(response.text)['response_data']['outputs']['BalanceSheetTable'])
    balanceSheetTable
    
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=balanceSheetTable['Dates'], y=balanceSheetTable['Solvency Ratio'], name="Solvency Ratio", mode="lines+markers"),
        secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(x=balanceSheetTable['Dates'], y=balanceSheetTable['Solvency Ratio (Base)'], name="Solvency Ratio (Base)", mode="lines+markers"),
        secondary_y=True
    )
    
    fig.add_trace(
        go.Bar(x=balanceSheetTable['Dates'], y=balanceSheetTable['Own Funds'], name="Own Funds"),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Bar(x=balanceSheetTable['Dates'], y=balanceSheetTable['SCR'], name="SCR"),
        secondary_y=False
    )
    
    fig.add_trace(
        go.Bar(x=balanceSheetTable['Dates'], y=balanceSheetTable['Excess Assets'], name="Excess Assets"),
        secondary_y=False
    )

    st.plotly_chart(fig, use_container_width=True)