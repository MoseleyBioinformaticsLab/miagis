# -*- coding: utf-8 -*-
import pytest

import json
import pathlib


from miagis.build import find_resource_properties, determine_table_fields, determine_json_fields
from miagis import miagis_schema


with open(pathlib.Path("tests", "testing_files", "resource_properties.json"), "r") as f:
    resource_properties_file_contents = json.loads(f.read())

@pytest.fixture
def resource_properties():
    return resource_properties_file_contents

def test_find_resource_properties_fuzzy_typical(resource_properties):
    
    del resource_properties["pfas_sampling_and_purchasing_and_intake_detail"]["alternate_locations"]
    
    current_resource_properties, alternate_locations, matched_name = \
    find_resource_properties(resource_properties, list(resource_properties.keys()), 
                             False, "PFAS_sampling_and_purchasing_and_intake detail", 
                             "layer_data\PFAS_sampling_and_purchasing_and_intake detail")
    
    assert current_resource_properties == resource_properties["pfas_sampling_and_purchasing_and_intake_detail"]
    assert alternate_locations == ["https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer",
                                   "layer_data\PFAS_sampling_and_purchasing_and_intake detail"]
    assert matched_name == "pfas_sampling_and_purchasing_and_intake_detail"


def test_find_resource_properties_fuzzy_multiple_matches(resource_properties):
    
    resource_properties["pfas_sampling_and_purchasing_and_intake detail"] = {}
    
    current_resource_properties, alternate_locations, matched_name = \
    find_resource_properties(resource_properties, list(resource_properties.keys()), 
                             False, "pfas_sampling_and_purchasing_and_intake_detail", 
                             "layer_data\pfas_sampling_and_purchasing_and_intake_detail")
    
    assert current_resource_properties == resource_properties["pfas_sampling_and_purchasing_and_intake_detail"]
    assert alternate_locations == ["https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer",
                                   "layer_data\pfas_sampling_and_purchasing_and_intake_detail"]
    assert matched_name == "pfas_sampling_and_purchasing_and_intake_detail"


def test_find_resource_properties_exact_match(resource_properties):
    
    resource_properties["PFAS_sampling_and_purchasing_and_intake detail"] = \
    resource_properties["pfas_sampling_and_purchasing_and_intake_detail"]
    del resource_properties["pfas_sampling_and_purchasing_and_intake_detail"]
    
    current_resource_properties, alternate_locations, matched_name = \
    find_resource_properties(resource_properties, list(resource_properties.keys()), 
                             True, "PFAS_sampling_and_purchasing_and_intake detail", 
                             "layer_data\PFAS_sampling_and_purchasing_and_intake detail")
    
    assert current_resource_properties == resource_properties["PFAS_sampling_and_purchasing_and_intake detail"]
    assert alternate_locations == ["https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer",
                                   "layer_data\PFAS_sampling_and_purchasing_and_intake detail"]
    assert matched_name == "PFAS_sampling_and_purchasing_and_intake detail"



def test_determine_table_fields_csv_headers():
    fields = determine_table_fields("csv", pathlib.Path("tests", "testing_files", "fields_with_headers.csv"))
    
    expected = {'FID': {'name': 'FID',
      'type': 'int',
      'identifier': 1,
      'identifier%type': 'column'},
     'OBJECTID': {'name': 'OBJECTID',
      'type': 'int',
      'identifier': 2,
      'identifier%type': 'column'},
     'WWD_NO': {'name': 'WWD_NO',
      'type': 'int',
      'identifier': 3,
      'identifier%type': 'column'},
     'PWSID': {'name': 'PWSID',
      'type': 'str',
      'identifier': 4,
      'identifier%type': 'column'}}
    
    assert fields == expected
    
def test_determine_table_fields_xlsx_no_headers():
    fields = determine_table_fields("xlsx", pathlib.Path("tests", "testing_files", "fields_without_headers.xlsx"))
    
    expected = {1: {'name': 1, 'type': 'int', 'identifier': 1, 'identifier%type': 'column'},
     2: {'name': 2, 'type': 'int', 'identifier': 2, 'identifier%type': 'column'},
     3: {'name': 3, 'type': 'int', 'identifier': 3, 'identifier%type': 'column'},
     4: {'name': 4, 'type': 'str', 'identifier': 4, 'identifier%type': 'column'}}
    
    assert fields == expected




@pytest.fixture
def schema_list():
    arcgis_type_map = {"esriFieldTypeOID":"int", "esriFieldTypeString":"str", "esriFieldTypeInteger":"int", 
                       "esriFieldTypeSmallInteger":"int", "esriFieldTypeSingle":"float", "esriFieldTypeDouble":"float",
                       "esriFieldTypeSmallInteger":"int", "esriFieldTypeDate":"int", "typeIdField":"string"}
    
    schema_list = []
    
    schema_list.append({"name":"In-built ESRI", "style":"mapping", "schema":miagis_schema.arcgis_schema, 
                    "field_path":'["layers"][0]["layerDefinition"]["fields"]', 
                    "name_key":"name", "type_key":"type", "type_map":arcgis_type_map})
    schema_list.append({"name":"In-built GEOJSON Single Feature", "style":"testing", "schema":miagis_schema.geojson_feature_schema, 
                        "features_path":"", "properties_key":"properties", "schema_URL":"https://datatracker.ietf.org/doc/html/rfc7946"})
    schema_list.append({"name":"In-built GEOJSON Collection", "style":"testing", "schema":miagis_schema.geojson_collection_schema, 
                        "features_path":'["features"]', "properties_key":"properties", "schema_URL":"https://datatracker.ietf.org/doc/html/rfc7946"})

    return schema_list



def test_determine_json_fields_geojson(schema_list):
    with open(pathlib.Path("tests", "testing_files", "water_district.geojson"), "r") as f:
        water_district = json.loads(f.read())
    
    fields, schema = determine_json_fields(schema_list, water_district, "file_path")
    
    expected_fields = {'F__OBJECTID': {'name': 'F__OBJECTID', 'type': 'int'},
      'AI_Name': {'name': 'AI_Name', 'type': 'str'},
      'Longitude': {'name': 'Longitude', 'type': 'float'},
      'Latitude': {'name': 'Latitude', 'type': 'float'},
      'Superfund_Site_Type': {'name': 'Superfund_Site_Type', 'type': 'str'}}
    
    expected_schema = 'https://datatracker.ietf.org/doc/html/rfc7946'
    
    assert fields == expected_fields
    assert schema == expected_schema
    

def test_determine_json_fields_esrijson(schema_list):
    with open(pathlib.Path("tests", "testing_files", "water_district.json"), "r") as f:
        water_district = json.loads(f.read())
    
    fields, schema = determine_json_fields(schema_list, water_district, "file_path")
    
    expected_fields = {'__OBJECTID': {'name': '__OBJECTID', 'type': 'int'},
     'AI_ID': {'name': 'AI_ID', 'type': 'str'},
     'AI_Name': {'name': 'AI_Name', 'type': 'str'},
     'SI_County': {'name': 'SI_County', 'type': 'str'},
     'Not_Com#': {'name': 'Not_Com#', 'type': 'str'},
     'SI_Decription': {'name': 'SI_Decription', 'type': 'str'},
     'Regulatory_Desc': {'name': 'Regulatory_Desc', 'type': 'str'},
     'Site_Status': {'name': 'Site_Status', 'type': 'str'},
     'Closure_Option': {'name': 'Closure_Option', 'type': 'str'},
     'Closure_Dt': {'name': 'Closure_Dt', 'type': 'str'},
     'Longitude': {'name': 'Longitude', 'type': 'float'},
     'Latitude': {'name': 'Latitude', 'type': 'float'},
     'SI_Addr_Line_1': {'name': 'SI_Addr_Line_1', 'type': 'str'},
     'SI_Addr_Line_2': {'name': 'SI_Addr_Line_2', 'type': 'str'},
     'Superfund_Site_Type': {'name': 'Superfund_Site_Type', 'type': 'str'},
     'Risk_Score': {'name': 'Risk_Score', 'type': 'str'}}
    
    expected_schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema',
     'title': 'In-built ESRI',
     'type': 'object',
     'properties': {'layers': {'type': 'array',
       'items': {'type': 'object',
        'properties': {'layerDefinition': {'type': 'object',
          'properties': {'fields': {'type': 'array',
            'items': {'type': 'object',
             'properties': {'name': {'type': 'string'},
              'type': {'type': 'string'}},
             'required': ['name', 'type']}}},
          'required': ['fields']}},
        'required': ['layerDefinition']}}},
     'required': ['layers']}
    
    assert fields == expected_fields
    assert schema == expected_schema


def test_determine_json_fields_no_match(schema_list):
    fields, schema = determine_json_fields(schema_list, {"asdf":"asdf"}, "file_path")
    
    assert fields == {}
    assert schema == ""
    
def test_determine_json_fields_bad_field_path(schema_list, capsys):
    with open(pathlib.Path("tests", "testing_files", "water_district.json"), "r") as f:
        water_district = json.loads(f.read())
        
    schema_list[0]["field_path"] = "['asdf']"
    fields, schema = determine_json_fields(schema_list, water_district, "file_path")
    captured = capsys.readouterr()

    assert captured.out == "Warning: The \"field_path\", ['asdf'], for the \"In-built ESRI\" json format schema does not work for file file_path. It will have an empty \"fields\" in the output." + "\n"

def test_determine_json_fields_bad_type_key(schema_list, capsys):
    with open(pathlib.Path("tests", "testing_files", "water_district.json"), "r") as f:
        water_district = json.loads(f.read())
        
    schema_list[0]["type_key"] = "asdf"
    fields, schema = determine_json_fields(schema_list, water_district, "file_path")
    captured = capsys.readouterr()

    assert captured.out == "Warning: The \"type_key\", asdf, for the \"In-built ESRI\" json format schema is not in all of the fields for file file_path. Some fields may be missing in the output." + "\n"

def test_determine_json_fields_bad_name_key(schema_list, capsys):
    with open(pathlib.Path("tests", "testing_files", "water_district.json"), "r") as f:
        water_district = json.loads(f.read())
        
    schema_list[0]["name_key"] = "asdf"
    fields, schema = determine_json_fields(schema_list, water_district, "file_path")
    captured = capsys.readouterr()

    assert captured.out == "Warning: The \"name_key\", asdf, for the \"In-built ESRI\" json format schema is not in all of the fields for file file_path. Some fields may be missing in the output." + "\n"

def test_determine_json_fields_bad_features_path(schema_list, capsys):
    with open(pathlib.Path("tests", "testing_files", "water_district.geojson"), "r") as f:
        water_district = json.loads(f.read())
        
    schema_list[2]["features_path"] = "['asdf']"
    fields, schema = determine_json_fields(schema_list, water_district, "file_path")
    captured = capsys.readouterr()

    assert captured.out == "Warning: The \"features_path\", ['asdf'] for the \"In-built GEOJSON Collection\" json format schema does not work for file file_path. It will have empty \"fields\" in the output." + "\n"

def test_determine_json_fields_features_path_wrong_type(schema_list, capsys):
    with open(pathlib.Path("tests", "testing_files", "water_district.geojson"), "r") as f:
        water_district = json.loads(f.read())
        
    water_district["features"] = "asdf"
    del schema_list[2]["schema"]["properties"]["features"]
    fields, schema = determine_json_fields(schema_list, water_district, "file_path")
    captured = capsys.readouterr()

    assert captured.out == "Warning: The \"features_path\", [\"features\"] for the \"In-built GEOJSON Collection\" json format schema does not lead to the appropriate type (list or dict) for file file_path. It will have empty \"fields\" in the output." + "\n"

def test_determine_json_fields_bad_properties_key(schema_list, capsys):
    with open(pathlib.Path("tests", "testing_files", "water_district.geojson"), "r") as f:
        water_district = json.loads(f.read())
        
    del water_district["features"][0]["properties"]
    fields, schema = determine_json_fields(schema_list, water_district, "file_path")
    captured = capsys.readouterr()

    assert captured.out == "Warning: The \"properties_key\", properties for the \"In-built GEOJSON Collection\" json format schema is not in all of the features for file file_path. Some fields may be missing in the output." + "\n"

def test_determine_json_fields_bad_style(schema_list, capsys):
    with open(pathlib.Path("tests", "testing_files", "water_district.geojson"), "r") as f:
        water_district = json.loads(f.read())
    
    schema_list[2]["style"] = "asdf"
    fields, schema = determine_json_fields(schema_list, water_district, "file_path")
    captured = capsys.readouterr()

    assert captured.out == "Warning: Unknown \"style\", asdf for the \"In-built GEOJSON Collection\" json format. The file at file_path will have empty \"fields\" in the output." + "\n"


