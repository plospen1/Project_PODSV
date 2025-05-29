# plots/dataset2_plots.py

import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, BoxAnnotation, Span, Label
from bokeh.palettes import BuPu, PuBu
from bokeh.models.formatters import DatetimeTickFormatter, NumeralTickFormatter


def plot_deaths_comparison(data_set2_mortality):
    data_set2_mortality["Parameter"] = data_set2_mortality["Parameter"].str.strip().str.lower()
    data_set2_mortality["Parameter"] = data_set2_mortality["Parameter"].replace({
        "deaths total": "deaths total",
        "total deaths": "deaths total",
        "total death": "deaths total"
    })

    month_map = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    data_set2_mortality["Month"] = data_set2_mortality["Month"].str.strip().str.lower().map(month_map)

    influenza_ch = data_set2_mortality[data_set2_mortality["Parameter"] == "deaths influenza"][["Year", "Month", "CH"]]
    total_ch = data_set2_mortality[data_set2_mortality["Parameter"] == "deaths total"][["Year", "Month", "CH"]]

    comparison_df = influenza_ch.copy()
    comparison_df = comparison_df.rename(columns={"CH": "Influenza_Deaths"})
    comparison_df["Total_Deaths"] = total_ch["CH"].values
    comparison_df["Date"] = pd.to_datetime(dict(year=comparison_df["Year"], month=comparison_df["Month"], day=1))
    comparison_df = comparison_df[(comparison_df["Year"] < 1958) | ((comparison_df["Year"] == 1958) & (comparison_df["Month"] <= 8))]

    source = ColumnDataSource(comparison_df)

    p = figure(title="Comparison: Monthly Influenza Deaths vs. Total Deaths in Switzerland (1953–1958)",
               x_axis_type="datetime", width=950, height=550,
               x_axis_label="Date", y_axis_label="Number of Deaths",
               tools="pan,wheel_zoom,box_zoom,reset,hover,save")

    p.varea(x='Date', y1=0, y2='Total_Deaths', source=source, fill_color=PuBu[7][0], fill_alpha=0.5, legend_label="Total Deaths")
    p.varea(x='Date', y1=0, y2='Influenza_Deaths', source=source, fill_color=BuPu[7][2], fill_alpha=0.8, legend_label="Influenza Deaths")

    p.line(x='Date', y='Influenza_Deaths', source=source, line_color=BuPu[7][3], line_alpha=0.0, line_width=5)
    p.line(x='Date', y='Total_Deaths', source=source, line_color=PuBu[7][2], line_alpha=0.0, line_width=5)

    hover = p.select_one(HoverTool)
    hover.tooltips = [
        ("Date", "@Date{%Y-%m}"),
        ("Influenza Deaths", "@Influenza_Deaths{0,0}"),
        ("Total Deaths", "@Total_Deaths{0,0}")
    ]
    hover.formatters = {'@Date': 'datetime'}
    hover.mode = 'vline'

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    return p


def plot_influenza_share(data_set2_mortality):
    # Ensure columns are treated as strings before using .str
    data_set2_mortality["Parameter"] = data_set2_mortality["Parameter"].astype(str).str.strip().str.lower()
    data_set2_mortality["Month"] = data_set2_mortality["Month"].astype(str).str.strip().str.lower()

    month_map = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    data_set2_mortality["Month"] = data_set2_mortality["Month"].map(month_map)

    influenza_ch = data_set2_mortality[data_set2_mortality["Parameter"] == "deaths influenza"][["Year", "Month", "CH"]]
    total_ch = data_set2_mortality[data_set2_mortality["Parameter"] == "deaths total"][["Year", "Month", "CH"]]

    comparison_df = influenza_ch.copy()
    comparison_df = comparison_df.rename(columns={"CH": "Influenza_Deaths"})
    comparison_df["Total_Deaths"] = total_ch["CH"].values
    comparison_df["Date"] = pd.to_datetime(dict(year=comparison_df["Year"], month=comparison_df["Month"], day=1))
    comparison_df["Influenza_Share"] = comparison_df["Influenza_Deaths"] / comparison_df["Total_Deaths"] * 100

    source = ColumnDataSource(comparison_df)

    p = figure(title="Influenza Deaths as Share of Total Deaths (1953–1958)",
               x_axis_type="datetime", width=950, height=500,
               x_axis_label="Date", y_axis_label="Influenza Share (%)",
               tools="pan,wheel_zoom,box_zoom,reset,hover,save")

    p.line(x='Date', y='Influenza_Share', source=source, line_width=3, color=BuPu[7][2], line_alpha=0.6)

    # FIXED: use scatter instead of deprecated circle()
    p.scatter(x='Date', y='Influenza_Share', source=source, size=5, color=BuPu[7][2], marker="circle")

    hover = p.select_one(HoverTool)
    hover.tooltips = [("Date", "@Date{%F}"), ("Share", "@Influenza_Share{0.00}%")]
    hover.formatters = {'@Date': 'datetime'}

    ref_line = Span(location=5, dimension='width', line_color='gray', line_dash='dashed', line_width=2)
    p.add_layout(ref_line)

    label = Label(x=comparison_df["Date"].iloc[5], y=5.3, text="5% Threshold", text_font_size="10pt", text_color="gray")
    p.add_layout(label)

    for year in range(1953, 1958):
        p.add_layout(BoxAnnotation(left=pd.Timestamp(f"{year}-12-01"),
                                   right=pd.Timestamp(f"{year+1}-03-01"),
                                   fill_alpha=0.1, fill_color='lightblue'))

    return p

def plot_weekly_cases(data_set2_incidence_weekly):
    weekly_ch = data_set2_incidence_weekly[data_set2_incidence_weekly["Parameter"] == "Cases Influenza"]
    weekly_ch = weekly_ch[["StartReportingPeriod", "CH"]].rename(columns={"StartReportingPeriod": "Date", "CH": "Weekly_Cases"})
    weekly_ch["Date"] = pd.to_datetime(weekly_ch["Date"])
    weekly_ch["Week_Year"] = weekly_ch["Date"].dt.strftime("%d %b %Y")

    source = ColumnDataSource(weekly_ch)

    p = figure(title="Weekly Influenza Cases in Switzerland (1956–1958)",
               x_axis_type="datetime", width=900, height=400,
               x_axis_label="Year", y_axis_label="Weekly Cases",
               tools="pan,wheel_zoom,box_zoom,reset,hover,save")

    p.line(x='Date', y='Weekly_Cases', source=source, line_width=2.5, color=PuBu[7][0], alpha=0.7)

    hover = p.select_one(HoverTool)
    hover.tooltips = [("Week", "@Week_Year"), ("Cases", "@Weekly_Cases{0,0}")]
    hover.formatters = {'@Date': 'datetime'}

    p.xaxis.formatter = DatetimeTickFormatter(years="%Y", months="%b %Y")
    p.yaxis.formatter = NumeralTickFormatter(format="0,0")

    return p

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.formatters import DatetimeTickFormatter, NumeralTickFormatter
from bokeh.palettes import PuBu, BuPu
import pandas as pd

def plot_monthly_cases_and_deaths(data_set2_incidence_weekly, data_set2_mortality):
    # --- Prepare monthly influenza cases ---
    cases_df = data_set2_incidence_weekly.copy()
    cases_df = cases_df[cases_df["Parameter"] == "Cases Influenza"]
    cases_df["Date"] = pd.to_datetime(cases_df["StartReportingPeriod"])
    cases_df["MonthStart"] = cases_df["Date"].values.astype("datetime64[M]")
    monthly_cases = (
        cases_df.groupby("MonthStart")["CH"]
        .sum()
        .reset_index()
        .rename(columns={"MonthStart": "Date", "CH": "Monthly_Cases"})
    )

    # --- Prepare monthly influenza deaths ---
    deaths_df = data_set2_mortality.copy()
    deaths_df["Parameter"] = deaths_df["Parameter"].str.strip().str.lower()
    deaths_df = deaths_df[deaths_df["Parameter"] == "deaths influenza"]
    deaths_df["Month"] = pd.to_numeric(deaths_df["Month"], errors="coerce")
    deaths_df["Date"] = pd.to_datetime(dict(year=deaths_df["Year"], month=deaths_df["Month"], day=1))
    monthly_deaths = (
        deaths_df.groupby("Date")["CH"]
        .sum()
        .reset_index()
        .rename(columns={"CH": "Monthly_Deaths"})
    )

    # --- Filter to 1957–1958 ---
    monthly_cases = monthly_cases[
        (monthly_cases["Date"].dt.year >= 1957) & (monthly_cases["Date"].dt.year <= 1958)
    ]
    monthly_deaths = monthly_deaths[
        (monthly_deaths["Date"].dt.year >= 1957) & (monthly_deaths["Date"].dt.year <= 1958)
    ]

    # --- Merge for plotting ---
    merged = pd.merge(monthly_cases, monthly_deaths, on="Date", how="outer").fillna(0).sort_values("Date")
    merged["Month_Year"] = merged["Date"].dt.strftime("%B %Y")
    source = ColumnDataSource(merged)

    # --- Bokeh plot ---
    p = figure(title="Monthly Influenza Cases and Deaths in Switzerland (1957–1958)",
               x_axis_type="datetime", width=900, height=450,
               x_axis_label="Year", y_axis_label="Count",
               tools="pan,wheel_zoom,box_zoom,reset,hover,save")

    p.line(x='Date', y='Monthly_Cases', source=source,
           line_width=3, color=PuBu[7][0], alpha=0.7, legend_label="Monthly Cases")

    p.scatter(x='Date', y='Monthly_Deaths', source=source,
              size=8, color=BuPu[7][2], alpha=0.8, legend_label="Monthly Influenza Deaths")

    # --- Hover formatting ---
    hover = p.select_one(HoverTool)
    hover.tooltips = [
        ("Month", "@Month_Year"),
        ("Monthly Cases", "@Monthly_Cases{0,0}"),
        ("Monthly Deaths", "@Monthly_Deaths{0,0}")
    ]
    hover.formatters = {'@Date': 'datetime'}
    hover.mode = 'vline'

    # --- Format axes and legend ---
    p.xaxis.formatter = DatetimeTickFormatter(years="%Y")
    p.yaxis.formatter = NumeralTickFormatter(format="0,0")
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.7
    p.title.text_font_size = '14pt'
    p.title.align = 'center'
    p.xaxis.axis_label_text_font_size = '10pt'
    p.yaxis.axis_label_text_font_size = '10pt'

    return p
