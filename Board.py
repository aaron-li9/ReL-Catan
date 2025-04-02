from typing import Set, Tuple, List
from Enum import *
from Utility import *
from BoardComponents import Tile, Node, Edge, Harbor
from BoardPieces import Robber, Dice


class Board:

    def __init__(self, generator_file=None):
        # Board Generation Variables (Only used during initialization)
        self.generator_file = generator_file
        self.resource_freq = {}
        self.number_freq = {}
        self.harbor_freq = {}
        self.center_tile = []
        self.tile_grid_locations = []
        self.harbor_locations = []

        # Board Grid (See implementation details)
        self.tile_grid = dict()
        self.num_to_tile = dict()
        self.robber_nodes = set()
        self.node_set = set()       # Quick access to all nodes
        self.ordered_nodes = dict()
        self.open_settlement_nodes = set()     # Quick access to settlment nodes
        self.open_city_nodes = set()
        self.edge_set = set()       # Quick access to all edges
        self.open_edges = set()     # Quick access to placeable edges
        self.harbor_set = set()     # Quick access to all harbors
        self.buildings = set()
        self.roads = set()

        # GUI Parameters
        self.center = np.zeros(2)

    def generate_board(self):
        # Read Board Specifications
        self._read_generation_file()
        self._assert_valid_read()

        # Populate Randomized Tiles
        tile_deck = self._generate_tile_deck()
        harbor_deck = self._generate_harbor_deck()
        self._populate_tile_grid(tile_deck)
        self._connect_tile_grid()
        self._populate_harbors(harbor_deck)

        # Set GUI Parameters
        self._set_gui_parameters()
        self.print_tile_grid()

    # Board Specification Read Functions
    def _read_generation_file(self):
        with open(self.generator_file, mode="r") as read_file:
            current_line = read_file.readline().strip()
            while current_line:
                current_line = current_line.strip()
                if current_line == "RESOURCES":
                    self._read_resource_freq(read_file)
                elif current_line == "NUMBERS":
                    self._read_number_freq(read_file)
                elif current_line == "HARBORS":
                    self._read_harbor_freq(read_file)
                elif current_line == "STRUCTURE":
                    structure_line = read_file.readline().strip()
                    if structure_line == "TILES":
                        self._read_tile_locations(read_file)
                    elif structure_line == "CENTER":
                        self._read_board_center(read_file)
                    elif structure_line == "HARBORS":
                        self._read_harbor_locations(read_file)
                current_line = read_file.readline()

    def _read_resource_freq(self, read_file):
        current_line = read_file.readline().strip()
        while current_line:
            resource, freq = current_line.split()
            self.resource_freq[ResourceType.STR_TO_RES[resource]] = int(freq)
            current_line = read_file.readline().strip()

    def _read_number_freq(self, read_file):
        current_line = read_file.readline().strip()
        while current_line:
            number, freq = current_line.split()
            self.number_freq[int(number)] = int(freq)
            current_line = read_file.readline().strip()

    def _read_harbor_freq(self, read_file):
        current_line = read_file.readline().strip()
        while current_line:
            harbor_type, freq = current_line.split()
            self.harbor_freq[HarborType.STR_TO_HBR[harbor_type]] = int(freq)
            current_line = read_file.readline().strip()

    def _read_tile_locations(self, read_file):
        current_line = read_file.readline().strip()
        while current_line:
            row, col = [int(x) for x in current_line.split()]
            self.tile_grid_locations.append([row, col])
            current_line = read_file.readline().strip()

    def _read_board_center(self, read_file):
        self.center_tile = [int(x) for x in read_file.readline().strip().split()]
        read_file.readline().strip()

    def _read_harbor_locations(self, read_file):
        current_line = read_file.readline().strip()
        while current_line:
            row, col, direction = current_line.split()
            self.harbor_locations.append([int(row), int(col), direction])
            current_line = read_file.readline().strip()

    def _assert_valid_read(self) -> None:
        n_resources = sum(self.resource_freq.values()) - self.resource_freq[ResourceType.DESERT]
        n_numbers = sum(self.number_freq.values())
        assert (n_numbers == n_resources)

    # Board Generation Functions
    def _generate_tile_deck(self) -> List[Tile]:
        # Randomize Resource and Number Pairing
        resource_list = []
        for resource in self.resource_freq.keys():
            if resource is not ResourceType.DESERT:
                resource_list += [resource] * self.resource_freq[resource]
        number_list = list(num for num in self.number_freq.keys() for freq in range(self.number_freq[num]))
        random.shuffle(resource_list)
        random.shuffle(number_list)
        random_pairs = list([res, num] for res, num in zip(resource_list, number_list))
        random_pairs += [[ResourceType.DESERT, 0]] * self.resource_freq[ResourceType.DESERT]
        random_pairs = np.asarray(random_pairs)

        # Create Tile Deck
        deck = []
        for resource, num in random_pairs:
            tile = Tile(resource, num)
            num_to_tile_list = self.num_to_tile.get(num)
            if num_to_tile_list is not None:
                self.num_to_tile[num].append(tile)
            else:
                self.num_to_tile[num] = [tile]
            self.robber_nodes.add(tile.get_robber_node())
            deck.append(tile)
        random.shuffle(deck)  # Shuffle again to account for addition of DESERT tiles
        return deck

    def _generate_harbor_deck(self) -> List[Harbor]:
        # Randomize Harbor Types
        harbor_list = list(harbor for harbor in self.harbor_freq.keys() for freq in range(self.harbor_freq[harbor]))
        random.shuffle(harbor_list)

        # Create Harbor Deck
        deck = []
        for harbor_type in harbor_list:
            deck.append(Harbor(harbor_type))
        return deck

    def _populate_tile_grid(self, tile_deck):
        tile_id = 0
        for row, col in self.tile_grid_locations:
            tile = tile_deck.pop()
            # Check if valid number placement
            if not self._is_valid_tile_placement(row, col, tile):
                # If not valid, then try to first replace current tile with remaining tile deck
                found_replacement = False
                for tile_idx in range(len(tile_deck)):
                    replace_tile = tile_deck[tile_idx]
                    if self._is_valid_tile_placement(row, col, replace_tile):
                        tile_deck[tile_idx] = tile
                        tile = replace_tile
                        found_replacement = True
                        break

                # If still not valid, then try replacing with placed tiles
                if not found_replacement:
                    for index, replace_tile in self.tile_grid.items():
                        can_replace_current = self._is_valid_tile_placement(row, col, replace_tile)
                        can_replace_previous = self._is_valid_tile_placement(int(index[0]), int(index[1]), tile)
                        if can_replace_current and can_replace_previous:
                            tile.set_id(replace_tile.get_id())
                            tile.set_grid_index(replace_tile.get_grid_index())
                            self.tile_grid[index] = tile
                            tile = replace_tile
                            found_replacement = True
                            break
                assert found_replacement

            # Edge case if not valid, then swap with the next valid one starting from the start
            tile_index = str(row) + str(col)
            tile.set_id(tile_id)
            tile.set_grid_index(tile_index)
            self.tile_grid[tile_index] = tile
            tile_id += 1

    def _connect_tile_grid(self):
        # For each tile,
        for index, tile in self.tile_grid.items():
            # Find neighboring tiles in the lower right quadrant
            neighbors = self._find_connect_tiles(int(index[0]), int(index[1]))
            # Connect current tile nodes and edges to those of neighboring tiles
            for neighbor, direction in neighbors:
                tile.connect_tile(neighbor, direction)

        # Run through tiles and connect edges and nodes
        for index, tile in self.tile_grid.items():
            # Add nodes to each edge
            nodes = tile.get_nodes()
            for edge_idx, edge in enumerate(tile.get_edges()):
                node1 = nodes[edge_idx]
                node2 = nodes[(edge_idx + 1) % 6]
                node1.add_edge(edge)
                node2.add_edge(edge)
                edge.add_node(node1)
                edge.add_node(node2)
                self.edge_set.add(edge)
                self.open_edges.add(edge)
                self.node_set.add(node1)
                self.open_settlement_nodes.add(node1)

        # Run through every tile and order the node ids
        node_id = 0
        for index, tile in self.tile_grid.items():
            for node in tile.get_nodes():
                if node.get_id() == -1:
                    node.set_id(node_id)
                    self.ordered_nodes[node_id] = node
                    node_id += 1

    def _populate_harbors(self, harbor_deck):
        for row, col, direction in self.harbor_locations:
            index = str(row) + str(col)
            tile = self.tile_grid.get(index)
            harbor = harbor_deck.pop()
            self.harbor_set.add(harbor)
            harbor.set_tile(tile)
            tile.set_harbor(harbor, TILE_DIRECTION_MAP[direction])
            for node in tile.get_edges()[TILE_DIRECTION_MAP[direction]].get_nodes():
                node.set_harbor(harbor)
                harbor.add_node(node)

    def _is_valid_tile_placement(self, row, col, tile) -> bool:
        tile_number = tile.get_number()
        if abs(tile_number - 7) != 1:   # Check if tile number is 6 or 8
            return True                 # Return true if not
        else:
            neighbors = self._find_neighbor_tiles(row, col)
            for neighbor_tile in neighbors:
                neighbor_number = neighbor_tile.get_number()
                if abs(neighbor_number - 7) == 1:
                    return False
            return True

    def _find_neighbor_tiles(self, row, col):
        neighbors = []
        for neighbor_coordinates in TILE_NEIGHBOR_LIST:
            index = str(row + neighbor_coordinates[0]) + str(col + neighbor_coordinates[1])
            neighbor_tile = self.tile_grid.get(index)
            if neighbor_tile is not None:
                neighbors.append(neighbor_tile)
        return neighbors

    def _find_connect_tiles(self, row, col):
        connectors = []
        for connect_row, connect_col, direction in TILE_CONNECT_LIST:
            index = str(row + connect_row) + str(col + connect_col)
            connect_tile = self.tile_grid.get(index)
            if connect_tile is not None:
                connectors.append([connect_tile, direction])
        return connectors

    # Board GUI Functions
    def _set_gui_parameters(self):
        for index, tile in self.tile_grid.items():
            self._set_tile_center(tile, index)
            self._set_node_centers(tile)
            self._set_edge_centers(tile)
            self._set_harbor_centers(tile)

    def _set_tile_center(self, tile, index):
        row_norm = int(index[0]) - self.center_tile[0]
        col_norm = int(index[1]) - self.center_tile[1]
        tile_x = 2 * col_norm * TILE_X_STEP - row_norm * TILE_X_STEP + self.center[0]
        tile_y = row_norm * TILE_Y_STEP + self.center[1]
        tile.set_center(tile_x, tile_y)

    def _set_node_centers(self, tile):
        nodes = tile.get_nodes()
        node_centers = HEXAGON_COORDINATE_TEMPLATE * TILE_SIDE_LENGTH + tile.get_center()
        for node_index, node_center in enumerate(node_centers):
            nodes[node_index].set_center(node_center[0], node_center[1])

    def _set_edge_centers(self, tile):
        edges = tile.get_edges()
        edge_centers = HEXAGON_EDGE_TEMPLATE * TILE_SIDE_LENGTH + tile.get_center()
        for edge_index, edge_center in enumerate(edge_centers):
            edges[edge_index].set_center(edge_center[0], edge_center[1])

    def _set_harbor_centers(self, tile):
        harbors = list(filter(None, tile.get_harbors()))
        for harbor in harbors:
            node_1, node_2 = harbor.get_nodes()
            midpoint = Vector(node_1.get_center(), node_2.get_center()).get_midpoint()
            center = -1 * Vector(midpoint, tile.get_center()).get_vector() + midpoint
            harbor.set_center(center[0], center[1])

    # Public Functions
    def set_center(self, x, y):
        self.center = np.asarray([x, y])
        self._set_gui_parameters()

    def set_generator_file(self, generator_file):
        self.generator_file = generator_file

    def get_center(self):
        return self.center

    def get_tile_grid(self):
        return self.tile_grid

    def get_open_settlement_nodes(self):
        return self.open_settlement_nodes

    def get_open_edges(self):
        return self.open_edges

    def get_robber_nodes(self):
        return self.robber_nodes

    def get_tiles_from_number(self, number):
        return self.num_to_tile.get(number, [])

    def add_building(self, node_building):
        if node_building.get_building_type() == BuildingType.ROAD:
            self.roads.add(node_building)
        else:
            self.buildings.add(node_building)

    def remove_building(self, node_building):
        if node_building.get_building_type() == BuildingType.ROAD:
            self.roads.remove(node_building)
        else:
            self.buildings.remove(node_building)

    def print_tile_grid(self):
        # DEBUG FUNCTION #
        for index, tile in self.tile_grid.items():
            # print("Tile ID:", tile.get_id(), "CENTER:", tile.get_center())
            pass

    def remove_settlement_nodes(self, center_node: Node):
        self.open_settlement_nodes.remove(center_node)
        self.open_city_nodes.add(center_node)
        for edge in center_node.get_edges():
            for node in edge.get_nodes():
                if center_node != node and node in self.open_settlement_nodes:
                    self.open_settlement_nodes.remove(node)

    def remove_available_edge(self, edge):
        if edge in self.open_edges:
            self.open_edges.remove(edge)

    def remove_city_node(self, city_node):
        self.open_city_nodes.remove(city_node)

    # GUI Functions
    def draw(self, gui) -> None:
        # Draw Ocean
        gui.screen.fill(Palette.BOARD_OCEAN)

        # Draw Tiles
        for index, tile in self.tile_grid.items():
            tile.draw(gui)

        # Draw Harbors
        for harbor in self.harbor_set:
            harbor.draw(gui)

        # Draw Roads
        for road in self.roads:
            road.draw(gui)

        # Draw Building
        for building in self.buildings:
            building.draw(gui)
