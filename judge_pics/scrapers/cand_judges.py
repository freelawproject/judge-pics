import hashlib
import json
import requests
import shutil

from judge_pics import judge_pics

from dateutil import parser
from lxml import html


token = ""
if token:
    headers = {"Authorization": "Token %s" % token}
else:
    print(
        "Warning: No CourtListener token used. You'll run out of free queries to the API quickly."
    )
    headers = {}


def granular_date(d, granularity):
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


def make_slug(name):
    """Hit our search engine and get back a good result. Look that up in the
    People endpoint to get glorius metadata.

    We start with a full name, so we plug that in.
    """
    # Drop middle initials
    name = name.lower()
    name = " ".join(
        [n.replace(",", "") for n in name.split() if not n.endswith(".")]
    )

    result_json = requests.get(
        "https://www.courtlistener.com/api/rest/v3/search/?type=p&name=%s&court=cand"
        % name,
        headers=headers,
    ).json()
    if result_json["count"] > 1:
        print(
            "Warning: Got back %s results for %s"
            % (result_json["count"], name,)
        )
        return None
    if result_json["count"] < 1:
        print("Warning: Got back no results for %s" % name)
        name_parts = name.split()
        if len(name_parts) == 2:
            return "%s-%s" % (name_parts[1].lower(), name_parts[0].lower())
        return None

    id = result_json["results"][0]["id"]
    result_json = requests.get(
        "https://www.courtlistener.com/api/rest/v3/people/?id=%s" % id,
        headers=headers,
    ).json()

    judge = result_json["results"][0]

    return "%s-%s%s" % (
        judge["name_last"].lower(),
        judge["name_first"].lower(),
        granular_date(judge["date_dob"], judge["date_granularity_dob"]),
    )


def get_hash_from_file(image):
    """Get the hash from the current file"""
    with open(image, "r") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_things():
    base_href = "http://www.cand.uscourts.gov"
    start_path = "/judges"
    start_url = base_href + start_path
    r = requests.get(start_url)
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
        judge_r = requests.get(judge_link)
        judge_html = html.fromstring(judge_r.text)
        judge_html.make_links_absolute(base_href)

        try:
            img_path = judge_html.xpath(
                '//div[@class = "judge_portrait"]//img/@src'
            )[0]
        except IndexError:
            print("Failed to find image for %s" % judge_link)
            continue

        img_r = requests.get(img_path, stream=True)
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
        open(os.path.join(judge_root, "judges.json"), "w"),
        sort_keys=True,
        indent=2,
    )


if __name__ == "__main__":
    run_things()
