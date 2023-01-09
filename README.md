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

    def onMd(self, dataRow):
        # your strat code goes here
        print("New row found: ")


app = TestSmartApiApp('/Users/jaskiratsingh/projects/smart-api-creds.ini')
app.set_start_date(datetime.strptime('2022-12-20 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
app.set_end_date(datetime.strptime('2022-12-29 11:39:00+05:30', '%Y-%m-%d %H:%M:%S%z'))
app.set_interval('ONE_MINUTE')
app.add_instrument(53825, "NFO")
app.add_instrument(48756, "NFO")
app.run()
```

## Helper for instruments
```python
from alphatools.utils.token_manager import TokenManager

tok = TokenManager()

# Refer documentation for more overrides
info = tok.get_instrument(53825) # Returns instrument info
info = tok.get_instrument('NIFTY23FEB23FUT') # Returns instrument info
```