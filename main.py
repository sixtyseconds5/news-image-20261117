#!/usr/bin/env python3
"""Copy entry.png into the make.fun output directory.

Stdlib only. The output directory comes from MAKEFUN_OUTPUT_DIR
(default /output) and is created if needed. Exits non-zero with a
message on stderr when entry.png is missing.
"""
import os
import shutil
import sys
from pathlib import Path


def main():
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")
    print(f"copied entry.png to {out_dir / 'entry.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
