# plots/plot_pandemic_history.py

import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import Title
from bokeh.palettes import Category10
from streamlit_bokeh import streamlit_bokeh
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from bokeh.plotting import figure, output_notebook, show
from bokeh.models import ColumnDataSource, Span
from bokeh.io import push_notebook
from bokeh.models.ranges import Range1d
from bokeh.palettes import PuBu, BuPu
from bokeh.models import (
    ColumnDataSource, HoverTool, Span, Range1d, LinearAxis, Label, LabelSet,
    PanTool, BoxZoomTool, WheelZoomTool, ResetTool, CrosshairTool,
    NumeralTickFormatter, Legend, Title, Select, RadioButtonGroup
)



def pandemic_death_rate_barplot(data_set1):
    pandemic_years = [1889, 1918, 1957, 1968, 2009, 2020]  # Major pandemic years
    pandemic_data = data_set1[data_set1['Jahr'].isin(pandemic_years)].copy()

    # Erstelle eine neue Spalte für die Todesfälle pro Pandemie
    pandemic_data['Todesfälle_100000'] = pandemic_data['Todesfälle_Grippe_100000'].fillna(0)
    # Ersetze COVID-Werte für 2020
    pandemic_data.loc[pandemic_data['Jahr'] == 2020, 'Todesfälle_100000'] = pandemic_data.loc[pandemic_data['Jahr'] == 2020, 'Todesfälle_Covid_100000'].fillna(0)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(12, 7))

    # Set width of bars
    bar_width = 0.6
    index = np.arange(len(pandemic_years))

    # Erstelle eine Farbliste (alle blau außer COVID in orange)
    colors = [PuBu[6][1], PuBu[6][1], PuBu[6][1], PuBu[6][1], PuBu[6][1], BuPu[7][2]]


    # Create the bars (nur ein Balken pro Pandemie)
    bars = ax.bar(index, pandemic_data['Todesfälle_100000'], 
              bar_width, color=colors, alpha=0.8)

    # Add labels, title
    ax.set_ylabel('Deaths per 100,000 Population', fontsize=12)
    ax.set_title('Comparison of Major Pandemic Death Rates', fontsize=20)

    # Add pandemic names with years directly in the x-tick labels
    pandemic_names_with_years = ["Russian Flu (1889)", "Spanish Flu (1918)", "Asian Flu (1957)", 
                                "Hong Kong Flu (1968)", "Swine Flu (2009)", "COVID-19 (2020)"]
    ax.set_xticks(index)
    ax.set_xticklabels(pandemic_names_with_years, rotation=45, ha='right')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
    if height > 0:
        ax.annotate(f'{height:.1f}', 
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3), textcoords="offset points", 
                   ha='center', va='bottom')

    # Füge eine Legende hinzu
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=PuBu[6][1], alpha =0.8, label='Historical Pandemics'),
        Patch(facecolor=BuPu[7][2], alpha = 0.8, label='COVID-19')
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    # Adjust layout
    plt.tight_layout()
    return fig




def plot_mortality_vs_population(data_set1):
    pandemic_years = [1889, 1918, 1957, 1968, 2009, 2020]
    pandemic_names = ["Russian Flu", "Spanish Flu", "Asian Flu", "Hong Kong Flu", "Swine Flu"]

    # Daten vorbereiten
    pandemic_data = data_set1.copy()
    highlight_data = data_set1[data_set1['Jahr'].isin(pandemic_years)].copy()


    source_main = ColumnDataSource(pandemic_data)
    source_highlights = ColumnDataSource(highlight_data)


    p = figure(
        title="Pandemic Mortality vs. Population Growth (1889-2020)",
        height=600,
        width=950,
        x_axis_label="Year",
        y_axis_label="Population",
        tools=""  
    )


    p.yaxis.formatter = NumeralTickFormatter(format="0,0")
    p.y_range = Range1d(0, pandemic_data['Population'].max() * 1.1)


    max_deaths = max(pandemic_data['Todesfälle_Grippe_100000'].max(), 
                pandemic_data['Todesfälle_Covid_100000'].max())
    p.extra_y_ranges = {"deaths": Range1d(0, max_deaths * 1.1)}
    p.add_layout(LinearAxis(y_range_name="deaths", axis_label="Deaths per 100,000 Population"), 'right')


    population_line = p.line(
        x='Jahr', y='Population', source=source_main,
        line_width=3, line_dash='dashed', color='black',
        alpha=0.5, legend_label="Population"
    )


    flu_line = p.line(
        x='Jahr', y='Todesfälle_Grippe_100000', source=source_main,
        y_range_name='deaths', line_width=3, color=PuBu[7][0],
        alpha=0.7, legend_label="Influenza Deaths"
    )


    for year in pandemic_years:
        if year in pandemic_data['Jahr'].values:
            vline = Span(location=year, dimension='height', 
                    line_color='grey', line_dash='dashed', line_width=1)
            p.add_layout(vline)


    flu_circles = p.circle(
        x='Jahr', y='Todesfälle_Grippe_100000', source=source_highlights,
        y_range_name='deaths', size=10, color=PuBu[7][0],
        line_color=PuBu[7][0], line_width=1, alpha = 0.8
    )


    # Tooltip für Crosshair
    hover = HoverTool(
        tooltips=[
            ("Year", "@Jahr"),
            ("Population", "@Population{0,0}"),
            ("Influenza Deaths", "@{Todesfälle_Grippe_100000}{0.0} per 100k")
        ],
        renderers=[population_line],
        mode='vline',  
        line_policy='nearest'
    )

    # Create a properly defined CrosshairTool
    crosshair = CrosshairTool(line_color="gray", line_alpha=0.5)

    # In 

    tools = [
        PanTool(),
        BoxZoomTool(),
        WheelZoomTool(),
        ResetTool(),
        crosshair,
        hover,
    ]
    p.add_tools(*tools)

    # Legende und Styling
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.7

    p.title.text_font_size = '14pt'
    p.title.align = 'center'

    p.grid.grid_line_alpha = 0.3

    return p



## doesn't work
def plot_covid_death(data_covid):
    # Filter for Switzerland
    switzerland_data = data_covid[data_covid['location'] == 'Switzerland'].copy()
    switzerland_data['date'] = pd.to_datetime(switzerland_data['date'])
    switzerland_data['year'] = switzerland_data['date'].dt.year

    # Get end-of-year totals for new_deaths instead of total_cases
    yearly_data = switzerland_data.groupby('year').agg({'new_deaths': 'max'}).reset_index()

    # --- Plot Design-Stil anpassen ---
    fig, ax = plt.subplots(figsize=(12, 7))

    # Linie mit Marker
    ax.plot(yearly_data['year'], yearly_data['new_deaths'],
            marker='o', markersize=10, linewidth=2.5,
            color=BuPu[7][2])  

    # Werte beschriften UNTER den Punkten
    for x, y in zip(yearly_data['year'], yearly_data['new_deaths']):
        # Format the number with comma separators
        ax.text(x, y - (yearly_data['new_deaths'].max() * 0.05),
                f'{int(y):,}', ha='center', va='top', fontsize=11)

    ax.set_title('COVID-19 New Deaths in Switzerland by Year', fontsize=20)
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Daily New Deaths', fontsize=12)

    # Format x-axis to use integers only (no decimal places)
    ax.xaxis.set_major_locator(plt.matplotlib.ticker.MaxNLocator(integer=True))

    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=-yearly_data['new_deaths'].max() * 0.08,
                top=yearly_data['new_deaths'].max() * 1.05)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Layout justieren
    plt.tight_layout()
    return fig


def plot_excess_mortality(data_set1, pandemic_years=None):
    """
    This function creates an interactive Bokeh plot of excess mortality in Switzerland, including marked pandemic years.
    
    Args:
        data_set1 (DataFrame): The input dataframe containing historical data.
        pandemic_years (list): A list of specific years to highlight as pandemic years (optional).
        
    Returns:
        None: Displays the plot.
    """
    # Prepare the data
    df = data_set1.copy()

    # Drop rows where either 'Jahr' or 'Überasterblichkeit_Alles' is missing
    df = df.dropna(subset=['Jahr', 'Überasterblichkeit_Alles'])

    # Data subsets for coloring
    df_pos = df[df['Überasterblichkeit_Alles'] > 0]
    df_neg = df[df['Überasterblichkeit_Alles'] <= 0]

    source_pos = ColumnDataSource(df_pos)
    source_neg = ColumnDataSource(df_neg)


    # Create the figure
    p = figure(
        title="Excess Mortality in Switzerland (1880–2022)",
        height=600,
        width=950,
        x_axis_label="Year",
        y_axis_label="Excess Mortality (%)",
        tools="pan,box_zoom,reset,wheel_zoom,hover",
        tooltips=[
            ("Year", "@Jahr"),
            ("Excess Mortality", "@Überasterblichkeit_Alles{0.0}%")
        ]
    )

    # Line showing the trend
    p.line('Jahr', 'Überasterblichkeit_Alles', source=df, line_width=3, color= PuBu[7][0], alpha= 0.7)

    # Colored points
    p.scatter(
        'Jahr', 'Überasterblichkeit_Alles', source=df,
        size=8, line_color='black', line_width=1
    )

    # Horizontal line at 0%
    zero_line = Span(location=0, dimension='width', line_color='black', line_dash='dashed', line_width=2, line_alpha= 0.7 )
    p.add_layout(zero_line)

    # Mark pandemic years
    pandemic_years = [1889, 1918, 1957, 1968, 2009, 2020]
    for year in pandemic_years:
        if year in df['Jahr'].values:
            vline = Span(location=year, dimension='height', line_color='grey', line_dash='dotted', line_width=1)
            p.add_layout(vline)

    # Styling
    p.title.text_font_size = '14pt'
    p.title.align = 'center'
    p.y_range = Range1d(-15, 50)

    p.grid.grid_line_alpha = 0.3


    p.scatter(
        x='Jahr', y='Überasterblichkeit_Alles', source=source_pos,
        size=8, color=BuPu[7][2], line_color=BuPu[7][2], line_width=1, alpha = 0.8,  legend_label='Excess Mortality > 0'
    )

    p.scatter(
        x='Jahr', y='Überasterblichkeit_Alles', source=source_neg,
        size=8, color=PuBu[6][1], line_color=PuBu[6][1], line_width=1, alpha = 0.8, legend_label='Excess Mortality ≤ 0'
    )

    # Legend styling
    p.legend.location = "top_right"
    p.legend.title = "Legend"
    p.legend.label_text_font_size = '10pt'
    p.legend.title_text_font_style = 'bold'
    p.legend.background_fill_alpha = 0.6

    return p

