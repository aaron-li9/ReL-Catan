import pygame

from Enum import *
from Utility import *
from GUI import GUI
from Board import Board
from BoardPieces import Robber, Dice
from Player import Player
from DevelopmentCards import DevelopmentCardDeck
from DummyPlacementModel import *
import random


class Mouse:

    def __init__(self):
        self._is_pressed = False
        self._is_clicked = False
        self._is_mouse_button_down = False
        self._is_mouse_button_up = False
        self.position = np.zeros(2)

    def update_click(self):
        if not self._is_mouse_button_down and not self._is_mouse_button_up:
            self._is_clicked = False
        if self._is_mouse_button_down:
            self._is_pressed = True
        elif self._is_mouse_button_up:
            if self._is_pressed:
                self._is_clicked = True
            self._is_pressed = False

    def reset_mouse_button(self):
        self._is_mouse_button_down = False
        self._is_mouse_button_up = False

    def set_mouse_button_down(self):
        self._is_mouse_button_down = True

    def set_mouse_button_up(self):
        self._is_mouse_button_up = True

    def update_position(self, position):
        self.position = np.asarray(position)

    def get_position(self):
        return self.position

    def is_clicked(self):
        return self._is_clicked

    def is_pressed(self):
        return self._is_pressed


class Game:

    def __init__(self, game_mode=GameMode.HUMAN):
        # Game Type
        self.game_mode = game_mode

        # Game State
        self.num_players = 0
        self.players = dict()
        self.player_order = list()
        self.turn = 0
        self.game_over = False
        self.game_phase = GamePhase.INIT
        self.current_turn = 0

        # Placement Phase Variables
        self.placement_order = list()
        self.placement_status = list()
        self.placement_turn = 0

        # Road Building Phase Variables
        self.n_roads_built = 0

        # Robber Phase Variables
        self.players_nearby = set()
        self.selected_robber_node = None
        self.moved_robber = False
        self.has_robbed = False

        # Dice Phase Variables
        self.has_rolled = False

        # Player Button Selection Variable (Mid Turn + Build)
        self.selected_game_phase = GamePhase.UNSELECTED
        self.selected_settlement_node = None
        self.selected_road_node = None
        self.selected_city_node = None

        # Game Components
        self.board_file = None
        self.development_file = None
        self.images_dir = None
        self.board = Board()
        self.development_deck = DevelopmentCardDeck()
        self.robber = Robber()
        self.dice = Dice()
        self.gui = GUI()

        # Mouse
        self.mouse = Mouse()

    # def get_players(self):
    #     while self.num_players > 4 or self.num_players < 3:
    #         self.num_players = int(input('Number of Players (3 or 4): '))
    #
    #     colors = {'RED': (255, 0, 0), 'BLUE': (0, 0, 255), 'GREEN': (0, 255, 0), 'GREY': (60, 60, 60)}
    #
    #     player_colors = list([color, colors[color]] for color in colors)
    #     random.shuffle(player_colors)
    #
    #     for i in range(self.num_players):
    #         number = i + 1
    #         player_name = input('Enter Player {0}\'s Name: '.format(number))
    #         color_register = player_colors.pop()
    #         self.players.append(Player(player_name, color_register[0], color_register[1]))
    #
    #     random.shuffle(self.players)
    #
    #     print('---- PLAYERS ----')
    #     for player in self.players:
    #         print(player.name)

    # def get_turn_player(self):
    #     return self.players[(self.current_turn - 1) % self.num_players]

    def set_board_file(self, board_file):
        self.board_file = board_file

    def set_development_file(self, development_file: str):
        self.development_file = development_file

    def set_images_dir(self, images_dir):
        self.images_dir = images_dir

    def set_game_mode(self, game_mode):
        self.game_mode = game_mode

    def set_num_players(self, num_players):
        self.num_players = num_players

    def _initialize_game(self):
        # Get Number of Players (Can be more robust)
        while not self.num_players:
            num_players = int(input("How many players? (3 or 4): "))
            if 3 <= num_players <= 4:
                self.num_players = num_players

        # Create Players
        self._initialize_players()

        # Check if current game includes HUMAN Players or CPU Players ONLY. (NEED TO ADD)
        if self.game_mode == GameMode.HUMAN:
            pass

        # Initialize GUI
        self._initialize_gui()

        # Initialize Board
        self._initialize_board()

        # Initialize Development Card Deck
        self._initialize_development_deck()

        # Initialize Robber
        self._initialize_robber()

        # Initialize Dice
        self._initialize_dice()

        # Draw the game
        self.gui.draw_game()

        # Signal transition to placement phase
        self.game_phase = GamePhase.PLACEMENT

    def _initialize_gui(self):
        self.gui.set_image_dir(self.images_dir)
        self.gui.load_images()

    def _initialize_players(self):
        # Randomize Player Order
        self.player_order = [player_id for player_id in range(self.num_players)]
        random.shuffle(self.player_order)

        # Initialize Players
        for list_index, player_id in enumerate(self.player_order):
            new_player = Player(player_id)
            new_center = np.array([PLAYER_TAG_LENGTH, PLAYER_TAG_WIDTH +
                                   (2 * list_index * PLAYER_TAG_WIDTH) - list_index * (PLAYER_OUTLINE_OFFSET / 2)])
            new_player.set_center(new_center)
            self.players.update({player_id: new_player})

        # Find Placement order
        self.placement_order = self.player_order + self.player_order[::-1]
        self.placement_status = [[None, None] for x in range(self.num_players)]
        self.gui.set_players(self.players)

    def _initialize_board(self):
        self.board.set_generator_file(self.board_file)
        self.board.set_center(2 * SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2)
        self.board.generate_board()
        self.gui.set_board(self.board)

    def _initialize_development_deck(self):
        self.development_deck.set_generator_file(self.development_file)
        self.development_deck.set_center(np.array([SCREEN_WIDTH - 128, 32]))
        self.development_deck.generate_deck()
        self.gui.set_development_deck(self.development_deck)

    def _initialize_robber(self):
        for index, tile in self.board.get_tile_grid().items():
            if tile.get_resource() == ResourceType.DESERT:
                self.robber.place_on_tile(tile.get_robber_node())
        self.gui.set_robber(self.robber)

    def _initialize_dice(self):
        self.dice.set_center(np.array([SCREEN_WIDTH - DICE_SIDE_LENGTH, SCREEN_HEIGHT - DICE_SIDE_LENGTH / 2]))
        self.gui.set_dice(self.dice)

    def _update_keybinds(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                self.mouse.set_mouse_button_down()
            if event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[0]:
                self.mouse.set_mouse_button_up()

        # Update Mouse Position
        self.mouse.update_click()
        self.mouse.update_position(pygame.mouse.get_pos())
        self.mouse.reset_mouse_button()

    def _get_current_player(self) -> Player:
        player_order_index = self.turn % self.num_players
        player_index = self.player_order[player_order_index]
        return self.players[player_index]

    def _play_placement(self):
        # Check if placement is finished
        if self.placement_turn < len(self.placement_order):
            # Get player information
            player_id = self.placement_order[self.placement_turn]
            player = self.players.get(player_id)
            player.set_turn(True)

            # Reload Board
            self.gui.reload_game()

            # Get placement status
            node, edge = self.placement_status[player_id]

            # If player has not placed settlement, give opportunity to place
            if node is None:
                self._player_settlement_placement(player)

            # If player has not placed road, have them place
            elif edge is None:
                self._player_road_placement(player, node)

            # Update placement status
            node, edge = self.placement_status[player_id]

            # If player has completed settlement and road placement, increment the turn order
            if node is not None and edge is not None:
                # Check if second settlement, then give resources
                self._hand_out_starting_resources(node)

                # Move onto next Player
                self.placement_status[player_id] = [None, None]
                self.placement_turn += 1
                player.set_turn(False)
        else:
            # Set the first player in the order
            self._get_current_player().set_turn(True)

            # Reload Game GUI
            self.gui.reload_game()

            # Set Game Phase to Pre-Turn
            self.game_phase = GamePhase.PRE_TURN

    def _player_settlement_placement(self, player):
        self._player_build_settlement(player, placement=True)

    def _player_road_placement(self, player, node):
        self._player_build_road(player, is_free=True, placement_node=node)

    def _hand_out_starting_resources(self, node):
        # Check if players are placing second settlements
        if self.placement_turn >= self.num_players:
            node_tiles = node.get_tiles()
            player = node.get_player()
            for tile in node_tiles:
                player.add_resource(tile.get_resource(), 1)

    def _play_pre_turn(self):
        self.gui.reload_game()
        self._get_current_player().update_pre_turn()
        ### TO DO ####
        # Add development Card option
        self.game_phase = GamePhase.DICE_ROLL

    def _play_dice_roll(self):
        # Check if player has rolled, if not check if they do roll on GUI
        if not self.has_rolled:
            self._select_dice_roll()
        # Else, roll the dice
        else:
            self.has_rolled = False
            self.dice.set_highlighted(False)
            roll = self.dice.roll()
            if roll == 7:
                self.game_phase = GamePhase.THEFT
            else:
                self.game_phase = GamePhase.RESOURCE_DISTRIBUTION
        self.gui.reload_game()

    def _select_dice_roll(self):
        if self.dice.is_mouse_inbound(self.mouse.get_position()):
            self.dice.set_highlighted(True)
            if self.mouse.is_clicked():
                self.has_rolled = True
        else:
            self.dice.set_highlighted(False)

    def _play_theft(self, is_knight=False):
        self.gui.reload_game()
        # Find all the available nodes and check if player selects the node
        self.selected_robber_node = None
        if not self.moved_robber:
            self._move_robber()

        # If player chose robber placement, place robber
        if self.selected_robber_node is not None:
            self.robber.remove_from_tile()
            self.robber.place_on_tile(self.selected_robber_node)
            self.moved_robber = True
            self.gui.reload_game()
            self._get_players_nearby()

        # Rob the players on the tile
        if self.moved_robber and not self.has_robbed:
            self._select_player_to_rob()

        if self.has_robbed:
            self.gui.reload_game()
            self.moved_robber = False
            self.has_robbed = False
            if is_knight:
                self.game_phase = GamePhase.DEV_CARD
            else:
                self.game_phase = GamePhase.MID_TURN

    def _get_players_nearby(self):
        # AGAIN MORE ROBUST IMPLEMENTATION IS IF ABSTRACT CLASS WAS USED
        self.players_nearby = set()
        tiles = self.robber.get_robber_node().get_tiles()
        current_player = self._get_current_player()
        for tile in tiles:
            for node in tile.get_nodes():
                player = node.get_player()
                if player is not None and player is not current_player:
                    self.players_nearby.add(player)

    def _move_robber(self):
        for robber_node in self.board.get_robber_nodes():
            if robber_node.get_robber() is None:
                if robber_node.is_mouse_inbound(self.mouse.get_position()):
                    robber_node.set_highlight(True)
                    if self.mouse.is_clicked():
                        self.selected_robber_node = robber_node
                else:
                    robber_node.set_highlight(False)
                robber_node.draw(self.gui)

    def _select_player_to_rob(self):
        # Get available players
        current_player = self._get_current_player()
        selected_player = None
        num_nearby_players = len(self.players_nearby)
        if num_nearby_players > 1:
            for player in self.players_nearby:
                if player is not current_player:
                    player.set_button_visibility(PlayerButtonType.THEFT, True)
                    if player.is_button_inbound(PlayerButtonType.THEFT, self.mouse.get_position()):
                        player.set_button_highlight(PlayerButtonType.THEFT, True)
                        if self.mouse.is_clicked():
                            selected_player = player
                    else:
                        player.set_button_highlight(PlayerButtonType.THEFT, False)
        elif num_nearby_players == 1:
            selected_player = self.players_nearby.pop()

        if selected_player is not None or num_nearby_players == 0:
            for player in self.players_nearby:
                player.set_button_visibility(PlayerButtonType.THEFT, False)
            if num_nearby_players != 0:
                stolen_resource = selected_player.get_robbed()
                current_player.add_resource(stolen_resource, 1)
            self.has_robbed = True

    def _play_resource_distribution(self):
        cur_roll = self.dice.get_current_roll()                 # Find the current roll
        tiles = self.board.get_tiles_from_number(cur_roll)      # Find the tiles matching the roll number
        for tile in tiles:
            tile.distribute_resource()          # For each tile, give players with built nodes their resources
        self.gui.reload_game()
        self.game_phase = GamePhase.MID_TURN

    def _play_mid_turn(self):
        self.gui.reload_game()
        self._detect_player_button_input()
        self._activate_player_button_input()
        self._check_player_win()

    def _check_player_win(self):
        if self._get_current_player().has_won_game():
            self.game_phase = GamePhase.POST_GAME

    def _play_trade(self):
        self.game_phase = GamePhase.MID_TURN    # Placeholder

    def _play_build(self):
        self.gui.reload_game()
        self._detect_player_button_input()
        self._activate_player_button_input()
        self._check_player_win()

    def _play_build_road(self):
        self.gui.reload_game()
        self._detect_player_button_input()
        self._activate_player_button_input()
        self._player_build_road(self._get_current_player())
        self._check_player_win()

    def _play_build_settlement(self):
        self.gui.reload_game()
        self._detect_player_button_input()
        self._activate_player_button_input()
        self._player_build_settlement(self._get_current_player())
        self._check_player_win()

    def _play_build_city(self):
        self.gui.reload_game()
        self._detect_player_button_input()
        self._activate_player_button_input()
        self._player_build_city(self._get_current_player())
        self._check_player_win()

    def _play_build_dev_card(self):
        self.gui.reload_game()
        self._get_current_player().build_dev_card(self.development_deck)
        self.game_phase = GamePhase.BUILD
        self._check_player_win()
        self.gui.reload_game()

    def _player_build_road(self, player, is_free=False, placement_node=None) -> bool:
        if placement_node is not None:
            available_nodes = placement_node.get_edges()
        else:
            available_nodes = player.get_available_road_nodes()
        for road_node in available_nodes:
            if road_node.is_mouse_inbound(self.mouse.get_position()):
                road_node.set_highlight(True)
                if self.mouse.is_clicked():
                    self.selected_road_node = road_node
            else:
                road_node.set_highlight(False)
            road_node.draw(self.gui)

        if self.selected_road_node is not None:
            if placement_node is not None:
                self.placement_status[player.get_id()][1] = self.selected_road_node
            player.build_road(self.selected_road_node, self.gui, self.board, is_free=is_free)

            # Universally update local player availabilities
            for _, selected_player in self.players.items():
                nodes_to_remove = set()
                for road_node in selected_player.get_available_road_nodes():
                    if road_node not in self.board.get_open_edges():
                        nodes_to_remove.add(road_node)
                for road_node in nodes_to_remove:
                    selected_player.remove_road_node(road_node)

            self.selected_road_node = None
            return True
        return False

    def _player_build_settlement(self, player, placement=False):
        # Find all the available nodes and check if player selects the node
        if placement:
            available_nodes = self.board.get_open_settlement_nodes()
        else:
            available_nodes = player.get_available_settlement_nodes()
        for settlement_node in available_nodes:
            if settlement_node.is_mouse_inbound(self.mouse.get_position()):
                settlement_node.set_highlight(True)
                if self.mouse.is_clicked():
                    self.selected_settlement_node = settlement_node
            else:
                settlement_node.set_highlight(False)
            settlement_node.draw(self.gui)

        # If player chose settlement, place settlement and move on
        if self.selected_settlement_node is not None:
            if placement:
                self.placement_status[player.get_id()][0] = self.selected_settlement_node
            player.build_settlement(self.selected_settlement_node, self.gui, self.board, placement=placement)

            # Universally update local player availabilities
            for _, selected_player in self.players.items():
                nodes_to_remove = set()
                for node in selected_player.get_available_settlement_nodes():
                    if node not in self.board.get_open_settlement_nodes():
                        nodes_to_remove.add(node)
                for node in nodes_to_remove:
                    selected_player.remove_settlement_node(node)

            self.selected_settlement_node = None

    def _player_build_city(self, player):
        for city_node in player.get_available_city_nodes():
            if city_node.is_mouse_inbound(self.mouse.get_position()):
                city_node.set_highlight(True)
                if self.mouse.is_clicked():
                    self.selected_city_node = city_node
            else:
                city_node.set_highlight(False)
            city_node.draw(self.gui)

        if self.selected_city_node is not None:
            player.build_city(self.selected_city_node, self.gui, self.board)
            self.selected_city_node = None

    def _play_dev_card(self):
        self.gui.reload_game()
        self._detect_player_button_input()
        self._activate_player_button_input()
        self._check_player_win()

    def _can_play_dev_card(self, card_type: DevelopmentCardType) -> bool:
        # Check if current player can play development card
        current_player = self._get_current_player()
        if current_player.available_dev_cards[card_type] and not current_player.used_dev_card:
            # Update player counts
            current_player.used_dev_cards[card_type] += 1
            current_player.unused_dev_cards[card_type] -= 1
            current_player.used_dev_card = True
            return True
        return False

    def _play_knight(self):
        if self._can_play_dev_card(DevelopmentCardType.KNIGHT):
            self.game_phase = GamePhase.KNIGHT_ACTION
        else:
            self.game_phase = GamePhase.DEV_CARD

    def _play_knight_action(self):
        self._play_theft(is_knight=True)

    def _play_year_of_plenty(self):
        if self._can_play_dev_card(DevelopmentCardType.YEAR_OF_PLENTY):
            self.game_phase = GamePhase.YEAR_OF_PLENTY_ACTION
        else:
            self.game_phase = GamePhase.DEV_CARD

    # TODO
    def _play_year_of_plenty_action(self):
        pass

    def _play_monopoly(self):
        if self._can_play_dev_card(DevelopmentCardType.MONOPOLY):
            self.game_phase = GamePhase.MONOPOLY_ACTION
        else:
            self.game_phase = GamePhase.DEV_CARD

    def _play_monopoly_action(self):
        self.gui.reload_game()
        self._detect_player_button_input()
        self._activate_player_button_input()

    def _play_monopoly_action_resource(self, resource_type):
        self.gui.reload_game()
        current_player = self._get_current_player()
        for _, player in self.players.items():
            if current_player != player:
                n_resources = player.resources[resource_type]
                current_player.resources[resource_type] += n_resources
                player.resources[resource_type] -= n_resources
        self.game_phase = GamePhase.DEV_CARD

    def _play_road_building(self):
        if self._can_play_dev_card(DevelopmentCardType.ROAD_BUILDING):
            self.game_phase = GamePhase.ROAD_BUILDING_ACTION
        else:
            self.game_phase = GamePhase.DEV_CARD

    def _play_road_building_action(self):
        if self.n_roads_built < 2:
            has_built_road = self._player_build_road(self._get_current_player(), is_free=True)
            if has_built_road:
                self.n_roads_built += 1
        else:
            self.n_roads_built = 0
            self.game_phase = GamePhase.DEV_CARD

    def _play_end_turn(self):
        self.gui.reload_game()
        self._get_current_player().set_turn(False)
        self.turn += 1
        self._get_current_player().set_turn(True)
        self.game_phase = GamePhase.PRE_TURN

    def _detect_player_button_input(self):
        # Get Current Player
        current_player = self._get_current_player()
        player_button_set = PlayerButtonType.PLAYER_PHASE_BUTTONS.get(self.game_phase, None)

        if player_button_set is not None:
            # Show Usable Buttons
            for button_type in player_button_set:
                current_player.set_button_visibility(button_type, True)
                if current_player.is_button_inbound(button_type, self.mouse.get_position()):
                    current_player.set_button_highlight(button_type, True)
                    if self.mouse.is_clicked():
                        self.selected_game_phase = PlayerButtonType.BUTTON_TO_PHASE.get(button_type)
                else:
                    current_player.set_button_highlight(button_type, False)

    def _activate_player_button_input(self):
        # Get Current Player
        current_player = self._get_current_player()
        player_button_set = PlayerButtonType.PLAYER_PHASE_BUTTONS.get(self.game_phase, None)

        if player_button_set is not None:
            # Listen for Actions
            if self.selected_game_phase != GamePhase.UNSELECTED:
                for button_type in player_button_set:
                    current_player.set_button_highlight(button_type, False)
                    current_player.set_button_visibility(button_type, False)
                self.gui.reload_game()
                self.game_phase = self.selected_game_phase
                self.selected_game_phase = GamePhase.UNSELECTED

    def play(self):
        # Initialize Game
        if self.game_mode != GameMode.DUMMY_PLACEMENTS:
            self._initialize_game()
        # Game Loop
        while not self.game_over:
            # Check initial key bindings
            self._update_keybinds()

            # Check which game phase, and act its function
            if self.game_phase == GamePhase.PLACEMENT:
                self._play_placement()
            elif self.game_phase == GamePhase.PRE_TURN:
                self._play_pre_turn()
            elif self.game_phase == GamePhase.DICE_ROLL:
                self._play_dice_roll()
            elif self.game_phase == GamePhase.RESOURCE_DISTRIBUTION:
                self._play_resource_distribution()
            elif self.game_phase == GamePhase.THEFT:
                self._play_theft()
            elif self.game_phase == GamePhase.KNIGHT:
                self._play_knight()
            elif self.game_phase == GamePhase.KNIGHT_ACTION:
                self._play_knight_action()
            elif self.game_phase == GamePhase.MONOPOLY:
                self._play_monopoly()
            elif self.game_phase == GamePhase.MONOPOLY_ACTION:
                self._play_monopoly_action()
            elif self.game_phase == GamePhase.WHEAT_MONOPOLY:
                self._play_monopoly_action_resource(ResourceType.WHEAT)
            elif self.game_phase == GamePhase.ORE_MONOPOLY:
                self._play_monopoly_action_resource(ResourceType.ORE)
            elif self.game_phase == GamePhase.WOOD_MONOPOLY:
                self._play_monopoly_action_resource(ResourceType.WOOD)
            elif self.game_phase == GamePhase.BRICK_MONOPOLY:
                self._play_monopoly_action_resource(ResourceType.BRICK)
            elif self.game_phase == GamePhase.SHEEP_MONOPOLY:
                self._play_monopoly_action_resource(ResourceType.SHEEP)
            elif self.game_phase == GamePhase.YEAR_OF_PLENTY:
                self._play_year_of_plenty()
            elif self.game_phase == GamePhase.ROAD_BUILDING:
                self._play_road_building()
            elif self.game_phase == GamePhase.ROAD_BUILDING_ACTION:
                self._play_road_building_action()
            elif self.game_phase == GamePhase.MID_TURN:
                self._play_mid_turn()
            elif self.game_phase == GamePhase.TRADE:
                self._play_trade()
            elif self.game_phase == GamePhase.BUILD:
                self._play_build()
            elif self.game_phase == GamePhase.BUILD_ROAD:
                self._play_build_road()
            elif self.game_phase == GamePhase.BUILD_SETTLEMENT:
                self._play_build_settlement()
            elif self.game_phase == GamePhase.BUILD_CITY:
                self._play_build_city()
            elif self.game_phase == GamePhase.BUILD_DEV_CARD:
                self._play_build_dev_card()
            elif self.game_phase == GamePhase.DEV_CARD:
                self._play_dev_card()
            elif self.game_phase == GamePhase.END_TURN:
                self._play_end_turn()

            self.gui.update()


def test_dummy_placements(game : Game, dpm):
    game._initialize_game()
    test_list = list(game.players.keys())
    for i in range(len(test_list)):
        player = game.players[test_list[i]]
        dpm.place_settlement(player)

    for i in range(len(game.players.keys()) - 1, -1, -1):
        player = game.players[test_list[i]]
        node = dpm.place_settlement(player)

        #handing out starting resources, but without the if statement because here placement status isn't updated
        node_tiles = node.get_tiles()
        player = node.get_player()
        for tile in node_tiles:
            player.add_resource(tile.get_resource(), 1)

        game.gui.update()


def dummy_placements():
    mode = GameMode.DUMMY_PLACEMENTS
    development_f = "standard_development.txt"
    board_f = "standard_board.txt"
    image_d = "image_map.txt"

    game = Game(mode)
    dpm = DummyPlacementModel(game)
    game.set_development_file(development_f)
    game.set_board_file(board_f)
    game.set_images_dir(image_d)
    game.set_num_players(4)
    test_dummy_placements(game, dpm)
    game.game_phase = GamePhase.PRE_TURN
    game.play()  # a little bit flawed because the test_dummy_placements doesn't fully do everything correctly
    # need it to do everything correctly so that we can use it to actually train a DQN for game actions


def main():
    mode = GameMode.CPU
    development_f = "standard_development.txt"
    board_f = "standard_board.txt"
    image_d = "image_map.txt"

    game = Game(mode)
    game.set_development_file(development_f)
    game.set_board_file(board_f)
    game.set_images_dir(image_d)
    game.set_num_players(4)
    #game._initialize_game()
    print("Got to here")
    game.play()         #a little bit flawed because the test_dummy_placements doesn't fully do everything correctly
    #need it to do everything correctly so that we can use it to actually train a DQN for game actions


if __name__ == "__main__":
    #main()
    dummy_placements()