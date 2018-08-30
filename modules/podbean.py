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
        '''
        Sets up most of the variables needed

        param id: The client ID
        param secret: The client secret
        '''

        self.id = id
        self.secret = secret
        self.token = None

        # urls for easy reading
        self.auth_url = 'https://api.podbean.com/v1/oauth/token'
        self.upload_url = 'https://api.podbean.com/v1/files/uploadAuthorize'
        self.publish_url = 'https://api.podbean.com/v1/episodes/'

        # episode
        self.ep = Episode()

    # ## AUTHORIZATION LAND # ##

    def auth(self):
        '''
        Logs into the Podbean API to do anything.
        This must be done before any uploading.

        Limitations: Requires an app to be registered for each user using this.
        '''

        # request auth
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

    def renew_auth(self):
        '''
        Renew the access token
        I should probably do this to save so many requests
        '''
        return

    # ## FILE UPLOAD LAND ## #

    def upload_file(self, fpath):
        '''
        Automatically determines what kind of file you are uploading and
        uploads it if the file type is supported

        param fpath: The file path to upload

        returns: temporary key to use in episode publishing
        '''

        # file info
        # fsize = os.path.getsize(fpath)
        fext = fpath.rsplit('.', 1)[-1]
        fname = fpath.rsplit('/', 1)[-1]

        # get podbean suitable file type
        if fext == 'mp3':
            ftype = 'audio/mp3'
        elif fext in ('jpg', 'jpeg', 'png'):
            ftype = f'image/{fext}'
        else:
            ftype = ''
            print('failure, you should probably handle this better')

        print(fext, fname, ftype)

        '''

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
        '''

    # ## EPISODE LAND # ##

    def publish_episode(self, title, desc, audio_key, img_key):
        # check for Nones
        if audio_key is None:
            audio_key = ''
        if img_key == None:
            img_key = ''

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
