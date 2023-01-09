from collections import defaultdict

from multipledispatch import dispatch

from alphatools.utils.smartapi_helper import SmartApiHelper


class TokenManager:

    token_to_instrument_info = defaultdict(None)
    symbol_to_instrument_info = defaultdict(None)

    def __init__(self):
        instruments_json = SmartApiHelper.get_instruments_list()
        for instrument in instruments_json:
            try:
                token = int(instrument['token'])
                symbol = instrument['symbol']
                self.token_to_instrument_info[token] = instrument
                self.symbol_to_instrument_info[symbol] = instrument
            except ValueError as e:
                print('Invalid token for instrument {}. Skipping this row'.format(instrument))

    @dispatch(int)
    def get_instrument(self, token):
        """
        :param token: Token number of the instrument specified by NSE
        :return: If token is valid {
            'token': '48756',
            'symbol': 'BANKNIFTY23FEB23FUT',
            'name': 'BANKNIFTY',
            'expiry': '23FEB2023',
            'strike': '-1.000000',
            'lotsize': '25',
            'instrumenttype': 'OPTIDX',
            'exch_seg': 'NFO',
            'tick_size': '5.000000'
        }
        Else None
        """
        return self.token_to_instrument_info.get(token)

    @dispatch(str)
    def get_instrument(self, symbol):
        return self.symbol_to_instrument_info.get(symbol)

    def get_fut(self, name, expiry):
        """
        Returns properties of future with requested params
        :param name: Underlying symbol
        :param expiry: Expiry Date
        :return: Refer @get_instrument for more details
        """
        symbol = "{}{}FUT".format(name, expiry)
        return self.get_instrument(symbol)

    def get_opt(self, name, strike, expiry, option_type):
        """
        Returns properties of option with requested params
        :param name: Underlying symbol
        :param strike: Strike Price
        :param expiry: Expiry Date
        :param option_type: Put or call
        :return: Returns a dictionary in the following format or None if the instrument is invalid/not found
        """
        symbol = "{}{}{}{}".format(name, strike, expiry, option_type)
        return self.get_instrument(symbol)
