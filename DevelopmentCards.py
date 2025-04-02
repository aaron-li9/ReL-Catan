from Utility import *
from Enum import *


# class DevelopmentCard:
#
#     def __init__(self, card_type: DevelopmentCardType):
#         self._player = None
#         self._card_type = card_type
#
#     def get_player(self):
#         return self._player
#
#     def get_card_type(self):
#         return self._card_type
#
#     def set_player(self, player):
#         self._player = player
#
#     def use_ability(self):
#         if self._card_type == DevelopmentCardType.MONOPOLY:
#             self._use_ability_monopoly()
#         elif self._card_type == DevelopmentCardType.YEAR_OF_PLENTY:
#             self._use_ability_year_of_plenty()
#         elif self._card_type == DevelopmentCardType.ROAD_BUILDING:
#             self._use_ability_knight()
#         elif self._card_type == DevelopmentCardType.KNIGHT:
#             self._use_ability_knight()
#         elif self._card_type == DevelopmentCardType.VICTORY_POINT_DEV:
#             self._use_ability_victory_point()
#
#     def _use_ability_victory_point(self):
#         self._player.hidden_points += 1
#
#     def _use_ability_monopoly(self, resource_type: ResourceType, players):
#         for _, player in players:
#             if player != self._player:
#                 num_resource = player.resources[resource_type]
#                 self._player.resources[resource_type] += num_resource
#                 player.resources[resource_type] -= num_resource
#
#     def _use_ability_year_of_plenty(self):
#         pass
#
#     def _use_ability_road_building(self):
#         pass
#
#     def _use_ability_knight(self):
#         pass


class DevelopmentCardDeck:

    def __init__(self):
        self._generator_file = None
        self._card_frequency = dict()
        self._deck = list()
        self._center = DEFAULT_CENTER

    def generate_deck(self):
        self._read_generation_file()
        self._create_randomized_deck()

    def draw_card(self):
        if len(self._deck) > 0:
            return self._deck.pop()
        else:
            return None

    def get_deck_size(self):
        return len(self._deck)

    def set_center(self, center):
        self._center = center

    def _create_randomized_deck(self):
        for card_type, frequency in self._card_frequency.items():
            self._deck += [card_type for freq in range(frequency)]
        random.shuffle(self._deck)

    def _read_generation_file(self):
        with open(self._generator_file, mode="r") as read_file:
            for line in read_file.readlines():
                card_type, freq = line.strip().split()
                self._card_frequency[DevelopmentCardType.STR_TO_TYPE.get(card_type)] = int(freq)

    def set_generator_file(self, generator_file: str):
        self._generator_file = generator_file

    def draw_update(self, gui):
        number_font = pygame.font.SysFont(NUMBER_FONT, NUMBER_SIZE, bold=True)
        text_surface = number_font.render(str(len(self._deck)), True, Palette.TRUE_BLACK)
        text_rect = text_surface.get_rect(center=self._center + np.array([64, 0]))
        gui.screen.blit(text_surface, text_rect)

    def draw(self, gui):
        image_icon = gui.get_image(Images.DEV_CARD_BUTTON)
        image_rect = image_icon.get_rect(center=self._center)
        gui.screen.blit(image_icon, image_rect)
