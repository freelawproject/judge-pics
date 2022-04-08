import json
import os
from enum import Enum
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Literal

import climage
import requests

ROOT = os.path.dirname(os.path.abspath(__file__))

with Path(ROOT, "data", "people.json").open() as f:
    judges = json.load(f)


class ImageSizes(Enum):
    SMALL = 128
    MEDIUM = 256
    LARGE = 512
    ORIGINAL = None


SIZES = Literal[
    ImageSizes.SMALL, ImageSizes.MEDIUM, ImageSizes.LARGE, ImageSizes.ORIGINAL
]


def portrait(person: int, size: SIZES = "orig") -> str:
    """Get URL for portait on free.law"""
    path = [x for x in judges if x["person"] == person][0]["path"]
    return f"https://portraits.free.law/v2/{size}/{path}.jpeg"


def show(person: int, size: ImageSizes = None) -> str:
    """Get the image as ANSI escape codes so you can print it out"""
    url = portrait(person, size)
    r = requests.get(url, timeout=10)
    with NamedTemporaryFile(suffix=".jpeg") as tmp:
        with open(tmp.name, "wb") as f:
            f.write(r.content)
        output = climage.convert(tmp.name, width=40)
    return output
