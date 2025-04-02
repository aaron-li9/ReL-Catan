from Enum import *
from Utility import *
from Board import Board
import os


class GUI:

    def __init__(self):
        # Dimensions
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.center = np.array([SCREEN_WIDTH, SCREEN_HEIGHT]) / 2

        # Images
        self.image_dir = None
        self.images = dict()

        # Game Components
        self.players = None
        self.board = None
        self.board_image = None
        self.robber = None
        self.dice = None
        self.development_deck = None

    def set_board(self, board):
        self.board = board

    def set_development_deck(self, development_deck):
        self.development_deck = development_deck

    def set_robber(self, robber):
        self.robber = robber

    def set_dice(self, dice):
        self.dice = dice

    def set_players(self, players):
        self.players = players

    def set_image_dir(self, image_dir):
        self.image_dir = image_dir

    def get_image(self, image_enum):
        return self.images.get(image_enum)

    def draw_game(self):
        self.board.draw(self)
        self._draw_player_scoreboards()
        pygame.image.save(self.screen, "current_board.png")
        self.board_image = pygame.image.load("current_board.png")

        self._draw_updated_numbers()
        self._draw_board_pieces()
        self.update()

    def _draw_board_pieces(self):
        self.robber.draw(self)
        self.dice.draw(self)
        self.development_deck.draw(self)

    def _draw_player_scoreboards(self):
        for player_id, player in self.players.items():
            player.draw_scoreboard(self)

    def _draw_updated_numbers(self):
        self._draw_development_deck_update()
        self._draw_player_update()

    def _draw_development_deck_update(self):
        self.development_deck.draw_update(self)

    def _draw_player_update(self):
        for player_id, player in self.players.items():
            player.draw_update(self)

    def load_images(self):
        with open(self.image_dir, mode="r") as read_file:
            for line in read_file:
                image_code, image_path = line.strip().split()
                if image_code == "ENUM_CODE": continue
                image_enum = Images.STR_TO_IMG.get(image_code, Images.EMPTY)
                if image_enum != Images.EMPTY and os.path.isfile(image_path):
                    self.images.update({image_enum: pygame.image.load(image_path)})
                else:
                    print("COULD NOT LOAD IMAGE AT ", image_path)

    def reload_game(self):
        screen_rect = self.board_image.get_rect(center=self.center)
        self.screen.blit(self.board_image, screen_rect)
        self._draw_updated_numbers()
        self._draw_board_pieces()

    @staticmethod
    def update():
        pygame.display.update()