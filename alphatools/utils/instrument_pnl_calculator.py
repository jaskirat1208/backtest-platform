import logging
import pandas as pd


class InstrumentPnlCalculator:
    logger = logging.getLogger(__name__)
    last_feed_info = pd.Series([], dtype='float64')

    def __init__(self, token):
        self.total_buy_qty = 0
        self.total_sell_qty = 0
        self.total_buy_val = 0
        self.total_sell_val = 0
        self.token = token

    def on_md(self, feed):
        self.last_feed_info = feed
        self.logger.debug("Feed Received by Pnl Calculator: {}".format(self.last_feed_info))

    def trade(self, qty):
        last_price = self.last_feed_info.CLOSE
        if qty > 0:
            self.total_buy_qty += qty
            self.total_buy_val += qty * last_price
        else:
            self.total_sell_qty -= qty
            self.total_sell_val -= qty * last_price

    def get_total_pnl(self):
        position = self.total_buy_qty - self.total_sell_qty
        if not len(self.last_feed_info) :
            return 0
        last_price = self.last_feed_info.CLOSE
        pnl = position * last_price - (self.total_buy_val - self.total_sell_val)
        self.logger.info("Pnl for instrument: {} = {}".format(self.token, pnl))
        return pnl
