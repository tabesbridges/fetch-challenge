import json
from flask import *
# The main functions are json.dumps(), which turns JSON objects into strings; and json.loads(), which does the reverse

app = Flask(__name__)

@app.route('/receipts/process', methods=['POST'])
def get_id():
    response = {'id'}