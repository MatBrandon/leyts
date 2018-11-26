# import datetime
import json, re, math
import time
import os
import sys
from datetime import datetime
import id3Parser
# import mutagen
# import mutagen.mp3
# from PIL import Image
import urllib.error
import urllib.request
# import urllib.parse
try:
    from urllib.parse import urlencode, unquote, quote_plus
    #from html.parser import HTMLParser
    # from urllib.request import Request, urlopen
    # from urllib.error import URLError, HTTPError
except ImportError:
    from urllib import urlencode, unquote, quote_plus
    #from HTMLParser import HTMLParser

class result(object):
    album_location_json = 'mp3/{}/info.json'
    album_location_cover = 'mp3/{}/cover{}'
    album_location_audio = 'mp3/{}/{}.mp3'
    album_cover_save_filename = False
    album_audio_save_filename = False
    artist_lists={}
    album_lists={}
    album_list_scan_audio_save = False
    album_list_scan_by_artist = 0
    error_msg=False
    user_agent = 'Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0'
    headers = {'User-Agent': user_agent}

    def __init__(self,domain_name,domain_extension):
        self.domain_name = domain_name[::-1]
        self.domain_extension = domain_extension[::-1]
        pass

    def load(self,url):
        """ get from online """
        req = urllib.request.Request(url, headers=self.headers)
        try:
            return urllib.request.urlopen(req)
        except urllib.error.URLError as errno:
            self.error_msg=str(errno.reason)

    def open(self):
        """ get from offline """
        pass

    def json_save(self,filename,data):
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(filename, "w", encoding='utf8') as file:
            json.dump(data, file, ensure_ascii=False)

    def json_load(self,filename):
        with open(filename, "r", encoding='utf8') as file:
            return json.load(file)

    def load_request(self,url):
        """ get from online """
        response = self.load(url)
        if response:
            data = response.read()
            data = data.decode('utf-8', 'replace')
            return re.sub("\s\s+", "", data).replace('\n', '').replace('\r', '')

    def artist_list_scan(self,item_lang,item_type,item_start,item_end=0):
        # en,mm - M,F,G
        # self.domain_name,self.domain_extension,
        url = 'https://www.{}.{}/{}/artists/list?artType={}&Artists-page={}'.format(self.domain_name,self.domain_extension,item_lang,item_type,item_start)
        data = self.load_request(url)
        if data:
            self.error_msg=False
            container = re.findall('<div.*?id="Artists".*?>(.*?)</div>', data)[0]
            artists_container = re.findall('<a href="/.*?/artists/browse/(.*?)/.*?".*?>(.*?)</a>', container)
            if artists_container:
                print('page-{}'.format(item_start))
                for artist in artists_container:
                    id=artist[0]
                    name=artist[1]
                    if hasattr(self, 'artist_ids'):
                        if id not in self.artist_ids:
                            self.artist_ids[id]={'name':name}
                            print(id)
                        else:
                            print('-',id)
                    self.artist_lists[id]= {'name':name}

                if item_end and item_start < item_end:
                    item_start = item_start + 1;
                    self.artist_list_scan(item_lang,item_type,item_start,item_end)
                else:
                    print('page-end-by-input-{}'.format(item_start))
            else:
                # NOTE: No more page
                print('page-end-at-last-{}'.format(item_start))
        elif item_lang == 'mm':
            print('...trying:{} in en'.format(item_start))
            self.artist_list_scan('en',item_type,item_start,item_end)
        elif self.error_msg:
            print('[??]',self.error_msg)
        else:
            print('{}-error'.format(item_start))

    def album_list_scan(self,item_lang,item_type,item_start,item_end=0):
        # en,mm - S,C,V
        # self.album_list_scan_by_artist = 12
        if self.album_list_scan_by_artist:
            url = 'https://www.{}.{}/{}/artists/browse/{}/a/{}?Albums-page={}'.format(self.domain_name,self.domain_extension,item_lang,self.album_list_scan_by_artist,item_type,item_start)
        else:
            url = 'https://www.{}.{}/{}/albums/index?albumType={}&Albums-page={}'.format(self.domain_name,self.domain_extension,item_lang,item_type,item_start)

        data = self.load_request(url)
        if data:
            self.error_msg=False
            container = re.findall('<div.*?id="Albums".*?>(.*?)</div>', data)[0]
            albums_container = re.findall('<a href="/.*?/albums/pull/(.*?)/.*?".*?>(.*?)</a>', container)
            if albums_container:
                print('page-{}'.format(item_start))
                for album in albums_container:
                    id=album[0]
                    title=album[1]
                    if hasattr(self, 'album_ids'):
                        if id not in self.album_ids:
                            self.album_ids[id]={'title':title}
                            print(id)
                        else:
                            print('-',id)
                    self.album_lists[id]= {'title':title}
                    if self.album_list_scan_audio_save:
                        self.album_info('mm',id,True)

                if item_end:
                    if not item_end.isnumeric():
                        self.album_list_scan('mm',item_type,int(item_start) + 1,item_end)
                    elif item_start < item_end:
                        self.album_list_scan('mm',item_type,int(item_start) + 1,item_end)
                    else:
                        print('page-end-by-input-{}'.format(item_start))
                # if item_end and item_start < item_end:
                #     item_start = item_start + 1;
                #     self.album_list_scan(item_lang,item_type,item_start,item_end)
                else:
                    print('page-end-one-{}'.format(item_start))
            else:
                # NOTE: No more page
                print('page-end-at-last-{}'.format(item_start))
        elif item_lang == 'mm':
            print('...trying:{} in en'.format(item_start))
            self.album_list_scan('en',item_type,item_start,item_end)
        elif self.error_msg:
            print('[??]',self.error_msg)
        else:
            print('{}-error'.format(item_start))

    def album_info(self,lang,album_id,album_info_save_audio=False):
        url = 'https://www.{}.{}/{}/albums/pull/{}/'.format(self.domain_name,self.domain_extension,lang,album_id)
        data = self.load_request(url)
        if data:
            container = re.findall('<div.*?id="albumwrap".*?>(.*?)</div>', data)
            if container:
                try:
                    album = self.json_load(self.album_location_json.format(album_id))
                except Exception as e:
                    album = {}

                album_cover = re.findall('<div.*?class="albumimg".*?><img.*?src="(.*?)".*?></div>', data)[0]
                album['id'] = album_id
                album['cover'] = album_cover
                if album_info_save_audio:
                    self.album_cover_save(album_id,album_cover)

                album_name = re.findall('<div.*?class="h1m".*?>(.*?)</div>', data)
                if album_name:
                    album_name = album_name[0]
                else:
                    album_name = re.findall('<span.*?class="h1e".*?>(.*?)</span>', data)[0]

                album_name = album_name.strip()
                album['name'] = album_name

                if 'artists' not in album:
                    album['artists']={}

                album_artist = re.findall('<div.*?class="albart".*?>.*?<ul.*?>(.*?)</ul>.*?</div>', data)
                album_artist = re.findall('<a.*?href="/.*?/Artists/Browse/(\d+)/.*?".*?>(.*?)</a>', album_artist[0])
                # album['artists'] = list(map(lambda x: {x[0]:x[1].strip()}, album_artist))
                for i in album_artist: album['artists'][i[0]]=i[1].strip()
                album_artist = album['artists']

                album_meta = re.findall('<div.*?class="descbox".*?>(.*?)</ul></div>', data)
                album_meta = re.sub('alt="Rate Album"', '', album_meta[0])
                album_meta = re.findall('<li.*?><img.*?alt="(.*?)".*?><span.*?>(.*?)</span></li>', album_meta)

                album['meta']={}
                album_year=False
                for i in album_meta: album['meta'][i[0]]=i[1].strip()

                if 'Released Date' in album['meta']:
                    # 13/03/2005
                    # album['meta']['Released Date']
                    # datestring = "2008-12-12 19:21:10" %Y-%m-%d %H:%M:%S
                    alb = datetime.strptime(album['meta']['Released Date'], '%d/%m/%Y')
                    # print alb.year, alb.month, alb.day
                    album_year = alb.year

                tracks = re.findall('<div.*?id="GridTracks".*?>.*?<table.*?>.*?<tbody.*?>(<tr.*?>.*?</tr>)</tbody>.*?</table>.*?</div>', data)
                tracks = re.findall('<tr.*?>.*?</tr>', tracks[0])

                if 'track' not in album:
                    album['track']={}

                for h in tracks:
                    track_id,track_title = re.findall('<div id=(\d+)><span.*?>(.*?)</span>', h)[0]
                    track_artist = re.findall('<span.*?><a.*?>(.*?)</a>', h)
                    track_artist = list(map(lambda x: x.strip(), track_artist))
                    tks = {'title':track_title,'artist':track_artist}
                    if album_info_save_audio:
                        if track_id not in album['track'] or 'local' not in album['track'][track_id] or not album['track'][track_id]['local']:
                            if self.album_audio_save(album_id,track_id):
                                mp3 = id3Parser.mp3()
                                mp3.load(self.album_audio_save_filename)
                                mp3.title(track_title)
                                mp3.artist(track_artist)
                                mp3.album_artist(list(album_artist.values()))
                                mp3.album(album_name)
                                if album_year:
                                    mp3.year(album_year)
                                mp3.cover(self.album_cover_save_filename)
                                mp3.save()
                                tks['local']=True
                            else:
                                tks['local']=False
                            print('+--{}-{} {}'.format(track_id, track_title,self.error_msg))
                        else:
                            print('---{}-{}'.format(track_id, track_title))
                            tks['local']=True
                    album['track'][track_id]=tks
                if album_info_save_audio:
                    self.json_save(self.album_location_json.format(album_id),album)
                    print('album-{}-{}'.format(album_id, album_name))
                else:
                    print('[Ok]',album_id, album_name)
                return album
            elif lang == 'mm':
                print('...trying:{} in en'.format(album_id))
                self.album_info('en',album_id,album_info_save_audio)
            else:
                # NOTE: No album found
                print('...no {}:{} found!'.format('Album',album_id))
        elif lang == 'mm':
            print('...trying:{} in en'.format(album_id))
            self.album_info('en',album_id,album_info_save_audio)
        elif self.error_msg:
            print('[??]',self.error_msg)
        else:
            print('[Error]',album_id)

    def album_cover_save(self,album,track):
        url = 'https://www.{}.{}{}'.format(self.domain_name,self.domain_extension,track)
        self.album_cover_save_filename=False
        response = self.load(url)
        if response:
            extension = os.path.splitext(url)[1]
            data = response.read()
            filename = self.album_location_cover.format(album,extension)
            directory = os.path.dirname(filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(filename, "wb") as file:
                self.album_cover_save_filename = filename
                file.write(data)

    def album_audio_save(self,album,track):
        url = 'https://www.{}.{}/track/ProcessNTrack/{}'.format(self.domain_name,self.domain_extension,track)
        self.album_audio_save_filename=False
        self.error_msg =''
        response = self.load(url)
        if response:
            data = response.read()
            filename = self.album_location_audio.format(album,track)
            directory = os.path.dirname(filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(filename, "wb") as file:
                file.write(data)
                self.album_audio_save_filename = filename
                return True
        elif self.error_msg:
            pass
            # print(self.error_msg)

    def album_id_collect(self):
        filename_ids = 'album-ids.json'
        filename_lists = 'album-list.{}.v181110.json'
        try:
            self.album_ids = self.json_load(filename_ids)
        except Exception as e:
            self.album_ids = {}

        # self.album_list_scan_by_artist=12
        # self.album_list_scan_audio_save=True
        # self.album_lists={}
        # self.album_list_scan('mm','S',1,100)
        # self.json_save(filename_lists.format('S'),self.album_lists)
        #
        # self.album_list_scan_audio_save=True
        # self.album_lists={}
        # self.album_list_scan('mm','C',1,100)
        # self.json_save(filename_lists.format('C'),self.album_lists)

        # self.album_list_scan_audio_save=True
        # self.album_lists={}
        # self.album_list_scan('mm','V',1,100)
        # self.json_save(filename_lists.format('V'),self.album_lists)

        # self.json_save(filename_ids,self.album_ids)

    def artist_id_collect(self):
        filename_ids = 'artist-ids.json'
        filename_lists = 'artist-list.{}.v181110.json'
        try:
            self.artist_ids = self.json_load(filename_ids)
        except Exception as e:
            self.artist_ids = {}

        # self.artist_lists={}
        # self.artist_list_scan('mm','M',1,100)
        # self.json_save(filename_lists.format('M'),self.artist_lists)
        #
        # self.artist_lists={}
        # self.artist_list_scan('mm','F',1,100)
        # self.json_save(filename_lists.format('F'),self.artist_lists)
        #
        # self.artist_lists={}
        # self.artist_list_scan('mm','G',1,100)
        # self.json_save(filename_lists.format('G'),self.artist_lists)

        self.json_save(filename_ids,self.artist_ids)

    def queries(self):
        query = {
            'type':'',
            'from':'',
            'to':'',
            'audio':False,
            'log-list':'album-list.{}.181114.json',
            'log-id':'album-ids.json'
        }
        for pair in sys.argv:
            try:
                key, value = pair.split('=')
                query[key] = value
            except Exception as e:
                pass
        return query

    def tmp(self):
        pass

if __name__=="__main__":
    pass
    # test=result('3pmramnaym','ten')
    # query = test.queries()
    # from=1 to=last type=scv
    # audio=yes album=3
    # audio=yes from=1 to=last type=scv artist=3

    # test.album_list_scan_audio_save=query['audio'] and True
    # query_from = query['from'].isnumeric() and int(query['from']) > 0 and query['from']
    # query_to = query['to']
    #
    # if 'album' in query and query['album'].isnumeric() and int(query['album']) > 0:
    #     test.album_info('mm',query['album'],True)
    # else:
    #     if 'artist' in query and query['artist'].isnumeric() and int(query['artist']) > 0:
    #         test.album_list_scan_by_artist=query['artist']
    #
    #     if query['log-id']:
    #         try:
    #             test.album_ids = test.json_load(query['log-id'])
    #         except Exception as e:
    #             test.album_ids = {}
    #
    #     for item_type in set(query['type']):
    #         if query_from and item_type in 'scv':
    #             test.album_lists={}
    #             test.album_list_scan('mm',item_type.upper(),query_from,query_to)
    #             if query['log-list']:
    #                 if test.album_lists:
    #                     test.json_save(query['log-list'].format(item_type),test.album_lists)
    #                 # if test.artist_lists:
    #                 #     test.json_save(query['log-list'].format(item_type),test.artist_lists)
    #
    #     if query['log-id']:
    #         test.json_save(query['log-id'],test.album_ids)
