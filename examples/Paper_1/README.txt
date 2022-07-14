This example uses the files from the first PFAS paper the Pennell lab published.
Note that the GIS_METADATA.json file is not valid, it will produce errors if you run "miagis validate" on it.
This is intended so you can reproduce the build results.

Command to replicate results:
miagis build --resource_properties=Paper_1\resource_properties.csv --base_metadata=Paper_1\base_metadata.json --add_resources --remove_optional_fields