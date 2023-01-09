from alphatools.base_trading_app import BaseTradingApp
import configparser
from datetime import datetime
import pandas as pd
from alphatools.utils.smartapi_helper import SmartApiHelper


class BackTestingApp(BaseTradingApp):
    instruments_list = []
    start_date = None
    end_date = None
    data_interval = 'ONE_MINUTE'

    def __init__(self, config_file):
        """

        :param config_file:
        """
        super().__init__()
        print(config_file)
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(config_file)
        self.api_key = cfg_parser.get('SMARTAPI_LOGIN', 'API_KEY')
        self.client_code = cfg_parser.get('SMARTAPI_LOGIN', 'CLIENT_CODE')
        self.password = cfg_parser.get('SMARTAPI_LOGIN', 'PASSWORD')
        self.totp_key = cfg_parser.get('SMARTAPI_LOGIN', 'TOTP_KEY')
        print(cfg_parser.sections())

    @staticmethod
    def _get_time(time):
        return datetime.strptime(time, '%Y-%m-%dT%H:%M:%S%z')

    def onMd(self, dataRow):
        print(dataRow)
        pass

    def add_instrument(self, token, exchange):
        self.instruments_list.append((token, exchange))

    def set_start_date(self, start_date):
        self.start_date = start_date

    def set_end_date(self, end_date):
        self.end_date = end_date

    def set_interval(self, interval='ONE_MINUTE'):
        self.data_interval = interval

    def run(self):
        results_df = pd.DataFrame.from_records([],
                                       columns=['Timestamp', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'])
        for token, exchange in self.instruments_list:
            candle_info_params = {
                "exchange": exchange,
                "symboltoken": token,
                "interval": self.data_interval,
                "fromdate": datetime.strftime(self.start_date, '%Y-%m-%d %H:%M'),
                "todate": datetime.strftime(self.end_date, '%Y-%m-%d %H:%M')
            }
            api_helper = SmartApiHelper(self.api_key, self.client_code, self.password, self.totp_key)
            results = api_helper.get_candle_info(candle_info_params)['data']
            df = pd.DataFrame.from_records(results,
                                           columns=['Timestamp', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'])
            df['Token'] = token
            df['Timestamp'] = df['Timestamp'].apply(lambda x: self._get_time(x))
            results_df = pd.concat([results_df, df])

        results_df = results_df.sort_values(by=['Timestamp', 'Token']).reset_index(drop=True)
        for idx, row in results_df.iterrows():
            self.onMd(row)
