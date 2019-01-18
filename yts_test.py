import math
from yts import yts, score

test = yts()
# test.search('limit=100')
# test.search('love genre=Action quality=1080p minimum_rating=4 sort_by=latest order_by=desc with_rt_ratings=Yes page=2 limit=10000')
# test.search('Scarlett Johansson page=2')
# test.search('Mandy Patinkin page=1')
test.search('Gerard Butler')
# test.search('Sylvester Stallone')
# test.search('love')
# for i in range(1, 10):
#     print(i)

# item_total = 9321
# item_limit = 20
# item_each = math.ceil(item_total/item_limit) + 1
#
# print(item_each)
# for i in range(1, 10):
#     print(i)