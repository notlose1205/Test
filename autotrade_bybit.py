from pybit.usdt_perpetual import HTTP
import pandas as pd
import time
from datetime import datetime
import calendar
import smtplib 
from email.mime.text import MIMEText
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
USDT = session.get_wallet_balance(coin="USDT")['result']['USDT']['available_balance'] # USDT 보유량
position_average_short = session.my_position(symbol='BTCUSDT')['result'][1]['entry_price'] # BTCUSDT short average position price
position_average_long = session.my_position(symbol='BTCUSDT')['result'][0]['entry_price'] # BTCUSDT long average position price
position_leverage_short = session.my_position(symbol='BTCUSDT')['result'][1]['leverage'] # BTCUSDT short 레버리지
position_leverage_long = session.my_position(symbol='BTCUSDT')['result'][0]['leverage'] # BTCUSDT long 레버리지
BTCUSDT_now = float(session.latest_information_for_symbol(symbol='BTCUSDT')['result'][0]['last_price']) # BTCUSDT 현재 가격
#### autotrade ####
pre_price5_0 = BTCUSDT_now
pre_price5_1 = BTCUSDT_now
pre_price5_2 = BTCUSDT_now
pre_price5_3 = BTCUSDT_now
pre_price5_4 = BTCUSDT_now
pre_price5_5 = BTCUSDT_now
pre_price15_0 = BTCUSDT_now
pre_price15_1 = BTCUSDT_now
pre_price15_2 = BTCUSDT_now
pre_price15_3 = BTCUSDT_now
pre_price15_4 = BTCUSDT_now
pre_price15_5 = BTCUSDT_now
now = datetime.now()
pre_minute = now.minute
short_open_ready = 0
long_open_ready =0
while True:
    BTCUSDT_now = float(session.latest_information_for_symbol(symbol='BTCUSDT')['result'][0]['last_price']) # BTCUSDT 현재 가격
    now = datetime.now()
    period_5 = now.minute % 5
    period_15 = now.minute % 15
    if period_5 == 0 and now.second < 2 :
        pre_price5_5 = pre_price5_4
        pre_price5_4 = pre_price5_3
        pre_price5_3 = pre_price5_2
        pre_price5_2 = pre_price5_1
        pre_price5_1 = pre_price5_0
        pre_price5_0 = BTCUSDT_now
        delta_price5_1 = pre_price5_0 - pre_price5_1
        delta_price5_2 = pre_price5_1 - pre_price5_2
        delta_price5_3 = pre_price5_2 - pre_price5_3
        delta_price5_4 = pre_price5_3 - pre_price5_4
        delta_price5_5 = pre_price5_4 - pre_price5_5          
    delta_price5_0 = BTCUSDT_now - pre_price5_0
    if period_15 == 0 and now.second < 2 :
        pre_price15_5 = pre_price15_4
        pre_price15_4 = pre_price15_3
        pre_price15_3 = pre_price15_2
        pre_price15_2 = pre_price15_1
        pre_price15_1 = pre_price15_0
        pre_price15_0 = BTCUSDT_now
        delta_price15_1 = pre_price15_0 - pre_price15_1
        delta_price15_2 = pre_price15_1 - pre_price15_2
        delta_price15_3 = pre_price15_2 - pre_price15_3
        delta_price15_4 = pre_price15_3 - pre_price15_4
        delta_price15_5 = pre_price15_4 - pre_price15_5         
    delta_price15_0 = BTCUSDT_now - pre_price15_0
    position_average_short = session.my_position(symbol='BTCUSDT')['result'][1]['entry_price'] # BTCUSDT short average position price
    position_average_long = session.my_position(symbol='BTCUSDT')['result'][0]['entry_price'] # BTCUSDT long average position price
    position_size_short = session.my_position(symbol='BTCUSDT')['result'][1]['size'] # BTCUSDT short 구매량
    position_size_long = session.my_position(symbol='BTCUSDT')['result'][0]['size'] # BTCUSDT long 구매량
    if position_size_short == 0:
        if position_size_long == 0:
            trade_state_bybit = 0 # no position
        else:
            trade_state_bybit = 1 # long posiont only
    else:
        if position_size_long == 0:
            trade_state_bybit = 2 # short position only
        else:
            trade_state_bybit = 3 # both position
    if trade_state_bybit == 0 : # no position
        if abs(delta_price15_0) > 50 :
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
            msg = MIMEText('현재가 : ' + str(BTCUSDT_now) + '\n15분봉에서 50point 이상 변화가 감지되었습니다. ' + str( datetime.now()))
            msg['Subject'] = '제목 : 15분봉에서 급격한 변동 신호가 잡혔습니다.'
            s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
            s.quit()
            time.sleep(30)
        if trade_state_bybit == 0 and short_open_ready == 0 : 
            if rsi_bybit(5) < 30 :
                if rsi_bybit(15) <30 :
                    short_open_ready =1
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
                    msg = MIMEText('현재가 : '  + str(BTCUSDT_now) + '\n과매도 구간에 진입했으니 long를 고려하세요.' + str( datetime.now()))
                    msg['Subject'] = '제목 : 과매도 신호가 잡혔습니다.'
                    s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
                    s.quit()
        if trade_state_bybit == 0 and long_open_ready == 0 : 
            if rsi_bybit(5) > 70 :
                if rsi_bybit(15) > 70 :
                    long_open_ready =1
                    short_open_ready =1
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
                    msg = MIMEText('현재가 : ' + str(BTCUSDT_now) + '\n과매수 구간에 진입했으니 short를 고려하세요.' + str( datetime.now()))
                    msg['Subject'] = '제목 : 과매수 신호가 잡혔습니다.'
                    s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
                    s.quit()
        if long_open_ready == 0 and short_open_ready == 0 and period_15 == 0 and now.second < 2 :
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
            msg = MIMEText(str(BTCUSDT_now) + '\n아직 position을 잡지 못했습니다.' + str( datetime.now()))
            msg['Subject'] = '제목 : no position notice'
            s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
            s.quit()
        if long_open_ready == 1 and delta_price15_1 > 0 :
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
            msg = MIMEText('현재가 : ' + str(BTCUSDT_now) + ' \n적극적으로 long position을 잡을 것을 고려하세요.' + str( datetime.now()))
            msg['Subject'] = '제목 : long position notice'
            s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
            s.quit()
        if short_open_ready ==1 and delta_price15_1 < 0 :
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
            msg = MIMEText('현재가 : ' + str(BTCUSDT_now) + ' \n적극적으로 short position을 잡을 것을 고려하세요.' + str( datetime.now()))
            msg['Subject'] = '제목 : short position notice'
            s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
            s.quit()
    if trade_state_bybit == 1 : # long position
        if abs(delta_price15_0) > 30 :
            unrealized_Pnl_long = session.my_position(symbol='BTCUSDT')['result'][0]['unrealised_pnl'] # BTCUSDT long unrelaized_pnl
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
            msg = MIMEText('Unrealized P/L :' + str(unrealized_Pnl_long) + '\n현재가 : ' + str(BTCUSDT_now) + '\n' + str(round(position_average_long,1)) + '에 long postion을 ' + str(position_size_long) + '보유중입니다.' + '\n' + str( datetime.now()))
            msg['Subject'] = '제목 : 15분봉에서 급격한 변동 신호가 잡혔습니다.'
            s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
            s.quit()
            time.sleep(30)
        else :
            if period_15 == 0 and now.second < 2 :
                unrealized_Pnl_long = session.my_position(symbol='BTCUSDT')['result'][0]['unrealised_pnl'] # BTCUSDT long unrelaized_pnl
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
                msg = MIMEText('Unrealized P/L :' + str(unrealized_Pnl_long) + '\n현재가 : ' + str(BTCUSDT_now) + '\n' + str(round(position_average_long,1)) + '에 long postion을 ' + str(position_size_long) + '보유중입니다.' + '\n' + str( datetime.now()))
                msg['Subject'] = '제목 : long position notice.'
                s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
                s.quit()
    if trade_state_bybit == 2 : # short position  
        if abs(delta_price15_0) > 30 :
            unrealized_Pnl_short = session.my_position(symbol='BTCUSDT')['result'][1]['unrealised_pnl'] # BTCUSDT short unrelaized_pnl
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
            msg = MIMEText('Unrealized P/L :' + str(unrealized_Pnl_short)  + '\n현재가 : ' + str(BTCUSDT_now) + '\n' + str(round(position_average_short,1)) + '에 short postion을 ' + str(position_size_short) + '보유중입니다.' + '\n' + str( datetime.now()))
            msg['Subject'] = '제목 : 15분봉에서 급격한 변동 신호가 잡혔습니다.'
            s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
            s.quit()
            time.sleep(30)
        else :
            if period_15 == 0 and now.second < 2 :
                unrealized_Pnl_short = session.my_position(symbol='BTCUSDT')['result'][1]['unrealised_pnl'] # BTCUSDT short unrelaized_pnl
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
                msg = MIMEText('Unrealized P/L :' + str(unrealized_Pnl_short) +'\n현재가 : ' + str(BTCUSDT_now) + '\n' + str(round(position_average_short,1)) + '에 short postion을 ' + str(position_size_short) + '보유중입니다.'  + '\n' + str( datetime.now()))
                msg['Subject'] = '제목 : short position notice.'
                s.sendmail("inhosuh2@gmail.com", "inhosuh2@gmail.com", msg.as_string())
                s.quit()
    time.sleep(2)

