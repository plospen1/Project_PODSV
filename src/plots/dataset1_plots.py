# plots/plot_pandemic_history.py

import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import Title
from bokeh.palettes import Category10

def create_influenza_covid_plot(pandemic_data):
    source = ColumnDataSource(pandemic_data)

    p = figure(
        height=500, 
        width=900,
        x_axis_label='Year',
        y_axis_label='Deaths per 100,000 Population',
        tools="pan,wheel_zoom,box_zoom,reset,save,hover",
        tooltips=[
            ("Year", "@Jahr"),
            ("Influenza Deaths", "@{Todesfälle_Grippe_100000}{0,0.0}"),
            ("COVID Deaths", "@{Todesfälle_Covid_100000}{0,0.0}"),
            ("Population", "@Population{0,0}")
        ]
    )

    p.line(x='Jahr', y='Todesfälle_Grippe_100000', source=source,
           line_width=3, color=Category10[3][0], alpha=0.8,
           legend_label='Influenza Deaths (per 100,000)')
    p.circle(x='Jahr', y='Todesfälle_Grippe_100000', source=source,
             size=8, color=Category10[3][0], alpha=0.8)

    p.line(x='Jahr', y='Todesfälle_Covid_100000', source=source,
           line_width=3, color=Category10[3][1], alpha=0.8,
           legend_label='COVID-19 Deaths (per 100,000)')
    p.circle(x='Jahr', y='Todesfälle_Covid_100000', source=source,
             size=8, color=Category10[3][1], alpha=0.8)

    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.5
    p.title = Title(text="Comparison of Influenza vs COVID-19 Deaths per 100,000 Population", 
                   text_font_size='16pt', align='center')
    p.grid.grid_line_alpha = 0.3

    hover = p.select(dict(type=HoverTool))
    hover.mode = 'vline'

    return p
