from Enum import *
from Utility import *
from BoardPieces import NodeBuilding


class PlayerButton:

    def __init__(self, player):
        self.player = player
        self.center = DEFAULT_CENTER
        self.offset = DEFAULT_CENTER
        self.is_highlighted = False
        self.is_visible = False
        self.upper_bound = Template.DEFAULT_BUTTON_UPPER_BOUND
        self.lower_bound = Template.DEFAULT_BUTTON_LOWER_BOUND

    def set_center(self, center):
        self.center = center + self.offset
        self.upper_bound = self.center + self.upper_bound
        self.lower_bound = self.center + self.lower_bound

    def set_bounds(self, upper_bound, lower_bound):
        # Bounds are relative to the center
        self.upper_bound = upper_bound + self.center
        self.lower_bound = lower_bound + self.center

    def set_visibility(self, is_visible):
        self.is_visible = is_visible

    def get_visibility(self):
        return self.is_visible

    def get_center(self):
        return self.center

    def set_highlight(self, is_highlighted):
        self.is_highlighted = is_highlighted

    def is_mouse_inbound(self, mouse_position):
        if self.lower_bound[0] <= mouse_position[0] <= self.upper_bound[0]:
            if self.lower_bound[1] <= mouse_position[1] <= self.upper_bound[1]:
                return True
        return False


class TheftButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.THEFT_BUTTON_OFFSET

    def draw(self, gui):
        theft_image = gui.get_image(Images.THEFT_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.THEFT_BUTTON)
        theft_rect = theft_image.get_rect(center=self.center)
        gui.screen.blit(theft_image, theft_rect)


class BuildButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.BUILD_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.BUILD_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.BUILD_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class TradeButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.TRADE_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.TRADE_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.TRADE_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class DevCardButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.DEV_CARD_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.DEV_CARD_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.DEV_CARD_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class EndTurnButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.END_TURN_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.END_TURN_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.END_TURN_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class BuildSettlementButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.BUILD_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.BUILD_SETTLEMENT_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.BUILD_SETTLEMENT)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class BuildRoadButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.TRADE_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.BUILD_ROAD_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.BUILD_ROAD)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class BuildDevCardButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.BUTTON_2_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.DEV_CARD_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.DEV_CARD_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class BuildCityButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.DEV_CARD_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.BUILD_CITY_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.BUILD_CITY)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class BackToMenuButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.END_TURN_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.END_TURN_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.END_TURN_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class BackToActionButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.TRADE_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.END_TURN_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.END_TURN_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class PlayKnightButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.BUILD_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.KNIGHT_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.KNIGHT_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class PlayMonopolyButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.TRADE_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.MONOPOLY_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.MONOPOLY_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class PlayRoadBuildingButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.DEV_CARD_BUTTON_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.ROAD_BUILDING_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.ROAD_BUILDING_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class PlayYearOfPlentyButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.BUTTON_2_OFFSET

    def draw(self, gui):
        icon_image = gui.get_image(Images.YEAR_OF_PLENTY_BUTTON_HIGHLIGHTED) if self.is_highlighted \
            else gui.get_image(Images.YEAR_OF_PLENTY_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class MonopolyWheatButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.MONOPOLY_ACTION_BUTTON_OFFSETS.get(ResourceType.WHEAT)

    def draw(self, gui):
        icon_image = gui.get_image(Images.WHEAT_BUTTON_HIGHLIGHT) if self.is_highlighted \
            else gui.get_image(Images.WHEAT_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class MonopolyOreButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.MONOPOLY_ACTION_BUTTON_OFFSETS.get(ResourceType.ORE)

    def draw(self, gui):
        icon_image = gui.get_image(Images.ORE_BUTTON_HIGHLIGHT) if self.is_highlighted \
            else gui.get_image(Images.ORE_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class MonopolyWoodButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.MONOPOLY_ACTION_BUTTON_OFFSETS.get(ResourceType.WOOD)

    def draw(self, gui):
        icon_image = gui.get_image(Images.WOOD_BUTTON_HIGHLIGHT) if self.is_highlighted \
            else gui.get_image(Images.WOOD_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class MonopolyBrickButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.MONOPOLY_ACTION_BUTTON_OFFSETS.get(ResourceType.BRICK)

    def draw(self, gui):
        icon_image = gui.get_image(Images.BRICK_BUTTON_HIGHLIGHT) if self.is_highlighted \
            else gui.get_image(Images.BRICK_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class MonopolySheepButton(PlayerButton):

    def __init__(self, player):
        PlayerButton.__init__(self, player)
        self.offset = Template.MONOPOLY_ACTION_BUTTON_OFFSETS.get(ResourceType.SHEEP)

    def draw(self, gui):
        icon_image = gui.get_image(Images.SHEEP_BUTTON_HIGHLIGHT) if self.is_highlighted \
            else gui.get_image(Images.SHEEP_BUTTON)
        icon_rect = icon_image.get_rect(center=self.center)
        gui.screen.blit(icon_image, icon_rect)


class Player:

    def __init__(self, player_id=-1):
        self.player_id = player_id
        self.player_color = PlayerColor.ID_TO_COLOR[player_id]
        self.player_color_code = Palette.PLAYER_CLR_TO_COLOR[self.player_color]
        self.num_points = 0     # Treat this as visible points
        self.hidden_points = 0  # Treat this as victory point card points

        self.resources = np.zeros(NUM_RESOURCES).astype(np.int)
        self.used_dev_cards = np.zeros(NUM_DEV_CARDS).astype(np.int)
        self.unused_dev_cards = np.zeros(NUM_DEV_CARDS).astype(np.int)
        self.available_dev_cards = np.zeros(NUM_DEV_CARDS).astype(np.int)
        self.buildables = np.array([NUM_TOTAL_ROADS, NUM_TOTAL_SETTLEMENTS, NUM_TOTAL_CITIES])
        self.longest_road = False
        self.largest_army = False
        self.used_dev_card = False

        # Available Buildings
        self.unused_roads = [NodeBuilding(self, BuildingType.ROAD) for freq in range(NUM_TOTAL_ROADS)]
        self.unused_settlements = [NodeBuilding(self, BuildingType.SETTLEMENT) for freq in range(NUM_TOTAL_SETTLEMENTS)]
        self.unused_cities = [NodeBuilding(self, BuildingType.CITY) for freq in range(NUM_TOTAL_CITIES)]

        # Available Placement Nodes
        self.available_settlement_nodes = set()
        self.available_road_nodes = set()
        self.available_city_nodes = set()

        # Placed Buildings
        self.placed_roads = []
        self.placed_settlements = []
        self.placed_cities = []

        self.player_turn = False

        # Player Buttons
        self.buttons = {PlayerButtonType.THEFT: TheftButton(self),
                        PlayerButtonType.BUILD: BuildButton(self),
                        PlayerButtonType.TRADE: TradeButton(self),
                        PlayerButtonType.DEV_CARD: DevCardButton(self),
                        PlayerButtonType.END_TURN: EndTurnButton(self),
                        PlayerButtonType.BUILD_ROAD: BuildRoadButton(self),
                        PlayerButtonType.BUILD_SETTLEMENT: BuildSettlementButton(self),
                        PlayerButtonType.BUILD_CITY: BuildCityButton(self),
                        PlayerButtonType.BUILD_DEV_CARD: BuildDevCardButton(self),
                        PlayerButtonType.BACK_TO_MENU: BackToMenuButton(self),
                        PlayerButtonType.BACK_TO_BUILD: BackToActionButton(self),
                        PlayerButtonType.PLAY_KNIGHT: PlayKnightButton(self),
                        PlayerButtonType.PLAY_MONOPOLY: PlayMonopolyButton(self),
                        PlayerButtonType.PLAY_ROAD_BUILDING: PlayRoadBuildingButton(self),
                        PlayerButtonType.PLAY_YEAR_OF_PLENTY: PlayRoadBuildingButton(self),
                        PlayerButtonType.WHEAT_MONOPOLY: MonopolyWheatButton(self),
                        PlayerButtonType.ORE_MONOPOLY: MonopolyOreButton(self),
                        PlayerButtonType.WOOD_MONOPOLY: MonopolyWoodButton(self),
                        PlayerButtonType.BRICK_MONOPOLY: MonopolyBrickButton(self),
                        PlayerButtonType.SHEEP_MONOPOLY: MonopolySheepButton(self)}

        self.center = DEFAULT_CENTER

    def get_id(self):
        return self.player_id

    def get_color(self):
        return self.player_color

    def get_is_turn(self):
        return self.player_turn

    def set_turn(self, is_turn):
        self.player_turn = is_turn

    def has_won_game(self):
        return self.num_points + self.hidden_points >= VP_GOAL

    def add_resource(self, resource_type, count):
        if resource_type != ResourceType.DESERT:
            self.resources[resource_type] += count

    def remove_resource(self, resource_type, count):
        if resource_type != ResourceType.DESERT and self.resources[resource_type] >= count:
            self.resources[resource_type] -= count

    def get_robbed(self):
        stolen_resource = ResourceType.EMPTY
        if np.sum(self.resources) > 0:
            hand = list()
            for resource_type in ResourceType.RES_LIST:
                if resource_type != ResourceType.DESERT:
                    hand += [resource_type] * self.resources[resource_type]
            random.shuffle(hand)
            stolen_resource = hand.pop()
            self.resources[stolen_resource] -= 1
        return stolen_resource

    def build_road(self, edge, gui, board, is_free=False):
        if is_free or self._can_build_road():
            road = self.unused_roads.pop()
            self.placed_roads.append(road)
            edge.place_road(self, road)
            board.remove_available_edge(edge)
            board.add_building(road)
            edge.get_road().animate(gui, board)

            # Find available settlement nodes
            for node in edge.get_nodes():
                if node in board.get_open_settlement_nodes():
                    self.available_settlement_nodes.add(node)
                # Find available road nodes
                for side_edge in node.get_edges():
                    if side_edge in board.get_open_edges():
                        self.available_road_nodes.add(side_edge)

            self.available_road_nodes.remove(edge)

            self.buildables[BuildingType.ROAD] -= 1
            if not is_free:
                self.resources -= ROAD_COST

    def build_settlement(self, node, gui, board, placement=False):
        # If placement settlement, don't check for resources
        if placement or self._can_build_settlement():
            settlement = self.unused_settlements.pop()
            self.placed_settlements.append(settlement)
            node.place_building(self, settlement)
            board.remove_settlement_nodes(node)
            board.add_building(settlement)
            node.get_building().animate(gui, board)

            for edge in node.get_edges():
                if edge in board.get_open_edges():
                    self.available_road_nodes.add(edge)

            self.available_city_nodes.add(node)

            self.num_points += 1
            self.buildables[BuildingType.SETTLEMENT] -= 1
            if not placement:
                self.resources -= SETTLEMENT_COST
                self.available_settlement_nodes.remove(node)

    def build_city(self, node, gui, board):
        if self._can_build_city():
            city = self.unused_cities.pop()
            self.placed_cities.append(city)
            settlement = node.remove_building()
            self.unused_settlements.append(settlement)
            node.place_building(self, city)
            board.remove_city_node(node)
            board.add_building(city)
            board.remove_building(settlement)
            node.get_building().animate(gui, board)

            self.available_city_nodes.remove(node)

            self.num_points += 1
            self.buildables[BuildingType.SETTLEMENT] += 1
            self.buildables[BuildingType.CITY] -= 1
            self.resources -= CITY_COST

    def build_dev_card(self, development_deck):
        if self._can_build_dev_card() and development_deck.get_deck_size() > 0:
            development_card = development_deck.draw_card()
            self.unused_dev_cards[development_card] += 1

            if development_card == DevelopmentCardType.VICTORY_POINT_DEV:
                self.hidden_points += 1

            self.resources -= DEV_CARD_COST

    def _can_build_settlement(self):
        difference = self.resources - SETTLEMENT_COST
        return np.all((difference >= 0)) and len(self.unused_settlements) > 0

    def _can_build_road(self):
        difference = self.resources - ROAD_COST
        return np.all((difference >= 0)) and len(self.unused_roads) > 0

    def _can_build_city(self):
        difference = self.resources - CITY_COST
        return np.all((difference >= 0)) and len(self.unused_cities) > 0

    def _can_build_dev_card(self):
        difference = self.resources - DEV_CARD_COST
        return np.all((difference >= 0))

    def get_available_settlement_nodes(self):
        return self.available_settlement_nodes

    def get_available_road_nodes(self):
        return self.available_road_nodes

    def get_available_city_nodes(self):
        return self.available_city_nodes

    def remove_settlement_node(self, node):
        self.available_settlement_nodes.remove(node)

    def remove_road_node(self, road_node):
        self.available_road_nodes.remove(road_node)

    def remove_city_node(self, city_node):
        self.available_city_nodes.remove(city_node)

    def get_center(self):
        return self.center

    def set_center(self, center):
        self.center = center
        for button_type, button in self.buttons.items():
            if button_type in PlayerButtonType.PLAYER_PHASE_BUTTONS.get(GamePhase.MONOPOLY_ACTION):
                button.set_center(DEFAULT_CENTER)
            else:
                button.set_center(self.center)

    def set_button_visibility(self, button_type, is_visible):
        self.buttons.get(button_type).set_visibility(is_visible)

    def set_button_highlight(self, button_type, is_highlighted):
        self.buttons.get(button_type).set_highlight(is_highlighted)

    def is_button_inbound(self, button_type, mouse_position):
        return self.buttons.get(button_type).is_mouse_inbound(mouse_position)

    def update_pre_turn(self):
        self.used_dev_card = False
        self.available_dev_cards = self.unused_dev_cards.copy()

    def draw_scoreboard(self, gui):
        # Draw Player Scoreboard Tile
        outer_coordinates = PLAYER_TAG_OUTLINE + self.center
        inner_coordinates = PLAYER_TAG_TEMPLATE + self.center
        pygame.draw.polygon(gui.screen, Palette.PLAYER_TAG_OUTLINE, outer_coordinates)
        pygame.draw.polygon(gui.screen, Palette.PLAYER_TAG, inner_coordinates)

        # Draw Player Icon
        pygame.draw.circle(gui.screen, self.player_color_code, PLAYER_ICON_CENTER + self.center, PLAYER_ICON_RADIUS)

        # Draw Victory Point Icon
        vp_image = gui.get_image(Images.VICTORY_POINT)
        vp_center = Template.PLAYER_VP_ICON_CENTER + self.center
        vp_rect = vp_image.get_rect(center=vp_center)
        gui.screen.blit(vp_image, vp_rect)

        # Draw Resource Icons
        for resource_type in ResourceType.RES_LIST:
            if resource_type != ResourceType.DESERT:
                resource_image = gui.get_image(Images.RES_TO_IMG.get(resource_type))
                resource_center = Template.PLAYER_RES_ICON_CENTER[resource_type] + self.center
                resource_rect = resource_image.get_rect(center=resource_center)
                gui.screen.blit(resource_image, resource_rect)

        # Draw Building Icons
        for building_type in BuildingType.BUILD_LIST:
            building_image = gui.get_image(Images.PLYR_CLR_TO_IMG[self.player_color][building_type])
            building_center = Template.PLAYER_BUILD_ICON_CENTER[building_type] + self.center
            building_rect = building_image.get_rect(center=building_center)
            gui.screen.blit(building_image, building_rect)

        # Draw Development Card Icons
        for development_card_type in DevelopmentCardType.CARD_LIST:
            card_image = gui.get_image(Images.CARD_TO_IMG.get(development_card_type))
            card_center = Template.PLAYER_CARD_ICON_CENTER.get(development_card_type) + self.center
            card_rect = card_image.get_rect(center=card_center)
            gui.screen.blit(card_image, card_rect)

    def draw_update(self, gui):
        # Check if current turn, then indicate
        if self.player_turn:
            indicator_image = gui.get_image(Images.TURN_INDICATOR)
            indicator_rect = indicator_image.get_rect(center=PLAYER_ICON_CENTER + self.center)
            gui.screen.blit(indicator_image, indicator_rect)

        # Display Resource Numbers
        number_font = pygame.font.SysFont(NUMBER_FONT, NUMBER_SIZE, bold=True)
        for resource_type in ResourceType.RES_LIST:
            if resource_type != ResourceType.DESERT:
                text_surface = number_font.render(str(self.resources[resource_type]), True, Palette.BLACK)
                text_rect = text_surface.get_rect(center=Template.PLAYER_RES_NUM_CENTER[resource_type] + self.center)
                gui.screen.blit(text_surface, text_rect)

        # Display Building Numbers
        self._draw_update_build_numbers(number_font, gui)

        # Display Development Card Numbers
        for card_type in DevelopmentCardType.CARD_LIST:
            # Display Used
            if card_type != DevelopmentCardType.VICTORY_POINT_DEV:
                text_surface = number_font.render(str(self.used_dev_cards[card_type]), True, Palette.BLACK)
                text_rect = text_surface.get_rect(center=Template.PLAYER_CARD_NUM_CENTER.get(card_type) + self.center + Template.PLAYER_USED_CARD_OFFSET)
                gui.screen.blit(text_surface, text_rect)

            # Display Unused
            text_surface = number_font.render(str(self.unused_dev_cards[card_type]), True, Palette.BLACK)
            if card_type == DevelopmentCardType.VICTORY_POINT_DEV:
                text_rect = text_surface.get_rect(center=Template.PLAYER_CARD_NUM_CENTER.get(card_type) + self.center)
            else:
                text_rect = text_surface.get_rect(center=Template.PLAYER_CARD_NUM_CENTER.get(card_type) + self.center + Template.PLAYER_UNUSED_CARD_OFFSET)
            gui.screen.blit(text_surface, text_rect)

        # Display Number of Victory Points
        text_surface = number_font.render(str(self.num_points), True, Palette.BLACK)
        text_rect = text_surface.get_rect(center=Template.PLAYER_VP_NUM_CENTER + self.center)
        gui.screen.blit(text_surface, text_rect)

        # Display Visible Buttons
        for button_type, button in self.buttons.items():
            if button.get_visibility():
                button.draw(gui)

    def _draw_update_build_numbers(self, number_font, gui):
        for building_type in BuildingType.BUILD_LIST:
            text_surface = number_font.render(str(self.buildables[building_type]), True, Palette.BLACK)
            text_rect = text_surface.get_rect(center=Template.PLAYER_BUILD_NUM_CENTER[building_type] + self.center)
            gui.screen.blit(text_surface, text_rect)
