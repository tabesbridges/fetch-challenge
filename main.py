import hashlib # the function hashlib.sha256() is a secure hashing algorithm
import requests
from fastapi import FastAPI
from math import ceil
from pydantic import BaseModel

app = FastAPI()

database = {"49f8d3bb7c9e68f1d2edebaf54e250a59f760c5cf7eab8136fb289cd7b2fe057": {
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },{
      "shortDescription": "Emils Cheese Pizza",
      "price": "12.25"
    },{
      "shortDescription": "Knorr Creamy Chicken",
      "price": "1.26"
    },{
      "shortDescription": "Doritos Nacho Cheese",
      "price": "3.35"
    },{
      "shortDescription": "Klarbrunn 12PK 12 FL OZ",
      "price": "12.00"
    }
  ],
  "total": "35.35"
}
}

class Item(BaseModel):
    shortDescription: str
    price: str

class Receipt(BaseModel):
    # to define a class that inherits from BaseModel, we simply list
    # the attributes and their types
    retailer: str
    purchaseDate: str
    purchaseTime: str
    items: Item
    total: str


@app.get('/receipts/process')
def process():
    """
    Process
    
    This path operation takes in a receipt as a JSON object from the request
    body, generates an ID using a hash function, and returns that id

    Parameters:
    - None

    Returns the id as a JSON object
    """
    # our database is a dictionary (defined globally), where we will use
    # our id as the key and the JSON object-cum-dictionary (the receipt)
    # as the value

    # prepare the key and value
    request_url = 'https://run.mocky.io/v3/a06975d3-cc19-431d-9358-53bc2afbd009'
    new_db_entry = requests.get(request_url).json()
    id_string = make_id(new_db_entry)
    new_db_key = id_string['id']

    # add the key-value pair to the database and return id string,
    # which FastAPI by default converts to JSON
    database[new_db_key] = new_db_entry
    return id_string
    

def make_id(json_receipt):
    # encode the JSON payload in bytes before hashing
    encoded_receipt = str(json_receipt).encode()

    # run the hashing algorithm
    hash_value = hashlib.sha256(encoded_receipt)

    # convert the hash object to a string
    hash_string = hash_value.hexdigest()

    # store the hash value in a dictionary and return it
    dict_to_return = {'id': hash_string}
    return dict_to_return

@app.get('/receipts/{id}/points')
def points(id: str):
    """
    Points
    
    This path operation takes in an ID, looks up the corresponding
    receipts, and computes the "score" of that receipt according
    to a given set of arbitrary rules

    Parameters:
    - id

    Returns the total score as a JSON object
    """
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

    # store the hash value in a dictionary and return it
    dict_to_return = {'points': score}
    return dict_to_return