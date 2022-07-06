User Guide
==========

Description
~~~~~~~~~~~

MIAGIS was created to help automate the process of creating a meatadata file for GIS 
data depositions. It is a command line tool that goes through all files and folders 
in the current directory and makes a best effort to fill in all of the metadata fields 
for the file. The resulting metadata file is saved as GIS_METADATA.json in the current 
directory. It is not expected for this initially generated file to be perfect, therefore 
the "validate" command of MIAGIS should be used to generate a list of problems with the 
metadata that the user needs to address manually. 

The overall expected workflow is for the user to gather all of their files for the deposition 
into a directory with the expected directory structure (explained below), use the "build" 
command of MIAGIS to create an initial metadata file, and then use the "validate" command 
to get a list of problems to fix and fix them until the "validate" command reports nothing.


Installation
~~~~~~~~~~~~

The MIAGIS package runs under Python 3.7+. Use pip_ to install.
Starting with Python 3.4, pip_ is included by default.


Install on Linux, Mac OS X
--------------------------

.. code:: bash

   python3 -m pip install miagis


Install on Windows
------------------

.. code:: bash

   py -3 -m pip install miagis


Upgrade on Linux, Mac OS X
--------------------------

.. code:: bash

   python3 -m pip install miagis --upgrade


Upgrade on Windows
------------------

.. code:: bash

   py -3 -m pip install miagis --upgrade



Install inside virtualenv
-------------------------

For an isolated install, you can run the same inside a virtualenv_.

.. code:: bash

   $ virtualenv -p /usr/bin/python3 venv            # create virtual environment, use python3 interpreter

   $ source venv/bin/activate                       # activate virtual environment

   $ python3 -m pip install miagis        # install academic_tracker as usual

   $ deactivate                                     # if you are done working in the virtual environment

Get the source code
~~~~~~~~~~~~~~~~~~~

Code is available on GitHub: https://github.com/MoseleyBioinformaticsLab/miagis

You can either clone the public repository:

.. code:: bash

   $ https://github.com/MoseleyBioinformaticsLab/miagis.git

Or, download the tarball and/or zipball:

.. code:: bash

   $ curl -OL https://github.com/MoseleyBioinformaticsLab/miagis/tarball/main

   $ curl -OL https://github.com/MoseleyBioinformaticsLab/miagis/zipball/main

Once you have a copy of the source, you can embed it in your own Python package,
or install it into your system site-packages easily:

.. code:: bash

   $ python3 setup.py install

Dependencies
~~~~~~~~~~~~

The MIAGIS package depends on several Python libraries. The ``pip`` command
will install all dependencies automatically, but if you wish to install them manually,
run the following commands:

   * docopt_ for creating the command-line interface.
      * To install docopt_ run the following:

        .. code:: bash

           python3 -m pip install docopt  # On Linux, Mac OS X
           py -3 -m pip install docopt    # On Windows
           
   * jsonschema_ for validating JSON.
      * To install the jsonschema_ Python library run the following:

        .. code:: bash

           python3 -m pip install jsonschema  # On Linux, Mac OS X
           py -3 -m pip install jsonschema    # On Windows
           
   * fuzzywuzzy_ for fuzzy matching publication titles.
      * To install the fuzzywuzzy_ Python library run the following:

        .. code:: bash

           python3 -m pip install fuzzywuzzy  # On Linux, Mac OS X
           py -3 -m pip install fuzzywuzzy    # On Windows
           
   * pandas_ for easy data manipulation.
      * To install the pandas_ Python library run the following:

        .. code:: bash

           python3 -m pip install pandas  # On Linux, Mac OS X
           py -3 -m pip install pandas    # On Windows
                      

Basic usage
~~~~~~~~~~~

MIAGIS can run without any inputs for the build command, but the resulting metadata 
file won't be as filled out as it could be with some simple inputs. Typically, 
users will want to create and provide a base metadata file and a file properties 
file. Details about the files and other inputs are in the :doc:`tutorial`.

.. code-block:: console  
 
 Usage:
    miagis build [options]
    miagis validate <metadata_json>

 Options:
    --help                              Show this help documentation.
    --file_properties=<file_path>       Filepath to a csv, xlsx, or JSON file with file properties.
    --json_schemas=<file_path>          Filepath to a JSON file with schemas for different JSON formats.
    --exact_name_match                  If used then file name matching will be done exactly instead of fuzzy.
    --remove_optional_fields            If used then delete optional metadata fields that are empty from files.

 Base Metadata Options:
    --entry_version=<integer>           Set the entry_version field for the metadata. Should be an integer starting from 1. [default: 1]
    --entry_id=<id>                     Set the entry_id field for the metadata.
    --description=<description>         Set the description field for the metadata
    --base_metadata=<file_path>         Filepath to a JSON file with the base metadata fields to use.




.. _pip: https://pip.pypa.io/
.. _virtualenv: https://virtualenv.pypa.io/
.. _docopt: https://pypi.org/project/docopt/
.. _jsonschema: https://pypi.org/project/jsonschema/
.. _fuzzywuzzy: https://pypi.org/project/fuzzywuzzy/
.. _pandas: https://pypi.org/project/pandas/
