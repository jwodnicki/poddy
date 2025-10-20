import bs4
import cloudscraper
import datetime


def get_url(pod):
    return f'https://kick.com/{pod}/videos'


def parse(page, pod):
    soup = bs4.BeautifulSoup(page, 'html.parser')
    data = cloudscraper.create_scraper().get(
        f'https://kick.com/api/v2/channels/{pod}/videos').json()
    return {
        'title': soup.title.get_text(strip=True),
        'img': soup.find('link', rel='preload', attrs={'as': 'image'}),
        'videos': [{
            'id': v['video']['uuid'],
            'title': v.get('session_title', ''),
            'url': f"https://kick.com/{pod}/videos/v['video']['uuid']",
            'img_url': v.get('thumbnail', {}).get('src', ''),
            'date': datetime.datetime.strptime(v.get('start_time', '1970-01-01 00:00:00'), '%Y-%m-%d %H:%M:%S').isoformat()
        } for v in data]
    }
