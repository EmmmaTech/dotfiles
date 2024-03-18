#!/usr/bin/env python

import argparse
import subprocess

import utils

device_name: str = ""

def get_default_device() -> str:
    cmd = subprocess.run(["brightnessctl", "-m", "info"], capture_output=True, text=True)
    return cmd.stdout.split(",")[0]

def notify_backlight(brightness: int):
    icon = utils.get_vol_icon(brightness)
    bar = utils.create_bar(brightness)

    utils.send_notif(f"{brightness}{bar}", f"{device_name}", icon, 91190, 800)

def modify_backlight(action: str, amount: int):
    cmd = subprocess.run(["brightnessctl", "-m", "set", f"{amount}%{action}"], capture_output=True, text=True)
    brightness = int(cmd.stdout.split(",")[3][:-1])

    notify_backlight(brightness)

def parse_args():
    parser = argparse.ArgumentParser(
        prog="backlightcontrol",
        description="A helper script to modify the backlight & send a notification.",
    )
    parser.add_argument("-i",
                        help="increase the brightness by the given amount",
                        action="store_true",
                        dest="increase")
    parser.add_argument("-d",
                        help="decrease the brightness by the given amount",
                        action="store_true",
                        dest="decrease")
    parser.add_argument("amount",
                        help="the amount to modify the brightness by",
                        type=int)

    return parser.parse_args()

def main():
    global device_name

    device_name = get_default_device()
    args = parse_args()

    if args.increase:
        modify_backlight("+", args.amount)
        exit(0)

    if args.decrease:
        modify_backlight("-", args.amount)
        exit(0)

if __name__ == "__main__":
    main()
