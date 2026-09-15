# coding: utf-8
import os
import subprocess
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlsplit

import requests

# CONSTANT
BASE_DIR = Path.home() / "Pictures" / "bing-wallpaper" / "bing-wallpapers"
BING = "https://www.bing.com/HPImageArchive.aspx?format=js&uhd=1&idx=0&n=1&mkt=en-GB"
BACKGROUND_SCHEMA = "org.gnome.desktop.background"
TIMEOUT = 10  # seconds


def set_wallpaper(image_path):
    image_uri = image_path.resolve().as_uri()
    settings_env = os.environ.copy()
    # Snap-packaged editors can override this with outdated desktop schemas.
    settings_env["GSETTINGS_SCHEMA_DIR"] = "/usr/share/glib-2.0/schemas"
    for key in ("picture-uri", "picture-uri-dark"):
        subprocess.run(
            ["gsettings", "set", BACKGROUND_SCHEMA, key, image_uri],
            check=True,
            env=settings_env,
        )


def check_new_image():
    response = requests.get(BING, timeout=TIMEOUT)
    response.raise_for_status()
    image_info = response.json()["images"][0]
    image_id = parse_qs(urlsplit(image_info["url"]).query)["id"][0]
    # Keep only the image ID: Bing's width/height parameters resize UHD images.
    image_url = "https://www.bing.com/th?" + urlencode({"id": image_id})
    image_name = Path(image_id).name.removeprefix("OHR.")
    filename = f"{image_info['startdate']}_{image_name}"
    # Download image if it doesn't exist
    image_path = BASE_DIR / filename
    if not image_path.exists():
        image = requests.get(image_url)
        image_path.write_bytes(image.content)
        set_wallpaper(image_path)


if __name__ == "__main__":
    check_new_image()
