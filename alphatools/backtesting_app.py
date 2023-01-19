import configparser
import pandas as pd
import logging

from datetime import datetime
from time import sleep

from alphatools.utils.pnl_calculator import PnlCalculator
from alphatools.utils.smartapi_helper import SmartApiHelper


class BackTestingApp:
    logger = logging.getLogger(__name__)
    instruments_list = []
    start_date = None
    end_date = None
    data_interval = 'ONE_MINUTE'
    pnl_calculator = PnlCalculator()

    def __init__(self, config_file):
        """

        :param config_file:
        """
        super().__init__()
        self.candle_info_df = None
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(config_file)
        self.api_key = cfg_parser.get('SMARTAPI_LOGIN', 'API_KEY')
        self.client_code = cfg_parser.get('SMARTAPI_LOGIN', 'CLIENT_CODE')
        self.password = cfg_parser.get('SMARTAPI_LOGIN', 'PASSWORD')
        self.totp_key = cfg_parser.get('SMARTAPI_LOGIN', 'TOTP_KEY')

    @staticmethod
    def _get_time(time):
        return datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')

    def _on_md(self, data_row):
        token = data_row["Token"]
        self.pnl_calculator.on_md(token, data_row)
        self.on_md(data_row)

    def on_md(self, data_row):
        """
        Basic onMd template. You can create a child class with backtestingApp as parent to
        come up with your own onMd function. See basic documentation.
        :param data_row:
        :return:
        """
        self.logger.info("Received row: {}".format(data_row))
        pass

    def add_instrument(self, token, exchange):
        """
        Adds an instrument to the subscriber list
        :param token: token number of the instrument
        :param exchange: Exchange in which the instrument is traded
        :return:
        """
        self.instruments_list.append((token, exchange))
        self.pnl_calculator.add_instrument_to_watch_list(token)

    def set_start_date(self, start_date):
        """
        Start datetime of simulation
        :param start_date: datetime
        :return: None
        """

        self.start_date = start_date

    def set_end_date(self, end_date):
        """
        End datetime of simulation
        :param end_date: datetime
        :return: None
        """
        self.end_date = end_date

    def set_interval(self, interval='ONE_MINUTE'):
        """
        Set frequency of requested data for simulation. Possible values:
                Interval	Description
                ONE_MINUTE	1 Minute
                THREE_MINUTE	3 Minute
                FIVE_MINUTE	5 Minute
                TEN_MINUTE	10 Minute
                FIFTEEN_MINUTE	15 Minute
                THIRTY_MINUTE	30 Minute
                ONE_HOUR	1 Hour
                ONE_DAY	1 Day

        :param interval: Requested interval

        :return:
        """
        self.data_interval = interval

    def _get_candle_info_results(self, _date, token, exchange):
        candle_info_params = {
            "exchange": exchange,
            "symboltoken": token,
            "interval": self.data_interval,
            "fromdate": datetime.strftime(_date, '%Y-%m-%d 00:00'),
            "todate": datetime.strftime(_date, '%Y-%m-%d 23:59')
        }
        self.logger.info("Sending candle request for {}".format(candle_info_params))
        api_helper = SmartApiHelper(self.api_key, self.client_code, self.password, self.totp_key)
        return api_helper.get_candle_info(candle_info_params)['data']

    def load_data(self):
        """
        Based on the instrument info requested, sends get Request to AB smart API server

        :return: None
        """
        self.candle_info_df = pd.DataFrame.from_records([],
                                                        columns=['Timestamp', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'])

        for _date in pd.date_range(self.start_date, self.end_date):
            for token, exchange in self.instruments_list:
                results = self._get_candle_info_results(_date, token, exchange)
                if not results:
                    self.logger.warning("No data available for Date: {}, "
                                      "Token: {}, Exchange: {}".format(_date, token, exchange))
                    continue
                df = pd.DataFrame.from_records(results,
                                               columns=['Timestamp', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'])
                df['Token'] = token
                df['Timestamp'] = df['Timestamp'].apply(lambda x: self._get_time(x))
                self.candle_info_df = pd.concat([self.candle_info_df, df])
                sleep(0.35)

        self.candle_info_df = self.candle_info_df.sort_values(by=['Timestamp', 'Token']).reset_index(drop=True)

    def get_candle_info_df(self, num_rows=-1):
        """
        Returns top n rows of the candle info dataframe

        :param num_rows: Number of rows required for training purposes
        :return: pandas dataframe
        """
        if num_rows == -1:
            return self.candle_info_df

        return self.candle_info_df.head(num_rows)

    def get_row_number(self, timestamp):
        """
        Returns index of the last row of df such that df.timestamp < timestamp.
        Makes it more convenient to split training and test dataset.

        For example, you want to train the model initially for say 9:30-11:30 and
        run the rest of the simulation online. Call this function to get the row number
        corresponding to 11:30 and send it to the functions simulate and
        get_candle_info_df() function.

        :param timestamp:  Benchmark time to split into training and test
        :return: Index of row
        """
        return len(self.candle_info_df[self.candle_info_df['Timestamp'] < timestamp])

    def simulate(self, start=0):
        """
        Runs simulation from the required position. It is recommended to use simulate without
        args to simulate everything online one by one.

        :param start: Offset starting position of online simulation
        :return: None
        """
        for idx, row in self.candle_info_df.iterrows():
            if idx >= start:
                self._on_md(row)

        self.post_simulation()

    def post_simulation(self):
        """
        This can be overriden to do some cleanup tasks at the end of simulation
        :return:
        """
        pass

    def trade(self, token, qty):
        self.pnl_calculator.trade(token, qty)

    def get_total_pnl(self):
        return self.pnl_calculator.get_total_pnl()
