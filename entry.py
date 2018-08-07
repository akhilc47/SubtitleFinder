import gzip
import json
import os
import requests
from helpers import get_movie_file, get_response


def main():
    movie_file = get_movie_file()
    parsed = json.loads(get_response(movie_file).content)
    if not parsed:
        print('Could not find subtitle')
        return
    sub_response = requests.get(parsed[0]['SubDownloadLink'])
    movie_dir = os.path.dirname(movie_file)
    sub_name = parsed[0]['SubFileName']
    with open(os.path.join(movie_dir, sub_name), 'wb') as fsub:
        fsub.write(gzip.decompress(sub_response.content))


if __name__ == "__main__":
    main()
