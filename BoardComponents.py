from Enum import *
from Utility import *
from BoardPieces import NodeBuilding
from Player import Player


class Tile:

    def __init__(self, resource, number):
        # Basic Variables
        self.resource = resource
        self.number = number
        self.has_robber = False
        self.tile_id = -1
        self.robber_node = Node(self)
        self.nodes = [Node(self) for x in range(6)]     # Nodes are counter-clockwise from top of hexagon
        self.edges = [Edge() for x in range(6)]
        self.harbors = [None for x in range(6)]
        self.tiles = [None for x in range(6)]       # NOT USED
        self.grid_index = ""

        # Graphics Variables
        self.center = np.zeros(2)
        self.num_color = Palette.NUMBER_COLOR_RED if np.abs(self.number - 7) == 1 else Palette.NUMBER_COLOR_BLACK

    # Basic Functions
    def get_number(self):
        return self.number

    def get_resource(self):
        return self.resource

    def get_id(self):
        return self.tile_id

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def get_tiles(self):
        return self.tiles

    def get_harbors(self):
        return self.harbors

    def get_grid_index(self):
        return self.grid_index

    def set_grid_index(self, index):
        self.grid_index = index

    def get_robber_node(self):
        return self.robber_node

    def set_id(self, tile_id):
        self.tile_id = tile_id
        # for node_idx in range(6):
        #     node = self.nodes[node_idx]
        #     node.set_id(tile_id)
        #     node.set_tile_index(node_idx)

        for edge_idx in range(6):
            edge = self.edges[edge_idx]
            edge.set_id(tile_id)
            edge.set_tile_index(edge_idx)

    def set_node(self, node, node_idx):
        node.add_tile(self)
        self.nodes[node_idx] = node

    def set_tile(self, tile, tile_idx):
        self.tiles[tile_idx] = tile

    def set_harbor(self, harbor, harbor_idx):
        self.harbors[harbor_idx] = harbor

    def set_edge(self, edge, edge_idx):
        self.edges[edge_idx] = edge

    def connect_tile(self, tile_neighbor, direction):
        # Obtain connection indices
        main_idx, neighbor_idx = TILE_NEIGHBOR_MAP[direction]
        node_map = TILE_NEIGHBOR_NODE_MAP[direction]

        # Connect Nodes
        for main_node, neighbor_node in node_map.items():
            tile_neighbor.set_node(self.nodes[main_node], neighbor_node)

        # Connect Edges
        tile_neighbor.set_edge(self.edges[main_idx], neighbor_idx)

        # Connect Tiles
        self.set_tile(tile_neighbor, main_idx)
        tile_neighbor.set_tile(self, neighbor_idx)

    def update_robber(self, has_robber):
        self.has_robber = has_robber

    # Graphical Functions
    def set_center(self, x, y):
        self.center = np.array([x, y])
        robber_center = self.center + Template.TILE_ROBBER_NODE_OFFSET
        self.robber_node.set_center(robber_center[0], robber_center[1])

    def get_center(self):
        return self.center

    def draw(self, gui):
        self._draw_tile(gui)                                # Draw Tile and Shore
        if self.resource != ResourceType.DESERT:            # Draw Number Tile
            self._draw_number_tile(gui)
        self._draw_image(gui)                               # Draw Image

    def _draw_number_tile(self, gui):
        # Get Constants
        number_font = pygame.font.SysFont(NUMBER_FONT, NUMBER_SIZE, bold=True)

        # Draw Number Tile
        pygame.draw.circle(gui.screen, Palette.NUMBER_TILE,
                           (self.center[0], self.center[1] + TILE_NUMBER_DISPLACEMENT), TILE_NUMBER_RADIUS)

        # Draw tile number and dots
        text_surface = number_font.render(str(self.number), True, self.num_color)
        text_rect = text_surface.get_rect(center=(self.center[0], self.center[1] + TILE_NUMBER_DISPLACEMENT - 3))
        gui.screen.blit(text_surface, text_rect)

        text_surface = number_font.render(NUMBER_DOTS_DICT[np.abs(self.number - 7)], True, self.num_color)
        text_rect = text_surface.get_rect(center=(self.center[0], self.center[1] + TILE_NUMBER_DISPLACEMENT + 6))
        gui.screen.blit(text_surface, text_rect)

    def _draw_tile(self, gui):
        # Get Tile and Outline Coordinates
        tile_coordinates = self.center + HEXAGON_COORDINATE_TEMPLATE * (TILE_SIDE_LENGTH - TILE_OUTLINE_SIZE)
        outline_coordinates = self.center + HEXAGON_COORDINATE_TEMPLATE * (TILE_SIDE_LENGTH + TILE_OUTLINE_SIZE)

        # Draw Tile and Shore
        pygame.draw.polygon(gui.screen, Palette.TILE_OUTLINE, outline_coordinates)              # Draw Shore
        pygame.draw.polygon(gui.screen, Palette.TILE_COLOR[self.resource], tile_coordinates)    # Draw Tile

    def _draw_image(self, gui):
        resource_image = gui.get_image(Images.RES_TO_IMG.get(self.resource))
        resource_rect = resource_image.get_rect(center=(self.center[0], self.center[1] + TILE_RESOURCE_OFFSET))
        gui.screen.blit(resource_image, resource_rect)


class Node:

    def __init__(self, tile):
        # Basic Variables
        self.player = None
        self.node_id = -1
        self.tile_index = -1
        self.harbor = None

        self.tiles = {tile}
        self.edges = set()

        # Graphical Variables
        self.center = DEFAULT_CENTER
        self.is_highlighted = False

        self.robber = None
        self.building = None

    # Basic Functions
    def get_player(self):
        return self.player

    def get_building(self) -> NodeBuilding:
        return self.building

    def get_harbor(self):
        return self.harbor

    def get_id(self):
        return self.node_id

    def get_tile_index(self):
        return self.tile_index

    def get_edges(self):
        return self.edges

    def get_tiles(self):
        return self.tiles

    def get_robber(self):
        return self.robber

    def add_tile(self, tile):
        self.tiles.add(tile)

    def set_tile_index(self, tile_index):
        self.tile_index = tile_index

    def set_player(self, player):
        self.player = player

    def set_id(self, node_id):
        self.node_id = node_id

    def set_harbor(self, harbor):
        self.harbor = harbor

    def add_edge(self, edge):
        self.edges.add(edge)

    def place_robber(self, robber):
        self.robber = robber
        # Better implementation would be to have node abstract class and have only one tile for RobberNode
        for tile in self.tiles:
            tile.update_robber(True)

    def remove_robber(self):
        self.robber = None
        for tile in self.tiles:
            tile.update_robber(False)

    def remove_building(self):
        building = self.building
        building.remove_node()
        self.building = None
        self.set_player(None)
        return building

    def place_building(self, player: Player, building: NodeBuilding):
        self.building = building
        self.building.set_node(self)
        self.set_player(player)

    # Graphical Functions
    def set_center(self, x, y):
        self.center = np.array([x, y])

    def get_center(self):
        return self.center

    def set_highlight(self, is_highlighted):
        self.is_highlighted = is_highlighted

    def is_mouse_inbound(self, mouse_position):
        lower_bound = self.center - NODE_RADIUS
        upper_bound = self.center + NODE_RADIUS
        if lower_bound[0] <= mouse_position[0] <= upper_bound[0]:
            if lower_bound[1] <= mouse_position[1] <= upper_bound[1]:
                return True
        return False

    def draw(self, gui):
        node_color = Palette.NODE_HIGHLIGHTED if self.is_highlighted else Palette.NODE
        node_surface = pygame.Surface(2 * NODE_RADIUS_ARRAY, pygame.SRCALPHA)
        node_surface.set_alpha(192)
        pygame.draw.circle(node_surface, node_color, NODE_RADIUS_ARRAY, NODE_RADIUS)
        node_rect = node_surface.get_rect(center=self.center)
        gui.screen.blit(node_surface, node_rect)


class Edge:

    def __init__(self):
        # Basic Variables
        self.player = None
        self.edge_id = -1
        self.tile_index = -1
        self.nodes = set()

        # Graphical Variables
        self.center = DEFAULT_CENTER
        self.is_highlighted = False

        self.road = None

    def get_id(self):
        return self.edge_id

    def get_nodes(self):
        return self.nodes

    def get_tile_index(self):
        return self.tile_index

    def get_player(self):
        return self.player

    def get_road(self):
        return self.road

    def set_player(self, player):
        self.player = player

    def set_tile_index(self, tile_index):
        self.tile_index = tile_index

    def add_node(self, node):
        self.nodes.add(node)

    def set_id(self, edge_id):
        self.edge_id = edge_id

    def place_road(self, player: Player, road: NodeBuilding):
        self.road = road
        self.road.set_node(self)
        self.set_player(player)

    # GUI Function
    def set_center(self, x, y):
        self.center = np.array([x, y])

    def get_center(self):
        return self.center

    def set_highlight(self, is_highlighted):
        self.is_highlighted = is_highlighted

    def is_mouse_inbound(self, mouse_position):
        lower_bound = self.center - NODE_RADIUS
        upper_bound = self.center + NODE_RADIUS
        if lower_bound[0] <= mouse_position[0] <= upper_bound[0]:
            if lower_bound[1] <= mouse_position[1] <= upper_bound[1]:
                return True
        return False

    def draw(self, gui):
        node_color = Palette.NODE_HIGHLIGHTED if self.is_highlighted else Palette.NODE
        node_surface = pygame.Surface(2 * NODE_RADIUS_ARRAY, pygame.SRCALPHA)
        node_surface.set_alpha(192)
        pygame.draw.circle(node_surface, node_color, NODE_RADIUS_ARRAY, NODE_RADIUS)
        node_rect = node_surface.get_rect(center=self.center)
        gui.screen.blit(node_surface, node_rect)


class Harbor:

    def __init__(self, harbor_type):
        # Basic Variables
        self.harbor_type = harbor_type
        self.nodes = set()
        self.tile = None

        # GUI Variables
        self.center = np.zeros(2)

    def get_harbor_type(self):
        return self.harbor_type

    def get_nodes(self):
        return self.nodes

    def set_harbor_type(self, harbor_type):
        self.harbor_type = harbor_type

    def set_tile(self, tile):
        self.tile = tile

    def set_center(self, x, y):
        self.center = np.array([x, y])

    def add_node(self, node):
        self.nodes.add(node)

    def draw(self, gui):
        # Draw Ports
        node_centers = []
        for node in self.nodes:
            node_center = node.get_center()
            node_centers.append(node_center)
            self._draw_port(gui, node_center)

        # Draw Ship
        self._draw_ship(gui, node_centers)

    def _draw_port(self, gui, node_center):
        harbor_to_node_vec = Vector(node_center, self.center)
        harbor_to_node_unit = harbor_to_node_vec.get_unit()
        harbor_to_node_norm = harbor_to_node_vec.get_normal()

        node_point = node_center + harbor_to_node_unit * PORT_SHORE_OFFSET
        ship_point = self.center - harbor_to_node_unit * PORT_SHIP_OFFSET

        coordinates = [node_point + harbor_to_node_norm * PORT_WIDTH, ship_point + harbor_to_node_norm * PORT_WIDTH,
                       ship_point - harbor_to_node_norm * PORT_WIDTH, node_point - harbor_to_node_norm * PORT_WIDTH]

        pygame.draw.polygon(gui.screen, Palette.PORT, coordinates)

    def _draw_ship(self, gui, node_centers):
        # Find center of ship
        edge_midpoint = Vector(node_centers[0], node_centers[1]).get_midpoint()
        ship_unit = Vector(edge_midpoint, self.center).get_unit()
        displacement = ship_unit * SHIP_DISPLACEMENT
        ship_center = self.center + displacement

        # Get ship image
        ship_image = gui.get_image(Images.BOAT)
        ship_rect = ship_image.get_rect(center=(ship_center[0], ship_center[1]))
        gui.screen.blit(ship_image, ship_rect)

        # Get resource image
        resource_image = gui.get_image(Images.HBR_TO_IMG.get(self.harbor_type))
        resource_rect = resource_image.get_rect(center=(ship_center[0], ship_center[1] - 2))
        gui.screen.blit(resource_image, resource_rect)

