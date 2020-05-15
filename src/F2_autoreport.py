# This script generates a report of the simulation automatically, with all the important data.

# Importing necessary packages
import dash
import dash_html_components as html
import time
import pandas as pd
import reverse_geocoder as rg
import dash_table
import base64
import git
import folium
import os

# Imports for generating pdf automatically
import threading
import pdfkit

from src.constants import REPO_PATH, OUTPUT_FOLDER, INPUTS_COPY, CSV_ELEMENTS
from src.constants import (
    PLOTS_BUSSES,
    PATHS_TO_PLOTS,
    PLOTS_DEMANDS,
    PLOTS_RESOURCES,
    PLOTS_NX,
    PLOTS_PERFORMANCE,
    PLOTS_COSTS,
)

OUTPUT_FOLDER = os.path.join(REPO_PATH, OUTPUT_FOLDER)
CSV_FOLDER = os.path.join(REPO_PATH, OUTPUT_FOLDER, INPUTS_COPY, CSV_ELEMENTS)


def print_pdf(app, path_pdf_report=os.path.join(OUTPUT_FOLDER, "out.pdf")):
    """Run the dash app in a thread an print a pdf before exiting"""
    td = threading.Thread(target=app.run_server)
    td.daemon = True
    td.start()
    # TODO change time (seconds) here to be able to visualize the report in the browser
    # time.sleep(5)
    pdfkit.from_url("http://127.0.0.1:8050", path_pdf_report)
    td.join(2)


def make_dash_data_table(df):
    """Function that creates a Dash DataTable from a Pandas dataframe"""
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_cell={
            "padding": "5px",
            "height": "auto",
            "width": "auto",
            "textAlign": "center",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "rgb(248, 248, 248)"}
        ],
        style_header={"fontWeight": "bold", "color": "#8c3604"},
        style_table={"margin": "30px", "fontSize": "40px"},
    )


def create_app(results_json):
    path_output_folder = results_json["simulation_settings"]["path_output_folder"]

    # Foundation JS styling sheets that are to be used to improve the formatting of the web app
    external_scripts = [
        {
            "src": "https://cdnjs.cloudflare.com/ajax/libs/foundation/6.6.3/js/foundation.min.js",
            "integrity": "sha256-pRF3zifJRA9jXGv++b06qwtSqX1byFQOLjqa2PTEb2o=",
            "crossorigin": "anonymous",
        }
    ]

    external_stylesheets = [
        {
            "href": "https://cdnjs.cloudflare.com/ajax/libs/foundation/6.6.3/css/foundation.min.css",
            "rel": "stylesheet",
            "integrity": "sha256-ogmFxjqiTMnZhxCqVmcqTvjfe1Y/ec4WaRj/aQPvn+I",
            "crossorigin": "anonymous",
        }
    ]

    # Initialize the app
    app = dash.Dash(__name__)

    colors = {
        "bg-head": "#9ae6db",
        "text-head": "#000000",
        "text-body": "#000000",
        "inp-box": "#03034f",
        "font-inpbox": "#FFFFFF",
    }
    # Reading the relevant user-inputs from the csv files into Pandas dataframes
    dfprojectData = pd.DataFrame.from_dict(results_json["project_data"])
    dfeconomicData = pd.DataFrame.from_dict(results_json["economic_data"]).loc["value"]

    # Obtaining the coordinates of the project location
    coordinates = (
        float(dfprojectData.latitude),
        float(dfprojectData.longitude),
    )

    # Determining the geographical location of the project
    geoList = rg.search(coordinates)
    geoDict = geoList[0]
    location = geoDict["name"]

    # Adds a map to the Dash app
    mapy = folium.Map(location=coordinates, zoom_start=14)
    tooltip = "Click here for more info"
    folium.Marker(
        coordinates,
        popup="Location of the project",
        tooltip=tooltip,
        icon=folium.Icon(color="red", icon="glyphicon glyphicon-flash"),
    ).add_to(mapy)
    mapy.save(os.path.join(REPO_PATH, "src", "assets", "proj_map"))

    dict_projectdata = {
        "Country": dfprojectData.country,
        "Project ID": dfprojectData.project_id,
        "Scenario ID": dfprojectData.scenario_id,
        "Currency": dfeconomicData.currency,
        "Project Location": location,
        "Discount Factor": dfeconomicData.discount_factor,
        "Tax": dfeconomicData.tax,
    }

    df_projectData = pd.DataFrame(
        list(dict_projectdata.items()), columns=["Label", "Value"]
    )

    dict_simsettings = {
        "Evaluated period": results_json["simulation_settings"]["evaluated_period"][
            "value"
        ],
        "Start date": results_json["simulation_settings"]["start_date"],
        "Timestep length": results_json["simulation_settings"]["timestep"]["value"],
    }

    df_simsettings = pd.DataFrame(
        list(dict_simsettings.items()), columns=["Setting", "Value"]
    )

    projectName = "Harbor Norway"
    scenarioName = "100% self-generation"

    releaseDesign = "0.0x"

    # Getting the branch ID
    repo = git.Repo(search_parent_directories=True)
    branchID = repo.head.object.hexsha

    simDate = time.strftime("%Y-%m-%d")

    ELAND_LOGO = base64.b64encode(
        open(
            os.path.join(REPO_PATH, "src", "assets", "logo-eland-original.jpg"), "rb"
        ).read()
    )

    # Determining the sectors which were simulated

    sectors = list(results_json["project_data"]["sectors"].keys())
    sec_list = """"""
    for sec in sectors:
        sec_list += "\n" + f"\u2022 {sec.upper()}"

    # Creating a dataframe for the demands
    demands = results_json["energyConsumption"]

    del demands["DSO_feedin"]
    del demands["Electricity excess"]

    dem_keys = list(demands.keys())

    demand_data = {}

    for dem in dem_keys:
        demand_data.update(
            {
                dem: [
                    demands[dem]["unit"],
                    demands[dem]["timeseries_peak"]["value"],
                    demands[dem]["timeseries_average"]["value"],
                    demands[dem]["timeseries_total"]["value"],
                ]
            }
        )

    df_dem = pd.DataFrame.from_dict(
        demand_data,
        orient="index",
        columns=["Unit", "Peak Demand", "Mean Demand", "Total Demand per annum"],
    )
    df_dem.index.name = "Demands"
    df_dem = df_dem.reset_index()
    df_dem = df_dem.round(2)

    # Creating a DF for the components table

    components1 = results_json["energyProduction"]
    components2 = results_json["energyConversion"]

    comp1_keys = list(components1.keys())
    comp2_keys = list(components2.keys())

    components = {}

    for comps in comp1_keys:
        components.update(
            {
                comps: [
                    components1[comps]["type_oemof"],
                    components1[comps]["unit"],
                    components1[comps]["installedCap"]["value"],
                    components1[comps]["optimizeCap"]["value"],
                ]
            }
        )
    for comps in comp2_keys:
        components.update(
            {
                comps: [
                    components2[comps]["type_oemof"],
                    components2[comps]["energyVector"],
                    components2[comps]["unit"],
                    components2[comps]["installedCap"]["value"],
                    components2[comps]["optimizeCap"]["value"],
                ]
            }
        )

    df_comp = pd.DataFrame.from_dict(
        components,
        orient="index",
        columns=[
            "Type of Component",
            "Energy Vector",
            "Unit",
            "Installed Capcity",
            "Optimization",
        ],
    )
    df_comp.index.name = "Component"
    df_comp = df_comp.reset_index()

    for i in range(len(df_comp)):
        if df_comp.at[i, "Optimization"]:
            df_comp.iloc[i, df_comp.columns.get_loc("Optimization")] = "Yes"
        else:
            df_comp.iloc[i, df_comp.columns.get_loc("Optimization")] = "No"

    # Creating a Pandas dataframe for the components optimization results table

    df_scalars = pd.read_excel(
        os.path.join(path_output_folder, "scalars.xlsx"), sheet_name="scalar_matrix"
    )
    df_scalars = df_scalars.drop(
        ["Unnamed: 0", "total_flow", "peak_flow", "average_flow"], axis=1
    )
    df_scalars = df_scalars.rename(
        columns={
            "label": "Component/Parameter",
            "optimizedAddCap": "CAP",
            "annual_total_flow": "Aggregated Flow",
        }
    )
    df_scalars = df_scalars.round(2)

    # Creating a Pandas dataframe for the costs' results

    df_costs1 = pd.read_excel(
        os.path.join(path_output_folder, "scalars.xlsx"), sheet_name="cost_matrix"
    )
    df_costs1 = df_costs1.round(2)
    df_costs = df_costs1[
        ["label", "costs_total", "costs_upfront", "annuity_total", "annuity_om"]
    ].copy()
    df_costs = df_costs.rename(
        columns={
            "label": "Component",
            "costs_total": "CAP",
            "costs_upfront": "Upfront Investment Costs",
        }
    )

    # Header section with logo and the title of the report, and CSS styling. Work in progress...

    app.layout = html.Div(
        [
            html.Div(
                className="header_title_logo",
                children=[
                    html.Img(
                        id="mvslogo",
                        src="data:image/png;base64,{}".format(ELAND_LOGO.decode()),
                        width="370px",
                    ),
                    html.H1("MULTI VECTOR SIMULATION - REPORT SHEET"),
                ],
                style={
                    "textAlign": "center",
                    "color": colors["text-head"],
                    "borderStyle": "solid",
                    "borderWidth": "thin",
                    "padding": "10px",
                    "margin": "30px",
                    "fontSize": "225%",
                },
            ),
            html.Div(
                className="imp-info",
                children=[
                    html.P(f"MVS Release: {releaseDesign}"),
                    html.P(f"Branch-id: {branchID}"),
                    html.P(f"Simulation date: {simDate}"),
                ],
                style={
                    "textAlign": "right",
                    "padding": "5px",
                    "fontSize": "22px",
                    "margin": "30px",
                },
            ),
            html.Div(
                className="imp_info2",
                children=[
                    html.Div(
                        [
                            html.Span(
                                "Project name   : ", style={"fontWeight": "bold"}
                            ),
                            f"{projectName}",
                        ]
                    ),
                    html.Br([]),
                    html.Div(
                        [
                            html.Span(
                                "Scenario name  : ", style={"fontWeight": "bold"}
                            ),
                            f"{scenarioName}",
                        ]
                    ),
                ],
                style={"textAlign": "left", "fontSize": "40px", "margin": "30px"},
            ),
            html.Div(
                className="blockoftext1",
                children=[
                    html.Div(
                        [
                            "The energy system with the ",
                            html.Span(f"{projectName}", style={"fontStyle": "italic"}),
                            " for the scenario ",
                            html.Span(f"{scenarioName}", style={"fontStyle": "italic"}),
                            " was simulated with the Multi-Vector simulation tool MVS 0.0x developed from the E-LAND toolbox "
                            "developed in the scope of the Horizon 2020 European research project. The tool was developed by "
                            "Reiner Lemoine Institute and utilizes the OEMOF framework.",
                        ]
                    )
                ],
                style={"textAlign": "justify", "fontSize": "40px", "margin": "30px"},
            ),
            html.Br([]),
            html.Div(
                className="inpdatabox",
                children=[html.H2("Input Data")],
                style={
                    "textAlign": "center",
                    "borderStyle": "solid",
                    "borderWidth": "thin",
                    "padding": "0.5px",
                    "margin": "30px",
                    "fontSize": "250%",
                    "width": "3000px",
                    "margin-left": "auto",
                    "margin-right": "auto",
                    "background": colors["inp-box"],
                    "color": colors["font-inpbox"],
                    "verticalAlign": "middle",
                },
            ),
            html.Br([]),
            html.Div(
                className="heading1",
                children=[
                    html.H2(
                        "Project Data",
                        style={
                            "textAlign": "left",
                            "margin": "30px",
                            "fontSize": "60px",
                            "color": "#8c3604",
                        },
                    ),
                    html.Hr(style={"color": "#000000", "margin": "30px",}),
                ],
            ),
            html.Div(
                className="blockoftext2",
                children=[
                    html.P(
                        "The most important simulation data will be presented below. "
                        "Detailed settings, costs, and technological parameters can "
                        "be found in the appendix.",
                        style={
                            "textAlign": "justify",
                            "fontSize": "40px",
                            "margin": "30px",
                        },
                    )
                ],
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4(
                                ["Project Location"],
                                className="projdataheading",
                                style={
                                    "position": "relative",
                                    "left": "0",
                                    "height": "20%",
                                    "borderLeft": "20px solid #8c3604",
                                    "background": "#ffffff",
                                    "paddingTop": "1px",
                                    "paddingBottom": "1px",
                                    "paddingLeft": "30px",
                                    "paddingRight": "60px",
                                    "fontSize": "40px",
                                },
                            ),
                            html.Iframe(
                                srcDoc=open(
                                    os.path.join(
                                        REPO_PATH, "src", "assets", "proj_map"
                                    ),
                                    "r",
                                ).read(),
                                width="70%",
                                height="700",
                            ),
                        ],
                        style={"margin": "30px", "width": "48%"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H4(
                                        ["Project Data"],
                                        className="projdataheading",
                                        style={
                                            "position": "relative",
                                            "left": "0",
                                            "height": "20%",
                                            "margin": "0mm",
                                            "borderLeft": "20px solid #8c3604",
                                            "background": "#ffffff",
                                            "paddingTop": "1px",
                                            "paddingBottom": "1px",
                                            "paddingLeft": "30px",
                                            "paddingRight": "60px",
                                        },
                                    ),
                                    html.Div(
                                        className="tableplay",
                                        children=[make_dash_data_table(df_projectData)],
                                    ),
                                ],
                                className="projdata",
                                style={
                                    "width": "48%",
                                    "margin": "30px",
                                    "fontSize": "40px",
                                },
                            )
                        ]
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H4(
                                        ["Simulation Settings"],
                                        className="projdataheading",
                                        style={
                                            "position": "relative",
                                            "left": "0",
                                            "height": "20%",
                                            "margin": "0mm",
                                            "borderLeft": "20px solid #8c3604",
                                            "background": "#ffffff",
                                            "paddingTop": "1px",
                                            "paddingBottom": "1px",
                                            "paddingLeft": "30px",
                                            "paddingRight": "60px",
                                        },
                                    ),
                                    html.Div(
                                        className="tableplay",
                                        children=[make_dash_data_table(df_simsettings)],
                                    ),
                                ],
                                className="projdata",
                                style={
                                    "width": "48%",
                                    "margin": "30px",
                                    "fontSize": "40px",
                                },
                            )
                        ]
                    ),
                ]
            ),
            html.Br(),
            html.Div(
                className="heading1",
                children=[
                    html.H2(
                        "Energy Demand",
                        style={
                            "textAlign": "left",
                            "margin": "30px",
                            "fontSize": "60px",
                            "color": "#8c3604",
                        },
                    ),
                    html.Hr(style={"color": "#000000", "margin": "30px",}),
                ],
            ),
            html.Div(
                className="blockoftext2",
                children=[
                    html.P(
                        "The simulation was performed for the energy system "
                        "covering the following sectors:"
                    ),
                    html.P(f"{sec_list}"),
                ],
                style={"textAlign": "justify", "fontSize": "40px", "margin": "30px"},
            ),
            html.Div(
                className="demandmatter",
                children=[
                    html.Br(),
                    html.H4("Electricity Demand", className="graph__pre-title",),
                    html.P("Electricity demands that have to be supplied are: "),
                ],
                style={"textAlign": "left", "fontSize": "40px", "margin": "30px"},
            ),
            html.Div(children=[make_dash_data_table(df_dem)]),
            html.Div(
                className="timeseriesplots",
                children=[
                    html.Div(
                        [
                            html.Img(
                                src="data:image/png;base64,{}".format(
                                    base64.b64encode(open(ts, "rb").read()).decode()
                                ),
                                width="1500px",
                            )
                            for ts in results_json[PATHS_TO_PLOTS][PLOTS_DEMANDS]
                        ]
                    ),
                    html.H4("Resources", className="graph__pre-title"),
                    html.Div(
                        [
                            html.Img(
                                src="data:image/png;base64,{}".format(
                                    base64.b64encode(open(ts, "rb").read()).decode()
                                ),
                                width="1500px",
                            )
                            for ts in results_json[PATHS_TO_PLOTS][PLOTS_RESOURCES]
                        ]
                    ),
                ],
                style={"margin": "30px"},
            ),
            html.Div(),
            html.Br(),
            html.Div(
                className="heading1",
                children=[
                    html.H2(
                        "Energy System Components",
                        style={
                            "textAlign": "left",
                            "margin": "30px",
                            "fontSize": "60px",
                            "color": "#8c3604",
                        },
                    ),
                    html.Hr(style={"color": "#000000", "margin": "30px",}),
                ],
            ),
            html.Div(
                className="blockoftext2",
                children=[
                    html.P(
                        "The energy system is comprised of the following components:"
                    )
                ],
                style={"textAlign": "justify", "fontSize": "40px", "margin": "30px"},
            ),
            html.Div(children=[make_dash_data_table(df_comp)]),
            html.Br([]),
            html.Div(
                className="simresultsbox",
                children=[html.H2("SIMULATION RESULTS")],
                style={
                    "textAlign": "center",
                    "borderStyle": "solid",
                    "borderWidth": "thin",
                    "padding": "0.5px",
                    "margin": "30px",
                    "fontSize": "250%",
                    "width": "3000px",
                    "margin-left": "auto",
                    "margin-right": "auto",
                    "background": colors["inp-box"],
                    "color": colors["font-inpbox"],
                    "verticalAlign": "middle",
                },
            ),
            html.Br([]),
            html.Div(
                className="heading1",
                children=[
                    html.H2(
                        "Dispatch & Energy Flows",
                        style={
                            "textAlign": "left",
                            "margin": "30px",
                            "fontSize": "60px",
                            "color": "#8c3604",
                        },
                    ),
                    html.Hr(style={"color": "#000000", "margin": "30px",}),
                ],
            ),
            html.Div(
                className="blockoftext2",
                children=[
                    html.P(
                        "The capacity optimization of components that were to be used resulted in:"
                    )
                ],
                style={"textAlign": "justify", "fontSize": "40px", "margin": "30px"},
            ),
            html.Div(children=[make_dash_data_table(df_scalars)]),
            html.Div(
                className="blockoftext2",
                children=[
                    html.P(
                        "With this, the demands are met with the following dispatch schedules:"
                    ),
                    html.P(
                        "a. Flows in the system for a duration of 14 days",
                        style={"marginLeft": "20px"},
                    ),
                ]
                + [
                    html.Div(
                        [
                            html.Img(
                                src="data:image/png;base64,{}".format(
                                    base64.b64encode(open(ts, "rb").read()).decode()
                                ),
                                width="1500px",
                            )
                            for ts in results_json[PATHS_TO_PLOTS][PLOTS_BUSSES]
                            + results_json[PATHS_TO_PLOTS][PLOTS_PERFORMANCE]
                        ]
                    ),
                ],
                style={"textAlign": "justify", "fontSize": "40px", "margin": "30px"},
            ),
            html.Br(style={"marginBottom": "5px"}),
            html.P(
                "This results in the following KPI of the dispatch:",
                style={
                    "marginLeft": "50px",
                    "textAlign": "justify",
                    "fontSize": "40px",
                },
            ),
            html.Div(
                className="heading1",
                children=[
                    html.H2(
                        "Economic Evaluation",
                        style={
                            "textAlign": "left",
                            "margin": "30px",
                            "fontSize": "60px",
                            "color": "#8c3604",
                        },
                    ),
                    html.Hr(style={"color": "#000000", "margin": "30px",}),
                ],
            ),
            html.P(
                "The following installation and operation costs result from capacity and dispatch optimization:",
                style={"margin": "30px", "textAlign": "justify", "fontSize": "40px",},
            ),
            html.Div(children=[make_dash_data_table(df_costs)]),
            html.Div(
                className="blockoftext2",
                children=[
                    html.Img(
                        src="data:image/png;base64,{}".format(
                            base64.b64encode(open(ts, "rb").read()).decode()
                        ),
                        width="1500px",
                    )
                    for ts in results_json[PATHS_TO_PLOTS][PLOTS_COSTS]
                ],
                style={"textAlign": "justify", "fontSize": "40px", "margin": "30px"},
            ),
        ]
    )
    return app


if __name__ == "__main__":
    test_app = create_app(CSV_FOLDER, OUTPUT_FOLDER)
    # app.run_server(debug=True)
    print_pdf(test_app)