# -*- coding: utf-8 -*-
"""
This module contains the code to build the metadata file.
"""

import pathlib
import datetime
import os
import copy
import json

import fuzzywuzzy
import pandas
import jsonschema

from . import miagis_schema
from . import user_input_checking


def build(file_properties_path, exact_matching, remove_optional_fields, entry_version, entry_id, base_description, products):
    directory = pathlib.Path.cwd()
    
    arcgis_type_map = {"esriFieldTypeOID":"int", "esriFieldTypeString":"str", "esriFieldTypeInteger":"int", 
                       "esriFieldTypeSmallInteger":"int", "esriFieldTypeSingle":"float", "esriFieldTypeDouble":"float",
                       "esriFieldTypeSmallInteger":"int", "esriFieldTypeDate":"int", "typeIdField":"string"}
    
    metadata = {
      "format_version" : "DRAFT_MIAGIS_VERSION_0.1", 
      "entry_version" : entry_version, 
      "entry_id" : entry_id,
      "date" : str(datetime.datetime.now().date()),
      "description" : base_description,
      "products" : products,
      "files" : {}
    }
    
    required_fields = miagis_schema.metadata_schema["properties"]["files"]["additionalProperties"]["then"]["required"]
    
    
    ## If --file_properties was given read in the data.
    file_properties = user_input_checking.read_in_file_properties(file_properties_path, exact_matching)
    file_properties_keys = list(file_properties.keys())
    file_matches_found =[]
        
    
    
    for root, directories, files in os.walk(directory):
        
        ## Only look in subfolders not the cwd.
        if pathlib.Path(root) == directory:
            continue
        
        relative_path = pathlib.Path(root).relative_to(directory).as_posix()
        folder_name = pathlib.Path(root).name
        
        for filename in files:
            extension = pathlib.Path(filename).suffix[1:].lower()
            filename_minus_extension = pathlib.Path(filename).stem
            
            relative_location = pathlib.Path(relative_path, filename).as_posix()
            
            if folder_name == "layer_data" or folder_name == "map_data":
                file_type = "GIS"
            else:
                file_type = ""
                
            if extension == "py":
                extension = "python"
                file_type = "program"
                
            
            metadata["files"][relative_location] = {"location":relative_location,
                                                    "type":file_type,
                                                    "description":"",
                                                    "fairness":"FAIR",
                                                    "format":extension,
                                                    "sources":[{"source":"", "type":""}]}
            
            ## Try to find properties for the file.
            current_file_properties, geographical_area, alternate_locations, matched_filename = find_file_properties(file_properties, file_properties_keys, exact_matching, 
                                                                                                                     filename_minus_extension, relative_location)
            metadata["files"][relative_location].update(current_file_properties)
            if matched_filename:
                file_matches_found.append(matched_filename)
            
            
            ## Try to add layer and maps to the products based on file structure.
            if folder_name == "layer_data":
                if filename_minus_extension in metadata["products"]["layers"]:
                    for location in alternate_locations:
                        if not location in metadata["products"]["layers"][filename_minus_extension]["locations"]:
                            metadata["products"]["layers"][filename_minus_extension]["locations"].append(location)
                else:
                    metadata["products"]["layers"][filename_minus_extension] = {"id":filename_minus_extension, 
                                                                                "locations":alternate_locations, 
                                                                                "geographical_area":geographical_area}
            
            if folder_name == "map_data":
                if filename_minus_extension in metadata["products"]["maps"]:
                    for loation in alternate_locations:
                        if not location in metadata["products"]["maps"][filename_minus_extension]["locations"]:
                            metadata["products"]["maps"][filename_minus_extension]["locations"].append(location)
                else:
                    metadata["products"]["maps"][filename_minus_extension] = {"id":filename_minus_extension,
                                                                              "layers":[],
                                                                              "locations":alternate_locations, 
                                                                              "geographical_area":geographical_area}
            
            ## Determine what kind of file it is and attempt to fill in the types of the fields.
            if extension == "json" or extension == "geojson" or extension == "csv" or extension == "xlsx":
                
                path_to_read_file = pathlib.Path(root, filename)
                
                ## Fill in the fields for tabular file types.
                if extension == "csv" or extension == "xlsx":                        
                    metadata["files"][relative_location]["fields"] = determine_table_fields(extension, path_to_read_file)
                
                else:
                    input_json = user_input_checking.load_json(path_to_read_file)
                    
                    ## If it isn't geojson or esrijson continue.
                    json_type = ""
                    try:
                        jsonschema.validate(input_json, miagis_schema.geojson_schema)
                        json_type = "geojson"
                    except jsonschema.ValidationError:                
                        try:
                            jsonschema.validate(input_json, miagis_schema.arcgis_schema)
                            json_type = "esrijson"
                        except jsonschema.ValidationError:
                            continue
                    
                    if json_type == "geojson":
                        metadata["files"][relative_location]["schema"] = "https://datatracker.ietf.org/doc/html/rfc7946"
                        
                        json_fields = {}
                        if input_json["type"] == "Feature":
                            if input_json["properties"]:
                                for key, value in input_json["properties"].items():
                                    value_type = type(value)
                                    if value_type == int:
                                        str_type = "int"
                                    elif value_type == float:
                                        str_type = "float"
                                    elif value_type == str:
                                        str_type = "str"
                                    elif value is None:
                                        str_type = "None"
                                    else:
                                        str_type = str(value_type)
                                    
                                    json_fields[key] = {"name":key, "type":str_type}
                        
                        elif input_json["type"] == "FeatureCollection":
                            for feature in input_json["features"]:
                                if feature["properties"]:
                                    for key, value in feature["properties"].items():
                                        value_type = type(value)
                                        if value_type == int:
                                            str_type = "int"
                                        elif value_type == float:
                                            str_type = "float"
                                        elif value_type == str:
                                            str_type = "str"
                                        elif value is None:
                                            str_type = "None"
                                        else:
                                            str_type = str(value_type)
                                            
                                        if key in json_fields and json_fields[key]["type"] != "None":
                                            continue
                                        else:
                                            json_fields[key] = {"name":key, "type":str_type}
                        
                        ## Remove any fields without a type.
                        fields_to_delete = []
                        for field_name, field_properties in json_fields.items():
                            if field_properties["type"] == "None":
                                fields_to_delete.append(field_name)
                                
                        for field_name in fields_to_delete:
                            del json_fields[field_name]
                            
                                            
                        metadata["files"][relative_location]["fields"] = json_fields
                    
                    elif json_type == "esrijson":
                        json_fields = {}
                        fields = input_json["layers"][0]["layerDefinition"]["fields"]
                        for field in fields:
                            if field["type"] in arcgis_type_map:
                                json_fields[field["name"]] = {"name":field["name"], "type":arcgis_type_map[field["type"]]}
                            else:
                                json_fields[field["name"]] = {"name":field["name"], "type":"UNKNOWN"}
                                
                        metadata["files"][relative_location]["fields"] = json_fields
            
            else:
                continue
            
            
    ## If --file_properties was given then look for any unmatched and assume they are online only and add to files and layers.
    for file_name in file_properties:
        if not file_name in file_matches_found:
            
            if "alternate_locations" in file_properties[file_name]:
                locations = copy.copy(file_properties[file_name]["alternate_locations"])
            else:
                locations = []
            
            ## Add to layers
            if "geographical_area" in file_properties[file_name] and file_properties[file_name]["geographical_area"]:
                metadata["products"]["layers"][file_name] = {"id":file_name, 
                                                             "locations":locations, 
                                                             "geographical_area":file_properties[file_name]["geographical_area"]}
            else:
                metadata["products"]["layers"][file_name] = {"id":file_name, 
                                                             "locations":locations}
            
            ## Add to files
            if "alternate_locations" in file_properties[file_name] \
                and file_properties[file_name]["alternate_locations"] \
                and not file_properties[file_name]["alternate_locations"][0] in metadata["files"]:
                
                location = file_properties[file_name]["alternate_locations"][0]
                metadata["files"][location] = {"location":location,
                                               "type":"GIS",
                                               "description":"",
                                               "fairness":"Fir",
                                               "format":"web",
                                               "sources":[{"source":"", "type":""}]}
                del file_properties[file_name]["alternate_locations"][0]
                metadata["files"][location].update(file_properties[file_name])
                    
                    
    ## Remove empty optional fields if the option was used.
    if remove_optional_fields:
        for file in metadata["files"]:
            fields_to_delete = []
            for field, field_value in metadata["files"][file].items():
                if not field in required_fields and not field_value:
                    fields_to_delete.append(field)
            for field in fields_to_delete:
                del metadata["files"][file][field]
            
        
    
    save_path = pathlib.Path(directory, "GIS_METADATA.json")
    with open(save_path, 'w') as outFile:
        print(json.dumps(metadata, indent=2, sort_keys=False), file=outFile)
        



def find_file_properties(file_properties, file_properties_keys, exact_matching, 
                         filename_minus_extension, relative_location):
    """"""
    
    current_file_properties = {}
    matched_filename = ""
    if not exact_matching:
        fuzzy_match_filename = filename_minus_extension.strip()
        fuzzy_match_filename = fuzzy_match_filename.lower()
        fuzzy_match_filename = fuzzy_match_filename.replace(" ", "_")
        
        fuzzy_matches = [layer_name for layer_name in file_properties_keys if fuzzywuzzy.fuzz.ratio(layer_name, fuzzy_match_filename) >= 90]
        if len(fuzzy_matches) == 1:
            current_file_properties = file_properties[fuzzy_matches[0]]
            matched_filename = fuzzy_matches[0]
        elif len(fuzzy_matches) > 1:
            if fuzzy_match_filename in file_properties:
                current_file_properties = file_properties[fuzzy_match_filename]
                matched_filename = fuzzy_match_filename
                
    else:
        if filename_minus_extension in file_properties:
            current_file_properties = file_properties[filename_minus_extension]
            matched_filename = filename_minus_extension
    
    if "geographical_area" in current_file_properties:
        geographical_area = current_file_properties["geographical_area"]
    else:
        geographical_area = ""
        
    if "alternate_locations" in current_file_properties:
        alternate_locations = copy.copy(current_file_properties["alternate_locations"])
    else:
        alternate_locations = []
    if not relative_location in alternate_locations:
        alternate_locations.append(relative_location)
        
    return current_file_properties, geographical_area, alternate_locations, matched_filename



def determine_table_fields(extension, path_to_read_file):
    """"""
    
    if extension == "csv":
        df = pandas.read_csv(path_to_read_file, encoding_errors="ignore")
    else:
        df = pandas.read_excel(path_to_read_file)
        
    ## try to tell if the first row is a header or not.
    ## If there are any headers that are numbers assume there aren't headers.
    has_headers = True
    for header in df.columns:
        try:
            float(header)
            has_headers = False
        except ValueError:
            pass
    
    
    fields_dict = df.dtypes.to_dict()
    
    for field, dtype in fields_dict.items():
        dtype_as_string = str(dtype)
        if "int" in dtype_as_string:
            new_dtype = "int"
        elif "float" in dtype_as_string:
            new_dtype = "float"
        else:
            new_dtype = "str"
            
        fields_dict[field] = new_dtype
    
    fields = {}
    if has_headers:
        for field_name, field_type in fields_dict.items():
            if not df.loc[:, field_name].isna().all():
                fields[field_name] = {"name":field_name, "type":field_type, "identifier":df.columns.get_loc(field_name)+1, "identifier%type":"column"}
    else:
        for field_name, field_type in fields_dict.items():
            if not df.loc[:, field_name].isna().all():
                column_number = df.columns.get_loc(field_name)
                fields[column_number] = {"name":column_number+1, "type":field_type, "identifier":column_number+1, "identifier%type":"column"}
        
    return fields




def determine_json_fields(schema_list, input_json, file_path):
    """"""
    
    schema_properties = {}
    schema_index = 0
    for format_properties in schema_list:
        
        try:
            jsonschema.validate(input_json, format_properties["schema"])
            schema_properties = format_properties
            break
        except jsonschema.ValidationError:
            continue
        
    if not schema_properties:
        return {}, ""
        
        
    if "schema_URL" in schema_properties:
        schema = schema_properties["schema_URL"]
    else:
        schema = schema_properties["schema"]
        
    if schema_properties["style"] == "mapping":
        
        field_path = schema_properties["field_path"]
        try:
            fields = eval("input_json" + field_path)
        except Exception:
            print("Warning: The \"field_path\" for the json format schema at index " + 
                  str(schema_index) + " does not work for file " + file_path 
                  + ". It will have empty \"fields\" in the output.")
            return {}, schema
        
        type_key = schema_properties["type_key"]
        name_key = schema_properties["name_key"]
        type_map = schema_properties["type_map"]
            
        json_fields = {}
        type_already_printed = False
        name_already_printed = False
        for field in fields:
            if not type_key in field:
                if not type_already_printed:
                    print("Warning: The \"type_key\" for the json format schema at index " + 
                          str(schema_index) + " is not in all of the fields for file " + 
                          file_path + ". Some fields may be missing in the output.")
                    type_already_printed = True
                continue
            
            if not name_key in field:
                if not name_already_printed:
                    print("Warning: The \"name_key\" for the json format schema at index " + 
                          str(schema_index) + " is not in all of the fields for file " + 
                          file_path + ". Some fields may be missing in the output.")
                    name_already_printed = True
                continue
                    
            if field[type_key] in type_map:
                json_fields[field[name_key]] = {"name":field[name_key], "type":type_map[field[type_key]]}
            else:
                json_fields[field[name_key]] = {"name":field[name_key], "type":"UNKNOWN"}
                
        return json_fields, schema
        
    
    elif schema_properties["style"] == "testing":
        
        features_path = schema_properties["features_path"]
        try:
            features = eval("input_json" + features_path)
        except Exception:
            print("Warning: The \"features_path\" for the json format schema at index " + 
                  str(schema_index) + " does not work for file " + file_path 
                  + ". It will have empty \"fields\" in the output.")
            return {}, schema
        
        properties_key = schema_properties["properties_key"]
        
        ## This loop assumes that each feature has the same properties and tries to determine the type of each property.
        ## It does not enforce features to have all the same properties. It simply accumulates all features it sees.
        ## Also assumes that any property will only have one type, so the first type seen is kept and not checked or overwritten except for None.
        json_fields = {}
        properties_already_printed = False
        for feature in features:
                        
            if not properties_key in feature:
                if not properties_already_printed:
                    print("Warning: The \"properties_key\" for the json format schema at index " + 
                          str(schema_index) + " is not in all of the features for file " + 
                          file_path + ". Some fields may be missing in the output.")
                    properties_already_printed = True
                continue
            
            if feature[properties_key]:
                for key, value in feature[properties_key].items():
                    value_type = type(value)
                    if value_type == int:
                        str_type = "int"
                    elif value_type == float:
                        str_type = "float"
                    elif value_type == str:
                        str_type = "str"
                    elif value is None:
                        str_type = "None"
                    else:
                        str_type = str(value_type)
                        
                    if key in json_fields and json_fields[key]["type"] != "None":
                        continue
                    else:
                        json_fields[key] = {"name":key, "type":str_type}
    
        ## Remove any fields without a type.
        fields_to_delete = []
        for field_name, field_properties in json_fields.items():
            if field_properties["type"] == "None":
                fields_to_delete.append(field_name)
                
        for field_name in fields_to_delete:
            del json_fields[field_name]
            
        return json_fields, schema
        
    else:
        print("Warning: Unknown \"style\" for the json format schema at index " + 
              str(schema_index) + ". The file at " + file_path 
              + " will have empty \"fields\" in the output.")
        return {}, schema
            
            
        


