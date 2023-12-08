# ----------------------------------------------------------------------------
# NOTICE: This code is the exclusive property of University of Kansas
#         Architecture Research and is strictly confidential.
#
#         Unauthorized distribution, reproduction, or use of this code, in
#         whole or in part, is strictly prohibited. This includes, but is
#         not limited to, any form of public or private distribution,
#         publication, or replication.
#
# For inquiries or access requests, please contact:
#         Alex Manley (amanley97@ku.edu)
#         Mahmudul Hasan (m.hasan@ku.edu)
# ----------------------------------------------------------------------------
from flask import Flask, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Filler values
board_types = ["simple"]
cache_types = ["no cache"]

@app.route('/')
def index():
    response1 = requests.get('http://127.0.0.1:5000/get-cpu-types')
    cpu_types = response1.json() if response1.status_code == 200 else None

    response2 = requests.get('http://127.0.0.1:5000/get-mem-types')
    mem_types = response2.json() if response2.status_code == 200 else None

    return render_template('index.html', 
                            board_types=board_types,
                            cpu_types=cpu_types,
                            mem_types=mem_types,
                            cache_types=cache_types)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
