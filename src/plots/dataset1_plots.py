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




def pandemic_death_rate_barplot(data_set1):
    pandemic_years = [1889, 1918, 1957, 1968, 2009, 2020]  # Major pandemic years
    pandemic_data = data_set1[data_set1['Jahr'].isin(pandemic_years)].copy()

    # Prepare death rates per 100,000
    pandemic_data['Todesfälle_100000'] = pandemic_data['Todesfälle_Grippe_100000'].fillna(0)
    pandemic_data.loc[pandemic_data['Jahr'] == 2020, 'Todesfälle_100000'] = (
        pandemic_data.loc[pandemic_data['Jahr'] == 2020, 'Todesfälle_Covid_100000'].fillna(0)
    )

    # Create plot with smaller size
    fig, ax = plt.subplots(figsize=(6, 5))  # Smaller figure size
    bar_width = 0.5  
    index = np.arange(len(pandemic_years))
    colors = ['#1f77b4'] * 5 + ['#ff7f0e']

    bars = ax.bar(index, pandemic_data['Todesfälle_100000'], 
                  bar_width, color=colors, alpha=0.8)

    # Labels and title with smaller font sizes
    ax.set_ylabel('Deaths per 100,000 Population', fontsize=6)
    ax.set_title('Comparison of Major Pandemic Death Rates', fontsize=10)

    pandemic_names_with_years = [
        "Russian Flu (1889)", "Spanish Flu (1918)", "Asian Flu (1957)", 
        "Hong Kong Flu (1968)", "Swine Flu (2009)", "COVID-19 (2020)"
    ]
    ax.set_xticks(index)
    ax.set_xticklabels(pandemic_names_with_years, rotation=45, ha='right', fontsize=5)

    # Value annotations with smaller font size
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{height:.1f}', 
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points", 
                        ha='center', va='bottom', fontsize=5)

    # Legend with smaller font size
    legend_elements = [
        Patch(facecolor='#1f77b4', label='Historical Pandemics'),
        Patch(facecolor='#ff7f0e', label='COVID-19')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=5)

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

    # Create a color column based on excess mortality
    df['color'] = df['Überasterblichkeit_Alles'].apply(lambda x: 'red' if x > 0 else 'green')

    # Create the ColumnDataSource
    source = ColumnDataSource(df)

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
    p.line('Jahr', 'Überasterblichkeit_Alles', source=source, line_width=3, color="gray", alpha=0.6)

    # Colored points
    p.scatter(
        'Jahr', 'Überasterblichkeit_Alles', source=source,
        size=8, color='color', line_color='black', line_width=1
    )

    # Horizontal line at 0%
    zero_line = Span(location=0, dimension='width', line_color='black', line_dash='dashed', line_width=2)
    p.add_layout(zero_line)

    # Mark pandemic years if provided
    if pandemic_years is None:
        pandemic_years = [1889, 1918, 1957, 1968, 2009, 2020]  # Default pandemic years

    for year in pandemic_years:
        if year in df['Jahr'].values:
            vline = Span(location=year, dimension='height', line_color='darkgray', line_dash='dotted', line_width=1)
            p.add_layout(vline)

    # Styling
    p.title.text_font_size = '14pt'
    p.title.align = 'center'
    p.y_range = Range1d(-15, 50)

    p.grid.grid_line_alpha = 0.3

    return p

