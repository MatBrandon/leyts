# VERSION: 3.0
# AUTHORS: Khen Solomon Lethil (khensolomon@gmail.com)
# CONTRIBUTORS: ??

import json
import time
import re
try:
    # python3
    from urllib.parse import urlencode, unquote, quote_plus
except ImportError:
    # python2
    from urllib import urlencode, unquote, quote_plus

# qBt
from novaprinter import prettyPrinter
from helpers import retrieve_url

class yts(object):
    url = 'https://yts.am'
    name = 'YTS'
    supported_categories = {'all': 'All', 'movies': 'Movie'}

    def search(self, keyword, cat='all'):
        base_url = "https://yts.am/api/v2/list_movies.json?%s"
        parameter = {}
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
            parameter['query_term'] = query_term

        # get response json
        # query_term, genre, quality, minimum_rating, sort_ty, order_by, with_rt_ratings, page, limit
        # keyword = unquote(keyword)
        # category_genre = self.supported_categories[cat]
        # parameter = urlencode({'query_term': keyword})
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

        magnet = "magnet:?xt=urn:btih:{Hashs}&{Downloads}&{Trackers}"

        for movies in j['data']['movies']:
            for torrent in movies['torrents']:
                res = {'link': magnet.format(Hashs=torrent['hash'],
                                            Downloads=urlencode({'dn': movies['title']}),
                                            Trackers='&'.join(map(lambda x: 'tr='+quote_plus(x.strip()), tr_tracker))),
                       'name': '{n} ({y}) [{q}]'.format(n=movies['title'], y=movies['year'], q=torrent['quality']),
                       'size': torrent['size'],
                       'seeds': torrent['seeds'],
                       'leech': torrent['peers'],
                       'engine_url': 'IMDB:[{rating}], Genre:[{genres}]'.format(rating=movies['rating'], genres=', '.join(movies['genres'])),
                       # 'engine_url': self.url,
                       'desc_link': movies['url']}
                prettyPrinter(res)
