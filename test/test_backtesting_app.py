import datetime
from unittest import TestCase
from alphatools import backtesting_app
from datetime import datetime

from alphatools.utils.token_manager import TokenManager
import logging

logging.basicConfig(level=logging.INFO)


class TestBackTestingApp(TestCase):
    logger = logging.getLogger(__name__)

    def test_run_backtesting_engine_basic(self):
        app = backtesting_app.BackTestingApp("/Users/jaskiratsingh/projects/smart-api-creds.ini")
        app.set_start_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_end_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_interval('ONE_MINUTE')
        app.add_instrument(53825, "NFO")
        app.add_instrument(48756, "NFO")
        app.load_data()                     # Loads the data into a dataframe
        app.simulate()                      # Starts simulation from the beginning
        app.get_candle_info_df()            # Returns the entire simulation dataframe

    def test_run_backtesting_engine_advanced(self):
        app = backtesting_app.BackTestingApp("/Users/jaskiratsingh/projects/smart-api-creds.ini")
        app.set_start_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_end_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_interval('ONE_MINUTE')
        app.add_instrument(53825, "NFO")
        app.add_instrument(48756, "NFO")
        app.load_data()                     # Loads the data into a dataframe
        app.get_candle_info_df(-1)          # Returns entire candle info dataframe
        app.get_candle_info_df(2)           # Returns first two rows of the dataframe
        app.simulate(3)                     # Starts simulating from index 3

    def test_run_token_manager(self):
        app = TokenManager()
        self.logger.info(app.get_instrument('BANKNIFTY23FEB23FUT'))
        self.logger.info(app.get_instrument(48756))
