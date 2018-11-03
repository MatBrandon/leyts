# VERSION: 1.0
# AUTHORS: Khen Solomon Lethil (khensolomon@gmail.com)

# dev
from novaprinter import prettyPrinter
from helpers import retrieve_url, download_file
# qBt
# from novaprinter import prettyPrinter
# from bs4 import BeautifulSoup
# from helpers import retrieve_url, download_file

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

from bs4 import BeautifulSoup

class yts(object):
    url = 'https://yts.am'
    name = 'YTS'
    supported_categories = {'all': ''}


    class SimpleHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            print("Start tag:", tag)
            for attr in attrs:
                print("     attr:", attr)

        def handle_endtag(self, tag):
            print("End tag  :", tag)

        def handle_data(self, data):
            print("Data     :", data)

        def handle_comment(self, data):
            print("Comment  :", data)

        def handle_entityref(self, name):
            c = chr(name2codepoint[name])
            print("Named ent:", c)

        def handle_charref(self, name):
            if name.startswith('x'):
                c = chr(int(name[1:], 16))
            else:
                c = chr(int(name))
            print("Num ent  :", c)

        def handle_decl(self, data):
            print("Decl     :", data)


    def search(self, what, cat='all'):
        parser = self.SimpleHTMLParser()
        parser.feed('<p><a class=link href=#main>tag soup</p ></a>')

if __name__=="__main__":
    yts.search(yts,'hate')