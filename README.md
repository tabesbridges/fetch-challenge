# fetch-challenge
a receipt-processing API


In order to test the functionality of this program, I used https://designer.mocky.io/ to simulate an HTML response (see line 68 of main.py); the body contains one of the example receipts as a JSON object. I have already added the corresponding entry to the simulated database (starting line 10 of main.py) since the database does not persist in memory over the course of testing the Process path and testing the Points path.

INSTRUCTIONS: to run this program, click Code>Codespaces>"Create codespace on main". Once the codespace has loaded, type "pip install requests fastapi pydantic uvicorn" into the terminal and hit ENTER to install dependencies. To run the program, type "uvicorn main:app --reload" into the terminal and hit ENTER. There should be a line close to

"INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"

where the URL can be opened by clicking with CTRL/CMD held down.

Note: I have hardcoded the simulated HTML response described above. To send different responses to the API, change the value of request_url in line 68 of main.py.
