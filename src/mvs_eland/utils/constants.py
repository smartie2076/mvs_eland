import os

from mvs_eland.utils.constants_json_strings import *

# path to the root of this repository (assumes this file is in src/mvs_eland/utils folder)
REPO_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
# name of the default input folder
INPUT_FOLDER = "inputs"
# name of the template input folder
TEMPLATE_INPUT_FOLDER = "input_template"
# name of the json extension
JSON_EXT = "json"
# name of the csv extension
CSV_EXT = "csv"
# name of the folder containing mvs model described by .csv files
CSV_ELEMENTS = "csv_elements"
# name of the json file which should be present in the input folder if option -i json was chosen
JSON_FNAME = "mvs_config.json"
# name of the json file which is should be created in the input folder if option -i csv was chosen
CSV_FNAME = "mvs_csv_config.json"
# allowed symbols for separating values in .csv files
CSV_SEPARATORS = (",", ";", "&")
# name of the folder containing timeseries described by .csv files
TIME_SERIES = "time_series"
# name of the folder containing the output of the simulation
OUTPUT_FOLDER = "MVS_outputs"
# name of the folder containing the copied content of the input folder within the output folder
INPUTS_COPY = INPUT_FOLDER
# name of the MVS log file
LOGFILE = "mvs_logfile.log"
# name of the automatically generated pdf report
PDF_REPORT = "simulation_report.pdf"
# path of the pdf report path
REPORT_PATH = os.path.join(REPO_PATH, "report")

# default paths to input, output and sequences folders
DEFAULT_INPUT_PATH = os.path.join(REPO_PATH, INPUT_FOLDER)
DEFAULT_OUTPUT_PATH = os.path.join(REPO_PATH, OUTPUT_FOLDER)

TEMPLATE_INPUT_PATH = os.path.join(REPO_PATH, TEMPLATE_INPUT_FOLDER)

PATH_INPUT_FILE = "path_input_file"
PATH_INPUT_FOLDER = "path_input_folder"
PATH_OUTPUT_FOLDER = "path_output_folder"
PATH_OUTPUT_FOLDER_INPUTS = "path_output_folder_inputs"
INPUT_TYPE = "input_type"
OVERWRITE = "overwrite"
DISPLAY_OUTPUT = "display_output"
SAVE_PNG = "save_png"

USER_INPUT_ARGUMENTS = (
    PATH_INPUT_FILE,
    PATH_INPUT_FOLDER,
    PATH_OUTPUT_FOLDER,
    INPUT_TYPE,
    OVERWRITE,
    DISPLAY_OUTPUT,
)

DEFAULT_MAIN_KWARGS = dict(
    overwrite=False,
    pdf_report=False,
    save_png=False,
    input_type=JSON_EXT,
    path_input_folder=DEFAULT_INPUT_PATH,
    path_output_folder=DEFAULT_OUTPUT_PATH,
    display_output="info",
    lp_file_output=False,
)
# list of csv filename which must be present within the CSV_ELEMENTS folder with the parameters
# associated to each of these filenames
REQUIRED_CSV_PARAMETERS = {
    CONSTRAINTS: [MINIMAL_RENEWABLE_SHARE],
    ENERGY_CONSUMPTION: [
        DSM,
        FILENAME,
        LABEL,
        TYPE_ASSET,
        OEMOF_ASSET_TYPE,
        ENERGY_VECTOR,
        INFLOW_DIRECTION,
        UNIT,
    ],
    ENERGY_CONVERSION: [
        AGE_INSTALLED,
        DEVELOPMENT_COSTS,
        SPECIFIC_COSTS,
        EFFICIENCY,
        INFLOW_DIRECTION,
        INSTALLED_CAP,
        LABEL,
        LIFETIME,
        SPECIFIC_COSTS_OM,
        DISPATCH_PRICE,
        OPTIMIZE_CAP,
        OUTFLOW_DIRECTION,
        OEMOF_ASSET_TYPE,
        ENERGY_VECTOR,
        UNIT,
    ],
    ENERGY_STORAGE: [
        INFLOW_DIRECTION,
        LABEL,
        OPTIMIZE_CAP,
        OUTFLOW_DIRECTION,
        OEMOF_ASSET_TYPE,
        STORAGE_FILENAME,
        ENERGY_VECTOR,
    ],
    ENERGY_PRODUCTION: [
        AGE_INSTALLED,
        DEVELOPMENT_COSTS,
        SPECIFIC_COSTS,
        FILENAME,
        INSTALLED_CAP,
        LABEL,
        LIFETIME,
        SPECIFIC_COSTS_OM,
        DISPATCH_PRICE,
        OPTIMIZE_CAP,
        OUTFLOW_DIRECTION,
        OEMOF_ASSET_TYPE,
        UNIT,
        ENERGY_VECTOR,
    ],
    ENERGY_PROVIDERS: [
        ENERGY_PRICE,
        FEEDIN_TARIFF,
        INFLOW_DIRECTION,
        LABEL,
        OPTIMIZE_CAP,
        OUTFLOW_DIRECTION,
        PEAK_DEMAND_PRICING,
        PEAK_DEMAND_PRICING_PERIOD,
        OEMOF_ASSET_TYPE,
        ENERGY_VECTOR,
    ],
    FIX_COST: [
        AGE_INSTALLED,
        DEVELOPMENT_COSTS,
        SPECIFIC_COSTS,
        LABEL,
        LIFETIME,
        SPECIFIC_COSTS_OM,
        DISPATCH_PRICE,
    ],
    SIMULATION_SETTINGS: [
        EVALUATED_PERIOD,
        LABEL,
        OUTPUT_LP_FILE,
        STORE_OEMOF_RESULTS,
        START_DATE,
        STORE_OEMOF_RESULTS,
        TIMESTEP,
    ],
    PROJECT_DATA: [
        COUNTRY,
        LABEL,
        LATITUDE,
        LONGITUDE,
        PROJECT_ID,
        PROJECT_NAME,
        SCENARIO_ID,
        SCENARIO_NAME,
    ],
    ECONOMIC_DATA: [
        CURR,
        DISCOUNTFACTOR,
        LABEL,
        PROJECT_DURATION,
        TAX,
    ],
}

# list of csv filename which must be present within the CSV_ELEMENTS folder
REQUIRED_CSV_FILES = tuple(REQUIRED_CSV_PARAMETERS.keys())
# list of parameters which must be present within the JSON_FNAME file with the sub-parameters
# note: if the value of a key is none, then the value is expected to be user-defined and thus cannot
# be in a required parameters dict
REQUIRED_JSON_PARAMETERS = {
    ECONOMIC_DATA: [CURR, DISCOUNTFACTOR, LABEL, PROJECT_DURATION, TAX],
    ENERGY_CONSUMPTION: None,
    ENERGY_CONVERSION: None,
    ENERGY_PRODUCTION: None,
    ENERGY_PROVIDERS: None,
    ENERGY_STORAGE: None,
    FIX_COST: None,
    CONSTRAINTS: [MINIMAL_RENEWABLE_SHARE],
    PROJECT_DATA: [
        COUNTRY,
        LABEL,
        LATITUDE,
        LONGITUDE,
        PROJECT_ID,
        PROJECT_NAME,
        SCENARIO_ID,
        SCENARIO_NAME,
    ],
    SIMULATION_SETTINGS: [
        EVALUATED_PERIOD,
        LABEL,
        OUTPUT_LP_FILE,
        START_DATE,
        STORE_OEMOF_RESULTS,
        TIMESTEP,
    ],
}
# references for which parameters must be present either in the json or csv input method
REQUIRED_MVS_PARAMETERS = {
    JSON_EXT: REQUIRED_JSON_PARAMETERS,
    CSV_EXT: REQUIRED_CSV_PARAMETERS,
}

MISSING_PARAMETERS_KEY = "missing_parameters"
EXTRA_PARAMETERS_KEY = "extra_parameters"

# Instroducting new parameters (later to be merged into list ll.77)
WARNING_TEXT = "warning_text"
REQUIRED_IN_CSV_ELEMENTS = "required in files"
DEFAULT_VALUE = "default"

# name of the key linking to the special type of data in a json object
DATA_TYPE_JSON_KEY = "data_type"
# possible type of variable stored into the json file
TYPE_DATETIMEINDEX = "pandas_DatetimeIndex"
TYPE_SERIES = "pandas_Series"
TYPE_DATAFRAME = "pandas_Dataframe"
TYPE_NDARRAY = "numpy_ndarray"
TYPE_TIMESTAMP = "pandas_Timestamp"
TYPE_BOOL = "bool"
TYPE_INT64 = "numpy_int64"
TYPE_STR = "str"
TYPE_NONE = "None"
TYPE_FLOAT = "float"

EXTRA_CSV_PARAMETERS = {
    UNIT: {
        DEFAULT_VALUE: "NA",
        UNIT: TYPE_STR,
        WARNING_TEXT: "defines the unit of power provided by a DSO (Values: str). ",
        REQUIRED_IN_CSV_ELEMENTS: [ENERGY_PROVIDERS],
    },
    MAXIMUM_CAP: {
        DEFAULT_VALUE: None,
        UNIT: TYPE_NONE,
        WARNING_TEXT: "allows setting a maximum capacity for an asset that is being capacity optimized (Values: None/Float). ",
        REQUIRED_IN_CSV_ELEMENTS: [ENERGY_CONVERSION, ENERGY_PRODUCTION],
    },
    RENEWABLE_ASSET_BOOL: {
        DEFAULT_VALUE: False,
        UNIT: TYPE_BOOL,
        WARNING_TEXT: "allows defining a energyProduction asset as either renewable (True) or non-renewable (False) source. ",
        REQUIRED_IN_CSV_ELEMENTS: [ENERGY_PRODUCTION],
    },
    RENEWABLE_SHARE_DSO: {
        DEFAULT_VALUE: 0,
        UNIT: TYPE_FLOAT,
        WARNING_TEXT: "allows defining the renewable share of the DSO supply (Values: Float). ",
        REQUIRED_IN_CSV_ELEMENTS: [ENERGY_PROVIDERS],
    },
}

ENERGY_CARRIER_UNIT = "energy_carrier_unit"
DEFAULT_WEIGHTS_ENERGY_CARRIERS = {
    "Electricity": {UNIT: "kWh_eleq/kWh_el", VALUE: 1, ENERGY_CARRIER_UNIT: "kWh_el"},
    "Heat": {UNIT: "KWh_eleq/kWh_therm", VALUE: 1, ENERGY_CARRIER_UNIT: "kWh_therm"},
    "H2": {
        UNIT: "kWh_eleq/kgH2",
        VALUE: 32.87,
        ENERGY_CARRIER_UNIT: "kgH2",
    },  # https://epact.energy.gov/fuel-conversion-factors
    "Diesel": {
        UNIT: "kWh_eleq/l",
        VALUE: 8.20,
        ENERGY_CARRIER_UNIT: "l",
    },  # https://epact.energy.gov/fuel-conversion-factors, convertion gallon->4.546092 l
    "Gas": {
        UNIT: "kWh_eleq/m3",
        VALUE: 5.38,
        ENERGY_CARRIER_UNIT: "l",
    },  # https://epact.energy.gov/fuel-conversion-factors, convertion gallon->4.546092 l
}

# dict keys in results_json file
TIMESERIES = "timeseries"

# filename of the energy system graph
ES_GRAPH = "energy_system_graph.png"

# key of the dict containing generated plots filesnames in results_json file
PATHS_TO_PLOTS = "paths_to_plots"
# keys' names of dict containing generated plots filenames
PLOTS_DEMANDS = "demands"
PLOTS_RESOURCES = "resources"
PLOTS_ES = "graphviz"
PLOTS_PERFORMANCE = "performance"
PLOTS_COSTS = "costs"
PLOTS_BUSSES = "flows_on_busses"

# structure of the dict containing generated plots filenames in results_json file
DICT_PLOTS = {
    PATHS_TO_PLOTS: {
        PLOTS_BUSSES: [],
        PLOTS_DEMANDS: [],
        PLOTS_RESOURCES: [],
        PLOTS_ES: [],
        PLOTS_PERFORMANCE: [],
        PLOTS_COSTS: [],
    }
}

# Reading data from csv file
HEADER = "header"

# Filenames of the json files stored to disc:

JSON_WITH_RESULTS = "json_with_results.json"