#!/usr/bin/env python3


import configparser
from typing import IO

from alphatools.utils import smartapi_helper

import argparse
from datetime import datetime
from alphatools.utils.alphatools_prompt import AlphaToolsCliPrompt


def query(args):
    pass    

class SmartApiQueryPrompt(AlphaToolsCliPrompt):
    def __init__(self, args) -> None:
        super().__init__()
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(args.config_file)
        api_key = cfg_parser.get('SMARTAPI_LOGIN', 'API_KEY')
        client_code = cfg_parser.get('SMARTAPI_LOGIN', 'CLIENT_CODE')
        password = cfg_parser.get('SMARTAPI_LOGIN', 'PASSWORD')
        totp_key = cfg_parser.get('SMARTAPI_LOGIN', 'TOTP_KEY')

        self.api_helper = smartapi_helper.SmartApiHelper(api_key=api_key, client_code=client_code, password=password, totp_key=totp_key)

    def do_getCandleInfo(self, args):
        # print(args.split())
        parser = argparse.ArgumentParser(exit_on_error=False)

        parser.add_argument("-e", "--exchange",
                            help="Config File with credentials", required=False, default='NSE')
        parser.add_argument("-t", "--token",
                            help="Config File with credentials", required=False, default='26000')
        parser.add_argument("-i", "--interval",
                            help="Config File with credentials", required=False, default='ONE_MINUTE')
        parser.add_argument("-d", "--date", help="Date", required=False, default=datetime.today().strftime('%Y%m%d'))
        
        args = parser.parse_args(args.split())
        print(args)
        # exchange, token, interval, date = args.split()
        self._getCandleInfo(args.exchange, args.token, args.interval, args.date) 
    
    def _getCandleInfo(self, exchange, token, interval='ONE_MINUTE', date=datetime.today().strftime('%Y%m%d')):
        _date = datetime.strptime(date, '%Y%m%d')
        candle_info_params = candle_info_params = {
                "exchange": exchange,
                "symboltoken": token,
                "interval": interval,
                "fromdate": datetime.strftime(_date, '%Y-%m-%d 00:00'),
                "todate": datetime.strftime(_date, '%Y-%m-%d 23:59')
            }
        print(self.api_helper.get_candle_info(candle_info_params))


    def help_getCandleInfo(self):
        print("Returns candle info")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    import sys
    print(sys.argv[1:])
    parser.add_argument("-c", "--config_file",
                        help="Config File with credentials", required=False, default='/Users/jaskiratsingh/projects/smart-api-creds.ini')
    
    args = parser.parse_args()
    
    prompt = SmartApiQueryPrompt(args)
    prompt.cmdloop()