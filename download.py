import requests
import os, sys
from urllib.parse import unquote


PY3 = sys.version_info[0] >= 3
if PY3: #python3
    from urllib.parse import urlparse
else: #python2
    from urlparse import urlparse


if len (sys.argv) != 2 :
    print("Usage: python download.py <<url>>")
    sys.exit (1)

link = sys.argv[1:][0]
if not os.path.exists("files"):
    os.makedirs("files")
file_name=os.path.normpath("files/"+unquote(os.path.basename(urlparse(link).path)))
print("Filename: "+file_name)
with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()