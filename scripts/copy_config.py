#!/usr/bin/env python

import pathlib
import shutil

def main():
    whitelist = pathlib.Path("./scripts/whitelist.txt").read_text().splitlines()
    out = pathlib.Path("./configs")
    homedir = pathlib.Path.home()

    if not out.exists():
        out.mkdir()

    for item in whitelist:
        raw = pathlib.Path(item)
        src = homedir / raw
        new = out / raw

        if not new.exists():
            if new.is_dir():
                new.mkdir(parents=True, exist_ok=True)
            else:
                new.parent.mkdir(parents=True, exist_ok=True)

        if src.is_dir():
            shutil.copytree(src, new, dirs_exist_ok=True)
        else:
            shutil.copy(src, new)

if __name__ == "__main__":
    main()
