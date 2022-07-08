# -*- coding: utf-8 -*-
"""
    For the current directory go through all files and folders and build a GIS metadata file.
    The output is saved as GIS_METADATA.json in the current directory and will overwrite without warning.
    
    The output is simply an attempt to automate as much of the metadata build as possible, 
    and is not guarenteed to be correct or be a valid metadata file. It is expected that 
    after the initial build a user will double check and correct by hand, and then use 
    the validate command to validate their metadata before submission.
    
    The resource_properties option file is expected to have a header row on the first row for tabular 
    files with "file_name" being the only required row to use as a key. Other headers should 
    match field names to go into the metadata[files] properties. Extra property names beyond 
    those in the metadata specification are allowed and simply added as is to any items.
    
    Example:
        file_name	    alternate_locations	     sources	        source_types	    description	           geographical_area
        example_name	URL_to_file	             source1,source2	organization,URL	example_description	   Kentucky

    
    Any directory structure will work, but there is additional functionality if the directories 
    are named a certain way. If layer data is kept in "layer_data" then the program will add them 
    to metadata[products][layers]. The same for maps in "map_data". 
    
    The standard example run:
        miagis build --remove_optional_fields --resource_properties <filepath> --base_metadata <filepath>
    
 
 Usage:
    miagis build [options]
    miagis validate <metadata_json>
    miagis print_map_layers <metadata_json> [--save_path=<save_path>]

 Options:
    --help                              Show this help documentation.
    --resource_properties=<file_path>   Filepath to a csv, xlsx, or JSON file with file properties.
    --exact_name_match                  If used then file name matching will be done exactly instead of fuzzy.
    --add_resources                     If used then add resources from resource_properties directly to the metadata.
    --overwrite_format                  If used then overwrite the determined format for files with what is in resource_properties.
    --overwrite_fairness                If used then overwrite the determined fairness for files with what is in resource_properties.
    --remove_optional_fields            If used then delete optional metadata fields that are empty from files.
    --json_schemas=<file_path>          Filepath to a JSON file with schemas for different JSON formats.
    

 Base Metadata Options:
    --entry_version=<integer>           Set the entry_version field for the metadata. Should be an integer starting from 1. [default: 1]
    --entry_id=<id>                     Set the entry_id field for the metadata.
    --description=<description>         Set the description field for the metadata
    --base_metadata=<file_path>         Filepath to a JSON file with the base metadata fields to use.
"""


import warnings

warnings.filterwarnings("ignore", module="fuzzywuzzy")

import docopt

from . import miagis_schema
from . import build
from . import validate
from . import user_input_checking
from . import print_map_layers



def main():
    args = docopt.docopt(__doc__)
    user_input_checking.validate_arbitrary_schema(args, miagis_schema.args_schema)
    user_input_checking.additional_args_checks(args)
        
    if args["build"]:
        
        if args["--json_schemas"]:
            schema_list = user_input_checking.load_json(args["--json_schemas"])
            user_input_checking.validate_arbitrary_schema(schema_list, miagis_schema.schema_list_schema)
            user_input_checking.additional_json_schemas_checks(schema_list)
        else:
            schema_list = []
        
        if args["--base_metadata"]:
            base_metadata = user_input_checking.load_json(args["--base_metadata"])
        else:
            base_metadata = {}
        
        
        build.build(args["--resource_properties"], args["--exact_name_match"], 
                    args["--remove_optional_fields"], args["--add_resources"],
                    args["--overwrite_format"], args["--overwrite_fairness"],
                    base_metadata, int(args["--entry_version"]), args["--entry_id"], 
                    args["--description"], [], schema_list)
    elif args["validate"]:
        validate.validate(user_input_checking.load_json(args["<metadata_json>"]))
    elif args["print_map_layers"]:
        print_map_layers.print_map_layers(user_input_checking.load_json(args["<metadata_json>"]), args["--save_path"])
    else:
        print("Unrecognized command")






if __name__ == "__main__":
    main()



