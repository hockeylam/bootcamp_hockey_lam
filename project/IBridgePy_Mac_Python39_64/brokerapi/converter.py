from brokerapi.softdollartier import SoftDollarTier
import json
from decimal import Decimal
from brokerapi.order import Order
from brokerapi.contract import Contract, ComboLeg
from brokerapi.scanner import ScannerSubscription


def order_converter(json_order):
    py_order = json.loads(json_order)
    ans = Order()
    for key in py_order:
        if key != 'softDollarTier' and py_order[key]:
            setattr(ans, key, py_order[key])
    if 'softDollarTier' in py_order:
        ans.softDollarTier = softDollarTier_converter(py_order['softDollarTier'])
    ans.totalQuantity = Decimal(ans.totalQuantity)
    if ans.filledQuantity:
        ans.filledQuantity = Decimal(ans.filledQuantity)
    return ans


def softDollarTier_converter(a_dict):
    ans = SoftDollarTier()
    for key in ['name', 'val', 'displayName']:
        if a_dict[key]:
            setattr(ans, key, a_dict[key])
    return ans


def contract_converter(json_contract):
    py_contract = json.loads(json_contract)
    # print(f'{__name__}::contract_converter: type(ppy_contract)={type(py_contract)} py_contract={py_contract}')
    if isinstance(py_contract, str):
        py_contract = json.loads(py_contract)
    ans = Contract()
    for key in py_contract:
        if key != 'comboLegs' and py_contract[key]:
            setattr(ans, key, py_contract[key])
    for key in py_contract:
        if key == 'comboLegs' and py_contract[key]:
            ans.comboLegs = []
            for leg in py_contract[key]:
                combo_leg = ComboLeg()
                for ky in leg:
                    setattr(combo_leg, ky, leg[ky])
                ans.comboLegs.append(combo_leg)
    # print(ans)
    return ans


def scannerSubscription_converter(json_order):
    py_order = json.loads(json_order)
    ans = ScannerSubscription()
    for key in py_order:
        if py_order[key]:
            setattr(ans, key, py_order[key])
    # print(ans)
    return ans


if __name__ == '__main__':

    myorder = {
        'action': 'BUY',
        'orderType': 'MKT',
        'totalQuantity': 10,
    }
    order_converter(json.dumps(myorder))