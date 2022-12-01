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

def price():
    price_now = float(session.latest_information_for_symbol(symbol='BTCUSDT')['result'][0]['last_price']) # BTCUSDT 현재 가격
    return price_now


def sendMail(content, subject):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('inhosuh2@gmail.com', 'gzkhsszlvisozhya')
    msg = MIMEText('현재가 : ' + str(price()) + content + str( datetime.now()))
    msg['Subject'] = subject
    s.sendmail("inhosuh2@gmail.com", "suhinho76@gmail.com", msg.as_string())
    s.quit()

sendMail('\n메일이 잘 가는지 확인바랍니다.\n', '제목 : Test Mail')

