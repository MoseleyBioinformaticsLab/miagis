# -*- coding: utf-8 -*-
"""
This module contains the code to print and save map structure.
"""

import pathlib

def print_map_layers(metadata: dict, save_path: str =""):
    """Find the maps and layers in metadata and pretty print them.
    
    Args:
        metadata: A valid metadata to find maps in.
        save_path: path to save the output to a file, doesn't save if it is an empty string.
    """
    
    maps_dict = {}
    for resource_name, resource_properties in metadata["resources"].items():
        if resource_properties["type"] == "map":
            layers = []
            if "sources" in resource_properties:
                for source in resource_properties["sources"]:
                    if metadata["resources"][source]["type"] == "layer":
                        layers.append(source)
            maps_dict[resource_name] = layers
    
    print_string = "Maps:\n"
    for map_name, layers in maps_dict.items():
        print_string += "\t" + map_name + "\n"
        print_string += "\t\tLayers:\n"
        for layer in layers:
            print_string += "\t\t\t" + layer + "\n"
        print_string += "\n"
            
    print(print_string)
    
    if save_path:
        extension = pathlib.Path(save_path).suffix[1:].lower()
        if extension != "txt":
            save_path += ".txt"
        with open(save_path, 'wb') as outFile:
            outFile.write(print_string.encode("utf-8"))