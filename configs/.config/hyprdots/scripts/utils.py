import math
import subprocess
import os

HOMEDIR = os.environ["HOME"]
CONFIGDIR = os.environ.get("XDG_CONFIG_HOME") or (HOMEDIR + "/.config")
ICONDIR = CONFIGDIR + "/dunst/icons/vol"

def send_notif(title: str, contents: str, iconpath: str, id: int, timeout: int):
    subprocess.run(["dunstify", "t2", "-a", title, contents, "-i", iconpath, "-r", str(id), "-t", str(timeout)])

def create_bar(val: int):
    return "." * math.floor(val / 15)

def get_vol_icon(val: int):
    angle = math.floor((val + 2) / 5) * 5
    return ICONDIR + f"/vol-{angle}.svg"
