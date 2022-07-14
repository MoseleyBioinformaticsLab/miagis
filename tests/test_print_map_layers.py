# -*- coding: utf-8 -*-
import pytest

import pathlib
import json
import shutil
import os
import time

from miagis.print_map_layers import print_map_layers

TESTING_DIR = "testing_dir"

def test_print_map_layers_no_save(capsys):
    with open(pathlib.Path("tests", "testing_files", "GIS_METADATA.json"), "r") as f:
        metadata = json.loads(f.read())

    print_map_layers(metadata)
    captured = capsys.readouterr()

    assert captured.out == 'Maps:\n\tCombined map\n\t\tLayers:\n\t\t\tPFAS_sampling_and_purchasing_and_intake_detail\n\t\t\tOhio_River_Marinas_WFL1 - Ohio River\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_2\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_1\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_3\n\t\t\twaterIntake\n\t\t\tWATER_SYSTEMS_IN_KENTUCKY\n\t\t\twater_district\n\t\t\thot-spot_map\n\t\t\tWaste WTP outfls\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky Water Lines1\n\t\t\tNew_KDEP_PFAS_Data_Compiled-2020_with_latlong\n\t\t\tKy_Wastewater_WGS84WM - Sewer Lines\n\t\t\tKy_Wastewater_WGS84WM - Water Treatment Plants\n\t\t\tKy_WaterResources_Polygons_WGS84WM - Sinkhole Drainage Areas\n\t\t\tKy_CountyLines_WGS84WM - County Lines\n\n\tWater map\n\t\tLayers:\n\t\t\tPFAS_sampling_and_purchasing_and_intake_detail\n\t\t\tOhio_River_Marinas_WFL1 - Ohio River\n\t\t\twaterIntake\n\t\t\twater_district\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky Water Lines1\n\t\t\tNew_KDEP_PFAS_Data_Compiled-2020_with_latlong\n\t\t\tKentucky County Polygons\n\n\tMap Sewer\n\t\tLayers:\n\t\t\tKy_WaterResources_Polygons_WGS84WM - Sinkhole Drainage Areas\n\t\t\tKy_Wastewater_WGS84WM - Sewer Lines\n\t\t\tWaste WTP outfls\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky County Polygons\n\n\tSWAPP map Ky\n\t\tLayers:\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_2\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_1\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_3\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky County Polygons\n\n\tHotspot Map\n\t\tLayers:\n\t\t\thot-spot_map\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky County Polygons\n\n' + "\n"




@pytest.fixture
def save_path_fixture():
    save_dir_name = TESTING_DIR
    save_path = os.path.join(save_dir_name, "test.txt")
    os.mkdir(save_dir_name)
    time_to_wait = 10
    time_counter = 0
    
    while not os.path.exists(save_dir_name):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise FileNotFoundError(save_dir_name + " was not created within " + str(time_to_wait) + " seconds, so it is assumed that it won't be and something went wrong.")
    
    yield save_dir_name, save_path
    
    os.remove(save_path)
    time_counter = 0
    while os.path.exists(save_path):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise FileExistsError(save_path + " was not deleted within " + str(time_to_wait) + " seconds, so it is assumed that it won't be and something went wrong.")
            
    
    os.rmdir(save_dir_name)
    time_counter = 0
    while os.path.exists(save_dir_name):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise FileExistsError(save_dir_name + " was not deleted within " + str(time_to_wait) + " seconds, so it is assumed that it won't be and something went wrong.")





def test_print_map_layers_save(save_path_fixture):
    
    save_dir_name, save_path = save_path_fixture
    
    with open(pathlib.Path("tests", "testing_files", "GIS_METADATA.json"), "r") as f:
        metadata = json.loads(f.read())

    print_map_layers(metadata, save_path)

    time_to_wait = 10
    time_counter = 0
    while not os.path.exists(save_path):
        time.sleep(1)
        time_counter += 1
        if time_counter > time_to_wait:
            raise FileNotFoundError(save_path + " was not created within " + str(time_to_wait) + " seconds, so it is assumed that it won't be and something went wrong.")
    
    with open(save_path, encoding = "utf-8") as document:
        lines = document.readlines()
        
    saved_text = "".join(lines)
        
    assert saved_text == 'Maps:\n\tCombined map\n\t\tLayers:\n\t\t\tPFAS_sampling_and_purchasing_and_intake_detail\n\t\t\tOhio_River_Marinas_WFL1 - Ohio River\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_2\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_1\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_3\n\t\t\twaterIntake\n\t\t\tWATER_SYSTEMS_IN_KENTUCKY\n\t\t\twater_district\n\t\t\thot-spot_map\n\t\t\tWaste WTP outfls\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky Water Lines1\n\t\t\tNew_KDEP_PFAS_Data_Compiled-2020_with_latlong\n\t\t\tKy_Wastewater_WGS84WM - Sewer Lines\n\t\t\tKy_Wastewater_WGS84WM - Water Treatment Plants\n\t\t\tKy_WaterResources_Polygons_WGS84WM - Sinkhole Drainage Areas\n\t\t\tKy_CountyLines_WGS84WM - County Lines\n\n\tWater map\n\t\tLayers:\n\t\t\tPFAS_sampling_and_purchasing_and_intake_detail\n\t\t\tOhio_River_Marinas_WFL1 - Ohio River\n\t\t\twaterIntake\n\t\t\twater_district\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky Water Lines1\n\t\t\tNew_KDEP_PFAS_Data_Compiled-2020_with_latlong\n\t\t\tKentucky County Polygons\n\n\tMap Sewer\n\t\tLayers:\n\t\t\tKy_WaterResources_Polygons_WGS84WM - Sinkhole Drainage Areas\n\t\t\tKy_Wastewater_WGS84WM - Sewer Lines\n\t\t\tWaste WTP outfls\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky County Polygons\n\n\tSWAPP map Ky\n\t\tLayers:\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_2\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_1\n\t\t\tKy_Water_Resources_Polygons_DOW_SWAPP_Zone_3\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky County Polygons\n\n\tHotspot Map\n\t\tLayers:\n\t\t\thot-spot_map\n\t\t\tBlank White Vector Basemap\n\t\t\tKentucky County Polygons\n\n'




@pytest.fixture(scope="module", autouse=True)
def cleanup(request):
    """Cleanup a testing directory once we are finished."""
    def remove_test_dir():
        if os.path.exists(TESTING_DIR):
            shutil.rmtree(TESTING_DIR)
    request.addfinalizer(remove_test_dir)