import os
from pathlib import Path
import requests
import xml.etree.ElementTree as ET

FEED_URL = 'https://raw.githubusercontent.com/mathebox/radioeins-podcast-split/feeds/radioeins-gut-und-boerse.xml'  # noqa: E501
COVER_ART_URL = 'https://raw.githubusercontent.com/mathebox/radioeins-podcast-split/feeds/covers/radioeins-gut-und-boerse.png'  # noqa: E501


def is_interesting(item):
    if 'Gut & Börse' in item.find('title').text:
        return True

    if description := item.find('description').text:
        if 'finanztip' in description.lower():
            return True

    return False


def parse():
    url = 'https://www.radioeins.de/export/updates.xml/feed=podcast.xml'
    r = requests.get(url)
    root = ET.fromstring(r.text)

    # Find and remove all items (podcast episodes) that are not 'interesting'
    for item in root[0].findall('item'):
        if not is_interesting(item):
            root[0].remove(item)

    # Rename channel
    root[0].find('title').text = 'Gut & Börse'

    # Change cover art of channel and episodes
    for href_tag in root[0].findall('.//*[@href]'):
        if 'image' in href_tag.tag:
            href_tag.set('href', COVER_ART_URL)
        elif 'link' in href_tag.tag:
            href_tag.set('href', FEED_URL)

    # Remove empty lines
    single_lines = ET.tostring(root).decode("utf-8").splitlines()
    xml = os.linesep.join([line for line in single_lines if line])

    Path('generated-feeds').mkdir(parents=True, exist_ok=True)
    with open('generated-feeds/radioeins-gut-und-boerse.xml', 'w') as f:
        f.write(xml)


if __name__ == "__main__":
    parse()
