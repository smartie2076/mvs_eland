import os

from .constants import REPO_PATH

import src.A1_csv_to_json as load_data_from_csv
import src.B0_data_input_json as data_input
from src.A1_csv_to_json import ALLOWED_FILES

elements = os.path.join(REPO_PATH, "tests", "inputs", "csv")


def test_create_input_json_required_fields_are_filled():
    pass
    #
    # js_file = load_data_from_csv.create_input_json(
    #     input_directory=elements, output_filename="test_example_field.json"
    # )
    # js = data_input.load_json(js_file)
    # for k in js.keys():
    #     assert k in ALLOWED_FILES


def test_load_json_overwrite_output_folder_from_json():
    pass
    # dict_values = data_input.load_json(
    #     os.path.join(elements, "test_example_create.json"), path_output_folder="test"
    # )
    # assert dict_values["simulation_settings"]["path_output_folder"] == "test"
    # assert dict_values["simulation_settings"][
    #     "path_output_folder_inputs"
    # ] == os.path.join("test", "inputs")


def test_load_json_overwrite_input_folder_from_json():
    pass
    # dict_values = data_input.load_json(
    #     os.path.join(elements, "test_example_create.json"), path_input_folder="test"
    # )
    # assert dict_values["simulation_settings"]["path_input_folder"] == "test"


def test_create_json_from_csv_file_not_exist():
    pass


def test_create_json_from_csv_correct_output():
    pass


def teardown_module():
    pass
    # os.remove(os.path.join(elements, "test_example_create.json"))
    # os.remove(os.path.join(elements, "test_example_field.json"))
