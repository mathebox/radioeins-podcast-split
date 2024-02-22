import os
from pathlib import Path
import requests
import xml.etree.ElementTree as ET

def parse():
    url = 'https://www.radioeins.de/export/updates.xml/feed=podcast.xml'
    r = requests.get(url)
    root = ET.fromstring(r.text)

    # Find and remove all items (podcast episodes) that don't have the title Gut & Börse'
    for item in root[0].findall('item'):
        title = item.find('title').text
        if title == 'Gut & Börse':
            publication_date = item.find('pubDate').text
            item.find('title').text = f"{title} ({publication_date[:16]})"
        else:
            root[0].remove(item)

    # Rename channel
    root[0].find('title').text = 'Radio Eins: Gut & Börse'

    # Remove empty lines
    xml = os.linesep.join([s for s in ET.tostring(root).decode("utf-8").splitlines() if s])

    Path('generated-feeds').mkdir(parents=True, exist_ok=True)
    with open('generated-feeds/radioeins-gut-und-boerse.xml', 'w') as f:
        f.write(xml)
        

if __name__ == "__main__":
    parse()
