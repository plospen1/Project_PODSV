import streamlit as st
import pandas as pd
from bokeh.plotting import show
from bokeh.models import ColumnDataSource
from plots.dataset1_plots import plot_excess_mortality
from plots.dataset1_plots import plot_mortality_vs_population
from plots.dataset1_plots import plot_covid_death
from plots.dataset1_plots import pandemic_death_rate_barplot
from plots.dataset3_plots import (
    plot_major_causes_over_time,
    plot_year_comparison_barplot,
    plot_infectious_diseases
)

from plots.dataset2_plots import (
    plot_deaths_comparison,
    plot_influenza_share,
    plot_weekly_cases,
    plot_monthly_cases_and_deaths
)

from streamlit_bokeh import streamlit_bokeh
import time
from utils import load_all_data

data = load_all_data()


data_set1 = data["data_set1"]  
data_set2_mortality = data["data_set2_mortality"]  
data_set2_incidence_weekly = data["data_set2_incidence_weekly"] 
data_set2_population = data["data_set2_population"]  
data_set3 = data["data_set3"] 
data_set3_cleaned = data["data_set3_cleaned"]  
data_covid = data["data_covid"]  
dataset3_infectdata = data["dataset3_infectdata"]  



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



# TABS
tab1, tab2, tab3 = st.tabs(["History of the pandemic", "Influenca in Switzerland", "Causes of Death"])


with tab1:
  
    st.header("1. Historical Overview")
    st.subheader("1.1 Pandemic Death Rates")
    st.markdown("""
    In 2020, the COVID-19 pandemic disrupted life across the globe. In Switzerland, as in many countries, society paused, reeled, and eventually adapted. As the emergency fades, a question lingers:
    > **Have we really learned from this crisis—or are we doomed to forget, again?**
    This project invites you on a journey. A journey through 130 years of Swiss pandemic history, told through data: deaths, diseases, and resilience. We visualize key insights from historical records to better understand how pandemics shaped our past—and how they can guide our future.
    #### How Deadly Were Past Pandemics?
    When people think of pandemics, COVID-19 is top of mind. But how does it compare to earlier pandemics?
    To answer this, we looked at death rates from major pandemics in Switzerland from 1889 to 2020, measured per 100,000 people. The bar chart below reveals the toll of each crisis:


    """)
    fig1_1 = pandemic_death_rate_barplot(data_set1)
    st.image("src/plots/save_figures/pandemic_death_rate_barplot.png", width=950)
    
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
    Pandemic impact doesn’t occur in isolation—it happens in the context of a growing society. To understand the broader picture, we plotted pandemic death rates alongside population growth over more than a century.
    **Tip:** Hover over the lines in the chart to explore each year. You’ll see how many people lived in Switzerland, and how many died from influenza or COVID-19 during that time. The vertical dashed lines mark the timing of major pandemics, we showed you earlier. 
    """)
    
    fig1_2 = plot_mortality_vs_population(data_set1)
    
    streamlit_bokeh(fig1_2, use_container_width=False, key="plot2")

    st.markdown("""
    >“A growing population does not automatically mean higher mortality—if health systems adapt.”

    #### Key Findings:
    - Switzerland's population grew from under 3 million in 1880 to over 8 million by 2022.
    - Despite this growth, pandemic death rates spiked dramatically only in select years—especially in 1918 and 2020.
    - Medical and public health advances appear to have helped reduce death rates in later pandemics.
    """)

    st.markdown("""
    ##### **Of particular interest to most: COVID-19.** 
    It is precisely from this current data that we can probably draw the most important insights. That is why it is also presented here individually and in more detail. The chart shows how many deaths from COVID-19 there have been in Switzerland each year.
    """)

    fig1_3 = plot_covid_death(data_covid)
    st.image("src/plots/save_figures/plot_covid_death.png", width= 950)
    
    
    st.divider()

    st.subheader("1.3 Excess Mortality Over Time")
    st.markdown(""" 
    To understand the true cost of pandemics, we looked beyond reported causes of death. Sometimes, people die because of a pandemic, but not from the disease itself—indirect effects like delayed treatments, overwhelmed hospitals, or social disruptions can all lead to excess deaths.

    This is where excess mortality becomes essential. It measures how many people died above or below what we would statistically expect in a normal year, based on historical trends.

    **How to read the graph:**

    - Each dot represents a year between 1880 and 2022.
    - **Purple dots** mean more people died than expected → positive excess mortality.

        This often occurs during severe flu seasons, pandemics, heatwaves, or crises.

    - **Blue dots** mean fewer people died than expected → negative excess mortality.

        This can reflect milder flu seasons, improved healthcare, or social measures like lockdowns reducing accidents.
        
    - The gray line shows the trend over time.
    - Vertical lines mark known pandemic years like 1918, 1957, and 2020.
    - The horizontal dashed line at 0% represents the baseline: deaths were as expected that year.          
    """)

    fig1_4 = plot_excess_mortality(data_set1)
    streamlit_bokeh(fig1_4, use_container_width=False, key="plot4")



with tab2:
    st.header("2. Influenza Dynamics")
    
    st.subheader("2.1 The Invisible Peaks: How Influenza Deaths Hide Within Total Mortality (1953–1958)")
    st.markdown("""
    When we think about causes of death, influenza often doesn’t come to mind first. Most people associate it with discomfort or seasonal sickness — not with mortality. Yet when we look closely at historical data, a different picture begins to emerge.
    Between 1953 and 1958, monthly death records from Switzerland show that flu outbreaks leave a clear seasonal trace. While the total number of deaths remained relatively stable, flu-related deaths would suddenly spike in winter months — especially in early 1953, early 1956, and the winter of 1957/58.
     These spikes are not random. They line up with documented influenza epidemics, including the well-known Asian Flu (H2N2), which began spreading worldwide in 1957. In Switzerland, this particular wave peaked in December 1957 to January 1958, causing a noticeable but temporary rise in flu deaths.
    However, even at their highest, influenza deaths remained just a small fraction of total mortality. That’s why they’re often overlooked and influenza's impact tends to blend into the bigger picture.
    Still, this matters. Even when it doesn’t dominate the statistics, influenza adds pressure to healthcare systems and contributes to seasonal death surges. These seasonal patterns show us that flu is not always deadly, but in certain years, it can be very serious — especially for older or vulnerable people.        
    """)

    fig2_1_1 = plot_deaths_comparison(data_set2_mortality)
    streamlit_bokeh(fig2_1_1, use_container_width=False, key="plot2_1_1")

    st.markdown("""
    **Key takeaways from the visualization below:**

    - Flu death spikes are clearly visible in winters of 1953, 1956, and 1957/58.
    - The 1957/58 peak matches the timing of the global Asian Flu pandemic (H2N2).
    - Total mortality remains mostly stable, but seasonal fluctuations include hidden flu effects.
    - Context matters: cold winters, aging populations, and coexisting illnesses all influence death patterns.

    *Note:*

    - All charts and data refer to Switzerland between 1953 and 1958.
    - Data from September to December 1958 is incomplete. This analysis includes only the fully documented period from January 1953 to August 1958.
    
    The plot shows how flu deaths (purple) compare to total deaths (blue) over time. You can see that flu rarely dominates, but it spikes sharply in some winters.
    In most months, flu caused less than 1% of all deaths. But during major outbreaks, such as winter 1957/58, flu accounted for over 10% of monthly deaths.
    ➤ This tells us: Even if influenza doesn’t always cause mass mortality, it can play a big role in certain years. That’s why flu prevention, vaccination, and awareness remain important — especially in colder months.
    """)


    st.markdown("""
    #### When Flu Deaths Break Through the Noise
    This next chart shows how big of a share influenza had in the total number of deaths each month in Switzerland between 1953 and 1958.
    """)

    fig2_1_2 = plot_influenza_share(data_set2_mortality)
    streamlit_bokeh(fig2_1_2, use_container_width=False, key="plot2_1_2")

    st.markdown("""
    - The line represents the flu death percentage each month — how much of all deaths that month were caused by influenza. 
    - The dashed line marks a 5% threshold — above that, flu becomes a noticeable contributor to overall mortality.
    - Each dot is a data point, and the dark purple one marks the first case of the Asian Flu in Switzerland (September 9, 1957).

    In most months, flu deaths were well below 1–2% of all deaths — almost invisible in the bigger picture. But in four major winter waves — 1953, 1955, 1956, and 1957/58 — flu deaths spiked above 5%, reaching over 10% during peak months. The 1957/58 wave is the most dramatic, peaking shortly after the first known case of the Asian Flu (H2N2) — a pandemic that swept across the globe.

    ➤ This plot makes the invisible visible: flu may not always stand out, but it can still shift mortality trends sharply and suddenly. This view helps us understand influenza not as a constant killer, but as a seasonal and sometimes explosive threat.
    """)

    st.divider()

    st.subheader("2.2 The 1957 Flu Pandemic in Switzerland: A Sharp Spike in Infections, But Mortality Stayed Low")
    
    st.markdown("""
    In the fall of 1957, a new influenza strain — H2N2, also known as the Asian Flu — reached Switzerland. By October, health officials were recording over 30,000 flu cases per week, as shown in the first chart below. This was an unprecedented surge.

    However, something interesting happened: deaths didn’t rise as dramatically as expected. While cases skyrocketed, monthly flu deaths peaked at fewer than 500 — high, but relatively small considering the size of the outbreak.

    Why were there so many infections, but relatively few deaths?

    - Lower severity: H2N2 spread rapidly, but caused fewer severe cases and deaths compared to earlier pandemics.
    - Younger population: Switzerland’s population in the 1950s was younger, meaning fewer high-risk elderly people.
    - Antibiotics: These were more widely available to treat deadly complications like pneumonia.
    - Better preparedness: Hospitals and health systems had improved significantly since earlier pandemics.
    - Vaccination: Some early flu vaccines were already in use, helping to reduce severity, even if they didn’t prevent all infections.

    **Result:** A massive wave of infection, but mortality stayed lower than in earlier pandemics.
    
    """)

    fig2_2_1 = plot_weekly_cases(data_set2_incidence_weekly)
    streamlit_bokeh(fig2_2_1, use_container_width=False, key="plot2_2_1")

    st.markdown("""
    The final months of 1957 show a dramatic spike in reported flu cases — far higher than any previous year in this dataset. It clearly marks the arrival and spread of the Asian Flu.
    """)

    fig2_2_2 = plot_monthly_cases_and_deaths(data_set2_incidence_weekly, data_set2_mortality)
    streamlit_bokeh(fig2_2_2, use_container_width=False, key="plot2_2_2")

    st.markdown("""
    This comparison makes the gap visible: while infections exploded, deaths remained relatively moderate. The purple dots (deaths) stay low, even during the peak of the blue line (cases).
    
    **Why this matters:**
    This example illustrates that not all flu outbreaks are equally deadly. The scale of infection doesn’t always predict the scale of death. But the strain on healthcare systems, the risk to vulnerable people, and the potential for rapid spread all remain serious concerns.

    ➤ Lesson: A pandemic doesn’t have to be "high-fatality" to be high-impact.
    """)


    st.divider()


    st.markdown("""
    #### Sources: Understanding the 1957 Influenza Pandemic
                
    **1. CDC – Pandemic Influenza (Historical Context)**
                
    These official resources from the Centers for Disease Control and Prevention (CDC) provide an overview of past influenza pandemics — including the 1957 H2N2 "Asian Flu" — as well as basic facts about pandemic influenza viruses, their origins, and public health impact.
    While the focus is primarily on the United States, the virological and epidemiological information helps contextualize the virus’s behavior and spread globally — including its arrival and effects in Switzerland.
    
    ➤[CDC Pandemic Overview (1957–1958)](https://archive.cdc.gov/www_cdc_gov/flu/pandemic-resources/1957-1958-pandemic.html) 
    
    ➤[CDC Pandemic Flu Basics](https://www.cdc.gov/pandemic-flu/basics/index.html)
    
    ➤[CDC Pandemic Flu Portal](https://www.cdc.gov/pandemic-flu/index.html)
    
    ➤[Timeline of Avian Influenza (1880–1959)](https://www.cdc.gov/bird-flu/avian-timeline/1880-1959.html) 
    
    **2. WHO – 1957–1958 Influenza Pandemic in the USSR**
                
    This historical report, published by the World Health Organization, documents the 1957 H2N2 “Asian Flu” pandemic in the USSR. While the report focuses on the Soviet Union, it offers important global context and insights into how the virus behaved. 
    
    ➤[WHO: The 1957 Influenza Pandemic in the USSR (Zhdanov, 1959)](https://iris.who.int/bitstream/handle/10665/265339/PMC2537752.pdf?sequence=1)

    **3. Demographics and Age Structure in 1950s Switzerland**
                
    These data from the Swiss Federal Statistical Office (BFS) show that Switzerland had a relatively young population structure in the early 1950s. This likely contributed to lower overall mortality during the 1957 pandemic, as younger populations were less vulnerable to severe outcomes.
    The NCBI report supports this, noting that age distribution plays a key role in pandemic impact, with risk varying across age groups in each major outbreak.
    
    ➤[BFS – Swiss Population Structure, 1950](https://www.bfs.admin.ch/asset/de/27225422)
    
    ➤[NCBI – The Story of Influenza](https://www.ncbi.nlm.nih.gov/books/NBK22148/)

    **4. Better Medical Care & Antibiotics**
                
    Studies show that many deaths during past pandemics — especially in 1918 and partly in 1957 — were caused by bacterial pneumonia, not the virus itself. By the 1950s, antibiotics were available, likely helping to reduce deaths in countries like Switzerland.
    
    ➤ [CDC – Bacterial Pneumonia & Influenza Planning](https://wwwnc.cdc.gov/eid/article/14/8/07-0751_article)
    
    ➤ [NCBI – Bacterial Pneumonia in Pandemic Influenza](https://pmc.ncbi.nlm.nih.gov/articles/PMC2599911/)

    **5. WHO – Vaccination and Influenza Prevention**
                
    The World Health Organization (WHO) outlines the critical role of vaccines in reducing illness and death from influenza and other infectious diseases. 
    
    ➤ [WHO – Vaccines and Immunization](https://www.who.int/europe/health-topics/vaccines-and-immunization#tab=tab_1)
    
    ➤ [WHO – History of Influenza Vaccination](https://www.who.int/news-room/spotlight/history-of-vaccination/history-of-influenza-vaccination) 
   
    """) 

with tab3:
    st.header("3. Causes of Death Over Time")

    st.subheader("3.1. Long-Term Shifts in Causes of Death in Switzerland (1876–2002)")

    st.markdown("""
    As we return from our data journey, we zoom out to see the bigger picture. The history of pandemics is only one thread in a much broader transformation:
    How the causes of death in Switzerland have changed over nearly 150 years.

    **The Decline of Infectious Diseases**
    In the late 19th and early 20th centuries, infectious diseases such as tuberculosis, measles, diphtheria, scarlet fever, and whooping cough were leading causes of death in Switzerland.

    - Several key developments contributed to their decline:

    - Public sanitation and clean water infrastructure drastically reduced the spread of waterborne and respiratory diseases.

    - Widespread vaccination campaigns targeted diseases like smallpox, measles, and diphtheria, dramatically lowering incidence and mortality.

    - The discovery and use of antibiotics, starting in the 1940s, enabled effective treatment of bacterial infections that had once been fatal.

    In the 19th century, tuberculosis alone accounted for a major share of deaths in cities like Bern.

    *Source: PMC article on tuberculosis mortality in Bern*

    """)

    fig3_1 = plot_major_causes_over_time(data_set3_cleaned)
    with st.container():
        streamlit_bokeh(fig3_1, use_container_width=False, key="plot3_1")
    
    st.divider()

    st.subheader("3.2. A Direct Comparison Across Time")

    st.markdown("""
    This visual offers a unique opportunity:
    It lets you freely compare any two years in Swiss mortality history—side by side.

    In the example shown (1876 vs. 2004), the differences are striking:

    - Infectious diseases, once dominant, had almost disappeared by 2004.

    - Meanwhile, cancers and respiratory diseases had become leading causes of death.

        The chart is interactive: simply select two years, and watch how the causes shift.
        It invites you to explore your own questions—whether you're interested in the long-term decline of epidemics, the rise of chronic illnesses, or the effects of public health interventions.

    This comparison isn’t just about numbers.
    It makes visible how our medical history, environment, and behaviors have fundamentally changed what it means to get sick—and what it means to die.

    """)

    fig3_2 = plot_year_comparison_barplot(data_set3_cleaned)
    with st.container():
        streamlit_bokeh(fig3_2, use_container_width=True, key="plot3_2")

    st.divider()
    
    st.subheader("3.3.  Breaking Down Epidemics: The Disappearance of Specific Infectious Diseases")
    
    st.markdown("""
    To go even deeper into the story of public health progress, we analyzed the **subgroups of infectious diseases** individually.
    Instead of treating infectious deaths as a single category, this visualization breaks them down into their historical components:

    * **Smallpox**
    * **Measles**
    * **Scarlet fever**
    * **Diphtheria**
    * **Typhus**
    * **Whooping cough**

    These diseases once claimed thousands of lives every year—especially among children. In the late 1800s and early 1900s, they were among the most feared causes of death in Switzerland.

    But over time, something remarkable happened.

    * One after another, these lines drop toward zero.
    * By the end of the 20th century, most of these diseases had effectively disappeared from the mortality statistics.

    > The thick gray line at the top of the chart shows the total deaths from infectious diseases.
    > The colored lines underneath it represent each subgroup—declining at different speeds.

    This chart does more than show death counts.
    It visualizes the impact of **vaccines**, **antibiotics**, **public health systems**, and **collective behavior**.
    It is, in a sense, a portrait of one of modern medicine’s greatest achievements:

    """)

    fig3_4 = plot_infectious_diseases(dataset3_infectdata)
    with st.container():
        streamlit_bokeh(fig3_4, use_container_width=False, key="plot3_4" )

    st.markdown("""
        #### **Conclusion: Remembering, Understanding, Preparing**
        Our journey through more than 140 years of health data has revealed one clear truth:
        Pandemics have never been rare exceptions—they are a recurring part of history.

        We explored how diseases like influenza spread across cantons, how mortality evolved, and how the causes of death shifted dramatically over time.
        What was once dominated by smallpox, measles, or diphtheria is now shaped by cancer and chronic illness.

        But even the 21st century remains vulnerable. COVID-19 was not a one-time shock—it was a reminder.

        > **The past doesn’t just tell us what has been—it warns us of what may come again.**

        This project is not meant to be a conclusion, but a call to action:

        * Historical data gives us context for current risks.
        * It makes visible what society often forgets.
        * And it empowers researchers, policymakers, and citizens alike to choose awareness over amnesia.

        Because only if we are willing to learn from the past, can we be better prepared for the future—as a society, as a health system, and as individuals.
    """)

    st.divider()

    st.markdown("""

        #### Sources:

        1. **Historical Disease Burden in Switzerland**

        * **Swiss Federal Statistical Office (BFS)**
        Die offiziellen Todesursachenstatistiken zeigen die rückläufige Entwicklung von Krankheiten wie Masern, Keuchhusten, Diphtherie etc. ab dem 20. Jahrhundert.
        [BFS – Causes of Death Statistics](https://www.bfs.admin.ch/bfs/en/home/statistics/health/state-of-health/mortality-causes-death.html)

        2. **The Role of Vaccination**

        * **European Centre for Disease Prevention and Control (ECDC)** – Impfprogramme in Europa haben Krankheiten wie Diphtherie, Keuchhusten und Masern stark reduziert.
        [ECDC – Vaccine-preventable diseases](https://www.ecdc.europa.eu/en/immunisation-vaccine-preventable-diseases)

        * **World Health Organization (WHO)** – Success stories of vaccination in Europe, incl. measles, diphtheria, smallpox.
        [WHO – Immunization in the European Region](https://www.who.int/europe/health-topics/vaccines-and-immunization)

        3. **Disease Elimination in Switzerland**

        * **Smallpox** was officially eradicated globally in 1980, but Switzerland had already stopped routine vaccination in 1972.
        [WHO Smallpox Eradication Timeline](https://www.who.int/news-room/fact-sheets/detail/smallpox)

        * **Diphtheria, Scarlet fever, Whooping cough (pertussis)**: sharp declines after vaccine introduction in mid-20th century.

        > For example, in 1945, whooping cough caused over 1,000 deaths in Switzerland. Today, the number is close to zero (source: BFS).

        4. **Academic Literature**

        * **Staub K, Rühli FJ, Woitek U, Pfister C.**
        *Historical mortality data for Switzerland 1876–2015.*
        This paper provides clean historical cause-of-death data and is frequently cited.
        PMID: 30318199](https://pubmed.ncbi.nlm.nih.gov/30318199/)

        * **Global Burden of Disease Project** (Institute for Health Metrics and Evaluation):
        Offers data visualizations showing long-term disease shifts.
        [GBD Data Explorer](https://vizhub.healthdata.org/gbd-results/)



""")