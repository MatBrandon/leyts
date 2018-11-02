# VERSION: 1.0
# AUTHORS: Khen Solomon Lethil (khensolomon@gmail.com)
# CONTRIBUTORS: ??

# Simple search
# just type -> Movie Title/IMDb Code, Actor Name/IMDb Code, Director Name/IMDb Code
# Advanced search
# love genre=? quality=? minimum_rating=? sort_by=? order_by=? with_rt_ratings=? page=? limit=?



import json
import time
import re
try:
    # python3
    from urllib.parse import urlencode, unquote
except ImportError:
    # python2
    from urllib import urlencode, unquote

# qBt
from novaprinter import prettyPrinter
from helpers import retrieve_url

class yts(object):
    url = 'https://yts.am'
    name = 'YTS'
    supported_categories = {'all': ''}

    def search(self, keyword, cat='all'):
        base_url = "https://yts.am/api/v2/list_movies.json?%s"
        parameter = {}
        keyword = unquote(keyword)

        genreRegex = "(genre=\w+[\s+|$]?)"
        genre = re.findall(genreRegex, keyword)
        if len(genre):
            keyword = re.sub(genreRegex,"",keyword)
            parameter['genre'] = re.findall("=(.*)", genre[0])[0].strip()

        qualityRegex = "(quality=\w+[\s+|$]?)"
        quality = re.findall(qualityRegex, keyword)
        if len(quality):
            keyword = re.sub(qualityRegex,"",keyword)
            parameter['quality'] = re.findall("=(.*)", quality[0])[0].strip()

        minimum_ratingRegex = "(rating=.*[\s+|$]?)"
        minimum_rating = re.findall(minimum_ratingRegex, keyword)
        if len(minimum_rating):
            keyword = re.sub(minimum_ratingRegex,"",keyword)
            parameter['minimum_rating'] = re.findall("=(.*)", minimum_rating[0])[0].strip()

        sortRegex = "(sort_by=.*[\s+|$]?)"
        sort_by = re.findall(sortRegex, keyword)
        if len(sort_by):
            keyword = re.sub(sortRegex,"",keyword)
            parameter['sort_by'] = re.findall("=(.*)", sort_by[0])[0].strip()

        orderRegex = "(order_by=.*[\s+|$]?)"
        order_by = re.findall(orderRegex, keyword)
        if len(order_by):
            keyword = re.sub(orderRegex,"",keyword)
            parameter['order_by'] = re.findall("=(.*)", order_by[0])[0].strip()

        with_rt_ratingsRegex = "(with_rt_ratings=.*[\s+|$]?)"
        with_rt_ratings = re.findall(with_rt_ratingsRegex, keyword)
        if len(order_by):
            keyword = re.sub(with_rt_ratingsRegex,"",keyword)
            parameter['with_rt_ratings'] = re.findall("=(.*)", with_rt_ratings[0])[0].strip()

        pageRegex = "(with_rt_ratings=.*[\s+|$]?)"
        page = re.findall(pageRegex, keyword)
        if len(page):
            keyword = re.sub(pageRegex,"",keyword)
            parameter['page'] = re.findall("=(.*)", page[0])[0].strip()

        limitRegex = "(with_rt_ratings=.*[\s+|$]?)"
        limit = re.findall(limitRegex, keyword)
        if len(limit):
            keyword = re.sub(limitRegex,"",keyword)
            parameter['limit'] = re.findall("=(.*)", limit[0])[0].strip()

        query_term = re.sub(' +',' ',keyword).strip()
        if query_term:
            parameter['query_term'] = query_term

        # get response json
        # query_term, genre, quality, minimum_rating, sort_ty, order_by, with_rt_ratings, page, limit
        # keyword = unquote(keyword)
        # category_genre = self.supported_categories[cat]
        # params = urlencode({'query_term': keyword})
        response = retrieve_url(base_url % urlencode(parameter))
        j = json.loads(response)

        # parse results
        tr_tracker = ['udp://open.demonii.com:1337/announce',
                    'udp://tracker.openbittorrent.com:80',
                    'udp://tracker.coppersurfer.tk:6969',
                    'udp://glotorrents.pw:6969/announce',
                    'udp://tracker.opentrackr.org:1337/announce',
                    'udp://torrent.gresille.org:80/announce',
                    'udp://p4p.arenabg.com:1337',
                    'udp://tracker.leechers-paradise.org:6969']

        magnet = "magnet:?xt=urn:btih:{Hashs}&{Downloads}&tr={Trackers}"

        for movies in j['data']['movies']:
            for torrent in movies['torrents']:
                res = {'link': magnet.format(Hashs=torrent['hash'], Downloads=urlencode({'dn': movies['title']}), Trackers='&tr='.join(tr_tracker)),
                       'name': '{n} ({y}) [{q}]'.format(n=movies['title'], y=movies['year'], q=torrent['quality']),
                       'size': torrent['size'],
                       'seeds': torrent['seeds'],
                       'leech': torrent['peers'],
                       'engine_url': 'IMDB:[{rating}], Genre:[{genres}]'.format(rating=movies['rating'], genres=', '.join(movies['genres'])),
                       # 'engine_url': self.url,
                       'desc_link': movies['url']}
                prettyPrinter(res)
