from unittest import TestCase

from alphatools.live_trading_app import LiveTradingApp


class TestLiveTradingApp(TestCase):
    def test_run_live(self):
        app = LiveTradingApp("/Users/jaskiratsingh/projects/smart-api-creds.ini")
        app.add_instrument(53825, "NFO")
        app.add_instrument(48756, "NFO")
        app.simulate()
