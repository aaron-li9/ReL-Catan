from Board import *
from Enum import *
from BoardPieces import NodeBuilding
from Player import Player
from Game import *
from BoardComponents import Tile, Node
from GUI import *
import time


class DummyPlacementModel:
    def __init__(self, game: Game):
        self.game = game

    def query_board_resource_count(self, resource) -> int:
        #used to see how much of a resource there is on board, tells whether a resource is common or rare
        production = 0
        for tile_key in self.game.board.tile_grid:
            tile = self.game.board.tile_grid[tile_key]
            if tile.resource == resource:
                production += ROLL_PRODUCTION_MAP[tile.number]
        return production

    def query_settlement_production(self, node : Node, resource) -> int:
        #tells how much production of a particular resource a node is associated with
        production = 0
        for tile in node.get_tiles():
            if tile.resource == resource:
                production += ROLL_PRODUCTION_MAP[tile.number]
        return production

    def query_total_settlement_production(self, node : Node) -> int:
        #tells how much total production a node is associated with
        production = 0
        for tile in node.get_tiles():
            if tile.resource != ResourceType.DESERT:
                production += ROLL_PRODUCTION_MAP[tile.number]
        return production

    def query_player_resource_count(self, node : Node, resource, player) -> int:
        #holistically considers all of a players settlements, and tells how much production they have of a particular resource
        count = 0
        settlement_list = player.placed_settlements
        for settlement in settlement_list:
            count += self.query_settlement_production(settlement.get_node(), resource)
        count += self.query_settlement_production(node, resource)
        return count


    def player_missing_resource(self, node : Node, resource, player) -> float:
        #used to penalize missing a resource. penalize more after we consider both the players placements holistically
        #because it's not as bad for the first placement to be missing multiple resources (in fact, it always is missing at least 2)
        if self.query_player_resource_count(node, resource, player) == 0 and len(player.placed_settlements) > 0:
            return 1
        else:
            return 0.5


    def production_exponent_index(self, player) -> float:
        #makes it so that the model values production slightly more for the first placement rather than the 2nd placement, so the 2nd
        #placement will be more focused on getting missing/critical resources
        if len(player.placed_settlements) == 0:
            return 4
        elif len(player.placed_settlements) > 0:
            return 3.5

    def query_all_opponent_resource_count(self, resource, player) -> int:
        count = 0
        for player_id in self.game.players:
            if player_id != player.player_id:
                for settlement in self.game.players[player_id].placed_settlements:
                    count += self.query_settlement_production(settlement.get_node(), resource)
        return count

    def evaluate_placement(self, node : Node, player) -> float:
        # score is calculated using a pretty arbitrary function that we made up using our knowledge of the game
        #takes into account aspects such as production, resource rarity, howhow well resources coordinate,
        #how much of a resource a player has relative to the others, and making sure the
        #player has somewhat diverse resource income

        #the goal of this function is to first give reasonable, although not optimal placements, in order to
        #generate boards that will help train the DQN for building actions in the game.

        score = self.query_settlement_production(node, ResourceType.ORE) ** 2 + \
                self.query_settlement_production(node, ResourceType.WHEAT) ** 2 + \
                0.6 * self.query_settlement_production(node, ResourceType.SHEEP) ** 2 + \
                0.8 * self.query_settlement_production(node, ResourceType.WOOD) ** 2 + \
                0.8 * self.query_settlement_production(node, ResourceType.BRICK) ** 2 - \
                self.query_all_opponent_resource_count(ResourceType.ORE, player) ** 2 - \
                self.query_all_opponent_resource_count(ResourceType.WHEAT, player) ** 2 - \
                0.6 * self.query_all_opponent_resource_count(ResourceType.SHEEP, player) ** 2 - \
                0.75 * self.query_all_opponent_resource_count(ResourceType.WOOD, player) ** 2 - \
                0.75 * self.query_all_opponent_resource_count(ResourceType.BRICK, player) ** 2 + \
                50 * (float(self.query_player_resource_count(node, ResourceType.ORE, player)) /
                      float(self.query_board_resource_count(ResourceType.ORE))) ** 2 + \
                60 * (float(self.query_player_resource_count(node, ResourceType.WHEAT, player)) /
                      float(self.query_board_resource_count(ResourceType.WHEAT))) ** 2 + \
                20 * (float(self.query_player_resource_count(node, ResourceType.SHEEP, player)) /
                      float(self.query_board_resource_count(ResourceType.SHEEP))) ** 2 + \
                35 * (float(self.query_player_resource_count(node, ResourceType.WHEAT, player)) /
                      float(self.query_board_resource_count(ResourceType.WHEAT))) ** 2 + \
                40 * (float(self.query_player_resource_count(node, ResourceType.WHEAT, player)) /
                      float(self.query_board_resource_count(ResourceType.WHEAT))) ** 2 + \
                6 * (min(1.00 * self.query_player_resource_count(node, ResourceType.ORE, player),
                         1.33 * self.query_player_resource_count(node, ResourceType.WHEAT, player))) ** 2 + \
                4.5 * (min(1.00 * self.query_player_resource_count(node, ResourceType.WOOD, player),
                           1.00 * self.query_player_resource_count(node, ResourceType.BRICK, player))) ** 2 + \
                12.0 * (min(self.query_player_resource_count(node, ResourceType.ORE, player),
                           self.query_player_resource_count(node, ResourceType.WHEAT, player),
                           2 * self.query_player_resource_count(node, ResourceType.SHEEP, player))) ** 2 - \
                (13 - self.query_total_settlement_production(node)) ** self.production_exponent_index(player) - \
                10 * self.player_missing_resource(node, ResourceType.WHEAT, player) - \
                10 * self.player_missing_resource(node, ResourceType.ORE, player) - \
                4 * self.player_missing_resource(node, ResourceType.SHEEP, player) - \
                7 * self.player_missing_resource(node, ResourceType.WOOD, player) - \
                7 * self.player_missing_resource(node, ResourceType.BRICK, player) + \
                (len(node.tiles) - 1) ** 5

        return score

    def place_settlement(self, player) -> Node:
        # evaluates all the available settlements on the board, then places the one that gives the highest score
        max_score = -1_000_000.0
        curr_max_node = None
        for node in self.game.board.open_settlement_nodes:
            curr_score = self.evaluate_placement(node, player)
            if curr_score > max_score:
                curr_max_node = node
                max_score = curr_score

        player.build_settlement(curr_max_node, self.game.gui, self.game.board, placement=True)  #place the settlement
        possible_road_edges = curr_max_node.edges

        road_node = random.choice(list(possible_road_edges))
        #randomly places a road: not ideal, we'd want a model for it, but for now this is OK as road is often not as big a deal
        player.build_road(road_node, self.game.gui, self.game.board, is_free=True)

        #need to return curr_max_node because the resource distribution function takes a node in as input, so we need
        #to distribute resources based on the node that we placed on (if the placement was a 2nd round placement, which we
        #can easily check)
        return curr_max_node