# coding: utf-8
import json
import subprocess
from pathlib import Path

import requests

# CONSTANT
BASE_DIR = Path.home() / "Pictures" / "bing-wallpaper" / "bing-wallpapers"
BING = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
CMD = 'gsettings set org.gnome.desktop.background picture-uri "file://{}"'


def check_new_image():
    r = requests.get(BING)
    j = json.loads(r.text)
    urlbase = j["images"][0]["urlbase"]
    image_url = f"https://bing.com{urlbase}_1920x1080.jpg"
    filename = image_url.split("/")[-1]

    image_path = BASE_DIR / filename
    if not image_path.exists():
        image = requests.get(image_url)
        with image_path.open("wb+") as f:
            f.write(image.content)
        subprocess.Popen(CMD.format(image_path.resolve()), shell=True)


if __name__ == "__main__":
    check_new_image()
