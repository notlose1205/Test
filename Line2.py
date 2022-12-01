from pybit.usdt_perpetual import HTTP
import pandas as pd
import time
from datetime import datetime
import calendar
import requests

##### bybit key #####
session = HTTP(
    endpoint="https://api.bybit.com", 
    api_key="iX7k37KXnQjwBzGZhd", 
    api_secret="srUkMMdV6LowHORthjqdNM2pkH8fI5VCjEVF"
)
##### RSI #####
def rsi_bybit(itv, symbol='BTCUSDT'):
    now = datetime.utcnow()
    unixtime = calendar.timegm(now.utctimetuple())
    since = unixtime-itv*60*200;
    response=session.query_kline(symbol='BTCUSDT',interval=str(itv),**{'from':since})['result']
    df = pd.DataFrame(response)
    rsi=rsi_calc(df,14).iloc[-1]
    rsi=round(rsi,2)
    return rsi
def rsi_calc(ohlc: pd.DataFrame, period: int = 14):
    ohlc = ohlc['close'].astype(float)
    delta = ohlc.diff()
    gains, declines = delta.copy(), delta.copy()
    gains[gains < 0] = 0
    declines[declines > 0] = 0
    _gain = gains.ewm(com=(period-1), min_periods=period).mean()
    _loss = declines.abs().ewm(com=(period-1), min_periods=period).mean()
    RS = _gain / _loss
    return pd.Series(100-(100/(1+RS)), name="RSI") 
##### States #####

position_leverage_short = session.my_position(symbol='BTCUSDT')['result'][1]['leverage'] # BTCUSDT short 레버리지
position_leverage_long = session.my_position(symbol='BTCUSDT')['result'][0]['leverage'] # BTCUSDT long 레버리지

def balance():
    balance = session.get_wallet_balance(coin="USDT")['result']['USDT']['available_balance'] # USDT 보유량
    return balance
def price():
    price_now = float(session.latest_information_for_symbol(symbol='BTCUSDT')['result'][0]['last_price']) # BTCUSDT 현재 가격
    return price_now
def size(x): # x=0 ; long, x=1 ; short
    position_size = session.my_position(symbol='BTCUSDT')['result'][x]['size']
    return position_size
def sendLine(content):
    now = datetime.now()
    try:
        TARGET_URL = 'https://notify-api.line.me/api/notify'
        TOKEN = 'yDUSKahXXt8Jr63GJ2eVMtekTB05EChUrPIZwk6b3CY' #'odbC9PrCtew1vMLA5qKQVJ71MbH882u9F1yTAFxjWR6'
        response = requests.post(
            TARGET_URL,
            headers={'Authorization': 'Bearer ' + TOKEN},
            data={'message':'\n현재가 : ' + str(price()) + '\n'+ content + '\n' +str( now.strftime('%Y.%m.%d - %H:%M:%S'))}
            )
    except Exception as ex:
            print(ex)
def entry_price(x) : # x=0 ; long, x=1 ; short
    entry_price = session.my_position(symbol='BTCUSDT')['result'][x]['entry_price'] # BTCUSDT average position price
    return entry_price
def unrealized(x) : # x=0 ; long, x=1 ; short
    unrealized = session.my_position(symbol='BTCUSDT')['result'][x]['unrealised_pnl'] # BTCUSDT short unrelaized_pnl
    return unrealized
short_open_ready = 0; long_open_ready =0; eventnotice = 0 # 변수의 초기값 설정
pre_price_1 = [ price(),price(),price(),price(),price() ]
pre_price_5 = [ price(),price(),price(),price(),price() ]; delta_price_5 = [0,0,0,0,0]
pre_price_15 = [ price(),price(),price(),price(),price() ]; delta_price_15 = [0,0,0,0,0]

sendLine('\nUnrealized P/L :' + str(unrealized(1))+'\n미실현 손익이 존재합니다. ')
