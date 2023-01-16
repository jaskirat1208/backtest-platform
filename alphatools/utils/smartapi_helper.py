from smartapi import SmartWebSocket, SmartConnect
import mintotp
import requests
import logging

from alphatools.utils import cache

INSTRUMENT_API_URL = 'http://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
CACHE_FILE_PATH = '/tmp/'


def _candle_info_params_hash(candle_info_params):
    exch = candle_info_params["exchange"]
    tok = candle_info_params["symboltoken"]
    interval = candle_info_params["interval"]
    fromdate = candle_info_params["fromdate"]
    todate = candle_info_params["todate"]

    return "{}.{}.{}.{}.{}".format(exch, tok, interval, fromdate, todate)


class SmartApiHelper:
    logger = logging.getLogger(__name__)

    def __init__(self, api_key, client_code, password, totp_key):
        self.api_key = api_key
        self.client_code = client_code
        self.passwd = password
        self.totp_key = totp_key

    @staticmethod
    def get_instruments_list():
        instruments_csv_list = requests.get(INSTRUMENT_API_URL)
        return instruments_csv_list.json()

    @cache.cache_to_file(CACHE_FILE_PATH, _candle_info_params_hash)
    def get_candle_info(self, candle_info_params):
        candle_info_results = []
        try:
            smart_conn = SmartConnect(api_key=self.api_key)
            totp = mintotp.totp(self.totp_key)
            smart_conn.generateSession(self.client_code, self.passwd, totp)
            candle_info_results = smart_conn.getCandleData(candle_info_params)
            smart_conn.terminateSession(self.client_code)
        except Exception as e:
            self.logger.error("Historical API failed with exception: {}".format(e.message))

        return candle_info_results
