import os, os.path import fnmatch import pathlib from glob import glob
from PIL import Image import get_exif_info
#c:\\users\\lalit\\documents\\lalit\\python\\ import webbrowser


def SearchAllPics(pathToSearch = r"C:\Users\lalit\Documents\Lalit\Pics\2016-03", ):
    # find all the picture files in this directory and sub-directories
    
    print("  -- Started -->  ")
    #picture file extensions
    picExts = ["*.jpg", "jpeg", "bmp", "png"]

    #Get all files with valid pic extensions
    files = sorted(pathlib.Path(pathToSearch).rglob(picExts[0]))

    FilesInfo = {}
    for file in files:
        with Image.open(file) as image:
            exif_data = get_exif_info.get_exif_data(image)
            #gps_info = get_exif_info.clean_gps_info(exif_data)
            la, lo = get_exif_info.get_lat_lon(exif_data)
            FilesInfo[file] = {'lat':la, 'lng':lo}

    i=0
    for k, v in FilesInfo.items():
        i=i+1
        #print("[{}] File: -> {}\tLat= [{}]\tLon= [{}]".format(i,k, v["lat"], v["lng"]))
    
    print("  <-- Ended --  ")

    return FilesInfo
SearchAllPics()


def open_photo_map():

    #first search all pics and extract the GPS locations
    #\2016-03
    FilesInfo = SearchAllPics(r"C:\Users\lalit\Documents\Lalit\Pics\2016-03")
    locations = ""
    for k, v in FilesInfo.items():
        #{lat: -31.563910, lng: 147.154312},
        if  v is None or v["lat"] is None or v["lng"] is None:
            locations = locations + "{lat:0, lng:0},"
        else:
            rk = (str(k)).replace("\\","\\\\")
            locations = locations + "{lat:" + str(v["lat"]) + ", lng:" + str(v["lng"]) + ", pic:\"file://" + rk + "\"},"
    
    #create javascript file # Create or overwrite the output file
    output_file = open('world_photo_locations.js', 'w')

    #form locations list
    str_locations = "var locations = [" + locations + "]"

    rendered_content = str_locations
    
    # Output the file
    output_file.write(rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.join(os.path.abspath(os.curdir),"photomap.html")
    #print(">>>>>>>>>>>>>>>File : " + url)
    webbrowser.open('file://' + url, new=2) # open in a new tab, if possible
open_photo_map()

