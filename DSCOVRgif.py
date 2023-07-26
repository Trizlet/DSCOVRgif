# this works but totally isnt perfect, so feel free to do what you want with it!
import argparse
import os
import shutil
import urllib.request

import imageio.v2 as imageio
import requests

# select image type
parser = argparse.ArgumentParser()
parser.add_argument('-t','--type', type=str, required=False, choices=['n', 'e', 'a','c'], default="n")
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

# get latest image data
response = requests.get("https://epic.gsfc.nasa.gov/api/" + type)
if str(response.status_code) != "200":
    print("API request failed! returned " + str(response.status_code))
list = response.json()
date = list[0]["date"][:10]

# create folder
folder = "./tempImages" # where to save images
if os.path.exists(folder + "/"):
    print(folder + " already exists! stopping just in case.")
    exit()
if not os.path.exists(folder + "/"):
    os.makedirs(folder + "/")

# get images
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
        "./tempImages/"
        + list[x]["image"]
        + ".png"
    )
    print("saving " + output)
    urllib.request.urlretrieve(url, output)

gif = type + "_" + date + ".gif"
print("creating animation at " + os.getcwd() + " please wait..")

images = []
for file_name in sorted(os.listdir(folder)):
    if file_name.endswith(".png"):
        file_path = os.path.join(folder, file_name)
        images.append(imageio.imread(file_path))
imageio.mimsave(
    "./" + gif, images,
)

shutil.rmtree("./tempImages") # remove this if you want to keep the saved images
print(gif + " successfully created at " + os.getcwd())

