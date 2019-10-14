#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import urllib.request, json
import ssl
import os
import time

__author__ = 'mustafauzun0'

def main():
    parser = argparse.ArgumentParser(description='Instagram user photos zipper')

    parser.add_argument('-u', '--user', dest='user', type=str, help='Instagram Username', required=True)
    parser.add_argument('-i', '--info', dest='info', action='store_true', help='User Info')
    parser.add_argument('-p', '--path', dest='path', default='.', type=str, help='Saved Path')
    parser.add_argument('-d', '--download', dest='download', action='store_true', help='Download')

    args = parser.parse_args()

    ssl._create_default_https_context = ssl._create_unverified_context

    with urllib.request.urlopen('https://www.instagram.com/' + args.user + '/?__a=1') as url:
        data = json.loads(url.read().decode())
        user = data['graphql']['user']

        if args.info:
                print('Ad:', user['full_name'])
                print('Bio:', user['biography'])
                print('Takip Edilenler:', user['edge_followed_by']['count'])
                print('Takipciler:', user['edge_follow']['count'])
                print('Gizli Hesap:', (user['blocked_by_viewer'] and 'Evet' or 'Hayır'))
        
        if args.download:
                print('Fotograflar Indiriliyor...', end='', flush=True)
                folder = '{path}/{folder}_{time}'.format(path=args.path, folder=user['username'], time=time.time())
                os.mkdir(folder)
                for image in user['edge_owner_to_timeline_media']['edges']:
                        urllib.request.urlretrieve(image['node']['display_url'], '{folder}/{file}.jpg'.format(folder=folder, file=image['node']['id']))
                print('\rFotograf Indirme Tamamlandı.\n', end='', flush=True)


if __name__ == '__main__':
    main()
