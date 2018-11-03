# leyts

## qBittorrent -> search plugin

# How do I install?
Insert this url in `Searh plugins` -> `install a new one` -> `web link`

```
https://raw.githubusercontent.com/khensolomon/leyts/master/yts.py
```

# How do I search?

```shell
# just type -> Movie Title/IMDb Code, Actor Name/IMDb Code, Director Name/IMDb Code
```
> or a little bit advanced

```shell
#love genre=? quality=? minimum_rating=? sort_by=? order_by=? with_rt_ratings=? page=? limit=?
love genre=Action quality=1080p minimum_rating=2.0 sort_by=a order_by=b with_rt_ratings=0 page=1 limit=30
```

> extract the Latest

```
%%
```

> Parameter	Required	Type	Default	Description

```json
{
  "limit": "Integer between 1 - 50 (inclusive)	20 The limit of results per page that has been set",
  "page": "Integer (Unsigned)	1	Used to see the next page of movies, eg limit=15 and page=2 will show you movies 15-30",
  "quality": "String (720p, 1080p, 3D)	All	Used to filter by a given quality",
  "minimum_rating": "Integer between 0 - 9 (inclusive)	0	Used to filter movie by a given minimum IMDb rating",
  "query_term": "String	0	Used for movie search, matching on: Movie Title/IMDb Code, Actor Name/IMDb Code, Director Name/IMDb Code",
  "genre": "String	All	Used to filter by a given genre (See http://www.imdb.com/genre/ for full list)",
  "sort_by": "String (title, year, rating, peers, seeds, download_count, like_count, date_added)	date_added	Sorts the results by choosen value",
  "order_by": "String (desc, asc)	desc	Orders the results by either Ascending or Descending order",
  "with_rt_ratings": "Boolean	false	Returns the list with the Rotten Tomatoes rating included"
}
```