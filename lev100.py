#from pybit.usdt_perpetual import HTTP
from pybit import usdt_perpetual
import datetime
#import pprint

##### bybit key #####

session = usdt_perpetual.HTTP(
    endpoint="https://api.bybit.com", 
    api_key="iX7k37KXnQjwBzGZhd", 
    api_secret="srUkMMdV6LowHORthjqdNM2pkH8fI5VCjEVF" 
)

now = datetime.datetime.utcnow()
price_now = session.public_trading_records(symbol='BTCUSDT', limit=1)['result'][0]['price']
price_long = price_now - 1000
price_short = price_now + 1000
leverage = 100
tp =1.5
sl =0.06

### 기본 세팅 ###

USDT = session.get_wallet_balance(coin="USDT")['result']['USDT']['available_balance'] # USDT 보유량
position_size_short = session.my_position(symbol='BTCUSDT')['result'][1]['size'] # BTCUSDT short 구매량
position_size_long = session.my_position(symbol='BTCUSDT')['result'][0]['size'] # BTCUSDT long 구매량

position_average_short = session.my_position(symbol='BTCUSDT')['result'][1]['entry_price'] # BTCUSDT short average position price
position_average_long = session.my_position(symbol='BTCUSDT')['result'][0]['entry_price'] # BTCUSDT long average position price

position_leverage_short = session.my_position(symbol='BTCUSDT')['result'][1]['leverage'] # BTCUSDT short 레버리지
position_leverage_long = session.my_position(symbol='BTCUSDT')['result'][0]['leverage'] # BTCUSDT long 레버리지

BTCUSDT_now = float(session.latest_information_for_symbol(symbol='BTCUSDT')['result'][0]['last_price']) # BTCUSDT 현재 가격

min_price = BTCUSDT_now
max_price = BTCUSDT_now
    
if position_size_short ==0:
    trade_state_bybit =1 # 매도상태
else:
    trade_state_bybit =0 # short open 상태
if position_size_long !=0:
    trade_state_bybit = 2 # long open 상태     

### 출력하기 ###

resp = session.place_active_order(
    symbol="BTCUSDT",
    side='Buy',
    order_type="Limit",
    qty=0.01,
    price=price_long,
    time_in_force="GoodTillCancel",
    reduce_only=False,
    close_on_trigger=False,
    take_profit=round( price_long * ( 1 + tp / leverage)),
    stop_loss=round( price_long * ( 1 - sl / leverage))
)

resp = session.place_active_order(
    symbol="BTCUSDT",
    side='Sell',
    order_type='Limit',
    qty=0.01,
    price=price_short,
    time_in_force="GoodTillCancel",
    reduce_only=False,
    close_on_trigger=False,
    take_profit=round( price_short * ( 1 - tp / leverage)),
    stop_loss=round( price_short * ( 1 + sl / leverage))
)



#print("auto trade start :", USDT, position_size_short, position_size_long, BTCUSDT_now, trade_state_bybit)