# VERSION: 1.0
# AUTHORS: Khen Solomon Lethil (khensolomon@gmail.com)
# CONTRIBUTORS: ??

# LICENSING INFORMATION
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import json
import time
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
        # get response json
        # query_term, genre, quality, minimum_rating, sort_ty, order_by, with_rt_ratings, page, limit
        keyword = unquote(keyword)
        category_genre = self.supported_categories[cat]
        params = urlencode({'query_term': keyword})
        response = retrieve_url(base_url % params)
        j = json.loads(response)

        # TODO: advanced query -> genre=Action page=1
        48105688
        # 'love genre=love '.search(r"<title>(.*)</title>", s, re.IGNORECASE)
        'love genre=love '.search(r"genre=(.*) ", s, re.IGNORECASE)
import re
q = 'love genre=love ':
r1 = re.findall(genre="^\w+",q)
print(r1)
p= re.match("genre=(.*) ", 'love genre=love ')

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
