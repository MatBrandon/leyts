import os
import time

# import libtorrent as lt

dir_path  = os.getcwd()
print(dir_path)
# ses = lt.session()
# params = { 'save_path': '/home/downloads/'}
# link = "magnet:?xt=urn:btih:4MR6HU7SIHXAXQQFXFJTNLTYSREDR5EI&tr=http://tracker.vodo.net:6970/announce"
# handle = lt.add_magnet_uri(ses, link, params)
#
# print 'downloading metadata...'
# while (not handle.has_metadata()): time.sleep(1)
# print 'got metadata, starting torrent download...'
# while (handle.status().state != lt.torrent_status.seeding):
#     print '%d %% done' % (handle.status().progress*100)
#     time.sleep(1)

