import numpy as np
import random
import math
import pygame
from BoardComponents import *
from BoardPieces import *


class Board:

    def __init__(self):
        self.random_tiles = []
        self.random_harbors = []

        self.board_tile_list = []
        self.board_node_list = []
        self.board_edge_list = []
        self.board_harbor_list = []

        self.available_node_list = []
        self.available_edge_list = []

        self.settlements = []
        self.cities = []
        self.roads = []

        self.robber = Robber()

        self.tile_width = 80

        # Center of the board
        self.x = 0
        self.y = 0

    # RANDOM BOARD GENERATION FUNCTIONS
    def generate_tiles(self):
        resources_list = {'WOOD': 4, 'WHEAT': 4, 'SHEEP': 4, 'ORE': 3, 'BRICK': 3}
        numbers_list = {2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 1}

        resources = list(x for x in resources_list.keys() for i in range(resources_list[x]))
        numbers = list(x for x in numbers_list.keys() for i in range(numbers_list[x]))

        random.shuffle(resources)
        random.shuffle(numbers)

        tile_register = list([resource, number] for resource, number in zip(resources, numbers))
        tile_register.append(['DESERT', None])

        self.random_tiles = np.asarray(tile_register)

    def generate_harbors(self):
        harbors_list = {'3FOR1': 4, 'WOOD_H': 1, 'WHEAT_H': 1, 'SHEEP_H': 1, 'ORE_H': 1, 'BRICK_H': 1}
        harbors = list(x for x in harbors_list.keys() for i in range(harbors_list[x]))

        random.shuffle(harbors)

        self.random_harbors = harbors

    def generate_tile_deck(self):
        td = []
        for tile_config in self.random_tiles:
            resource = tile_config[0]
            number = tile_config[1]
            tile = Tile(resource, number)
            if resource == 'DESERT':
                self.robber.place_on_tile(tile)
            td.append(tile)
        return td

    def generate_harbor_deck(self):
        hd = []
        for harbor_name in self.random_harbors:
            hd.append(Harbor(harbor_name))
        return hd

    def generate_random_board(self):
        self.generate_harbors()
        self.generate_tiles()
        self.generate_skeleton()

    # LINKING OF BOARD SKELETON FUNCTIONS
    @staticmethod
    def link_tile(tile_1, tile_2):
        tile_1.tiles.append(tile_2)
        tile_2.tiles.append(tile_1)

    @staticmethod
    def link_edge(edge, node_1, node_2):
        edge.nodes.append(node_1)
        edge.nodes.append(node_2)
        node_1.edges.append(edge)
        node_2.edges.append(edge)

    @staticmethod
    def is_valid_tile_placement(tile, link_tile_list):
        has_red_tile = False

        for link_tile in link_tile_list:
            number = link_tile.number
            if number == 6 or number == 8:
                has_red_tile = True

        if has_red_tile:
            if tile.number == 6 or tile.number == 8:
                return False
        return True

    def link_tiles(self, td):
        head_tile = td.pop()
        location_list = [head_tile]

        # First Row
        for i in range(2):
            prev_tile_list = [location_list[-1]]
            tile = td.pop()

            while not self.is_valid_tile_placement(tile, prev_tile_list):
                new_tile = td[0]
                td = td[1:]
                td.append(tile)
                tile = new_tile

            for prev_tile in prev_tile_list:
                self.link_tile(prev_tile, tile)

            location_list.append(tile)
        print('First Row Complete')
        # Second Row
        for i in range(3, 7):
            tile = td.pop()
            prev_tile_list = []

            if i == 3:
                prev_tile_list.append(location_list[0])
            elif i == 6:
                prev_tile_list.append(location_list[2])
                prev_tile_list.append(location_list[-1])
            else:
                prev_tile_list.append(location_list[i - 4])
                prev_tile_list.append(location_list[i - 3])
                prev_tile_list.append(location_list[-1])

            while not self.is_valid_tile_placement(tile, prev_tile_list):
                new_tile = td[0]
                td = td[1:]
                td.append(tile)
                tile = new_tile

            for prev_tile in prev_tile_list:
                self.link_tile(prev_tile, tile)

            location_list.append(tile)
        print('Second Row Complete')
        # Third Row
        for i in range(7, 12):
            tile = td.pop()

            prev_tile_list = []

            if i == 7:
                prev_tile_list.append(location_list[3])
            elif i == 11:
                prev_tile_list.append(location_list[6])
                prev_tile_list.append(location_list[-1])
            else:
                prev_tile_list.append(location_list[i - 5])
                prev_tile_list.append(location_list[i - 4])
                prev_tile_list.append(location_list[-1])

            while not self.is_valid_tile_placement(tile, prev_tile_list):
                new_tile = td[0]
                td = td[1:]
                td.append(tile)
                tile = new_tile

            for prev_tile in prev_tile_list:
                self.link_tile(prev_tile, tile)

            location_list.append(tile)
        print('Third Row Complete')
        # Fourth Row
        for i in range(12, 16):
            tile = td.pop()

            prev_tile_list = []

            if i == 12:
                prev_tile_list.append(location_list[7])
                prev_tile_list.append(location_list[8])
            else:
                prev_tile_list.append(location_list[i - 5])
                prev_tile_list.append(location_list[i - 4])
                prev_tile_list.append(location_list[-1])

            while not self.is_valid_tile_placement(tile, prev_tile_list):
                new_tile = td[0]
                td = td[1:]
                td.append(tile)
                tile = new_tile

            for prev_tile in prev_tile_list:
                self.link_tile(prev_tile, tile)

            location_list.append(tile)
        print('Fourth Row Complete')
        # Fifth Row
        for i in range(16, 19):
            tile = td.pop()

            prev_tile_list = []

            if i == 16:
                prev_tile_list.append(location_list[12])
                prev_tile_list.append(location_list[13])
            else:
                prev_tile_list.append(location_list[i - 4])
                prev_tile_list.append(location_list[i - 3])
                prev_tile_list.append(location_list[-1])

            if not self.is_valid_tile_placement(tile, prev_tile_list):
                print('Special Case Board')
                for placed_tile in location_list:
                    if self.is_valid_tile_placement(tile, placed_tile.tiles) \
                            and self.is_valid_tile_placement(placed_tile, prev_tile_list):
                        # Couple the new tile
                        tile.tiles = placed_tile.tiles

                        ## Update adjacent tiles => Remove old tile and add new tile
                        for adjacent_tile in placed_tile.tiles:
                            adjacent_tile.tiles.remove(placed_tile)
                            adjacent_tile.tiles.append(tile)

                        # Update location list
                        index = location_list.index(placed_tile)
                        location_list[index] = tile

                        # Recouple the old tile onto the last placement
                        placed_tile.tiles = []
                        tile = placed_tile

            for prev_tile in prev_tile_list:
                self.link_tile(prev_tile, tile)

            location_list.append(tile)
        print('Fifth Row Complete')
        self.board_tile_list = location_list
        print('Linked Tiles')

    def link_nodes(self):

        num_nodes = 54

        # Initialize Node Web
        for i in range(num_nodes):
            self.board_node_list.append(Node())

        # for each node, specify the tiles that the node is touching
        for i in range(len(self.board_node_list)):
            if i == 0 or i == 1 or i == 2:
                self.board_node_list[i].tiles.append(self.board_tile_list[i])
            elif i == 3:
                self.board_node_list[i].tiles.append(self.board_tile_list[0])
            elif i == 4:
                self.board_node_list[i].tiles.append(self.board_tile_list[0])
                self.board_node_list[i].tiles.append(self.board_tile_list[1])
            elif i == 5:
                self.board_node_list[i].tiles.append(self.board_tile_list[1])
                self.board_node_list[i].tiles.append(self.board_tile_list[2])
            elif i == 6:
                self.board_node_list[i].tiles.append(self.board_tile_list[2])
            elif i == 7:
                self.board_node_list[i].tiles.append(self.board_tile_list[0])
                self.board_node_list[i].tiles.append(self.board_tile_list[3])
            elif i == 8:
                self.board_node_list[i].tiles.append(self.board_tile_list[0])
                self.board_node_list[i].tiles.append(self.board_tile_list[1])
                self.board_node_list[i].tiles.append(self.board_tile_list[4])
            elif i == 9:
                self.board_node_list[i].tiles.append(self.board_tile_list[1])
                self.board_node_list[i].tiles.append(self.board_tile_list[2])
                self.board_node_list[i].tiles.append(self.board_tile_list[5])
            elif i == 10:
                self.board_node_list[i].tiles.append(self.board_tile_list[2])
                self.board_node_list[i].tiles.append(self.board_tile_list[6])
            elif i == 11:
                self.board_node_list[i].tiles.append(self.board_tile_list[3])
            elif i == 12:
                self.board_node_list[i].tiles.append(self.board_tile_list[0])
                self.board_node_list[i].tiles.append(self.board_tile_list[3])
                self.board_node_list[i].tiles.append(self.board_tile_list[4])
            elif i == 13:
                self.board_node_list[i].tiles.append(self.board_tile_list[1])
                self.board_node_list[i].tiles.append(self.board_tile_list[4])
                self.board_node_list[i].tiles.append(self.board_tile_list[5])
            elif i == 14:
                self.board_node_list[i].tiles.append(self.board_tile_list[2])
                self.board_node_list[i].tiles.append(self.board_tile_list[5])
                self.board_node_list[i].tiles.append(self.board_tile_list[6])
            elif i == 15:
                self.board_node_list[i].tiles.append(self.board_tile_list[6])
            elif i == 16:
                self.board_node_list[i].tiles.append(self.board_tile_list[3])
                self.board_node_list[i].tiles.append(self.board_tile_list[7])
            elif i == 17:
                self.board_node_list[i].tiles.append(self.board_tile_list[3])
                self.board_node_list[i].tiles.append(self.board_tile_list[4])
                self.board_node_list[i].tiles.append(self.board_tile_list[8])
            elif i == 18:
                self.board_node_list[i].tiles.append(self.board_tile_list[4])
                self.board_node_list[i].tiles.append(self.board_tile_list[5])
                self.board_node_list[i].tiles.append(self.board_tile_list[9])
            elif i == 19:
                self.board_node_list[i].tiles.append(self.board_tile_list[5])
                self.board_node_list[i].tiles.append(self.board_tile_list[6])
                self.board_node_list[i].tiles.append(self.board_tile_list[10])
            elif i == 20:
                self.board_node_list[i].tiles.append(self.board_tile_list[6])
                self.board_node_list[i].tiles.append(self.board_tile_list[11])
            elif i == 21:
                self.board_node_list[i].tiles.append(self.board_tile_list[7])
            elif i == 22:
                self.board_node_list[i].tiles.append(self.board_tile_list[3])
                self.board_node_list[i].tiles.append(self.board_tile_list[7])
                self.board_node_list[i].tiles.append(self.board_tile_list[8])
            elif i == 23:
                self.board_node_list[i].tiles.append(self.board_tile_list[4])
                self.board_node_list[i].tiles.append(self.board_tile_list[8])
                self.board_node_list[i].tiles.append(self.board_tile_list[9])
            elif i == 24:
                self.board_node_list[i].tiles.append(self.board_tile_list[5])
                self.board_node_list[i].tiles.append(self.board_tile_list[9])
                self.board_node_list[i].tiles.append(self.board_tile_list[10])
            elif i == 25:
                self.board_node_list[i].tiles.append(self.board_tile_list[6])
                self.board_node_list[i].tiles.append(self.board_tile_list[10])
                self.board_node_list[i].tiles.append(self.board_tile_list[11])
            elif i == 26:
                self.board_node_list[i].tiles.append(self.board_tile_list[11])
            elif i == 27:
                self.board_node_list[i].tiles.append(self.board_tile_list[7])
            elif i == 28:
                self.board_node_list[i].tiles.append(self.board_tile_list[7])
                self.board_node_list[i].tiles.append(self.board_tile_list[8])
                self.board_node_list[i].tiles.append(self.board_tile_list[12])
            elif i == 29:
                self.board_node_list[i].tiles.append(self.board_tile_list[8])
                self.board_node_list[i].tiles.append(self.board_tile_list[9])
                self.board_node_list[i].tiles.append(self.board_tile_list[13])
            elif i == 30:
                self.board_node_list[i].tiles.append(self.board_tile_list[9])
                self.board_node_list[i].tiles.append(self.board_tile_list[10])
                self.board_node_list[i].tiles.append(self.board_tile_list[14])
            elif i == 31:
                self.board_node_list[i].tiles.append(self.board_tile_list[10])
                self.board_node_list[i].tiles.append(self.board_tile_list[11])
                self.board_node_list[i].tiles.append(self.board_tile_list[15])
            elif i == 32:
                self.board_node_list[i].tiles.append(self.board_tile_list[11])
            elif i == 33:
                self.board_node_list[i].tiles.append(self.board_tile_list[7])
                self.board_node_list[i].tiles.append(self.board_tile_list[12])
            elif i == 34:
                self.board_node_list[i].tiles.append(self.board_tile_list[8])
                self.board_node_list[i].tiles.append(self.board_tile_list[12])
                self.board_node_list[i].tiles.append(self.board_tile_list[13])
            elif i == 35:
                self.board_node_list[i].tiles.append(self.board_tile_list[9])
                self.board_node_list[i].tiles.append(self.board_tile_list[13])
                self.board_node_list[i].tiles.append(self.board_tile_list[14])
            elif i == 36:
                self.board_node_list[i].tiles.append(self.board_tile_list[10])
                self.board_node_list[i].tiles.append(self.board_tile_list[14])
                self.board_node_list[i].tiles.append(self.board_tile_list[15])
            elif i == 37:
                self.board_node_list[i].tiles.append(self.board_tile_list[11])
                self.board_node_list[i].tiles.append(self.board_tile_list[15])
            elif i == 38:
                self.board_node_list[i].tiles.append(self.board_tile_list[12])
            elif i == 39:
                self.board_node_list[i].tiles.append(self.board_tile_list[12])
                self.board_node_list[i].tiles.append(self.board_tile_list[13])
                self.board_node_list[i].tiles.append(self.board_tile_list[16])
            elif i == 40:
                self.board_node_list[i].tiles.append(self.board_tile_list[13])
                self.board_node_list[i].tiles.append(self.board_tile_list[14])
                self.board_node_list[i].tiles.append(self.board_tile_list[17])
            elif i == 41:
                self.board_node_list[i].tiles.append(self.board_tile_list[14])
                self.board_node_list[i].tiles.append(self.board_tile_list[15])
                self.board_node_list[i].tiles.append(self.board_tile_list[18])
            elif i == 42:
                self.board_node_list[i].tiles.append(self.board_tile_list[15])
            elif i == 43:
                self.board_node_list[i].tiles.append(self.board_tile_list[12])
                self.board_node_list[i].tiles.append(self.board_tile_list[16])
            elif i == 44:
                self.board_node_list[i].tiles.append(self.board_tile_list[13])
                self.board_node_list[i].tiles.append(self.board_tile_list[16])
                self.board_node_list[i].tiles.append(self.board_tile_list[17])
            elif i == 45:
                self.board_node_list[i].tiles.append(self.board_tile_list[14])
                self.board_node_list[i].tiles.append(self.board_tile_list[17])
                self.board_node_list[i].tiles.append(self.board_tile_list[18])
            elif i == 46:
                self.board_node_list[i].tiles.append(self.board_tile_list[15])
                self.board_node_list[i].tiles.append(self.board_tile_list[18])
            elif i == 47:
                self.board_node_list[i].tiles.append(self.board_tile_list[16])
            elif i == 48:
                self.board_node_list[i].tiles.append(self.board_tile_list[16])
                self.board_node_list[i].tiles.append(self.board_tile_list[17])
            elif i == 49:
                self.board_node_list[i].tiles.append(self.board_tile_list[17])
                self.board_node_list[i].tiles.append(self.board_tile_list[18])
            elif i == 50:
                self.board_node_list[i].tiles.append(self.board_tile_list[18])
            elif i == 51 or i == 52 or i == 53:
                self.board_node_list[i].tiles.append(self.board_tile_list[i - 35])

        # for each tile, specify the nodes that it is touching
        for i in range(len(self.board_tile_list)):
            if i == 0:
                self.board_tile_list[i].nodes.append(self.board_node_list[0])
                self.board_tile_list[i].nodes.append(self.board_node_list[3])
                self.board_tile_list[i].nodes.append(self.board_node_list[4])
                self.board_tile_list[i].nodes.append(self.board_node_list[7])
                self.board_tile_list[i].nodes.append(self.board_node_list[8])
                self.board_tile_list[i].nodes.append(self.board_node_list[12])
            elif i == 1:
                self.board_tile_list[i].nodes.append(self.board_node_list[1])
                self.board_tile_list[i].nodes.append(self.board_node_list[4])
                self.board_tile_list[i].nodes.append(self.board_node_list[5])
                self.board_tile_list[i].nodes.append(self.board_node_list[8])
                self.board_tile_list[i].nodes.append(self.board_node_list[9])
                self.board_tile_list[i].nodes.append(self.board_node_list[13])
            elif i == 2:
                self.board_tile_list[i].nodes.append(self.board_node_list[2])
                self.board_tile_list[i].nodes.append(self.board_node_list[5])
                self.board_tile_list[i].nodes.append(self.board_node_list[6])
                self.board_tile_list[i].nodes.append(self.board_node_list[9])
                self.board_tile_list[i].nodes.append(self.board_node_list[10])
                self.board_tile_list[i].nodes.append(self.board_node_list[14])
            elif i == 3:
                self.board_tile_list[i].nodes.append(self.board_node_list[7])
                self.board_tile_list[i].nodes.append(self.board_node_list[11])
                self.board_tile_list[i].nodes.append(self.board_node_list[12])
                self.board_tile_list[i].nodes.append(self.board_node_list[16])
                self.board_tile_list[i].nodes.append(self.board_node_list[17])
                self.board_tile_list[i].nodes.append(self.board_node_list[22])
            elif i == 4:
                self.board_tile_list[i].nodes.append(self.board_node_list[8])
                self.board_tile_list[i].nodes.append(self.board_node_list[12])
                self.board_tile_list[i].nodes.append(self.board_node_list[13])
                self.board_tile_list[i].nodes.append(self.board_node_list[17])
                self.board_tile_list[i].nodes.append(self.board_node_list[18])
                self.board_tile_list[i].nodes.append(self.board_node_list[23])
            elif i == 5:
                self.board_tile_list[i].nodes.append(self.board_node_list[9])
                self.board_tile_list[i].nodes.append(self.board_node_list[13])
                self.board_tile_list[i].nodes.append(self.board_node_list[14])
                self.board_tile_list[i].nodes.append(self.board_node_list[18])
                self.board_tile_list[i].nodes.append(self.board_node_list[19])
                self.board_tile_list[i].nodes.append(self.board_node_list[24])
            elif i == 6:
                self.board_tile_list[i].nodes.append(self.board_node_list[10])
                self.board_tile_list[i].nodes.append(self.board_node_list[14])
                self.board_tile_list[i].nodes.append(self.board_node_list[15])
                self.board_tile_list[i].nodes.append(self.board_node_list[19])
                self.board_tile_list[i].nodes.append(self.board_node_list[20])
                self.board_tile_list[i].nodes.append(self.board_node_list[25])
            elif i == 7:
                self.board_tile_list[i].nodes.append(self.board_node_list[16])
                self.board_tile_list[i].nodes.append(self.board_node_list[21])
                self.board_tile_list[i].nodes.append(self.board_node_list[22])
                self.board_tile_list[i].nodes.append(self.board_node_list[27])
                self.board_tile_list[i].nodes.append(self.board_node_list[28])
                self.board_tile_list[i].nodes.append(self.board_node_list[33])
            elif i == 8:
                self.board_tile_list[i].nodes.append(self.board_node_list[17])
                self.board_tile_list[i].nodes.append(self.board_node_list[22])
                self.board_tile_list[i].nodes.append(self.board_node_list[23])
                self.board_tile_list[i].nodes.append(self.board_node_list[28])
                self.board_tile_list[i].nodes.append(self.board_node_list[29])
                self.board_tile_list[i].nodes.append(self.board_node_list[34])
            elif i == 9:
                self.board_tile_list[i].nodes.append(self.board_node_list[18])
                self.board_tile_list[i].nodes.append(self.board_node_list[23])
                self.board_tile_list[i].nodes.append(self.board_node_list[24])
                self.board_tile_list[i].nodes.append(self.board_node_list[29])
                self.board_tile_list[i].nodes.append(self.board_node_list[30])
                self.board_tile_list[i].nodes.append(self.board_node_list[35])
            elif i == 10:
                self.board_tile_list[i].nodes.append(self.board_node_list[19])
                self.board_tile_list[i].nodes.append(self.board_node_list[24])
                self.board_tile_list[i].nodes.append(self.board_node_list[25])
                self.board_tile_list[i].nodes.append(self.board_node_list[30])
                self.board_tile_list[i].nodes.append(self.board_node_list[31])
                self.board_tile_list[i].nodes.append(self.board_node_list[36])
            elif i == 11:
                self.board_tile_list[i].nodes.append(self.board_node_list[20])
                self.board_tile_list[i].nodes.append(self.board_node_list[25])
                self.board_tile_list[i].nodes.append(self.board_node_list[26])
                self.board_tile_list[i].nodes.append(self.board_node_list[31])
                self.board_tile_list[i].nodes.append(self.board_node_list[32])
                self.board_tile_list[i].nodes.append(self.board_node_list[37])
            elif i == 12:
                self.board_tile_list[i].nodes.append(self.board_node_list[28])
                self.board_tile_list[i].nodes.append(self.board_node_list[33])
                self.board_tile_list[i].nodes.append(self.board_node_list[34])
                self.board_tile_list[i].nodes.append(self.board_node_list[38])
                self.board_tile_list[i].nodes.append(self.board_node_list[39])
                self.board_tile_list[i].nodes.append(self.board_node_list[43])
            elif i == 13:
                self.board_tile_list[i].nodes.append(self.board_node_list[29])
                self.board_tile_list[i].nodes.append(self.board_node_list[34])
                self.board_tile_list[i].nodes.append(self.board_node_list[35])
                self.board_tile_list[i].nodes.append(self.board_node_list[39])
                self.board_tile_list[i].nodes.append(self.board_node_list[40])
                self.board_tile_list[i].nodes.append(self.board_node_list[44])
            elif i == 14:
                self.board_tile_list[i].nodes.append(self.board_node_list[30])
                self.board_tile_list[i].nodes.append(self.board_node_list[35])
                self.board_tile_list[i].nodes.append(self.board_node_list[36])
                self.board_tile_list[i].nodes.append(self.board_node_list[40])
                self.board_tile_list[i].nodes.append(self.board_node_list[41])
                self.board_tile_list[i].nodes.append(self.board_node_list[45])
            elif i == 15:
                self.board_tile_list[i].nodes.append(self.board_node_list[31])
                self.board_tile_list[i].nodes.append(self.board_node_list[36])
                self.board_tile_list[i].nodes.append(self.board_node_list[37])
                self.board_tile_list[i].nodes.append(self.board_node_list[41])
                self.board_tile_list[i].nodes.append(self.board_node_list[42])
                self.board_tile_list[i].nodes.append(self.board_node_list[46])
            elif i == 16:
                self.board_tile_list[i].nodes.append(self.board_node_list[39])
                self.board_tile_list[i].nodes.append(self.board_node_list[43])
                self.board_tile_list[i].nodes.append(self.board_node_list[44])
                self.board_tile_list[i].nodes.append(self.board_node_list[47])
                self.board_tile_list[i].nodes.append(self.board_node_list[48])
                self.board_tile_list[i].nodes.append(self.board_node_list[51])
            elif i == 17:
                self.board_tile_list[i].nodes.append(self.board_node_list[40])
                self.board_tile_list[i].nodes.append(self.board_node_list[44])
                self.board_tile_list[i].nodes.append(self.board_node_list[45])
                self.board_tile_list[i].nodes.append(self.board_node_list[48])
                self.board_tile_list[i].nodes.append(self.board_node_list[49])
                self.board_tile_list[i].nodes.append(self.board_node_list[52])
            elif i == 18:
                self.board_tile_list[i].nodes.append(self.board_node_list[41])
                self.board_tile_list[i].nodes.append(self.board_node_list[45])
                self.board_tile_list[i].nodes.append(self.board_node_list[46])
                self.board_tile_list[i].nodes.append(self.board_node_list[49])
                self.board_tile_list[i].nodes.append(self.board_node_list[50])
                self.board_tile_list[i].nodes.append(self.board_node_list[53])
        self.available_node_list = self.board_node_list

        print('Linked Nodes')

    def link_edges(self):
        edge_nodes_map = {0: [3, 0], 1: [4, 0], 2: [4, 1], 3: [5, 1], 4: [5, 2], 5: [6, 2],
                          6: [7, 3], 7: [8, 4], 8: [9, 5], 9: [10, 6],
                          10: [11, 7], 11: [12, 7], 12: [12, 8], 13: [13, 8], 14: [13, 9], 15: [14, 9], 16: [14, 10], 17: [15, 10],
                          18: [16, 11], 19: [17, 12], 20: [18, 13], 21: [19, 14], 22: [20, 15],
                          23: [21, 16], 24: [22, 16], 25: [22, 17], 26: [23, 17], 27: [23, 18], 28: [24, 18], 29: [24, 19], 30: [25, 19], 31: [25, 20], 32: [26, 20],
                          33: [27, 21], 34: [28, 22], 35: [29, 23], 36: [30, 24], 37: [31, 25], 38: [32, 26],
                          39: [33, 27], 40: [33, 28], 41: [34, 28], 42: [34, 29], 43: [35, 29], 44: [35, 30], 45: [36, 30], 46: [36, 31], 47: [37, 31], 48: [37, 32],
                          49: [38, 33], 50: [39, 34], 51: [40, 35], 52: [41, 36], 53: [42, 37],
                          54: [43, 38], 55: [43, 39], 56: [44, 39], 57: [44, 40], 58: [45, 40], 59: [45, 41], 60: [46, 41], 61: [46, 42],
                          62: [47, 43], 63: [48, 44], 64: [49, 45], 65: [50, 46],
                          66: [51, 47], 67: [51, 48], 68: [52, 48], 69: [52, 49], 70: [53, 49], 71: [53, 50]}

        num_edges = 72

        for i in range(num_edges):
            edge = Edge()
            nodes_indices = edge_nodes_map[i]
            node_1 = self.board_node_list[nodes_indices[0]]
            node_2 = self.board_node_list[nodes_indices[1]]
            self.link_edge(edge, node_1, node_2)
            self.board_edge_list.append(edge)
        self.available_edge_list = self.board_edge_list

    def link_nodes_to_harbors(self, hd):
        num_harbors = 9
        # Make the nodes touch their corresponding ports
        for i in range(num_harbors):
            curr_harbor = hd.pop()
            if i == 0:
                self.board_node_list[0].harbor = curr_harbor
                self.board_node_list[3].harbor = curr_harbor
                curr_harbor.nodes.append(self.board_node_list[0])
                curr_harbor.nodes.append(self.board_node_list[3])
            elif i == 1:
                self.board_node_list[1].harbor = curr_harbor
                self.board_node_list[5].harbor = curr_harbor
                curr_harbor.nodes.append(self.board_node_list[1])
                curr_harbor.nodes.append(self.board_node_list[5])
            elif i == 2:
                self.board_node_list[10].harbor = curr_harbor
                self.board_node_list[15].harbor = curr_harbor
                curr_harbor.nodes.append(self.board_node_list[10])
                curr_harbor.nodes.append(self.board_node_list[15])
            elif i == 3:
                self.board_node_list[11].harbor = curr_harbor
                self.board_node_list[16].harbor = curr_harbor
                curr_harbor.nodes.append(self.board_node_list[11])
                curr_harbor.nodes.append(self.board_node_list[16])
            elif i == 4:
                self.board_node_list[26].harbor = curr_harbor
                self.board_node_list[32].harbor = curr_harbor
                curr_harbor.nodes.append(self.board_node_list[26])
                curr_harbor.nodes.append(self.board_node_list[32])
            elif i == 5:
                self.board_node_list[33].harbor = curr_harbor
                self.board_node_list[38].harbor = curr_harbor
                curr_harbor.nodes.append(self.board_node_list[33])
                curr_harbor.nodes.append(self.board_node_list[38])
            elif i == 6:
                self.board_node_list[42].harbor = curr_harbor
                self.board_node_list[46].harbor = curr_harbor
                curr_harbor.nodes.append(self.board_node_list[42])
                curr_harbor.nodes.append(self.board_node_list[46])
            elif i == 7:
                self.board_node_list[47].harbor = curr_harbor
                self.board_node_list[51].harbor = curr_harbor
                curr_harbor.nodes.append(self.board_node_list[47])
                curr_harbor.nodes.append(self.board_node_list[51])
            elif i == 8:
                self.board_node_list[49].harbor = curr_harbor
                self.board_node_list[52].harbor = curr_harbor
                curr_harbor.nodes.append(self.board_node_list[49])
                curr_harbor.nodes.append(self.board_node_list[52])
            self.board_harbor_list.append(curr_harbor)

    def generate_skeleton(self):
        tile_deck = self.generate_tile_deck()
        random.shuffle(tile_deck)

        harbor_deck = self.generate_harbor_deck()
        random.shuffle(harbor_deck)

        self.link_tiles(tile_deck)
        self.link_nodes()
        self.link_edges()
        self.link_nodes_to_harbors(harbor_deck)

        self.set_object_centers()
        print('Completed Skeleton')

    # DEFINING BOARD PIECE LOCATION FUNCTIONS
    def set_board_center(self, x, y):
        self.x = x
        self.y = y

    def set_tile_centers(self):
        x_step = self.tile_width * math.cos(math.pi / 6)
        y_step = self.tile_width * (1 + math.sin(math.pi / 6))

        step_map_tile = {0: [-2, -2], 1: [0, -2], 2: [2, -2],
                         3: [-3, -1], 4: [-1, -1], 5: [1, -1], 6: [3, -1],
                         7: [-4, 0], 8: [-2, 0], 9: [0, 0], 10: [2, 0], 11: [4, 0],
                         12: [-3, 1], 13: [-1, 1], 14: [1, 1], 15: [3, 1],
                         16: [-2, 2], 17: [0, 2], 18: [2, 2]}

        for index in range(len(self.board_tile_list)):
            tile = self.board_tile_list[index]
            step_scale = step_map_tile[index]

            x = self.x + x_step * step_scale[0]
            y = self.y + y_step * step_scale[1]

            tile.set_center(x, y)

    def set_node_centers(self):
        x_step = self.tile_width * math.cos(math.pi / 6)
        y_step = self.tile_width * math.sin(math.pi / 6)

        step_map_node = {0: [-2, -8], 1: [0, -8], 2: [2, -8],
                         3: [-3, -7], 4: [-1, -7], 5: [1, -7], 6: [3, -7],
                         7: [-3, -5], 8: [-1, -5], 9: [1, -5], 10: [3, -5],
                         11: [-4, -4], 12: [-2, -4], 13: [0, -4], 14: [2, -4], 15: [4, -4],
                         16: [-4, -2], 17: [-2, -2], 18: [0, -2], 19: [2, -2], 20: [4, -2],
                         21: [-5, -1], 22: [-3, -1], 23: [-1, -1], 24: [1, -1], 25: [3, -1], 26: [5, -1],
                         27: [-5, 1], 28: [-3, 1], 29: [-1, 1], 30: [1, 1], 31: [3, 1], 32: [5, 1],
                         33: [-4, 2], 34: [-2, 2], 35: [0, 2], 36: [2, 2], 37: [4, 2],
                         38: [-4, 4], 39: [-2, 4], 40: [0, 4], 41: [2, 4], 42: [4, 4],
                         43: [-3, 5], 44: [-1, 5], 45: [1, 5], 46: [3, 5],
                         47: [-3, 7], 48: [-1, 7], 49: [1, 7], 50: [3, 7],
                         51: [-2, 8], 52: [0, 8], 53: [2, 8]}

        for index in range(len(self.board_node_list)):
            node = self.board_node_list[index]
            step_scale = step_map_node[index]

            x = self.x + x_step * step_scale[0]
            y = self.y + y_step * step_scale[1]

            node.set_center(x, y)

    def set_edge_centers(self):
        x_step = (self.tile_width * math.cos(math.pi / 6)) / 2
        y_step = (self.tile_width * math.sin(math.pi / 6)) / 2

        step_map_edge = {0: [-5, -15], 1: [-3, -15], 2: [-1, -15], 3: [1, -15], 4: [3, -15], 5: [5, -15],
                         6: [-6, -12], 7: [-2, -12], 8: [2, -12], 9: [6, -12],
                         10: [-7, -9], 11: [-5, -9], 12: [-3, -9], 13: [-1, -9], 14: [1, -9], 15: [3, -9], 16: [5, -9],
                         17: [7, -9],
                         18: [-8, -6], 19: [-4, -6], 20: [0, -6], 21: [4, -6], 22: [8, -6],
                         23: [-9, -3], 24: [-7, -3], 25: [-5, -3], 26: [-3, -3], 27: [-1, -3], 28: [1, -3], 29: [3, -3],
                         30: [5, -3], 31: [7, -3], 32: [9, -3],
                         33: [-10, 0], 34: [-6, 0], 35: [-2, 0], 36: [2, 0], 37: [6, 0], 38: [10, 0],
                         39: [-9, 3], 40: [-7, 3], 41: [-5, 3], 42: [-3, 3], 43: [-1, 3], 44: [1, 3], 45: [3, 3],
                         46: [5, 3], 47: [7, 3], 48: [9, 3],
                         49: [-8, 6], 50: [-4, 6], 51: [0, 6], 52: [4, 6], 53: [8, 6],
                         54: [-7, 9], 55: [-5, 9], 56: [-3, 9], 57: [-1, 9], 58: [1, 9], 59: [3, 9], 60: [5, 9],
                         61: [7, 9],
                         62: [-6, 12], 63: [-2, 12], 64: [2, 12], 65: [6, 12],
                         66: [-5, 15], 67: [-3, 15], 68: [-1, 15], 69: [1, 15], 70: [3, 15], 71: [5, 15]}
        for index in range(len(self.board_edge_list)):
            edge = self.board_edge_list[index]
            step_scale = step_map_edge[index]

            x = self.x + x_step * step_scale[0]
            y = self.y + y_step * step_scale[1]

            edge.set_center(x, y)

    def set_harbor_centers(self):
        x_step = self.tile_width * math.cos(math.pi / 6)
        y_step = self.tile_width * (1 + math.sin(math.pi / 6))

        step_map_tile = {0: [-3, -3], 1: [1, -3], 2: [4, -2],
                         3: [-5, -1], 4: [6, 0], 5: [-5, 1], 6: [4, 2],
                         7: [-3, 3], 8: [1, 3]}
        for index in range(len(self.board_harbor_list)):
            harbor = self.board_harbor_list[index]
            step_scale = step_map_tile[index]
            x = self.x + x_step * step_scale[0]
            y = self.y + y_step * step_scale[1]

            harbor.set_center(x, y)

    def set_object_centers(self):
        self.set_tile_centers()
        self.set_node_centers()
        self.set_edge_centers()
        self.set_harbor_centers()

    # NODE/EDGE AVAILABILITY DETECTION FUNCTIONS
    def get_node_availability(self):
        return self.available_node_list

    def remove_node_availability(self, node):
        unavailable_nodes = [node]

        for edge in node.edges:
            for edge_node in edge.nodes:
                if edge_node != node and edge_node in self.available_node_list:
                    unavailable_nodes.append(edge_node)

        for unavailable_node in unavailable_nodes:
            self.available_node_list.remove(unavailable_node)

    def remove_edge_availability(self, edge):
        if edge in self.available_edge_list:
            self.available_edge_list.remove(edge)

    def get_edge_availability(self, node, player):
        available_edges = []

        eligible = False

        if node.settlement is not None:
            if node.settlement.player == player:
                eligible = True
        elif len(node.edges) > 0:
            for edge in node.edge:
                if edge.road is not None and edge.road.player == player:
                    eligible = True

        if eligible:
            # Check if each edge is in available edge list
            for edge in node.edges:
                if edge in self.available_edge_list:
                    available_edges.append(edge)

        return available_edges

    # SIZE CUSTOMIZATION FUNCTIONS
    def set_tile_width(self, width):
        self.tile_width = width

    # GUI FUNCTIONS
    def get_center(self):
        return self.x, self.y

    def draw(self, gui):
        background_color = (0, 140, 255)
        gui.screen.fill(background_color)

        for tile in self.board_tile_list:
            tile.draw(gui)

        for harbor in self.board_harbor_list:
            harbor.draw(gui)

        for road in self.roads:
            road.draw(gui)

        for settlement in self.settlements:
            settlement.draw(gui)


        '''
        for edge in self.board_edge_list:
            edge.draw(gui)

        for node in self.board_node_list:
            node.draw(gui)
        '''

        self.robber.draw(gui)

        pygame.display.update()

        # Save drawn board
        pygame.image.save(gui.screen, 'Board.png')
        gui.board_image = pygame.image.load('Board.png')


class Vector:

    def __init__(self, x1, y1, x2, y2):
        self.vector = (float(x2 - x1), float(y2 - y1))
        self.magnitude = math.sqrt(sum(s ** 2 for s in self.vector))
        self.midpoint = (float((x1 + x2) / 2), float((y1 + y2) / 2))
        self.unit_vector = tuple(x * (1 / self.magnitude) for x in self.vector)
        self.unit_normal = (self.unit_vector[1], -self.unit_vector[0])


class GUI:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen_dimensions = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.images = {}
        self.load_images()

        self.board = None
        self.board_image = None

    def initialize_board(self, board):
        self.board = board
        self.board.draw(self)

    def reset_board(self):
        x = self.screen_dimensions[0] / 2
        y = self.screen_dimensions[1] / 2
        image_rect = self.board_image.get_rect(center=(x, y))
        self.screen.blit(self.board_image, image_rect)

    def load_images(self):
        image_paths = {'WHEAT': 'Images/Wheat.png',
                       'WHEAT_H': 'Images/Wheat_24px.png',
                       'WOOD': 'Images/Wood.png',
                       'WOOD_H': 'Images/Wood_24px.png',
                       'ORE': 'Images/Ore.png',
                       'ORE_H': 'Images/Ore_24px.png',
                       'BRICK': 'Images/Brick.png',
                       'BRICK_H': 'Images/Brick_24px.png',
                       'SHEEP': 'Images/Sheep.png',
                       'SHEEP_H': 'Images/Sheep_24px.png',
                       '3FOR1': 'Images/QMark.png',
                       'BOAT': 'Images/Boat_64px.png',
                       'DUNES': 'Images/Dunes.png',
                       'DESERT': 'Images/Cactus.png',
                       'ROBBER': 'Images/Robber3.png',
                       'RED_S': 'Images/Settlement/Red Settlement.png',
                       'BLUE_S': 'Images/Settlement/Blue Settlement.png',
                       'GREY_S': 'Images/Settlement/Grey Settlement.png',
                       'GREEN_S': 'Images/Settlement/Green Settlement.png'}

        for key in image_paths.keys():
            image = pygame.image.load(image_paths[key])
            self.images[key] = image

    def get_screen_dimensions(self):
        return self.screen_dimensions[0], self.screen_dimensions[1]

    @staticmethod
    def update():
        pygame.display.update()


class Player:

    def __init__(self, name, color_name, color_RGB):
        self.name = name
        self.color_name = color_name
        self.color = color_RGB

        self.num_points = 0
        self.num_settlements = 5
        self.num_cities = 4
        self.num_roads = 13
        self.used_knights = 0
        self.longest_road = 0
        self.resources = {'WOOD': 0, 'WHEAT': 0, 'BRICK': 0, 'ORE': 0, 'SHEEP': 0}
        self.development_cards = {'KNIGHT': 0, 'MONOPOLY': 0, 'YEAR OF PLENTY': 0, 'ROAD BUILDING': 0, 'VICTORY POINT': 0}

        self.settlements = []
        self.cities = []

    def place_settlement(self, node, board, gui):
        x, y = node.get_center()
        settlement = Settlement(self)
        settlement.set_center(x, y)
        settlement.node = node
        settlement.animate_placement(gui)

        board.settlements.append(settlement)
        node.settlement = settlement
        self.settlements.append(settlement)

        self.num_settlements -= 1
        self.num_points += 1

    def place_road(self, edge, board, gui):
        x, y = edge.get_center()
        nodes = edge.nodes
        road = Road(self, edge, nodes)

        road.set_center(x, y)
        road.animate_placement(gui)

        board.roads.append(road)
        edge.road = road
        self.num_roads -= 1

    def draw(self, gui):
        pass


class Game:

    def __init__(self):
        self.num_players = 0
        self.players = []
        self.current_turn = 1
        self.start_placements()
        self.board = None
        self.gui = None

    def start_placements(self):

        finished_placements = False

        placement_order = [player for player in self.players]
        for i in range(len(placement_order)):
            placement_order.append(self.players[-(i + 1)])

        current_player_index = 0
        previous_player_index = 0
        current_player = placement_order[current_player_index]
        available_placements = self.board.get_node_availability()

        settlement_selection = True
        road_selection = False

        settlement_placed = False
        selected_node = None

        road_placed = False
        selected_edge = None

        # Mouse Boolean
        left_click_pressed = False
        click_selection = False

        while not finished_placements:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished_placements = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        finished_placements = True

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    left_click_pressed = True

                if event.type == pygame.MOUSEBUTTONUP and left_click_pressed:
                    click_selection = True
                    left_click_pressed = False

            mx, my = pygame.mouse.get_pos()

            # Display available spots
            self.gui.reset_board()

            if settlement_selection:
                for node in available_placements:
                    if node.is_mouse_in_bound(mx, my):
                        node.draw(self.gui, highlighted=True)

                        # Detect for mouse click
                        if click_selection:  # Probably exists a better way to detect if click is lifted
                            settlement_placed = True
                            selected_node = node
                    else:
                        node.draw(self.gui)

                # If so, check coordinates and if they match the node then place settlement and move onto next player
                if settlement_placed:
                    current_player.place_settlement(selected_node, self.board, self.gui)
                    self.board.remove_node_availability(selected_node)
                    self.board.draw(self.gui)

                    settlement_selection = False
                    road_selection = True

            elif road_selection:
                for edge in self.board.get_edge_availability(selected_node, current_player):
                    if edge.is_mouse_in_bound(mx, my):
                        edge.draw(self.gui, highlighted=True)

                        if click_selection:
                            road_placed = True
                            selected_edge = edge
                    else:
                        edge.draw(self.gui)

                if road_placed:
                    current_player.place_road(selected_edge, self.board, self.gui)
                    self.board.remove_edge_availability(selected_edge)
                    self.board.draw(self.gui)

                    settlement_selection = True
                    road_selection = False

            if settlement_placed and road_placed:
                settlement_placed = False
                road_placed = False
                current_player_index += 1

                # Give out resources to second settlements
                if current_player_index > int(len(placement_order) / 2):
                    second_settlement = current_player.settlements[-1]
                    for tile in second_settlement.node.tiles:
                        if tile.resource != 'DESERT':
                            resource_count = current_player.resources.get(tile.resource)
                            current_player.resources[tile.resource] = resource_count + 1

            # If clicked, but not on target nodes, then disregard click
            click_selection = False

            self.gui.update()

            if current_player_index < len(placement_order):
                # Check for available spots if player index changes
                if current_player_index != previous_player_index:
                    # Check player index is within range
                    current_player = placement_order[current_player_index]
                    available_placements = self.board.get_node_availability()
                    previous_player_index += 1
            else:
                finished_placements = True

    def play_turn(self, player):
        finished = False

        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True

                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    left_click_pressed = True

                if event.type == pygame.MOUSEBUTTONUP and left_click_pressed:
                    click_selection = True
                    left_click_pressed = False



    @staticmethod
    def roll_dice():
        return random.randint(1, 6) + random.randint(1, 6)

    def get_players(self):
        while self.num_players > 4 or self.num_players < 3:
            self.num_players = int(input('Number of Players (3 or 4): '))

        colors = {'RED': (255, 0, 0), 'BLUE': (0, 0, 255), 'GREEN': (0, 255, 0), 'GREY': (60, 60, 60)}

        player_colors = list([color, colors[color]] for color in colors)
        random.shuffle(player_colors)

        for i in range(self.num_players):
            number = i + 1
            player_name = input('Enter Player {0}\'s Name: '.format(number))
            color_register = player_colors.pop()
            self.players.append(Player(player_name, color_register[0], color_register[1]))

        random.shuffle(self.players)

        print('---- PLAYERS ----')
        for player in self.players:
            print(player.name)

    def get_turn_player(self):
        return self.players[(self.current_turn - 1) % self.num_players]

    def play_game(self):
        game_over = False

        self.get_players()

        self.gui = GUI()
        self.board = Board()

        screen_width, screen_height = self.gui.get_screen_dimensions()
        self.board.set_board_center(screen_width / 3, screen_height / 2.5)
        self.board.generate_random_board()
        self.gui.initialize_board(self.board)

        self.start_placements()

        # Game Loop Start
        while not game_over:

            player = self.get_turn_player()

            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True

            self.gui.update()

            self.current_turn += 1


if __name__ == "__main__":
    Game().play_game()


