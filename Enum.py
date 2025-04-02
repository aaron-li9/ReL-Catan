import numpy as np
import pygame

# BASIC CONSTANTS
VP_GOAL = 10
MAX_PLAYER_NUM = 4
NUM_RESOURCES = 5
NUM_DEV_CARDS = 5
NUM_TOTAL_ROADS = 15
NUM_TOTAL_SETTLEMENTS = 5
NUM_TOTAL_CITIES = 4

ROLL_PRODUCTION_MAP = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}

# BUILDABLE COSTS (SEE RESOURCE TYPE)
ROAD_COST = np.array([0, 0, 0, 1, 1])
SETTLEMENT_COST = np.array([1, 0, 1, 1, 1])
CITY_COST = np.array([2, 3, 0, 0, 0])
DEV_CARD_COST = np.array([1, 1, 1, 0, 0])

DEFAULT_BANK_RESOURCE_NUM = 19

# GUI CONSTANTS
pygame.init()
pygame.font.init()
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

DEFAULT_CENTER = np.zeros(2)
ANIMATION_SPEED = 1  # Smoothing
ANIMATION_FRAMES = 5  # Time
ANIMATION_OFFSET = np.array([0, -ANIMATION_FRAMES * ANIMATION_SPEED])
ANIMATION_STEP = np.array([0, ANIMATION_SPEED])

TILE_SIDE_LENGTH = 80
TILE_OUTLINE_SIZE = 5
TILE_NUMBER_DISPLACEMENT = 15
TILE_NUMBER_RADIUS = 28
TILE_RESOURCE_OFFSET = -40
TILE_X_STEP = TILE_SIDE_LENGTH * np.cos(np.pi / 6)
TILE_Y_STEP = TILE_SIDE_LENGTH * (1 + np.sin(np.pi / 6))

TILE_DIRECTION_MAP = {"NW": 0, "W": 1, "SW": 2, "SE": 3, "E": 4, "NE": 5}
TILE_NEIGHBOR_LIST = [[-1, 0], [-1, -1], [0, -1], [1, 0], [1, 1], [0, 1]]
TILE_CONNECT_LIST = [[1, 0, "SW"], [1, 1, "SE"], [0, 1, "E"]]
TILE_NEIGHBOR_MAP = {"SW": [2, 5], "SE": [3, 0], "E": [4, 1]}
TILE_NEIGHBOR_NODE_MAP = {"SW": {2: 0, 3: 5}, "SE": {3: 1, 4: 0}, "E": {4: 2, 5: 1}}

NUMBER_SIZE = 24
NUMBER_FONT = "Montserrat"
NUMBER_DOTS_DICT = {1: ".....", 2: "....", 3: "...", 4: "..", 5: "."}

HEXAGON_ANGLE = np.pi / 6
HEXAGON_X = np.cos(HEXAGON_ANGLE)
HEXAGON_Y = np.sin(HEXAGON_ANGLE)
HEXAGON_COORDINATE_TEMPLATE = np.array([[0.0, -1.0], [-HEXAGON_X, -HEXAGON_Y], [-HEXAGON_X, HEXAGON_Y],
                                        [0.0, 1.0], [HEXAGON_X, HEXAGON_Y], [HEXAGON_X, -HEXAGON_Y]])
HEXAGON_EDGE_TEMPLATE = np.array([(HEXAGON_COORDINATE_TEMPLATE[0] + HEXAGON_COORDINATE_TEMPLATE[1]) / 2,
                                  (HEXAGON_COORDINATE_TEMPLATE[1] + HEXAGON_COORDINATE_TEMPLATE[2]) / 2,
                                  (HEXAGON_COORDINATE_TEMPLATE[2] + HEXAGON_COORDINATE_TEMPLATE[3]) / 2,
                                  (HEXAGON_COORDINATE_TEMPLATE[3] + HEXAGON_COORDINATE_TEMPLATE[4]) / 2,
                                  (HEXAGON_COORDINATE_TEMPLATE[4] + HEXAGON_COORDINATE_TEMPLATE[5]) / 2,
                                  (HEXAGON_COORDINATE_TEMPLATE[5] + HEXAGON_COORDINATE_TEMPLATE[0]) / 2])

NODE_RADIUS = 15
NODE_RADIUS_ARRAY = np.array([NODE_RADIUS, NODE_RADIUS])

ROAD_LENGTH = 25
ROAD_WIDTH = 2.5
ROAD_OUTLINE = 2.5

PORT_WIDTH = 5
PORT_SHORE_OFFSET = 10
PORT_SHIP_OFFSET = 30
SHIP_DISPLACEMENT = 10

PLAYER_TAG_LENGTH = SCREEN_WIDTH / 6
PLAYER_TAG_WIDTH = SCREEN_HEIGHT / 9
PLAYER_OUTLINE_OFFSET = 5
PLAYER_TAG_OUTLINE = np.array([[-PLAYER_TAG_LENGTH, -PLAYER_TAG_WIDTH], [PLAYER_TAG_LENGTH, -PLAYER_TAG_WIDTH],
                               [PLAYER_TAG_LENGTH, PLAYER_TAG_WIDTH], [-PLAYER_TAG_LENGTH, PLAYER_TAG_WIDTH]])
PLAYER_TAG_TEMPLATE = PLAYER_TAG_OUTLINE + np.array([[PLAYER_OUTLINE_OFFSET, PLAYER_OUTLINE_OFFSET],
                                                     [-PLAYER_OUTLINE_OFFSET, PLAYER_OUTLINE_OFFSET],
                                                     [-PLAYER_OUTLINE_OFFSET, -PLAYER_OUTLINE_OFFSET],
                                                     [PLAYER_OUTLINE_OFFSET, - PLAYER_OUTLINE_OFFSET]])
PLAYER_ICON_CENTER = np.array([(-4 / 5) * PLAYER_TAG_LENGTH, (-3 / 6) * PLAYER_TAG_WIDTH])
PLAYER_TURN_CENTER = np.array([(4 / 5) * PLAYER_TAG_LENGTH, (-3 / 6) * PLAYER_TAG_WIDTH])
PLAYER_ICON_RADIUS = 30
PLAYER_RES_ICON_OFFSET = PLAYER_TAG_LENGTH / 7
PLAYER_BUILD_ICON_OFFSET = PLAYER_TAG_LENGTH / 7
PLAYER_RES_NUM_OFFSET = np.array([40, 0])
PLAYER_BUILD_NUM_OFFSET = np.array([40, 0])
TURN_MARKER_RADIUS = 20

DICE_SIDE_LENGTH = 150
DICE_INTERNAL_OFFSET = 10
DICE_DOT_RADIUS = 15
DICE_DOT_LENGTH = DICE_SIDE_LENGTH / 4


# Enum Values
class GamePhase:

    UNSELECTED = -1
    INIT = 0
    PLACEMENT = 1
    PRE_TURN = 2
    DICE_ROLL = 3
    THEFT = 4
    RESOURCE_DISTRIBUTION = 5
    MID_TURN = 6
    TRADE = 7
    BUILD = 8
    BUILD_ROAD = 9
    BUILD_SETTLEMENT = 10
    BUILD_CITY = 11
    BUILD_DEV_CARD = 12
    DEV_CARD = 13
    END_TURN = 14
    POST_GAME = 15
    KNIGHT = 16
    KNIGHT_ACTION = 17
    MONOPOLY = 18
    MONOPOLY_ACTION = 19
    YEAR_OF_PLENTY = 20
    YEAR_OF_PLENTY_ACTION = 21
    ROAD_BUILDING = 22
    ROAD_BUILDING_ACTION = 23

    WOOD_MONOPOLY = 24
    BRICK_MONOPOLY = 25
    SHEEP_MONOPOLY = 26
    WHEAT_MONOPOLY = 27
    ORE_MONOPOLY = 28


class GameMode:
    HUMAN = 0
    CPU = 1
    DUMMY_PLACEMENTS = 2


class PlayerColor:
    RED = 0
    BLUE = 1
    BLACK = 2
    GREEN = 3

    ID_TO_COLOR = {0: RED, 1: BLUE, 2: BLACK, 3: GREEN}


class ResourceType:
    EMPTY = -1
    WHEAT = 0
    ORE = 1
    SHEEP = 2
    WOOD = 3
    BRICK = 4
    DESERT = 5

    RES_LIST = [WHEAT, ORE, SHEEP, WOOD, BRICK, DESERT]
    STR_TO_RES = {"WOOD": WOOD, "BRICK": BRICK, "SHEEP": SHEEP, "ORE": ORE, "WHEAT": WHEAT, "DESERT": DESERT}

    # Debugging/Terminal Purposes
    RES_TO_STR = {WOOD: "WOOD", BRICK: "BRICK", SHEEP: "SHEEP", ORE: "ORE", WHEAT: "WHEAT", DESERT: "DESERT"}


class HarborType:
    EMPTY = -1
    WHEAT = 0
    ORE = 1
    SHEEP = 2
    WOOD = 3
    BRICK = 4
    THREE2ONE = 5

    STR_TO_HBR = {"WOOD": WOOD, "BRICK": BRICK, "SHEEP": SHEEP, "ORE": ORE, "WHEAT": WHEAT, "THREE2ONE": THREE2ONE}

    # Debugging/Terminal Purposes
    HBR_TO_STR = {WOOD: "WOOD", BRICK: "BRICK", SHEEP: "SHEEP", ORE: "ORE", WHEAT: "WHEAT", THREE2ONE: "THREE2ONE"}


class DevelopmentCardType:
    EMPTY = -1
    VICTORY_POINT_DEV = 0
    KNIGHT = 1
    YEAR_OF_PLENTY = 2
    MONOPOLY = 3
    ROAD_BUILDING = 4

    CARD_LIST = [VICTORY_POINT_DEV, KNIGHT, YEAR_OF_PLENTY, MONOPOLY, ROAD_BUILDING]
    STR_TO_TYPE = {"VICTORY_POINT": VICTORY_POINT_DEV, "KNIGHT": KNIGHT, "YEAR_OF_PLENTY": YEAR_OF_PLENTY,
                   "MONOPOLY": MONOPOLY, "ROAD_BUILDING": ROAD_BUILDING}


class BuildingType:

    EMPTY = -1
    ROAD = 0
    SETTLEMENT = 1
    CITY = 2

    BUILD_LIST = [ROAD, SETTLEMENT, CITY]


class TradeMode:

    PLAYER_BANK = 0
    DISCARD = 1
    YEAR_OF_PLENTY = 2


class ButtonFunctionCode:
    # Replace with direct dependency to GamePhase, etc.
    NO_FUNCTION = -1
    INCREMENT_BY_ONE = 0
    DECREMENT_BY_ONE = 1


class PlayerButtonType:

    THEFT = 0
    BUILD = 1
    TRADE = 2
    DEV_CARD = 3
    END_TURN = 4
    BACK_TO_MENU = 5
    BUILD_SETTLEMENT = 6
    BUILD_ROAD = 7
    BUILD_CITY = 8
    BUILD_DEV_CARD = 9
    BACK_TO_BUILD = 10
    BACK_TO_TRADE = 11
    BACK_TO_DEV_CARD = 12
    PLAY_KNIGHT = 13
    PLAY_MONOPOLY = 14
    PLAY_ROAD_BUILDING = 15
    PLAY_YEAR_OF_PLENTY = 16
    WOOD_MONOPOLY = 17
    BRICK_MONOPOLY = 18
    SHEEP_MONOPOLY = 19
    WHEAT_MONOPOLY = 20
    ORE_MONOPOLY = 21

    PLAYER_PHASE_BUTTONS = {GamePhase.MID_TURN: [BUILD, TRADE, DEV_CARD, END_TURN],
                            GamePhase.BUILD: [BUILD_SETTLEMENT, BUILD_ROAD, BUILD_CITY, BUILD_DEV_CARD, BACK_TO_MENU],
                            GamePhase.DEV_CARD: [PLAY_KNIGHT, PLAY_MONOPOLY, PLAY_YEAR_OF_PLENTY, PLAY_ROAD_BUILDING,
                                                 BACK_TO_MENU],
                            GamePhase.BUILD_ROAD: [BACK_TO_BUILD],
                            GamePhase.BUILD_SETTLEMENT: [BACK_TO_BUILD],
                            GamePhase.BUILD_CITY: [BACK_TO_BUILD],
                            GamePhase.MONOPOLY_ACTION: [WOOD_MONOPOLY, BRICK_MONOPOLY, SHEEP_MONOPOLY, WHEAT_MONOPOLY, ORE_MONOPOLY]}
    BUTTON_TO_PHASE = {BUILD: GamePhase.BUILD,
                       TRADE: GamePhase.TRADE,
                       DEV_CARD: GamePhase.DEV_CARD,
                       END_TURN: GamePhase.END_TURN,
                       BUILD_ROAD: GamePhase.BUILD_ROAD,
                       BUILD_SETTLEMENT: GamePhase.BUILD_SETTLEMENT,
                       BUILD_CITY: GamePhase.BUILD_CITY,
                       BUILD_DEV_CARD: GamePhase.BUILD_DEV_CARD,
                       BACK_TO_MENU: GamePhase.MID_TURN,
                       BACK_TO_BUILD: GamePhase.BUILD,
                       BACK_TO_TRADE: GamePhase.TRADE,
                       BACK_TO_DEV_CARD: GamePhase.DEV_CARD,
                       PLAY_KNIGHT: GamePhase.KNIGHT,
                       PLAY_MONOPOLY: GamePhase.MONOPOLY,
                       PLAY_YEAR_OF_PLENTY: GamePhase.YEAR_OF_PLENTY,
                       PLAY_ROAD_BUILDING: GamePhase.ROAD_BUILDING,
                       WHEAT_MONOPOLY: GamePhase.WHEAT_MONOPOLY,
                       ORE_MONOPOLY: GamePhase.ORE_MONOPOLY,
                       WOOD_MONOPOLY: GamePhase.WOOD_MONOPOLY,
                       BRICK_MONOPOLY: GamePhase.BRICK_MONOPOLY,
                       SHEEP_MONOPOLY: GamePhase.SHEEP_MONOPOLY}


class Palette:
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLACK = (60, 60, 60)
    TRUE_BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_GREY = (230, 230, 230)

    PLAYER_CLR_TO_COLOR = {PlayerColor.RED: RED, PlayerColor.BLUE: BLUE,
                           PlayerColor.BLACK: BLACK, PlayerColor.GREEN: GREEN}

    TILE_COLOR = {ResourceType.WHEAT: (240, 223, 77),
                  ResourceType.ORE: (160, 160, 160),
                  ResourceType.SHEEP: (95, 230, 95),
                  ResourceType.WOOD: (0, 153, 76),
                  ResourceType.BRICK: (242, 100, 44),
                  ResourceType.DESERT: (224, 208, 144)}

    TILE_OUTLINE = (242, 238, 200)
    NUMBER_COLOR_RED = (253, 42, 0)
    NUMBER_COLOR_BLACK = (0, 0, 0)
    NUMBER_TILE = (242, 235, 206)
    BOARD_OCEAN = (0, 140, 255)
    PORT = (174, 115, 57)
    NODE = (120, 212, 0)
    NODE_HIGHLIGHTED = (168, 227, 0)
    ROAD_OUTLINE = (0, 0, 0)
    PLAYER_TAG_OUTLINE = (204, 194, 159)
    PLAYER_TAG = (255, 248, 222)
    TURN_MARKER = (183, 0, 255)


class Images:
    EMPTY = -1
    VICTORY_POINT = -2
    VICTORY_POINT_DEV = -3
    KNIGHT = -4
    YEAR_OF_PLENTY = -5
    MONOPOLY = -6
    ROAD_BUILDING = -7
    TURN_INDICATOR = -8

    THEFT_BUTTON = -20
    THEFT_BUTTON_HIGHLIGHTED = -21
    BUILD_BUTTON = -22
    BUILD_BUTTON_HIGHLIGHTED = -23
    TRADE_BUTTON = -24
    TRADE_BUTTON_HIGHLIGHTED = -25
    DEV_CARD_BUTTON = -26
    DEV_CARD_BUTTON_HIGHLIGHTED = -27
    END_TURN_BUTTON = -28
    END_TURN_BUTTON_HIGHLIGHTED = -29
    BUILD_SETTLEMENT = -30
    BUILD_SETTLEMENT_HIGHLIGHTED = -31
    BUILD_ROAD = -32
    BUILD_ROAD_HIGHLIGHTED = -33
    BUILD_CITY = -34
    BUILD_CITY_HIGHLIGHTED = -35
    KNIGHT_BUTTON = -36
    KNIGHT_BUTTON_HIGHLIGHTED = -37
    MONOPOLY_BUTTON = -38
    MONOPOLY_BUTTON_HIGHLIGHTED = -39
    YEAR_OF_PLENTY_BUTTON = -40
    YEAR_OF_PLENTY_BUTTON_HIGHLIGHTED = -41
    ROAD_BUILDING_BUTTON = -42
    ROAD_BUILDING_BUTTON_HIGHLIGHTED = -43
    WHEAT_BUTTON = -44
    WHEAT_BUTTON_HIGHLIGHT = -45
    WOOD_BUTTON = -46
    WOOD_BUTTON_HIGHLIGHT = -47
    BRICK_BUTTON = -48
    BRICK_BUTTON_HIGHLIGHT = -49
    SHEEP_BUTTON = -50
    SHEEP_BUTTON_HIGHLIGHT = -51
    ORE_BUTTON = -52
    ORE_BUTTON_HIGHLIGHT = -53

    WHEAT_HARBOR = 0
    WOOD_HARBOR = 1
    ORE_HARBOR = 2
    BRICK_HARBOR = 3
    SHEEP_HARBOR = 4
    WHEAT = 5
    WOOD = 6
    ORE = 7
    BRICK = 8
    SHEEP = 9
    THREEFORONE = 10
    BOAT = 11
    DUNES = 12
    DESERT = 13
    ROBBER = 14
    RED_SETTLEMENT = 15
    RED_ROAD = 16
    RED_CITY = 17
    BLUE_SETTLEMENT = 18
    BLUE_ROAD = 19
    BLUE_CITY = 20
    BLACK_SETTLEMENT = 21
    BLACK_ROAD = 22
    BLACK_CITY = 23
    GREEN_SETTLEMENT = 24
    GREEN_ROAD = 25
    GREEN_CITY = 26

    STR_TO_IMG = {"WHEAT_HARBOR": WHEAT_HARBOR, "WOOD_HARBOR": WOOD_HARBOR, "ORE_HARBOR": ORE_HARBOR,
                  "BRICK_HARBOR": BRICK_HARBOR, "SHEEP_HARBOR": SHEEP_HARBOR, "WHEAT": WHEAT, "WOOD": WOOD,
                  "ORE": ORE, "BRICK": BRICK, "SHEEP": SHEEP, "THREEFORONE": THREEFORONE, "BOAT": BOAT,
                  "DUNES": DUNES, "DESERT": DESERT, "ROBBER": ROBBER, "VICTORY_POINT": VICTORY_POINT,
                  "WHEAT_BUTTON": WHEAT_BUTTON, "WHEAT_BUTTON_HIGHLIGHT": WHEAT_BUTTON_HIGHLIGHT,
                  "ORE_BUTTON": ORE_BUTTON, "ORE_BUTTON_HIGHLIGHT": ORE_BUTTON_HIGHLIGHT,
                  "SHEEP_BUTTON": SHEEP_BUTTON, "SHEEP_BUTTON_HIGHLIGHT": SHEEP_BUTTON_HIGHLIGHT,
                  "BRICK_BUTTON": BRICK_BUTTON, "BRICK_BUTTON_HIGHLIGHT": BRICK_BUTTON_HIGHLIGHT,
                  "WOOD_BUTTON": WOOD_BUTTON, "WOOD_BUTTON_HIGHLIGHT": WOOD_BUTTON_HIGHLIGHT,
                  "VICTORY_POINT_DEV": VICTORY_POINT_DEV, "KNIGHT": KNIGHT, "YEAR_OF_PLENTY": YEAR_OF_PLENTY,
                  "MONOPOLY": MONOPOLY, "ROAD_BUILDING": ROAD_BUILDING, "TURN_INDICATOR": TURN_INDICATOR,
                  "THEFT_BUTTON": THEFT_BUTTON, "THEFT_BUTTON_HIGHLIGHT": THEFT_BUTTON_HIGHLIGHTED,
                  "BUILD_BUTTON": BUILD_BUTTON, "BUILD_BUTTON_HIGHLIGHT": BUILD_BUTTON_HIGHLIGHTED,
                  "TRADE_BUTTON": TRADE_BUTTON, "TRADE_BUTTON_HIGHLIGHT": TRADE_BUTTON_HIGHLIGHTED,
                  "DEV_BUTTON": DEV_CARD_BUTTON, "DEV_BUTTON_HIGHLIGHT": DEV_CARD_BUTTON_HIGHLIGHTED,
                  "END_BUTTON": END_TURN_BUTTON, "END_BUTTON_HIGHLIGHT": END_TURN_BUTTON_HIGHLIGHTED,
                  "BUILD_SETTLEMENT_H": BUILD_SETTLEMENT_HIGHLIGHTED, "BUILD_SETTLEMENT": BUILD_SETTLEMENT,
                  "BUILD_ROAD_H": BUILD_ROAD_HIGHLIGHTED, "BUILD_ROAD": BUILD_ROAD,
                  "BUILD_CITY_H": BUILD_CITY_HIGHLIGHTED, "BUILD_CITY": BUILD_CITY,
                  "KNIGHT_BUTTON": KNIGHT_BUTTON, "KNIGHT_BUTTON_HIGHLIGHT": KNIGHT_BUTTON_HIGHLIGHTED,
                  "MONOPOLY_BUTTON": MONOPOLY_BUTTON, "MONOPOLY_BUTTON_HIGHLIGHT": MONOPOLY_BUTTON_HIGHLIGHTED,
                  "YEAR_OF_PLENTY_BUTTON": YEAR_OF_PLENTY_BUTTON, "YEAR_OF_PLENTY_BUTTON_HIGHLIGHT": YEAR_OF_PLENTY_BUTTON_HIGHLIGHTED,
                  "ROAD_BUILDING_BUTTON": ROAD_BUILDING_BUTTON, "ROAD_BUILDING_BUTTON_HIGHLIGHT": ROAD_BUILDING_BUTTON_HIGHLIGHTED,
                  "RED_SETTLEMENT": RED_SETTLEMENT, "RED_ROAD": RED_ROAD, "RED_CITY": RED_CITY,
                  "BLUE_SETTLEMENT": BLUE_SETTLEMENT, "BLUE_ROAD": BLUE_ROAD, "BLUE_CITY": BLUE_CITY,
                  "BLACK_SETTLEMENT": BLACK_SETTLEMENT, "BLACK_ROAD": BLACK_ROAD, "BLACK_CITY": BLACK_CITY,
                  "GREEN_SETTLEMENT": GREEN_SETTLEMENT, "GREEN_ROAD": GREEN_ROAD, "GREEN_CITY": GREEN_CITY}
    RES_TO_IMG = {ResourceType.WHEAT: WHEAT, ResourceType.ORE: ORE, ResourceType.WOOD: WOOD, ResourceType.BRICK: BRICK,
                  ResourceType.SHEEP: SHEEP, ResourceType.DESERT: DESERT}
    CARD_TO_IMG = {DevelopmentCardType.VICTORY_POINT_DEV: VICTORY_POINT_DEV, DevelopmentCardType.KNIGHT: KNIGHT,
                   DevelopmentCardType.YEAR_OF_PLENTY: YEAR_OF_PLENTY, DevelopmentCardType.MONOPOLY: MONOPOLY,
                   DevelopmentCardType.ROAD_BUILDING: ROAD_BUILDING}
    HBR_TO_IMG = {HarborType.WHEAT: WHEAT_HARBOR, HarborType.ORE: ORE_HARBOR, HarborType.WOOD: WOOD_HARBOR,
                  HarborType.BRICK: BRICK_HARBOR, HarborType.SHEEP: SHEEP_HARBOR, HarborType.THREE2ONE: THREEFORONE}
    PLYR_CLR_TO_IMG = {PlayerColor.RED: {BuildingType.SETTLEMENT: RED_SETTLEMENT,
                                         BuildingType.ROAD: RED_ROAD,
                                         BuildingType.CITY: RED_CITY},
                       PlayerColor.BLUE: {BuildingType.SETTLEMENT: BLUE_SETTLEMENT,
                                          BuildingType.ROAD: BLUE_ROAD,
                                          BuildingType.CITY: BLUE_CITY},
                       PlayerColor.BLACK: {BuildingType.SETTLEMENT: BLACK_SETTLEMENT,
                                           BuildingType.ROAD: BLACK_ROAD,
                                           BuildingType.CITY: BLACK_CITY},
                       PlayerColor.GREEN: {BuildingType.SETTLEMENT: GREEN_SETTLEMENT,
                                           BuildingType.ROAD: GREEN_ROAD,
                                           BuildingType.CITY: GREEN_CITY}}


class Template:
    # Array (x, y) where x is horizontal (columns) and y is vertical (rows). Origin is top left corner of screen.

    DEFAULT_BUTTON_SHAPE = np.array([64, 64])

    DEFAULT_BUTTON_UPPER_BOUND = np.array([32, 32])
    DEFAULT_BUTTON_LOWER_BOUND = np.array([-32, -32])

    THEFT_BUTTON_OFFSET = np.array([PLAYER_TAG_LENGTH + 40, -50])

    BUILD_BUTTON_OFFSET = np.array([PLAYER_TAG_LENGTH + 40, -PLAYER_TAG_WIDTH + 32])
    TRADE_BUTTON_OFFSET = np.array([PLAYER_TAG_LENGTH + 40, 0])
    DEV_CARD_BUTTON_OFFSET = np.array([PLAYER_TAG_LENGTH + 40, PLAYER_TAG_WIDTH - 32])

    END_TURN_BUTTON_OFFSET = np.array([PLAYER_TAG_LENGTH + 40 + 10 + 64, 0])
    BUTTON_2_OFFSET = np.array([PLAYER_TAG_LENGTH + 40 + 10 + 64, -PLAYER_TAG_WIDTH + 32])

    MONOPOLY_ACTION_BUTTON_OFFSETS = {ResourceType.WOOD: np.array([64, SCREEN_HEIGHT - 64]),
                                      ResourceType.BRICK: np.array([64 * 2 + 16 * 1, SCREEN_HEIGHT - 64]),
                                      ResourceType.SHEEP: np.array([64 * 3 + 16 * 2, SCREEN_HEIGHT - 64]),
                                      ResourceType.WHEAT: np.array([64 * 4 + 16 * 3, SCREEN_HEIGHT - 64]),
                                      ResourceType.ORE: np.array([64 * 5 + 16 * 4, SCREEN_HEIGHT - 64])}

    TILE_ROBBER_NODE_OFFSET = np.array([40, -20])

    DICE_DOT_CENTERS = {1: np.array([[0, 0]]),
                        2: np.array([[-DICE_DOT_LENGTH, -DICE_DOT_LENGTH], [DICE_DOT_LENGTH, DICE_DOT_LENGTH]]),
                        3: np.array([[-DICE_DOT_LENGTH, -DICE_DOT_LENGTH], [0, 0], [DICE_DOT_LENGTH, DICE_DOT_LENGTH]]),
                        4: np.array([[-DICE_DOT_LENGTH, -DICE_DOT_LENGTH], [-DICE_DOT_LENGTH, DICE_DOT_LENGTH],
                                     [DICE_DOT_LENGTH, -DICE_DOT_LENGTH], [DICE_DOT_LENGTH, DICE_DOT_LENGTH]]),
                        5: np.array([[-DICE_DOT_LENGTH, -DICE_DOT_LENGTH], [-DICE_DOT_LENGTH, DICE_DOT_LENGTH],
                                     [DICE_DOT_LENGTH, -DICE_DOT_LENGTH], [DICE_DOT_LENGTH, DICE_DOT_LENGTH], [0, 0]]),
                        6: np.array([[-DICE_DOT_LENGTH, -DICE_DOT_LENGTH], [-DICE_DOT_LENGTH, 0],
                                     [-DICE_DOT_LENGTH, DICE_DOT_LENGTH], [DICE_DOT_LENGTH, -DICE_DOT_LENGTH],
                                     [DICE_DOT_LENGTH, 0], [DICE_DOT_LENGTH, DICE_DOT_LENGTH]])}

    DICE_OFFSET = np.array([DICE_SIDE_LENGTH / 2, 0])

    DICE_OUTLINE_CORNERS = np.array([[-DICE_SIDE_LENGTH / 2, -DICE_SIDE_LENGTH / 2],
                                     [DICE_SIDE_LENGTH / 2, -DICE_SIDE_LENGTH / 2],
                                     [DICE_SIDE_LENGTH / 2, DICE_SIDE_LENGTH / 2],
                                     [-DICE_SIDE_LENGTH / 2, DICE_SIDE_LENGTH / 2]])

    DICE_INSIDE_CORNERS = np.array([[-DICE_SIDE_LENGTH / 2 + DICE_INTERNAL_OFFSET,
                                     -DICE_SIDE_LENGTH / 2 + DICE_INTERNAL_OFFSET],
                                    [DICE_SIDE_LENGTH / 2 - DICE_INTERNAL_OFFSET,
                                     -DICE_SIDE_LENGTH / 2 + DICE_INTERNAL_OFFSET],
                                    [DICE_SIDE_LENGTH / 2 - DICE_INTERNAL_OFFSET,
                                     DICE_SIDE_LENGTH / 2 - DICE_INTERNAL_OFFSET],
                                    [-DICE_SIDE_LENGTH / 2 + DICE_INTERNAL_OFFSET,
                                     DICE_SIDE_LENGTH / 2 - DICE_INTERNAL_OFFSET]])

    DEFAULT_DICE_LOWER_BOUND = DICE_OUTLINE_CORNERS[0] - DICE_OFFSET
    DEFAULT_DICE_UPPER_BOUND = DICE_OUTLINE_CORNERS[2] + DICE_OFFSET

    PLAYER_VP_ICON_CENTER = np.array([(4 / 6) * PLAYER_TAG_LENGTH - PLAYER_BUILD_ICON_OFFSET,
                                      (-3 / 6) * PLAYER_TAG_WIDTH])
    PLAYER_VP_NUM_CENTER = PLAYER_VP_ICON_CENTER + PLAYER_BUILD_NUM_OFFSET

    PLAYER_DEFAULT_BUILDABLES = np.array([NUM_TOTAL_ROADS, NUM_TOTAL_SETTLEMENTS, NUM_TOTAL_CITIES])

    PLAYER_RES_ICON_CENTER = {ResourceType.WHEAT: np.array([(-4 / 6) * PLAYER_TAG_LENGTH - PLAYER_RES_ICON_OFFSET,
                                                            (4 / 6) * PLAYER_TAG_WIDTH]),
                              ResourceType.ORE: np.array([(-2 / 6) * PLAYER_TAG_LENGTH - PLAYER_RES_ICON_OFFSET,
                                                          (4 / 6) * PLAYER_TAG_WIDTH]),
                              ResourceType.SHEEP: np.array([-PLAYER_RES_ICON_OFFSET, (4 / 6) * PLAYER_TAG_WIDTH]),
                              ResourceType.BRICK: np.array([(2 / 6) * PLAYER_TAG_LENGTH - PLAYER_RES_ICON_OFFSET,
                                                            (4 / 6) * PLAYER_TAG_WIDTH]),
                              ResourceType.WOOD: np.array([(4 / 6) * PLAYER_TAG_LENGTH - PLAYER_RES_ICON_OFFSET,
                                                           (4 / 6) * PLAYER_TAG_WIDTH])}
    PLAYER_RES_NUM_CENTER = {ResourceType.WHEAT: PLAYER_RES_ICON_CENTER[ResourceType.WHEAT] + PLAYER_RES_NUM_OFFSET,
                             ResourceType.ORE: PLAYER_RES_ICON_CENTER[ResourceType.ORE] + PLAYER_RES_NUM_OFFSET,
                             ResourceType.SHEEP: PLAYER_RES_ICON_CENTER[ResourceType.SHEEP] + PLAYER_RES_NUM_OFFSET,
                             ResourceType.BRICK: PLAYER_RES_ICON_CENTER[ResourceType.BRICK] + PLAYER_RES_NUM_OFFSET,
                             ResourceType.WOOD: PLAYER_RES_ICON_CENTER[ResourceType.WOOD] + PLAYER_RES_NUM_OFFSET}
    PLAYER_BUILD_ICON_CENTER = {BuildingType.ROAD: np.array([(-2 / 6) * PLAYER_TAG_LENGTH - PLAYER_BUILD_ICON_OFFSET,
                                                             (-3 / 6) * PLAYER_TAG_WIDTH]),
                                BuildingType.SETTLEMENT: np.array([-PLAYER_BUILD_ICON_OFFSET,
                                                                   (-3 / 6) * PLAYER_TAG_WIDTH]),
                                BuildingType.CITY: np.array([(2 / 6) * PLAYER_TAG_LENGTH - PLAYER_BUILD_ICON_OFFSET,
                                                             (-3 / 6) * PLAYER_TAG_WIDTH])}
    PLAYER_BUILD_NUM_CENTER = {BuildingType.ROAD: PLAYER_BUILD_ICON_CENTER[BuildingType.ROAD] + PLAYER_BUILD_NUM_OFFSET,
                               BuildingType.SETTLEMENT: PLAYER_BUILD_ICON_CENTER[BuildingType.SETTLEMENT]
                                                        + PLAYER_BUILD_NUM_OFFSET,
                               BuildingType.CITY: PLAYER_BUILD_ICON_CENTER[BuildingType.CITY] + PLAYER_BUILD_NUM_OFFSET}
    PLAYER_CARD_ICON_CENTER = {DevelopmentCardType.VICTORY_POINT_DEV: np.array([(-4 / 6) * PLAYER_TAG_LENGTH
                                                                                - PLAYER_RES_ICON_OFFSET,
                                                                                (1 / 8) * PLAYER_TAG_WIDTH]),
                               DevelopmentCardType.KNIGHT: np.array([(-2 / 6) * PLAYER_TAG_LENGTH
                                                                     - PLAYER_RES_ICON_OFFSET,
                                                                     (1 / 8) * PLAYER_TAG_WIDTH]),
                               DevelopmentCardType.YEAR_OF_PLENTY: np.array([-PLAYER_RES_ICON_OFFSET,
                                                                             (1 / 8) * PLAYER_TAG_WIDTH]),
                               DevelopmentCardType.MONOPOLY: np.array([(2 / 6) * PLAYER_TAG_LENGTH
                                                                       - PLAYER_RES_ICON_OFFSET,
                                                                       (1 / 8) * PLAYER_TAG_WIDTH]),
                               DevelopmentCardType.ROAD_BUILDING: np.array([(4 / 6) * PLAYER_TAG_LENGTH
                                                                            - PLAYER_RES_ICON_OFFSET,
                                                                            (1 / 8) * PLAYER_TAG_WIDTH])}
    PLAYER_UNUSED_CARD_OFFSET = np.array([0, 16])
    PLAYER_USED_CARD_OFFSET = np.array([0, -16])
    PLAYER_CARD_NUM_CENTER = {DevelopmentCardType.VICTORY_POINT_DEV: PLAYER_CARD_ICON_CENTER[DevelopmentCardType.VICTORY_POINT_DEV] + PLAYER_RES_NUM_OFFSET,
                              DevelopmentCardType.KNIGHT: PLAYER_CARD_ICON_CENTER[DevelopmentCardType.KNIGHT] + PLAYER_RES_NUM_OFFSET,
                              DevelopmentCardType.MONOPOLY: PLAYER_CARD_ICON_CENTER[DevelopmentCardType.MONOPOLY] + PLAYER_RES_NUM_OFFSET,
                              DevelopmentCardType.ROAD_BUILDING: PLAYER_CARD_ICON_CENTER[DevelopmentCardType.ROAD_BUILDING] + PLAYER_RES_NUM_OFFSET,
                              DevelopmentCardType.YEAR_OF_PLENTY: PLAYER_CARD_ICON_CENTER[DevelopmentCardType.YEAR_OF_PLENTY] + PLAYER_RES_NUM_OFFSET}
