import os
import datetime
import pandas as pd
import psycopg2
from kiteconnect import KiteConnect
from collections import namedtuple
from datetime import timedelta
import datetime

# Constants and Configurations
API_KEY = '6b0dp5ussukmo67h'
ACCESS_TOKEN = 'lF8hXyXYILNB0TQm7aZkNtWCVqSdp8Er'
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

base_symbol_map = {
    0: ["MIDCPNIFTY"],
    1: ["FINNIFTY"],
    2: ["BANKNIFTY"],
    3: ["NIFTY"],
    4: ["SENSEX"],
}

TOKEN_MAP = {
    'NIFTY': '256265',
    'BANKNIFTY': '260105',
    'FINNIFTY': '257801',
    'MIDCPNIFTY': '288009',
    'SENSEX': '265'
}

holidays = [datetime.date(2023, i, j) for i, j in [
    (1, 26), (3, 7), (3, 30), (4, 4), (4, 7), (4, 14),
    (4, 22), (5, 1), (6, 28), (8, 15), (9, 19), (10, 4),
    (10, 24), (11, 14), (11, 27), (12, 25)]
]

def get_strikeprc(token):
    ltp_data = kite.ltp(token)
    ltp = ltp_data[token]['last_price']
    return round(ltp / 100) * 100

Instrument = namedtuple("Instrument", ['exchange', 'token', 'symbol', 'name', 'expiry', 'lot_size'])

def get_option_tokens(base_symbol, expiry_date, option_type, strike_prc):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    instruments_df = pd.read_csv(os.path.join(script_dir, '..', 'Utils', 'instruments.csv'))
    instruments_df = instruments_df[
        ["instrument_token", "tradingsymbol", "name", "exchange", "lot_size", "instrument_type", "expiry", "strike"]
    ]
    
    if base_symbol == 'SENSEX':
        exchange = 'BFO'
    else:
        exchange = 'NFO'
    
    nfo_ins_df = instruments_df[
        (instruments_df["exchange"] == exchange)
        & (instruments_df["name"] == str(base_symbol))
        & (instruments_df["expiry"] == str(expiry_date))
        & (instruments_df["strike"] == int(strike_prc))
        & (instruments_df["instrument_type"] == str(option_type))
    ]
    print(base_symbol, expiry_date, strike_prc, option_type)
    tokens = []  
    trading_symbol_list = []
    tokens.append(int(nfo_ins_df['instrument_token'].values[0]))  # CE token
    trading_symbol_list.append(nfo_ins_df['tradingsymbol'].values[0])  # CE trading symbol

    # Extract the token from the trading symbol
    token_CE = nfo_ins_df['tradingsymbol'].values[0]
    trading_symbol_aliceblue = []

    for token, single_trading_symbol in zip(tokens, trading_symbol_list):
        trading_symbol_aliceblue.append(Instrument(exchange, token, base_symbol, single_trading_symbol, expiry_date, 50))
    return tokens, trading_symbol_list, trading_symbol_aliceblue


def get_next_weekday(d, weekday):
    """
    Returns the next specified weekday. 
    d is the current date, weekday is the desired weekday (0 for Monday, 1 for Tuesday, etc.)
    """
    days_ahead = weekday - d.weekday()
    if days_ahead < 0:  # If the desired day has already passed in the current week
        days_ahead += 7
    elif days_ahead == 0 and datetime.datetime.now().time() > datetime.time(23, 30):  # If it's the desired day, but after 4:30 PM
        days_ahead += 7
    next_date = d + datetime.timedelta(days_ahead)
    while next_date in holidays:
        next_date += datetime.timedelta(1)
    return next_date

def get_weekly_expiry(base_symbol):
    # Get the current date
    today = datetime.date.today()
    
    # Based on the base_symbol, determine the weekday of the expiry
    if base_symbol == "MIDCPNIFTY":
        weekly_expiry = get_next_weekday(today, 0)  # Monday
    elif base_symbol == "FINNIFTY":
        weekly_expiry = get_next_weekday(today, 1)  # Tuesday
    elif base_symbol == "BANKNIFTY":
        weekly_expiry = get_next_weekday(today, 2)  # Wednesday    
    elif base_symbol == "NIFTY":
        weekly_expiry = get_next_weekday(today, 3)  # Thursday
    elif base_symbol == "SENSEX":
        weekly_expiry = get_next_weekday(today, 4)  # Friday

    # Check if tomorrow is a holiday
    tomorrow = today + datetime.timedelta(days=1)
    # If tomorrow is a holiday, prepond the weekly expiry to today
    if tomorrow in holidays:
        weekly_expiry = today

    return weekly_expiry

def get_monthly_expiry(base_symbol):
    # Get the current date
    today = datetime.date.today()
    
    # Determine the original weekday of the expiry based on the base_symbol
    if base_symbol == "MIDCPNIFTY":
        expiry_weekday = 0  # Monday
    elif base_symbol == "FINNIFTY":
        expiry_weekday = 1  # Tuesday
    elif base_symbol == "BANKNIFTY":
        expiry_weekday = 2  # Wednesday    
    elif base_symbol == "NIFTY":
        expiry_weekday = 3  # Thursday
    elif base_symbol == "SENSEX":
        expiry_weekday = 4  # Friday

    # Get the last day of the month
    last_day = datetime.date(today.year, today.month+1, 1) - datetime.timedelta(1)
    
    # Find the last weekday of the month that matches the regular expiry weekday
    while last_day.weekday() != expiry_weekday or last_day in holidays:
        last_day -= datetime.timedelta(1)
    
    return last_day


def get_expiry_dates(base_symbol):
    weekly_expiry = get_weekly_expiry(base_symbol)
    monthly_expiry = get_monthly_expiry(base_symbol)
    return weekly_expiry, monthly_expiry



def connect_to_db(base_symbol):
    print(f"Connecting to database {base_symbol.lower()}...")
    return psycopg2.connect(
        dbname=base_symbol.lower(),
        user="postgres",
        password="K@nnada0",
        host="localhost",
        port="5432"
    )

def store_data_in_postgres(trading_symbol_list, all_data, cursor):
    table_name =trading_symbol_list[0]
    
    table_name =trading_symbol_list[0]
    
    if " " or "(" or")" in table_name:
        table_name = table_name.replace(" ", "").replace("(", "").replace(")", "")

    print(f"Storing data in table {table_name}...")
    # table_name = trading_symbol_list[0].replace("-", "_").lower()
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (date TIMESTAMP, open REAL, high REAL, low REAL, close REAL, volume INT);"
    cursor.execute(create_table_query)
    
    for record in all_data:
        date = record['date'].strftime('%Y-%m-%d %H:%M:%S')
        open_price = record['open']
        high = record['high']
        low = record['low']
        close_price = record['close']
        volume = record['volume']
        
        insert_query = f"INSERT INTO {table_name} (date, open, high, low, close, volume) VALUES ('{date}', {open_price}, {high}, {low}, {close_price}, {volume});"
        try:
            cursor.execute(insert_query)
        except Exception as e:
            print(f"Error while inserting record {table_name}: {e}")
    
    cursor.connection.commit()

def fetch_and_store_historical_data(token,base_symbol, expiry_date,future_expiry, start_date, end_date, cursor):
    if base_symbol == 'NIFTY' or base_symbol == 'FINNIFTY' or base_symbol == 'MIDCPNIFTY' :
        strike_prc = get_strikeprc(token)
        upper_strikes = [(strike_prc  + i*50) for i in range(1, 9)]
        lower_strikes = [(strike_prc - i*50) for i in range(1, 9)]
    elif base_symbol == 'BANKNIFTY' or base_symbol == 'SENSEX':
        strike_prc = get_strikeprc(token)
        upper_strikes = [(strike_prc + i*100) for i in range(1, 9)]
        lower_strikes = [(strike_prc - i*100) for i in range(1, 9)]
    all_strikes = lower_strikes + [strike_prc] + upper_strikes

    data = kite.historical_data(instrument_token=token, from_date=start_date, to_date=end_date, interval="minute", continuous=False)
    store_data_in_postgres([base_symbol], data, cursor)
    
    future_token,future_symbol,_ = get_option_tokens(base_symbol, future_expiry, "FUT", 0)
    data = kite.historical_data(instrument_token=future_token[0], from_date=start_date, to_date=end_date, interval="minute", continuous=False)
    store_data_in_postgres(future_symbol, data, cursor)

    for strike in all_strikes:
        print(strike)
        for option_type in ["CE", "PE"]:
            tokens, trading_symbol_list, _ = get_option_tokens(base_symbol, expiry_date, option_type, strike)
            
            for token, trading_symbol in zip(tokens, trading_symbol_list):
                data = kite.historical_data(instrument_token=token, from_date=start_date, to_date=end_date, interval="minute", continuous=False)
                # Store the data for this trading_symbol
                store_data_in_postgres(trading_symbol_list, data, cursor)

def main():
    current_day = datetime.datetime.now().weekday()
    base_symbols = base_symbol_map.get(current_day, [])
    
    # Check if tomorrow is a holiday
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    if tomorrow in holidays:
        # If today is Friday, we need to check for Monday's base_symbol
        if current_day == 4:
            next_day_base_symbols = base_symbol_map.get(0, [])
        else:
            next_day_base_symbols = base_symbol_map.get(current_day + 1, [])
        base_symbols.extend(next_day_base_symbols)

    for base_symbol in base_symbols:
        conn = connect_to_db(base_symbol)
        cursor = conn.cursor()
        
        token = TOKEN_MAP[base_symbol]
        start_date = (datetime.datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date = datetime.datetime.now().strftime('%Y-%m-%d')

        expiry_date, future_expiry = get_expiry_dates(base_symbol)
        fetch_and_store_historical_data(token, base_symbol, expiry_date, future_expiry, start_date, end_date, cursor)

        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()

