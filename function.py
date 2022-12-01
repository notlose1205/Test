from pybit.usdt_perpetual import HTTP
from datetime import datetime
import time

##### bybit key #####
session = HTTP(
    endpoint="https://api.bybit.com", 
    api_key="iX7k37KXnQjwBzGZhd", 
    api_secret="srUkMMdV6LowHORthjqdNM2pkH8fI5VCjEVF" 
)

USDT = session.get_wallet_balance(coin="USDT")['result']['USDT']['available_balance'] # USDT 보유량
#position_average_short = session.my_position(symbol='BTCUSDT')['result'][1]['entry_price'] # BTCUSDT short average position price
position_average_long = session.my_position(symbol='BTCUSDT')['result'][0]['entry_price'] # BTCUSDT long average position price
position_leverage_short = session.my_position(symbol='BTCUSDT')['result'][1]['leverage'] # BTCUSDT short 레버리지
position_leverage_long = session.my_position(symbol='BTCUSDT')['result'][0]['leverage'] # BTCUSDT long 레버리지
BTCUSDT_now = float(session.latest_information_for_symbol(symbol='BTCUSDT')['result'][0]['last_price']) # BTCUSDT 현재 가격

def price():
    BTCUSDT_now = float(session.latest_information_for_symbol(symbol='BTCUSDT')['result'][0]['last_price']) # BTCUSDT 현재 가격
    return BTCUSDT_now

pre_price = [BTCUSDT_now, BTCUSDT_now, BTCUSDT_now, BTCUSDT_now, BTCUSDT_now]
delta_price = [0,0,0,0,0]
print(pre_price)

while True:
    now = datetime.now()

    period_5 = now.minute % 5


    if period_5 == 0 and now.second < 1 :

        for i in range(0,4):
            pre_price[4-i] = pre_price[3-i]
        pre_price[0] = price()

        for i in range(0,4):
            delta_price[4-i] = pre_price[3-i] -pre_price[4-i]

    delta_price[0] = price() - pre_price[0]    
    
    print(price(), delta_price, pre_price, now)    

    time.sleep(1)













