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
   :target: https://doi.org/10.3390/metabo11030163
   :alt: Citation link

.. image:: https://img.shields.io/github/stars/MoseleyBioinformaticsLab/miagis.svg?style=social&label=Star
    :target: https://github.com/MoseleyBioinformaticsLab/miagis
    :alt: GitHub project

|


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
Academic Tracker has several commands and options. The simplest most common use 
case is simply:

.. code:: bash
    
    academic_tracker author_search config_file.json

Academic Tracker's behavior can be quite complex though, so it is highly encouraged 
to read the `guide <https://moseleybioinformaticslab.github.io/academic_tracker/guide.html>`_ 
and `tutorial <https://moseleybioinformaticslab.github.io/academic_tracker/tutorial.html>`_.


Creating The Configuration JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A configuration JSON file is required to run Academic Tracker, but initially creating 
it the first time can be burdensome. Unfortunately, there is no easy solution for 
this. It is encouraged to read the configuration JSON section in `jsonschema <https://moseleybioinformaticslab.github.io/academic_tracker/jsonschema.html>`_ 
and use the example there to create it initially. The add_authors command can help 
with building the Authors section if you already have a csv file with author 
information. A good tool to help track down pesky JSON syntax errors is `here <https://csvjson.com/json_validator>`__. 
There are also examples in the `example_configs <https://github.com/MoseleyBioinformaticsLab/academic_tracker/tree/main/example_configs>`__ 
directory of the GitHub repo. There are also more example in the supplemental 
material of the paper https://doi.org/10.6084/m9.figshare.19412165.



          
Mac OS Note
~~~~~~~~~~~
When you try to run the program on Mac OS you may get an SSL error.

    certificate verify failed: unable to get local issuer certificate
    
This is due to a change in Mac OS and Python. To fix it go to to your Python 
folder in Applications and run the Install Certificates.command shell command 
in the /Applications/Python 3.x folder. This should fix the issue.



License
~~~~~~~
This package is distributed under the BSD `license`.


.. _GitHub: https://github.com/MoseleyBioinformaticsLab/miagis
.. _Pages: https://moseleybioinformaticslab.github.io/miagis/
.. _PyPI: https://pypi.org/project/miagis
.. _pip: https://pip.pypa.io