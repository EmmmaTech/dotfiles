# Installation on Apple Silicon Macs

Install the base Arch Linux image with the instructions from the [Asahi Linux](https://asahilinux.org) website.

Once installed, you can install these dotfiles using the [normal instructions](./README.md#installation).

(Note: it's recommended to switch the `asahi` repo in `pacman.conf` to `asahi-dev` for updated packages)

### Enabling the Speakers

On Fedora Asahi, it comes out of the box with speakers supported. Arch Asahi has everything it needs for speakers, but some packages need to be built manually.

Make a clone of this [PKGBUILDs](https://github.com/joske/PKGBUILDs/tree/main) repo, then make and install these packages (in this order):

- `alsa-ucm-conf-asahi`
- `bankstown`
- `speakersafetyd`
- `asahi-audio`

These packages are needed in order for Pipewire to interface with the speaker drivers and to keep the speakers safe.

However, the speakers won't work quite yet because the driver is disabled for safety reasons.

To fix this, modify `GRUB_CMDLINE_LINUX` in `/etc/default/grub` to include this:

```
"snd_soc_macaudio.please_blow_up_my_speakers=1"
```

This will bypass any safety checks that the speaker driver has and force enable it. Despite the option name, your speakers will be safe because of the packages we installed before.
