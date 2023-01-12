import datetime
from unittest import TestCase
from alphatools import backtesting_app
from datetime import datetime

from alphatools.utils.token_manager import TokenManager
import logging

logging.basicConfig(level=logging.INFO)


class TestBackTestingApp(TestCase):
    logger = logging.getLogger(__name__)

    def test_run_backtesting_engine(self):
        app = backtesting_app.BackTestingApp("/Users/jaskiratsingh/projects/smart-api-creds.ini")
        app.set_start_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_end_date(datetime.strptime('2022-12-29 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
        app.set_interval('ONE_MINUTE')
        app.add_instrument(53825, "NFO")
        app.add_instrument(48756, "NFO")
        app.run()

    def test_run_token_manager(self):
        app = TokenManager()
        self.logger.info(app.get_instrument('BANKNIFTY23FEB23FUT'))
        self.logger.info(app.get_instrument(48756))
