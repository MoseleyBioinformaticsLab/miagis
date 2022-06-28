# -*- coding: utf-8 -*-
"""
This module contains the JSON schema used to validate various inputs and outputs.
"""



## This could crank down harder, but it should be enough to be confident we are looking at geojson.
geojson_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    
    "type":"object",
    "properties":{
        "type":{"type":"string", "enum":["Feature", "FeatureCollection"]},
        "features":{"type":"array", 
                    "items":{"type":"object",
                             "properties":{
                                 "type":{"type":"string", "enum":["Feature"]},
                                 "properties":{"type":["object", "null"]},
                                 "geometry":{"type":["null", "object"]}},
                             "required":["type", "properties", "geometry"]}}},
    "required":["type"],
    "if":{"properties":{"type":{"const":"Feature"}}},
    "then":{
        "additionalProperties":{
            "type":"object",
            "properties":{
                "type":{"type":"string", "enum":["Feature"]},
                "properties":{"type":["object", "null"]},
                "geometry":{"type":["null", "object"]}},
            "required":["type", "properties", "geometry"]}}}

geojson_feature_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    
    "type":"object",
    "properties":{
        "type":{"type":"string", "enum":["Feature"]},
        "properties":{"type":["object", "null"]},
        "geometry":{"type":["null", "object"]}},
    "required":["type", "properties", "geometry"]
    }

geojson_collection_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    
    "type":"object",
    "properties":{
        "type":{"type":"string", "enum":["FeatureCollection"]},
        "features":{"type":"array", 
                    "items":{"type":"object",
                             "properties":{
                                 "type":{"type":"string", "enum":["Feature"]},
                                 "properties":{"type":["object", "null"]},
                                 "geometry":{"type":["null", "object"]}},
                             "required":["type", "properties", "geometry"]}}},
    "required":["type", "features"],
    }

## This is an abbreviated schema that should be enough to check if the JSON is the format we are looking for.
arcgis_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    
    "type":"object",
    "properties":{
        "layers":{"type":"array", 
                  "items":{"type":"object",
                           "properties":{
                               "layerDefinition":{"type":"object",
                                                  "properties":{
                                                      "fields":{"type":"array",
                                                                "items":{"type":"object",
                                                                         "properties":{
                                                                             "name":{"type":"string"},
                                                                             "type":{"type":"string"}},
                                                                         "required":["name","type"]}}},
                                                  "required":["fields"]}},
                           "required":["layerDefinition"]}},},
    "required":["layers"]}




metadata_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    
    "type":"object",
    "properties":{
        "format_version":{"type":"string", "minLength":1},
        "entry_version":{"type":"integer", "minimum":1},
        "entry_id":{"type":"string", "minLength":1},
        "date":{"type":"string", "minLength":1},
        "description":{"type":"string", "minLength":1},
        "products":{"type":"object", 
                    "properties":{
                        "maps":{"type":"object",
                                "additionalProperties":{"type":"object",
                                                        "minProperties":1,
                                                        "properties":{
                                                            "id":{"type":"string", "minLength":1},
                                                            "geographical_area":{"type":"string", "minLength":1},
                                                            "layers":{"type":"array", "minItems":1, "items":{"type":"string", "minLength":1}},
                                                            "locations":{"type":"array", "minItems":1, "items":{"type":"string", "minLength":1}}},
                                                        "required":["id", "layers", "locations"]}},
                        "layers":{"type":"object",
                                  "additionalProperties":{"type":"object",
                                                          "minProperties":1,
                                                          "properties":{
                                                              "id":{"type":"string", "minLength":1},
                                                              "geographical_area":{"type":"string", "minLength":1},
                                                              "locations":{"type":"array", "minItems":1, "items":{"type":"string", "minLength":1}}},
                                                          "required":["id", "locations"]}},
                        "others":{"type":"object",
                                  "additionalProperties":{"type":"object",
                                                          "minProperties":1,
                                                          "properties":{
                                                              "id":{"type":"string", "minLength":1},
                                                              "geographical_area":{"type":"string", "minLength":1},
                                                              "locations":{"type":"array", "minItems":1, "items":{"type":"string", "minLength":1}}},
                                                          "required":["id",  "locations"]}}},
                    "required":["maps", "layers"]},
        "files":{"type":"object",
                 "minProperties":1,
                 "additionalProperties":{"type":"object",
                                         "properties":{
                                             "location":{"type":"string", "minLength":1},
                                             "alternate_locations":{"type":"array", "items":{"type":"string", "minLength":1}},
                                             "type":{"type":"string", "minLength":1},
                                             "fairness":{"type":"string", "pattern":"(?i)^f?a?i?r?$"},
                                             "format":{"type":"string", "minLength":1},
                                             "schema":{"type":["string", "object"], "minLength":1},
                                             "sources":{"type":"array", "minItems":1, "items":{"type":"object",
                                                                                               "properties":{
                                                                                                   "source":{"type":"string", "minLength":1},
                                                                                                   "type":{"type":"string", "minLength":1, "enum":["URL", "organization", "author", "DOI", "file"]}},
                                                                                               "required":["source", "type"]}},
                                             "fields":{"type":"object",
                                                       "minProperties":1,
                                                       "additionalProperties":{"type":"object",
                                                                               "properties":{
                                                                                   "name":{"type":"string", "minLength":1},
                                                                                   "type":{"type":"string", "enum":["ontology_term", "int", "float", "str"]},
                                                                                   "identifier":{"type":["string", "integer"], "minLength":1},
                                                                                   "identifier%type":{"type":"string", "minLength":1}},
                                                                               "required":["name", "type"]}}},
                                         "if":{"anyOf":[
                                                 {"properties":{"type":{"anyOf":[{"const":"program"},
                                                                                 {"const":"other"}]}}},
                                                 {"properties":{"schema":{"type":"string", "minLength":1}},
                                                  "required":["schema"]},
                                                 {"properties":{"format":{"const":"web"}}}]},
                                         "then":{"required":["location", "type", "fairness", "format", "sources"]},
                                         "else":{"required":["location", "type", "fairness", "format", "sources", "fields"]}}},
        },
    "required":["format_version", "entry_version", "entry_id", "date", "description", "products", "files"]}



args_schema = {
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "title": "CLI inputs",
 
 "type":"object",
 "properties":{
     "--file_properties":{"type":["string", "null"], "minLength":1},
     "--entry_id":{"type":["string", "null"], "minLength":1},
     "--description":{"type":["string", "null"], "minLength":1},
     "--base_metadata":{"type":["string", "null"], "minLength":1},
     "--products":{"type":["string", "null"], "minLength":1},},
 }


base_metadata_dict = {"entry_version":1, "entry_id":"", "description":"", "products":{"maps":{}, "layers":{}}}

base_schema = {
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "title": "base metadata",
 
 "type":"object",
 "properties":{},
 }

for base_key in base_metadata_dict:
    base_schema["properties"][base_key] = metadata_schema["properties"][base_key]




schema_list_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "JSON Schemas List",
    
    "type":"array",
    "items":{"type":"object",
             "properties":{
                 "style":{"type":"string", "enum":["testing", "mapping"]},
                 "schema":{"type":"object"},
                 "schema_URL":{"type":"string", "minLength":1},
                 
                 "field_path":{"type":"string", "minLength":1},
                 "name_key":{"type":"string", "minLength":1},
                 "type_key":{"type":"string", "minLength":1},
                 "type_map":{"type":"object", "minProperties":1},
                 
                 "features_path":{"type":"string"},
                 "properties_key":{"type":"string", "minLength":1}},
             "required":["schema", "style"],
             "allOF":[
                 {"if":{"properties":{"style":{"const":"mapping"}}},
                 "then":{"required":["field_path", "name_key", "type_key", "type_map"]},},
                 {"if":{"properties":{"style":{"const":"testing"}}},
                 "then":{"required":["features_path", "properties_key"]}}
                 ]
             }
    
    }









