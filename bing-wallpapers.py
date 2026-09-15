# coding: utf-8
import json
import subprocess
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import requests

# CONSTANT
BASE_DIR = Path.home() / "Pictures" / "bing-wallpaper" / "bing-wallpapers"
BING = "https://www.bing.com/HPImageArchive.aspx?format=js&uhd=1&idx=0&n=1&mkt=en-GB"
CMD = 'gsettings set org.gnome.desktop.background picture-uri "file://{}"'


def check_new_image():
    r = requests.get(BING)
    j = json.loads(r.text)
    image_info = j["images"][0]
    urlbase = image_info["urlbase"]
    image_url = f"https://bing.com{urlbase}_UHD.jpg"
    image_id = parse_qs(urlsplit(image_url).query)["id"][0]
    image_name = Path(image_id).name.removeprefix("OHR.")
    filename = f"{image_info['startdate']}_{image_name}"

    image_path = BASE_DIR / filename
    if not image_path.exists():
        image = requests.get(image_url)
        with image_path.open("wb+") as f:
            f.write(image.content)
        subprocess.Popen(CMD.format(image_path.resolve()), shell=True)


if __name__ == "__main__":
    check_new_image()
