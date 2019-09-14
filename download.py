
from logging.handlers import RotatingFileHandler

import requests
import os, sys
from urllib.parse import unquote

import logging
import traceback




PY3 = sys.version_info[0] >= 3
if PY3: #python3
    from urllib.parse import urlparse
    from urllib.request import urlopen
else: #python2
    from urlparse import urlparse
    from urllib2 import urlopen # Python 2


if __name__ =='__main__':  
 handler = RotatingFileHandler('downloadapp.log', maxBytes=10000, backupCount=3)        
 logger = logging.getLogger(__name__)
 logger.setLevel(logging.ERROR)
 logger.addHandler(handler)
 logger.error("output: test")
 if len (sys.argv) != 2 :
    print("Usage: python download.py <<url>>")
    sys.exit (1)

 link = sys.argv[1:][0]
#link = 'https://nl18.seedr.cc/ff_get/510875226/www.TamilRockers.ws%20-%20X-Men%20Dark%20Phoenix%20(2019)[720p%20-%20BDRip%20-%20Org%20Auds%20[Tamil%20%20Telugu%20%20Hindi]%20-%20AC3%205.1%20-%20HEVC].mkv?st=v_kl_vuJ6OenhFktGNYb8w&e=1568024548'
 if not os.path.exists("files"):
    os.makedirs("files")
 file_name=os.path.normpath("files/"+unquote(os.path.basename(urlparse(link).path)))
 print("Filename: "+file_name)
 print("Downloading %s" % file_name)
 response = urlopen(link)
 CHUNK = 16 * 1024
 with open(file_name, 'wb') as f:
    while True:
        chunk = response.read(CHUNK)
        if not chunk:
            break
        f.write(chunk)
