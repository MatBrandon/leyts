# VERSION: 3.3
# AUTHORS: Khen Solomon Lethil (khensolomon@gmail.com)
import json
import time
import re
import math
try:
    # python3
    from urllib.parse import urlencode, unquote, quote_plus
    from html.parser import HTMLParser
except ImportError:
    # python2
    from urllib import urlencode, unquote, quote_plus
    from HTMLParser import HTMLParser

# local
from novaprinter import prettyPrinter
from helpers import retrieve_url

class yts(object):
    url = 'https://yts.am'
    name = 'YTS'
    supported_categories = {'all': 'All', 'movies': 'Movie'}

    def search(self, keyword, cat='all'):
        params = {}
        keyword = unquote(keyword)

        genre_regex = "(genre=\w+[\s+|$]?)"
        genre_param = re.findall(genre_regex, keyword)
        if len(genre_param):
            keyword = re.sub(genre_regex,"",keyword)
            params['genre'] = re.findall("=(.*)", genre_param[0])[0].strip()

        quality_regex = "(quality=\w+[\s+|$]?)"
        quality_param  = re.findall(quality_regex, keyword)
        if len(quality_param):
            keyword = re.sub(quality_regex,"",keyword)
            params['quality'] = re.findall("=(.*)", quality_param[0])[0].strip()

        minimum_rating_regex = "(minimum_rating=?[0-9]*[.]?[0-9]+[\s+|$]?)"
        minimum_rating_param = re.findall(minimum_rating_regex, keyword)
        if len(minimum_rating_param):
            keyword = re.sub(minimum_rating_regex,"",keyword)
            params['minimum_rating'] = re.findall("=(.*)", minimum_rating_param[0])[0].strip()

        sort_by_regex = "(sort_by=\w+[\s+|$]?)"
        sort_by_param = re.findall(sort_by_regex, keyword)
        if len(sort_by_param):
            keyword = re.sub(sort_by_regex,"",keyword)
            params['sort_by'] = re.findall("=(.*)", sort_by_param[0])[0].strip()

        order_by_regex = "(order_by=\w+[\s+|$]?)"
        order_by_param = re.findall(order_by_regex, keyword)
        if len(order_by_param):
            keyword = re.sub(order_by_regex,"",keyword)
            params['order_by'] = re.findall("=(.*)", order_by_param[0])[0].strip()

        with_rt_ratings_regex = "(with_rt_ratings=\w+[\s+|$]?)"
        with_rt_ratings_param = re.findall(with_rt_ratings_regex, keyword)
        if len(with_rt_ratings_param):
            keyword = re.sub(with_rt_ratings_regex,"",keyword)
            params['with_rt_ratings'] = re.findall("=(.*)", with_rt_ratings_param[0])[0].strip()

        page_regex = "(page=\w+[\s+|$]?)"
        page_param = re.findall(page_regex, keyword)
        if len(page_param):
            keyword = re.sub(page_regex,"",keyword)
            page_param = re.findall("=(.*)", page_param[0])[0].strip()
            if page_param > '1':
                params['page'] = page_param

        limit_regex = "(limit=.*[\s+|$]?)"
        limit_param = re.findall(limit_regex, keyword)
        if len(limit_param):
            keyword = re.sub(limit_regex,"",keyword)
            limit_param = re.findall("=(.*)", limit_param[0])[0].strip()
            if limit_param > '1':
                params['limit'] = limit_param

        query_term_param = re.sub(' +',' ',keyword).strip()
        if query_term_param:
            if query_term_param !='%%':
                params['query_term'] = query_term_param
                # params['query_term'] = quote_plus(query_term_param)

        url = scriptive.urlBuilder(self.url,['api', 'v2', 'list_movies.json'],params)
        data = retrieve_url(url)
        j = json.loads(data)
        if j['data']['movie_count']:
            result_page = str(j['data']['page_number'])+'of'+str(math.ceil(j['data']['movie_count'] / j['data']['limit']))
            for movies in j['data']['movies']:
                for torrent in movies['torrents']:
                    res = {'link':scriptive.magnetBuilder(torrent['hash'],movies['title']),
                           'name': '{n} ({y}) [{q}]-[{p}]-[{i}]'.format(n=movies['title'], y=movies['year'], q=torrent['quality'], p=result_page, i=self.name),
                           'size': torrent['size'],
                           'seeds': torrent['seeds'],
                           'leech': torrent['peers'],
                           'engine_url': 'IMDB:{rating}, [{genres}]'.format(rating=movies['rating'], genres=', '.join(movies['genres'])),
                           'desc_link': movies['url']}
                    scriptive.urlResponse(res)
        elif scriptive.supported_browse_movies:
            urlPath={'query_term':'0', 'quality':'all','genre':'all','minimum_rating':'0','sort_by':'latest'}
            for i in urlPath:
                if i in params:
                    urlPath[i]=params[i]
            urlPath = list(urlPath.values())
            urlPath.insert(0,scriptive.supported_browse_movies)

            url = scriptive.urlBuilder(self.url,urlPath,'page' in params and {'page':params['page']})
            data = retrieve_url(url)
            data = re.sub("\s\s+", "", data).replace('\n', '').replace('\r', '')

            data_container = re.findall('<div class="browse-content"><div class="container">.*?<section><div class="row">(.*?)</div></section>.*?</div></div>', data)
            result_page = re.findall('<li class="pagination-bordered">(.*?)</li>', data)[0] # 1 of 5
            result_page = result_page and re.sub(' +','',result_page).strip() or '?'

            data_movie = re.findall('<div class=".?browse-movie-wrap.*?">.*?</div></div></div>', data_container[0])
            for hM in data_movie:
                movie_link = re.findall('<a href="(.*?)" class="browse-movie-link">.*?</a>', hM)[0]
                response_detail = retrieve_url(movie_link)
                response_detail = re.sub("\s\s+", "", response_detail).replace('\n', '').replace('\r', '')
                movie_id = re.findall('data-movie-id="(\d+)"', response_detail)[0]
                if movie_id:
                    url = scriptive.urlBuilder(self.url,['api', 'v2', 'movie_details.json'],{'movie_id':movie_id})
                    data_detail = retrieve_url(url)
                    j = json.loads(data_detail)
                    movies = j['data']['movie']
                    for torrent in movies['torrents']:
                        res = {'link':scriptive.magnetBuilder(torrent['hash'],movies['title']),
                               'name': '{n} ({y}) [{q}]-[{p}]-[{i}]'.format(n=movies['title'], y=movies['year'], q=torrent['quality'], p=result_page,i=self.name[:-1]),
                               'size': torrent['size'],
                               'seeds': torrent['seeds'],
                               'leech': torrent['peers'],
                               'engine_url': 'IMDB:{rating}, [{genres}]'.format(rating=movies['rating'], genres=', '.join(movies['genres'])),
                               'desc_link': movies['url']}
                        scriptive.urlResponse(res)
                else:
                    movie_title = re.findall('<a.*?class="browse-movie-title".*?>(.*?)</a>', hM)[0]
                    movie_year = re.findall('<div.?class="browse-movie-year".*?>(.*?)</div>', hM)[0]

                    movie_rate = re.findall('<h4.?class="rating".*?>(.*?)</h4>', hM)[0]
                    movie_rate = movie_rate.split('/')[0]

                    movie_genre = re.findall('<figcaption class=".*?">.*?(<h4>.*</h4>).*?</figcaption>', hM)[0]
                    movie_genre = re.findall('<h4>(.*?)</h4>', movie_genre)
                    # print(movie_title,movie_link,movie_year,movie_rate,movie_genre)
                    scriptive.urlResponse()
        else:
            scriptive.urlResponse()

class scriptive(object):
    supported_browse_movies = 'browse-movies'

    def magnetBuilder(hash, name):
        tr_tracker = ['udp://open.demonii.com:1337/announce',
                    'udp://tracker.openbittorrent.com:80',
                    'udp://tracker.coppersurfer.tk:6969',
                    'udp://glotorrents.pw:6969/announce',
                    'udp://tracker.opentrackr.org:1337/announce',
                    'udp://torrent.gresille.org:80/announce',
                    'udp://p4p.arenabg.com:1337',
                    'udp://tracker.leechers-paradise.org:6969']
        return "magnet:?xt=urn:btih:{}&{}&{}".format(hash,urlencode({'dn': name}),'&'.join(map(lambda x: 'tr='+quote_plus(x.strip()), tr_tracker)))

    def urlBuilder(url, uri=[], param={}):
        for r in uri:
            url = '{}/{}'.format(url, r)
        if param:
            url = '{}?{}'.format(url, urlencode(param))
        return url

    def urlResponse(res={}):
        if res:
            # print(res['name'])
            prettyPrinter(res)
        else:
            print('none')

if __name__=="__main__":
    # Scarlett Johansson
    # yts.search(yts,'Mandy Patinkin page=1')
    yts.search(yts,'Shekhar Kapur')
    # yts.search(yts,'love page=5')
