# Author:  Benjamin Johnson
# Version: 0.1
# Purpose: A Python3 wrapper for the Podbean API

import requests
import json
import os


# episode class
class Episode:
    def __init__(self):
        self.title = ''
        self.desc = ''
        self.audio_key = ''
        self.img_key = ''


class Podbean():
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret
        self.token = None

        # episode
        self.ep = Episode()

        # build episode
        self.ep.title = title
        self.ep.desc = desc
        self.ep.audio_key = audio_key
        self.ep.img = img_key

        # make request
        url = 'https://api.podbean.com/v1/episodes/'
        data = {
            'access_token': self.token,
            'title': self.ep.title,
            'type': 'public',
            'status': 'publish'
        }
        r = requests.post(url, data=data).json()

        print(r)

    def auth(self):
        # request
        url = 'https://api.podbean.com/v1/oauth/token'
        creds = (self.id, self.secret)
        data = {'grant_type': 'client_credentials'}
        r = requests.post(url, auth=creds, data=data).json()

        # error checking
        # TODO: clean this mess up
        if 'error' in r:
            print(f"failed\nreason: {r['error_description']}")
            return False
        else:
            print('Auth success')
            self.token = r['access_token']
            self.scope = r['scope']
            return True

    def upload_audio(self, fpath, fname):
        return self.upload_file('audio/mpeg', fpath, fname)

    def upload_image(self, fpath, fname):
        # TODO: maybe autodetect image filetype?
        return self.upload_file('image/jpeg', fpath, fname)

    def upload_file(self, ftype, fpath, fname):
        if fpath is None:
            return ''

        # file info
        fsize = os.path.getsize(fpath)

        # file authorize
        url = 'https://api.podbean.com/v1/files/uploadAuthorize'
        data = {
            'access_token': self.token,
            'filename': fname,
            'filesize': fsize,
            'content_type': ftype
        }
        r = requests.get(url, params=data).json()

        # error checking
        if 'error' in r:
            print('file auth failed')
        else:
            print('Get Presigned URL success')
            # print(r)
            self.presigned_url = r['presigned_url']
            self.file_key = r['file_key']

        # file upload
        head = {'Content-Type': ftype}
        with open(fpath, 'rb') as f:
            print(f)
        files = {'file': open(fpath, 'rb')}
        r = requests.put(self.presigned_url, headers=head, files=files)

        # check for success
        print('STATUS CODE')
        print(r.status_code)
        if r.status_code == 200:
            print('200: File upload success')
            return self.file_key
        else:
            print('not 200: File Upload fail')

    # episode creation
    def publish_episode(self, title, desc, audio_key, img_key):
        # check for Nones
        if audio_key is None:
            audio_key = ''
        if img_key == None:
            img_key = ''
