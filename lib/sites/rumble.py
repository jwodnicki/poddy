import bs4
import datetime
import urllib.parse


def get_url(pod):
    return f'https://rumble.com/user/{pod}/livestreams?e9s=src_v1_cmd&duration=any&sort=date&date=all-time'


def parse(page, pod):
    soup = bs4.BeautifulSoup(page, 'html.parser')
    page_title = soup.title.get_text(strip=True)
    channel_img_tag = soup.select_one('img.channel-header--img')['src']
    channel_img_url = channel_img_tag if channel_img_tag else None
    videos = []
    for ctr in soup.select('div.videostream.thumbnail__grid--item, div.videostream.thumbnail__grid--item'):
        title_tag = ctr.select_one('a.title__link h3.thumbnail__title')
        link_tag = ctr.select_one('a.title__link')
        time_tag = ctr.select_one('time.videostream__time')
        img_tag = ctr.select_one('img.thumbnail__image')
        if not (title_tag and link_tag and time_tag):
            continue
        title = title_tag.get('title') or title_tag.get_text(strip=True)
        href = link_tag.get('href', '')
        url = urllib.parse.urljoin('https://rumble.com', href)
        img_url = img_tag.get('src', '')
        datetime_attr = time_tag.get('datetime', '').strip()
        try:
            parsed_date = datetime.datetime.fromisoformat(datetime_attr)
            iso_date = parsed_date.isoformat()
        except Exception:
            iso_date = datetime_attr
        videos.append({
            'id': url.split('/')[-1].split('-')[0],
            'title': title,
            'url': url,
            'img_url': img_url,
            'date': iso_date,
        })
    return {
        'title': page_title,
        'img': channel_img_url,
        'videos': videos,
    }
