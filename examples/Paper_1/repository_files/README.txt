This is the FigShare repository for the paper, A geospatial and binomial logistic regression model to prioritize sampling for per- and polyfluorinated alkyl substances in public water systems.
DOI: https://doi.org/10.1002/ieam.4614

The primary results of this paper were 2 maps that were created in ArcGIS Online.
Map1: https://uky-edu.maps.arcgis.com/home/item.html?id=b191e64fbdef44a78d6bbf1f68ef4d8e
Map2: https://uky-edu.maps.arcgis.com/home/item.html?id=ed727263056e411ca2a7a86587a57f65

The individual layers for each map are included in this repository in the layer_data folder. Each layer's data is in 3 formats, CSV, GEOJSON, and ESRIJSON.
Data that was used to eventually create the layers and any other miscellaneous documents are in the "other" folder.
Metadata about the files are in the GIS_METADATA.json file.

Description of layers in Map-1

groundwater_not_detected
Source - Kentucky Department of Environmental Proetection Agency(KDEP) report 2019
url-https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf
list of water systems with groundwater source in which PFAS were not detected.

gw_sampled and detected.csv-groundwater_not_detected
Source - Kentucky Department of Environmental Proetection Agency(KDEP) report 2019
Link-https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf
listed the water systems with groundwater source in which PFAS were detected.

Hot spot map
Source- Kentucky Department of Environmental Proetection Agency(KDEP)
The data includes all the operation sites, hazardous sites and aiports 
The indicator scores were assigned to all sites considering the magnitude of PFAS produced.
Using all sites and indicator scores, Hot-spot map is present in this layer.
Note- location of superfund sites and manufacturing sites were emailed by KDEP staffs 
The location of Kentucky airport were extracted from the website URL:https://www.latlong.net/category/airports-236-19.html


Ky_Water_Resources_Polygons_DOW_SWAPP_Zone_1
Source- Kygeoportal 
The layer is extracted from KYgeoportal using the URL
url-https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/SWAPP_Zone1/FeatureServer

Ky_Water_Resources_Polygons_DOW_SWAPP_Zone_2
Source- Kygeoportal 
The Layer is extracted from KYgeoportal using the URL
url-https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/SWAPP_Zone2/FeatureServer
 
Ky_Water_Resources_Polygons_DOW_SWAPP_Zone_3
Source- Kygeoportal 
The layer is extracted from KYgeoportal using the URL
URL-https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/SWAPP_Zone3_Copy/FeatureServer

Model_says_NO.csv
Source-Pennell lab
Statistical model result that says there are less chances of PFAS detection in water systems. 

Model_says_yes.csv
Source-Pennell lab
Statistical model result that says there are chances of PFAS detection in water systems. 

PFAS_detected_sites.csv
Source- Kentucky Department of Environmental Protection Agency PFAS report 2019
Link-https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf
list of the water systems in which PFAS were detected.

PFAS_sampling_and_purchasing_and_intake_detail
Source-Kentucky Department of Environmental Protection Agency PFAS report 2019
Link-https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf
list of all water systems in which PFAS were sampled.

Risk_map_with_landfill
Source- Kentucky Department of Environmental Proetection Agency(KDEP)
The data includes all the operation sites, landfill sites, superfund sites and aiports 
The indicator scores were assigned to all sites considering the magnitude of PFAS produced.
Using all sites and indicator scores, Hot-spot map is present in this layer.
Note- location of superfund sites, landfill sites and manufacturing sites were emailed by KDEP staffs 
The location of Kentucky airport were extracted from the website URL:https://www.latlong.net/category/airports-236-19.html

Surface_water_sampled_and_not_detected
Source-Kentucky Department of Environmental Protection Agency(KDEP) PFAS report 2019
Link-https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf
list of all water systems with surface water source in which PFAS were not detected.

Surface_water_sampled_and_detected
Source-Kentucky Department of Environmental Protection Agency(KDEP) PFAS report 2019
Link-https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf
list of all water systems with surface water source in which PFAS were detected.

TRI_IA_LA.csv
Source- Toxic release Inventory data-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of the states that starts with IA to LA. 
States name were alphabetically arranged.
The indicator scores were assigned to all sites considering the magnitude of PFAS produced.

TRI_MA_MT.csv
Source- Toxic release Inventory data-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of the states that starts with MA to MT. 
States name were alphabetically arranged.
The indicator scores were assigned to all sites considering the magnitude of PFAS produced.

TRI_NC_OH.csv
Source- Toxic release Inventory data-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of the states that starts with NC to OH. 
States name were alphabetically arranged.
The indicator scores were assigned to all sites considering the magnitude of PFAS produced.


TRI_CA_HI.csv
Source- Toxic release Inventory data; URL-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of the states that starts with CA to HI. 
States name were alphabetically arranged.
The indicator scores were assigned to all sites considering the magnitude of PFAS produced.

TRI_TX_WV.csv
Source- Toxic release Inventory data; URL-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of the states that starts with TX to WV. 
States name were alphabetically arranged.
The indicator scores were assigned to all sites considering the magnitude of PFAS produced.

TRI_OK_TN.csv
Source- Toxic release Inventory data; URL-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of the states that starts with OK to TN. 
States name were alphabetically arranged.
The indicator scores were assigned to all sites considering the magnitude of PFAS produced.


TRI_DATA_IN_KENTUCKY.csv
Source- Toxic release Inventory data; URL-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of Kentucky.
The indicator scores were assigned to all sites considering the magnitude of PFAS produced.


TRI_only_A.csv
Source- Toxic release Inventory data; URL-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of states that starts with A.
States name were alphabetically arranged.

water_district.csv
Source- WRIS 
URL-https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/water_district_Kentucky/FeatureServer
Note- The data was emailed by WRIS staff


WATER_SYSTEMS_IN_KENTUCKY.csv
Source- Kygeoportal
URL-https://services.arcgis.com/vQ8kO5zdqETeirEL/arcgis/rest/services/Watersystemin_Kentucky/FeatureServer
It includes water systems in Kentucky


waterintake
Source-KYgeoportal and Kentucky Department of Environmental Proetection Agency(KDEP) report 2019
It provides information about water systems that has PFAS detection. Data were compared and reported accordingly. 


Others data
All LIST REPORTS RAW
Source- Kentucky Department of Environmental Proetection Agency(KDEP)
It provides all the sites that were provided by KDEP.
Note- DATA was emailed by KDEP staffs

all_12_mile_water_risk_TRI.csv
Source- TRI database and Kygeoportal
It includes the sites and water systems that are in 12 miles

gis_distance_martix.py
Source-Pennel Lab
It was used to get the sites that are in 12 miles from the water systems

HISTORIC LANDFILLS MAP- 2019 RAW.csv
Source-Kentucky Department of Environmental Proetection Agency(KDEP)
It includes the location of landfill in Kentucky.
Note-DATA was emailed by KDEP staff.

KY_WATER_SYSTEMS
Source-KYgeoportal and Kentucky Department of Environmental Proetection Agency(KDEP) PFAS report-2019
It provides the locations of water systems that has PFAS detection.

Model result for regression.csv
Source- Pennell lab
It is the result of statistical model.

PFA_SITES.csv
source- Kentucky Department of Environmental Proetection Agency(KDEP) 
It includes all the list of potential PFAS users with indicator scores.

PFAS DRINKING WATER REPORT FINAL.pdf
Source- https://eec.ky.gov/Documents%20for%20URLs/PFAS%20Drinking%20Water%20Report%20Final.pdf


SUPERFUND_SITESRAW.xlsx
Source-Kentucky Department of Environmental Proetection Agency(KDEP)  
It includes the location of superfund sites in Kentucky.
Note- DATA was emailed by KDEP staffs.


TRI_2019_KY RAW.csv
Source-Toxic release Inventory data-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of Kentucky.


TRI_2019_US RAW.csv
Source-Toxic release Inventory data-https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present
It includes TRI data of United states.






















































