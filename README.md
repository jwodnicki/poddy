# poddy

**poddy** converts videos from various streaming platforms into podcast-ready audio streams.
It’s designed for people who want to turn video libraries into audio-friendly feeds for easy listening on the go.

---

## 🚀 Features

- 🎥 Converts video site archives into podcast audio streams
- 🔊 Adjustable bitrate and stereo support
- 🌐 Generates self-hostable podcast feeds with your own base URL
- ⚙️ Simple command-line interface

---

## 🧰 Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 💡 Usage

Run the script from the command line:

```bash
python run.py -u https://your-host.com/podcast
```

### Available Options

| Option | Long form | Type | Default | Description |
|:-------|:-----------|:------|:----------|:-------------|
| `-d` | `--dir` | `str` | `.` | Base directory for input/output |
| `-n` | `--num-files` | `int` | `None` | Number of files to process |
| `-b` | `--bitrate` | `int` | `128` | Output audio bitrate (kbps) |
| `-s` | `--stereo` | flag | `False` | Enable stereo output |
| `-c` | `--purge-missing` | flag | `False` | Delete missing or invalid files |
| `-u` | `--host-url` | `str` | *required* | Base URL for podcast hosting |

Example:

```bash
python run.py -d ./downloads -n 10 -b 192 -s -u https://your-host.com/feed
```

This command:
- Converts up to 10 files from `./downloads/youtube/channelname`
- Outputs in 192kbps stereo
- Generates podcast metadata using your host URL

---

## 🧩 Example Integration

Use `cron` or `systemd` to automate updates:

```bash
0 3 * * * /usr/bin/python3 /path/to/run.py -u https://your-host.com/podcast
```

---

## ❤️ Contributing

Pull requests are welcome!
If you have ideas for new sources or better feed handling, feel free to open an issue.

---

## 🌟 Future Plans

- Support for more video sites
- Transcription and chapter markers
- Web dashboard for feed management
