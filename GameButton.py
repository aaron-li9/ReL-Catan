from Utility import *
from Enum import *


class Button:

    def __init__(self, button_shape=Template.DEFAULT_BUTTON_SHAPE):
        self._center = DEFAULT_CENTER
        self._shape = button_shape
        self._upper_bound = self._shape / 2.0
        self._lower_bound = self._shape / -2.0

        self._function_code = ButtonFunctionCode.NO_FUNCTION        # Change this later

        self._image_id = None
        self._image_highlighted_id = None

        self._is_highlighted = False
        self._is_visible = False

    def set_center(self, center):
        self._center = center
        self._upper_bound += center
        self._lower_bound += center

    def set_bounds(self, lower_bound, upper_bound):
        self._lower_bound = lower_bound + self._center
        self._upper_bound = upper_bound + self._center

    def set_image_id(self, image_id, image_highlighted_id=None):
        self._image_id = image_id
        self._image_highlighted_id = image_highlighted_id

    def set_visibility(self, is_visible):
        self._is_visible = is_visible

    def set_highlight(self, is_highlighted):
        self._is_highlighted = is_highlighted

    def set_function_code(self, function_code):
        self._function_code = function_code

    def get_center(self):
        return self._center

    def get_visibility(self):
        return self._is_visible

    def get_function_code(self):
        return self._function_code

    def is_mouse_inbound(self, mouse_position):
        if self._lower_bound[0] <= mouse_position[0] <= self._upper_bound[0]:
            if self._lower_bound[1] <= mouse_position[1] <= self._upper_bound[1]:
                return True
        return False

    def draw(self, gui):
        ## Check if the image is loaded in before blitting
        if self._image_highlighted_id is not None and self._is_highlighted:
            image = gui.get_image(self._image_highlighted_id)
        else:
            image = gui.get_image(self._image_id)
        image_rect = image.get_rect(center=self._center)
        gui.screen.blit(image, image_rect)

