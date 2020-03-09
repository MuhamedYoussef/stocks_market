import concurrent.futures
import json
import string
import random

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView


class Stocks(TemplateView):
    template_name = 'stocks/stocks.html'




alphabet = list(string.ascii_lowercase)


# Due to API limitation, just decided to have multibale api key so we less likely to wait
API_KEYS_FEATCHING = [
    'DOFH5YHCP9UC43S3',
    'SYVSOE4WGQXSH4F5',
    'MUW8UDTMRIFQ2N2H',
    '3W6QJ37PFZCJ1OBK'
]


API_KEYS_DETAILS = [
    'WFJYN96EUGP206WM',
    'Y33FIBNZ8VS7UDOB',
    'F7X0VUQBTIPUUNIH',
    '00B0JMXSTRLK6VWD',
    'WU3VGNPFA9DU7GNR'
]



def get_stocks(request):
    
    def get_stock(alpha):
        # Send the request to the api and return the stock data
        r = requests.get(f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={alpha}&apikey={API_KEYS_FEATCHING}')
        return json.loads(r.text)


    # Using threads we send requests to the servers simultaneously and return a json response to the client
    data_by_symoble = {}

    with concurrent.futures.ThreadPoolExecutor() as executer:
        results = [executer.submit(get_stock, alpha) for alpha in alphabet]

        for f in concurrent.futures.as_completed(results):
            if 'bestMatches' in f.result().keys():
                
                for match in f.result()['bestMatches']:
                    if match['1. symbol'] not in data_by_symoble.keys():
                        data_by_symoble[match['1. symbol']] = match

    return JsonResponse(data_by_symoble, safe=False)


def get_stock_detail(request):
    symbol = request.GET['symbol']
    r = requests.get(f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={random.choice(API_KEYS_DETAILS)}')
    return JsonResponse(json.loads(r.text), safe=False)