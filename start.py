from logging.handlers import RotatingFileHandler


from flask import Flask, stream_with_context, Response, request, send_from_directory, jsonify
from datetime import datetime
from time import strftime

import subprocess
import os, sys
import logging
import traceback

app = Flask(__name__) #creating the Flask class object   
app._static_folder = os.path.abspath("assets/")
 
@app.route('/') #decorator drfines the   
def root():  
    root_dir = os.path.dirname(os.getcwd())
    #return send_from_directory(os.path.join(root_dir, 'assets'), 'index.html')
    return app.send_static_file('index.html')


@app.route('/download/request', methods=['GET', 'POST'])  
def saveDownload(): 
    data = request.get_json()
    durl = data.durl 
    process = subprocess.Popen(['python3' , 'download.py', durl ], stdout=subprocess.PIPE)
    out, err = process.communicate()
    logger.error("output:"+out)
    logger.error("error:"+err)
    return "submitted"

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('assets', path)

@app.route('/getfile/<string:file>')
def send_file(file):
    return send_from_directory('files', file)

@app.route('/deletefile/<string:file>')
def delete_file(file):
    os.remove('files/'+file)
    return "success"

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



@app.route("/error")
def get_nothing():
    """ Route for intentional error. """
    return foobar # intentional non-existent variable


@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response


@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500




if __name__ =='__main__':  
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)        
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    app.run(host ='0.0.0.0',debug = True)  
