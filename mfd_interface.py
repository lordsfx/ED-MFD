import pygame
from constants import *
from library import *

# class MFD
class MFD:
    scale = 1
    font = None

    @staticmethod
    def set_scale(scale):
        MFD.scale = scale

    def set_font(font_file):
        MFD.font = pygame.font.Font(font_file, FONT_SIZE)

    def sd(dim):
        return int(dim * MFD.scale)


# class Button
class Button(object):
    TYPE_PUSH   = 1
    TYPE_TOGGLE = 2
    TYPE_HOLD   = 3
    TYPE_SWITCH_1 = 11
    STATE_RELEASED = STATE_OFF = 0
    STATE_PUSHED   = STATE_ON  = STATE_HOLD = 1
    TIMER_STEP   = 5  # milliseconds
    TIMER_PUSH   = TIMER_STEP * 2
    TIMER_HOLD   = TIMER_STEP * 20
    TIMER_TOGGLE = -1
    TIMER_SWITCH_1 = -1

    def __init__(self, name, pos_x, pos_y, style, _type=TYPE_PUSH, state=STATE_OFF):
        self.name   = name
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.style  = style
        self.type   = _type
        self.state  = state
        self.timer  = 0

    def get_offset(self):
        return (self.pos_x, self.pos_y)

    def get_rect(self):
        return (self.pos_x, self.pos_y, BTN1_WIDTH, BTN1_HEIGHT)

    def default_timer(self):
        if self.type == self.TYPE_PUSH:     self.timer = self.TIMER_PUSH
        if self.type == self.TYPE_TOGGLE:   self.timer = self.TIMER_TOGGLE
        if self.type == self.TYPE_HOLD:     self.timer = self.TIMER_HOLD
        if self.type == self.TYPE_SWITCH_1: self.timer = self.TIMER_SWITCH_1

    def set_state(self, state):
        self.state = state
        self.default_timer()

    def update_state(self):
        if self.type == self.TYPE_PUSH:
            self.state = self.STATE_PUSHED
        if self.type == self.TYPE_TOGGLE:
            self.state = (self.state + 1) % 2
        if self.type == self.TYPE_HOLD:
            self.state = self.STATE_ON
        if self.type == self.TYPE_SWITCH_1:
            self.state = (self.state + 1) % 2
        self.default_timer()

    def reset_state(self):
        self.state = self.STATE_OFF
        self.timer = 0

    def activated(self):
        if self.state == self.STATE_ON: return True
        else: return False

    def tick(self):
        if self.timer > 0:
            self.timer -= 1
        if self.timer == 0:
            self.state = self.STATE_OFF


# class Coriolis
class Coriolis:
    layout = pygame.image.load(IMAGE_CORIOLIS_LAYOUT)
    padnum = pygame.image.load(IMAGE_CORIOLIS_PADNUM)
    width  = layout.get_width()
    height = layout.get_height()
    scale  = 1

    @staticmethod
    def init():
        s_width = MFD.sd(MFD_RP_WIDTH)
        orig_width = Coriolis.layout.get_width()
        if orig_width > s_width:
            s_height = int(s_width * Coriolis.height / Coriolis.width)
            Coriolis.layout = pygame.transform.smoothscale(Coriolis.layout, (s_width, s_height))
            Coriolis.padnum = pygame.transform.smoothscale(Coriolis.padnum, (s_width, s_height))
            Coriolis.width = s_width
            Coriolis.height = s_height
            Coriolis.scale = s_width / orig_width


# class Panel
class Panel(object):
    MAX_ROWS  = 40

    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.width  = width
        self.height = height
        self.lines  = [ ( "text", "" ) ] * self.MAX_ROWS

    def get_offset(self):
        return (self.pos_x, self_pos_y)

    def add_text(self, text_lines):
        for text in text_lines:
            wrapped_text = wrap_text(text, MFD.font, MFD.sd(MFD_RP_WIDTH))
            for t in reversed(wrapped_text):
                self.add_lines( [ ("text", t) ] )

    def add_lines(self, lines):
        if len(lines) > self.MAX_ROWS: lines = lines[:self.MAX_ROWS]
        self.lines = lines + self.lines[:(self.MAX_ROWS - len(lines))]

    def shift_lines(self, num_lines, _type):
        if num_lines > self.MAX_ROWS: num_lines = self.MAX_ROWS
        self.lines = [ ( _type, "" ) ] * num_lines + self.lines[:(self.MAX_ROWS - num_lines)]

    def add_image(self, imagefile):
        img = pygame.image.load(imagefile)
        s_height = img.get_height()
        s_width = self.width - 16
        if img.get_width() > s_width:
            s_height = int(s_width * img.get_height() / img.get_width())
            img = pygame.transform.smoothscale(img, (s_width, s_height))
        num_rows = int((s_height + FONT_SIZE - 1) / FONT_SIZE)
        self.shift_lines(num_rows, "empty")
        self.lines = [ ( "image", img ) ] + self.lines[:(self.MAX_ROWS - 1)]

    def add_coriolis(self, pad):
        num_rows = int((Coriolis.height + FONT_SIZE - 1) / FONT_SIZE)
        self.shift_lines(num_rows, "empty")
        self.lines = [ ( "coriolis", pad ) ] + self.lines[:(self.MAX_ROWS - 1)]

    def render_panel(self, surface):
        for row, (_type, _content) in enumerate(self.lines):
            if _type == "text":
                # _content = text
                label = MFD.font.render(_content, True, COLOR_ORANGE)
                surface.blit(label, (self.pos_x + 3, self.pos_y + row * FONT_SIZE))
            if _type == "image":
                # _content = pygame surface
                x_offset = int((self.width - _content.get_width()) / 2)
                num_rows = int((_content.get_height() + FONT_SIZE - 1) / FONT_SIZE)
                y_offset = int((num_rows * FONT_SIZE - _content.get_height()) / 2)
                surface.blit(_content, (self.pos_x + x_offset, self.pos_y + row * FONT_SIZE + y_offset))
            if _type == "coriolis":
                # _content = pad number
                x_offset = int((self.width - Coriolis.width) / 2)
                num_rows = int((Coriolis.height + FONT_SIZE - 1) / FONT_SIZE)
                y_offset = int((num_rows * FONT_SIZE - Coriolis.height) / 2)
                position = self.pos_x + x_offset, self.pos_y + row * FONT_SIZE + y_offset
                surface.blit(Coriolis.layout, position)
                if _content == 0:
                    surface.blit(Coriolis.padnum, position)
                if _content > 0:
                    num_pos = CORIOLIS_POS[_content - 1]
                    x = int(num_pos[0] * Coriolis.scale)
                    y = int(num_pos[1] * Coriolis.scale)
                    w = int((num_pos[2] - num_pos[0]) * Coriolis.scale)
                    h = int((num_pos[3] - num_pos[1]) * Coriolis.scale)
                    surface.blit(Coriolis.padnum, (position[0] + x, position[1] + y), (x, y, w, h))

