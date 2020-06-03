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
FIX_COST = "fixcost"
ECONOMIC_DATA = "economic_data"
PROJECT_DATA = "project_data"
# Parameters
SECTORS = "sectors"
OUTFLOW_DIRECTION = "outflow_direction"
INFLOW_DIRECTION = "inflow_direction"
ENERGY_VECTOR = "energyVector"
OEMOF_ASSET_TYPE = "type_oemof"
# Allowed types
OEMOF_TRANSFORMER = "transformer"
OEMOF_GEN_STORAGE = "storage"
OEMOF_SOURCE = "source"
OEMOF_SINK = "sink"
# OEMOF_BUSSES = "bus"

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

EFFICIENCY = "efficiency"
OPTIMIZE_CAP = "optimizeCap"
INSTALLED_CAP = "installedCap"
AGE_INSTALLED = "age_installed"
LIFETIME = "lifetime"
CAPEX_FIX = "capex_fix"
CAPEX_VAR = "capex_var"
OPEX_FIX = "opex_fix"
OPEX_VAR = "opex_var"
