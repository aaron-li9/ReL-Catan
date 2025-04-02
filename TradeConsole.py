from Utility import *
from Enum import *
from Bank import Bank
from Player import Player


class TradeConsole:

    def __init__(self, bank: Bank):
        self._bank = bank
        self._recipient = None
        self._requester = None
        self._current_trader = None

        self._trade_offer = np.zeros(NUM_RESOURCES).astype(np.int)

        self._center = DEFAULT_CENTER

    def set_requester(self, requester: Player):
        self._requester = requester

    def set_recipient(self, recipient: Player):
        self._recipient = recipient

    def request_player_trade(self, requester, request, recipient, receipt):

        # Default the recipient and requester to None
        self._requester = None
        self._recipient = None

    def request_bank_trade(self, request, receipt):
        pass

    def request_bank_year_of_plenty(self, request):
        pass

    def draw(self, gui):
        pass

    def update(self):
        pass
