"""
    Coronavirus Analysis
    @author: Fatjon Tushe
    July 2020
    Project For Personal Portfolio
"""
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.subplots as subpyo
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()


def matplotLibAnalysis(customDf, customPlace):
    customDf.plot(x="date", y=["total_cases", "total_deaths"], subplots=False)
    plt.title("Coronavirus Development in " + customPlace)
    customDf.hist(column=["new_cases", "new_deaths"])
    plt.suptitle("Probability of Event Distribution")
    plt.figure(3)
    sns.barplot(data=customDf, x="date", y="new_cases", color="blue")
    plt.tick_params(rotation=90)
    plt.ylabel("New Cases")
    plt.title("New Cases Development")
    plt.figure(4)
    sns.distplot(customDf["Daily_New_Cases_Change"])


def dashboardInit(df, customISO):
    temp = df.loc[df[customISO, "total_cases"] > 0]
    scatterplot = html.Div([
        dcc.Graph(id="Scatter Plot", figure=dict(
            data=[go.Scatter(x=temp.index, y=temp[customISO, "total_cases"],
                             mode="lines+markers", name="Total Cases"),
                  go.Scatter(x=temp.index, y=temp[customISO, "total_deaths"],
                             mode="lines+markers", name="Total Deaths")],
            layout=go.Layout(title="Coronavirus Development in " + customISO,
                             xaxis=dict(title="Date"), template="plotly_dark", height=1000)))
    ])

    newCasesHistogram = html.Div([
        html.Div(dcc.Graph(id="new_cases_hist", figure=dict(
            data=[go.Histogram(x=temp[customISO, "new_cases"],
                               name="New Cases", text="New Cases", opacity=0.5, histnorm="probability density")],
            layout=go.Layout(title="New Cases Probability Distribution", width=943, height=800, template="plotly_dark")
        )), style={'display': 'inline-block'}),
        html.Div(dcc.Graph(id="new_deaths_hist", figure=dict(
            data=[go.Histogram(x=temp[customISO, "new_deaths"],
                               name="New Deaths", text="New Deaths",
                               histnorm="probability density", opacity=0.5, marker=dict(color='red'))],
            layout=go.Layout(title="New Deaths Probability Distribution", width=943, height=800, template="plotly_dark")
        )), style={'display': 'inline-block'})
    ], style={'width': '100%', 'display': 'inline-block'})

    boxPlotDataDist = html.Div([
        dcc.Graph(id="Box Plot", figure=dict(
            data=[go.Box(y=temp[customISO, "new_cases"], name="New Cases"),
                  go.Box(y=temp[customISO, "new_deaths"], name="New Deaths")],
            layout=go.Layout(title="Box Plot Data Distribution", template="plotly_dark", height=1000)
        ))
    ])

    barplot = html.Div([
        dcc.Graph(id="Bar Plot", figure=dict(
            data=[go.Bar(x=temp.index, y=temp[customISO, "new_deaths"], name="New Deaths",
                         text="New Deaths", marker=dict(color="red")),
                  go.Bar(x=temp.index, y=temp[customISO, "new_cases"], name="New Cases",
                         text="New Cases", marker=dict(color="blue"))],
            layout=go.Layout(title="New Cases Development in " + customISO, barmode='stack', template="plotly_dark",
                             height=1000)
        ))
    ])

    bubbleChart = html.Div([
        dcc.Graph(id="Bubble Chart", figure=dict(
            data=[go.Scatter(x=temp.index, y=temp[customISO, "total_cases"],
                             mode="markers", text="Total Cases\n"
                                                  "Total Cases Per Million(Size)\n"
                                                  "Total Deaths per Million(Color)",
                             marker=dict(size=temp[customISO, "total_cases_per_million"]/100,
                                         color=temp[customISO, "total_deaths_per_million"],
                                         showscale=True))],
            layout=go.Layout(title="Total Cases in " + customISO + " and Total Cases Per Million",
                             template="plotly_dark", height=1000)
        ))
    ])
    MapData = df.loc["2020-06-20", df.columns.get_level_values(1) == "total_cases"]
    indexes = MapData.index.levels[0]
    print(indexes)
    starttime = datetime.now()
    choromap = html.Div([
        dcc.Graph(id="choroplethMap", figure=dict(
            data=[dict(type='choropleth',
                       locations=indexes,
                       z=MapData,
                       colorbar=dict(title="Total Cases of COVID-19"),
                       style=dict(lataxis_showgrid=True, lonaxis_showgrid=True,
                                  resolution=50,
                                  showcoastlines=True, coastlinecolor="RebeccaPurple",
                                  showland=True, landcolor="LightGreen",
                                  showocean=True, oceancolor="LightBlue",
                                  showlakes=True, lakecolor="Blue",
                                  showrivers=True, rivercolor="Blue")
                       )],
            layout=dict(title="Total Cases of COVID-19",
                        geo=dict(showframe=False, projection={"type": "equirectangular"}),
                        width=1900, height=1000)
        ))
    ])
    endtime = datetime.now()
    print("Start {}, End {}".format(starttime, endtime))
    app.layout = html.Div([scatterplot, newCasesHistogram, boxPlotDataDist, barplot, bubbleChart])


def PlotlyAnalysis(customDf, customPlace):
    trace1 = go.Scatter(x=customDf["date"],
                        y=customDf["total_cases"],
                        mode="lines+markers",
                        name="Total Cases")
    trace2 = go.Scatter(x=customDf["date"],
                        y=customDf["total_deaths"],
                        mode="lines+markers",
                        name="Total Deaths")
    data = [trace1, trace2]
    layout = go.Layout(title="Coronavirus Development in " + customPlace,
                       xaxis=dict(title="Date"))
    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename="CoronavirusCases.html")

    fig = subpyo.make_subplots(rows=1, cols=2, column_titles=["New Cases", "New Deaths"], print_grid=True)
    fig.add_trace(go.Histogram(x=customDf["new_cases"],
                               text="New Cases"), row=1, col=1)
    fig.add_trace(go.Histogram(x=customDf["new_deaths"],
                               text="New Deaths"), row=1, col=2)
    pyo.plot(fig, filename="NewCasesHistogram.html")

    data = [go.Box(y=customDf["new_cases"], name="New Cases"), go.Box(y=customDf["new_deaths"], name="New Deaths")]
    layout = go.Layout(title="Box Plot Data Distribution")

    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename="BoxPlot.html")

    data = [go.Bar(x=customDf["date"], y=customDf["new_deaths"], name="New Deaths", text="New Deaths",
                   marker=dict(color="red")), go.Bar(
        x=customDf["date"], y=customDf["new_cases"], name="New Cases", text="New Cases", marker=dict(color="blue"))]
    layout = go.Layout(title="New Cases Development in " + customPlace, barmode='stack')

    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename="BarPlot.html")

    data = [go.Scatter(x=customDf["date"], y=customDf["total_cases"],
                       mode="markers", text="Total Cases\n"
                                            "Total Cases Per Million(Size)\n"
                                            "Total Deaths per Million(Color)",
                       marker=dict(size=customDf["total_cases_per_million"] / 10,
                                   color=customDf["total_deaths_per_million"],
                                   showscale=True))]
    layout = go.Layout(title="Total Cases in " + customPlace + " and Total Cases Per Million")

    fig = go.Figure(data=data, layout=layout)
    pyo.plot(fig, filename="BubbleChart.html")

    fig = ff.create_distplot([customDf["Daily_New_Cases_Change"].dropna().values.tolist()],
                             ["New Cases Daily Change in Percentage"])
    pyo.plot(fig, filename="DistributionPlot.html")


def main():
    customISO = "USA"
    try:
        df = pd.read_csv("custom_table.csv", header=[0, 1], index_col=0, low_memory=False)
        print(df)
    except FileNotFoundError:
        df = pd.read_csv("owid-covid-data.csv")
        df = df.loc[df["iso_code"] != "OWID_WRL"]
        df = df.loc[df["location"] != "International"]

        dates = []
        iso_codes = df["iso_code"].dropna().unique()
        innercolumns = df.loc[:, 'total_cases':'life_expectancy'].columns
        for date in df["date"].unique():
            dates.append(datetime.strptime(date, "%Y-%m-%d"))

        columns = pd.MultiIndex.from_product([iso_codes, innercolumns])
        print(columns)
        testingDf = pd.DataFrame(index=sorted(dates), columns=columns)
        print(testingDf)

        # Converting the CSV to the Multidim dataframe
        start_time = datetime.now()
        for i in df.index:
            source = df.loc[i]["total_cases":"human_development_index"]
            for column in source.index:
                #print(source[column])
                testingDf.at[datetime.strptime(df.loc[i]["date"], "%Y-%m-%d"), (df.loc[i]["iso_code"], column)] = \
                    source[column]

            print("Progress: {}".format(i * 100 / len(df.index)))
        end_time = datetime.now()
        print("Started at " + start_time.strftime("%Y-%m-%d %H:%M:%S") + ", Ended at " + end_time.strftime("%Y-%m-%d "
                                                                                                           "%H:%M:%S"))
        # print(testingDf)
        testingDf.to_csv("custom_table.csv")
        df = testingDf

    # oldFormatDF = pd.read_csv("owid-covid-data.csv")
    # customDf = oldFormatDF.loc[oldFormatDF["location"] == "Albania"]
    # customDf = customDf.loc[customDf["total_cases"] > 0]
    # customDf["Daily_New_Cases_Change"] = customDf.loc[:, "new_cases"].pct_change().replace([np.inf, -np.inf],
    #                                                                                        np.nan)
    #
    # PlotlyAnalysis(customDf, "Albania")
    # customDf = pd.read_csv("owid-covid-data.csv")
    # customDf = customDf.loc[customDf["date"] == "2020-05-25"]
    # starttime = datetime.now()
    # data = [dict(type='choropleth',
    #              locations=customDf["iso_code"],
    #              z=customDf["total_cases"],
    #              text=customDf["location"],
    #              colorbar=dict(title="Total Cases of COVID-19")
    #              )]
    # layout = dict(title="Total Cases of COVID-19", geo=dict(showframe=True, projection={"type": "mercator"}))
    # fig = go.Figure(data, layout)
    # pyo.plot(fig, filename="GeographicPlot.html")
    # endtime = datetime.now()
    # print("Start {}, End {}".format(starttime, endtime))

    dashboardInit(df, customISO)
    # plt.show()


if __name__ == '__main__':
    main()
    app.run_server()
