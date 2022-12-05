JSON Schema
===========

MIAGIS uses and produces JSON files in its execution. This document describes 
their structure and gives examples. `JSON Schema <https://json-schema.org/>`_ is used 
here to describe the structure and used in the program to validate inputs.

Metadata JSON
~~~~~~~~~~~~~
The main JSON file is of course the metadata that is generated and validated by 
MIAGIS. The metadata schema was generated out of a need to publish GIS data in 
the FAIRest way possible that is not too burdensome. MIAGIS was then born out of 
a need to relieve some of the burden of creating the metadata file.

There are 2 main sections to the metadata, the base and the resources. The base 
is the collection of simple properties that describe the overall project and 
deposition. While the "resources" property details all of the resources of the 
project, such as files, layers, and maps. "resources" is a JSON object where the 
keys are a unique id for the resource, which could be a name, filepath, or URL.

Simple Schema
-------------

.. code-block:: console
    
    {
      "format_version" : "DRAFT_MIAGIS_VERSION_0.1", # MIAGIS - Minimum Information About GIS
      "entry_version" : <version>, # starting with "1"
      "entry_id" : <entry_id>,
      "date" : <date>,
      "description" : <description>, 
      "products" : [ <id>, ... ],
      "resources" : { 
         <id> : {
          "location" : <filepath | URL | DOI>,
          "alternate_locations" : [<filepath | URL | DOI>, ...], # optional
          "type" : <map | layer | statistics | program | other | ...>, 
          "creator" : [ { "name" : <organization | author>, "type" : <organization | author> }, ... ] # optional
          "description" : "...", 
          "fairness" : <FAIR>,
          "format" : <json | xml | csv | txt | web ...>,
          "schema" : <ESRI | undefined | ...>, # optional
          "fields" : { <fieldname> : {  # optional for "program" and "other" type, or when the file is not Accessible.
              "name" :  <fieldname>, 
              "type": <ontology_term | int | float | str>, 
              "identifier" : <id>, # optional, but should be specified when the identifier is different from the <fieldname> or is nested in a data structure. Colons should be used to separate nested identifiers.
              "identifier%type" : <column_name | column_index | key_name | nested>, # optional 
              ... }, 
            ... },
          "sources" : [ <id>, ... ] # optional, but should be provided if possible.
          },
      ... }
    }

Validating JSON Schema
----------------------

.. code-block:: console

    {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    
    "type":"object",
    "properties":{
        "format_version":{"type":"string", "minLength":1},
        "entry_version":{"type":"integer", "minimum":1},
        "entry_id":{"type":"string", "minLength":1},
        "date":{"type":"string", "minLength":1},
        "description":{"type":"string", "minLength":1},
        "products":{"type":"array", "items":{"type":"string", "minLength":1}},
        "resources":{"type":"object",
                     "minProperties":1,
                     "additionalProperties":{"type":"object",
                                             "properties":{
                                                 "location":{"type":"string", "minLength":1},
                                                 "alternate_locations":{"type":"array", "items":{"type":"string", "minLength":1}, "minItems":1},
                                                 "type":{"type":"string", "minLength":1},
                                                 "fairness":{"type":"string", "pattern":"(?i)^f?a?i?r?$"},
                                                 "format":{"type":"string", "minLength":1},
                                                 "schema":{"type":["string", "object"], "minLength":1},
                                                 "sources":{"type":"array", "items":{"type":"string", "minLength":1}},
                                                 "description":{"type":"string", "minLength":1},
                                                 "creator":{"type":"array", "minItems":1, "items":{"type":"object",
                                                                                                   "properties":{
                                                                                                       "name":{"type":"string", "minLength":1},
                                                                                                       "type":{"type":"string", "minLength":1, "enum":["URL", "organization", "author", "DOI"]}},
                                                                                                   "required":["name", "type"]}},
                                                 "fields":{"type":"object",
                                                           "minProperties":1,
                                                           "additionalProperties":{"type":"object",
                                                                                   "properties":{
                                                                                       "name":{"type":"string", "minLength":1},
                                                                                       "type":{"type":"string", "enum":["ontology_term", "int", "float", "str"]},
                                                                                       "identifier":{"type":["string", "integer"], "minLength":1},
                                                                                       "identifier%type":{"type":"string", "minLength":1}},
                                                                                   "if":{"anyOf":[
                                                                                       {"properties":{"identifier":{"type":["string", "integer"], "minLength":1}},
                                                                                        "required":["identifier"]},
                                                                                       {"properties":{"identifier%type":{"type":"string", "minLength":1}},
                                                                                        "required":["identifier%type"]}]},
                                                                                   "then":{"required":["name", "type", "identifier", "identifier%type"]},
                                                                                   "else":{"required":["name", "type"]}}}},
                                             "if":{"anyOf":[
                                                     {"properties":{"type":{"anyOf":[{"const":"program"},
                                                                                     {"const":"other"}]}}},
                                                     {"properties":{"format":{"const":"web"}}}]},
                                             "then":{"required":["location", "type", "fairness", "format", "description"]},
                                             "else":{"required":["location", "type", "fairness", "format", "description", "fields"]}}},
        },
    "required":["format_version", "entry_version", "entry_id", "date", "description", "products", "resources"]}


Sections
--------
Base Properties
+++++++++++++++
format_version: Required

String that describes the version of the metadata schema being used. The current 
latest version is "DRAFT_MIAGIS_VERSION_0.1". MIAGIS sets this to the version it 
generates by default.
  
entry_version: Required

An integer starting from 1. This should be incremented everytime the deposition 
changes or is updated. MIAGIS sets this to 1 by default.

entry_id: Required

A unique id assigned to a deposition to easily identify it. This can or cannot 
change as the deposition is changed or updated depending on user preference.

date: Required

A string with the date of the metadata creation or deposition creation or update. 
MIAGIS fills this in by default with the date it is ran with the format "YYYY-MM-DD".

description: Required

A description of the deposition or project.

products:  Required

A list of resource id's that are the new resources created during the project.


Resources Properties
++++++++++++++++++++
location: Required

A string that is the location of the resource. This can be a file path within the 
deposition directory, a URL, or a DOI for example. MIAGIS sets file id's and locations 
to their relative location in the deposition directory by default.
      
alternate_locations: Optional

Similar to "location", but a list of strings instead of a single string. While 
"location" should be the main location for the resource alternate_locations can 
be other locations to get the same information. For example, a layer can be downloaded 
into many different formats, so each different format can have the other formats 
as alternate_locations, or a URL to where the layer is hosted online. If the 
--resource_properties option is used MIAGIS will accumulate all of the locations 
of matching resources and add them as alternate_locations for each matching resource.

type: Required

The type of resource. Typically one of "map", "layer", "statistics", "program", 
or "other". Specifica allowed values are not required, but when validating the 
metadata if the type is not "program" or "other" then the "fields" property is 
required.

creator: Optional

A list of JSON objects with keys for "name" and "type". Each object is a creator 
of the resource. This is used somewhat loosely, so for example an organization 
that merely hosts the resource can be considered a creator and added to this list. 
Typically, this will be organizations, authors, or URLs of the creators of the 
resource.

description: Required

A description of the resource. Typically just a few short words to describe what 
it is, but can be longer.

fairness: Required

A string with some combination of the letters "F", "A", "I", and "R". By default 
any files in the deposition directory are given "FAIR" since the data is being 
made completely publicly available, but some resources can't meet the full FAIR 
criteria. Maps and layers on the ArcGIS Online plaatform for example are "Fir" 
because they are findable, not accessible, but interoperable and reusable, but 
only on their platform, thus the lower case.

format: Required

The format of the resource. Typically the file extension or "web". By default 
MIAGIS uses the file extension.

schema: Optional

Either a string that describes the schema, a URL to the schema, or a dictionary 
of the valid `JSON Schema <https://json-schema.org/>`_ .

fields: Required if type is not "program" or "other" or "format" is not "web"

A JSON object where the keys are fieldnames and the values are "name", "type", 
"identifier", and "identifier%type". "name" is simply the key or fieldname repeated. 
"type" is one of "int", "float", "str", or "ontology_term". "identifier" is an 
optional way to identify the field. For instance, you can specify a column number. 
"identifier_type" would then need to be "column". If the identifier is different 
from the fieldname it is highly encouraged to use this field to specify how to 
get to the field. If it is a nested type use colons to seperate identifiers.
      
sources: Optional, but should be provided if possible

A list of resource ids that are sources to the resource. For instance, every map 
should put the layer resources as sources.



GIS Format Schemas
~~~~~~~~~~~~~~~~~~
MIAGIS is aware of the ESRIJSON format and the GEOJSON format. These are the JSON 
Schemas used to identify if an arbitrary JSON file is of that format.

ESRIJSON
--------

.. code-block:: console

    {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title":"In-built ESRI",
    
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

    
Single Feature GEOJSON
----------------------

.. code-block:: console
    
    {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title":"In-built GEOJSON Single Feature",
    
    "type":"object",
    "properties":{
        "type":{"type":"string", "enum":["Feature"]},
        "properties":{"type":["object", "null"]},
        "geometry":{"type":["null", "object"]}},
    "required":["type", "properties", "geometry"]
    }


Collection GEOJSON
------------------

.. code-block:: console
    
    {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title":"In-built GEOJSON Collection",
    
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


Schema List
~~~~~~~~~~~
The JSON Schema used to validate the --json_schemas option is given below.

.. code-block:: console

    {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "JSON Schemas List",
    
    "type":"array",
    "items":{"type":"object",
             "properties":{
                 "name":{"type":"string", "minLength":1},
                 "style":{"type":"string", "enum":["testing", "mapping"]},
                 "schema":{"type":"object"},
                 "schema_URL":{"type":"string", "minLength":1},
                 
                 "field_path":{"type":"string", "minLength":1},
                 "name_key":{"type":"string", "minLength":1},
                 "type_key":{"type":"string", "minLength":1},
                 "type_map":{"type":"object", "minProperties":1},
                 
                 "features_path":{"type":"string"},
                 "properties_key":{"type":"string", "minLength":1}},
             "required":["name", "schema", "style"],
             "allOF":[
                 {"if":{"properties":{"style":{"const":"mapping"}}},
                 "then":{"required":["field_path", "name_key", "type_key", "type_map"]},},
                 {"if":{"properties":{"style":{"const":"testing"}}},
                 "then":{"required":["features_path", "properties_key"]}}
                 ]
             }
    
    }




.. _jsonschema: https://json-schema.org/