import hashlib
import json
import os
import re
import shutil
import subprocess
from typing import Optional

import requests
from lxml import html
from requests import RequestException, Timeout

from judge_pics import judge_pics, judge_root

root_url = "http://dcchs.org/Portraits/"
line_re = re.compile('<a href="(.*)">(.*)</a')


def make_slug(name: str, path: str) -> str:
    """Generate a slug based on the provided name and path.

    :param name: the full name
    :param path: the html path
    :return the generated slug
    """
    last_name = re.search("(.*),", name).group(1).lower()
    first_name = re.search("([A-Z].*)[A-Z]", path).group(1).lower()
    return f"{last_name}-{first_name}"


def get_artist_and_date_created(
    full_url: str,
) -> tuple[Optional[str], Optional[str]]:
    """Open firefox, prompt for answer, sanitize answer and return it.

    :param full_url: The URL to be opened in the Firefox browser
    :return A tuple containing the artist's name and the creation date.
    """
    subprocess.Popen(["firefox", full_url], shell=False).communicate()
    artist = input("Who made this: ")
    if artist == "":
        artist = None

    d = input("When did they make it: ")
    if d == "":
        d = None
    return artist, d


def get_hash_from_file(image: str) -> str:
    """Get the hash from the current file

    :param image: The file path to compute the hash for
    :return The SHA-256 hash of the file content
    """
    with open(image, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_things():
    with open("sources.txt", encoding="utf-8") as f:
        for line in f:
            # <a href="JesseAdkins.html">Adkins, Jesse C.</a><br>
            path = line_re.search(line).group(1)
            name = line_re.search(line).group(2)

            slug = make_slug(name, path)

            full_url = root_url + path

            try:
                r = requests.get(
                    full_url,
                    headers={"UserAgent": "freelawproject.org"},
                    timeout=10,
                )
                tree = html.fromstring(r.text)
                try:
                    img_path = tree.xpath(
                        '//div[@id="contentcolumn"]//img/@src'
                    )[0]
                    full_img_src = root_url + img_path
                except IndexError:
                    print(f"Failed to find image for {full_url}")
                    continue
            except Timeout:
                print(
                    f"Request to {full_url} timed out. Please try again later."
                )
                continue
            except RequestException as e:
                print(f"An error occurred: {e}")
                continue

            try:
                r_img = requests.get(full_img_src, stream=True, timeout=10)
            except Timeout:
                print(
                    f"Request to {full_img_src} timed out. Please try again later."
                )
                continue
            except RequestException as e:
                print(f"An error occurred: {e}")
                continue

            if r_img.status_code == 200:
                with open(slug + ".jpeg", "wb") as f_img:
                    r_img.raw.decode_content = True
                    shutil.copyfileobj(r_img.raw, f_img)

            artist, date_created = get_artist_and_date_created(full_url)

            img_hash = get_hash_from_file(slug + ".jpeg")

            # Update judges.json
            judge_pics[slug] = {
                "artist": artist,
                "date_created": date_created,
                "license": "Work of Federal Government",
                "source": "Historical Society of the District of Columbia "
                "Circuit",
                "hash": img_hash,
            }

    with open(
        os.path.join(judge_root, "judges.json"), "w", encoding="utf-8"
    ) as fp:
        json.dump(
            judge_pics,
            fp,
            sort_keys=True,
            indent=2,
        )


if __name__ == "__main__":
    run_things()
