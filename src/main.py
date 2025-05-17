import streamlit as st
import pandas as pd
from bokeh.plotting import show
from bokeh.models import ColumnDataSource
from plots.dataset1_plots import plot_excess_mortality
from plots.dataset1_plots import plot_mortality_vs_population
from plots.dataset1_plots import plot_covid_death
from plots.dataset1_plots import pandemic_death_rate_barplot
from plots.dataset3_plots import create_bokeh_comparison_plot
from plots.utils import preprocess_data_set3

from streamlit_bokeh import streamlit_bokeh
import time



st.set_page_config(
    page_title="Pandemic in Switzerland",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': "# This is a project from ADLS23 students"
    }
)
with st.spinner("Wait for it...", show_time=True):
    time.sleep(1)
st.success("Done!")
st.button("Rerun")

st.title("Lessons from the Past: Visualizing Switzerland’s Pandemic History to Prepare for the Future")
st.divider()
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
data_set3_cleaned = pd.read_csv("Data/data_set3_cleaned.csv")
data_covid = pd.read_csv("Data/full_data.csv")

# Tabs erstellen
tab1, tab2, tab3 = st.tabs(["History of the pandemic", "Influenca in Switzerland", "Causes of Death"])


with tab1:
  
    st.header("1 Historical Overview")
    st.subheader("1.1 Pandemic Death Rates")
    st.markdown("""
    In 2020, the COVID-19 pandemic disrupted life across the globe. In Switzerland, as in many countries, society paused, reeled, and eventually adapted. 
    As the emergency fades, a question lingers:
    **Have we really learned from this crisis or are we doomed to forget, again?**
    This project invites you on a journey. A journey through 130 years of Swiss pandemic history, told through data: deaths, diseases, 
    and resilience. We visualize key insights from historical records to better understand how pandemics shaped our past—and how they can guide our future.
    #### How Deadly Were Past Pandemics?
    When people think of pandemics, COVID-19 is top of mind. But how does it compare to earlier pandemics?
    To answer this, we looked at death rates from major pandemics in Switzerland from 1889 to 2020, measured per 100,000 people. 
    The bar chart below reveals the toll of each crisis:

    """)
    fig1_1 = pandemic_death_rate_barplot(data_set1)

    with st.container():
        st.pyplot(fig1_1, use_container_width=False) 
    
    st.markdown("""
   #### Key Findings:

    - The 1918 Spanish Flu had by far the highest death rate in Swiss history—more than five times higher than COVID-19.
    - Pandemics in 1957 (Asian Flu) and 1968 (Hong Kong Flu) caused significant but lesser mortality.
    - The 2009 Swine Flu was comparatively mild in Switzerland.

    COVID-19 was not the deadliest pandemic in Swiss history. In fact, the Spanish Flu of 1918 remains unmatched in scale. 
    But history shows: even ‘moderate’ pandemics can leave lasting scars.            
    """)

    st.divider()

    st.subheader("1.2 Population and Pandemic Deaths Over Time")
    st.markdown("""
    #### Time, Population, and Mortality: The Bigger Picture
    Pandemic impact doesn’t occur in isolation, it happens in the context of a growing society. To understand the broader picture, we plotted pandemic death rates alongside population growth over more than a century.
    
    **Tip:** Hover over the lines in the chart to explore each year. You’ll see how many people lived in Switzerland, and how many died from influenza or COVID-19 during that time.    
    """)
    
    fig1_2 = plot_mortality_vs_population(data_set1)
    with st.container():
        streamlit_bokeh(fig1_2, use_container_width=True, key="plot2")

    st.markdown("""
        “*A growing population does not automatically mean higher mortality if health systems adapt. Still, sharp spikes in 1918 and 2020 show that even modern nations remain vulnerable when overwhelmed.*”

    #### Key Findings:
    - Switzerland's population grew from under 3 million in 1880 to over 8 million by 2022.
    - Despite this growth, pandemic death rates spiked dramatically only in select years—especially in 1918 and 2020.
    - Medical and public health advances appear to have helped reduce death rates in later pandemics.
    """)

    st.markdown("""
    ##### **Of particular interest to most: COVID-19.** 

    We can probably draw the most important insights from COVID-19. 
    That is why it is also presented here individually and in more detail. The chart shows how many deaths from COVID-19 there have been in Switzerland each year.
    
    """)

    fig1_3 = plot_covid_death(data_set1)

    with st.container():
        st.pyplot(fig1_3, use_container_width=False) 
    
    
    st.divider()

    st.subheader("1.3 Excess Mortality Over Time")
    st.markdown("""
    #### Excess Mortality Over Time 
    To understand the true cost of pandemics, we looked beyond reported causes of death. Sometimes, people die because of a pandemic, but not from the disease itself—indirect effects like delayed treatments, overwhelmed hospitals, or social disruptions can all lead to excess deaths.
    
    This is where excess mortality becomes essential. It measures how many people died above or below what we would statistically expect in a normal year, based on historical trends.
                
    **How to read the graph:**

    - Each dot represents a year between 1880 and 2022.
    - Red dots mean more people died than expected → positive excess mortality. This often occurs during severe flu seasons, pandemics, heatwaves, or crises.
    - Green dots mean fewer people died than expected → negative excess mortality. This can reflect milder flu seasons, improved healthcare, or social measures like lockdowns reducing accidents.
    - The gray line shows the trend over time.
    - Vertical lines mark known pandemic years like 1918, 1957, and 2020.
    - The horizontal dashed line at 0% represents the baseline: deaths were as expected that year.            
    """)

    fig1_4 = plot_excess_mortality(data_set1)
    with st.container():
        streamlit_bokeh(fig1_4, use_container_width=True, key="plot4")

with tab2:
    st.header("Dataset 2: Influenza Dynamics")
    
    st.subheader("1. Population of Cantons and Switzerland")
    st.dataframe(data_set2_population)

with tab3:
    st.header("Dataset 3: Causes of Death Over Time")
    
    st.subheader("1. Deaths by Cause Over the Years")


    fig3_2 = create_bokeh_comparison_plot(data_set3_cleaned)
    with st.container():
        streamlit_bokeh(fig3_2, use_container_width=True, key="plot3_2")

