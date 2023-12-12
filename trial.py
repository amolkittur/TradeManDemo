#TODO System Wide Rules
#1 - All the non integer digits should be represented in 2 decimal places on all reports
#2 - Strategy name should be of format OvernightOptions across the entire code base including json files
#3 - All the base symbols should be in uppercase NIFTY
#4 - Strategy behaviour for order_tag in {strategy}.json file
#5 - Update the requirements.txt file



# import os, sys

# DIR_PATH = os.getcwd()
# sys.path.append(DIR_PATH)

# import Brokers.place_order as place_order
# from MarketUtils.InstrumentBase import Instrument


# order_details = {  
#         "strategy": "Extra",
#         "broker": "aliceblue",
#         "username": "vimala",
#         "base_symbol": "NIFTY",
#         "exchange_token" : 43083,     
#         "segment" : "NFO",
#         "transaction_type": "SELL",  
#         "order_type" : "Stoploss", 
#         "product_type" : "MIS",
#         "limit_prc" : 10.0,
#         "trigger_prc" : 10.5,
#         "order_mode" : [],
#         "trade_id" : "EXTRA1_entry",
#         "qty" : 50, 
#     }

# place_order.place_order_for_broker(order_details=order_details)
# # token = Instrument().get_segment_by_exchange_token(43083) 

# # print(token)

from enum import Enum
strategy_prefix_map = {
        'AmiPy': 'AP',
        'MPWizard': 'MP',
        'ExpiryTrader': 'ET',
        'OvernightFutures': 'OF'
    }

# class StrategyPrefix(Enum):
#     AmiPy = "AP"
#     MPWizard = "MP"
#     ExpiryTrader = "ET"
#     OvernightFutures = "OF"

class StrategyPrefix(Enum):
    AmiPy = "AP"
    MPWizard = "MP"
    ExpiryTrader = "ET"
    OvernightFutures = "OF"
    Extra = "EXTRA"
    Stock = "STOCK"
    
    @staticmethod
    def get_strategy_by_prefix(prefix):
        for strategy in StrategyPrefix:
            if strategy.value == prefix:
                return strategy.name
        return None

# strategy_prefix = StrategyPrefix["OvernightFutures"].value
# print(strategy_prefix)

# strategy = StrategyPrefix.get_strategy_by_prefix("AP")
# print(strategy)
import re
def get_strategy_name(trade_id):
    trade_id = trade_id.split("_")[0]
    match = re.match(r'^[A-Za-z]+', trade_id).group()

    # If not a direct match, extract prefix and look up strategy
    strategy_name = StrategyPrefix.get_strategy_by_prefix(match)
    
    # Return the strategy name based on the prefix
    return strategy_name if strategy_name else None


# def get_strategy_name(trade_id):
#     # Define the mapping between trade_id prefix and strategy name
#     strategy_map = {
#         'AP': 'AmiPy',
#         'MP': 'MPWizard',
#         'ET': 'ExpiryTrader',
#         'OF': 'OvernightFutures',
#         'EXTRA': 'Extra',
#         'STOCK': 'Stock'
#     }
#     if trade_id.startswith('EXTRA'):
#         return strategy_map['EXTRA']
#     elif trade_id.startswith('STOCK'):
#         return strategy_map['STOCK']

#     # Extract the prefix from the trade_id
#     prefix = trade_id[:2]  # assuming all prefixes are two characters long
    
#     # Return the strategy name based on the prefix, or a default value if not found
#     return strategy_map.get(prefix, "Unknown Strategy")

strategy_name = get_strategy_name("AP1_entry")
print(strategy_name)