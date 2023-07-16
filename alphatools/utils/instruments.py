import nsepython
from datetime import datetime
from functools import lru_cache
from enum import Enum
import pandas as pd

from alphatools.utils.token_manager import TokenManager

class ExpiryType(Enum):
    WEEKLY = 0
    MONTHLY = 1


def get_kth_expiry(symbol, k=1, type=ExpiryType.WEEKLY):
    expiry_df = _get_expiry_list(symbol, 'pandas')
    if k <= 0 or k > len(expiry_df):
        raise Exception("Invalid expiry date")

    convert_to_date = lambda exp_date: datetime.strptime(exp_date, '%d-%b-%Y')
    date_list = expiry_df['Date'].apply(convert_to_date)
    if type == ExpiryType.WEEKLY:
        return date_list[0].strftime('%d%b%y').upper()

    last_date = date_list[0]
    for exp_date in date_list:
        if exp_date.month != datetime.now().month:
            return last_date.strftime('%d%b%y').upper()

        last_date = exp_date

    return last_date.strftime('%d%b%y').upper()

@lru_cache(maxsize=None)
def _get_expiry_list(symbol, type='list'):
    try:
        _get_expiry_lists(symbol=symbol, type=type)
    except Exception as e:
        print("Some exception occured. Returning current expiry as list")
        next_expiry = '20-JUL-2023'
        next2next_expiry = '20-JUL-2023'
        if type == 'list':
            convert_to_date = lambda exp_date: _convert_date(exp_date, '%d-%b-%Y', '%d%b%y').upper()
            return [convert_to_date(next_expiry), convert_to_date(next2next_expiry)]
        else:
            return pd.DataFrame({'Date': [next_expiry, next2next_expiry]})

def _get_expiry_lists(symbol, type='list'):
    if type != 'list':
        return nsepython.expiry_list(symbol, type)
    convert_to_date = lambda exp_date: _convert_date(exp_date, '%d-%b-%Y', '%d%b%y').upper()
    date_list = map(convert_to_date, nsepython.expiry_list(symbol, type))
    return list(date_list)


def _convert_date(exp_date, inp_date_fmt, out_date_fmt):
    datetime_obj = datetime.strptime(exp_date, inp_date_fmt)
    return datetime_obj.strftime(out_date_fmt)

def round_to_base(n, base= 10):
    return int(n/base) * base


def get_derivatives(symbol):
    if symbol == "NIFTY" or symbol == 'FINNIFTY':
        min_strike = 18500
        max_strike = 20500
        interval = 50

        token_manager = TokenManager()
        token_list = []
        # Add futures to instrument list
        for exp_date in _get_expiry_list(symbol):
            fut_info = token_manager.get_fut(symbol, exp_date)
            if fut_info != None:
                token_list.append(fut_info)

        # Add options to instrument list
        for strike in range(min_strike, max_strike, interval):
            for exp_date in _get_expiry_list(symbol):
                ce_info = token_manager.get_opt(symbol, exp_date, strike, 'CE')
                pe_info = token_manager.get_opt(symbol, exp_date, strike, 'PE')
                if ce_info != None:
                    token_list.append(ce_info)
                if pe_info != None:
                    token_list.append(pe_info)

        return token_list
    else:
        raise "Unsupported instrument: {}".format(symbol)

if __name__ == '__main__':
    # Instruments test
    import logging
    logging.basicConfig(level=logging.DEBUG)
    exp_list = _get_expiry_list('NIFTY')
    d = get_derivatives('NIFTY')
    print(d)
    # Expiry date test
    exp_date = get_kth_expiry('FINNIFTY', type=ExpiryType.MONTHLY)
    print(exp_date)