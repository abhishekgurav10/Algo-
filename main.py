
# import pymongo

# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["praticeDB"]
# collection = db["strike_price"]

hedges = int(input("Enter the hedge: "))

if hedges == 0:
    print("Enter the 1")
    # Fetch and process options data
    # from statergy import *
    # options_df = fetch_options_data()
    # ATM_0, ATM_1, Trading_symbols_0, Trading_symbols_1 = process_options_data(options_df)
    # time.sleep(2)
    # print("ATM_0:", ATM_0)
    # print("ATM_1:", ATM_1)
    # print("Trading_symbols_0:", Trading_symbols_0)
    # print("Trading_symbols_1:", Trading_symbols_1)
    # data_to_insert = {
    #     "ATM_0": ATM_0,
    #     "ATM_1": ATM_1,
    #     "Trading_symbols_0": Trading_symbols_0,
    #     "Trading_symbols_1": Trading_symbols_1
    # }
    # collection.insert_one(data_to_insert)

    # Call the place_order function for each trading symbol
    # place_order(Trading_symbols_0)
    # place_order(Trading_symbols_1)
    # ATM_0 = "43987" 
    # ATM_1 = "43530"
    # Trading_symbols_0 = "BANKNIFTY2450852100CE"
    # Trading_symbols_1 = "BANKNIFTY2450845100PE"
    # time.sleep(2)
    # print('Average buying price of position')
    # avg_prices = get_positions()
    # print(avg_prices)
    # insert = {"avg_price":avg_prices}
    # collection.insert_one(insert)
    # subscribe(ATM_0, ATM_1)
    # webstock(avg_prices, ATM_0, ATM_1, Trading_symbols_0, Trading_symbols_1)
if hedges == 1:

    import datetime
    import time
    from Hedges_1 import * 

    def main():
        # run this on 9:10:0 
        # quantities = get_quantity()
        # stoploss_value = stoploss()
        # options_df = fetch_options_data()
        # ATM_CE, ATM_PE, Trading_symbols_0, Trading_symbols_1, Hedges_CE, Hedges_PE, Trading_symbols_2, Trading_symbols_5 = process_options_data(options_df)

        # print("ATM_CE:", ATM_CE)
        # print("ATM_PE:", ATM_PE)
        # print("Hedges_CE:", Hedges_CE)
        # print("Hedges_PE:", Hedges_PE)
        # print("Trading_symbols_0:", Trading_symbols_0)
        # print("Trading_symbols_1:", Trading_symbols_1)
        # print("Trading_symbols_2:", Trading_symbols_2)
        # print("Trading_symbols_5:", Trading_symbols_5)
        # timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # data = {
        #     'ATM_CE': ATM_CE,
        #     'ATM_PE': ATM_PE,
        #     'Hedges_CE': Hedges_CE,
        #     'Hedges_PE': Hedges_PE,
        #     'Trading_symbols_0': Trading_symbols_0,
        #     'Trading_symbols_1': Trading_symbols_1,
        #     'Trading_symbols_2': Trading_symbols_2,
        #     'Trading_symbols_5': Trading_symbols_5
        # }
        # # Use a Redis hash to store the data
        # r.hmset(f"options_data:{timestamp}", data)
        # r.lpush("options_data_timestamps", f"options_data:{timestamp}")

        # # we run this loop to get the got run on the price we have decided 
        # while True:
        #     current_time = datetime.datetime.now().time()
        #     print(f"Current time: {current_time}")
            
        #     if current_time.hour == 22 and current_time.minute == 30 and current_time.second == 10:
        #         place_buy_orders(Trading_symbols_0, Trading_symbols_5)
                
        #         buy_order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #         r.lpush("buy_order_times", buy_order_time)
        #         print(f"Buy orders placed at {buy_order_time}")

        #         time.sleep(10)  # Ensure buy orders are placed before sell orders
        #         place_sell_orders_in_chunks(Trading_symbols_1, Trading_symbols_2)
                
        #         sell_order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #         r.lpush("sell_order_times", sell_order_time)
        #         print(f"Sell orders placed at {sell_order_time}")
        #         break

        #     # Sleep for a short interval to avoid excessive CPU usage
        #     time.sleep(1)
        # time should be 16:00 to 16:30
        # when we run this fucntion we the tradign symbol and token so it the output should be displayed in the front-end
        ORDER()
        time.sleep(2)
        # time should be around 16:00 to 16:30
        # over here we get the average price of the trade we have took we should be able to display this prices as well  
        avg_prices = get_positions()
        print(avg_prices)
        
        avg_prices = get_positions()
        # avg_prices = {
        #                 "36884": {"avgPrice": 20, "position": "buy"},
        #                 "36357": {"avgPrice": 30, "position": "buy"},
        #                 "36920": {"avgPrice": 100, "position": "sell"},
        #                 "36341": {"avgPrice": 110, "position": "sell"}
        #     }
        ATM_0, ATM_1, HED_0, HED_1, Trading_symbols_0, Trading_symbols_1, Trading_symbols_2, Trading_symbols_3 = ORDER()
        # ATM_0 = "36884" 
        # ATM_1 = "36357"
        # HED_0 = "36920"
        # HED_1 = "36341"
        # Trading_symbols_0 = "FINFTY2461124000C"
        # Trading_symbols_1 = "FINFTY2461120100P"
        # Trading_symbols_2 = "FINFTY2461124100C"
        # Trading_symbols_3 = "FINFTY2461120000P"
        webstock(avg_prices, ATM_0, ATM_1, HED_0, HED_1, Trading_symbols_0, Trading_symbols_1, Trading_symbols_2, Trading_symbols_3)
        

    if __name__ == "__main__":
        main()

    