import xml.etree.ElementTree as ET
import datetime


def create(outfile, site, title, pod, videos, host_url):
    pod_url = f'{host_url}/{site}/{pod}'

    rss = ET.Element('rss', version='2.0', attrib={
        'xmlns:itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
    })

    channel = ET.SubElement(rss, 'channel')
    ET.SubElement(channel, 'title').text = title
    ET.SubElement(channel, 'link').text = pod_url
    ET.SubElement(
        channel, 'description').text = f'{title} fetched from {site} by poddy'
    ET.SubElement(channel, 'itunes:image', href=f'{pod_url}/img/{channel}')
    for video in videos:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = video['title']
        ET.SubElement(item, 'enclosure', url=f"{pod_url}/{video['id']}.mp3", length=str(
            video.get('length', 0)), type='audio/mpeg')
        ET.SubElement(item, 'guid').text = pod_url + '/' + video['id']
        ET.SubElement(item, 'pubDate').text = datetime.datetime.fromisoformat(
            video['date']).strftime('%a, %d %b %Y %H:%M:%S GMT')
        ET.SubElement(item, 'itunes:duration').text = video.get('duration', '')

    ET.ElementTree(rss).write(outfile, encoding='utf-8', xml_declaration=True)
