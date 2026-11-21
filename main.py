"""Entry point for the 20 November 2026 news-image bounty.

Copies the bundled entry.png to /output/entry.png when that
directory exists, otherwise to ./output/entry.png.

Deterministic copy: shutil.copyfile writes the bundled bytes
unchanged, with no clock, network, or randomness involved, so
running this program twice writes identical bytes every time.
"""

import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main():
    target_dir = Path("/output") if Path("/output").is_dir() else HERE / "output"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
