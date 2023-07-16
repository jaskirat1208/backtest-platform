#!/usr/bin/env python3

import argparse
from typing import IO

from alphatools.utils.alphatools_prompt import AlphaToolsCliPrompt
from alphatools.utils.token_manager import TokenManager


class InstrumentsCliPrompt(AlphaToolsCliPrompt):
    def __init__(self, completekey: str = "tab", stdin: IO[str] | None = None, stdout: IO[str] | None = None) -> None:
        super().__init__(completekey, stdin, stdout)
        self.token_manager = TokenManager()


    def do_getInstrumentInfo(self, instrument_id):
        print(self.token_manager.get_instrument(int(instrument_id)))
        pass

    def do_getInstrumentInfoForSymbol(self, symbol):
        print(self.token_manager.get_instrument(symbol))

    def help_getInstrumentInfo(self):
        print("Returns Instrument symbol for instrument id")

    def help_getInstrumentInfoForSymbol(self):
        print("Returns Instrument symbol for symbol")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config_file",
                        help="Config File with credentials", required=False, default='/Users/jaskiratsingh/projects/smart-api-creds.ini')


    InstrumentsCliPrompt().cmdloop()