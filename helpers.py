import configparser
import os
import requests
import struct
from tkinter import filedialog, Tk


def get_movie_file()-> str:
    """
    Browse for a movie file and return filename.
    :return: filename
    """
    Tk().withdraw()
    return filedialog.askopenfilename(title='Select Movie File')


def get_user_agent()-> str:
    """
    Parse config.ini and return the User Agent string.
    This is sort of like the API for opensubtitles.org
    :return:
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['REMOTE']['user_agent']


def get_hash_value(name: str)-> str:
    """
    This function returns hash for a file.

    Hash along with file size is used to identify movie file by opensubtitles.org

    Lines 26 and 34 were modified for integer division in python3.6
    :param name: movie filename which needs to be hashed.
    :return:
    """
    try:

        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat)

        f = open(name, "rb")

        filesize = os.path.getsize(name)
        hash = filesize

        if filesize < 65536 * 2:
            return "SizeError"

        for x in range(65536//bytesize):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number


        f.seek(max(0,filesize-65536),0)
        for x in range(65536//bytesize):
            buffer = f.read(bytesize)
            (l_value,)= struct.unpack(longlongformat, buffer)
            hash += l_value
            hash = hash & 0xFFFFFFFFFFFFFFFF

        f.close()
        returnedhash =  "%016x" % hash
        return returnedhash

    except(IOError):
        return "IOError"


def get_response(movie_file: str):
    """
    For a given movie file, returns the response from opensubtitles.org.
    :param movie_file:
    :return:
    """
    user_agent = get_user_agent()
    header = {'User-Agent': user_agent}
    base_url = 'https://rest.opensubtitles.org/search'
    file_size = os.path.getsize(movie_file)
    file_hash = get_hash_value(movie_file)
    request_url = base_url+'/moviebytesize-%s/moviehash-%s/sublanguageid-eng' % (file_size, file_hash)
    return requests.get(request_url, headers=header)
