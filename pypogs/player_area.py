import pygame
from pygame.locals import *

from pypogs import grid
from pypogs import render
from pypogs import piece
from pypogs import events

# Rendering constants
OUTER_COLOR_OFFSET = 10

COLORS = {
    1: (0, 0, 255),
    2: (0, 255, 0),
    3: (255, 0, 0),
    4: (255, 255, 0),
    5: (0, 255, 255),
    6: (128, 255, 0),
    8: (128, 128, 128),
    7: (0, 255, 128),
    11: (0, 0, 128),
    12: (0, 128, 0),
    13: (128, 0, 0),
    14: (128, 128, 0),
    15: (0, 128, 128),
    16: (64, 128, 0),
    17: (0, 128, 64),
    18: (64, 64, 64)
    }

class PlayerArea(grid.Grid):

    def __init__(self, positions, player_id = 0):
        grid.Grid.__init__(self, player_id)
        self._positions = positions

    def render(self, surface):
        """Renders the player area onto the given screen."""
        grid_x = self._positions.grid_x(self._player_id)
        grid_y = self._positions.grid_y(self._player_id)

        next_x = self._positions.next_piece_x(self._player_id)
        next_y = self._positions.next_piece_y(self._player_id)

        lines_x = self._positions.lines_box_x(self._player_id)
        lines_y = self._positions.lines_box_y(self._player_id)
        level_x = self._positions.level_box_x(self._player_id)
        level_y = self._positions.level_box_y(self._player_id)
        score_x = self._positions.score_box_x(self._player_id)
        score_y = self._positions.score_box_y(self._player_id)
        text_box_width = self._positions.text_box_width
        text_box_height = self._positions.text_box_height

        font = self._positions.text_box_font

        box_thickness = self._positions.grid_thickness

        inner_frame_color = (0, 0, 0)
        outer_frame_color = (0, 64, 128)
        font_color = (255, 255, 255)


        self._render_frame(surface, lines_x, lines_y,
                           text_box_width, text_box_height, box_thickness,
                           inner_frame_color, outer_frame_color)

        render.render_text_centered(surface, font, lines_x, lines_y,
                                   text_box_width, text_box_height,
                                   str(self._lines_cleared),
                                   font_color)

        self._render_frame(surface, level_x, level_y,
                           text_box_width, text_box_height, box_thickness,
                           inner_frame_color, outer_frame_color)

        render.render_text_centered(surface, font, level_x, level_y,
                                   text_box_width, text_box_height,
                                   str(self._level),
                                   font_color)

        self._render_frame(surface, score_x, score_y,
                           text_box_width, text_box_height, box_thickness,
                           inner_frame_color, outer_frame_color)

        render.render_text_centered(surface, font, score_x, score_y,
                                   text_box_width, text_box_height,
                                   str(self._score),
                                   font_color)

        self._render_frame(surface, next_x, next_y,
                           self._positions.next_piece_width,
                           self._positions.next_piece_height,
                           box_thickness,
                           inner_frame_color, outer_frame_color)

        self._render_frame(surface, grid_x, grid_y,
                           self._positions.grid_width,
                           self._positions.grid_height,
                           box_thickness,
                           inner_frame_color, outer_frame_color)

        self._render_next_piece(surface, next_x, next_y)
        self._render_grid(surface, grid_x, grid_y)



    def _render_next_piece(self, surface, x, y):
        block_size = self._positions.block_size
        block_edge_thickness = self._positions.block_edge_thickness

        # Render the next piece in the middle of the box, which is half a block
        # away from the edge of the box.
        actual_x = x + (block_size / 2)
        actual_y = y + (block_size / 2)

        for row in range(piece.Piece.ROWS):
            for col in range(piece.Piece.COLUMNS):
                block_value = self._next_piece.value_at(row, col)
                if block_value > 0:
                    self._render_block(actual_x, actual_y, row, col, block_size,
                                       block_edge_thickness, block_value,
                                       surface)

    def _render_grid(self, surface, x, y):
        block_size = self._positions.block_size
        block_edge_thickness = self._positions.block_edge_thickness

        for row in range(grid.GRID_ROWS):
            for col in range(grid.GRID_COLUMNS):
                block_value = self.value_at(row, col)
                if block_value > 0:
                    self._render_block(x, y, row, col, block_size,
                                       block_edge_thickness, block_value,
                                       surface)

    def _render_frame(self, surface, x, y, width, height, frame_thickness,
                      inner_color, outer_color):
        outer_rect = pygame.Rect(x - frame_thickness, y - frame_thickness,
                                 width + (2 * frame_thickness),
                                 height + (2 * frame_thickness))
        inner_rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(surface, outer_color, outer_rect)
        pygame.draw.rect(surface, inner_color, inner_rect)

    def _render_block(self, grid_x, grid_y, row, col, size,
                      edge_thickness, value, surface):

        left = grid_x + (col * size)
        top = grid_y + (row * size)

        inner_size = size - (2 * edge_thickness)

        outer_rect = pygame.Rect(left, top, size, size)
        inner_rect = pygame.Rect(left + edge_thickness,
                                 top + edge_thickness,
                                 inner_size, inner_size)

        outer_color = self._value_to_color(value + OUTER_COLOR_OFFSET,
                                           self._counter_to_clear_blocks)
        inner_color = self._value_to_color(value, self._counter_to_clear_blocks)

        pygame.draw.rect(surface, outer_color, outer_rect)
        pygame.draw.rect(surface, inner_color, inner_rect)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            self._handle_key_event(event.key)
        elif event.type == JOYBUTTONDOWN:
            self._handle_joy_button_event(event.joy, event.button)
        elif event.type == JOYAXISMOTION:
            self._handle_joy_axis_event(event.joy, event.axis, event.value)

    def _handle_joy_button_event(self, id, button):
        if id != self._player_id:
            return

        if button == events.JOY_ROTATE_BUTTON:
            self._rotate_current_piece_clockwise()

    def _handle_joy_axis_event(self, id, axis, value):
        if value < 0.1 and value > -0.1:
            return

        if id != self._player_id:
            return

        if axis == events.JOY_X_AXIS:
            if value > 0:
                self._move_current_piece_right()
            else:
                self._move_current_piece_left()
        elif axis == events.JOY_Y_AXIS:
            if value > 0:
                self._drop_current_piece_one_row()
            else:
                self._drop_current_piece_to_floor()

    def _handle_key_event(self, key):
        if key == K_LEFT:
            self._move_current_piece_left()
        elif key == K_RIGHT:
            self._move_current_piece_right()
        elif key == K_DOWN:
            self._drop_current_piece_one_row()
        elif key == K_UP:
            self._drop_current_piece_to_floor()
        elif key == K_SPACE:
            self._rotate_current_piece_clockwise()

    def _value_to_color(self, value, dimmer = 0):
        color = COLORS.get(value, (0, 0, 0))
        # Fix this hack.
        if dimmer > 0 and (value == grid.BLOCK_TO_BE_CLEARED or
                           value == grid.BLOCK_TO_BE_CLEARED + 10):
            pct_dimmed = float(dimmer) / float(grid.TICKS_TO_CLEAR_BLOCKS)
            color = (color[0] * pct_dimmed,
                     color[1] * pct_dimmed,
                     color[2] * pct_dimmed)

        return color
