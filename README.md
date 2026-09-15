# Bing wallpaper

Download Bing's daily wallpaper and set it as the GNOME desktop background. The script requests UHD images for the UK bing and saves them with a date prefix.

## Requirements

- Ubuntu with GNOME and `gsettings`
- Python 3.9 or newer and the `requests` package
- An active desktop session for the user running the script.

## Setup

Place this project at `~/Pictures/bing-wallpaper`, then run:

```bash
cd ~/Pictures/bing-wallpaper
mkdir -p bing-wallpapers
python3 -m venv .venv
.venv/bin/python -m pip install requests
.venv/bin/python bing-wallpapers.py
```

If creating the virtual environment fails because `venv` is unavailable, install
Ubuntu's `python3-venv` package first.

Images are saved in `~/Pictures/bing-wallpaper/bing-wallpapers`. Change `BASE_DIR`
in the script to use another download directory, and create that directory before
running it. Existing filenames are skipped when downloading.

Change `mkt=en-GB` in the `BING` URL to select other locations, such as `en-US`.

## Run automatically

To run the script every minute:

1. Open a terminal as your normal desktop user and run `id -u` to find your user ID.
2. Run `crontab -e` to open your user's scheduled tasks in a text editor. Do NOT use
   `sudo`. If prompted to choose an editor, select nano.
3. Paste the following three lines at the bottom of the file opened by
   `crontab -e`. The line starting with `* * * * *` belongs in this file; keep the
   entire command on one line.

```cron
XDG_RUNTIME_DIR=/run/user/1000
DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
* * * * * /home/YOUR_USER/Pictures/bing-wallpaper/.venv/bin/python /home/YOUR_USER/Pictures/bing-wallpaper/bing-wallpapers.py >> /home/YOUR_USER/Pictures/bing-wallpaper/wallpaper.log 2>&1
```

Replace `/home/YOUR_USER` with your home directory and `1000` with the output of
`id -u`. The Python path assumes you created `.venv` using the setup instructions;
adjust it if your virtual environment is elsewhere.

4. Save and close the editor. In nano, press **Ctrl+O**, **Enter**, then **Ctrl+X**.
   Cron installs the schedule when you save and exit.
5. Run `crontab -l` in the terminal to confirm the entry was saved.

The five asterisks mean “every minute.” Wallpaper updates require your desktop
session to be running. Check `wallpaper.log` in the project directory for errors.

## Troubleshooting

- **Wallpaper does not change:** run the script from a terminal in your GNOME
  desktop session, using your normal user account. Both light and dark wallpaper
  settings are updated.
- **Running from VS Code installed through Snap:** the script explicitly uses
  `/usr/share/glib-2.0/schemas` to avoid outdated schemas inherited from the editor.
- **Black wallpaper after replacing an image:** confirm the file opens in an image
  viewer. Selecting another wallpaper in Settings and then rerunning the script
  forces GNOME to reload it.
