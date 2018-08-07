# SubtitleFinder
Find subtitle online using opensubtitles.org

## How to Run

1. `pipenv shell`
2. `pipenv install`
3. `python entry.py`
4. Browse and select a movie file, subtitle will be downloaded to the same folder.

## `config.ini` format

Create a `config.ini` file and paste the following.
```
[REMOTE]
opensub_url = https://rest.opensubtitles.org/search
user_agent = <user_agent>
```
Note: <user_agent> should be replaced with your id after you register at opensubtitles.org
