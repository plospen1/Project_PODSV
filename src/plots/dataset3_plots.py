import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select, CustomJS,  HoverTool, RadioButtonGroup, CustomJS
from bokeh.layouts import column, row
from bokeh.transform import dodge
from bokeh.palettes import PuBu, BuPu
from bokeh.plotting import figure, show


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

    p = figure(y_range=comparison_df['Cause'], height=400, width=800,
               title=f"Causes of Death: {year_a} vs {year_b}",
               x_axis_label="Number of Deaths", toolbar_location=None)

    p.hbar(y=dodge('Cause', -0.2, range=p.y_range), right='Year A', height=0.35,
           source=source, color=PuBu[6][1], alpha=0.8, legend_label=str(year_a))

    p.hbar(y=dodge('Cause',  0.2, range=p.y_range), right='Year B', height=0.35,
           source=source, color=BuPu[7][2], alpha=0.8, legend_label=str(year_b))
    p.legend.location = "bottom_right"
    p.legend.click_policy = "hide"

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



def infectious_disease_lineplot(dataframe):
    df = dataframe.copy()
    df = df.loc[:, ~df.columns.duplicated()]

    infectious_cols = [
        col for col in df.columns
        if col.startswith("Infektions-") and
        any(kw in col.lower() for kw in ["pocken", "masern", "schar", "typhus", "diph", "keuch"]) and
        not col.strip().endswith("Total")
    ]

    df['Year'] = pd.to_numeric(df['Jahr'], errors='coerce')
    df_subset = df[['Year'] + infectious_cols].dropna()

    for col in infectious_cols:
        df_subset[col] = pd.to_numeric(df_subset[col], errors='coerce')

    df_subset[infectious_cols] = df_subset[infectious_cols].clip(lower=0)
    df_subset['Total_Infectious'] = df_subset[infectious_cols].sum(axis=1)

    source = ColumnDataSource(df_subset)

    colors = [PuBu[7][0], BuPu[6][0], PuBu[7][3], PuBu[9][0], BuPu[5][2], BuPu[3][0], BuPu[7][2]]
    label_map = {
        "Schar-": "Scarlet fever",
        "Pocken": "Smallpox",
        "Masern": "Measles",
        "Typhus,": "Typhus",
        "Diph-": "Diphtheria",
        "Keuch-": "Whooping cough"
    }

    def create_plot(y_axis_type="linear"):
        p = figure(
            title="Infectious Disease Subgroups in Switzerland (1876–2002)",
            x_axis_label="Year", y_axis_label="Deaths",
            y_axis_type=y_axis_type,
            width=900, height=500, tools=""
        )

        for i, col in enumerate(infectious_cols):
            label = col.split('|')[-1].strip()
            for short, full in label_map.items():
                label = label.replace(short, full)

            p.line(x='Year', y=col, source=source,
                   line_width=2, color=colors[i % len(colors)],
                   legend_label=label)

        total_line = p.line(x='Year', y='Total_Infectious', source=source,
                            line_width=3, color='grey',
                            legend_label='Total')

        tooltip_items = [("Year", "@Year")]
        for col in infectious_cols:
            label = col.split('|')[-1].strip()
            for short, full in label_map.items():
                label = label.replace(short, full)
            tooltip_items.append((label, f"@{{{col}}}"))

        hover = HoverTool(tooltips=tooltip_items, mode='vline', renderers=[total_line])
        p.add_tools(hover)

        p.legend.location = "top_right"
        p.legend.click_policy = "hide"

        return p

    plot_linear = create_plot("linear")
    plot_log = create_plot("log")
    plot_log.visible = False

    toggle = RadioButtonGroup(labels=["Linear", "Logarithmic"], active=0)
    callback = CustomJS(args=dict(p1=plot_linear, p2=plot_log), code="""
        if (this.active === 0) {
            p1.visible = true;
            p2.visible = false;
        } else {
            p1.visible = false;
            p2.visible = true;
        }
    """)
    toggle.js_on_change("active", callback)

    return column(toggle, plot_linear, plot_log)
