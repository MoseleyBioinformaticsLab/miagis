# -*- coding: utf-8 -*-
"""
This module contains the functions used to read in and validate various inputs.
"""

import sys
import pathlib
import json

import jsonschema
import pandas



def load_json(filepath):
    """Adds error checking around loading a json file.
    
    Args:
        filepath (str): filepath to the json file
        
    Returns:
        internal_data (dict): json read from file in a dictionary
        
    Raises:
        Exception: If file opening has a problem will raise an exception.
    """
    if pathlib.Path(filepath).exists():
        try:
            with open(filepath, "r") as f:
                internal_data = json.loads(f.read())
        except Exception as e:
            raise e

        return internal_data
    else:
        print("No such file: " + filepath)
        sys.exit()




def read_in_file_properties(file_properties_path, exact_matching):
    
    if file_properties_path == None:
        return {}
    
    if not pathlib.Path(file_properties_path).exists():
        print("No such file: " + file_properties_path)
        sys.exit()
    
    extension = pathlib.Path(file_properties_path).suffix[1:].lower()
    if extension == "csv":
        file_properties_df = pandas.read_csv(file_properties_path, dtype=str)
    elif extension == "xlsx":
        file_properties_df = pandas.read_excel(file_properties_path, dtype=str)
    elif extension == "json":
        return load_json(file_properties_path)
    else:
        print("Error: Unknown file type for --file_properties.")
        sys.exit()
    
    if not "file_name" in file_properties_df.columns:
        print("Error: The file input for --file_properties does not have a file_name column.")
        sys.exit()
    
    file_properties_df = file_properties_df.fillna("")
    
    if not exact_matching:
        file_properties_df.loc[:, "file_name"] = file_properties_df.loc[:, "file_name"].str.strip()
        file_properties_df.loc[:, "file_name"] = file_properties_df.loc[:, "file_name"].str.lower()
        file_properties_df.loc[:, "file_name"] = file_properties_df.loc[:, "file_name"].str.replace(" ", "_")
    
    if "alternate_locations" in file_properties_df:
        file_properties_df.loc[:, "alternate_locations"] = file_properties_df.loc[:, "alternate_locations"].str.strip()
    
    file_properties_df = file_properties_df.drop_duplicates()
    file_properties_df = file_properties_df.set_index("file_name", drop=True)
    
    file_properties = file_properties_df.to_dict(orient="index")
    for file_name, properties in file_properties.items():
        if "alternate_locations" in file_properties_df.columns:
            file_properties[file_name]["alternate_locations"] = [location.strip() for location in properties["alternate_locations"].split(",") if location.strip()]
            
        if "sources" in file_properties_df.columns and "source_types" in file_properties_df.columns:
            sources = [source.strip() for source in properties["sources"].split(",")]
            source_types = [source_type.strip() for source_type in properties["source_types"].split(",")]
            if len(sources) == len(source_types):
                file_properties[file_name]["sources"] = [{"source":sources[i], "type":source_types[i]} for i in range(len(sources))]
            else:
                print("Warning: Not every source in \"sources\" has a \"source_types\" for " + file_name + " in the --file_properties file.")
            
            del[file_properties[file_name]["source_types"]]
    
    
    return file_properties




def validate_arbitrary_schema(dict_to_validate, schema):
        
    try:
        jsonschema.validate(dict_to_validate, schema)
    except jsonschema.ValidationError as e:
        
        message = "ValidationError: An error was found in the " + schema["title"] + ".\n"
        custom_message = ""
        
        if e.validator == "minLength":
            custom_message = " cannot be an empty string."
        elif e.validator == "maxLength":
            custom_message = " is too long."
        elif e.validator == "minItems":
            custom_message = " cannot be empty."
        elif e.validator == "type":
            if type(e.validator_value) == list:
                custom_message = " is not any of the allowed types: ["
                for allowed_type in e.validator_value:
                    custom_message += "\'" + allowed_type + "\', "
                custom_message = custom_message[:-2]
                custom_message += "]."
            else:
                custom_message = " is not of type \"" + e.validator_value + "\"."
        elif e.validator == "enum":
            custom_message = " is not one of [" + "%s" % ", ".join(repr(index) for index in e.validator_value) + "]"
        elif e.validator == "format":
            custom_message = " is not a valid " + e.validator_value + "."
        elif e.validator == "minimum":
            custom_message = " must be greater than or equal to " + str(e.validator_value)
        elif e.validator == "maximum":
            custom_message = " must be less than or equal to " + str(e.validator_value)
        else:
            raise e
        
        
        if custom_message:
            message = message + "The value for " + "[%s]" % "][".join(repr(index) for index in e.relative_path) + custom_message
        print(message)
        sys.exit()


def additional_args_checks(args):
    file_path_properties = ["--file_properties", "--base_metadata", "<metadata_json>"]
    for path in file_path_properties:
        if args[path] and not pathlib.Path(args[path]).exists():
            print("Error: The value entered for " + path + " is not a valid file path or does not exist.")
            sys.exit()
                
        
    try:
        entry_version = int(args["--entry_version"])
    except ValueError:
        print("Error: The value entered for --entry_version is not an integer.")
        sys.exit()
        
    if entry_version < 1:
        print("Error: The value entered for --entry_version is less than 1.")
        sys.exit()