
import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger()
logger.propagate = False
import requests
import json
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import matplotlib.pyplot as plt
import math
from time import sleep
import pandas as pd
import csv
import datetime
from binance.um_futures import UMFutures
futures = UMFutures(key='2e9liyhYbVsY86Zktwd9iFHC0XwuSE8TCurRROrhRbt9xdRCvexpPqswrpsaGYfX',
                    secret='bcUCKjqb3V75OtDrjqsevA1W1J2BYQ6EdVKPVlPWtyPaX04t4YiasThnT87sVbRu')
from binance.spot import Spot as Client
client = Client(api_key='2e9liyhYbVsY86Zktwd9iFHC0XwuSE8TCurRROrhRbt9xdRCvexpPqswrpsaGYfX',
                api_secret='bcUCKjqb3V75OtDrjqsevA1W1J2BYQ6EdVKPVlPWtyPaX04t4YiasThnT87sVbRu')

#######################################################################################
def get_df_cl(coin,interval="1m",limit=30):
    para = f"{coin}USDT"
    df = client.klines(para,interval=interval,limit = limit)
    df = pd.DataFrame(df,columns=["open_time","open","high","low","close","volume","close_time",
                                "quote_volume","count","taker_buy_volume","taker_buy_quote_volume","guyn"])
    df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
    df["close_time"] = pd.to_datetime(df["close_time"], unit='ms')
    df["open"] = df["open"].astype('float')
    df["high"] = df["high"].astype('float')
    df["low"] = df["low"].astype('float')
    df["count"] = df["count"].astype('float')
    df["close"] = df["close"].astype('float')
    df["volume"] = df["volume"].astype('float')
    df["quote_volume"] = df["quote_volume"].astype('float')
    df["taker_buy_volume"] = df["taker_buy_volume"].astype('float')
    df["taker_buy_quote_volume"] = df["taker_buy_quote_volume"].astype('float')
    df.index = pd.to_datetime(df['open_time'])

    df = df.drop(columns=['close_time',"quote_volume",
                        "taker_buy_volume","taker_buy_quote_volume",
                        "open_time",], axis=1)#"close","open",
    

    df['smma_3'] = df['close'].ewm(span=3, adjust=False).mean()
    df['smma_7'] = df['close'].ewm(span=7, adjust=False).mean()
    df['smma_35'] = df['close'].ewm(span=35, adjust=False).mean()
    df['std_7'] = df['close'].rolling(window=7).std()
    df['max_7'] = df['close'].rolling(window=7).max()
    df['min_7'] = df['close'].rolling(window=7).min()
    df['mean_7'] = df['close'].rolling(window=7).mean()
    df['q_15'] = df['close'].rolling(window=7).quantile(0.15)
    df['q_85'] = df['close'].rolling(window=7).quantile(0.85)
    df['qmin'] = df['low'].quantile(0.15)# 15
    df['qmax'] = df['high'].quantile(0.85)# 85
    df['btc_price'] = float(futures.ticker_price("BTCUSDT")['price'])
    df['eth_price'] = float(futures.ticker_price("ETHUSDT")['price'])
    df['guyn'] = df['close']-df['open']
    df['guyn'] = df['guyn'].apply(lambda x: 0 if x < 0 else 1)
    df = df[-1:]
    price = df["close"].values[-1]
    qmin = df['qmin'].values[-1]
    qmax = df['qmax'].values[-1]
    return price, qmin, qmax

############################################################################################
def get_df(coin,interval="1m",limit=30):
    para = f"{coin}USDT"
    # print(para,coin)
    df = futures.klines(para,interval=interval,limit = limit)
    df = pd.DataFrame(df,columns=["open_time","open","high","low","close","volume","close_time",
                                "quote_volume","count","taker_buy_volume","taker_buy_quote_volume","guyn"])
    df["open_time"] = pd.to_datetime(df["open_time"], unit='ms')
    df["close_time"] = pd.to_datetime(df["close_time"], unit='ms')
    df["open"] = df["open"].astype('float')
    df["high"] = df["high"].astype('float')
    df["low"] = df["low"].astype('float')
    df["count"] = df["count"].astype('float')
    df["close"] = df["close"].astype('float')
    df["volume"] = df["volume"].astype('float')
    df["quote_volume"] = df["quote_volume"].astype('float')
    df["taker_buy_volume"] = df["taker_buy_volume"].astype('float')
    df["taker_buy_quote_volume"] = df["taker_buy_quote_volume"].astype('float')
    df.index = pd.to_datetime(df['open_time'])

    df = df.drop(columns=['close_time',"quote_volume",
                        "taker_buy_volume","taker_buy_quote_volume",
                        "open_time",], axis=1)#"close","open",
    

    df['smma_3'] = df['close'].ewm(span=3, adjust=False).mean()
    df['smma_7'] = df['close'].ewm(span=7, adjust=False).mean()
    df['smma_35'] = df['close'].ewm(span=35, adjust=False).mean()
    df['std_7'] = df['close'].rolling(window=7).std()
    df['max_7'] = df['close'].rolling(window=7).max()
    df['min_7'] = df['close'].rolling(window=7).min()
    df['mean_7'] = df['close'].rolling(window=7).mean()
    df['q_15'] = df['close'].rolling(window=7).quantile(0.15)
    df['q_85'] = df['close'].rolling(window=7).quantile(0.85)
    df['qmin'] = df['low'].quantile(0.15)# 15
    df['qmax'] = df['high'].quantile(0.85)# 85
    df['btc_price'] = float(futures.ticker_price("BTCUSDT")['price'])
    df['eth_price'] = float(futures.ticker_price("ETHUSDT")['price'])
    df['guyn'] = df['close']-df['open']
    df['guyn'] = df['guyn'].apply(lambda x: 0 if x < 0 else 1)
    df = df[-1:]
    price = df["close"].values[-1]
    qmin = df['qmin'].values[-1]
    qmax = df['qmax'].values[-1]
    return price, qmin, qmax

########################################################################################################
def send_text(text):
    tok = "6460907609:AAH0ZCfogSLjFUc0aVnS8ZO9McP7OF8DLek" #@Saponjyan_Bot
    my_id = "6346385312"  
    my_id = "-1002064596122" # spj_signals
    url_req = "https://api.telegram.org/bot" + tok + "/sendMessage" + "?chat_id=" + my_id + "&text=" + text
    results = requests.get(url_req)

#################################################################################################
def pl(c,coin,msg = " "):
    para = f"{coin}USDT"
    if c == "c":
        df = client.klines(para,interval="15m",limit = 1000)
    else:
        df = futures.klines(para,interval="15m",limit = 1000)
    # df = client.klines(para,interval="1m",limit = 1000)
    df = pd.DataFrame(df,columns=["open_time","open","high","low","close","volume","close_time",
                                "quote_volume","count","taker_buy_volume","taker_buy_quote_volume","guyn"])
    df["close"] = df["close"].astype('float')
    
    price = df["close"].values[-1]
    df["close_time"] = pd.to_datetime(df["close_time"], unit='ms')
    df['close_time'] = df['close_time'].dt.floor('s')# min
    
    # print(df["close_time"])
    # df.set_index('close_time', inplace=True)
    # df['close_time'] = pd.to_datetime(df['close_time'])
    
    # Построение линий
    plt.plot(df.index, df['close'], label=f'price {price}')
    # plt.plot(df["close"], df['close_time'], label=f'price {price}')
    plt.legend()
    # Настройка осей и заголовка
    plt.xlabel(f"{msg}")
    plt.ylabel(f'{coin} 15 minute')
    plt.title(f'ATTENTION!!! {coin} price {price} {msg}')
    
    image_path = 'graph2.png'
    plt.savefig(image_path)
    # Отображение графика
    # display(plt.show())
    plt.close()


    bot_token = '6460907609:AAH0ZCfogSLjFUc0aVnS8ZO9McP7OF8DLek'
    chat_id = "6346385312"
    chat_id = "-1002064596122" # spj_signals
    
    file = "graph2.png"

    files = {
        'photo': open(file, 'rb')
    }

    message = ('https://api.telegram.org/bot'+ bot_token + '/sendPhoto?chat_id=' 
            + chat_id)
    send = requests.post(message, files = files)
#################################################################################################

def scan():
    send_text("start")
    count = 0
    ccoins = []
    fcoins = []
    fundings = []
    while True:

        
        # count = count +1
        # if count % 5 == 0:
        #     ccoins = []
        #     fcoins = []
        #     fundings = []
        
    #############################################################################################
        df = futures.ticker_24hr_price_change()
        df = pd.DataFrame(df)
        df = df[df['symbol'].str.endswith("USDT")]
        paras = list(df['symbol'])
        
        

        for para in paras:
            # print(para)
            try:
                para = para.split("USDT")[0]
                price, qmin, qmax = get_df(para,'1m',1000)
                if price * 0.95 >= qmax or price * 1.05 <= qmin:
                    if para not in fcoins:
                        # send_text(f"ATTENTION! USDⓈ-M {para}")
                        pl(c="f",coin=para,msg = f"USDⓈ-M")
                        fcoins.append(para)
            except:
                print("error")
    ###################################################################################
        for para in paras:
            funding = round(float(requests.get(f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={para}").json()['lastFundingRate']),3)
            para = para.split("USDT")[0]
            if abs(funding) > 0.5:
                if para not in fundings:
                    # send_text(f"ATTENTION! USDⓈ-M {para}  {funding}")
                    pl(c ="f",coin = para,msg=f"Funding Rate is  {funding}")
                    fundings.append(para)
        
        
        df = client.ticker_24hr()
        df = pd.DataFrame(df)
        df = df[df['symbol'].str.endswith("USDT")]
        paras = list(df['symbol'])
        
        for para in paras:
            
            para = para.split("USDT")[0]
            price, qmin, qmax = get_df_cl(para,'1m',1000)
            if price * 0.95 >= qmax or price * 1.05 <= qmin:
                if para not in ccoins:
                    # send_text(f"ATTENTION! SPOT {para}")
                    pl("c",para,msg="SPOT")
                    ccoins.append(para)
