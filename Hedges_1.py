from login_details import client
import pandas as pd
from dateutil.relativedelta import relativedelta
import datetime
import time
from threading import Thread, Lock
from neo_api_client import NeoAPI
import pymongo
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
redis_client = redis.Redis(host='localhost', port=6379, db=0)
consumer_key = 
consumer_secret = 
mobilenumber = 
password = 
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["practiceDB"]
pnl_collection = db["PnL"]

live_data = {}
lock = Lock()

def get_quantity():
    qty_A = input("Enter the quantity you want to trade in ATM: ")
    qty_H = input("Enter the quantity of hedges: ")
    qty_ATM = int(qty_A)
    qty_Hedges = int(qty_H)

    # Store the quantities in Redis
    r.set('qty_ATM', qty_ATM)
    r.set('qty_Hedges', qty_Hedges)
    
    print(f"Stored qty_ATM: {qty_ATM} and qty_Hedges: {qty_Hedges} in Redis")
    
    return qty_A, qty_ATM, qty_Hedges, qty_H

# quantity = qt()
# print(f"quantity = \"{quantity}\"")


def stoploss():
    value = input("Enter the stoploss value: ")
    stoploss_value = -int(value)

    # Store the stoploss value in Redis
    r.set('stoploss', stoploss_value)
    
    print(f"Stored stoploss value: {stoploss_value} in Redis")
    
    return stoploss_value

def fetch_options_data():
    options_data = client.scrip_master(exchange_segment="NFO")  
    df = pd.read_csv(options_data)
    return df

def process_options_data(options_df):
    options_df.columns = [c.strip() for c in options_df.columns]
    options_df['lExpiryDate'] = pd.to_datetime(options_df['lExpiryDate']).apply(lambda x: x.date() + relativedelta(years=10))
    
    strike_price_input = input("Enter the strike price (comma-separated for multiple values): ")
    strike_prices = [int(x.strip()) for x in strike_price_input.split(",")]

    dynamic_part = input("Enter the dynamic part of the symbol (e.g., 703): ")

    # Construct the full symbol string
    full_symbol = f"BANKNIFTY24{dynamic_part}"
    strike_prices = [int(x.strip()) for x in strike_price_input.split(",")]

    filtered_data = options_df[(options_df['pInstType'] == "OPTIDX") & 
                            (options_df['pTrdSymbol'].str.startswith(full_symbol)) & 
                            (options_df['dStrikePrice;'].isin(strike_prices))]

    symbols = filtered_data[['pSymbol', 'pTrdSymbol']].iloc[:5]
    
    Hedges_CE = symbols.iloc[4]['pSymbol']
    Hedges_PE = symbols.iloc[1]['pSymbol']
    ATM_CE = symbols.iloc[2]['pSymbol']
    ATM_PE = symbols.iloc[3]['pSymbol']
    Trading_symbols_0 = symbols.iloc[1]['pTrdSymbol']
    Trading_symbols_1 = symbols.iloc[2]['pTrdSymbol']
    Trading_symbols_2 = symbols.iloc[3]['pTrdSymbol']
    Trading_symbols_5 = symbols.iloc[4]['pTrdSymbol']
    
    return ATM_CE, ATM_PE, Trading_symbols_0, Trading_symbols_1, Hedges_CE, Hedges_PE, Trading_symbols_2, Trading_symbols_5

def place_order(trading_symbol, quantity, transaction_type):
    client.place_order(
        exchange_segment='nse_fo',
        product='NRML',
        price='0',
        order_type='MKT',
        quantity=quantity,
        validity='DAY',
        trading_symbol=trading_symbol,
        transaction_type=transaction_type,
        amo="NO",
        disclosed_quantity="0",
        market_protection="0",
        pf="N",
        trigger_price="0",
        tag=None
    )

def place_buy_orders(Trading_symbols_0, Trading_symbols_5):
    place_order(Trading_symbols_0, "30", 'B')
    place_order(Trading_symbols_5, "30", 'B')

def place_sell_orders_in_chunks(Trading_symbols_1, Trading_symbols_2):
    for quantity in ["30", "15"]:
        place_order(Trading_symbols_1, quantity, 'S')
        place_order(Trading_symbols_2, quantity, 'S')
        print(f"Sell orders placed ({quantity} units). Waiting for 10 seconds...")
        time.sleep(10)
    
    print("Second sell orders placed (60 units).")

def ORDER():
    data = client.positions()
    positions = data['data']

    ATM_0 = positions[1]['tok']
    ATM_1 = positions[2]['tok']
    HED_0 = positions[0]['tok']
    HED_1 = positions[3]['tok']

    Trading_symbols_0 = positions[1]['trdSym']
    Trading_symbols_1 = positions[2]['trdSym']
    Trading_symbols_2 = positions[0]['trdSym']
    Trading_symbols_3 = positions[3]['trdSym']

    # Print the results in the desired format
    print(f"ATM_0 = \"{ATM_0}\"")
    print(f"ATM_1 = \"{ATM_1}\"")
    print(f"HED_0 = \"{HED_0}\"")
    print(f"HED_1 = \"{HED_1}\"")
    print(f"Trading_symbols_0 = \"{Trading_symbols_0}\"")
    print(f"Trading_symbols_1 = \"{Trading_symbols_1}\"")
    print(f"Trading_symbols_2 = \"{Trading_symbols_2}\"")
    print(f"Trading_symbols_3 = \"{Trading_symbols_3}\"")
    return ATM_0, ATM_1, HED_0, HED_1, Trading_symbols_0, Trading_symbols_1, Trading_symbols_2, Trading_symbols_3

def get_positions():
    pos_data = client.positions()  
    data = []
    for item in pos_data['data']:
        flBuyQty = int(item['flBuyQty'])
        flSellQty = int(item['flSellQty'])
        multiplier = int(item['multiplier'])
        genNum = int(item['genNum'])
        genDen = int(item['genDen'])
        prcNum = int(item['prcNum'])
        prcDen = int(item['prcDen'])
        precision = int(item['precision'])
        
        if flBuyQty > flSellQty:
            avgPrice = float(item['buyAmt']) / (
                flBuyQty * multiplier * (genNum / genDen) * (prcNum / prcDen)
            )
            position = 'buy'
        elif flBuyQty < flSellQty:
            avgPrice = float(item['sellAmt']) / (
                flSellQty * multiplier * (genNum / genDen) * (prcNum / prcDen)
            )
            position = 'sell'
        else:
            avgPrice = 0
            position = 'none'
        
        data.append({
            "symbol": item['tok'],
            "avgPrice": round(avgPrice, precision) if avgPrice != 0 else 0,
            "position": position,
            "precision": precision
        })

    # Create a dictionary of average prices keyed by symbol
    avg_prices = {item["symbol"]: {"avgPrice": item["avgPrice"], "position": item["position"]} for item in data}

    return avg_prices


mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["practiceDB"]

# Create a collection for storing PnL values
pnl_collection = db["PnL"]
lock = Lock()
live_data = {}

def on_message(message):
    global live_data
    try:
        print("Received message:", message)
        with lock:
            if 'data' in message:
                for data_item in message['data']:
                    if 'tk' in data_item and 'ltp' in data_item:
                        # Convert 'ltp' to float and update live_data
                        live_data[data_item['tk']] = float(data_item['ltp'])
    except Exception as e:
        print('Exception occurred in on_message:', e)

def on_error(message):
    result = message
    print('[OnError]: ', result)

def on_close(message):
    print('[OnClose]: ', message)

def subscribe(ATM_0, ATM_1, HED_0, HED_1):
    global live_data
    trading_client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, environment="prod", access_token=None, neo_fin_key=None)

    trading_client.login(mobilenumber=mobilenumber, password=password)
    MPIN = 
    trading_client.session_2fa(OTP=MPIN)

    trading_client.on_message = on_message
    trading_client.on_error = on_error
    trading_client.on_close = on_close  # called when websocket connection is closed

    # Subscribe to instrument tokens
    trading_client.subscribe(instrument_tokens=[
        {"instrument_token": ATM_0, "exchange_segment": "nse_fo"},
        {"instrument_token": ATM_1, "exchange_segment": "nse_fo"},
        {"instrument_token": HED_0, "exchange_segment": "nse_fo"},
        {"instrument_token": HED_1, "exchange_segment": "nse_fo"}
    ], isIndex=False, isDepth=False)

def place_order(trading_symbol, quantity, transaction_type):
    client.place_order(
        exchange_segment='nse_fo',
        product='NRML',
        price='0',
        order_type='MKT',
        quantity=quantity,
        validity='DAY',
        trading_symbol=trading_symbol,
        transaction_type=transaction_type,
        amo="NO",
        disclosed_quantity="0",
        market_protection="0",
        pf="N",
        trigger_price="0",
        tag=None
    )


def webstock(avg_prices, ATM_0, ATM_1, HED_0, HED_1, Trading_symbols_0, Trading_symbols_1, Trading_symbols_2, Trading_symbols_3):
    qty_A, qty_ATM, qty_Hedges, qty_H = get_quantity()
    stoploss_value = stoploss()

    websocket_thread = Thread(target=subscribe, args=(ATM_0, ATM_1, HED_0, HED_1))
    websocket_thread.start()

    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["practiceDB"]
    collection = db["live_data"]

    symbol_pnl = {}
    order_placed = False

    trading_client = NeoAPI(consumer_key=consumer_key, consumer_secret=consumer_secret, environment="prod", access_token=None, neo_fin_key=None)
    trading_client.login(mobilenumber=mobilenumber, password=password)
    MPIN = 
    trading_client.session_2fa(OTP=MPIN)

    while True:
        print("Current live_data:", live_data)
        parsed_data = {"timestamp": datetime.datetime.now(), "data": live_data}
        collection.insert_one(parsed_data)
        current_time = datetime.datetime.now().time()

        for symbol, ltp in live_data.items():
            if symbol in avg_prices:
                avg_price = avg_prices[symbol]['avgPrice']
                position = avg_prices[symbol]['position']

                if position == 'buy':
                    pnl = (ltp - avg_price) * qty_Hedges
                else:
                    pnl = (avg_price - ltp) * qty_ATM

                symbol_pnl[symbol] = pnl
                print(f"PnL for {symbol} ({position}): {pnl:.2f}")

        total_pnl = sum(symbol_pnl.values())
        print(f"Combined PnL: {total_pnl:.2f}")
        combined_pnl_document = {
            "timestamp": datetime.datetime.now(),
            "total_pnl": round(total_pnl, 2)
        }
        pnl_collection.insert_one(combined_pnl_document)
        redis_client.publish('total_pnl_channel', round(total_pnl, 2))

        if total_pnl <= stoploss_value and not order_placed:
            orders_to_place = []
            
            def prepare_orders(trading_symbol, qty_H, qty_A):
                position = avg_prices.get(trading_symbol, {}).get('position')
                if position == 'sell':
                    orders_to_place.append(('buy', trading_symbol, qty_A))
                    orders_to_place.append(('sell', trading_symbol, qty_A))
                elif position == 'buy':
                    orders_to_place.append(('sell', trading_symbol, qty_H))

            prepare_orders(Trading_symbols_0, qty_H, qty_A)
            prepare_orders(Trading_symbols_1, qty_H, qty_A)
            prepare_orders(Trading_symbols_2, qty_H, qty_A)
            prepare_orders(Trading_symbols_3, qty_H, qty_A)

            for transaction_type, symbol, quantity in orders_to_place:
                place_order(symbol, quantity, transaction_type)
            
            order_placed = True
            print("Stoploss triggered. Orders placed.")
            break
        elif current_time.hour == 15 and current_time.minute == 29 and current_time.second == 20:
            orders_to_place = []

            prepare_orders(Trading_symbols_0, qty_H, qty_A)
            prepare_orders(Trading_symbols_1, qty_H, qty_A)
            prepare_orders(Trading_symbols_2, qty_H, qty_A)
            prepare_orders(Trading_symbols_3, qty_H, qty_A)

            for transaction_type, symbol, quantity in orders_to_place:
                place_order(symbol, quantity, transaction_type)

            print("Time reached (15:29:20)! Orders placed.")
            break

        time.sleep(0.5)

if __name__ == "__main__":
    ORDER()
    time.sleep(2)
    avg_prices = get_positions()
    ATM_0, ATM_1, HED_0, HED_1, Trading_symbols_0, Trading_symbols_1, Trading_symbols_2, Trading_symbols_3 = ORDER()
    webstock(avg_prices, ATM_0, ATM_1, HED_0, HED_1, Trading_symbols_0, Trading_symbols_1, Trading_symbols_2, Trading_symbols_3)