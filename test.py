
import json
import time
import re
try:
    # python3
    from urllib.parse import urlencode, unquote, quote_plus
except ImportError:
    # python2
    from urllib import urlencode, unquote, quote_plus

# keyword = "love genre=Action quality=1080p minimum_rating=2.0 sort_by=a order_by=b with_rt_ratings=0 page=1 limit=30"
keyword = "love   genre=Action quality=1080p minimum_rating=2.0"
# keyword = "love genre=Loves"
# keyword = "love genre=Loves as"





# genre = re.findall("(genre=.*\s+)", xx)
# genre = re.findall("(genre=\.*)", xx) -> genre=
# genre = re.findall(r"genre=\w+[\s+|$]?", xx) -> working

# query_term, genre, quality, minimum_rating, sort_by, order_by, with_rt_ratings, page, limit
parameter = {}

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

print(parameter)

abc = map(lambda x: 'tr='+quote_plus(x.strip()), tr_tracker)



# quality = re.findall("(quality=\w+)", xx)
# quality = re.findall("(quality=.*[$\s?+])", xx)
# rating = re.findall("(rating=.*\s*$)", xx)
# print(genre,quality,rating)

# re.sub(' +',' ',keyword).strip()
# print("-"+re.sub(' +',' ',keyword).strip()+"-")


# genre = re.findall(r"genre=\w+[\s+|$]?", keyword)
# if len(genre):
#     # print(genre)
#     keyword = re.sub(r"genre=\w+[\s+|$]?","",keyword)
# else:
#     print ('none')
#
# quality = re.findall(r"quality=\w+[\s+|$]?", keyword)
# if len(quality):
#     keyword = re.sub(r"quality=\w+[\s+|$]?","",keyword)
# else:
#     print ('none')
#
# rating = re.findall(r"rating=\w+[\s+|$]?", keyword)
# if len(rating):
#     keyword = re.sub(r"rating=\w+[\s+|$]?","",keyword)
# else:
#     print ('none')
