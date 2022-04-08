import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Optional

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if ROOT_DIR.split("/")[-1] != "judge_pics":
    raise "Please run update from the judge_pics directory"


def get_hash_from_file(image) -> str:
    """Get the sha256 hash from the current file"""
    with Path(ROOT_DIR, "data", "orig", image).open(mode="rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def strip_metadata_from_file(image) -> None:
    """Remove any metadata from the file and replace it."""

    command = [
        "exiftool",
        "-q",  # Quiet mode
        "-all=",  # Make all tags = ''
        "-overwrite_original",
        Path(ROOT_DIR, "data", "orig", image),
    ]
    subprocess.Popen(command, shell=False).communicate()


def update_judge_json(
    filename: str,
    person: int,
    date_created: Optional[str],
    artist: Optional[str],
    source: Optional[str],
    license: Optional[str],
) -> None:
    """Add new file to repository metadata

    :param filename: The filename
    :param person: The person ID from CL
    :param date_created: The date created
    :param artist: The artist
    :param source: The source
    :param license: The license
    :return:
    """
    with Path(ROOT_DIR, "data", "people.json").open(mode="r") as f:
        judges_json = json.load(f)

    judge = [x for x in judges_json if x["person"] == person]

    if judge:
        raise ValueError("Judge already exists")
    strip_metadata_from_file(filename)
    sha_hash = get_hash_from_file(filename)
    if any([x["hash"] == sha_hash for x in judges_json]):
        raise ValueError(
            f"Image with hash '{sha_hash}' already exists in the database"
        )

    judges_json.append(
        {
            "hash": sha_hash,
            "license": license,
            "source": source,
            "artist": artist,
            "date_created": date_created,
            "path": filename,
            "person": person,
        }
    )

    with Path(ROOT_DIR, "data", "people.json").open(mode="w") as f:
        json.dump(judges_json, f, sort_keys=True, indent=2)


if __name__ == "__main__":
    """Before one can add to the repository you must first strip the exif data
    from the image and add the metadata of the file to the list of judges.
    This method checks that the image is not already in the system and updates
    people.json.
    """

    parse = argparse.ArgumentParser(description="Create a new portrait")
    parse.add_argument(
        "--filename", help="The name of the file", required=True
    )
    parse.add_argument(
        "--person", type=int, help="The CourtListener Person ID", required=True
    )
    parse.add_argument(
        "--source",
        help="The source (url) of the image for record keeping",
        required=False,
        default=None,
    )
    parse.add_argument(
        "--artist", help="The artist", required=False, default=None
    )
    parse.add_argument(
        "--license",
        help="The license of the image",
        required=False,
        default="Work of Federal Government",
    )
    parse.add_argument(
        "--date-created", help="The date created", required=False, default=None
    )

    update_judge_json(
        filename=parse.parse_args().filename,
        person=parse.parse_args().person,
        date_created=parse.parse_args().date_created,
        artist=parse.parse_args().artist,
        source=parse.parse_args().source,
        license=parse.parse_args().license,
    )
