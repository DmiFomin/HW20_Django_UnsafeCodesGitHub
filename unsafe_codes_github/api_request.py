import requests
import pprint


response = requests.get('http://127.0.0.1:8000/api/0/unsafe_codes')

pprint.pprint(response.json())