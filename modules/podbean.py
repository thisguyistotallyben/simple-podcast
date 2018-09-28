# Author:  Benjamin Johnson
# Version: 0.1
# Purpose: A Python3 wrapper for the Podbean API (Python 3.6 or higher)

import requests
import json
import os

from pydub import AudioSegment


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

    def update_credentials(self, id, secret):
        self.id = id
        self.secret = secret

    def auth(self):
        '''
        Logs into the Podbean API to do anything.
        This must be done before any uploading.

        Limitations: Requires an app to be registered for each user using this.
        '''

        # request auth
        creds = (self.id, self.secret)
        data = {'grant_type': 'client_credentials'}
        r = requests.post(self.auth_url, auth=creds, data=data).json()

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
        try:
            fsize = os.path.getsize(fpath)
        except FileNotFoundError as e:
            raise PodbeanError('file upload', 'file does not exist')
        fext = fpath.rsplit('.', 1)[-1]
        fname = fpath.rsplit('/', 1)[-1]

        # get podbean suitable file type
        if fext == 'mp3':
            ftype = f'audio/{fext}'
        if fext == 'wav':
            print('Converting wav to mp3')
            self.convert(fpath)
            # TEMPORARY FOR NOW PLS FIX FPATH THANKS
            fpath = 'output.mp3'
            ftype = 'audio/mp3'
            fname = 'output.mp3'
        elif fext in ('jpg', 'jpeg', 'png'):
            ftype = f'image/{fext}'
        else:
            raise PodbeanError('file upload', f'unsupported file type {fext}')

        print(fext, fname, ftype)

        # file authorize
        data = {
            'access_token': self.token,
            'filename': fname,
            'filesize': fsize,
            'content_type': ftype
        }
        r = requests.get(self.upload_url, params=data).json()

        # error checking
        if 'error' in r:
            raise PodbeanError('file upload', r['error_description'])
        else:
            print('Get Presigned URL success')
            # print(r)
            self.presigned_url = r['presigned_url']
            self.file_key = r['file_key']

        # file upload
        head = {'Content-Type': ftype}
        files = {'file': open(fpath, 'rb')}
        r = requests.put(self.presigned_url, headers=head, files=files)

        # check for success
        print('STATUS CODE')
        print(r.status_code)
        if r.status_code == 200:
            print('200: File upload success')
            return self.file_key
        else:
            raise PodbeanError('file upload', 'upload failed')

    # ## EPISODE LAND # ##

    def publish_episode(self, **kwargs):
        '''
        Publishes an episode
        TODO: Add full list of possible kwargs
        '''

        # build POST data
        # TODO: actually error check this
        for k in kwargs.keys():
            if k not in ('title', 'content', 'status', 'type', 'media_key', 'logo_key'):
                raise PodbeanError('publish episode', f'invalid arg {k}')

        # add necessary stuff
        kwargs['access_token'] = self.token
        if 'status' not in kwargs.keys():
            kwargs['status'] = 'publish'
        if 'type' not in kwargs.keys():
            kwargs['type'] = 'public'

        print(kwargs)
        r = requests.post(self.publish_url, data=kwargs).json()

        print(r)

    def convert(self, fpath):
        audio = AudioSegment.from_wav(fpath)
        # FIX THIS - JUST FOR TESTING
        audio.export('output.mp3', format='mp3')

'''
Exception Central
'''

# base exception
class PodbeanError(Exception):
    def __init__(self, stage, reason):
        self.stage = stage
        self.reason = reason
