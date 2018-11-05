#!/usr/bin/env python
# VERSION: 3.3
# AUTHORS: Khen Solomon Lethil (khensolomon@gmail.com)
import json
import time
import re
import math
try:
    # python3
    from urllib.parse import urlencode, unquote, quote_plus
    from html.parser import HTMLParser
except ImportError:
    # python2
    from urllib import urlencode, unquote, quote_plus
    from HTMLParser import HTMLParser

# local
from novaprinter import prettyPrinter
from helpers import retrieve_url
