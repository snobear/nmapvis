#!/usr/bin/env python
"""
nmapvis REST API
"""
from flask import Flask, render_template, request, jsonify
from flask_uploads import UploadSet, configure_uploads
import os
import sys
import errno
from backend.log import setup_logging
from backend.nmap import scan_exists, process_file, get_results
from xml.etree.ElementTree import ParseError

# configs
DBNAME = "./backend/nmap.db"
app = Flask(__name__)
app.config['UPLOADED_FILES_DEST'] = 'uploads'
xml_file = UploadSet('files', ('xml',))

log = setup_logging(level='debug', log_to_terminal=True)

configure_uploads(app, xml_file)

# helpers
def startup_checks():
    """
    Run some pre-start checks:
    - uploads directory exists and is writeable by flask
    - sqlite DB exists
    """
    # debug
    if not os.path.exists(app.config['UPLOADED_FILES_DEST']):
        log.error("error: uploads directory %s does not exist." % app.config['UPLOADED_FILES_DEST'])
        sys.exit(1)

    if not os.access(app.config['UPLOADED_FILES_DEST'], os.R_OK | os.W_OK | os.X_OK):
        log.error("error: uploads directory %s is not writeable by web server." % app.config['UPLOADED_FILES_DEST'])
        sys.exit(1)

    if not os.path.exists(DBNAME):
        log.error("database %s does not exist. You must initialize the sqlite db with the schema." % DBNAME)
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), DBNAME)

# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-results', methods=['GET'])
def get_scan_results():
    """Fetch scan results"""
    try:
        res = get_results(DBNAME)
        return jsonify(res), 200
    except Exception as e:
        log.error("exception during get_scan_results fetch: %s" % e)
        return jsonify("encountered server error while fetching results"), 500

@app.route('/upload', methods=['POST'])
def upload():
    """Upload xml file endpoint"""
    if 'scanresults' in request.files:
        filename = request.files['scanresults'].filename
        overwrite = request.form.get('overwrite')
        log.debug(overwrite)
        if scan_exists(DBNAME, filename) and (overwrite != 'true'):
            msg = "%s already imported and overwrite not selected." % filename
            log.debug(msg)
            resp={ 'result': 'UPLOAD_FILE_EXISTS', 'msg': msg }
            return jsonify(resp), 400

        try:
            # save file to disk
            result_filename = xml_file.save(request.files['scanresults'])
            upload_path = "%s/%s" % (app.config['UPLOADED_FILES_DEST'], result_filename)
            log.debug("file saved successfully: %s" % upload_path)

            # parse and ingest data to DB
            process_file(DBNAME, filename, upload_path, overwrite)

            resp={ 'result': 'UPLOAD_SUCCESS', 'msg': 'File imported successfully'}
            return jsonify(resp), 200
        except ParseError as e:
            log.error("xml parse error: %s" % e)
            resp={ 'result': 'INVALID_XML', 'msg': 'not a valid xml file.' }
            return jsonify(resp), 400
        except Exception as e:
            log.error("exception during file import: %s" % e)
            return jsonify("encountered server error while importing file"), 500

    else:
        msg = 'scanresults file not present in request.'
        log.debug(msg)
        resp={ 'result': 'FILE_NOT_ATTACHED', 'msg': msg }
        return jsonify(resp), 400

if __name__ == "__main__":
    startup_checks()
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)
