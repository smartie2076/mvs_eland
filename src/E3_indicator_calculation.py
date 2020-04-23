r"""
Module E3 indicator calculation
-------------------------------

In module E3 the technical KPI are evaluated:
- calculate renewable share
- calculate degree of autonomy
- calculate total generation of each asset
- calculate energy flows between sectors
- calculate degree of sector coupling
"""
import logging
import pandas as pd

from src.constants import DEFAULT_WEIGHTS_ENERGY_CARRIERS
from src.constants import (
    KPI_DICT,
    KPI_SCALARS_DICT,
    KPI_UNCOUPLED_DICT,
    KPI_COST_MATRIX,
)


def all_totals(dict_values):
    """
    Calculate sum of all cost parameters
    :param dict_values: dict all input parameters and restults up to E0
    :return: List of all total cost parameters for the project
    """
    for column in dict_values[KPI_DICT][KPI_COST_MATRIX].columns:
        if column != "label":
            dict_values[KPI_DICT][KPI_SCALARS_DICT].update(
                {column: dict_values[KPI_DICT][KPI_COST_MATRIX][column].sum()}
            )
    return


def total_demand_each_sector(dict_values):
    """

    :param dict_values: dict with all project input data and results up to E0
    :return:
    """
    return


def total_renewable_and_non_renewable_energy_origin(dict_values):
    """
    Identifies all renewable generation assets and summs up their total generation to total renewable generation
    :param dict_values: dict with all project input data and results up to E0
    :return: Updated dict_values with total internal/overall renewable and non-renewable energy origin
    """
    dict_values[KPI_DICT].update({KPI_UNCOUPLED_DICT: {}})

    renewable_origin = {}
    non_renewable_origin = {}
    for sector in dict_values["project_data"]["sectors"]:
        renewable_origin.update({sector: 0})
        non_renewable_origin.update({sector: 0})

    for asset in dict_values["energyProduction"]:
        if "renewableAsset" in dict_values["energyProduction"][asset]:
            sector = dict_values["energyProduction"][asset]["energyVector"]
            if (
                dict_values["energyProduction"][asset]["renewableAsset"]["value"]
                is True
            ):
                renewable_origin[sector] += dict_values["energyProduction"][asset][
                    "total_flow"
                ]["value"]
            else:
                non_renewable_origin[sector] += dict_values["energyProduction"][asset][
                    "total_flow"
                ]["value"]

    dict_values[KPI_DICT][KPI_UNCOUPLED_DICT].update(
        {
            "Total internal renewable generation": renewable_origin.copy(),
            "Total internal non-renewable generation": non_renewable_origin.copy(),
        }
    )

    for DSO in dict_values["energyProviders"]:
        sector = dict_values["energyProviders"][DSO]["energyVector"]
        for DSO_source in dict_values["energyProviders"][DSO][
            "connected_consumption_sources"
        ]:
            renewable_origin[sector] += (
                dict_values["energyProduction"][DSO_source]["total_flow"]["value"]
                * dict_values["energyProviders"][DSO]["renewable_share"]["value"]
            )
            non_renewable_origin[sector] += dict_values["energyProduction"][DSO_source][
                "total_flow"
            ]["value"] * (
                1 - dict_values["energyProviders"][DSO]["renewable_share"]["value"]
            )

    dict_values[KPI_DICT][KPI_UNCOUPLED_DICT].update(
        {
            "Total renewable energy use": renewable_origin,
            "Total non-renewable energy use": non_renewable_origin,
        }
    )

    for sector_specific_kpi in [
        "Total internal renewable generation",
        "Total internal non-renewable generation",
        "Total renewable energy use",
        "Total non-renewable energy use",
    ]:
        weighting_for_sector_coupled_kpi(dict_values, sector_specific_kpi)
    return


def renewable_share(dict_values):
    """
    Determination of renewable share of one sector
    :param dict_values: dict with all project information and results, after applying total_renewable_and_non_renewable_energy_origin
    :param sector: Sector for which renewable share is being calculated
    :return: updated dict_values with renewable share of a specific sector
    """
    kpi_name = "Renewable share"
    dict_renewable_share = {}
    for sector in dict_values["project_data"]["sectors"]:
        total_res = dict_values[KPI_DICT][KPI_UNCOUPLED_DICT][
            "Total renewable energy use"
        ][sector]
        total_non_res = dict_values[KPI_DICT][KPI_UNCOUPLED_DICT][
            "Total non-renewable energy use"
        ][sector]
        dict_renewable_share.update(
            {sector: renewable_share_equation(total_res, total_non_res)}
        )

    dict_values[KPI_DICT][KPI_UNCOUPLED_DICT].update({kpi_name: dict_renewable_share})

    total_res = dict_values[KPI_DICT][KPI_SCALARS_DICT]["Total renewable energy use"]
    total_non_res = dict_values[KPI_DICT][KPI_SCALARS_DICT][
        "Total non-renewable energy use"
    ]
    dict_values[KPI_DICT][KPI_SCALARS_DICT].update(
        {kpi_name: renewable_share_equation(total_res, total_non_res)}
    )
    return


def renewable_share_equation(total_res, total_non_res):
    """
    Calculates the renewable share
    :param total_res: Renewable generation of a system
    :param total_non_res: Non-renewable generation of a system
    :return: Renewable share

    renewable share = 1 - all energy in the energy system is of renewable origin
    renewable share < 1 - part of the energy in the system is of renewable origin
    renewable share = 0 - no energy is of renewable orgigin

    As for now this is relative to generation, but not consumption of energy, the renewable share can not be larger 1. If in future however the renewable share is calculated relative to the energy consumption, a renewable share larger 1 is possible in case of overly high renewable gerneation within the system that is later fed into the DSO grid.
    """
    renewable_share = total_res / (total_non_res + total_res)
    return renewable_share


def weighting_for_sector_coupled_kpi(dict_values, kpi_name):
    """
    Calculates the weighted kpi for a specific kpi_name
    :param dict_values:  dict with all project information and results, including KPI_UNCOUPLED_DICT with the specifc kpi_name in question
    :param kpi_name: str with the kpi which should be weighted
    :return: Specific KPI that describes sector-coupled system
    """
    energy_equivalent = 0

    for sector in dict_values["project_data"]["sectors"]:
        if sector in DEFAULT_WEIGHTS_ENERGY_CARRIERS:
            energy_equivalent += (
                dict_values[KPI_DICT][KPI_UNCOUPLED_DICT][kpi_name][sector]
                * DEFAULT_WEIGHTS_ENERGY_CARRIERS[sector]["value"]
            )
        else:
            raise ValueError(
                f"The electricity equivalent value of energy carrier {sector} is not defined. "
                f"Please add this information to the variable DEFAULT_WEIGHTS_ENERGY_CARRIERS in constants.py."
            )

        dict_values[KPI_DICT][KPI_SCALARS_DICT].update({kpi_name: energy_equivalent})
    return
