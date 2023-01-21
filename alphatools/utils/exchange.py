from enum import Enum


class Exchange(Enum):
    nse_cm = 1
    NSE = nse_cm
    nse_fo = 2
    NFO = nse_fo
    bse_cm = 3
    BSE = bse_cm
    bse_fo = 4
    mcx_cm = 5
    mcx_fo = 7
    cde_fo = 13
