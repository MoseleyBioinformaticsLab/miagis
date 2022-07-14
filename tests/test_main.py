# -*- coding: utf-8 -*-
import pytest

import pathlib
import os
import time
import copy

from miagis.user_input_checking import load_json


@pytest.fixture(scope="module", autouse=True)
def change_cwd():
    cwd = pathlib.Path.cwd()
    os.chdir(pathlib.Path("tests", "testing_files", "main_dir"))
    yield
    os.chdir(cwd)


metadata_path = pathlib.Path("GIS_METADATA.json")
@pytest.fixture(autouse=True)
def delete_metadata():
    # yield
    if metadata_path.exists():
        os.remove(metadata_path)
        time_to_wait=10
        time_counter = 0
        while metadata_path.exists():
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:
                raise FileExistsError(metadata_path + " was not deleted within " + str(time_to_wait) + " seconds, so it is assumed that it won't be and something went wrong.")

metadata_for_comparison = load_json(pathlib.Path("tests", "testing_files", "main_dir", "GIS_METADATA_for_comparison.json").as_posix())
@pytest.fixture
def metadata_compare():
    return copy.deepcopy(metadata_for_comparison)






def test_normal_build_run(metadata_compare):
    command = "miagis build --resource_properties=resource_properties.csv --base_metadata=base_metadata.json --remove_optional_fields --add_resources"
    os.system(command)
    
    assert metadata_path.exists()
    
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata
    

def test_normal_build_run_no_add_resources(metadata_compare):
    command = "miagis build --resource_properties=resource_properties.csv --base_metadata=base_metadata.json --remove_optional_fields"
    os.system(command)
    
    assert metadata_path.exists()
    
    del metadata_compare["resources"]["Combined map"]
    del metadata_compare["resources"]["PFAS_sampling_and_purchasing_and_intake_detail"]
    del metadata_compare["resources"]["https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf"]
    
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata


def test_normal_build_run_no_remove_fields(metadata_compare):
    command = "miagis build --resource_properties=resource_properties.csv --base_metadata=base_metadata.json --add_resources"
    os.system(command)
    
    assert metadata_path.exists()
    
    metadata_compare["resources"]["Combined map"]["alternate_locations"] =[]
    metadata_compare["resources"]["https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf"]["alternate_locations"] =[]
    metadata_compare["resources"]["https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf"]["sources"] =[]
        
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata
    

def test_normal_build_run_exact_name_match(metadata_compare):
    command = "miagis build --resource_properties=resource_properties.csv --base_metadata=base_metadata.json --remove_optional_fields --add_resources --exact_name_match"
    os.system(command)
    
    assert metadata_path.exists()
    
    metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.csv"]["description"] = ""
    del metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.csv"]["alternate_locations"]
    del metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.csv"]["creator"]
    del metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.csv"]["sources"]
    del metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.csv"]["geographical_area"]
    
    metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.json"]["description"] = ""
    del metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.json"]["alternate_locations"]
    del metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.json"]["creator"]
    del metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.json"]["sources"]
    del metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.json"]["geographical_area"]
    
    del metadata_compare["resources"]["layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson"]["alternate_locations"][1]
    del metadata_compare["resources"]["layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson"]["alternate_locations"][1]
    
    del metadata_compare["resources"]["PFAS_sampling_and_purchasing_and_intake_detail"]["alternate_locations"][0]
    del metadata_compare["resources"]["PFAS_sampling_and_purchasing_and_intake_detail"]["alternate_locations"][0]
    
    
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata


def test_normal_build_run_overwrite_format(metadata_compare):
    command = "miagis build --resource_properties=resource_properties.csv --base_metadata=base_metadata.json --remove_optional_fields --add_resources --overwrite_format"
    os.system(command)
    
    assert metadata_path.exists()
    
    metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.csv"]["format"] = "web"
    metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.json"]["format"] = "web"
    metadata_compare["resources"]["layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson"]["format"] = "web"
    
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata


def test_normal_build_run_overwrite_fairness(metadata_compare):
    command = "miagis build --resource_properties=resource_properties_different_fairness.xlsx --base_metadata=base_metadata.json --remove_optional_fields --add_resources --overwrite_fairness"
    os.system(command)
    
    assert metadata_path.exists()
    
    metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.csv"]["fairness"] = "asdf"
    metadata_compare["resources"]["layer_data/PFAS sampling and purchasing and intake detail.json"]["fairness"] = "asdf"
    metadata_compare["resources"]["layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson"]["fairness"] = "asdf"
    metadata_compare["resources"]["PFAS_sampling_and_purchasing_and_intake_detail"]["fairness"] = "asdf"
    
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata
    

def test_normal_build_run_schema_list(metadata_compare):
    command = "miagis build --resource_properties=resource_properties.csv --base_metadata=base_metadata.json --remove_optional_fields --add_resources --json_schemas=schema_list.json"
    os.system(command)
    
    assert metadata_path.exists()
    
    del metadata_compare["resources"]["layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson"]["fields"]
    
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata
    
    
def test_normal_build_run_entry_version_override(metadata_compare):
    command = "miagis build --resource_properties=resource_properties.csv --base_metadata=base_metadata.json --remove_optional_fields --add_resources --entry_version=5"
    os.system(command)
    
    assert metadata_path.exists()
    
    metadata_compare["entry_version"] = 5
    
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata
    

def test_normal_build_run_entry_id_override(metadata_compare):
    command = "miagis build --resource_properties=resource_properties.csv --base_metadata=base_metadata.json --remove_optional_fields --add_resources --entry_id=asdf"
    os.system(command)
    
    assert metadata_path.exists()
    
    metadata_compare["entry_id"] = "asdf"
    
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata
    

def test_normal_build_run_description_override(metadata_compare):
    command = "miagis build --resource_properties=resource_properties.csv --base_metadata=base_metadata.json --remove_optional_fields --add_resources --description=asdf"
    os.system(command)
    
    assert metadata_path.exists()
    
    metadata_compare["description"] = "asdf"
    
    metadata = load_json(metadata_path.as_posix())
    
    del metadata["date"]
    del metadata_compare["date"]
    
    assert metadata_compare == metadata




