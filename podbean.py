# Author:  Benjamin Johnson
# Version: 0.1
# Purpose: A Python3 wrapper for the Podbean API

import requests
import json
import os

class Podbean():
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret
        self.token = None

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
        else:
            print('Auth success')
            self.token = r['access_token']

    def upload_audio(self, path, fname):
        # file info
        fsize = os.path.getsize(path)

        # file authorize
        url = 'https://api.podbean.com/v1/files/uploadAuthorize'
        data = {
            'access_token': self.token,
            'filename': path,
            'filesize': fsize,
            'content_type': 'audio/mpeg'
        }
        r = requests.get(url, params=data).json()

        # error checking
        if 'error' in r:
            print('failed')
        else:
            print('Get Presigned URL success')
            print(r)
            self.presigned_url = r['presigned_url']
            self.file_key = r['file_key']

        # file upload
        head = {'Content-Type': 'audio/mpeg'}
        files = {'testaudio.mp3': open(path, 'rb')}
        r = requests.put(self.presigned_url, headers=head, files=files)

        print(r.status_code)
        print(r.content)


if __name__ == '__main__':
    pb = Podbean('id', 'secret')

    pb.auth()
    pb.upload_audio('path/to/filename', 'filename.mp3')
    print(pb.presigned_url)
