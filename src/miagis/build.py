# -*- coding: utf-8 -*-
"""
This module contains the code to build the metadata file.
"""

import pathlib
import datetime
import os
import copy
import json

import fuzzywuzzy.fuzz
import pandas
import jsonschema

from . import miagis_schema
from . import user_input_checking


def build(resource_properties_path, exact_matching=False, remove_optional_fields=True, 
          add_resources=True, overwrite_format=False, overwrite_fairness=False,
          base_metadata={}, entry_version=1, entry_id="", base_description="", products=[], schema_list = []):
    """Build a metadata file from the input settings in the current directory.
    
    Loop over files in the folders of the current directory, ignoring files in 
    the top level of the current directory, and fill in what information can be 
    about the file in the metadata. If resource_properties are provided then resources 
    are matched to those in resource_properties and more information is able to be 
    automatically put into the metadata. 
    
    Args:
        resource_properties_path (str): filepath to a file containing file properties.
        exact_matching (bool): if True file names are matched exactly. if False names are modified and matched fuzzy.
        remove_optional_fields (bool): if True optional metadata fields that are empty or null are removed.
        add_resources (bool): if True add resources that aren't in the metadata after looping over the files to the metadata.
        overwrite_format (bool): if True overwrite the default format determined from the file extension for files with what is in resource_properties.
        overwrite_fairness (bool): if True overwrite the default value of "FAIR" for files with what is in resource_properties.
        base_metadata (dict): update the metadata dict with this input dict.
        entry_version (int): version number of the metadata.
        entry_id (str): unique id for the metadata.
        base_description (str): description of the metadata.
        products (dict): a list of resource ids.
        schema_list (list): a list of dicitonaries with information about how to detect if a JSON file is using that schema, and how to decode that schema to fill in the metadata.
    """
    directory = pathlib.Path.cwd()
    
    ## Add gejson and acrgis json to schema's to look for.
    arcgis_type_map = {"esriFieldTypeOID":"int", "esriFieldTypeString":"str", "esriFieldTypeInteger":"int", 
                       "esriFieldTypeSmallInteger":"int", "esriFieldTypeSingle":"float", "esriFieldTypeDouble":"float",
                       "esriFieldTypeSmallInteger":"int", "esriFieldTypeDate":"int", "typeIdField":"string"}
    
    schema_list.append({"name":"In-built ArcGIS", "style":"mapping", "schema":miagis_schema.arcgis_schema, 
                    "field_path":'["layers"][0]["layerDefinition"]["fields"]', 
                    "name_key":"name", "type_key":"type", "type_map":arcgis_type_map})
    schema_list.append({"name":"In-built GEOJSON Single Feature", "style":"testing", "schema":miagis_schema.geojson_feature_schema, 
                        "features_path":"", "properties_key":"properties", "schema_URL":"https://datatracker.ietf.org/doc/html/rfc7946"})
    schema_list.append({"name":"In-built GEOJSON Collection", "style":"testing", "schema":miagis_schema.geojson_collection_schema, 
                        "features_path":'["features"]', "properties_key":"properties", "schema_URL":"https://datatracker.ietf.org/doc/html/rfc7946"})
    
    ## Initially build the metadata, and then update it with base metadata, and then overwrite values with input arguments if not null.
    metadata = {
      "format_version" : "DRAFT_MIAGIS_VERSION_0.1", 
      "entry_version" : entry_version, 
      "entry_id" : entry_id,
      "date" : str(datetime.datetime.now().date()),
      "description" : base_description,
      "products" : products,
      "resources" : {}
    }
    
    metadata.update(base_metadata)
    if base_description:
        metadata["description"] = base_description
    if entry_version != 1:
        metadata["entry_version"] = entry_version
    if entry_id:
        metadata["entry_id"] = entry_id
    if products:
        metadata["products"] = products
    
    
    ## If --resource_properties was given read in the data.
    resource_properties, resource_original_name_map = user_input_checking.read_in_resource_properties(resource_properties_path, exact_matching)
    resource_properties_keys = list(resource_properties.keys())
    resource_matches = {}
    
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
            
            if folder_name == "layer_data":
                file_type = "layer"
            elif folder_name == "map_data":
                file_type = "map"
            else:
                file_type = ""
                
            if extension == "py":
                extension = "python"
                file_type = "program"
                
            
            metadata["resources"][relative_location] = {"location":relative_location,
                                                    "type":file_type,
                                                    "description":"",
                                                    "fairness":"FAIR",
                                                    "format":extension,}
            
            ## Try to find properties for the file.
            current_resource_properties, alternate_locations, matched_name = find_resource_properties(resource_properties, resource_properties_keys, exact_matching, 
                                                                                                      filename_minus_extension, relative_location)
            
            ## Keep track of what files get matched so the alternate locations can all be updated at the end.
            if matched_name:
                if matched_name in resource_matches:
                    resource_matches[matched_name].append(relative_location)
                else:
                    resource_matches[matched_name] = [relative_location]
                
                metadata["resources"][relative_location].update(current_resource_properties)
                metadata["resources"][relative_location]["location"] = relative_location
                metadata["resources"][relative_location]["alternate_locations"] = alternate_locations
                
                if not overwrite_format:
                    metadata["resources"][relative_location]["format"] = extension
                if not overwrite_fairness:
                    metadata["resources"][relative_location]["fairness"] = "FAIR"
            
                        
            ## Determine what kind of file it is and attempt to fill in the types of the fields.
            if extension == "json" or extension == "geojson" or extension == "csv" or extension == "xlsx":
                
                path_to_read_file = pathlib.Path(root, filename)
                
                ## Fill in the fields for tabular file types.
                if extension == "csv" or extension == "xlsx":                        
                    metadata["resources"][relative_location]["fields"] = determine_table_fields(extension, path_to_read_file)
                
                else:
                    input_json = user_input_checking.load_json(path_to_read_file)
                    
                    json_fields, schema = determine_json_fields(schema_list, input_json, relative_location)
                    
                    if schema:
                        metadata["resources"][relative_location]["schema"] = schema
                        
                    metadata["resources"][relative_location]["fields"] = json_fields
            
            else:
                continue
            
    ## Add all resources to the metadata.
    if add_resources:
        for resource_name in resource_properties:
            if not resource_name in metadata["resources"] and \
                "location" in resource_properties[resource_name] and resource_properties[resource_name]["location"]:
                metadata["resources"][resource_original_name_map[resource_name]] = resource_properties[resource_name]
        
    ## Go through all matches and update alternate_locations so they all reference each other.
    for resource_name in resource_matches:
        total_list = resource_matches[resource_name]
        if resource_name in metadata["resources"]:
            total_list.append(resource_original_name_map[resource_name])
        
        all_locations = set()
        for name in total_list:
            all_locations.add(metadata["resources"][name]["location"])
            if "alternate_locations" in metadata["resources"][name]:
                for location in metadata["resources"][name]["alternate_locations"]:
                    all_locations.add(location)
        all_locations = list(all_locations)
            
        for name in total_list:
            metadata["resources"][name]["alternate_locations"] = [location for location in all_locations if location != metadata["resources"][name]["location"]]
                    
                    
    ## Remove empty optional fields if the option was used.
    required_fields = miagis_schema.metadata_schema["properties"]["resources"]["additionalProperties"]["then"]["required"]
    if remove_optional_fields:
        for resource in metadata["resources"]:
            fields_to_delete = []
            for field, field_value in metadata["resources"][resource].items():
                if not field in required_fields and not field_value:
                    fields_to_delete.append(field)
            for field in fields_to_delete:
                del metadata["resources"][resource][field]
            
        
    
    save_path = pathlib.Path(directory, "GIS_METADATA.json")
    with open(save_path, 'w') as outFile:
        print(json.dumps(metadata, indent=2, sort_keys=False), file=outFile)
        



def find_resource_properties(resource_properties, resource_properties_keys, exact_matching, 
                         filename_minus_extension, relative_location):
    """Match filename to an entry in resource_properties and pull out properties.
    
    The point of this function is to find the match in resource_properties and format 
    all of the information so it can be easily added to metadata without more logic 
    after returning from this function.
    
    Args:
        resource_properties (dict): dictionary where the keys are filenames and values are properties of the file to go in the metadata.
        resource_properties_keys (list): list of the resource_properties_keys, it is given as an input so the list isn't created every time the function runs.
        exact_matching (bool): if True filename is matched as is, if False the filename is stripped, lowered, and spaces replaced with underscores before matching
        filename_mins_extension (str): the filename to match with the extension removed.
        relative_location (str): location of the file relative to the current directory, input here so it can be added to alternate_locations.
        
    Returns:
        current_resource_properties (dict): the properties of the matched filename from resource_properties.
        alternate_locations (list): if alternate_locations is in resource_properties return it, else return an empty list, but always add the relative_location to the list
        matched_name (str): the resource_name in resource_properties that was matched to filename_minus_extension.
    """
    
    current_resource_properties = {}
    matched_name = ""
    if not exact_matching:
        fuzzy_match_filename = filename_minus_extension.strip()
        fuzzy_match_filename = fuzzy_match_filename.lower()
        fuzzy_match_filename = fuzzy_match_filename.replace(" ", "_")
        
        fuzzy_matches = [layer_name for layer_name in resource_properties_keys if fuzzywuzzy.fuzz.ratio(layer_name, fuzzy_match_filename) >= 90]
        if len(fuzzy_matches) == 1:
            current_resource_properties = resource_properties[fuzzy_matches[0]]
            matched_name = fuzzy_matches[0]
        elif len(fuzzy_matches) > 1:
            if fuzzy_match_filename in resource_properties:
                current_resource_properties = resource_properties[fuzzy_match_filename]
                matched_name = fuzzy_match_filename
                
    else:
        if filename_minus_extension in resource_properties:
            current_resource_properties = resource_properties[filename_minus_extension]
           
    if "alternate_locations" in current_resource_properties:
        alternate_locations = copy.copy(current_resource_properties["alternate_locations"])
    else:
        alternate_locations = []
    if not relative_location in alternate_locations:
        alternate_locations.append(relative_location)
    if "location" in current_resource_properties and current_resource_properties["location"] and \
        not current_resource_properties["location"] in alternate_locations:
        alternate_locations.append(current_resource_properties["location"])
        
    return current_resource_properties, alternate_locations, matched_name



def determine_table_fields(extension, path_to_read_file):
    """Read in the tabular file and determine the names and types of the columns.
    
    Args:
        extension (str): the extension of the file without the period, used to read in the file correctly.
        path_to_read_file (pathlib.Path): filepath to read in the file from.
        
    Returns:
        fields (dict): keys are the field name or column number and values are the name, type, and column number for each field. Ex: field_name : {"name":field_name, "type":field_type, "identifier":column_number+1, "identifier%type":"column"}
    """
    
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
                fields[column_number+1] = {"name":column_number+1, "type":field_type, "identifier":column_number+1, "identifier%type":"column"}
        
    return fields




def determine_json_fields(schema_list, input_json, file_path):
    """Determine the types of the feature properties in the JSON file.
    
    Based on the ESRIJSON and GEOJSON formats there are 2 types of schema styles, 
    mapping and testing. The mapping style has types already identified with the 
    properties in the JSON, but the types are not the same as those defined in the 
    MIAGIS schema, so a mapping between the types is necessary. This style's dict 
    entry looks like:
        {"style":"mapping", "schema":valid_jsonschema, "field_path":path_to_fields, 
         "name_key":key_to_name, "type_key":key_to_type, "type_map":type_mapping}
    
    Actual ESRIJSON example:
        {"style":"mapping", "schema":miagis_schema.arcgis_schema, 
         "field_path":'["layers"][0]["layerDefinition"]["fields"]', 
         "name_key":"name", "type_key":"type", "type_map":arcgis_type_map}
    
    The testing style doesn't have types listed directly in the JSON so each field's 
    type must be tested. This style's dict entry looks like:
        {"style":"testing", "schema":valid_jsonschema, 
         "features_path":path_to_features, "properties_key":key_to_properties}
        
    Actual GEOJSON example:
        {"style":"testing", "schema":miagis_schema.geojson_feature_schema, 
         "features_path":"", "properties_key":"properties", "schema_URL":"https://datatracker.ietf.org/doc/html/rfc7946"}
        
    Note that the features_path is assumed to lead to a dict or list, and will 
    print a warning if does is not.
        
    Args:
        schema_list (list): list of dictionaries where each dictionary describes a schema to look for and how to determine field types.
        input_json (dict): the JSON to determine field types for.
        file_path (str): path to the JSON file, used for printing error messages.
        
    Returns:
        json_fields (dict): a dictionary of the fields and their types. Ex field_name : {"name":field_name, "type":field_type}
        schema (dict or str): if "schema_URL" is in the schema dictionary then this is returned, otherwise return the jsonschema.
    """
    
    schema_properties = {}
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
            print("Warning: The \"field_path\", " + field_path + ", for the \"" + schema_properties["name"] + 
                  "\" json format schema does not work for file " + file_path + 
                  ". It will have empty \"fields\" in the output.")
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
                    print("Warning: The \"type_key\", " + type_key + " for the \"" + schema_properties["name"] + 
                          "\" json format is not in all of the fields for file " + 
                          file_path + ". Some fields may be missing in the output.")
                    type_already_printed = True
                continue
            
            if not name_key in field:
                if not name_already_printed:
                    print("Warning: The \"name_key\", " + name_key + " for the \"" + schema_properties["name"] + 
                          "\" json format schema is not in all of the fields for file " + 
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
            print("Warning: The \"features_path\", " + features_path + " for the \"" + schema_properties["name"] + 
                  "\" json format schema does not work for file " + file_path + 
                  ". It will have empty \"fields\" in the output.")
            return {}, schema
        
        if type(features) != list and type(features) != dict:
            print("Warning: The \"features_path\", " + features_path + " for the \"" + schema_properties["name"] + 
                  "\" json format schema does not lead to the appropriate type (list or dict) for file " + file_path 
                  + ". It will have empty \"fields\" in the output.")
            return {}, schema
        
        ## In the case where there is only a single feature we make the dictionary become a list with that dictionary inside it.
        if type(features) == dict:
            features = [features]
        
        properties_key = schema_properties["properties_key"]
        
        ## This loop assumes that each feature has the same properties and tries to determine the type of each property.
        ## It does not enforce features to have all the same properties. It simply accumulates all features it sees.
        ## Also assumes that any property will only have one type, so the first type seen is kept and not checked or overwritten except for None.
        json_fields = {}
        properties_already_printed = False
        for feature in features:
                        
            if not properties_key in feature:
                if not properties_already_printed:
                    print("Warning: The \"properties_key\", " + properties_key + " for the \"" + schema_properties["name"] + 
                          "\" json format schema is not in all of the features for file " + 
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
        print("Warning: Unknown \"style\", " + schema_properties["style"] + " for the \"" + schema_properties["name"] + 
              "\" json format. The file at " + file_path 
              + " will have empty \"fields\" in the output.")
        return {}, schema
            
            
        


