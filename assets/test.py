import re
keyword = "love genre=Loves quality=3D rating=2.5"
# keyword = "love genre=Loves"
# keyword = "love genre=Loves as"
genre=''
quality=''
rating=''


# Simple search
# just type -> Movie Title/IMDb Code, Actor Name/IMDb Code, Director Name/IMDb Code
# Advanced search
# love genre=? quality=? minimum_rating=? sort_by=? order_by=? with_rt_ratings=? page=? limit=?


# genre = re.findall("(genre=.*\s+)", xx)
# genre = re.findall("(genre=\.*)", xx) -> genre=
# genre = re.findall(r"genre=\w+[\s+|$]?", xx) -> working

# query_term, genre, quality, minimum_rating, sort_by, order_by, with_rt_ratings, page, limit
param_url = {}

genreRegex = "(genre=\w+[\s+|$]?)"
genre = re.findall(genreRegex, keyword)
if len(genre):
    keyword = re.sub(genreRegex,"",keyword)
    param_url['genre'] = re.findall("=(.*)", genre[0])[0].strip()

qualityRegex = "(quality=\w+[\s+|$]?)"
quality = re.findall(qualityRegex, keyword)
if len(quality):
    keyword = re.sub(qualityRegex,"",keyword)
    param_url['quality'] = re.findall("=(.*)", quality[0])[0].strip()

minimum_ratingRegex = "(rating=.*[\s+|$]?)"
minimum_rating = re.findall(minimum_ratingRegex, keyword)
if len(minimum_rating):
    keyword = re.sub(minimum_ratingRegex,"",keyword)
    param_url['minimum_rating'] = re.findall("=(.*)", minimum_rating[0])[0].strip()

sortRegex = "(sort_by=.*[\s+|$]?)"
sort_by = re.findall(sortRegex, keyword)
if len(sort_by):
    keyword = re.sub(sortRegex,"",keyword)
    param_url['sort_by'] = re.findall("=(.*)", sort_by[0])[0].strip()

orderRegex = "(order_by=.*[\s+|$]?)"
order_by = re.findall(orderRegex, keyword)
if len(order_by):
    keyword = re.sub(orderRegex,"",keyword)
    param_url['order_by'] = re.findall("=(.*)", order_by[0])[0].strip()

with_rt_ratingsRegex = "(with_rt_ratings=.*[\s+|$]?)"
with_rt_ratings = re.findall(with_rt_ratingsRegex, keyword)
if len(order_by):
    keyword = re.sub(with_rt_ratingsRegex,"",keyword)
    param_url['with_rt_ratings'] = re.findall("=(.*)", with_rt_ratings[0])[0].strip()

pageRegex = "(with_rt_ratings=.*[\s+|$]?)"
page = re.findall(pageRegex, keyword)
if len(page):
    keyword = re.sub(pageRegex,"",keyword)
    param_url['page'] = re.findall("=(.*)", page[0])[0].strip()

limitRegex = "(with_rt_ratings=.*[\s+|$]?)"
limit = re.findall(limitRegex, keyword)
if len(limit):
    keyword = re.sub(limitRegex,"",keyword)
    param_url['limit'] = re.findall("=(.*)", limit[0])[0].strip()


query_term = re.sub(' +',' ',keyword).strip()
if query_term:
    param_url['query_term'] = query_term

print(param_url)
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
