from alphatools.utils.instrument_pnl_calculator import InstrumentPnlCalculator


class PnlCalculator:
    def __init__(self):
        self.instrument_pnl_calculators = {}

    def on_md(self, token, feed):
        if token in self.instrument_pnl_calculators:
            pnl_calculator = self.instrument_pnl_calculators[token]
            pnl_calculator.on_md(feed)

    def add_instrument_to_watch_list(self, token):
        self.instrument_pnl_calculators[token] = InstrumentPnlCalculator(token)

    def trade(self, token, qty):
        """

        :param token: Token of the instrument to be traded
        :param qty: Quantity traded, positive if bought, negative if sold
        :return:
        """
        instrument_pnl_calc = self.instrument_pnl_calculators[token]
        instrument_pnl_calc.trade(qty)

    def get_total_pnl(self):
        result = 0
        for pnl_calculator in self.instrument_pnl_calculators.values():
            result += pnl_calculator.get_total_pnl()

        return result
