import pytest
from eodentry import overnight_futures_details, segregate_by_strategy


def test_overnight_futures_details_empty_orders():
    assert overnight_futures_details([], 'zerodha') == {}

def test_overnight_futures_details_only_buy_orders():
    orders = [{'trade_type': 'BUY', 'order_type': 'entry'} for _ in range(5)]
    assert overnight_futures_details(orders, 'zerodha') == {'OvernightFutures': {'Afternoon': [{'direction': 'BULLISH'} for _ in range(5)]}}

def test_overnight_futures_details_only_sell_orders():
    orders = [{'trade_type': 'SELL', 'order_type': 'entry'} for _ in range(5)]
    assert overnight_futures_details(orders, 'zerodha') == {'OvernightFutures': {'Afternoon': [{'direction': 'BEARISH'} for _ in range(5)]}}

def test_overnight_futures_details_mixed_orders():
    orders = [{'trade_type': 'BUY', 'order_type': 'entry'}, {'trade_type': 'SELL', 'order_type': 'entry'}]
    assert overnight_futures_details(orders, 'zerodha') == {'OvernightFutures': {'Afternoon': [{'direction': 'BEARISH'}, {'direction': 'BEARISH'}]}}

def test_overnight_futures_details_no_broker():
    assert overnight_futures_details([{'trade_type': 'BUY', 'order_type': 'entry'}], None) == {}

def test_segregate_by_strategy_empty_details():
    assert segregate_by_strategy({}, ['AmiPy'], 'zerodha') == {}

def test_segregate_by_strategy_single_strategy():
    details = {'AmiPy': [{'trade_type': 'BUY', 'order_type': 'entry'}]}
    assert segregate_by_strategy(details, ['AmiPy'], 'zerodha') == {'AmiPy': [{'trade_type': 'BUY', 'order_type': 'entry'}]}

def test_segregate_by_strategy_multiple_strategies():
    details = {'AmiPy': [{'trade_type': 'BUY', 'order_type': 'entry'}], 'MPWizard': [{'trade_type': 'SELL', 'order_type': 'entry'}]}
    assert segregate_by_strategy(details, ['AmiPy', 'MPWizard'], 'zerodha') == details

def test_segregate_by_strategy_empty_strategies():
    details = {'AmiPy': [{'trade_type': 'BUY', 'order_type': 'entry'}]}
    assert segregate_by_strategy(details, [], 'zerodha') == {}
