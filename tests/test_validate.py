# -*- coding: utf-8 -*-
import pytest

import pathlib
import json

from miagis.validate import validate


@pytest.fixture
def metadata():
    metadata = {
      "format_version": "DRAFT_MIAGIS_VERSION_0.1",
      "entry_version": 1,
      "entry_id": "KY PFAS Paper",
      "date": "2022-07-07",
      "description": "Data used for the paper titled \"A geospatial and binomial logistic regression model to prioritize sampling for per- and polyfluorinated alkyl substances in public water systems\". DOI: https://doi.org/10.1002/ieam.4614",
      "products": [
        "PFAS_detected_sites"
      ],
      "resources": {
        "PFAS_detected_sites": {
          "location": "https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_detected_sites2019/FeatureServer",
          "creator": [
            {
              "name": "Kentucky Department of Environmental Protection",
              "type": "organization"
            }
          ],
          "fairness": "FAIR",
          "format": "web",
          "type": "layer",
          "description": "asdf",
          "geographical_area": "Kentucky",
        },
        "layer_data/PFAS_detected_sites.json": {
          "location": "layer_data/PFAS_detected_sites.json",
          "type": "layer",
          "description": "List of the water systems in which PFAS were detected.",
          "fairness": "FAIR",
          "format": "json",
          "creator": [
            {
              "name": "Kentucky Department of Environmental Protection",
              "type": "organization"
            }
          ],
          "geographical_area": "Kentucky",
          "alternate_locations": [
            "https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_detected_sites2019/FeatureServer"
          ],
          "schema": {
            "asdf": "qwer"
          },
          "fields": {
            "__OBJECTID": {
              "name": "__OBJECTID",
              "type": "int"
            },
            "TYPE": {
              "name": "TYPE",
              "type": "str",
              "identifier":1,
              "identifier%type": "column"
            },
            "WATER_SYSTEM": {
              "name": "WATER_SYSTEM",
              "type": "str"
            },
            "LATITUDE": {
              "name": "LATITUDE",
              "type": "float"
            },
            "LONGITUDE": {
              "name": "LONGITUDE",
              "type": "float"
            },
            "PFAS": {
              "name": "PFAS",
              "type": "float"
            },
            "CODE": {
              "name": "CODE",
              "type": "str"
            }
          }
        }
      }
    }
    return metadata


@pytest.mark.parametrize("instance, error_message", [
        
        ({"resources":{}}, "The value for ['resources'] cannot be empty.\nThe product, PFAS_detected_sites, is not in \"resources\"."),
        ("del metadata['format_version']", "The required property 'format_version' is missing."),
        ("del metadata['entry_id']", "The required property 'entry_id' is missing."),
        ("del metadata['date']", "The required property 'date' is missing."),
        ("del metadata['description']", "The required property 'description' is missing."),
        ("del metadata['products']", "The required property 'products' is missing."),
        ("del metadata['resources']", "The required property 'resources' is missing."),
        ("del metadata['resources']['PFAS_detected_sites']['creator'][0]['name']", "The entry ['resources']['PFAS_detected_sites']['creator'][0] is missing the required property 'name'."),
        ("del metadata['resources']['PFAS_detected_sites']['creator'][0]['type']", "The entry ['resources']['PFAS_detected_sites']['creator'][0] is missing the required property 'type'."),
        ("del metadata['resources']['layer_data/PFAS_detected_sites.json']['fields']['TYPE']['identifier']", "The entry ['resources']['layer_data/PFAS_detected_sites.json']['fields']['TYPE'] is missing the required property 'identifier'."),
        ("del metadata['resources']['layer_data/PFAS_detected_sites.json']['fields']['TYPE']['identifier%type']", "The entry ['resources']['layer_data/PFAS_detected_sites.json']['fields']['TYPE'] is missing the required property 'identifier%type'."),
        ("del metadata['resources']['layer_data/PFAS_detected_sites.json']['fields']['TYPE']['name']", "The entry ['resources']['layer_data/PFAS_detected_sites.json']['fields']['TYPE'] is missing the required property 'name'."),
        ("del metadata['resources']['layer_data/PFAS_detected_sites.json']['fields']['TYPE']['type']", "The entry ['resources']['layer_data/PFAS_detected_sites.json']['fields']['TYPE'] is missing the required property 'type'."),
        ("del metadata['resources']['layer_data/PFAS_detected_sites.json']['fields']", "The entry ['resources']['layer_data/PFAS_detected_sites.json'] is missing the required property 'fields'."),
        ("del metadata['resources']['layer_data/PFAS_detected_sites.json']['type']", "The entry ['resources']['layer_data/PFAS_detected_sites.json'] is missing the required property 'type'."),
        ("del metadata['resources']['layer_data/PFAS_detected_sites.json']['fairness']", "The entry ['resources']['layer_data/PFAS_detected_sites.json'] is missing the required property 'fairness'."),
        ("del metadata['resources']['layer_data/PFAS_detected_sites.json']['format']", "The entry ['resources']['layer_data/PFAS_detected_sites.json'] is missing the required property 'format'."),
        ("del metadata['resources']['layer_data/PFAS_detected_sites.json']['description']", "The entry ['resources']['layer_data/PFAS_detected_sites.json'] is missing the required property 'description'."),
        ({"format_version":""}, "The value for ['format_version'] cannot be an empty string."),
        ("metadata['resources']['PFAS_detected_sites']['alternate_locations']=[]", "The value for ['resources']['PFAS_detected_sites']['alternate_locations'] cannot be empty."),
        ("metadata['resources']['layer_data/PFAS_detected_sites.json']['schema']=1", "The value for ['resources']['layer_data/PFAS_detected_sites.json']['schema'] is not any of the allowed types: ['string', 'object']."),
        ("metadata['resources']['layer_data/PFAS_detected_sites.json']['description']=1", "The value for ['resources']['layer_data/PFAS_detected_sites.json']['description'] is not of type \"string\"."),
        ("metadata['resources']['PFAS_detected_sites']['creator'][0]['type']=\"asdf\"", "The value for ['resources']['PFAS_detected_sites']['creator'][0]['type'] is not one of ['URL', 'organization', 'author', 'DOI']."),
        ({"entry_version":0}, "The value for ['entry_version'] must be greater than or equal to 1."),
        ("metadata['resources']['PFAS_detected_sites']['sources']=[\"asdf\"]", "The source, asdf, for resource, PFAS_detected_sites, does not exist in resources."),
        ("metadata['resources']['layer_data/PFAS_detected_sites.json']['schema']={'properties':'asdf'}", "The \"schema\" field for resource, layer_data/PFAS_detected_sites.json, is not a valid JSON Schema."),
        ("metadata['resources']['layer_data/PFAS_detected_sites.json']['fields']['CODE']['name']='asdf'", "The \"name\" property for field, CODE, for resource, layer_data/PFAS_detected_sites.json, does not match its key value."),
        ])


def test_validate(metadata, instance, error_message, capsys):
    
    if type(instance) == dict:
        metadata.update(instance)
    else:
        exec(instance)
    
    validate(metadata)
    captured = capsys.readouterr()
    assert captured.out == error_message + "\n"
    

def test_validate_no_errors():
    
    with open(pathlib.Path("tests", "testing_files", "GIS_METADATA.json"), "r") as f:
        metadata = json.loads(f.read())
    validate(metadata)











