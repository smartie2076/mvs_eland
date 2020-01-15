import pandas as pd
import os
import json
from pathlib import Path
import logging

"""
How to use:
all default input csv"s are stored in "/mvs_eland/inputs/elements/default_csv"
or the input directory/default_csv.
These csvs are not to be changed! All csvs that you need in order to set up 
your energy system should be stored into "/mvs_eland/inputs/elements/csv" or
the input directory/csv. In this directory you can change parameters and add 
components within the csv files. The given parameters need to be maintained. 
your energy system should be stored into "/mvs_eland/inputs/elements/csv" or
the input directory/csv. In this directory you can change parameters and add 
components within the csv files. The given parameters need to be maintained.
Storage: The "energyStorage.csv" contains information about all storages. 
For each storage there needs to be another file named exactly as the according 
storage-column in "energyStorage.csv", usually this is "storage_01", 
"storage_02" etc. Please stick to this convention.
After all the function "infer_resources()" reads all csv that are stored in 
the folder "/mvs_eland/inputs/elements/csv"/the input directory and creates one
json input file for mvs
"""


class DataInputFromCsv:
    def create_input_json(input_directory=None,
                          output_filename= "working_example2.json",
                          pass_back=True):

        """
        Method looks at all csv-files in "mvs_eland/inputs/elements/csv",
        converts them into json files and joins them together into the file
        "mvs_eland/inputs/working_example2.json". When reading the csv files it is
        checked, weather all required parameters for each component are given.
        Missing parameters will return a message.

        :param input_directory: str
            path of the directory where the input csv files can be found
        :param output_filename: str
            path of the output file with file extension (it should be .json)
        :param pass_back: binary
            if pass_back=True: the final json dict is returned. Otherwise it is
            only saved

        :return: None
            saves
        """
        if input_directory == None:
            input_directory = os.path.join(
            Path(os.path.dirname(__file__)).parent, "inputs/elements/"
        )

        logging.info(
            "loading and converting all csv's from %s" % input_directory +
            "csv/ into one json"
        )

        input_json = {}
        # hardcoded required lists of parameters for the according csv file
        maximum_files=['energyProduction', 'project', 'fixcost',
                              'simulation_settings', 'project_data',
                              'economic_data', 'energyConversion',
                              'energyStorage', 'energyProviders']
        required_files_list=['energyProduction', 'project', 'fixcost',
                              'simulation_settings', 'project_data',
                              'economic_data', 'energyProduction']
        parameterlist = {}
        parameterlist.update({'energyConsumption': ["dsm", "file_name", "label",
                                                     "type_asset", "type_oemof"]})
        parameterlist.update({'energyConversion': [
                    "age_installed",
                    "capex_fix",
                    "capex_var",
                    "efficiency",
                    "inflow_direction",
                    "installedCap",
                    "label",
                    "lifetime",
                    "opex_fix",
                    "opex_var",
                    "optimizeCap",
                    "outflow_direction",
                    "type_oemof",
                ]})
        parameterlist.update({'energyStorage': [
                    "inflow_direction",
                    "label",
                    "optimizeCap",
                    "outflow_direction",
                    "type_oemof",
                    "storage_filename",
                ]})
        parameterlist.update({'energyProduction': [
                    "age_installed",
                    "capex_fix",
                    "capex_var",
                    "file_name",
                    "installedCap",
                    "label",
                    "lifetime",
                    "opex_fix",
                    "opex_var",
                    "optimizeCap",
                    "outflow_direction",
                    "type_oemof",
                    "unit",
                ]})
        parameterlist.update({'energyProviders': [
                    "energy_price",
                    "feedin_tariff",
                    "inflow_direction",
                    "label",
                    "optimizeCap",
                    "outflow_direction",
                    "peak_demand_pricing",
                    "peak_demand_pricing_period",
                    "type_oemof",
                ]})
        parameterlist.update({'project': [
                    "capex_fix",
                    "capex_var",
                    "label",
                    "lifetime",
                    "opex_fix",
                    "opex_var",
                ]})
        parameterlist.update({'fixcost': [
                    "age_installed",
                    "capex_fix",
                    "capex_var",
                    "label",
                    "lifetime",
                    "opex_fix",
                    "opex_var",
                ]})
        parameterlist.update({'simulation_settings': [
                    "display_output",
                    "evaluated_period",
                    "input_file_name",
                    "label",
                    "oemof_file_name",
                    "output_lp_file",
                    "overwrite",
                    "path_input_file",
                    "path_input_folder",
                    "path_output_folder",
                    "path_output_folder_inputs",
                    "restore_from_oemof_file",
                    "start_date",
                    "store_oemof_results",
                    "timestep",
                ]})
        parameterlist.update({'project_data': [
                    "country",
                    "label",
                    "latitude",
                    "longitude",
                    "project_id",
                    "project_name",
                    "scenario_id",
                    "scenario_name",
                    "sectors",
                ]})
        parameterlist.update({'economic_data': [
                    "currency",
                    "discount_factor",
                    "label",
                    "project_duration",
                    "tax"
                ]})
        list_assets = []
        for f in os.listdir(os.path.join(input_directory, "csv/")):
            filename = f[:-4]
            if filename in parameterlist.keys():
                list_assets.append(str(filename))
                parameters = parameterlist[filename]
                single_dict = DataInputFromCsv.create_json_from_csv(input_directory,
                                                   filename,
                                                   parameters=parameters)
                input_json.update(single_dict)
            elif "storage_" in f:
                list_assets.append(str(f[:-4]))
                pass
            else:
                csv_default_directory = os.path.join(
                    Path(os.path.dirname(__file__)).parent,
                    "tests/default_csv/")
                logging.error(
                    "The file %s" % f + " is not recognized as input file for mvs "
                    "check %s", csv_default_directory + "for correct "
                    "file names."
                )
        #check if all required files are available
        extra = list(set(list_assets) ^ set(maximum_files))
#        missing = list(set(list_assets) ^ set(required_files_list))
        for i in extra:
            if i in required_files_list:
                logging.error(
                    'Required input file %s' %i + " is missing! Please add it"
                "into %s" %os.path.join(input_directory, "csv/") +".")
            elif i in maximum_files:
                logging.debug("No %s" %i +".csv file found. This is an "
                                          "accepted option.")
            elif "storage_" in i:
                pass
            else:
                logging.debug("File %s" % i + ".csv is an unknown filename and"
                              " will not be processed.")


        with open(os.path.join(input_directory, output_filename), "w") as outfile:
            json.dump(input_json, outfile, skipkeys=True, sort_keys=True, indent=4)
        logging.info("Json file created successully from csv's and stored into"
                     "/mvs_eland/inputs/%s" % output_filename + "\n"
                    "Scenario includes %s" % len(list_assets) + " assets of "
                    "type: %s" % list_assets)
        logging.debug("Json created successfully from csv.")
        if pass_back:
            return input_json


    def create_json_from_csv(input_directory, filename, parameters):

        """
        One csv file is loaded and it's parameters are checked. The csv file is
        then converted to a dictionary; the name of the csv file is used as the
        main key of the dictionary. Exceptions are made for the files
        ["economic_data", "project", "project_data", "simulation_settings"], here
        no main key is added. Another exception is made for the file
        "energyStorage". When this file is processed, the according "storage_"
        files (names of the "storage_"-columns in "energyStorage" are called and
        added to the energyStorage Dictionary.


        :param input_directory: str
            path of the directory where the input csv files can be found
        :param filename: str
            name of the inputfile that is transformed into a json, without
            extension
        :param parameters: list
            List of parameters names that are required
        :return: dict
            the converted dictionary
        """

        logging.debug(
            "Loading input data from csv: %s", filename
        )
        csv_default_directory=os.path.join(
            Path(os.path.dirname(__file__)).parent, "tests/default_csv/")
        df = pd.read_csv(
            os.path.join(input_directory, "csv/", "%s.csv" % filename),
            sep=",",
            header=0,
            index_col=0,
        )

        # check parameters
        extra = list(set(parameters) ^ set(df.index))
        if len(extra) > 0:
            for i in extra:
                if i in parameters:
                    logging.error(
                        "In the file %s.csv" % filename
                        + " the parameter "
                        + str(i)
                        + " is missing. "
                        "check %s", csv_default_directory + "for correct "
                        "parameter names."
                    )
                else:
                    logging.error(
                        "In the file %s.csv" % filename
                        + " the parameter "
                        + str(i)
                        + " is not recognized. \n"
                        "check %s", csv_default_directory + "for correct "
                        "parameter names."
                    )

        # convert csv to json
        single_dict2 = {}
        single_dict = {}
        if len(df.columns) ==1:
            logging.debug(
                "No %s" % filename + " assets are added because all "
                                     "columns of the csv file are empty.")
        for column in df:
            if column != "unit":
                column_dict = {}
                for i, row in df.iterrows():
                    if row["unit"] == "str":
                        column_dict.update({i: row[column]})
                    else:
                        column_dict.update({i: {"value": row[column], "unit": row["unit"]}})
                single_dict.update({column: column_dict})
                # add exception for energyStorage
                if filename == "energyStorage":
                    storage_dict = DataInputFromCsv.add_storage(column, input_directory)
                    single_dict[column].update(storage_dict)
        # add exception for single dicts
        if filename in ["economic_data", "project", "project_data", "simulation_settings"]:
            return single_dict
        elif "storage_" in filename:
            return single_dict
        else:
            single_dict2.update({filename: single_dict})
            return single_dict2


    def add_storage(storage_filename, input_directory):

        """
        loads the csv of a the specific storage listed as column in
        "energyStorage.csv", checks for complete set of parameters and creates a
        json dictionary.
        :param storage_filename: str
            name of storage, given by the column name in "energyStorage.csv
        :param input_directory: str
            path of the input directory
        :return: dict
            dictionary containing the storage parameters
        """

        if not os.path.exists(
            os.path.join(input_directory, "csv/", "%s.csv" % storage_filename)
        ):
            logging.error("The storage file %s.csv" % storage_filename + " is missing!")
        else:
            parameters = [
                "age_installed",
                "capex_fix",
                "capex_var",
                "crate",
                "efficiency",
                "installedCap",
                "label",
                "lifetime",
                "opex_fix",
                "opex_var",
                "soc_initial",
                "soc_max",
                "soc_min",
                "unit",
            ]
            single_dict = DataInputFromCsv.create_json_from_csv(
                input_directory, filename=storage_filename, parameters=parameters
            )
            return single_dict


if __name__ == "__main__":
    DataInputFromCsv.create_input_json()
