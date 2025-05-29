import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select, CustomJS,  HoverTool, RadioButtonGroup, CustomJS
from bokeh.layouts import column, row
from bokeh.transform import dodge
from bokeh.palettes import PuBu, BuPu
from bokeh.plotting import figure, show
import streamlit as st
import streamlit as st
import streamlit.components.v1 as components
from bokeh.embed import file_html
from bokeh.resources import CDN

def plot_major_causes_over_time(df):
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]
    df['Year'] = pd.to_numeric(df['Jahr'], errors='coerce')

    # Wähle Spalten
    cols = [
        "Infektions- und parasitäre Krankheiten | Pocken, Scharlach, Masern, Typhus, Diphtherie, Keuchhusten | Total",
        "Atmungsorgane | Total | Aids",
        "Neubildungen | Total | chitis"
    ]

    col_map = {
        cols[0]: "Infectious Diseases",
        cols[1]: "Respiratory Diseases",
        cols[2]: "Neoplasms"
    }

    df_subset = df[["Year"] + cols].dropna()
    for col in cols:
        df_subset[col] = pd.to_numeric(df_subset[col], errors='coerce')
    df_subset[cols] = df_subset[cols].clip(lower=0)

    source = ColumnDataSource(df_subset)

    colors = (PuBu[6][1], PuBu[7][0], BuPu[7][2])
    renderers = {}

    p = figure(title="Major Causes of Death in Switzerland",
               x_axis_label="Year", y_axis_label="Deaths",
               width=950, height=550, tools="")

    for i, col in enumerate(cols):
        readable = col_map[col]
        line = p.line(x='Year', y=col, source=source,
                      line_width=3 if readable == "Respiratory Diseases" else 2,
                      color=colors[i],
                      alpha=0.7,
                      legend_label=readable)
        renderers[readable] = line

    hover = HoverTool(
        tooltips=[
            ("Year", "@Year"),
            ("Respiratory Deaths", f"@{{{cols[1]}}}{{0,0}}"),
            ("Infectious Deaths", f"@{{{cols[0]}}}{{0,0}}"),
            ("Neoplasms Deaths", f"@{{{cols[2]}}}{{0,0}}")
        ],
        renderers=[renderers["Respiratory Diseases"]],
        mode='vline'
    )

    p.add_tools(hover)
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.7
    p.title.text_font_size = '14pt'
    p.title.align = 'center'
    p.xaxis.axis_label_text_font_size = '10pt'
    p.yaxis.axis_label_text_font_size = '10pt'

    return p




def plot_year_comparison_barplot(df):
    df = df.copy()
    df = df.loc[:, ~df.columns.duplicated()]
    df['Year'] = pd.to_numeric(df['Jahr'], errors='coerce')

    cols = [
        "Infektions- und parasitäre Krankheiten | Pocken, Scharlach, Masern, Typhus, Diphtherie, Keuchhusten | Total",
        "Atmungsorgane | Total | Aids",
        "Neubildungen | Total | chitis"
    ]

    col_map = {
        cols[0]: "Infectious Diseases",
        cols[1]: "Respiratory Diseases",
        cols[2]: "Neoplasms"
    }

    df = df.dropna(subset=["Year"] + cols)
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df[cols] = df[cols].clip(lower=0)

    years = sorted(df["Year"].dropna().unique().astype(int))

    year_a = years[0]
    year_b = years[-1]

    def get_comparison(year1, year2):
        row1 = df[df['Year'] == year1][cols].iloc[0]
        row2 = df[df['Year'] == year2][cols].iloc[0]
        return pd.DataFrame({
            'Cause': [col_map[c] for c in cols],
            'Year A': row1.values,
            'Year B': row2.values
        })

    comparison_df = get_comparison(year_a, year_b)
    source = ColumnDataSource(comparison_df)

    p = figure(y_range=comparison_df['Cause'], height=550, width=950,
               title=f"Causes of Death: {year_a} vs {year_b}",
               x_axis_label="Number of Deaths", toolbar_location=None)

    p.hbar(y=dodge('Cause', -0.2, range=p.y_range), right='Year A', height=0.35,
           source=source, color=PuBu[6][1], alpha=0.8, legend_label= 'Year A')

    p.hbar(y=dodge('Cause',  0.2, range=p.y_range), right='Year B', height=0.35,
           source=source, color=BuPu[7][2], alpha=0.8, legend_label='Year B')
    p.legend.location = "bottom_right"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.7
    p.title.text_font_size = '14pt'
    p.title.align = 'center'
    p.xaxis.axis_label_text_font_size = '10pt'
    p.yaxis.axis_label_text_font_size = '10pt'

    select_a = Select(title="Select Year A", value=str(year_a), options=[str(y) for y in years])
    select_b = Select(title="Select Year B", value=str(year_b), options=[str(y) for y in years])

    js_code = """
        const ya = parseInt(select_a.value);
        const yb = parseInt(select_b.value);

        const causes = ["Infectious Diseases", "Respiratory Diseases", "Neoplasms"];
        const cols = [
            "Infektions- und parasitäre Krankheiten | Pocken, Scharlach, Masern, Typhus, Diphtherie, Keuchhusten | Total",
            "Atmungsorgane | Total | Aids",
            "Neubildungen | Total | chitis"
        ];

        const new_data = {Cause: causes, "Year A": [], "Year B": []};

        for (let i = 0; i < cols.length; i++) {
            let col = cols[i];
            let index_a = df["Year"].indexOf(ya);
            let index_b = df["Year"].indexOf(yb);
            new_data["Year A"].push(df[col][index_a]);
            new_data["Year B"].push(df[col][index_b]);
        }

        source.data = new_data;
        p.title.text = `Causes of Death: ${ya} vs ${yb}`;
        p.legend.items[0].label = {value: String(ya)};
        p.legend.items[1].label = {value: String(yb)};
        source.change.emit();
    """

    callback = CustomJS(args=dict(source=source, df=df.to_dict(orient='list'),
                                  select_a=select_a, select_b=select_b, p=p),
                        code=js_code)

    select_a.js_on_change("value", callback)
    select_b.js_on_change("value", callback)

    return column(row(select_a, select_b), p)


def plot_infectious_diseases(infectdata: pd.DataFrame):
    infectious_cols = [
        "Smallpox", "Scarlet_Fever", "Measles",
        "Typhoid_Paratyphoid", "Diphtheria", "Whooping_Cough"
    ]

    label_map = {
        "Smallpox": "Smallpox",
        "Scarlet_Fever": "Scarlet Fever",
        "Measles": "Measles",
        "Typhoid_Paratyphoid": "Typhoid & Paratyphoid",
        "Diphtheria": "Diphtheria",
        "Whooping_Cough": "Whooping Cough"
    }

    df = infectdata.copy()
    df = df.loc[:, ~df.columns.duplicated()]
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df_subset = df[['Year'] + infectious_cols].dropna()

    for col in infectious_cols:
        df_subset[col] = pd.to_numeric(df_subset[col], errors='coerce')
    df_subset[infectious_cols] = df_subset[infectious_cols].clip(lower=0)
    df_subset['Total_Infectious'] = df_subset[infectious_cols].sum(axis=1)

    source = ColumnDataSource(df_subset)
    colors = [PuBu[7][0], BuPu[6][0], PuBu[7][3], PuBu[9][0], BuPu[5][2], BuPu[3][0]]

    scale = st.radio("Y-Axis Scale", ["Linear", "Logarithmic"], index=0)
    y_axis_type = "linear" if scale == "Linear" else "log"

    p = figure(
        title="Infectious Disease Subgroups in Switzerland (1876–2002)",
        x_axis_label="Year",
        y_axis_label="Deaths",
        y_axis_type=y_axis_type,
        width=950,
        height=550,
        tools=""
    )

    for i, col in enumerate(infectious_cols):
        label = label_map.get(col, col)
        p.line(x="Year", y=col, source=source, line_width=2,
               color=colors[i % len(colors)], legend_label=label)

    p.line(x="Year", y="Total_Infectious", source=source,
           line_width=3, color="gray", legend_label="Total")

    hover = HoverTool(
        tooltips=[("Year", "@Year")] + [(label_map.get(col, col), f"@{{{col}}}") for col in infectious_cols],
        mode="vline"
    )
   
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    p.legend.background_fill_alpha = 0.7
    p.title.text_font_size = '14pt'
    p.title.align = 'center'
    p.xaxis.axis_label_text_font_size = '10pt'
    p.yaxis.axis_label_text_font_size = '10pt'

    return p
    
