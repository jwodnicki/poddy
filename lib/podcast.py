import yt_dlp
import mutagen
import mutagen.mp3
import os


def fetch(outfile, url, title, artist, cover, bitrate='128', stereo=False):
    yt_dlp.YoutubeDL({
        'format': 'bestaudio/best',
        'outtmpl': outfile,
        'quiet': False,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': str(bitrate),
        }],
        'postprocessor_args': [
            '-ac', '2' if stereo else '1'
        ],
        'keepvideo': False
    }).download([url])
    outfile += '.mp3'

    audio = mutagen.easyid3.EasyID3(outfile)
    audio['title'] = title
    audio['artist'] = artist
    audio.save()

    id3 = mutagen.id3.ID3(outfile)
    with open(cover, 'rb') as img:
        id3['APIC'] = mutagen.id3.APIC(
            encoding=3,
            mime='image/jpeg',
            type=3,
            desc='Cover',
            data=img.read()
        )
    id3.save()


def get_metadata(outfile):
    t = int(mutagen.mp3.MP3(outfile).info.length)
    return os.path.getsize(outfile), f"{t//3600:02}:{(t % 3600)//60:02}:{t % 60:02}"
