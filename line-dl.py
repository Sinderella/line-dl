# coding=utf-8

import json
import os
import re

from requester import Requester


class LineDL(object):
    def __init__(self, proxy):
        self.bad_kws = ['behind-the-scene']
        self.base_url = 'https://tv.line.me{}'
        self.api_url = 'http://global-nvapis.line.me/linetv/rmcnmv/vod_play_videoInfo.json?videoId={}&key={}'
        self.list_url = 'https://tv.line.me/api/{0}/playlist/{1}/{2}/false/false'
        self.playlist_pattern = re.compile('var currentClipNo = "([0-9]+)";\s+var currentPlaylistId = "([0-9]+)')
        self.playlist_api_pattern = re.compile('href="(.*?)"')
        self.title_pattern = re.compile('clickcr\(this, \'vpr\.title\', \'([A-Za-z0-9]+)\'')
        self.key_pattern = re.compile('videoId: \'([A-Za-z0-9]+)\',\s+key: \'([A-Za-z0-9]+)\'')

        self.req = Requester(proxy)

    def download_list(self, list_url):
        resp = self.req.getp(list_url)
        tmp = self.playlist_pattern.search(resp.text)
        clip_no = tmp.group(1)
        playlist_id = tmp.group(2)

        tmp = self.title_pattern.search(resp.text)
        title = tmp.group(1)

        list_url_api = self.list_url.format(clip_no, title, playlist_id)
        resp = self.req.getp(list_url_api)
        urls = sorted(set(self.playlist_api_pattern.findall(resp.text)))
        for url in urls:
            if any(bad_kw in url for bad_kw in self.bad_kws):
                continue
            self.download_ep(self.base_url.format(url))

    def download_ep(self, url):
        resp = self.req.getp(url)
        tmp = self.key_pattern.search(resp.text)
        video_id = tmp.group(1)
        key = tmp.group(2)
        json_resp = self.req.getp(self.api_url.format(video_id, key))

        json_loaded = json.loads(json_resp.text)
        # pick highest res
        ep_name = json_loaded['meta']['subject']
        print('Downloading {}'.format(ep_name))
        self.req.download(json_loaded['videos']['list'][-1]['source'], os.path.expanduser('~/Downloads/'), ep_name)


if __name__ == '__main__':
    urls = [
            ]
    proxy = ''

    ldl = LineDL(proxy)
    [ldl.download_list(url) for url in urls]
