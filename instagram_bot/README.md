# Instagram Auto Downloader & Reposter Bot

## Description
This Python script automates the process of:
1. Downloading the latest post from a specific Instagram account.
2. Saving session credentials to avoid repeated logins.
3. Extracting captions and media files.
4. Reposting the content with the original caption.

## Requirements
- Python 3.x
- Instaloader (`pip install instaloader`)
- Requests (`pip install requests`)

## Setup Instructions
1. **Edit `InstagramReuploader.py`**:
   - Add your Instagram **username/password**.
   - Add **Instagram API access token** (needed for reuploading).

2. **Run the bot**:
   ```sh
   python InstagramReuploader.py
   ```
