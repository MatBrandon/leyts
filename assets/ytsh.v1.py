# VERSION: 1.0
# AUTHORS: Khen Solomon Lethil (khensolomon@gmail.com)

import json
import time
import re
try:
    # python3
    from urllib.parse import urlencode, unquote, quote_plus
    from html.parser import HTMLParser
except ImportError:
    # python2
    from HTMLParser import HTMLParser
    from urllib import urlencode, unquote, quote_plus

# local
from novaprinter import prettyPrinter
from helpers import retrieve_url
#
# import re
# # dev
# from novaprinter import prettyPrinter
# from helpers import retrieve_url, download_file
# qBt
# from novaprinter import prettyPrinter
# from bs4 import BeautifulSoup
# from helpers import retrieve_url, download_file

# try:
#     from HTMLParser import HTMLParser
# except ImportError:
#     from html.parser import HTMLParser

# from bs4 import BeautifulSoup

class yts(object):
    url = 'https://yts.am'
    name = 'YTS'
    supported_categories = {'all': 'All', 'movies': 'Movie'}

    def search(self, keyword, cat='all'):
        # base_url = "https://yts.am/api/v2/list_movies.json?%s"
        base_url = self.url+"/browse-movies/{query_term}/{quality}/{genre}/{minimum_rating}/{order_by}"
        parameter = {
            'query_term':'0',
            'quality':'0',
            'genre':'0',
            'minimum_rating':'0',
            'order_by':'0'}

        keyword = unquote(keyword)

        genreRegex = "(genre=\w+[\s+|$]?)"
        genre = re.findall(genreRegex, keyword)
        if len(genre):
            keyword = re.sub(genreRegex,"",keyword)
            parameter['genre'] = re.findall("=(.*)", genre[0])[0].strip()

        quality_regex = "(quality=\w+[\s+|$]?)"
        quality = re.findall(quality_regex, keyword)
        if len(quality):
            keyword = re.sub(quality_regex,"",keyword)
            parameter['quality'] = re.findall("=(.*)", quality[0])[0].strip()

        minimum_rating_regex = "(minimum_rating=?[0-9]*[.]?[0-9]+[\s+|$]?)"
        minimum_rating = re.findall(minimum_rating_regex, keyword)
        if len(minimum_rating):
            keyword = re.sub(minimum_rating_regex,"",keyword)
            parameter['minimum_rating'] = re.findall("=(.*)", minimum_rating[0])[0].strip()

        sort_by_regex = "(sort_by=\w+[\s+|$]?)"
        sort_by = re.findall(sort_by_regex, keyword)
        if len(sort_by):
            keyword = re.sub(sort_by_regex,"",keyword)
            parameter['sort_by'] = re.findall("=(.*)", sort_by[0])[0].strip()

        order_by_regex = "(order_by=\w+[\s+|$]?)"
        order_by = re.findall(order_by_regex, keyword)
        if len(order_by):
            keyword = re.sub(order_by_regex,"",keyword)
            parameter['order_by'] = re.findall("=(.*)", order_by[0])[0].strip()

        with_rt_ratings_regex = "(with_rt_ratings=\w+[\s+|$]?)"
        with_rt_ratings = re.findall(with_rt_ratings_regex, keyword)
        if len(with_rt_ratings):
            keyword = re.sub(with_rt_ratings_regex,"",keyword)
            parameter['with_rt_ratings'] = re.findall("=(.*)", with_rt_ratings[0])[0].strip()

        page_regex = "(page=\w+[\s+|$]?)"
        page = re.findall(page_regex, keyword)
        if len(page):
            keyword = re.sub(page_regex,"",keyword)
            parameter['page'] = re.findall("=(.*)", page[0])[0].strip()

        limit_regex = "(limit=.*[\s+|$]?)"
        limit = re.findall(limit_regex, keyword)
        if len(limit):
            keyword = re.sub(limit_regex,"",keyword)
            parameter['limit'] = re.findall("=(.*)", limit[0])[0].strip()

        query_term = re.sub(' +',' ',keyword).strip()
        if query_term:
            if query_term !='%%':
                parameter['query_term'] = query_term


        search_url = base_url.format(query_term=parameter['query_term'],
                                    quality=parameter['quality'],
                                    genre=parameter['genre'],
                                    minimum_rating=parameter['minimum_rating'],
                                    order_by=parameter['order_by'])
        # response = retrieve_url('https://yts.am/browse-movies/')
        response_html = retrieve_url(search_url)
        # response = retrieve_url(search_url % urlencode(parameter))
                # what = what.replace('%2B', '+')
                # https://yts.am/browse-movies/0/720p/adventure/8/seeds
                # https://yts.am/browse-movies/0/0/0/0/0

        # response_html = retrieve_url('https://yts.am/movie/dark-money-2018')
        # response_html = retrieve_url('https://yts.am/browse-movies/0/0/0/0/0')
        # print(response_html)
        # print(search_url)

        # response_html ='<div>first</div><div>\
        # <div class="container">\
        #     <h2>9,234 YIFY Movies Found</h2>\
        #     <div class="hidden-sm hidden-xs">\
        #         <ul class="tsc_pagination tsc_paginationA tsc_paginationA06">\
        #             <li>page 1</li>\
        #         </ul>\
        #     </div>\
        #     <div class="hidden-sm hidden-lg">\
        #         none\
        #     </div>\
        #     <section>\
        #         <div class="row">\
        #             <div class="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4">\
        #                 <a href="link1" class="browse-movie-link">\
        #                     <figure>\
        #                       <img class="img-responsive" src="" alt="" width="170" height="255">\
        #                       <figcaption class="hidden-xs hidden-sm">\
        #                         <span class="icon-star"></span>\
        #                         <h4 class="rating">8.2 / 10</h4>\
        #                         <h4>Comedy</h4>\
        #                         <h4>Adventure</h4>\
        #                         <span class="button-green-download2-big">View Details</span>\
        #                       </figcaption>\
        #                     </figure>\
        #                 </a>\
        #                 <div class="browse-movie-bottom">\
        #                     <a href="one" class="browse-movie-title">Little Man</a>\
        #                     <div class="browse-movie-year">2014</div>\
        #                     <div class="browse-movie-tags">\
        #                       <a href="https://yts.am/torrent/download/a" rel="nofollow" title="Download Avengers: Infinity War 3D Torrent">first</a>\
        #                       <a href="https://yts.am/torrent/download/b" rel="nofollow" title="Download Avengers: Infinity War 720p Torrent">720p</a>\
        #                       <a href="https://yts.am/torrent/download/c" rel="nofollow" title="Download Avengers: Infinity War 1080p Torrent">1080p</a>\
        #                     </div>\
        #                 </div>\
        #             </div>\
        #             <div class="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4">\
        #                 <a href="link2" class="browse-movie-link">\
        #                     <figure>\
        #                       <img class="img-responsive" src="" alt="" width="170" height="255">\
        #                       <figcaption class="hidden-xs hidden-sm">\
        #                         <span class="icon-star"></span>\
        #                         <h4 class="rating">8.6 / 10</h4>\
        #                         <h4>Action</h4>\
        #                         <h4>Adventure</h4>\
        #                         <span class="button-green-download2-big">View Details</span>\
        #                       </figcaption>\
        #                     </figure>\
        #                 </a>\
        #                 <div class="browse-movie-bottom">\
        #                     <a href="one" class="browse-movie-title">Little Boy</a>\
        #                     <div class="browse-movie-year">2015</div>\
        #                     <div class="browse-movie-tags">\
        #                       <a href="https://yts.am/torrent/download/d" rel="nofollow" title="Download Avengers: Infinity War 3D Torrent">3D</a>\
        #                       <a href="https://yts.am/torrent/download/e" rel="nofollow" title="Download Avengers: Infinity War 720p Torrent">720p</a>\
        #                       <a href="https://yts.am/torrent/download/f" rel="nofollow" title="Download Avengers: Infinity War 1080p Torrent">last</a>\
        #                     </div>\
        #                 </div>\
        #             </div>\
        #         </div>\
        #     </section>\
        # </div>\
        # </div><div>last</div>'

        tr_tracker = ['udp://open.demonii.com:1337/announce',
                    'udp://tracker.openbittorrent.com:80',
                    'udp://tracker.coppersurfer.tk:6969',
                    'udp://glotorrents.pw:6969/announce',
                    'udp://tracker.opentrackr.org:1337/announce',
                    'udp://torrent.gresille.org:80/announce',
                    'udp://p4p.arenabg.com:1337',
                    'udp://tracker.leechers-paradise.org:6969']

        magnet = "magnet:?xt=urn:btih:{Hashs}&{Downloads}&{Trackers}"

        response_html = re.sub("\s\s+", "", response_html)
        response_html = response_html.replace('\n', '').replace('\r', '')
        # response_container = re.findall('<div class="browse-content"><div class="container">.*</div></div>', response_html)
        response_container = re.findall('<div class="browse-content"><div class="container">.*?<section><div class="row">(.*?)</div></section>.*?</div></div>', response_html)
        # response_section_row = re.findall('<section><div class="row">.*?</div></section>', response_container[0])
        # print(response_container)
        # print(len(response_container))
        # response_section_row_movie = re.findall('<div class=".?browse-movie-wrap.*?">.*?</div>.*?</div></div>', response_section_row)
        response_section_row_movie = re.findall('<div class=".?browse-movie-wrap.*?">.*?</div></div></div>', response_container[0])
        # print(response_section_row_movie)
        # print(len(response_section_row_movie))



        for hM in response_section_row_movie:
            movie_link = re.findall('<a href="(.*?)" class="browse-movie-link">.*?</a>', hM)[0]
            # main-content container row movie-info
            response_detail = retrieve_url(movie_link)
            response_detail = re.sub("\s\s+", "", response_detail).replace('\n', '').replace('\r', '')

            movie_id = re.findall('data-movie-id="(\d+)"', response_detail)[0]
            if movie_id:
                api_detail = retrieve_url('https://yts.am/api/v2/movie_details.json?movie_id='+movie_id)
                j = json.loads(api_detail)
                movies = j['data']['movie']
                for torrent in movies['torrents']:
                    res = {'link': magnet.format(Hashs=torrent['hash'],
                                                Downloads=urlencode({'dn': movies['title']}),
                                                Trackers='&'.join(map(lambda x: 'tr='+quote_plus(x.strip()), tr_tracker))),
                           'name': '{n} ({y}) [{q}]-[{i}]'.format(n=movies['title'], y=movies['year'], q=torrent['quality'], i=self.name),
                           'size': torrent['size'],
                           'seeds': torrent['seeds'],
                           'leech': torrent['peers'],
                           'engine_url': 'IMDB:[{rating}], Genre:[{genres}]'.format(rating=movies['rating'], genres=', '.join(movies['genres'])),
                           # 'engine_url': self.url,
                           'desc_link': movies['url']}
                    # prettyPrinter(res)
                    print(res)
            else:
                print('nothing')
                movie_title = re.findall('<a.*?class="browse-movie-title".*?>(.*?)</a>', hM)[0]
                movie_year = re.findall('<div.?class="browse-movie-year".*?>(.*?)</div>', hM)[0]

                movie_rate = re.findall('<h4.?class="rating".*?>(.*?)</h4>', hM)[0]
                movie_rate = movie_rate.split('/')[0]

                movie_genre = re.findall('<figcaption class=".*?">.*?(<h4>.*</h4>).*?</figcaption>', hM)[0]
                movie_genre = re.findall('<h4>(.*?)</h4>', movie_genre)

                # print(movie_title,movie_link,movie_year,movie_rate,movie_genre)

            # movie_torrent = re.findall('<div class="modal-torrent">.*?</div>.*?</div>', response_detail)
            # print(len(movie_torrent))
            # print(movie_torrent)
            # for torrent in movie_torrent:
            #     torrent_size = re.findall('<p class="quality-size">(.*?)</p>', torrent)
            #     movie_type = torrent_size[0] #BluRay
            #     movie_size = torrent_size[1] # 1.69 GB
            #     movie_quality = re.findall('<div.*?><span>(.*?)</span></div>', torrent)[0] #1080p
            #     torrent_hash = re.findall('href="https://yts.am/torrent/download/(.*?)"', torrent)[0]
            #     torrent_magnet = re.findall('href="magnet:?(.*?)"', torrent)
            #     # print(movie_type,movie_size,movie_quality,torrent_hash)
            #     res = {'link': magnet.format(Hashs=hash,
            #                                 Downloads=urlencode({'dn': movie_title}),
            #                                 Trackers='&'.join(map(lambda x: 'tr='+quote_plus(x.strip()), tr_tracker))),
            #            'name': '{n} ({y}) [{q}]-[{i}]'.format(n=movie_title, y=movie_year, q=quality, i='tmp'),
            #            'size': quality,
            #            'seeds': 'unknown',
            #            'leech': 'unknown',
            #            'engine_url': 'IMDB:[{rating}], Genre:[{genres}]'.format(rating=movie_rate, genres=', '.join(movie_genre)),
            #            # 'engine_url': self.url,
            #            'desc_link': movie_link}
            #     # prettyPrinter(res)
            #     print(res)

            # movie_torrent = re.findall('<div class="browse-movie-tags">.*?(<a.*?href=".*?".*?>.*?</a>).*?</div>', hM)
            # print(movie_title,movie_torrent)
            # movie_torrent = re.findall('<a href=".*?".*?>.*?</a>', movie_torrent[0])
            # for torrent in movie_torrent:
            #     torrent_object={};
            #     torrent_hash = re.findall('<a href=".*?torrent/download/(.*?)".*?>(.*?)</a>', torrent)[0]
            #     if torrent_hash:
            #         hash = torrent_hash[0]
            #         quality = torrent_hash[1]
            #         res = {'link': magnet.format(Hashs=hash,
            #                                     Downloads=urlencode({'dn': movie_title}),
            #                                     Trackers='&'.join(map(lambda x: 'tr='+quote_plus(x.strip()), tr_tracker))),
            #                'name': '{n} ({y}) [{q}]-[{i}]'.format(n=movie_title, y=movie_year, q=quality, i='tmp'),
            #                'size': quality,
            #                'seeds': 'unknown',
            #                'leech': 'unknown',
            #                'engine_url': 'IMDB:[{rating}], Genre:[{genres}]'.format(rating=movie_rate, genres=', '.join(movie_genre)),
            #                # 'engine_url': self.url,
            #                'desc_link': movie_link}
            #         # prettyPrinter(res)
            #         print(res)

if __name__=="__main__":
    yts.search(yts,'Shekhar Kapur')