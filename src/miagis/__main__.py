# -*- coding: utf-8 -*-
"""
 miagis.py
    For the current directory go through all files and folders and build a GIS metadata file.
    The output is saved as GIS_METADATA.json in the current directory and will overwrite without warning.
    
    The output is simply an attempt to automate as much of the metadata build as possible, 
    and is not guarenteed to be correct or be a valid metadata file. It is expected that 
    after the initial build a user will double check and correct by hand, and then use 
    the validate command to validate their metadata before submission.
    
    The file_properties option file is expected to have a header row on the first row for tabular 
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
        miagis.py build --remove_optional_fields --file_properties <filepath> --base_metadata <filepath>
    
 
 Usage:
    miagis.py build [options]
    miagis.py validate <metadata_json>

    <metadata_json> - metadata file to validate.

 Options:
    --help                              Show this help documentation.
    --file_properties=<file_path>       Filepath to a csv, xlsx, or JSON file with file properties.
    --exact_name_match                  If used then file name matching will be done exactly instead of fuzzy.
    --remove_optional_fields            If used then delete optional metadata fields that are empty from files.
    --entry_version=<integer>           Set the entry_version field for the metadata. Should be an integer starting from 1. [default: 1]
    --entry_id=<id>                     Set the entry_id field for the metadata.
    --description=<description>         Set the description field for the metadata
    --base_metadata=<file_path>         Filepath to a JSON file with the base metadata fields to use.
"""

## TODO generalize to accept other JSON schemas.

import warnings

warnings.filterwarnings("ignore", module="fuzzywuzzy")

import docopt

from . import miagis_schema
from . import build
from . import validate
from . import user_input_checking





def main():
    args = docopt.docopt(__doc__)
    user_input_checking.validate_arbitrary_schema(args, miagis_schema.args_schema)
    user_input_checking.additional_args_checks(args)
    
    base_metadata_dict = miagis_schema.base_metadata_dict
    
    if args["build"]:
        if args["--base_metadata"]:
            base_metadata = user_input_checking.load_json(args["--base_metadata"])
            user_input_checking.validate_arbitrary_schema(base_metadata, miagis_schema.base_schema)
        
        for base_key in base_metadata_dict:
            if args["--base_metadata"] and base_key in base_metadata:
                base_metadata_dict[base_key] = base_metadata[base_key]
            else: 
                args_key = "--" + base_key
                if args[args_key]:
                    base_metadata_dict[base_key] = args[args_key]
        
        build.build(args["--file_properties"], args["--exact_name_match"], args["--remove_optional_fields"], 
              int(base_metadata_dict["entry_version"]), base_metadata_dict["entry_id"], 
              base_metadata_dict["description"], base_metadata_dict["products"])
    elif args["validate"]:
        validate.validate(user_input_checking.load_json(args["<metadata_json>"]))
    else:
        print("Unrecognized command")






if __name__ == "__main__":
    main()



