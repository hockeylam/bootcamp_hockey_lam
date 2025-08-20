"""
Copyright (C) 2019 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
 and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.
"""

from brokerapi.object_implem import Object
from brokerapi.utils import intMaxString
from brokerapi.utils import floatMaxString

class CommissionReport(Object):
    def __init__(self):
        self.execId = ""
        self.commission = 0. 
        self.currency = ""
        self.realizedPNL =  0.
        self.yield_ = 0.
        self.yieldRedemptionDate = 0  # YYYYMMDD format

    def __str__(self):
        return "ExecId: %s, Commission: %s, Currency: %s, RealizedPnL: %s, Yield: %s, YieldRedemptionDate: %s" % (self.execId, 
            floatMaxString(self.commission), self.currency, floatMaxString(self.realizedPNL), floatMaxString(self.yield_), intMaxString(self.yieldRedemptionDate))
