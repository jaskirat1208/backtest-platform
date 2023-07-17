import time

from SmartApi import SmartConnect
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

    def get_candle_info(self, candle_info_params):
        candle_info = self._get_candle_info(candle_info_params)
        if 'data' not in candle_info or not candle_info['data']:
            # print (candle_info['data'])
            # print("Could not load data from cache")
            return self._get_candle_info(candle_info_params, force_reload=True)
        
        return candle_info
    
    @cache.cache_to_file(CACHE_FILE_PATH, _candle_info_params_hash)
    # def _get_candle_info_wrap(self, candle_info_params):
    #     self.logger.info("Calling getCandleInfo wrapper")

    #     return self._get_candle_info(candle_info_params)

    def _get_candle_info(self, candle_info_params):
        candle_info_results = []

        n_retries_left = 3
        while n_retries_left > 0:
            try:
                smart_conn = SmartConnect(api_key=self.api_key)
                totp = mintotp.totp(self.totp_key)
                conn = smart_conn.generateSession(self.client_code, self.passwd, totp)
                refresh_token = conn['data']['refreshToken']
                candle_info_results = smart_conn.getCandleData(candle_info_params)
                smart_conn.terminateSession(self.client_code)
            except Exception as e:
                logging.exception("Historical API failed with exception")
                logging.info("Waiting for 5 seconds.")
                time.sleep(5)
                n_retries_left -= 1
                logging.info("Retrying. {} retries left".format(n_retries_left))

            return candle_info_results
