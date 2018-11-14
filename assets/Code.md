```python
supported_browse_movies = 'browse-movies'
supported_browse_params = {'query_term':'0', 'quality':'all','genre':'all','minimum_rating':'0','sort_by':'latest'}
default_params = {
    'genre':{'x':'(term=\w+[\s+|$]?)'},
    'quality':{'x':'(term=\w+[\s+|$]?)'},
    'minimum_rating':{'x':'(term=?[0-9]*[.]?[0-9]+[\s+|$]?)'},
    'sort_by':{'x':'(term=\w+[\s+|$]?)'},
    'order_by':{'x':'(term=\w+[\s+|$]?)'},
    'with_rt_ratings':{'x':'(term=\w+[\s+|$]?)'},
    'page':{'x':'(term=\w+[\s+|$]?)','value':'1'},
    'limit':{'x':'(term=.*[\s+|$]?)','value':'1'},
    'query_term':{'x':'(term=.*[\s+|$]?)','value':'%%'}}

params={'page':'1','genre':'Action'}

# v3.5    
url_path=supported_browse_params
for i in url_path:
    if i in params:
        url_path[i]=params[i]
url_path = list(url_path.values())
url_path.insert(0,supported_browse_movies)

# v3.5.1
for i in filter(lambda y: y in params, url_path):
    url_path[i]=params[i]
url_path = list(url_path.values()).insert(0,supported_browse_movies)
url_path = url_path.values().insert(0,supported_browse_movies)

# v3.5.2
url_path = list(map(lambda i: i in params and params[i] or url_path[i], url_path))
```