import random
import requests
import json
import re
from common.header import UA_LIST
from bs4 import BeautifulSoup
ua = {
    'user-agent': random.choice(UA_LIST)
}


def GET(url: str):
    try:
        r = requests.get(url=url, headers=ua)
        r.raise_for_status()
        print('Request GET successfully!')
        return BeautifulSoup(r.text, 'lxml')
    except:
        print("Request GET Failed")
