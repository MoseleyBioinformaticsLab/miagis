MIAGIS
================

.. image:: https://img.shields.io/pypi/v/miagis.svg
   :target: https://pypi.org/project/miagis
   :alt: Current library version

.. image:: https://img.shields.io/pypi/pyversions/miagis.svg
   :target: https://pypi.org/project/miagis
   :alt: Supported Python versions

.. image:: https://github.com/MoseleyBioinformaticsLab/miagis/actions/workflows/build.yml/badge.svg
   :target: https://github.com/MoseleyBioinformaticsLab/miagis/actions/workflows/build.yml
   :alt: Build status

.. image:: https://codecov.io/gh/MoseleyBioinformaticsLab/miagis/branch/main/graphs/badge.svg?branch=main
   :target: https://codecov.io/gh/MoseleyBioinformaticsLab/miagis
   :alt: Code coverage information

.. image:: https://img.shields.io/badge/DOI-10.3390%2Fmetabo11030163-blue.svg
   :target: https://doi.org/10.6084/m9.figshare.15218958
   :alt: Citation link

.. image:: https://img.shields.io/github/stars/MoseleyBioinformaticsLab/miagis.svg?style=social&label=Star
    :target: https://github.com/MoseleyBioinformaticsLab/miagis
    :alt: GitHub project

|


MIAGIS (Minimum Information About Geospatial Information System) was created to help automate the process of creating a metadata file for GIS 
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


Links
~~~~~

   * MIAGIS @ GitHub_
   * MIAGIS @ PyPI_
   * Documentation @ Pages_


Installation
~~~~~~~~~~~~
The MIAGIS package runs under Python 3.7+. Use pip_ to install.
Starting with Python 3.4, pip_ is included by default. Be sure to use the latest 
version of pip as older versions are known to have issues grabbing all dependencies.


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



Quickstart
~~~~~~~~~~
First create a directory with directories for "layer_data", "map_data", and "other" 
as necessary. Then run the "build" command.

MIAGIS has many options. The simplest use case is:

.. code:: bash
    
    miagis build

Although this will run and generate a metadata file, MIAGIS can do a lot more by 
using some of the simplest options. A more common use case is:

.. code:: bash
    
    miagis build --remove_optional_fields --add_resources --resource_properties <filepath> --base_metadata <filepath>
    
Detailed descriptions of the options and input files are in the `tutorial <https://moseleybioinformaticslab.github.io/miagis/tutorial.html>`_.

MIAGIS's behavior can be quite complex, so it is highly encouraged to read the 
`guide <https://moseleybioinformaticslab.github.io/miagis/guide.html>`_ and `tutorial <https://moseleybioinformaticslab.github.io/miagis/tutorial.html>`_.
There are also examples available in the examples folder on the GitHub_ repo.

          
Mac OS Note
~~~~~~~~~~~
When you try to run the program on Mac OS you may get an SSL error.

    certificate verify failed: unable to get local issuer certificate
    
This is due to a change in Mac OS and Python. To fix it go to to your Python 
folder in Applications and run the Install Certificates.command shell command 
in the /Applications/Python 3.x folder. This should fix the issue.



License
~~~~~~~
This package is distributed under the BSD `license <https://moseleybioinformaticslab.github.io/miagis/license.html>`__.


.. _GitHub: https://github.com/MoseleyBioinformaticsLab/miagis
.. _Pages: https://moseleybioinformaticslab.github.io/miagis/
.. _PyPI: https://pypi.org/project/miagis
.. _pip: https://pip.pypa.io