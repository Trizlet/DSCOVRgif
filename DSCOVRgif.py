# this works but totally isnt perfect, so feel free to do what you want with it!
import argparse
import os
import shutil
import urllib.request

import imageio.v2 as imageio
import requests

# select arguments
parser = argparse.ArgumentParser(
                    prog=__file__,
                    description='A tool to create gifs from imagery gathered by the EPIC instrument onboard the DSCOVR spacecraft.',
                    epilog='@Trizlet was here :P')
parser.add_argument('-t','--type', type=str, required=False, choices=['n', 'e', 'a','c'], default="n", help = 'to select natural, enhanced, aerosol, or cloud imagery. (Natural on default)')
parser.add_argument('-nr', '--noremove', action='store_true', help = 'to keep downloaded images after use (Deleted on default)')
parser.add_argument('-nl', '--noloop', action='store_true', help = 'disable gif looping. (Loops on default)')
parser.add_argument('-v', '--verbose', action='store_true', help = 'to see what images are being downloaded (Disabled on default)')
args = parser.parse_args()
if args.type == "n":
    type = "natural"
elif args.type == "e":
    type = "enhanced"
elif args.type == "a":
    type = "aerosol"
elif args.type == "c":
    type = "cloud"
else: 
    type ="natural"

# get latest image data from API
response = requests.get("https://epic.gsfc.nasa.gov/api/" + type)
if str(response.status_code) != "200":
    print("API request failed! returned " + str(response.status_code))
list = response.json()
date = list[0]["date"][:10]

# create folder
folder = os.path.dirname(os.path.realpath(__file__)) + "/tempImages" # where to save images
if os.path.exists(folder + "/"):
    if input(folder+ " already exists! Would you like to write over it? this will delete the file! (y/n)\n").strip().lower() == "y":
        shutil.rmtree(folder)
        os.makedirs(folder + "/")
    else:
        print("stopping.")
        exit()
if not os.path.exists(folder + "/"):
    os.makedirs(folder + "/")

# get images
print("Downloading images...")
for x, item in enumerate(list):
    url = (
        "https://epic.gsfc.nasa.gov/archive/"+type+"/" 
        + list[x]["date"][:4]
        + "/"
        + list[x]["date"][5:7]
        + "/"
        + list[x]["date"][8:10]
        + "/png/"
        + list[x]["image"]
        + ".png"
    )
    output = (
        folder+"/"
        + list[x]["image"]
        + ".png"
    )
    if args.verbose:
        print("saving " + url)
    urllib.request.urlretrieve(url, output)

gif = type + "_" + date + ".gif" # remove the _ and date from this if you just want them to come out as the same filename every day
print("Creating animation at " + os.getcwd() + " please wait...")

# create gif
images = []
for file_name in sorted(os.listdir(folder)):
    if file_name.endswith(".png"):
        file_path = os.path.join(folder, file_name)
        images.append(imageio.imread(file_path))

if not args.noloop:
    imageio.mimsave(
    os.path.dirname(os.path.realpath(__file__))+ "/" + gif, images, loop = 0
    )
else:
    imageio.mimsave(
        os.path.dirname(os.path.realpath(__file__))+ "/" + gif, images
    )
if not args.noremove:
    shutil.rmtree(folder) # removes image folder
print(gif + " successfully created at " + os.path.dirname(os.path.realpath(__file__)))

