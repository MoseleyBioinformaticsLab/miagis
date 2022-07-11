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
        metadata: input dictionary of metadata.
        
    Raises:
        jsonschema.ValidationError: any validation errors that aren't handled reraise the original.
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
        
        
    
    ## Check that all products are in resources.
    if "products" in metadata and "resources" in metadata:
        for product in metadata["products"]:
            if product not in metadata["resources"]:
                print("The product, " + product + ", is not in \"resources\".")
    
    ## Check that all sources exist in resources, schema are valid json schema, and field names match ids.
    if "resources" in metadata:
        for resource_name, resource_fields in metadata["resources"].items():
            
            if "sources" in resource_fields:
                for source in resource_fields["sources"]:
                    if not source in metadata["resources"]:
                        print("The source, " + source + ", for resource, " + resource_name + ", does not exist in resources.")
                
            if "schema" in resource_fields and type(resource_fields["schema"]) == dict:
                schema_validator = jsonschema.validators.validator_for(resource_fields["schema"])
                try:
                    schema_validator.check_schema(resource_fields["schema"])
                except jsonschema.SchemaError:
                    print("The \"schema\" field for resource, " + resource_name + ", is not a valid JSON Schema.")
                    
            if "fields" in resource_fields:
                for field_name, field_values in resource_fields["fields"].items():
                    if "name" in field_values and field_name != field_values["name"]:
                        print("The \"name\" property for field, " + field_name + ", for resource, " + resource_name + ", does not match its key value.")
            
            