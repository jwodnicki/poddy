import cloudscraper
import json


def get_url(pod):
    return


def parse(page, pod):
    data = cloudscraper.create_scraper().post(
        'https://gql.twitch.tv/gql',
        json={
            'operationName': 'FilterableVideoTower_Videos',
            'variables': {
                'limit': 30,
                'channelOwnerLogin': pod,
                'broadcastType': 'ARCHIVE',
                'videoSort': 'TIME'
            },
            'extensions': {
                'persistedQuery': {
                    'version': 1,
                    'sha256Hash': 'a937f1d22e269e39a03b509f65a7490f9fc247d7f83d6ac1421523e3b68042cb'
                }
            }
        },
        headers={
            'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        }
    ).json()
    user = data.get('data', {}).get('user')

    videos = []
    for video in user.get('videos', {}).get('edges', []):
        node = video.get('node', {})
        videos.append({
            'id': node.get('id', ''),
            'title': node.get('title', ''),
            'url': f'https://www.twitch.tv/videos/{node.get('id', '')}',
            'img_url': node.get('previewThumbnailURL', ''),
            'date': node.get('publishedAt', '')
        })

    return {
        'title': user.get('displayName', pod),
        'img': user.get('profileImageURL', ''),
        'videos': videos
    }
