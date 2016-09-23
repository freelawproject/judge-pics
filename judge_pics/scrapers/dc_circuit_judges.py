import hashlib
import json
import re
import requests
import shutil
import subprocess
import os

from lxml import html

from judge_pics import judge_pics, judge_root


root_url = 'http://dcchs.org/Portraits/'
line_re = re.compile('<a href="(.*)">(.*)</a')


def make_slug(name, path):
    last_name = re.search('(.*),', name).group(1).lower()
    first_name = re.search('([A-Z].*)[A-Z]', path).group(1).lower()
    return '%s-%s' % (last_name, first_name)


def get_artist_and_date_created(full_url):
    # Open firefox, prompt for answer, sanitize answer and return it.
    subprocess.Popen(['firefox', full_url], shell=False).communicate()
    artist = raw_input('Who made this: ')
    if artist == '':
        artist = None

    d = raw_input('When did they make it: ')
    if d == '':
        d = None
    return artist, d


def get_hash_from_file(image):
    """Get the hash from the current file"""
    with open(image, 'r') as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_things():
    with open('sources.txt', 'r') as f:
        for line in f:
            # <a href="JesseAdkins.html">Adkins, Jesse C.</a><br>
            path = line_re.search(line).group(1)
            name = line_re.search(line).group(2)

            slug = make_slug(name, path)

            full_url = root_url + path

            r = requests.get(full_url,
                             headers={'UserAgent': 'freelawproject.org'})
            tree = html.fromstring(r.text)
            try:
                img_path = tree.xpath('//div[@id="contentcolumn"]//img/@src')[0]
                full_img_src = root_url + img_path
            except IndexError:
                print "Failed to find image for %s" % full_url
                continue

            r_img = requests.get(full_img_src, stream=True)
            if r_img.status_code == 200:
                with open(slug + '.jpeg', 'wb') as f_img:
                    r_img.raw.decode_content = True
                    shutil.copyfileobj(r_img.raw, f_img)

            artist, date_created = get_artist_and_date_created(full_url)

            img_hash = get_hash_from_file(slug + '.jpeg')

            # Update judges.json
            judge_pics[slug] = {
                'artist': artist,
                'date_created': date_created,
                'license': 'Work of Federal Government',
                'source': 'Historical Society of the District of Columbia '
                          'Circuit',
                'hash': img_hash,
            }

    json.dump(
        judge_pics,
        open(os.path.join(judge_root, 'judges.json'), 'w'),
        sort_keys=True,
        indent=2,
    )

if __name__ == '__main__':
    run_things()
