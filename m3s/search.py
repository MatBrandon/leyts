import leht
# from datetime import datetime
test=leht.result('3pmramnaym','ten')
query = test.queries()

# 30/12/2003
# 13/03/2005
# 13/03/2005

# datestring = "2008-12-12 19:21:10" %Y-%m-%d %H:%M:%S
# alb = datetime.strptime('13/03/2005', '%d/%m/%Y')
# alb = datetime.strptime('13/03/2005', '%d/%m/%Y')
# # print alb.year, alb.month, alb.day
# print(alb.year)


test.album_location_json = '../dist/mp3/{}/info.json'
test.album_location_cover = '../dist/mp3/{}/cover{}'
test.album_location_audio = '../dist/mp3/{}/{}.mp3'

# from=1 to=last type=scv
# audio=yes album=3
# audio=yes from=1 to=last type=scv artist=3
# audio=yes from=1 to=last type=scv artist=29

test.album_list_scan_audio_save=query['audio'] and True
query_from = query['from'].isnumeric() and int(query['from']) > 0 and query['from']
query_to = query['to']

if 'album' in query and query['album'].isnumeric() and int(query['album']) > 0:
    test.album_info('mm',query['album'],True)
else:
    if 'artist' in query and query['artist'].isnumeric() and int(query['artist']) > 0:
        test.album_list_scan_by_artist=query['artist']

    if query['log-id']:
        try:
            test.album_ids = test.json_load(query['log-id'])
        except Exception as e:
            test.album_ids = {}

    for item_type in set(query['type']):
        if query_from and item_type in 'scv':
            test.album_lists={}
            test.album_list_scan('mm',item_type.upper(),query_from,query_to)
            if query['log-list']:
                if test.album_lists:
                    test.json_save(query['log-list'].format(item_type),test.album_lists)
                # if test.artist_lists:
                #     test.json_save(query['log-list'].format(item_type),test.artist_lists)

    if query['log-id']:
        test.json_save(query['log-id'],test.album_ids)