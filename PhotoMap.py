import os, os.path
import fnmatch
import pathlib
from glob import glob
from PIL import Image
import get_exif_info
import webbrowser


def SearchAllPics(pathToSearch = r"C:\Users\lalit\Documents\Lalit\Pics\2016-03", ):
    # find all the picture files in this directory and sub-directories
    
    print("  -- Started -->  ")
    #picture file extensions
    picExts = ["*.jpg", "jpeg", "bmp", "png"]

    #Get all files with valid pic extensions
    files = sorted(pathlib.Path(pathToSearch).rglob(picExts[0]))

    FilesInfo = {}
    for file in files:
            try:
                with Image.open(file) as image:
                    exif_data = get_exif_info.get_exif_data(image)
                    #gps_info = get_exif_info.clean_gps_info(exif_data)
                    la, lo = get_exif_info.get_lat_lon(exif_data)
                    FilesInfo[file] = {'lat':la, 'lng':lo}
            except:
                pass
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
    FilesInfo = SearchAllPics(r"C:\Users\lalit\Documents\Lalit\Pics")
    locations = ""
    for k, v in FilesInfo.items():
        #{lat: -31.563910, lng: 147.154312},
        
        #replace backslash with double backslash so that JS does not escape \
        rk = (str(k)).replace("\\","\\\\")
        if  v is None or v["lat"] is None or v["lng"] is None:
            locations = locations + "{lat:0, lng:0, pic:\"file://" + rk + "\"},"
        else:
            locations = locations + "{lat:" + str(v["lat"]) + ", lng:" + str(v["lng"]) + ", pic:\"file://" + rk + "\"},"
    
    #create javascript file # Create or overwrite the output file
    #explicity encoding required because the generated file can have some escaped combinations
    output_file = open('world_photo_locations.js', 'w', encoding='utf-8')

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

