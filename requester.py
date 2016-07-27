import os
import subprocess

from requests import Session
from requests.adapters import HTTPAdapter


class Requester(object):
    def __init__(self, proxy):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
        }
        self.proxies = {
            'http': proxy,
            'https': proxy
        }
        self.session = Session()
        self.session.headers.update(self.headers)
        self.session.mount('http://', HTTPAdapter(max_retries=10))
        self.session.mount('https://', HTTPAdapter(max_retries=10))

    def getnop(self, url):
        return self.session.get(url)

    def getp(self, url):
        return self.session.get(url, proxies=self.proxies)

    @staticmethod
    def download(url, path, file_name):
        cleaned_fn = file_name.replace('/', '-') + '.mp4'
        subprocess.Popen(['/usr/local/bin/aria2c', '-x', '4', '-d', path, '-o', cleaned_fn, url]).wait()
        # res = self.session.get(url, stream=True)
        # with open(os.path.join(path, cleaned_fn), 'wb') as f:
        #     for chunk in res.iter_content(chunk_size=2048):
        #         if chunk:
        #             f.write(chunk)
