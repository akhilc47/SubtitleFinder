import gzip
import json
import os
import requests
from helpers import get_movie_file, get_response


def main():
    try:
        movie_file = get_movie_file()
    except FileNotFoundError:
        print('File not selected, exiting')
        return -1

    response = get_response(movie_file)
    if 'useragent is not valid' in response.text:
        print(response.text)
        return -1

    parsed = json.loads(response.content)
    if not parsed:
        print('Could not find subtitle')
        return -1

    print('Movie Found: %s' % parsed[0]['MovieName'])
    sub_response = requests.get(parsed[0]['SubDownloadLink'])
    print('Subtitle Found: %s' % parsed[0]['SubFileName'])
    movie_dir = os.path.dirname(movie_file)
    sub_name = parsed[0]['SubFileName']
    with open(os.path.join(movie_dir, sub_name), 'wb') as fsub:
        fsub.write(gzip.decompress(sub_response.content))
    print('Subtitle extracted to the movie folder')
    return 0


if __name__ == "__main__":
    if main() == 0:
        print('Exiting...')
