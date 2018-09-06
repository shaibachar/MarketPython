class Tradable(object):

    def __init__(self,tradableId,bid,ask,bidAmount,AskAmount, updated):
        self.tradableId = tradableId
        self.bid = bid
        self.ask = ask
        self.bidAmount = bidAmount
        self.askAmount = AskAmount
        self.updated = updated

    