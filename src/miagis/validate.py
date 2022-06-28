# -*- coding: utf-8 -*-
"""
This module contains the code to validate the metadata file.
"""

import re

import jsonschema

from . import miagis_schema

def validate(metadata):
    """Validate input metadata against the MIAGIS schema.
    
    Use jsonschema to validate input metadata, and then do some additional checking 
    that jsonschema alone cannot, such as checking that all layers for each map 
    exist in the layers section.
    
    The specific JSON schema used is the metadata_schema in the miagis_schema module.
    
    Args:
        metadata (dict): input dictionary of metadata.
    """
    validator = jsonschema.Draft202012Validator(miagis_schema.metadata_schema)
    errors_generator = validator.iter_errors(metadata)
    
    for error in errors_generator:
        
        message = ""
        custom_message = ""
        
        if error.validator == "minProperties":
            custom_message = " cannot be empty."
        elif error.validator == "required":
            required_property = re.match(r"(\'.*\')", error.message).group(1)
            if len(error.relative_path) == 0:
                message += "The required property " + required_property + " is missing."
            else:
                message += "The entry " + "[%s]" % "][".join(repr(index) for index in error.relative_path) + " is missing the required property " + required_property + "."
        elif error.validator == "dependencies":
            message += "The entry " + "[%s]" % "][".join(repr(index) for index in error.relative_path) + " is missing a dependent property.\n"
            message += error.message
        elif error.validator == "dependentRequired":
            message += "The entry " + "[%s]" % "][".join(repr(index) for index in error.relative_path) + " is missing a dependent property.\n"
            message += error.message
        elif error.validator == "minLength":
            custom_message = " cannot be an empty string."
        elif error.validator == "maxLength":
            custom_message = " is too long."
        elif error.validator == "minItems":
            custom_message = " cannot be empty."
        elif error.validator == "type":
            if type(error.validator_value) == list:
                custom_message = " is not any of the allowed types: ["
                for allowed_type in error.validator_value:
                    custom_message += "\'" + allowed_type + "\', "
                custom_message = custom_message[:-2]
                custom_message += "]."
            else:
                custom_message = " is not of type \"" + error.validator_value + "\"."
        elif error.validator == "enum":
            custom_message = " is not one of [" + "%s" % ", ".join(repr(index) for index in error.validator_value) + "]"
        elif error.validator == "format":
            custom_message = " is not a valid " + error.validator_value + "."
        elif error.validator == "pattern":
            custom_message = " must be \"FAIR\", so it can only include the letters F, A, I, and R in that order, case-insensitive."
        elif error.validator == "minimum":
            custom_message = " must be greater than or equal to " + str(error.validator_value)
        elif error.validator == "maximum":
            custom_message = " must be less than or equal to " + str(error.validator_value)
        else:
            print(error.message)
        
        
        if custom_message:
            message = message + "The value for " + "[%s]" % "][".join(repr(index) for index in error.relative_path) + custom_message
        print(message)
        
        
    ##Check that all layers in maps exist in layers and all layers have a location in files.
    for map_name, map_fields in metadata["products"]["maps"].items():
        for layer in map_fields["layers"]:
            if not layer in metadata["products"]["layers"]:
                print("The layer, " + layer + ", for the map, " + map_name + ", is not in the product layers.")
                
    file_locations = {location for file_fields in metadata["files"].values() if "alternate_locations" in file_fields for location in file_fields["alternate_locations"]}
    file_locations = file_locations | set(metadata["files"].keys())
    for layer_name, layer_fields in metadata["products"]["layers"].items():
        if not any([location in file_locations for location in layer_fields["locations"]]):
            print("The layer, " + layer_name + ", does not have a location in files.")
            
    ## Check that maps, layers, and fields ids match.
    for map_name, map_fields in metadata["products"]["maps"].items():
        if map_name != map_fields["id"]:
            print("The \"id\" field for map, " + map_name + ", does not match its key.")
            
    for layer_name, layer_fields in metadata["products"]["layers"].items():
        if layer_name != layer_fields["id"]:
            print("The \"id\" field for layer, " + layer_name + ", does not match its key.")
            
    for file_location, file_fields in metadata["files"].items():
        if file_location != file_fields["location"]:
            print("The \"location\" field for file, " + file_location + ", does not match its key.")
            
        if "schema" in file_fields and type(file_fields["schema"]) == dict:
            schema_validator = jsonschema.validators.validator_for(file_fields["schema"])
            try:
                schema_validator.check_schema(file_fields["schema"])
            except jsonschema.SchemaError:
                print("The \"schema\" field for file, " + file_location + ", is not a valid JSON Schema.")
            
            