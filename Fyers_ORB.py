import time
from fyers_api import fyersModel
from datetime import datetime
from Fyers_Auth import *
import os

client_id = '' # You will get this from Fyers API app. Same as app ID.

check()
access_token = read_file()
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, log_path=os.getcwd())

symbols = ["NSE:SBIN-EQ","NSE:KOTAKBANK-EQ","NSE:JSWSTEEL-EQ","NSE:GRASIM-EQ","NSE:IOC-EQ"
           ,"NSE:EICHERMOT-EQ","NSE:TATASTEEL-EQ","NSE:AXISBANK-EQ","NSE:HDFCBANK-EQ","NSE:BPCL-EQ","NSE:ADANIPORTS-EQ","NSE:BAJAJ-AUTO-EQ"
           ,"NSE:ICICIBANK-EQ","NSE:ONGC-EQ","NSE:M&M-EQ","NSE:HEROMOTOCO-EQ",
           "NSE:HINDUNILVR-EQ","NSE:LT-EQ","NSE:CIPLA-EQ","NSE:RELIANCE-EQ","NSE:COALINDIA-EQ","NSE:BHARTIARTL-EQ",
           "NSE:UPL-EQ","NSE:ITC-EQ","NSE:HDFCLIFE-EQ","NSE:TATAMOTORS-EQ","NSE:INDUSINDBK-EQ"
           ,"NSE:HDFC-EQ","NSE:SBILIFE-EQ","NSE:HINDALCO-EQ","NSE:TITAN-EQ","NSE:SUNPHARMA-EQ","NSE:TCS-EQ","NSE:NTPC-EQ","NSE:TATACONSUM-EQ"
           ,"NSE:POWERGRID-EQ","NSE:WIPRO-EQ","NSE:HCLTECH-EQ","NSE:INFY-EQ","NSE:TECHM-EQ"]

def data_handling(symbol):
    date = datetime.today().strftime('%Y-%m-%d')
    hist_data = {"symbol":symbol,"resolution":"15","date_format":1,"range_from":date,"range_to":date,"cont_flag":"1"}
    srp = fyers.history(hist_data)
    hl_data = srp["candles"][0]
    high = hl_data[2]
    low = hl_data[3]
    print("High:",high,"  ","Low:",low)
    return high, low
    

def place_orders(symbol,h,l):
    df = {"symbols":symbol}
    var = fyers.quotes(df)["d"]
    ltp = var[0]["v"]['lp']F
    print("LTP:",ltp)
    if ltp>h:
        data = {"symbol":symbol,"qty":1,"type":2,"side":1,"productType":"CO",
                "limitPrice":0,"stopPrice":0,"validity":"DAY","disclosedQty":0,"offlineOrder":"False",  "stopLoss":l-1,"takeProfit":0}
        response = fyers.place_order(data)
        print("Placing buy market cover order!")
        print("Response:",response["s"] , "\n"+"Message:",response["message"])
    elif ltp<l:
        data = {"symbol":symbol,"qty":1,"type":2,"side":-1,"productType":"CO",
        "limitPrice":0,"stopPrice":0,"validity":"DAY","disclosedQty":0,"offlineOrder":"False",  "stopLoss":h+1,"takeProfit":0}
        response = fyers.place_order(data)
        print("Placing sell market cover order!")
        print("Response:",response["s"] , "\n"+"Message:",response["message"])
    else:
        print("Price between Opening Range High and Low!")
    
start = "09:30:00"    
end = "15:30:00"
now = datetime.strftime(datetime.now(),"%H:%M:%S")

run = True if ((now>start) & (now<end)) else False

if run==False and now<start:
    x = True
    while x:
        print("Waiting for market to open")
        time.sleep(60)
        now = datetime.strftime(datetime.now(),"%H:%M:%S")
        x = True if now<start else False
    run = True
    

while run:
    print("\nCurrent time","   ",now)
    for i in symbols:
        print("\n"+i)
        h,l = data_handling(i)
        place_orders(i,h,l)
    time.sleep(300)
    now = datetime.strftime(datetime.now(),"%H:%M:%S")
    run = True if ((now>start) & (now<end)) else False

if now>end:
    print("\nMarket Closed!")

    
    
