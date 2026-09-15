# coding: utf-8
import subprocess
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

import requests

# CONSTANT
BASE_DIR = Path.home() / "Pictures" / "bing-wallpaper" / "bing-wallpapers"
BING = "https://www.bing.com/HPImageArchive.aspx?format=js&uhd=1&idx=0&n=1&mkt=en-GB"
CMD = 'gsettings set org.gnome.desktop.background picture-uri "file://{}"'


def check_new_image():
    response = requests.get(BING)
    response.raise_for_status()
    image_info = response.json()["images"][0]
    image_id = parse_qs(urlsplit(image_info["url"]).query)["id"][0]
    image_id = image_id.rsplit("_", 1)[0] + "_UHD.jpg"
    # Keep only the image ID: Bing's width/height parameters resize UHD images.
    image_url = "https://www.bing.com/th?" + urlencode({"id": image_id})
    image_name = Path(image_id).name.removeprefix("OHR.")
    filename = f"{image_info['startdate']}_{image_name}"

    image_path = BASE_DIR / filename
    if not image_path.exists():
        image = requests.get(image_url)
        image_path.write_bytes(image.content)
        subprocess.Popen(CMD.format(image_path.resolve()), shell=True)


if __name__ == "__main__":
    check_new_image()
