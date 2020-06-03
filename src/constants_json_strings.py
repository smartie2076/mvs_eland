"""
Defines the strings of different json parameters
Not defining parameters as strings can be helpful, ig. if
    if string in dict_values
Is used, where typos can be very bad for future handling.
"""

# Asset groups
ENERGY_CONVERSION = "energyConversion"
ENERGY_CONSUMPTION = "energyConsumption"
ENERGY_PRODUCTION = "energyProduction"
ENERGY_STORAGE = "energyStorage"
ENERGY_BUSSES = "energyBusses"

ENERGY_PROVIDERS = "energyProviders"
SIMULATION_SETTINGS = "simulation_settings"
EVALUATED_PERIOD = "evaluated_period"
START_DATE = "start_date"
END_DATE = "end_date"
TIMESTEP = "timestep"
TIME_INDEX = "time_index"
TIMESERIES = "timeseries"
TIMESERIES_NORMALIZED = "timeseries_normalized"
TIMESERIES_PEAK = "timeseries_peak"

ENERGY_PRICE = "energy_price"
FEEDIN_TARIFF = "feedin_tariff"
ANNUITY_FACTOR = "annuity_factor"
FIX_COST = "fixcost"
ECONOMIC_DATA = "economic_data"
PROJECT_DATA = "project_data"
# Parameters
SECTORS = "sectors"
OUTFLOW_DIRECTION = "outflow_direction"
INFLOW_DIRECTION = "inflow_direction"
OUTPUT_BUS_NAME = "output_bus_name"
INPUT_BUS_NAME = "input_bus_name"
ENERGY_VECTOR = "energyVector"
OEMOF_ASSET_TYPE = "type_oemof"
# Allowed types
OEMOF_TRANSFORMER = "transformer"
OEMOF_GEN_STORAGE = "storage"
OEMOF_SOURCE = "source"
OEMOF_SINK = "sink"
# OEMOF_BUSSES = "bus"

C_RATE = "c_rate"
INPUT_POWER = "input power"
OUTPUT_POWER = "output power"
STORAGE_CAPACITY = "storage capacity"
SOC_INITIAL = "soc_initial"
SOC_MAX = "soc_max"
SOC_MIN = "soc_min"
# Dict generated from above defined strings
ACCEPTED_ASSETS_FOR_ASSET_GROUPS = {
    ENERGY_CONVERSION: [OEMOF_TRANSFORMER],
    ENERGY_STORAGE: [OEMOF_GEN_STORAGE],
    ENERGY_PRODUCTION: [OEMOF_SOURCE],
    ENERGY_CONSUMPTION: [OEMOF_SINK],
}

# Central constant variables
UNIT = "unit"
VALUE = "value"

# Parameter strings in json and csv files
CURR = "currency"
DISCOUNTFACTOR = "discount_factor"
LABEL = "label"
PROJECT_DURATION = "project_duration"
TAX = "tax"
FILENAME = "file_name"
STORAGE_FILENAME = "storage_filename"

EFFICIENCY = "efficiency"
OPTIMIZE_CAP = "optimizeCap"
INSTALLED_CAP = "installedCap"
AGE_INSTALLED = "age_installed"
LIFETIME = "lifetime"
CAPEX_FIX = "capex_fix"
CAPEX_VAR = "capex_var"
OPEX_FIX = "opex_fix"
OPEX_VAR = "opex_var"
PEAK_DEMAND_PRICING = "peak_demand_pricing"
PEAK_DEMAND_PRICING_PERIOD = "peak_demand_pricing_period"
