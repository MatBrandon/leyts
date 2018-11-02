When you need it!
No common, but wide!
ignore but unforget

letytsy
leyts
https://yts.am/api/v2/list_movies.json
https://yts.am/api/v2/list_movies.jsonp
https://yts.am/api/v2/list_movies.xml
https://yts.am/rss/0/1080p/action/7
yts

limit		Integer between 1 - 50 (inclusive)	20	The limit of results per page that has been set
page		Integer (Unsigned)	1	Used to see the next page of movies, eg limit=15 and page=2 will show you movies 15-30
quality		String (720p, 1080p, 3D)	All	Used to filter by a given quality
minimum_rating		Integer between 0 - 9 (inclusive)	0	Used to filter movie by a given minimum IMDb rating
query_term		String	0	Used for movie search, matching on: Movie Title/IMDb Code, Actor Name/IMDb Code, Director Name/IMDb Code
genre		String	All	Used to filter by a given genre (See http://www.imdb.com/genre/ for full list)
sort_by		String (title, year, rating, peers, seeds, download_count, like_count, date_added)	date_added	Sorts the results by choosen value
order_by		String (desc, asc)	desc	Orders the results by either Ascending or Descending order
with_rt_ratings		Boolean	false	Returns the list with the Rotten Tomatoes rating included

'movies': 'Movie'


'all': 'All',
                          'action': 'Action',
                          'adventure': 'Adventure',
                          'animation': 'Animation',
                          'biography': 'Biography',
                          'comedy': 'Comedy',
                          'crime': 'Crime',
                          'documentary': 'Documentary',
                          'drama': 'Drama',
                          'family': 'Family',
                          'fantasy': 'Fantasy',
                          'film-noir': 'Film-Noir',
                          'game-show': 'Game-Show',
                          'history': 'History',
                          'horror': 'Horror',
                          'music': 'Music',
                          'musical': 'Musical',
                          'mystery': 'Mystery',
                          'news': 'News',
                          'reality-tv': 'Reality-TV',
                          'romance': 'Romance',
                          'sci-fi': 'Sci-Fi',
                          'sport': 'Sport',
                          'talk-show': 'Talk-Show',
                          'thriller': 'Thriller',
                          'war': 'War',
                          'western': 'Western'
