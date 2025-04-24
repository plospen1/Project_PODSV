import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pandemic in Switzerland", layout="wide")

st.title("Lessons from the Past: Visualizing Switzerland’s Pandemic History to Prepare for the Future")

st.markdown("""
### Project Overview

Welcome to our data story on **the history of pandemics in Switzerland**.  
This project dives deep into how past pandemics unfolded across the country,  
and what we can learn from them today.

We explore:
- The spread and intensity of influenza and other pandemics
- Mortality, morbidity, and excess death trends
- Geographic distribution and regional impacts across Swiss cantons
- Causes of death and shifts in epidemiology over time

Our **key message**:  
> _By visualizing historical data on cases, mortality, and geographic spread, we can gain valuable insights into how pandemics evolved and how society responded. Learning from the past is key to protecting the future._

---

### Target Audience

This data story is designed for:
- **The general public**, curious about health and history



### Data & Visualizations

This dashboard is based on static historical data from the Swiss National Science Foundation project  
**"Bridging the Gap"**, hosted on **[leaddata.ch](https://www.leaddata.ch)**.

We use three core datasets:
- Dataset 1: Pandemic history (COVID, Influenza, excess mortality)
- Dataset 2: Canton-level details from the 1950s (cases, deaths, population)
- Dataset 3: Causes of death in Switzerland from 1876–2002


---
""")





# Daten einlesen
data_set1 = pd.read_excel("Data/1_History_Pandemics.xlsx")
data_set2_mortality = pd.read_excel("Data/2_All_cantons_1953-1958_Mortality.xlsx")
data_set2_incidence_weekly = pd.read_excel("Data/2_Data_cantons_incidence_weekly_56_58_NEW.xlsx")
data_set2_population = pd.read_excel("Data/2_Population_cantons.xlsx")
data_set3 = pd.read_excel("Data/3_Todesursachen Schweiz ohne Alter 1876-2002.xlsx")

# Tabs erstellen
tab1, tab2, tab3 = st.tabs(["History of the pandemic", "Influenca in Switzerland", "Infectious disease"])


with tab1:
    st.header("Dataset 1: Historical Overview")

    st.subheader("1. Influenza/COVID Deaths vs. Population")


with tab2:
    st.header("Dataset 2: Influenza Dynamics")
    
    st.subheader("1. Population of Cantons and Switzerland")
    st.dataframe(data_set2_population)

with tab3:
    st.header("Dataset 3: Causes of Death Over Time")
    
    st.subheader("1. Deaths by Cause Over the Years")
  