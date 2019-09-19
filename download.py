
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
 logger.error("link :"+link)
#link = 'https://nl27.seedr.cc/ff_get/515994809/www.TamilRockers.ws%20-%20Bakrid%20(2019)%20Tamil%20HDRip%20x264%20400MB.mkv?st=mK8oo4-6kipmBM5D9W0hNA&e=1568945595'
if not os.path.exists("files"):
    os.makedirs("files")
file_name=os.path.abspath("files/"+unquote(os.path.basename(urlparse(link).path)))
logger.error("filename :"+file_name)
print("Filename: "+file_name)
print("Downloading %s" % file_name)
try:
   response = urlopen(link)
   CHUNK = 16 * 1024
   with open(file_name, 'wb') as f:
     while True:
        chunk = response.read(CHUNK)
        if not chunk:
            break
        f.write(chunk)
except Exception as e:
    logger.error(e)
