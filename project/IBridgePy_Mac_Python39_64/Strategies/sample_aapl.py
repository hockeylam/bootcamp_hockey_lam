from IBridgePy.IbridgepyTools import superSymbol

def initialize(context):
    # Named args guarantee you won't swap anything by mistake
    context.aapl = superSymbol(
        secType='STK',
        symbol='AAPL',
        currency='USD',
        exchange='SMART',
        primaryExchange='NASDAQ'   # optional, but good to be explicit
    )
    context.has_ordered = False

def handle_data(context, data):
    if not context.has_ordered:
        price = data.current(context.aapl, 'price')
        order(context.aapl, 10)
        context.has_ordered = True
        print(f"Ordered 10 AAPL shares at ${price}")