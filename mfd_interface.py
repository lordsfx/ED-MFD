import pygame
from constants import *

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

# class Panel
class Panel(object):
    FONT_SIZE = 16
    MAX_COLS  = 30
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
            self.add_lines( [ ("text", text) ] )

    def add_lines(self, lines):
        if len(lines) > self.MAX_ROWS: lines = lines[:self.MAX_ROWS]
        self.lines = lines + self.lines[:(self.MAX_ROWS - len(lines))]

    def shift_lines(self, num_lines, _type):
        if num_lines > self.MAX_ROWS: num_lines = self.MAX_ROWS
        self.lines = [ ( _type, "" ) ] * num_lines + self.lines[:(self.MAX_ROWS - num_lines)]

    def add_image(self, imagename):
        img = pygame.image.load(imagename)
        if img.get_width() > 300:
            s_height = int(300 * img.get_height() / img.get_width())
            img = pygame.transform.smoothscale(img, (300, s_height))
        num_rows = int((s_height + self.FONT_SIZE - 1) / self.FONT_SIZE)
        self.shift_lines(num_rows, "empty")
        self.lines = [ ( "image", img ) ] + self.lines[:(self.MAX_ROWS - 1)]

    def render_panel(self, surface, font):
        for row, (_type, _content) in enumerate(self.lines):
            if _type == "text":
                label = font.render(_content, True, COLOR_ORANGE)
                surface.blit(label, (self.pos_x, self.pos_y + row * self.FONT_SIZE))
            if _type == "image":
                surface.blit(_content, (self.pos_x, self.pos_y + row * self.FONT_SIZE))

