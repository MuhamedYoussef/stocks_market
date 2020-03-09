import concurrent.futures
import json
import string
import random

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView


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



class Stocks(TemplateView):
    template_name = 'stocks/stocks.html'


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



"""
    __NOTES__

    As per API docs there weren't any end point that can expose a list of companies for us, so i figured out to search by all the alphabets, ofc waiting for the resposne takes a lot of time so I used threads to send multible requests in the same time, I also tried to seperate the API keys for fetching the companies list from those which just get the detail of a given symbol, It didn't go well for all cases though! BTW if you click on a symbol and it continue to give you the limitation error please try again after 1m.

    I was asked to use DRF and model-based serializer in this test, however I didn't find any reasonable situation where I can make use of them, except if you wanted to save the returned data in the database for some reason!

    Please feel free to contact me for more explanation or details. Thank you)

"""