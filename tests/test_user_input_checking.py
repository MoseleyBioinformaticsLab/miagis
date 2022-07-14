# -*- coding: utf-8 -*-
import pytest

import os
import pathlib

from jsonschema import ValidationError
from contextlib import nullcontext as does_not_raise

from miagis.user_input_checking import load_json, validate_arbitrary_schema, read_in_resource_properties
from miagis.user_input_checking import additional_args_checks, additional_json_schemas_checks


TESTING_DIR = "test_dir"


@pytest.fixture
def test_json():
    return {
              "affiliations": [
                "kentucky"
              ],
              "cc_email": [],
              "cutoff_year": 2019,
              "email_subject": "New PubMed Publications",
              "email_template": "Hey <author_first_name>,\n\nThese are the publications I was able to find on PubMed. Are any missing?\n\n<total_pubs>\n\nKind regards,\n\nThis email was sent by an automated service. If you have any questions or concerns please email my creator ptth222@uky.edu",
              "from_email": "ptth222@uky.edu",
              "grants": [
                "P42ES007380",
                "P42 ES007380"
              ]
            }


def test_load_json_error():
    path = os.path.join("tests", "testing_files", "load_json_error")
    
    with pytest.raises(BaseException):
        load_json(path)


def test_load_json_no_error(test_json):
    
    path = os.path.join("tests", "testing_files", "config.json")
    
    data = load_json(path)
    
    assert data == test_json
    
    
def test_load_json_no_path():
    path = os.path.join("tests", "testing_files", "asdf.asdf")
    
    with pytest.raises(SystemExit):
        load_json(path)




## Commenting $schema out because the jsonschema package produces warnings if left in. It is a known issue in their package. 10-18-2021
@pytest.fixture
def test_schema():
    schema = {
#     "$schema": "https://json-schema.org/draft/2020-12/schema",
     "title": "Test Schema",
     "description": "Schema to test tracker_validate",
     
     "type": "object",
     "minProperties":1,
     "properties": {
             "required_test":{"type": "object",
                              "properties": {"required_test": {"type": "string"}},
                              "required": ["required_test"]},
             "max_length_test":{"type": "string", "maxLength":2},
             "empty_string_test": {"type": "string", "minLength": 1},
             "empty_list_test": {"type": "array", "minItems":1},
             "wrong_type_test": {"type": "string"}, 
             "wrong_list_type": {"type":["string", "array"]},
             "enum_test": {"type":"string", "enum":["asdf"]},
             "other_error_type": {"type": "number", "exclusiveMaximum":100}
             },
     "required": ["required_test"]
             
    }
     
    return schema


@pytest.mark.parametrize("instance, error_message", [
        
        ({}, "ValidationError: An error was found in the Test Schema.\nThe entry [] cannot be empty."),
        ({"asdf":"asdf"}, "ValidationError: An error was found in the Test Schema.\nThe required property \'required_test\' is missing."),
        ({"required_test":{"asdf":"asdf"}}, "ValidationError: An error was found in the Test Schema.\nThe entry [\'required_test\'] is missing the required property \'required_test\'."),
        ({"required_test":{"required_test":""}, "max_length_test":"asdf"}, "ValidationError: An error was found in the Test Schema.\nThe value for ['max_length_test'] is too long."),
        ({"required_test":{"required_test":""}, "empty_string_test":""}, "ValidationError: An error was found in the Test Schema.\nThe value for ['empty_string_test'] cannot be an empty string."),
        ({"required_test":{"required_test":""}, "empty_list_test":[]}, "ValidationError: An error was found in the Test Schema.\nThe value for ['empty_list_test'] cannot be empty."),
        ({"required_test":{"required_test":""}, "wrong_list_type":{}}, "ValidationError: An error was found in the Test Schema.\nThe value for ['wrong_list_type'] is not any of the allowed types: ['string', 'array']."),
        ({"required_test":{"required_test":""}, "wrong_type_test":123}, "ValidationError: An error was found in the Test Schema.\nThe value for ['wrong_type_test'] is not of type \"string\"."),
        ({"required_test":{"required_test":""}, "enum_test":"qwer"}, "ValidationError: An error was found in the Test Schema.\nThe value for ['enum_test'] is not one of ['asdf']."),
        ])


def test_validate_arbitrary_schema(instance, test_schema, error_message, capsys):
        
    with pytest.raises(SystemExit):
        validate_arbitrary_schema(instance, test_schema)
    captured = capsys.readouterr()
    assert captured.out == error_message + "\n"


def test_validate_arbitrary_schema_other_errors(test_schema, capsys):
    
    instance = {"required_test":{"required_test":""}, "other_error_type":1000}
    
    with pytest.raises(ValidationError):
        validate_arbitrary_schema(instance, test_schema)
        

def test_validate_arbitrary_schema_no_error(test_schema):
    with does_not_raise():
        validate_arbitrary_schema({"required_test":{"required_test":""}}, test_schema)




def test_read_in_resource_properties_wrong_file_type():
    with pytest.raises(SystemExit):
        read_in_resource_properties("asdf.asdf", False)
        
def test_read_in_resource_properties_no_resource_name_column():
    with pytest.raises(SystemExit):
        read_in_resource_properties(pathlib.Path("tests", "testing_files", "resource_properties_missing_column.csv").as_posix(), False)


@pytest.fixture
def resource_properties_exact_match():
    resource_properties = {'PFAS_sampling_and_purchasing_and_intake_detail': {'location': 'https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer',
      'alternate_locations': [],
      'creator': [{'name': 'Kentucky Department of Environmental Protection',
        'type': 'organization'}],
      'sources': ['https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf'],
      'fairness': 'FAIR',
      'format': 'web',
      'type': 'layer',
      'description': 'List of all water systems in which PFAS were sampled.',
      'geographical_area': 'Kentucky'},
     'Ohio_River_Marinas_WFL1 - Ohio River': {'location': 'https://services8.arcgis.com/Xcpl3GIMvkCI3oFI/arcgis/rest/services/Ohio_River_Marinas_WFL1/FeatureServer',
      'alternate_locations': ['https://www.arcgis.com/home/item.html?id=bfb75bf75ca441778c4be87e23094527',
       'https://uky-edu.maps.arcgis.com/home/item.html?id=6913699f89454bcdb86441fa14dd90cc'],
      'creator': [{'name': 'Ohio River Valley Water Sanitation Commision',
        'type': 'organization'}],
      'sources': [],
      'fairness': 'Fir',
      'format': 'web',
      'type': 'layer',
      'description': 'Publicly available layer findable on ArcGIS Online.',
      'geographical_area': 'Kentucky'}}
    
    return resource_properties

def test_read_in_resource_properties_exact_matching_true(resource_properties_exact_match):
    properties, mapping = read_in_resource_properties(pathlib.Path("tests","testing_files", "resource_properties.csv").as_posix(), True)
    
    assert properties == resource_properties_exact_match
    assert mapping == {'PFAS_sampling_and_purchasing_and_intake_detail': 'PFAS_sampling_and_purchasing_and_intake_detail',
     'Ohio_River_Marinas_WFL1 - Ohio River': 'Ohio_River_Marinas_WFL1 - Ohio River'}
    

@pytest.fixture
def resource_properties_fuzzy_match():
    resource_properties = {'pfas_sampling_and_purchasing_and_intake_detail': {'location': 'https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer',
      'alternate_locations': [],
      'creator': [{'name': 'Kentucky Department of Environmental Protection',
        'type': 'organization'}],
      'sources': ['https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf'],
      'fairness': 'FAIR',
      'format': 'web',
      'type': 'layer',
      'description': 'List of all water systems in which PFAS were sampled.',
      'geographical_area': 'Kentucky'},
     'ohio_river_marinas_wfl1_-_ohio_river': {'location': 'https://services8.arcgis.com/Xcpl3GIMvkCI3oFI/arcgis/rest/services/Ohio_River_Marinas_WFL1/FeatureServer',
      'alternate_locations': ['https://www.arcgis.com/home/item.html?id=bfb75bf75ca441778c4be87e23094527',
       'https://uky-edu.maps.arcgis.com/home/item.html?id=6913699f89454bcdb86441fa14dd90cc'],
      'creator': [{'name': 'Ohio River Valley Water Sanitation Commision',
        'type': 'organization'}],
      'sources': [],
      'fairness': 'Fir',
      'format': 'web',
      'type': 'layer',
      'description': 'Publicly available layer findable on ArcGIS Online.',
      'geographical_area': 'Kentucky'}}
    
    return resource_properties

def test_read_in_resource_properties_exact_matching_false(resource_properties_fuzzy_match):
    properties, mapping = read_in_resource_properties(pathlib.Path("tests","testing_files", "resource_properties.csv").as_posix(), False)
    
    assert properties == resource_properties_fuzzy_match
    assert mapping == {'pfas_sampling_and_purchasing_and_intake_detail': 'PFAS_sampling_and_purchasing_and_intake_detail',
     'ohio_river_marinas_wfl1_-_ohio_river': 'Ohio_River_Marinas_WFL1 - Ohio River'}
    
def test_read_in_resource_properties_xlsx(resource_properties_fuzzy_match):
    properties, mapping = read_in_resource_properties(pathlib.Path("tests","testing_files", "resource_properties.xlsx").as_posix(), False)
    
    assert properties == resource_properties_fuzzy_match
    assert mapping == {'pfas_sampling_and_purchasing_and_intake_detail': 'PFAS_sampling_and_purchasing_and_intake_detail',
     'ohio_river_marinas_wfl1_-_ohio_river': 'Ohio_River_Marinas_WFL1 - Ohio River'}
    
def test_read_in_resource_properties_json(resource_properties_fuzzy_match):
    properties, mapping = read_in_resource_properties(pathlib.Path("tests","testing_files", "resource_properties.json").as_posix(), False)
    
    assert properties == resource_properties_fuzzy_match
    assert mapping == {'pfas_sampling_and_purchasing_and_intake_detail': 'pfas_sampling_and_purchasing_and_intake_detail',
     'ohio_river_marinas_wfl1_-_ohio_river': 'ohio_river_marinas_wfl1_-_ohio_river'}
    
def test_read_in_resource_properties_creator_mismatch(capsys):
    read_in_resource_properties(pathlib.Path("tests","testing_files", "resource_properties_creator_mismatch.csv").as_posix(), False)
    
    captured = capsys.readouterr()
    assert captured.out == "Warning: Not every creator in \"creator\" has a \"creator_type\" for pfas_sampling_and_purchasing_and_intake_detail in the --resource_properties file.\n"
    
def test_read_in_resource_properties_path_is_none():
    properties, mapping = read_in_resource_properties(None, True)
    
    assert properties == {}
    assert mapping == {}
    


@pytest.mark.parametrize("args, error_message", [
        
        ({"--resource_properties":"asdf", "--base_metadata":"", "--json_schemas":"", "<metadata_json>":""}, "Error: The value entered for --resource_properties is not a valid file path or does not exist."),
        ({"--resource_properties":"", "--base_metadata":"asdf", "--json_schemas":"", "<metadata_json>":""}, "Error: The value entered for --base_metadata is not a valid file path or does not exist."),
        ({"--resource_properties":"", "--base_metadata":"", "--json_schemas":"asdf", "<metadata_json>":""}, "Error: The value entered for --json_schemas is not a valid file path or does not exist."),
        ({"--resource_properties":"", "--base_metadata":"", "--json_schemas":"", "<metadata_json>":"asdf"}, "Error: The value entered for <metadata_json> is not a valid file path or does not exist."),
        ({"--resource_properties":"", "--base_metadata":"", "--json_schemas":"", "<metadata_json>":"", "--entry_version":"asdf"}, "Error: The value entered for --entry_version is not an integer."),
        ({"--resource_properties":"", "--base_metadata":"", "--json_schemas":"", "<metadata_json>":"", "--entry_version":-1}, "Error: The value entered for --entry_version is less than 1."),
        ])


def test_additional_args_checks_errors(args, error_message, capsys):
    with pytest.raises(SystemExit):
        additional_args_checks(args)
    captured = capsys.readouterr()
    assert captured.out == error_message + "\n"

def test_additional_args_checks_passing():
    additional_args_checks({"--resource_properties":"", "--base_metadata":"", "--json_schemas":"", "<metadata_json>":"", "--entry_version":1})




def test_additional_json_schemas_checks_errors(capsys):
    with pytest.raises(SystemExit):
        additional_json_schemas_checks([{"schema":{"asdf"}}])
    captured = capsys.readouterr()
    assert captured.out == "Error: The schema for index 0 in the input JSON schema list is not valid JSON Schema.\n"
    
def test_additional_json_schemas_checks_passing():
    additional_json_schemas_checks([{"schema":{}}])










