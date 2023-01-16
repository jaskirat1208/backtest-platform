
class PnlCalculator:
    def __init__(self):
        self.pnl = 0
        pass

    def on_md(self):
        pass

    def add_instrument_to_watch_list(self, token):
        pass

    def trade(self, token, qty):
        """

        :param token: Token of the instrument to be traded
        :param qty: Quantity traded, positive if bought, negative if sold
        :return:
        """
        pass

    def get_total_pnl(self):
        return self.pnl
