#!/usr/bin/env python3

import sys
import requests
import json

FINNA_API_SEARCH='https://api.finna.fi/v1/search'

def search_finna(keyword, page=1):
#    keywords = ['miehet','naiset','lapset','nuoret','aikuiset','perheet',
#                'vanhukset','ikääntyneet','muotokuvat','ryhmäkuvat','henkilöt']
#    keywords = ['muotokuvat']
    keywords = [keyword]

    fields = ['title','images','nonPresenterAuthors','buildings','id','year']
    params = {'filter': 'format:0/Image/',
              'field[]': fields,
              'join': 'AND',
              'bool0[]': 'OR',
              'lookfor0[]': keywords,
              'type0': 'AllFields',
              'limit': 100,
              'page': page}
    req = requests.get(FINNA_API_SEARCH, params=params)
    response = req.json()
    if 'records' in response:
        return response['records']
    return None

keyword = sys.argv[1]

for page in range(1, 1001):
    records = search_finna(keyword, page)
    if not records:
        break
    for rec in records:
        print(json.dumps(rec))
