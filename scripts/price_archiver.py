#!/usr/bin/env python3

import argparse
from datetime import datetime

from alphatools.backtesting_app import BackTestingApp

from alphatools.utils import instruments

import logging

# logging.getLogger().setLevel(logging.DEBUG)
# formatter = logging.Formatter(fmt='[%(filename)s:%(lineno)s :%(asctime)s: %(funcName)s] %(levelname)-8s : %(message)s',
#                                 datefmt='%Y-%m-%d %H:%M:%S')
# import sys
# # handler = logging.StreamHandler(sys.stdout)
# # handler.setFormatter(formatter)

class PriceArchiverStrat(BackTestingApp):
    def __init__(self, creds):
        # self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        super().__init__(creds)

    def load_instruments(self, underliers, start_date, end_date):
        self.set_start_date(start_date)
        self.set_end_date(end_date)
        for underlying in underliers:
            nifty_token_list = instruments.get_derivatives(underlying)
            for token_info in nifty_token_list:
                token = token_info['token']
                exch_seg = token_info['exch_seg']
                self.add_instrument(token, exch_seg)

        self.load_data()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-u", "--underlying", nargs='+',
                        help="Instrument whose derivatives have to be recorded", required=True)
    parser.add_argument("-s", "--start_date",
                        help="Instrument whose derivatives have to be recorded", required=False,
                        default=datetime.now().strftime('%Y%m%d'))
    parser.add_argument("-e", "--end_date",
                        help="Instrument whose derivatives have to be recorded", required=False,
                        default=datetime.now().strftime('%Y%m%d'))
    args = parser.parse_args()
    start_date = datetime.strptime(args.start_date, '%Y%m%d')
    end_date = datetime.strptime(args.end_date, '%Y%m%d')
    strat = PriceArchiverStrat('/Users/jaskiratsingh/projects/smart-api-creds.ini')
    strat.load_instruments(args.underlying, start_date, end_date)
