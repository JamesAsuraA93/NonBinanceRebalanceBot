import os
import ccxt
import time
import json
import datetime



def running():
  now = datetime.datetime.now()
  file = open('config.json')
  config = json.load(file)
  fix = int(config['fix']) # 75
  fee = int(config['rebal']) # 7
  top = (fix+fee) - 1  # 82 (-1) = 81
  bottom = (fix-fee) + 1  # 68 (+1) = 69

  my_API = os.environ['API']
  my_secret = os.environ['Secret']
  


  bn = ccxt.binance({
    'api_key': my_API,  # API Keys
    'secret': my_secret,  # API Secret
    'enableRateLimit': True,
  })

  C98_info = bn.fetch_tickers('C98/BUSD')
  Balance = bn.fetchBalance()

  C98 = C98_info['C98/BUSD']['last']  # ราคา C98 ต่อ BUSD ล่าสุด  
  C98_V = Balance['C98']['free']  # จำนวน C98 ที่มีในกระเป๋า     
  V_C98 = C98 * C98_V  # จำนวน C98 ต่อ BUSD ที่มี $   
  BUSD_V = Balance['BUSD']['free']

  s,h,m,d,mth = now.second,now.hour,now.minute,now.day,now.month

  t,b = top,bottom
  GMT = 7
  temp = (h+GMT) // 24
  h += GMT
  if h > 24:
    h -= 24
  else:
    pass
  d += temp
  if V_C98 > t:  # V > 82 - 1
    orderSell = (10/C98)+0.13
    bn.create_market_sell_order('C98/BUSD',orderSell)
    print(f"SELL C98 @Marketprice {orderSell}$")
    print(f"ราคา C98 = {C98}")
    print(f"จำนวน C98 ที่มี = {C98_V}")
    print(f"C98 รวมแล้วมี {V_C98} ~$")
    print(f"BUSD รวมแล้วมี {BUSD_V} ~$")
    print(f"วันเวลา {h}:{m}:{s} วันที่ {d} เดือน {mth}")
    print("\r")
    time.sleep(2)
  
  elif V_C98 < b:  # V < 68 + 1
    orderBuy = (10/C98)+0.13
    bn.create_market_buy_order('C98/BUSD',orderBuy)
    print(f"BUY C98 @Marketprice {orderBuy}$")
    print(f"ราคา C98 = {C98}")
    print(f"จำนวน C98 ที่มี = {C98_V}")
    print(f"C98 รวมแล้วมี {V_C98} ~$")
    print(f"BUSD รวมแล้วมี {BUSD_V} ~$")
    print(f"วันเวลา {h}:{m}:{s} วันที่ {d} เดือน {mth}")
    print("\r")
    time.sleep(2)
  else:
    print("นั่งทับมือ")
    print(f"ราคา C98 = {C98}")
    print(f"C98 รวมแล้วมี {V_C98} ~$")
    print(f"วันเวลา {h}:{m}:{s} วันที่ {d} เดือน {mth}")
    print("\r")
