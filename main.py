import json # The main functions are json.loads(), which turns JSON objects into strings; and json.dumps(), which does the reverse
import hashlib # the function hashlib.sha256() is a secure hashing algorithm
from flask import *
from math import ceil

database = {}

json_receipt = """
{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-03-20",
  "purchaseTime": "14:33",
  "items": [
    {
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    },{
      "shortDescription": "Gatorade",
      "price": "2.25"
    }
  ],
  "total": "9.00"
}
"""

app = Flask(__name__)

@app.route('/receipts/process', methods=['POST'])
def process():
    # our database is a dictionary, where we will use our id as the key and the
    # JSON object-cum-dictionary as the value

    # prepare the key and value
    new_db_entry = json.loads(json_receipt)
    json_id = make_id()
    new_db_key = json.loads(json_id)['id']

    # add the key-value pair to the database and return the JSON id object
    database[new_db_key] = new_db_entry
    return json_id
    

def make_id():
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

@app.route(f'/receipts/{process()}/points', methods=['GET'])
def points(id):
    # look up the receipt in the database
    receipt = database[id]

    # extract strings from the receipt
    retailer = receipt["retailer"]
    purchase_date = receipt["purchaseDate"]
    purchase_time = receipt["purchaseTime"]
    total = receipt["total"]
    # and extract the final entry of the receipt, which is itself a list of dictionaries
    items = receipt["items"]

    # initialize running total
    score = 0

    # add 1 point for alphanumeric characters in the retailer name
    for char in retailer:
        if char.isalnum():
            score += 1
    
    # add 50 points for round dollar amounts, and 25 points for totals
    # ending in .00, .25, .50, or .75
    cents = total.split('.')[1]
    if cents == "00":
        score += 75
    elif cents == "25" or cents == "50" or cents == "75":
        score += 25
    
    # add 5 points for every two items on the receipt
    item_count = len(items)
    adjusted_item_count = item_count // 2
    score += 5 * adjusted_item_count

    # check for items whose description has length a multiple of 3, adjust the price (*.2 and round up), and add to 
    for item in items:
        if len(item["shortDescription"]) % 3 == 0:
            price = item["price"]
            adjusted_price = ceil(float(price) * 0.2)
            score += adjusted_price
    
    # check for odd purchase date, in which case add 6
    date = int(purchase_date.split('-')[2])
    if date % 2 == 1:
        score += 6

    # check for time between 2:00pm and 4:00pm, in which case add 10
    hour = int(purchase_time.split(':')[0])
    minute = int(purchase_time.split(':')[1])
    if hour == 15:
        score += 10
    elif hour == 14 and minute != 00:
        score += 10

    # store the hash value in a dictionary
    dict_to_return = {'points': score}

    # convert the dictionary to a JSON object and return it
    json_dict = json.dumps(dict_to_return)
    return json_dict

