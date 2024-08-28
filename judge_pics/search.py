import json
import os
import re
from enum import Enum
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Literal, Optional, List, Union

import climage
import requests
from fuzzywuzzy import fuzz

ROOT = os.path.dirname(os.path.abspath(__file__))

with Path(ROOT, "data", "people.json").open() as f:
    judges = json.load(f)


class ImageSizes(Enum):
    SMALL = 128
    MEDIUM = 256
    LARGE = 512
    ORIGINAL = "orig"


SIZES = Literal[
    ImageSizes.SMALL, ImageSizes.MEDIUM, ImageSizes.LARGE, ImageSizes.ORIGINAL
]


def query(search_str: str, size: SIZES = ImageSizes.MEDIUM) -> Optional[List]:
    """Find a judge by name"""
    paths = [j["path"] for j in judges]

    xlist = []
    for path in paths:
        matching_path = re.sub(r"[\d-]+", " ", path).strip()
        m = fuzz.token_sort_ratio(matching_path, search_str.lower())
        xlist.append((path, m))
        if m > 95:
            return [f"https://portraits.free.law/v2/{size}/{path}.jpeg"]
    xlist.sort(key=lambda y: -y[1])
    if len(xlist) == 0:
        return None

    return [
        f"https://portraits.free.law/v2/{size}/{x[0]}.jpeg"
        for x in xlist
        if x[1] > 10
    ]


def portrait(
    person: Union[str, int], size: SIZES = ImageSizes.ORIGINAL
) -> Optional[str]:
    """Get URL for portait on free.law"""
    if type(person) == int:
        paths = [x for x in judges if x["person"] == person]
        if len(paths) > 0:
            return f"https://portraits.free.law/v2/{size.value}/{paths[0]['path']}.jpeg"
        else:
            return None
    else:
        matches = query(person, size.value)
        if matches:
            return matches[0]
        return None


def show(person: int, size: ImageSizes = None) -> str:
    """Get the image as ANSI escape codes so you can print it out"""
    url = portrait(person, size)
    r = requests.get(url, timeout=10)
    with NamedTemporaryFile(suffix=".jpeg") as tmp:
        with open(tmp.name, "wb") as f:
            f.write(r.content)
        output = climage.convert(tmp.name, width=40)
    return output
