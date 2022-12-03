import json # The main functions are json.loads(), which turns JSON objects into strings; and json.dumps(), which does the reverse
import hashlib # the function hashlib.sha256() is a secure hashing algorithm
from flask import *


app = Flask(__name__)

@app.route('/receipts/process', methods=['POST'])
def get_id():
    # encode the JSON payload in bytes before hashing
    encoded_receipt = json_receipt.encode()

    # run the hashing algorithm
    hash_value = hashlib.sha256(encoded_receipt)

    # convert the hash object to a string
    hash_string = hash_value.hexdigest()

    # store the hash value in a dictionary
    dict_to_return = {'id': hash_string}

    # convert the dictionary to a JSON object and return it
    json_dict = json.dumps(dict_to_return)
    return json_dict

