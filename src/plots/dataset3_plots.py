import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column, row
from bokeh.transform import dodge
from bokeh.palettes import PuBu, BuPu



def create_bokeh_comparison_plot(data_set3: pd.DataFrame):
    """
    Creates an interactive Bokeh plot comparing causes of death between two years.
    """
    df = data_set3.copy()
    df = df.loc[:, ~df.columns.duplicated()]
    
    df['Year'] = pd.to_numeric(df['Jahr'], errors='coerce')
    if "Jahr" not in df.columns:
        raise ValueError(f"'Jahr' not found in columns: {df.columns.tolist()}")

    
    # Wähle relevante Krankheitsgruppen-Spalten
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

    years = sorted(df_subset["Year"].dropna().unique().astype(int))
    year_a = years[0]
    year_b = years[-1]

    def get_comparison_data(year1, year2):
        row1 = df_subset[df_subset['Year'] == year1][cols].iloc[0]
        row2 = df_subset[df_subset['Year'] == year2][cols].iloc[0]
        return pd.DataFrame({
            'Cause': [col_map[col] for col in cols],
            'Year A': row1.values,
            'Year B': row2.values
        })

    comparison_df = get_comparison_data(year_a, year_b)
    source = ColumnDataSource(comparison_df)

    # Plot
    p = figure(y_range=comparison_df['Cause'], height=400, width=800,
               title=f"Causes of Death: {year_a} vs {year_b}",
               x_axis_label="Number of Deaths", toolbar_location=None)

    p.hbar(y=dodge('Cause', -0.2, range=p.y_range), right='Year A', height=0.35,
           source=source, color=PuBu[6][1], alpha=0.8, legend_label=str(year_a))

    p.hbar(y=dodge('Cause', 0.2, range=p.y_range), right='Year B', height=0.35,
           source=source, color=BuPu[7][2], alpha=0.8, legend_label=str(year_b))

    p.ygrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"

    # Widgets
    select_a = Select(title="Select Year", value=str(year_a), options=[str(y) for y in years])
    select_b = Select(title="Select Year", value=str(year_b), options=[str(y) for y in years])

    def update(attr, old, new):
        ya = int(select_a.value)
        yb = int(select_b.value)
        updated_df = get_comparison_data(ya, yb)
        source.data = ColumnDataSource.from_df(updated_df)
        p.title.text = f"Causes of Death: {ya} vs {yb}"
        p.legend.items[0].label = str(ya)
        p.legend.items[1].label = str(yb)

    select_a.on_change("value", update)
    select_b.on_change("value", update)

    return column(row(select_a, select_b), p)
