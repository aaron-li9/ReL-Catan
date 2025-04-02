from Utility import *
from Enum import *
from Player import Player


class Bank:

    def __init__(self):
        self._resources = np.ones(NUM_RESOURCES) * DEFAULT_BANK_RESOURCE_NUM

    def respond_to_offer(self, requester: Player):
        pass

    def has_enough_resources(self, resource_type: ResourceType, requested_number: int):
        return self._resources[resource_type] >= requested_number
