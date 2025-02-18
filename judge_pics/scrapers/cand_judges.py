import hashlib
import json
import os
import shutil
from typing import Optional

import requests
from dateutil import parser
from lxml import html
from requests import RequestException, Timeout

from judge_pics import judge_pics, judge_root

token = ""
if token:
    headers = {"Authorization": "Token %s" % token}
else:
    print(
        "Warning: No CourtListener token used. You'll run out of free "
        "queries to the API quickly."
    )
    headers = {}


def granular_date(d: Optional[str], granularity: str) -> str:
    """Convert a date string into a formatted date based on the specified
    granularity

    :param d: the date to format, as a string.
    :param granularity: the level of granularity for the formatted date
    :return The formatted date string based on the given granularity
    """
    if not d:
        return ""

    d = parser.parse(d).date()

    GRANULARITY_YEAR = "%Y"
    GRANULARITY_MONTH = "%Y-%m"
    GRANULARITY_DAY = "%Y-%m-%d"
    if granularity == GRANULARITY_DAY:
        return "-" + d.strftime("%Y-%m-%d")
    elif granularity == GRANULARITY_MONTH:
        return "-" + d.strftime("%Y-%m")
    elif granularity == GRANULARITY_YEAR:
        return "-" + d.strftime("%Y")


def make_slug(name: str) -> str | None:
    """Hit our search engine and get back a good result. Look that up in the
    People endpoint to get glorious metadata.

    We start with a full name, so we plug that in.
    """
    # Drop middle initials
    name = name.lower()
    name = " ".join(
        [n.replace(",", "") for n in name.split() if not n.endswith(".")]
    )

    try:
        result_json = requests.get(
            "https://www.courtlistener.com/api/rest/v4/search/?type=p&name=%s&court=cand"
            % name,
            headers=headers,
            timeout=10,
        ).json()
    except Timeout:
        print(f"Request timed out while searching for {name}.")
        return None
    except RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None
    except ValueError as e:
        print(f"Failed to parse JSON response while searching for {name}: {e}")
        return None

    if result_json["count"] > 1:
        print(
            "Warning: Got back %s results for %s"
            % (
                result_json["count"],
                name,
            )
        )
        return None
    if result_json["count"] < 1:
        print("Warning: Got back no results for %s" % name)
        name_parts = name.split()
        if len(name_parts) == 2:
            return f"{name_parts[1].lower()}-{name_parts[0].lower()}"
        return None

    result_id = result_json["results"][0]["id"]
    result_json = requests.get(
        "https://www.courtlistener.com/api/rest/v4/people/?id=%s" % result_id,
        headers=headers,
        timeout=10,
    ).json()

    judge = result_json["results"][0]

    return "{}-{}{}".format(
        judge["name_last"].lower(),
        judge["name_first"].lower(),
        granular_date(judge["date_dob"], judge["date_granularity_dob"]),
    )


def get_hash_from_file(image: str) -> str:
    """Get the hash from the current file

    :param image: The file path to compute the hash for
    :return The SHA-256 hash of the file content
    """
    with open(image, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_things():
    base_href = "http://www.cand.uscourts.gov"
    start_path = "/judges"
    start_url = base_href + start_path

    try:
        r = requests.get(start_url, timeout=10)
    except Timeout:
        print(f"Request to {start_url} timed out. Please try again later.")
        return
    except RequestException as e:
        print(f"An error occurred: {e}")
        return

    html_tree = html.fromstring(r.text)
    html_tree.make_links_absolute(base_href)
    judge_nodes = html_tree.xpath('//section[@id="main-content"]//li')
    judge_info = []
    for node in judge_nodes:
        try:
            name = node.xpath("a/text()")[0]
            url = node.xpath("a/@href")[0]
        except IndexError:
            continue
        else:
            judge_info.append((name, url))

    for judge_name, judge_link in judge_info:

        try:
            judge_r = requests.get(judge_link, timeout=10)
        except Timeout:
            print(
                f"Request to {judge_link} timed out. Please try again later."
            )
            continue
        except RequestException as e:
            print(f"An error occurred: {e}")
            continue

        judge_html = html.fromstring(judge_r.text)
        judge_html.make_links_absolute(base_href)

        try:
            img_path = judge_html.xpath(
                '//div[@class = "judge_portrait"]//img/@src'
            )[0]
        except IndexError:
            print("Failed to find image for %s" % judge_link)
            continue

        try:
            img_r = requests.get(img_path, stream=True, timeout=10)
        except Timeout:
            print(f"Request to {img_path} timed out. Please try again later.")
            continue
        except RequestException as e:
            print(f"An error occurred: {e}")
            continue

        if img_r.status_code == 200:
            slug = make_slug(judge_name)
            if not slug:
                continue

            with open(slug + ".jpeg", "wb") as f_img:
                img_r.raw.decode_content = True
                shutil.copyfileobj(img_r.raw, f_img)

            img_hash = get_hash_from_file(slug + ".jpeg")

            # Update judges.json
            judge_pics[slug] = {
                "artist": None,
                "date_created": None,
                "license": "Work of Federal Government",
                "source": judge_link,
                "hash": img_hash,
            }

    json.dump(
        judge_pics,
        open(os.path.join(judge_root, "judges.json"), "w", encoding="utf-8"),
        sort_keys=True,
        indent=2,
    )


if __name__ == "__main__":
    run_things()
