import configparser
import logging

import mintotp
from smartapi import SmartConnect

from alphatools.utils.exchange import Exchange
from alphatools.utils.smart_ws_v2 import SmartWebSocketV2


class LiveTradingApp:
    logger = logging.getLogger(__name__)

    def __init__(self, config_file):
        self.mode = 1
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(config_file)
        self.api_key = cfg_parser.get('SMARTAPI_LOGIN', 'API_KEY')
        self.client_code = cfg_parser.get('SMARTAPI_LOGIN', 'CLIENT_CODE')
        self.password = cfg_parser.get('SMARTAPI_LOGIN', 'PASSWORD')
        self.totp_key = cfg_parser.get('SMARTAPI_LOGIN', 'TOTP_KEY')

        smart_conn = SmartConnect(api_key=self.api_key)
        totp = mintotp.totp(self.totp_key)
        data = smart_conn.generateSession(self.client_code, self.password, totp)
        auth_token = data['data']['jwtToken']
        feed_token = smart_conn.getfeedToken()
        self.corr_id = data['data']['name']

        self.smart_ws = SmartWebSocketV2(auth_token, self.api_key, self.client_code, feed_token)
        self.subscription_list = {}         # List of exchange to instruments mapping(int to list map)

    def add_instrument(self, token, exchange):
        exchange_id = Exchange[exchange].value
        if exchange_id not in self.subscription_list:
            self.subscription_list[exchange_id] = []

        self.subscription_list[exchange_id].append(token)

    def set_mode(self, mode):
        self.mode = mode

    def _on_open(self, ws):
        self.logger.info("Connection to websocket opened")
        subscribed_instruments = []
        for exch in self.subscription_list.keys():
            tokens = self.subscription_list[exch]
            subscribed_instruments.append({'exchangeType': exch, 'tokens': tokens})
        self.smart_ws.subscribe(self.corr_id, self.mode, subscribed_instruments)
        self.logger.info("Subscription to instruments: {} initiated".format(subscribed_instruments))

    def _on_error(self, ws, message):
        self.logger.error(message)

    def on_md(self, ws, md):
        self.logger.info("Received feed: {}".format(md))

    def on_close(self, ws):
        pass

    def simulate(self):
        self.smart_ws.on_open = self._on_open
        self.smart_ws.on_close = self.on_close
        self.smart_ws.on_data = self.on_md
        self.smart_ws.on_error = self._on_error

        self.smart_ws.connect()
