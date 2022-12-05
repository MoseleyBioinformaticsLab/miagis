Tutorial
========
MIAGIS is intended to be used solely as a command line program. This tutorial 
describes each command and its options. Some simple examples are given here, but 
examples of papers actually published are in the examples folder on GitHub_.

Metadata JSON File
~~~~~~~~~~~~~~~~~~
Details about the metadata JSON file created and validated by MIAGIS can be found 
in the :doc:`jsonschema` section. In short there are 2 sections to the metadata, 
the base and the resources. The base is a few short entries describing the overall 
project, deposition, and products. The resources are details about each resource 
used or created during the project and included in the deposition. MIAGIS does 
the heavy lifting of filling out some of the tedious and repetitive parts in the 
resources section.

Deposition Directory
~~~~~~~~~~~~~~~~~~~~
Although MIAGIS will work with any directory structure it has extra functionality 
if a certain structure is used. The expected structure is a directory named "map_data", 
a directory named "layer_data", and a directory named "other". "map_data" contains 
data for whole GIS maps, "layer_data" contains files for individual layers of a 
map, and "other" contains any other data that is not maps or layers. Any directory 
that does not contain files should be deleted.

Before Running
~~~~~~~~~~~~~~
Getting the initial metadata build to come out as close to finished to as possible 
with a minimum amount of manual entry needed is heavily facilitated by getting 
everything in order before running the command. First create a directory with 
the structure as described above, and put all of the files in the appropriate 
locations. Then create a base metadata JSON file that fills out the base metadata. 
Then create a resource properties file that contains information about each 
resource. The base metadata file and resource properties file are detailed below 
with examples. With all of this done the preparation for running the build 
command is complete.

Input Files
~~~~~~~~~~~

Base Metadata File
------------------
The base metadata file that can be input to MIAGIS through the --base_metadata 
option is a JSON file with the base section of the metadata. Unfortunately, much 
of this information must be filled out by hand because it cannot be determined 
or inferred programmatically. 

The reason to create a separate file and deliver it to MIAGIS rather than simply 
filling them in after MIAGIS creates the metadata is for the case where the 
build command needs to be ran more than once. Although you may think you have 
all of the files prepared for the deposition it is not uncommon to miss or 
forget things and need to rebuild or modify the metadata file. Depending on the 
specific situation it can be easier to rebuild using MIAGIS than modifying by hand. 

Example:

.. code-block:: console

    {
      "format_version": "DRAFT_MIAGIS_VERSION_0.1",
      "entry_version": 1,
      "entry_id": "KY SOP Paper",
      "description": "Data used for the paper titled \"Paper Title\"  DOI: ",
      "products": [
          "Combined map",
          "Water map",
          "Map Sewer",
          "SWAPP map Ky"
          "Hotspot Map"]
    }


Resource Properties File
------------------------
The resource properties file is either a tabular or JSON file that contains information 
about resources in the deposition. It serves a few purposes. One purpose is to give 
a more condensed view of the resources and their properties in the case of the tabular 
form. It can be much easier to collect and manipulate all of the resource information 
in Excel or Google Sheets rather than trying to manage it in JSON directly. Another 
purpose is to avoid repetition. Due to a variety of formats the same data may be 
included multiple times in multiple files. The resource properties file allows you 
to enter information about a resource once and MIAGIS will copy it to all files that 
match the resource name. Names do not have to be exact unless the --exact_name_match 
option is used, by default MIAGIS does fuzzy name matching.

If using the tabular form the file must have a header row on the first row and 
a column named "resource_name". All other columns will be inserted into the metadata 
files section with the exact column name in the header. "resource_name" is not the 
only special column name. "alternate_locations", "sources", "creator", and "creator_type" 
can be single entries or multiple entries separated by commas. There is further 
logic that looks to see if the "creator" and "creator_type" have the same number 
of entries in a row and prints a warning if they do not.

If using the JSON form of the file each entry should meet the schema of the resources 
section of the metadata. As with the tabular form all properties are simply copied 
into the metadata for files whose names match the key in the JSON.

Short Example Tabular:

.. code-block:: console

    resource_name	    alternate_locations	   creator	             creator_type	            description	        geographical_area
    <resource_name>	    <URL_to_file>,...	   <creator_name>,...	 <organization|URL>,...	    <description>	    <geographical_area>
    

Short Example JSON:

.. code-block:: console

    {
     <resource_name>: {
      'alternate_locations': [<URL_to_file>],
      'creator': [{'name': <creator_name>, 'type': 'organization'},
                  {'name': <creator_name>, 'type': 'URL'}],
      'description': <description>,
      'geographical_area': <geographical_area>}
    }


Long Example Tabular:

.. code-block:: console

    file_name	                                     alternate_locations	                                                                                                                                                               creator	                                                                                                                        creator_type	     description	                                            geographical_area
    PFAS_sampling_and_purchasing_and_intake_detail	 https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer	Kentucky                                                       Department of Environmental Protection,https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf    organization,URL     List of all water systems in which PFAS were sampled.	    Kentucky
    Ohio_River_Marinas_WFL1 - Ohio River	         https://services8.arcgis.com/Xcpl3GIMvkCI3oFI/arcgis/rest/services/Ohio_River_Marinas_WFL1/FeatureServer                                                                              ArcGIS Online	                                                                                                                organization	     Publicly available layer findable on ArcGIS Online.	    Kentucky
    Kentucky Water Lines1	                         https://kygisserver.ky.gov/arcgis/rest/services/WGS84WM_Services/Ky_Water_WGS84WM/MapServer/11, https://uky-edu.maps.arcgis.com/home/item.html?id=29713c2b8be14534943b8e2e5fa16daa    https://kygeoportal.ky.gov/                                                                                                      URL	                 Locations of water lines in Kentucky.	                    Kentucky

    
Long Example JSON:

.. code-block:: console

    {
     'PFAS_sampling_and_purchasing_and_intake_detail': {
      'alternate_locations': ['https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer'],
      'creator': [{'name': 'Kentucky Department of Environmental Protection',
                   'type': 'organization'},
                  {'name': 'https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf',
                   'type': 'URL'}],
      'description': 'List of all water systems in which PFAS were sampled.',
      'geographical_area': 'Kentucky'},
     
     'Ohio_River_Marinas_WFL1 - Ohio River': {
      'alternate_locations': ['https://services8.arcgis.com/Xcpl3GIMvkCI3oFI/arcgis/rest/services/Ohio_River_Marinas_WFL1/FeatureServer'],
      'creator': [{'name': 'ArcGIS Online', 'type': 'organization'}],
      'description': 'Publicly available layer findable on ArcGIS Online.',
      'geographical_area': 'Kentucky'},
     
     'Kentucky Water Lines1': {
      'alternate_locations': ['https://kygisserver.ky.gov/arcgis/rest/services/WGS84WM_Services/Ky_Water_WGS84WM/MapServer/11',
                                                       'https://uky-edu.maps.arcgis.com/home/item.html?id=29713c2b8be14534943b8e2e5fa16daa'],
      'creator': [{'name': 'https://kygeoportal.ky.gov/', 'type': 'URL'}],
      'description': 'Locations of water lines in Kentucky.',
      'geographical_area': 'Kentucky'}
    }
    
    
JSON Schemas File
-----------------
The JSON Schemas file is a JSON file that allows you to specify different styles 
or formats of JSON files so that MIAGIS can accurately describe the fields in the 
file. MIAGIS is inherently aware of GEOJSON and ESRIJSON, but in the case of other 
proprietary or unique JSON formats this file may be used to let MIAGIS process 
them. 

The first thing that is required is a way to test a given JSON file and see if 
it matches the format. This is accomplished using `JSON Schema <https://json-schema.org/>`_ . 
A valid JSON Schema must be created for the format so that if the file under 
question is validated by the schema we can be reasonably sure it is of that format. 
The Schema does not have to be complicated and fully describe the format. It just 
needs to be robust enough that if a JSON file is validated by the Schema we are 
sure it is of our format. The Schema used to validate the GEOJSON and ESRIJSON 
formats are in the :doc:`jsonschema` section.

The next pieces that are required depend on the style of the format. The JSON 
Schemas file is based off of the GEOJSON and ESRIJSON formats, so there are 2 
"styles", "mapping" and "testing". The ESRIJSON format already has a section inside 
its format that describes each field and gives it a type directly. These types 
are not the same types as those accepted by the MIAGIS Schema, so a mapping between 
the ESRI types and MIAGIS types must be made. The specific path to the list of 
metadata fields, the key to the name of the field, and the key to the type of the 
field must also be given. 


Mapping Style Generic Example:

.. code-block:: console

    {
     "style":"mapping", 
     "schema":valid_json_schema, 
     "field_path":'["path"]["to"]["fields"]', 
     "name_key":"name", 
     "type_key":"type", 
     "type_map":{"unique_type_1":"str", "unique_type_2":"float"}
    }


All of the properties in the above example are required for the mapping style. 
"schema" should be a valid JSON Schema that will be used to validate JSON files 
and match it to the format. "field_path" is a string that leads to where the 
fields are in the format. The path is assumed to lead to a list of dictionaries 
where each dictionary describes a field in the data. The string should use the 
familiar subscript notation for accessing dictionaries or objects in many 
programming languages. "name_key" is simply the key value in the field dictionary 
that will access the name of the field. "type _key" is simply the key value in 
the field dictionary that will access the type of the field. "type_map" is a 
dictionary that translates the format's types into MIAGIS types. Any types not 
in the map will be typed as "UNKNOWN".


ESRIJSON Excerpt:

.. code-block:: console

    // Shortened for Space
    {
     "layers":
         [{"layerDefinition":
           {"geometryType":"esriGeometryPoint",
            "objectIdField":"__OBJECTID",
            "type":"Feature Layer",
            "fields":[
                {"name":"__OBJECTID","alias":"__OBJECTID","type":"esriFieldTypeOID","editable":false,"nullable":false,"domain":null},
                {"name":"Sites","alias":"Sites","type":"esriFieldTypeString","length":255,"editable":true,"nullable":true,"domain":null},
                {"name":"Latitude","alias":"Latitude","type":"esriFieldTypeDouble","editable":true,"nullable":true,"domain":null},
                {"name":"Longitude","alias":"Longitude","type":"esriFieldTypeDouble","editable":true,"nullable":true,"domain":null},
                {"name":"Site_Types","alias":"Site Types","type":"esriFieldTypeString","length":255,"editable":true,"nullable":true,"domain":null},
                {"name":"Risk_score","alias":"Risk score","type":"esriFieldTypeInteger","editable":true,"nullable":true,"domain":null}
                ],
            }
           }
          ]
    }


The GEOJSON format does not provide field type information, so the type of the 
fields has to be tested to determine its type. 


Testing Style Generic Example:

.. code-block:: console

    {
     "style":"testing", 
     "schema":valid_json_schema, 
     "features_path":'["path"]["to"]["features"]', 
     "properties_key":"properties"
    }


All of the properties in the above example are required for the testing style. 
"features_path" is similary to "field_path" for the mapping style, but instead 
can lead to a list of dictionaries or a single dictionary. Each dictionary is 
expected to be a feature with a properties attribute that is a dictionary of 
properties. Each property in each feature is tested to determine the type of the 
property. "properties_key" is the key to the properties in each feature.


GEOJSON Excerpt:

.. code-block:: console

    // Shortened for Space
    {
     "type":"FeatureCollection",
     "crs":{
            "type":"name",
            "properties":{"name":"EPSG:4326"}},
     "features":[
                 {"type":"Feature",
                  "id":1,
                  "geometry":{"type":"Point","coordinates":[-85.0965039679502,38.7155959953824]},
                  "properties":
                      {"F__OBJECTID":1,"Sites":"Cabot Corporation","Latitude":38.715596,"Longitude":-85.096504,"Site_Types":"Chemical manufacturing","Risk_score":100}},
                 {"type":"Feature",
                  "id":2,
                  "geometry":{"type":"Point","coordinates":[-84.462112007506,38.0473190082068]},
                  "properties":
                      {"F__OBJECTID":2,"Sites":"Src Of Lexington","Latitude":38.047319,"Longitude":-84.462112,"Site_Types":"Chemical manufacturing","Risk_score":100}}
                ]
    }


Building
~~~~~~~~
Command Line Signature
----------------------

.. code-block:: console

    miagis build [options]


Description
-----------
For each subdirectory in the current directory loop through all of the files and 
make a best attempt at adding it to the resources section of the metadata, filling 
in as much information as possible. Files found in "layer_data" automatically get 
a "layer" type and those found in "map_data" get a "map" type.


Options
-------
--resource_properties: 

Supply a tabular or JSON file to MIAGIS that it will use to match file names and 
fill in more information in the resources section of the metadata. MIAGIS also 
keeps track of all files matched and updates all matches "alternate_locations", 
so that every match has alternate_locations to each other.

--exact_name_match: 

If used MIAGIS will match file names in the resource properties file exactly rather 
than the default of fuzzy matching.

--add_resources: 

If used then add resources from resource_properties directly to the metadata. More 
specifically, MIAGIS will loop over files and match file names to resource names, 
using that to fill in more information about the files, but at the end each resource 
will also be added to the metadata with its resource_name. This option exists so 
that each layer and map can be added as a resource to condense information. Instead 
of having to pick a single layer file as a source to a map, or add all of the files 
you can add the layer as a resource and use that as the source. The layer then 
has all of its files in its resource entry. 

If your resource_properties file is a mix of resources that you want to add and 
simple file matching that you don't want to add there is a way to signal this. 
In the resource_properties file make sure there is a "location" column, and for 
any resource that you do not want to add directly leave this column blank. There 
should be a "location" anyway for any resources that you do want to add to the 
metadata directly.

--overwrite_format: 

If used then overwrite the determined format for files with what is in resource_properties. 
This option was created in tandem with the --add_resources option. If you use the 
--add_resources option you will want to give the resource its own format, but if 
you add a "format" column in the resource_properties file that value will be used 
for any matched files. To avoid this use this option. Using this option will have 
MIAGIS ignore the "format" column in resource_properties for any matched files and 
instead use the format determined by the file extension. 

--overwrite_fairness: 

If used then overwrite the determined fairness for files with what is in resource_properties.
This option was created in tandem with the --add_resources option. If you use the 
--add_resources option you will want to give the resource its own fairness, but if 
you add a "fairness" column in the resource_properties file that value will be used 
for any matched files. To avoid this use this option. Using this option will have 
MIAGIS ignore the "fairness" column in resource_properties for any matched files and 
instead use the default value of "FAIR".

--json_schemas: 

Supply a JSON file to MIAGIS that describes new JSON formats to look for and how 
to find the metadata fields in them. 
            
--remove_optional_fields: 

If used all empty optional fields in the metadata will be removed.

--entry_version: 

Supply an integer starting from 1 to MIAGIS to use in the "entry_version" of the 
metadata.

--entry_id: 

Supply a string to MIAGIS to use in the "entry_id" of the metadata.

--description: 

Supply a string to MIAGIS to use in the "description" of the metadata.

--base_metadata: 

Supply a JSON file to MIAGIS that contains base metadata information. It will be 
copied into the metadata as is. If other options conflict with the data in the 
file (entry_version, entry_id, or description) the command line option will overwrite 
what is in the file.


Outputs
-------
Outputs a file named GIS_METADATA.json in the current directory.


Examples
--------
Typical run.

Console:

.. code-block:: console
    
    miagis build --resource_properties file_location --base_metadata file_location --add_resources --remove_optional_fields

resource_properties.csv:

.. code-block:: console

    file_name	                                     location	                                                                                                                                                                           creator	                                                                                                                        creator_type         format	     fairness    description	                                            geographical_area
    PFAS_sampling_and_purchasing_and_intake_detail	 https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer	Kentucky                                                       Department of Environmental Protection,https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf    organization,URL     web         Fir         List of all water systems in which PFAS were sampled.	    Kentucky
    Ohio_River_Marinas_WFL1 - Ohio River	         https://services8.arcgis.com/Xcpl3GIMvkCI3oFI/arcgis/rest/services/Ohio_River_Marinas_WFL1/FeatureServer                                                                              ArcGIS Online	                                                                                                                organization	     web         Fir         Publicly available layer findable on ArcGIS Online.	    Kentucky
    Kentucky Water Lines1	                         https://kygisserver.ky.gov/arcgis/rest/services/WGS84WM_Services/Ky_Water_WGS84WM/MapServer/11, https://uky-edu.maps.arcgis.com/home/item.html?id=29713c2b8be14534943b8e2e5fa16daa    https://kygeoportal.ky.gov/                                                                                                      URL	                 web         Fir         Locations of water lines in Kentucky.	                    Kentucky

base_metadata.json:

.. code-block:: console

    {
      "format_version": "DRAFT_MIAGIS_VERSION_0.1",
      "entry_version": 1,
      "entry_id": "KY SOP Paper",
      "description": "Data used for the paper titled \"Paper Title\"  DOI: ",
      "products": [
          "Map 1"]
    }


Current Directory:

├─ layer_data/
│  ├─ PFAS sampling and purchasing and intake detail.json
│  ├─ PFAS_sampling_and_purchasing_and_intake_detail.geojson
│  ├─ PFAS sampling and purchasing and intake detail.csv


Output Metadata:

.. code-block:: console
    
    {
      "format_version": "DRAFT_MIAGIS_VERSION_0.1",
      "entry_version": 1,
      "entry_id": "KY SOP Paper",
      "description": "Data used for the paper titled \"Paper Title\"  DOI: ",
      "products": [
          "Map 1"],
      "resources":{
        "layer_data/PFAS sampling and purchasing and intake detail.csv": {
          "location": "layer_data/PFAS sampling and purchasing and intake detail.csv",
          "type": "layer",
          "description": "List of all water systems in which PFAS were sampled.",
          "fairness": "FAIR",
          "format": "csv",
          "creator": [
            {
              "name": "Kentucky Department of Environmental Protection",
              "type": "organization"
            },
            {
              "name": "https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf",
              "type": "URL"
            }
          ],
          "alternate_locations": [
            "https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer",
            "layer_data/PFAS sampling and purchasing and intake detail.csv",
            "layer_data/PFAS sampling and purchasing and intake detail.json",
            "layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson"
          ],
          "geographical_area": "Kentucky",
          "fields": {
            "__OBJECTID": {
              "name": "__OBJECTID",
              "type": "int",
              "identifier": 1,
              "identifier%type": "column"
            },
            "Sample": {
              "name": "Sample",
              "type": "str",
              "identifier": 2,
              "identifier%type": "column"
            },
            "Collected": {
              "name": "Collected",
              "type": "str",
              "identifier": 3,
              "identifier%type": "column"
            },
            "Received": {
              "name": "Received",
              "type": "str",
              "identifier": 4,
              "identifier%type": "column"
            },
            "PSWID": {
              "name": "PSWID",
              "type": "str",
              "identifier": 5,
              "identifier%type": "column"
            },
            "Location": {
              "name": "Location",
              "type": "str",
              "identifier": 6,
              "identifier%type": "column"
            },
            "Intake /purchase": {
              "name": "Intake /purchase",
              "type": "str",
              "identifier": 7,
              "identifier%type": "column"
            },
            "Type": {
              "name": "Type",
              "type": "str",
              "identifier": 8,
              "identifier%type": "column"
            },
            "PFBS": {
              "name": "PFBS",
              "type": "float",
              "identifier": 9,
              "identifier%type": "column"
            },
            "HFPO- DA": {
              "name": "HFPO- DA",
              "type": "float",
              "identifier": 10,
              "identifier%type": "column"
            },
            "PFHpA": {
              "name": "PFHpA",
              "type": "float",
              "identifier": 11,
              "identifier%type": "column"
            },
            "PFHxS": {
              "name": "PFHxS",
              "type": "float",
              "identifier": 12,
              "identifier%type": "column"
            },
            "ADONA": {
              "name": "ADONA",
              "type": "int",
              "identifier": 13,
              "identifier%type": "column"
            },
            "PFOA": {
              "name": "PFOA",
              "type": "float",
              "identifier": 14,
              "identifier%type": "column"
            },
            "PFOS": {
              "name": "PFOS",
              "type": "float",
              "identifier": 15,
              "identifier%type": "column"
            },
            "PFNA": {
              "name": "PFNA",
              "type": "float",
              "identifier": 16,
              "identifier%type": "column"
            },
            "PFOA+PFOS": {
              "name": "PFOA+PFOS",
              "type": "float",
              "identifier": 17,
              "identifier%type": "column"
            },
            "Sum of PFAS": {
              "name": "Sum of PFAS",
              "type": "float",
              "identifier": 18,
              "identifier%type": "column"
            },
            "Units": {
              "name": "Units",
              "type": "str",
              "identifier": 19,
              "identifier%type": "column"
            },
            "LATITUDE": {
              "name": "LATITUDE",
              "type": "float",
              "identifier": 20,
              "identifier%type": "column"
            },
            "LONGITUDE": {
              "name": "LONGITUDE",
              "type": "float",
              "identifier": 21,
              "identifier%type": "column"
            },
            "Aquifer/Source": {
              "name": "Aquifer/Source",
              "type": "str",
              "identifier": 22,
              "identifier%type": "column"
            },
            "River Basin": {
              "name": "River Basin",
              "type": "str",
              "identifier": 23,
              "identifier%type": "column"
            },
            "Aquifer General": {
              "name": "Aquifer General",
              "type": "str",
              "identifier": 24,
              "identifier%type": "column"
            },
            "Land Use": {
              "name": "Land Use",
              "type": "str",
              "identifier": 25,
              "identifier%type": "column"
            },
            "x": {
              "name": "x",
              "type": "float",
              "identifier": 26,
              "identifier%type": "column"
            },
            "y": {
              "name": "y",
              "type": "float",
              "identifier": 27,
              "identifier%type": "column"
            }
          }
        },
        "layer_data/PFAS sampling and purchasing and intake detail.json": {
          "location": "layer_data/PFAS sampling and purchasing and intake detail.json",
          "type": "layer",
          "description": "List of all water systems in which PFAS were sampled.",
          "fairness": "FAIR",
          "format": "json",
          "creator": [
            {
              "name": "Kentucky Department of Environmental Protection",
              "type": "organization"
            },
            {
              "name": "https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf",
              "type": "URL"
            }
          ],
          "alternate_locations": [
            "https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer",
            "layer_data/PFAS sampling and purchasing and intake detail.csv",
            "layer_data/PFAS sampling and purchasing and intake detail.json",
            "layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson"
          ],
          "geographical_area": "Kentucky",
          "fields": {
            "__OBJECTID": {
              "name": "__OBJECTID",
              "type": "int"
            },
            "Sample": {
              "name": "Sample",
              "type": "str"
            },
            "Collected": {
              "name": "Collected",
              "type": "str"
            },
            "Received": {
              "name": "Received",
              "type": "str"
            },
            "PSWID": {
              "name": "PSWID",
              "type": "str"
            },
            "Location": {
              "name": "Location",
              "type": "str"
            },
            "Intake_purchase": {
              "name": "Intake_purchase",
              "type": "str"
            },
            "Type": {
              "name": "Type",
              "type": "str"
            },
            "PFBS": {
              "name": "PFBS",
              "type": "float"
            },
            "HFPO_DA": {
              "name": "HFPO_DA",
              "type": "float"
            },
            "PFHpA": {
              "name": "PFHpA",
              "type": "float"
            },
            "PFHxS": {
              "name": "PFHxS",
              "type": "float"
            },
            "ADONA": {
              "name": "ADONA",
              "type": "int"
            },
            "PFOA": {
              "name": "PFOA",
              "type": "float"
            },
            "PFOS": {
              "name": "PFOS",
              "type": "float"
            },
            "PFNA": {
              "name": "PFNA",
              "type": "float"
            },
            "PFOA+PFOS": {
              "name": "PFOA+PFOS",
              "type": "float"
            },
            "Sum_of_PFAS": {
              "name": "Sum_of_PFAS",
              "type": "float"
            },
            "Units": {
              "name": "Units",
              "type": "str"
            },
            "LATITUDE": {
              "name": "LATITUDE",
              "type": "float"
            },
            "LONGITUDE": {
              "name": "LONGITUDE",
              "type": "float"
            },
            "Aquifer_Source": {
              "name": "Aquifer_Source",
              "type": "str"
            },
            "River_Basin": {
              "name": "River_Basin",
              "type": "str"
            },
            "Aquifer_General": {
              "name": "Aquifer_General",
              "type": "str"
            },
            "Land_Use": {
              "name": "Land_Use",
              "type": "str"
            }
          }
        },
        "layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson": {
          "location": "layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson",
          "type": "layer",
          "description": "List of all water systems in which PFAS were sampled.",
          "fairness": "FAIR",
          "format": "geojson",
          "creator": [
            {
              "name": "Kentucky Department of Environmental Protection",
              "type": "organization"
            },
            {
              "name": "https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf",
              "type": "URL"
            }
          ],
          "alternate_locations": [
            "https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_sampling_and_purchasing_data_2019/FeatureServer",
            "layer_data/PFAS sampling and purchasing and intake detail.csv",
            "layer_data/PFAS sampling and purchasing and intake detail.json",
            "layer_data/PFAS_sampling_and_purchasing_and_intake_detail.geojson"
          ],
          "geographical_area": "Kentucky",
          "schema": "https://datatracker.ietf.org/doc/html/rfc7946",
          "fields": {
            "F__OBJECTID": {
              "name": "F__OBJECTID",
              "type": "int"
            },
            "Sample": {
              "name": "Sample",
              "type": "str"
            },
            "Collected": {
              "name": "Collected",
              "type": "str"
            },
            "Received": {
              "name": "Received",
              "type": "str"
            },
            "PSWID": {
              "name": "PSWID",
              "type": "str"
            },
            "Location": {
              "name": "Location",
              "type": "str"
            },
            "Intake_purchase": {
              "name": "Intake_purchase",
              "type": "str"
            },
            "Type": {
              "name": "Type",
              "type": "str"
            },
            "PFBS": {
              "name": "PFBS",
              "type": "float"
            },
            "HFPO_DA": {
              "name": "HFPO_DA",
              "type": "int"
            },
            "PFHpA": {
              "name": "PFHpA",
              "type": "float"
            },
            "PFHxS": {
              "name": "PFHxS",
              "type": "int"
            },
            "ADONA": {
              "name": "ADONA",
              "type": "int"
            },
            "PFOA": {
              "name": "PFOA",
              "type": "float"
            },
            "PFOS": {
              "name": "PFOS",
              "type": "float"
            },
            "PFNA": {
              "name": "PFNA",
              "type": "int"
            },
            "PFOA_PFOS": {
              "name": "PFOA_PFOS",
              "type": "float"
            },
            "Sum_of_PFAS": {
              "name": "Sum_of_PFAS",
              "type": "float"
            },
            "Units": {
              "name": "Units",
              "type": "str"
            },
            "LATITUDE": {
              "name": "LATITUDE",
              "type": "float"
            },
            "LONGITUDE": {
              "name": "LONGITUDE",
              "type": "float"
            },
            "Aquifer_Source": {
              "name": "Aquifer_Source",
              "type": "str"
            },
            "River_Basin": {
              "name": "River_Basin",
              "type": "str"
            },
            "Aquifer_General": {
              "name": "Aquifer_General",
              "type": "str"
            },
            "Land_Use": {
              "name": "Land_Use",
              "type": "str"
            }
          }
        },
        "https://services8.arcgis.com/Xcpl3GIMvkCI3oFI/arcgis/rest/services/Ohio_River_Marinas_WFL1/FeatureServer": {
          "location": "https://services8.arcgis.com/Xcpl3GIMvkCI3oFI/arcgis/rest/services/Ohio_River_Marinas_WFL1/FeatureServer",
          "type": "layer",
          "description": "Publicly available layer findable on ArcGIS Online.",
          "fairness": "Fir",
          "format": "web",
          "creator": [
            {
              "name": "ArcGIS Online",
              "type": "organization"
            }
          ],
          "geographical_area": "Kentucky"
        },
        "https://kygisserver.ky.gov/arcgis/rest/services/WGS84WM_Services/Ky_Water_WGS84WM/MapServer/11": {
          "location": "https://kygisserver.ky.gov/arcgis/rest/services/WGS84WM_Services/Ky_Water_WGS84WM/MapServer/11",
          "type": "layer",
          "description": "Locations of water lines in Kentucky.",
          "fairness": "Fir",
          "format": "web",
          "creator": [
            {
              "name": "https://kygeoportal.ky.gov/",
              "type": "URL"
            }
          ],
          "alternate_locations": [
            "https://uky-edu.maps.arcgis.com/home/item.html?id=29713c2b8be14534943b8e2e5fa16daa"
          ],
          "geographical_area": "Kentucky"
        }
       }
    }



Validating
~~~~~~~~~~
Command Line Signature
----------------------

.. code-block:: console

    miagis validate <metadata_json_file>


Description
-----------
Validate the input file against the metadata JSON Schema in the :doc:`jsonschema` 
section. Additionally, perform some other logical checks such as making sure all 
references exist, and that keys and id attributes match.


Options
-------
No options at this time.


Outputs
-------
Prints messages to the console about errors in the metadata.


Examples
--------
Typical run.

GIS_MEATADATA.json:

.. code-block:: console

    {
      "format_version": "DRAFT_MIAGIS_VERSION_0.1",
      "entry_version": 1,
      "entry_id": "KY PFAS Paper",
      "date": "2022-07-07",
      "description": "Data used for the paper titled \"A geospatial and binomial logistic regression model to prioritize sampling for per- and polyfluorinated alkyl substances in public water systems\". DOI: https://doi.org/10.1002/ieam.4614",
      "products": [
        "Map 1 Potential hot-spot map"
      ],
      "resources": {
        "PFAS_detected_sites": {
          "location": "https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_detected_sites2019/FeatureServer",
          "creator": [
            {
              "name": "Kentucky Department of Environmental Protection",
              "type": "organization"
            }
          ],
          "sources": [
            "https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf"
          ],
          "fairness": "FAIR",
          "format": "web",
          "type": "layer",
          "description": "",
          "geographical_area": "Kentucky",
          "alternate_locations": []
        },
        "layer_data/PFAS_detected_sites.json": {
          "location": "layer_data/PFAS_detected_sites.json",
          "type": "layer",
          "description": "List of the water systems in which PFAS were detected.",
          "fairness": "FAIR",
          "format": "json",
          "creator": [
            {
              "name": "Kentucky Department of Environmental Protection",
              "type": "organization"
            }
          ],
          "sources": [
            "https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf"
          ],
          "geographical_area": "Kentucky",
          "alternate_locations": [
            "https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/PFAS_detected_sites2019/FeatureServer"
          ],
          "schema": {
            "asdf": "qwer"
          },
          "fields": {
            "__OBJECTID": {
              "name": "__OBJECTID",
              "type": "int"
            },
            "TYPE": {
              "name": "TYPE",
              "type": "str"
            },
            "WATER_SYSTEM": {
              "name": "WATER_SYSTEM",
              "type": "str"
            },
            "LATITUDE": {
              "name": "LAT",
              "type": "float"
            },
            "LONGITUDE": {
              "name": "LONGITUDE",
              "type": "float"
            },
            "PFAS": {
              "name": "PFAS",
              "type": "float"
            },
            "CODE": {
              "name": "CODE",
              "type": "str"
            }
          }
        }
      }
    }
    

Console:

.. code-block:: console
    
    >miagis validate metadata_file_path
    The value for ['resources']['PFAS_detected_sites']['alternate_locations'] cannot be empty.
    The product, Map 1 Potential hot-spot map, is not in "resources".
    The source, https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf, for resource, PFAS_detected_sites, does not exist in resources.
    The source, https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf, for resource, layer_data/PFAS_detected_sites.json, does not exist in resources.
    The "name" property for field, LATITUDE, for resource, layer_data/PFAS_detected_sites.json, does not match its key value.




Print Map Layers
~~~~~~~~~~~~~~~~
Command Line Signature
----------------------

.. code-block:: console

    miagis print_map_layers <metadata_json> [--save_path=<save_path>]


Description
-----------
Go through the metadata file, pull out each map and display its layers. This 
command was added so that the simple structure of the project can be seen without 
having to sort through all of the files. With this command, if the metadata is 
constructed as expected it is easy to see the maps and their layers.


Options
-------
--save_path:

If provided save the console output to a text file.


Outputs
-------
Pretty print the maps and layers of the metadata.


Examples
--------
Typical run.

Console:

.. code-block:: console
    
    >miagis print_map_layers metadata_file_path
    Maps:
    	Map 1 Potential hot-spot map
    		Layers:
    			PFAS_detected_sites
    			PFAS_sampling_and_purchasing_and_intake_detail
    			TRI_DATA_IN_KENTUCKY
    			Risk map with landfill
    			Ohio_River_Marinas_WFL1 - Ohio River
    			Ky_Water_Resources_Polygons_DOW_SWAPP_Zone_2
    			Ky_Water_Resources_Polygons_DOW_SWAPP_Zone_1
    			Ky_Water_Resources_Polygons_DOW_SWAPP_Zone_3
    			waterIntake
    			Surfacewater_sampled_and_detected
    			gw_sampled_and_detected
    			groundwater_not_detected
    			Surface_water_sampled_and_not_detected
    			WATER_SYSTEMS_IN_KENTUCKY
    			water_district
    			Model_says_NO
    			hot-spot_map
    			Model_says_yes
    			Waste WTP outfls
    			Kentucky County Polygons
    			Blank White Vector Basemap

    	US map
    		Layers:
    			TRI_only_A
    			TRI_CA-HI
    			TRI__IA-LA
    			TRI__MA-MT
    			TRI__NC-OH
    			TRI__TX-WV
    			TRI__OK-TN
    			USA States Generalized1
    			USA_State_Internal_Boundaries
    			Blank White Vector Basemap



.. _GitHub: https://github.com/MoseleyBioinformaticsLab/miagis