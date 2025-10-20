#!/usr/bin/env python

import lib.podcast
import lib.rss
import cloudscraper
import argparse
import configparser
import importlib
import os

HDR = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Safari/605.1.1'
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('-d', '--dir', default='.',
                   help="Base directory (default: %(default)s)")
    p.add_argument('-n', '--num-files', type=int, help="Number of files")
    p.add_argument('-b', '--bitrate', type=int, default=128,
                   help="Bitrate (default: %(default)s)")
    p.add_argument('-s', '--stereo', action='store_true',
                   help="Enable stereo (default: False)")
    p.add_argument('-c', '--purge-missing', action='store_true',
                   help="Purge missing files (default: False)")
    p.add_argument('-u', '--host-url', required=True,
                   help="Base URL for hosting")
    return p.parse_args()


def get_pods(args):
    config = configparser.ConfigParser()
    cs = cloudscraper.create_scraper()
    for site in [s for s in os.listdir(args.dir) if not s.startswith('.')]:
        site_dir = os.path.join(args.dir, site)
        mod = importlib.import_module(f'lib.sites.{site}')
        for pod in [s for s in os.listdir(site_dir) if not s.startswith('.')]:
            pod_dir = os.path.join(site_dir, pod)
            config_file = os.path.join(pod_dir, 'config.ini')
            override = {}
            if os.path.exists(config_file):
                config.read(config_file)
                for key in ('title', 'url'):
                    value = config.get('podcast', key, fallback=None)
                    if value:
                        override[key] = value
            url = override.get('url', mod.get_url(pod))
            page = mod.parse(
                cs.get(url, headers=HDR).text if url else None,
                pod
            )
            page['title'] = override.get('title', page['title'])
            os.makedirs(os.path.join(pod_dir, 'img'), exist_ok=True)
            if page['img']:
                img_path = os.path.join(pod_dir, 'img', 'channel')
                if not os.path.exists(img_path):
                    with open(img_path, 'wb') as f:
                        f.write(cs.get(page['img'], headers=HDR).content)
            mp3_exists = set(os.listdir(pod_dir))
            videos = page['videos'][:args.num_files]
            for video in videos:
                outfile = os.path.join(pod_dir, video['id'])
                if video['img_url']:
                    img_path = os.path.join(
                        pod_dir, 'img', video['id'] + '.jpg')
                    if not os.path.exists(img_path):
                        with open(img_path, 'wb') as f:
                            f.write(cs.get(
                                video['img_url'], headers=HDR).content)
                if video['id'] + '.mp3' in mp3_exists:
                    mp3_exists.remove(video['id'] + '.mp3')
                else:
                    lib.podcast.fetch(
                        outfile=outfile,
                        url=video['url'],
                        title=video['title'],
                        artist=pod,
                        cover=img_path,
                        bitrate=args.bitrate,
                        stereo=args.stereo,
                    )
                video['length'], video['duration'] = lib.podcast.get_metadata(
                    outfile + '.mp3')
            lib.rss.create(
                outfile=os.path.join(pod_dir, 'index.xml'),
                site=site,
                title=page['title'],
                pod=pod,
                videos=videos,
                host_url=args.host_url,
            )
            if args.purge_missing:
                for missing in mp3_exists:
                    os.remove(os.path.join(pod_dir, missing))
                    os.remove(os.path.join(
                        pod_dir, 'img', missing[:-4] + '.jpg'))


if __name__ == '__main__':
    get_pods(parse_args())
