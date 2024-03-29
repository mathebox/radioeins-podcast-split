import os
from pathlib import Path
import requests
import xml.etree.ElementTree as ET

FEED_URL = 'https://raw.githubusercontent.com/mathebox/radioeins-podcast-split/feeds/radioeins-gut-und-boerse.xml'
COVER_ART_URL = 'https://raw.githubusercontent.com/mathebox/radioeins-podcast-split/feeds/covers/radioeins-gut-und-boerse.png'

def parse():
    url = 'https://www.radioeins.de/export/updates.xml/feed=podcast.xml'
    r = requests.get(url)
    root = ET.fromstring(r.text)

    # Find and remove all items (podcast episodes) that don't have the title Gut & Börse'
    for item in root[0].findall('item'):
        title = item.find('title').text
        if not 'Gut & Börse' in title:
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
    xml = os.linesep.join([s for s in ET.tostring(root).decode("utf-8").splitlines() if s])

    Path('generated-feeds').mkdir(parents=True, exist_ok=True)
    with open('generated-feeds/radioeins-gut-und-boerse.xml', 'w') as f:
        f.write(xml)
        

if __name__ == "__main__":
    parse()
