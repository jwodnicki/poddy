import datetime
import json
import re


def get_url(pod):
    return f'https://www.youtube.com/@{pod}/streams'


def parse(page, pod):
    m = re.search(r'var ytInitialData = ({.*?});</script>', page)
    j = json.loads(m.group(1))
    page_title = re.search(r'<title>(.*?)</title>',
                           page).group(1).replace(' - YouTube', '')
    img = re.search(r'"avatar":\{"thumbnails":\[\{"url":"(https:[^"]+)"', page)
    channel_img_url = img.group(1) if img else ''
    videos = []
    for tab in j['contents']['twoColumnBrowseResultsRenderer']['tabs']:
        cont = tab.get('tabRenderer', {}).get('content', {})
        if 'richGridRenderer' in cont:
            items = cont['richGridRenderer'].get('contents', [])
        elif 'sectionListRenderer' in cont:
            items = cont['sectionListRenderer']['contents']
        else:
            continue
        for it in items:
            vr = (it.get('richItemRenderer', {}) or {}).get('content', {}).get('videoRenderer') \
                or (it.get('gridRenderer', {}) or {}).get('items', [{}])[0].get('gridVideoRenderer')
            if not vr:
                continue
            title = vr.get('title', {}).get('runs', [{}])[0].get('text', '')
            url = 'https://www.youtube.com/watch?v=' + vr.get('videoId', '')
            img_url = vr.get('thumbnail', {}).get(
                'thumbnails', [{}])[-1].get('url', '')
            t = vr.get('publishedTimeText', {}).get('simpleText', '')
            n = int(re.search(r'\d+', t).group()
                    ) if re.search(r'\d+', t) else 0
            delta = datetime.timedelta(days=n if 'day' in t else 0,
                                       weeks=n if 'week' in t else 0,
                                       hours=n if 'hour' in t else 0)
            date = (datetime.datetime.utcnow() - delta).isoformat()
            videos.append({
                'id': url.split('v=')[1],
                'title': title,
                'url': url,
                'img_url': img_url,
                'date': date,
            })
    return {
        'title': page_title,
        'img': channel_img_url,
        'videos': videos,
    }
