import datetime
from unittest import TestCase
from alphatools import backtesting_app
from datetime import datetime

from alphatools.utils.token_manager import TokenManager
import logging

logging.basicConfig(level=logging.INFO)


class BackTestingAppOnDummyData(backtesting_app.BackTestingApp):
    dummy_feed = [
        ['2022-12-20T11:39:00+05:30', 973.0, 973.0, 972.25, 972.25, 40],
        ['2022-12-20T11:40:00+05:30', 972.25, 972.25, 972.25, 972.25, 1],
        ['2022-12-20T11:41:00+05:30', 972.25, 972.25, 972.25, 972.25, 1],
        ['2022-12-20T11:42:00+05:30', 974.2, 974.2, 972.6, 972.6, 11],
        ['2022-12-20T11:43:00+05:30', 972.6, 972.6, 972.6, 972.6, 1],
        ['2022-12-20T11:44:00+05:30', 972.6, 974.35, 972.6, 974.35, 12],
        ['2022-12-20T11:45:00+05:30', 972.5, 974.55, 972.5, 974.55, 19],
        ['2022-12-20T11:46:00+05:30', 974.7, 974.95, 974.05, 974.95, 20],
        ['2022-12-20T11:47:00+05:30', 972.45, 972.45, 972.0, 972.0, 124],
        ['2022-12-20T11:48:00+05:30', 973.7, 973.7, 972.05, 972.05, 18],
        ['2022-12-20T11:49:00+05:30', 972.05, 972.05, 972.05, 972.05, 1]
    ]

    def _get_candle_info_results(self, _date, token, exchange):
        return self.dummy_feed

    def on_md(self, data_row):
        self.trade(data_row.Token, 1)

    def post_simulation(self):
        self.logger.info("Total Pnl: {}".format(self.get_total_pnl()))


class TestBackTestingApp(TestCase):
    logger = logging.getLogger(__name__)

    def test_run_backtesting_engine_basic(self):
        app = BackTestingAppOnDummyData("/Users/jaskiratsingh/projects/smart-api-creds.ini")
        app.set_start_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_end_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_interval('ONE_MINUTE')
        app.add_instrument(53825, "NFO")
        app.add_instrument(48756, "NFO")
        app.load_data()                     # Loads the data into a dataframe
        app.get_row_number(datetime.strptime('2022-12-23 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        df = app.get_candle_info_df()            # Returns the entire simulation dataframe
        assert len(df) == 2 * len(app.dummy_feed)

    def test_run_backtesting_engine_advanced(self):
        app = BackTestingAppOnDummyData("/Users/jaskiratsingh/projects/smart-api-creds.ini")
        app.set_start_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_end_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_interval('ONE_MINUTE')
        app.add_instrument(53825, "NFO")
        app.add_instrument(48756, "NFO")
        app.load_data()                             # Loads the data into a dataframe
        df1 = app.get_candle_info_df(-1)            # Returns entire candle info dataframe
        df2 = app.get_candle_info_df(2)             # Returns first two rows of the dataframe
        assert len(df1) == 2 * len(app.dummy_feed)
        assert len(df2) == 2

    def test_run_token_manager(self):
        app = TokenManager()
        self.logger.info(app.get_instrument('BANKNIFTY23FEB23FUT'))
        self.logger.info(app.get_instrument(48756))
        self.logger.info(app.get_opt("NIFTY", "09FEB23", 16000, "PE"))

