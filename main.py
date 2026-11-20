#!/usr/bin/env python3
"""news-image-20261120 — emit the entry image.

Copies the stored entry.png to $MAKEFUN_OUTPUT_DIR (falling back to this
script's own directory when the variable is unset), verifies the copy with
a sha256 comparison, prints the destination and hash, and exits 0.

Stdlib only: the grading environment has no Pillow, runs the repo read-only
as an unprivileged user, and sets MAKEFUN_OUTPUT_DIR to a writable path.
This script never writes into the repo directory when MAKEFUN_OUTPUT_DIR
is set.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

ENTRY = "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = Path(__file__).resolve().parent
    src = here / ENTRY
    if not src.is_file():
        print("missing source: %s" % src, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or str(here)
    dest = Path(out_dir) / ENTRY
    dest.parent.mkdir(parents=True, exist_ok=True)
    # When the output dir IS the repo dir, src and dest are the same file;
    # copying it onto itself would raise SameFileError, so skip the copy
    # and just verify + report the file in place.
    if dest.resolve() != src.resolve():
        shutil.copyfile(src, dest)
    want = sha256_of(src)
    got = sha256_of(dest)
    if got != want:
        print("hash mismatch: %s != %s" % (got, want), file=sys.stderr)
        return 1
    print("wrote %s" % dest)
    print("sha256 %s" % got)
    return 0


if __name__ == "__main__":
    sys.exit(main())
