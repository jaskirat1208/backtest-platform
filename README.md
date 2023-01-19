# About project
A small wrapper over smartapi to backtest basic trading strategies. 
Easy installation and usage

# Installation
```
pip install alphatools_jv
```

# Usage
## Creating and running a strategy
```python
from alphatools.backtesting_app import BackTestingApp
from datetime import datetime

class TestSmartApiApp(BackTestingApp):

    def on_md(self, data_row):
        # your strat code goes here
        print("New row found: {}".format(data_row))


app = TestSmartApiApp('/Users/jaskiratsingh/projects/smart-api-creds.ini')
app.set_start_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
app.set_end_date(datetime.strptime('2022-12-29 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
app.set_interval('ONE_MINUTE')
app.add_instrument(53825, "NFO")
app.add_instrument(48756, "NFO")
app.load_data()                     # Loads the data into a dataframe
app.get_candle_info_df()            # Returns the entire simulation dataframe
app.simulate()                      # Starts simulation from the beginning

# To place a trade, use trade api to send the orders to the pnl calculator. 
# Pnl calculator uses last tick prices to calculate the observed Pnl
app.trade(53825, 1)     # Buys 1 unit for token 53825
app.trade(53825, -3)    # Sells 3 units for token 53825
app.get_total_pnl()     # Returns pnl after all trades are made
```

## Helper for instruments
```python
from alphatools.utils.token_manager import TokenManager

tok = TokenManager()

# Refer documentation for more overrides
info = tok.get_instrument(53825) # Returns instrument info
info = tok.get_instrument('NIFTY23FEB23FUT') # Returns instrument info
```