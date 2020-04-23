import json
import numpy
import pandas as pd
import logging
import matplotlib.pyplot as plt
import os

import src.F1_plotting as plots

r"""
Module F0 Output
================
The model F0 output defines all functions that store evaluation results to file.
- Aggregate demand profiles to a total demand profile
- Plotting all energy flows for both 14 and 365 days for each energy bus
- Store timeseries of all energy flows to excel (one sheet = one energy bus)
- execute function: plot optimised capacities as a barchart (F1)
- execute function: plot all annuities as a barchart (F1)
- store scalars/KPI to excel
- process dictionary so that it can be stored to Json
- store dictionary to Json
"""


def evaluate_dict(dict_values):
    """
    This is the main function of F0. It calls all functions that prepare the simulation output, ie. Storing all simulation output into excellent files, bar charts, and graphs.
    :param dict_values: dict Of all input and output parameters up to F0
    :return: NA
    """

    logging.info(
        "Summarizing simulation results to results_timeseries and results_scalars_assets."
    )

    for sector in dict_values["project_data"]["sectors"]:
        sector_name = dict_values["project_data"]["sectors"][sector]

        logging.info("Aggregating flows for the %s sector.", sector_name)

        # Plot flows for one sector for the 14 first days
        plots.flows(
            dict_values["simulation_settings"],
            dict_values["project_data"],
            dict_values["optimizedFlows"][sector_name + " bus"],
            sector,
            14,
        )

        # Plot flows for one sector for a year
        plots.flows(
            dict_values["simulation_settings"],
            dict_values["project_data"],
            dict_values["optimizedFlows"][sector_name + " bus"],
            sector,
            365,
        )

        """
        ###
        # Aggregation of demand profiles to total demand
        ###
        This would store demands are twice - as total demand as well as individual demand!

        # Initialize
        total_demand = pd.Series(
            [0 for i in dict_values["simulation_settings"]["time_index"]],
            index=dict_values["simulation_settings"]["time_index"],
        )

        # Add demands (exclude excess)
        for asset in dict_values["energyConsumption"]:
            # key "energyVector" not included in excess sinks, ie. this filters them out from demand.
            if "energyVector" in dict_values["energyConsumption"][asset].keys() \
                    and dict_values["energyConsumption"][asset]["energyVector"] == sector_name:
                total_demand = (
                    total_demand + dict_values["energyConsumption"][asset]["flow"]
                )

        # todo this should actually link to C0: helpers.bus_suffix
        dict_values["optimizedFlows"][sector_name + " bus"][
            "Total demand " + sector_name
        ] = total_demand
        """

    # storing all flows to exel.
    store_timeseries_all_busses_to_excel(dict_values)

    # plot optimal capacities if there are optimized assets
    plot_optimized_capacities(dict_values)

    # plot annuity, first-investment and om costs
    plots.costs(dict_values)

    # Write everything to file with multipe tabs
    store_scalars_to_excel(dict_values)
    return


def plot_optimized_capacities(dict_values):
    """
    This function determinants whether or not any capacities are added to the optimal system and calls the function plotting those capacities as a bar chart.
    :param dict_values: dict Of all input and output parameters up to F0
    :return: Bar chart of capacities
    """

    show_optimal_capacities = False
    for element in dict_values["kpi"]["scalar_matrix"]["optimizedAddCap"].values:
        if element > 0:
            show_optimal_capacities = True
    if show_optimal_capacities:
        plots.capacities(
            dict_values["simulation_settings"],
            dict_values["project_data"],
            dict_values["kpi"]["scalar_matrix"]["label"],
            dict_values["kpi"]["scalar_matrix"]["optimizedAddCap"],
        )
    return


def store_scalars_to_excel(dict_values):
    """
    All output data that is a scalar is storage to an excellent file tab. This could for example be economical data or technical data.
    :param dict_values: dict Of all input and output parameters up to F0
    :return: Excel file with scalar data
    """
    results_scalar_output_file = "/scalars" + ".xlsx"
    with pd.ExcelWriter(
        dict_values["simulation_settings"]["path_output_folder"]
        + results_scalar_output_file
    ) as open_file:  # doctest: +SKIP
        for kpi_set in dict_values["kpi"]:
            if isinstance(dict_values["kpi"][kpi_set], dict):
                data = pd.DataFrame([dict_values["kpi"][kpi_set]]).to_excel(
                    open_file, sheet_name=kpi_set
                )
            else:
                dict_values["kpi"][kpi_set].to_excel(open_file, sheet_name=kpi_set)
            logging.info(
                "Saved scalar results to: %s, tab %s.",
                results_scalar_output_file,
                kpi_set,
            )
    return


def store_timeseries_all_busses_to_excel(dict_values):
    """
    This function plots the energy flows of each single bus and the energy system and saves it as PNG and additionally as a tab and an Excel sheet.
    :param dict_values: dict Of all input and output parameters up to F0
    :return: Plots and excel with all timeseries of each bus
    """

    timeseries_output_file = "/timeseries_all_busses" + ".xlsx"
    with pd.ExcelWriter(
        dict_values["simulation_settings"]["path_output_folder"]
        + timeseries_output_file
    ) as open_file:  # doctest: +SKIP
        for bus in dict_values["optimizedFlows"]:
            dict_values["optimizedFlows"][bus].to_excel(open_file, sheet_name=bus)
            dict_values["optimizedFlows"][bus].plot()
            plt.savefig(
                dict_values["simulation_settings"]["path_output_folder"]
                + "/"
                + bus
                + " flows.png",
                bbox_inches="tight",
            )

            plt.close()
            plt.clf()
            plt.cla()

    logging.info("Saved flows at busses to: %s.", timeseries_output_file)
    return


def convert(o):
    """
    This converts all data stored in dict_values that is not compatible with the json format to a format that is compatible.
    :param o: Any type. Object to be converted to json-storable value.
    :return: json-storable value.
    """
    if isinstance(o, numpy.int64):
        answer = int(o)
    # todo this actually drops the date time index, which could be interesting
    elif isinstance(o, pd.DatetimeIndex):
        answer =  "date_range"
    elif isinstance(o, pd.Timestamp):
        answer =  str(o)
    # todo this also drops the timeindex, which is unfortunate.
    elif isinstance(o, pd.Series):
        answer =  "pandas timeseries"
    elif isinstance(o, numpy.ndarray):
        answer =  "numpy timeseries"
    elif isinstance(o, pd.DataFrame):
        answer =  "pandas dataframe"
    else:
        raise TypeError(
            "An error occurred when converting the simulation data (dict_values) to json, as the type is not recognized: \n"
            "Type: " + str(type(o)) + " \n "
            "Value(s): " + str(o) + "\n"
            "Please edit function CO_data_processing.dataprocessing.store_as_json."
    )

    return answer

def store_as_json(dict_values, output_folder, file_name):
    """
    Stores are dictionary as a Json file and converts all values that are incompatible with the Json format
    :param dict_values: dict to be stored as json
    :param output_folder: Folder into which json should be stored
    :param file_name: Name of the file the json should be stored as
    :return: Stored json file
    """
    file_path = os.path.abspath(os.path.join(output_folder, file_name + ".json"))
    myfile = open(file_path, "w")
    json_data = json.dumps(
        dict_values, skipkeys=True, sort_keys=True, default=convert, indent=4
    )
    myfile.write(json_data)
    myfile.close()
    logging.info(
        "Converted and stored processed simulation data to json: %s", file_path
    )
    return
