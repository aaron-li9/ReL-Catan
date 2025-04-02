from Enum import *
from Utility import *


class Dice:

    def __init__(self):
        # Basic Variables
        self.dice_1_value = np.random.randint(1, 7)
        self.dice_2_value = np.random.randint(1, 7)
        self.cur_roll = self.dice_1_value + self.dice_2_value

        # Graphical Variables
        self.is_highlighted = False
        self.center = DEFAULT_CENTER
        self.lower_bound = Template.DEFAULT_DICE_LOWER_BOUND
        self.upper_bound = Template.DEFAULT_DICE_UPPER_BOUND

    # Basic Functions
    def roll(self):
        self.dice_1_value = np.random.randint(1, 7)
        self.dice_2_value = np.random.randint(1, 7)
        self.cur_roll = self.dice_1_value + self.dice_2_value
        return self.cur_roll

    def get_current_roll(self):
        return self.cur_roll

    # Graphical Functions
    def is_mouse_inbound(self, mouse_position):
        if self.lower_bound[0] <= mouse_position[0] <= self.upper_bound[0]:
            if self.lower_bound[1] <= mouse_position[1] <= self.upper_bound[1]:
                return True
        return False

    def set_center(self, center):
        self.center = center
        self.upper_bound = self.center + self.upper_bound
        self.lower_bound = self.center + self.lower_bound

    def set_highlighted(self, is_highlighted):
        self.is_highlighted = is_highlighted

    def draw(self, gui):
        # Draw Dice Blocks
        self._draw_die(-Template.DICE_OFFSET, self.dice_1_value, gui)
        self._draw_die(Template.DICE_OFFSET, self.dice_2_value, gui)

    def _draw_die(self, offset, number, gui):
        # Draw Dice Block
        outline_corners = Template.DICE_OUTLINE_CORNERS + self.center + offset
        corners = Template.DICE_INSIDE_CORNERS + self.center + offset
        dice_outline_color = Palette.WHITE if self.is_highlighted else Palette.LIGHT_GREY
        dice_inside_color = Palette.LIGHT_GREY if self.is_highlighted else Palette.WHITE
        pygame.draw.polygon(gui.screen, dice_outline_color, outline_corners)
        pygame.draw.polygon(gui.screen, dice_inside_color, corners)

        # Draw Dots
        for dot_center in Template.DICE_DOT_CENTERS.get(number):
            pygame.draw.circle(gui.screen, Palette.BLACK, dot_center + self.center + offset, 10)


class Robber:

    def __init__(self):
        # Basic Variables
        self.center = np.zeros(2)
        self.tile_robber_node = None

    def place_on_tile(self, robber_node):
        self.tile_robber_node = robber_node
        self.tile_robber_node.place_robber(self)
        self.center = self.tile_robber_node.get_center()

    def remove_from_tile(self):
        self.tile_robber_node.remove_robber()
        self.tile_robber_node = None

    def get_robber_node(self):
        return self.tile_robber_node

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center

    def draw(self, gui):
        robber_image = gui.get_image(Images.ROBBER)
        robber_rect = robber_image.get_rect(center=self.center)
        gui.screen.blit(robber_image, robber_rect)


class NodeBuilding:

    def __init__(self, player, building_type=BuildingType.EMPTY):
        self.building_type = building_type
        self.node = None
        self.player = player
        self.center = DEFAULT_CENTER

    def set_building_type(self, building_type: BuildingType):
        self.building_type = building_type

    def set_center(self, center):
        self.center = center

    def set_player(self, player):
        self.player = player

    def set_node(self, node):
        self.node = node
        self.center = node.get_center()

    def remove_node(self):
        self.node = None

    def get_node(self):
        return self.node

    def get_player(self):
        return self.player

    def get_center(self):
        return self.center

    def get_building_type(self) -> BuildingType:
        return self.building_type

    def draw(self, gui):
        if self.building_type == BuildingType.SETTLEMENT:
            self._draw_settlement(gui)
        elif self.building_type == BuildingType.ROAD:
            self._draw_road(gui)
        elif self.building_type == BuildingType.CITY:
            self._draw_city(gui)

    def animate(self, gui, board):
        target_center = self.center.copy()
        self.center += ANIMATION_OFFSET
        while self.center[0] != target_center[0] or self.center[1] != target_center[1]:
            gui.reload_game()
            self.draw(gui)
            gui.update()
            self.center += ANIMATION_STEP
        # Add building to board and redraw
        gui.draw_game()

    def _draw_road(self, gui):
        node_1, node_2 = list(self.node.get_nodes())        # An edge disguised as a node
        road_vector = Vector(node_2.get_center(), node_1.get_center())
        inner_road_coord = self._get_road_coordinates(road_vector)
        outline_coord = self._get_road_coordinates(road_vector, True)

        pygame.draw.polygon(gui.screen, Palette.ROAD_OUTLINE, outline_coord)
        pygame.draw.polygon(gui.screen, Palette.PLAYER_CLR_TO_COLOR[self.player.get_color()], inner_road_coord)

    def _get_road_coordinates(self, road_vector, outline=False):
        road_unit = road_vector.get_unit()
        road_norm = road_vector.get_normal()
        length = ROAD_LENGTH + ROAD_OUTLINE if outline else ROAD_LENGTH
        width = ROAD_WIDTH + ROAD_OUTLINE if outline else ROAD_WIDTH

        left_side = self.center - road_unit * length
        right_side = self.center + road_unit * length

        coordinates = np.vstack((left_side + road_norm * width,
                                 right_side + road_norm * width,
                                 right_side - road_norm * width,
                                 left_side - road_norm * width))
        return coordinates

    def _draw_settlement(self, gui):
        settlement_image = gui.images.get(Images.PLYR_CLR_TO_IMG[self.player.get_color()][BuildingType.SETTLEMENT])
        settlement_rect = settlement_image.get_rect(center=self.center)
        gui.screen.blit(settlement_image, settlement_rect)

    def _draw_city(self, gui):
        city_image = gui.images.get(Images.PLYR_CLR_TO_IMG[self.player.get_color()][BuildingType.CITY])
        city_rect = city_image.get_rect(center=self.center)
        gui.screen.blit(city_image, city_rect)
