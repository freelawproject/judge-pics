import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Literal

import climage
import requests

ROOT = os.path.dirname(os.path.abspath(__file__))

with Path(ROOT, "data", "people.json").open() as f:
    judges = json.load(f)


class ImageSizes:
    small: int = 128
    medium: int = 256
    large: int = 512
    original: None = None


SIZES = Literal[
    ImageSizes.small, ImageSizes.medium, ImageSizes.large, ImageSizes.original
]


def portrait(person: int, size: SIZES = None) -> str:
    """Get URL for portait on CL"""
    if not size:
        size = "orig"
    path = [x for x in judges if x["person"] == person][0]["path"]
    return f"https://portraits.free.law/v2/{size}/{path}.jpeg"


def show(person: int, size: ImageSizes = None) -> str:
    """"""
    url = portrait(person, size)
    r = requests.get(url, timeout=10)
    with NamedTemporaryFile(suffix=".jpeg") as tmp:
        with open(tmp.name, "wb") as f:
            f.write(r.content)
        output = climage.convert(tmp.name, width=40)
    return output
