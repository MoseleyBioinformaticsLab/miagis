#!/usr/bin/python3
""" 
 gis_distance_matrix.py
    Find the distance between all latitude and longitude points in 2 files and write out the locations that are within the given milage.
    The output file will contain both the rows of the input files for any points within the specified distance plus the distance appended to the end of the row.
    
 Usage:
    gis_distance_matrix.py <input_csv_1> <latitude1> <longitude1> <input_csv_2> <latitude2> <longitude2> <maximum_miles> <output_filename> [options]
    gis_distance_matrix.py --help

    <input_csv_1> - input csv file with longitude and latitude data in the columns.
    <latitude1> - the integer column number (starting from 0) where the latitude numbers are in input_csv_1.
    <longitude1> - the integer column number (starting from 0) where the longitude numbers are in input_csv_1.
    <input_csv_2> - input csv file with longitude and latitude data in the columns.
    <latitude2> - the integer column number (starting from 0) where the latitude numbers are in input_csv_2.
    <longitude2> - the integer column number (starting from 0) where the longitude numbers are in input_csv_2.
    <maximum_miles> - if the 2 locations are within this number of miles from each other then include them in the output.
    <output_filename> - name of the csv file that will be created in the current directory.

 Options:
    --help  - show this help documentation.
"""


import csv
import math
import os
import sys

import docopt



def main():
    args = docopt.docopt(__doc__)
    
    column_args = ["<latitude1>", "<latitude2>", "<longitude1>", "<longitude2>", "<maximum_miles>"]
    
    for column_arg in column_args:
        try: 
            int(args[column_arg])
        except ValueError:
            print("The given value for " + column_arg + " is not an integer.")
            sys.exit()

    file1_rows = load_csv(args["<input_csv_1>"], int(args["<latitude1>"]), int(args["<longitude1>"]))
    file2_rows = load_csv(args["<input_csv_2>"], int(args["<latitude2>"]), int(args["<longitude2>"]))
    
    
    
    outfile_filename = args["<output_filename>"]
    ## If the file extension isn't .csv then there will be an error, so force it.
    extension = os.path.splitext(outfile_filename)[1][1:].lower()
    if not extension == "csv":
        outfile_filename += ".csv"
    
    output_rows = []
    for row1 in file1_rows:
        for row2 in file2_rows:
            x1 = float (row1[int(args["<latitude1>"])])
            y1 = float (row1[int(args["<longitude1>"])])
            x2 = float (row2[int(args["<latitude2>"])])
            y2 = float (row2[int(args["<longitude2>"])])

            dist = funHaversine(y1, x1, y2, x2)

            if dist <= int(args["<maximum_miles>"]):
                temp_row = row1 + row2
                temp_row.append(str(dist))
                output_rows.append(temp_row)
    
    with open(outfile_filename, 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        for row in output_rows:
            writer.writerow(row)
            # output_file.write( ",".join(row1 + row2) + "," + str(dist) + "\n")



def load_csv(filepath, latitude_column, longitude_column):
    """Adds error checking around loading a csv file.
    
    Args:
        filepath (str): filepath to the csv file
        latitude_column (int): column where latitude should be
        longitude_column (int): column where longitude should be
        
    Returns:
        file_rows (list): each row of csv file
        
    Raises:
        Exception: If file opening has a problem will raise an exception.
    """
    
    file_rows = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                csv_reader1 = csv.reader(f)
                for row in csv_reader1:
                    try:
                        float(row[latitude_column])
                        float(row[longitude_column])
                    except ValueError:
                        continue
                    else:
                        file_rows.append(row)
        except Exception as e:
            raise e

        return file_rows
    else:
        print("No such file: " + filepath)
        sys.exit()



def funHaversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    
    Args:
        lon1: longitude of first point.
        lat1: latitudes of first point.
        lon2: longitude of second point.
        lat2: latitudes of second point.
        
    Returns:
        miles: great circle distance in miles.
    """

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of earth in kilometers is 6371
    miles = (6371* c)/1.6
    return miles



if __name__ == "__main__":
    main()


