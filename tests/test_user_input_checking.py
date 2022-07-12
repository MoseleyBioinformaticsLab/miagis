# -*- coding: utf-8 -*-
import pytest

import os

from jsonschema import ValidationError
from contextlib import nullcontext as does_not_raise

from miagis.user_input_checking import load_json, validate_arbitrary_schema


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
        
        ({}, "ValidationError: An error was found in the Test Schema. \nThe entry [] cannot be empty."),
        ({"asdf":"asdf"}, "ValidationError: An error was found in the Test Schema. \nThe required property \'required_test\' is missing."),
        ({"required_test":{"asdf":"asdf"}}, "ValidationError: An error was found in the Test Schema. \nThe entry [\'required_test\'] is missing the required property \'required_test\'."),
        ({"required_test":{"required_test":""}, "max_length_test":"asdf"}, "ValidationError: An error was found in the Test Schema. \nThe value for ['max_length_test'] is too long."),
        ({"required_test":{"required_test":""}, "empty_string_test":""}, "ValidationError: An error was found in the Test Schema. \nThe value for ['empty_string_test'] cannot be an empty string."),
        ({"required_test":{"required_test":""}, "empty_list_test":[]}, "ValidationError: An error was found in the Test Schema. \nThe value for ['empty_list_test'] cannot be empty."),
        ({"required_test":{"required_test":""}, "wrong_list_type":{}}, "ValidationError: An error was found in the Test Schema. \nThe value for ['wrong_list_type'] is not any of the allowed types: ['string', 'array']."),
        ({"required_test":{"required_test":""}, "wrong_type_test":123}, "ValidationError: An error was found in the Test Schema. \nThe value for ['wrong_type_test'] is not of type \"string\"."),
        ({"required_test":{"required_test":""}, "enum_test":"qwer"}, "ValidationError: An error was found in the Test Schema. \nThe value for ['enum_test'] is not one of ['asdf']."),
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



