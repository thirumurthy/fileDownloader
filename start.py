from flask import Flask, stream_with_context, Response, request, send_from_directory, jsonify
from datetime import datetime

import subprocess
import os, sys
 

app = Flask(__name__) #creating the Flask class object   
app._static_folder = os.path.abspath("assets/")
 
@app.route('/') #decorator drfines the   
def root():  
    root_dir = os.path.dirname(os.getcwd())
    #return send_from_directory(os.path.join(root_dir, 'assets'), 'index.html')
    return app.send_static_file('index.html')


@app.route('/download/request')  
def saveDownload(): 
    durl = request.args.get('durl')
    process = subprocess.Popen(['python' , 'download.py', durl ], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return "submitted"

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/getfile/<string:file>')
def send_file(file):
    return send_from_directory('files', file)

@app.route('/getfileinfo')
def getfileDetails():
    finfo =[]
    with os.scandir('files') as dir_entries:
        for entry in dir_entries:
            slgdata = {}
            info = entry.stat()
            slgdata['name'] = entry.name
            slgdata['ctime'] = datetime.utcfromtimestamp(info.st_ctime).strftime('%Y-%m-%d %I:%M %p')
            slgdata['size'] = human_size(info.st_size)
            finfo.append(slgdata)
            print(info.st_mtime)
    return jsonify(finfo)

def human_size(size_bytes):
    """
    format a size in bytes into a 'human' file size, e.g. bytes, KB, MB, GB, TB, PB
    Note that bytes/KB will be reported in whole numbers but MB and above will have greater precision
    e.g. 1 byte, 43 bytes, 443 KB, 4.3 MB, 4.43 GB, etc
    """
    if size_bytes == 1:
        # because I really hate unnecessary plurals
        return "1 byte"

    suffixes_table = [('bytes',0),('KB',0),('MB',1),('GB',2),('TB',2), ('PB',2)]

    num = float(size_bytes)
    for suffix, precision in suffixes_table:
        if num < 1024.0:
            break
        num /= 1024.0

    if precision == 0:
        formatted_size = "%d" % num
    else:
        formatted_size = str(round(num, ndigits=precision))

    return "%s %s" % (formatted_size, suffix)

if __name__ =='__main__':  
    app.run(debug = True)  
