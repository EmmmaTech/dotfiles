#!/usr/bin/env python

import argparse
import subprocess
import re

import utils

DEFAULT_SINK_REGEX = r"([0-9]*) \"(.*)\" \"(.*)\""

sink_id: int = 0
sink_name: str = ""

# TODO: support changing the volume for input devices

def get_default_sink() -> tuple[int, str]:
    cmd = subprocess.run(["pamixer", "--get-default-sink"], capture_output=True, text=True)
    parsed = re.match(DEFAULT_SINK_REGEX, cmd.stdout.splitlines()[1])

    return parsed.group(1, 2)

def notify_volume(vol: int):
    icon = utils.get_vol_icon(vol)
    bar = utils.create_bar(vol)

    utils.send_notif(f"{vol}{bar}", f"{sink_name}", icon, 91190, 800)

def notify_mute(muted: bool):
    notif_title = "muted" if muted else "unmuted"
    icon = utils.ICONDIR + f"/{notif_title}-speaker.svg"

    utils.send_notif(notif_title, sink_name, icon, 91190, 800)

def modify_volume(action: str, amount: int):
    subprocess.run(["pamixer", "--sink", str(sink_id), action, str(amount)])
    cmd = subprocess.run(["pamixer", "--sink", str(sink_id), "--get-volume"], capture_output=True, text=True)

    vol = int(cmd.stdout)
    notify_volume(vol)

def toggle_mute():
    subprocess.run(["pamixer", "--sink", str(sink_id), "-t"])
    cmd = subprocess.run(["pamixer", "--sink", str(sink_id), "--get-mute"], capture_output=True, text=True)

    muted = True if cmd.stdout.strip() == "true" else False
    notify_mute(muted)

def parse_args():
    parser = argparse.ArgumentParser(
        prog="volumecontrol",
        description="A helper script to modify the volume & send a notification.",
    )
    parser.add_argument("-i",
                        help="increase the volume by the given amount",
                        action="store_true",
                        dest="increase_vol")
    parser.add_argument("-d",
                        help="decrease the volume by the given amount",
                        action="store_true",
                        dest="decrease_vol")
    parser.add_argument("-m",
                        help="switches between muted and unmuted",
                        action="store_true",
                        dest="mute")
    parser.add_argument("amount",
                        help="the amount to modify the volume by",
                        nargs="?",
                        type=int,
                        default=0)
    
    return parser.parse_args()

def main():
    global sink_id, sink_name

    sink_id, sink_name = get_default_sink()
    args = parse_args()

    if args.increase_vol:
        modify_volume("-i", args.amount)
        exit(0)

    if args.decrease_vol:
        modify_volume("-d", args.amount)
        exit(0)

    if args.mute:
        toggle_mute()
        exit(0)

if __name__ == "__main__":
    main()
