import logging
from collections import defaultdict
from datetime import date

from multipledispatch import dispatch

from alphatools.utils.smartapi_helper import *


def _instruments_api_hash(sim_date):
    return str(sim_date)

class TokenManager:
    logger = logging.getLogger(__name__)
    token_to_instrument_info = defaultdict(None)
    symbol_to_instrument_info = defaultdict(None)

    def __init__(self):
        instruments_json = self._get_instruments_list(date.today())
        self.logger.info("Instruments Received: {}".format(len(instruments_json)))
        for instrument in instruments_json:
            try:
                token = int(instrument['token'])
                symbol = instrument['symbol']
                self.token_to_instrument_info[token] = instrument
                self.symbol_to_instrument_info[symbol] = instrument
            except ValueError as e:
                self.logger.debug('Invalid token for instrument {}. Skipping this row'.format(instrument))

        self.logger.info("Instruments processed successfully: {}".format(len(self.token_to_instrument_info)))

    @cache.cache_to_file(CACHE_FILE_PATH, _instruments_api_hash)
    def _get_instruments_list(self, sim_date):
        return SmartApiHelper.get_instruments_list()

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
        self.logger.info("Searching for symbol: {}".format(symbol))
        return self.get_instrument(symbol)

    def get_opt(self, name, expiry, strike, option_type):
        """
        Returns properties of option with requested params
        :param name: Underlying symbol
        :param strike: Strike Price
        :param expiry: Expiry Date
        :param option_type: Put or call
        :return: Returns a dictionary in the following format or None if the instrument is invalid/not found
        """
        symbol = "{}{}{}{}".format(name, expiry, strike, option_type)
        self.logger.info("Searching for symbol: {}".format(symbol))
        return self.get_instrument(symbol)
