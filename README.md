# fetch-challenge
a receipt-processing API


In order to test the functionality of this program, I used https://designer.mocky.io/ to simulate an HTML response (see line 68 of main.py); the body contains one of the example receipts as a JSON object. I have already added the corresponding entry to the simulated database (starting line 10 of main.py) since the database does not persist in memory from testing the Process path to testing the Points path.

INSTRUCTIONS: to run the program in this codespace, type "uvicorn main:app --reload" into the terminal and hit ENTER. There should be a line close to

"INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"

where the underlined path can be opened via CTRL+Click. To send a different JSON request, change the value of request_url in line 68 of main.py.