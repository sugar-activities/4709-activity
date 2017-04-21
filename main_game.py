# -*- coding: utf-8 -*-

"""
HitTheBalls : hit the ball(s) with the good result.
Copyright (C) 2013  Laurent Bernabe <laurent.bernabe@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Manages the main game.
"""

from gettext import gettext as _
from gi.repository import Gtk
import pygame
from random import randint
from sys import exit
from pygame.locals import QUIT, USEREVENT, MOUSEBUTTONUP
from elements_painter import paint_ball, paint_time_bar, paint_result_bar,\
    paint_results
from time_bar import TimeBar
from result_bar import ResultBar
from game_state import GameState
from balls_generator import BallsGenerator
import balls_collision
from operation import OPER_ADD, OPER_SUB, OPER_MUL, OPER_DIV
from balls_generator import OperationConfig


class Game:

    """
    Manages the game.
    """

    def __init__(self):
        """
        Constructor.
        """
        self._initialized = False

    def _lazy_init(self):
        """
        Lazy initialization : main code is only called once, thanks to
        an internal flag.
        """
        if self._initialized:
            return
        pygame.init()
        self._LEFT_BUTTON = 1
        self._FPS = 40
        self._MENU_LEVELS_RECTS_Y_GAP = 30
        self._MENU_LEVELS_RECTS_WIDTH = 345
        self._MENU_LEVELS_RECTS_HEIGHT = 60
        self._MENU_LEVELS_RECTS_TXT_OFFSET = (60, -2)
        self._MENU_LEVELS_RECTS_BG_COLOR = (255, 0, 0)
        self._MENU_LEVELS_RECTS_TXT_COLOR = (255, 255, 0)
        self._MENU_BACKGROUND = (255, 255, 255)
        self._GAME_BACKGROUND = (255, 255, 255)
        self._TIME_BAR_HEIGHT = 20
        self._BLACK = (0, 0, 0)
        self._BLUE = (0, 0, 255)
        self._YELLOW = (255, 255, 0)
        self._RED = (255, 0, 0)
        self._DARK_GREEN = (0, 100, 0)
        self._GRAY = (200, 200, 200)

        self._screen = pygame.display.get_surface()
        if not(self._screen):
            self._size = (600, 400)
            self._screen = pygame.display.set_mode(self._size)
            pygame.display.set_caption("Hit the balls")
        else:
            self._size = self._screen.get_size()

        self._game_font = pygame.font.Font(None, 34)
        self._menu_font = pygame.font.Font(None, 90)
        self._end_font = pygame.font.Font(None, 40)
        self._END_TXT_POS = (int(self._size[0] / 8)), int(self._size[1] / 2.6)

        self._clock = pygame.time.Clock()
        self._levels = [
            # level 1
            [OperationConfig(OPER_ADD, 9, 9),
             OperationConfig(OPER_MUL, 9, 9),
             OperationConfig(OPER_SUB, 18, 9),
             OperationConfig(OPER_DIV, 81, 9, 9)],
            # level 2
            [OperationConfig(OPER_ADD, 99, 99, 100),
             OperationConfig(OPER_MUL, 99, 9),
             OperationConfig(OPER_SUB, 100, 98),
             OperationConfig(OPER_DIV, 891, 9, 99)],
            # level 3
            [OperationConfig(OPER_ADD, 999, 999, 1000),
             OperationConfig(OPER_MUL, 99, 99, 1000),
             OperationConfig(OPER_SUB, 1000, 998),
             OperationConfig(OPER_DIV, 1000, 99)]
        ]
        self._MENU_LEVELS_RECT_X = (self._size[0] -
                                    self._MENU_LEVELS_RECTS_WIDTH) / 2
        self._MENU_LEVEL_1_RECT_Y = (self._size[1] -
                                     (self._MENU_LEVELS_RECTS_HEIGHT +
                                      self._MENU_LEVELS_RECTS_Y_GAP) *
                                     len(self._levels) +
                                     self._MENU_LEVELS_RECTS_Y_GAP) / 2

        self._levels_rect = [(self._MENU_LEVELS_RECT_X,
                              self._MENU_LEVEL_1_RECT_Y +
                              y * (self._MENU_LEVELS_RECTS_HEIGHT +
                                   self._MENU_LEVELS_RECTS_Y_GAP),
                              self._MENU_LEVELS_RECTS_WIDTH,
                              self._MENU_LEVELS_RECTS_HEIGHT)
                             for y in range(len(self._levels))]
        self._initialized = True

    def _get_result_at_pos(self, point, balls_list):
        """
        Returns the result of the ball located at point (from the balls_list)
        and its index in the balls_list,
        if any, else returns None.
        point : point to test => tuple of 2 integers
        balls_list : list of balls to test => list of Ball
        => dictionnary with "result" key => value : integer
                             "index" key => value : integer
        """
        for ball_index in range(len(balls_list)):
            ball = balls_list[ball_index]
            if ball.contains(point):
                return {"result": ball.get_operation().get_result(),
                        "index": ball_index}
        return None

    def _all_target_balls_destroyed(self, target_result, balls_list):
        """
        Says whether all target ball, those with the expected result, have been
        removed from the given list.
        target_result : expected result => integer
        balls_list : list of balls => list of Ball
        => Boolean
        """
        for ball in balls_list:
            if ball.is_visible() \
                    and ball.get_operation().get_result() == target_result:
                return False
        return True

    def _point_in_rect(self, point, rect):
        """
        Says whether a point is in a rect.
        point : the point to test => tuple of 2 integers (x,y)
        rect : the rect to test => tuple of 4 integers (x,y, width, height)
        => Boolean
        """
        x_good = point[0] >= rect[0] and point[0] <= rect[0] + rect[2]
        y_good = point[1] >= rect[1] and point[1] <= rect[1] + rect[3]
        return x_good and y_good

    def _play_game(self, time_seconds, operations_config):
        """ The main game routine
            time_seconds : time limit in seconds => integer
            operations_config : configurations for the wanted operations
            => list of
            OperationConfig.
        """
        # Shows loading screen
        self._screen.fill(self._MENU_BACKGROUND)
        loading_txt = _("Loading...")
        loading_txt_surface = self._end_font.render(
            loading_txt,
            True,
            self._BLUE
        )
        txt_size = self._end_font.size(loading_txt)
        self._screen.blit(loading_txt_surface, (
            (self._size[0] - txt_size[0]) / 2,
            (self._size[1] - txt_size[1]) / 2,
        ))
        pygame.display.update()

        game_state = GameState.NORMAL

        result_bar = ResultBar(self._game_font, txt_color=self._YELLOW,
                               bg_color=self._RED,
                               header=_("Hit the ball (or the balls) with result : "),
                               width=self._size[0])
        RESULT_BAR_HEIGHT = result_bar.get_height()

        time_bar = TimeBar(self._size[0], self._TIME_BAR_HEIGHT,
                           self._DARK_GREEN,
                           self._GRAY, lftp_edge=(0, RESULT_BAR_HEIGHT))
        # Don't forget that it will take time argument * 10 milliseconds
        time_bar.start(time_seconds * 100, 1)

        balls_area = (0, self._TIME_BAR_HEIGHT + RESULT_BAR_HEIGHT,
                      self._size[0], self._size[1])

        the_balls = BallsGenerator().generate_list(5, operations_config,
                                                   balls_area, self._game_font,
                                                   self._BLACK)

        result_index = randint(1, len(the_balls)) - 1
        target_result = the_balls[result_index].get_operation().get_result()
        result_bar.set_result(target_result)

        balls_collision.place_balls(the_balls, balls_area)

        show_status = True
        pygame.time.set_timer(USEREVENT + 2, 1000)

        while True:
            pygame.display.update()
            self._screen.fill(self._GAME_BACKGROUND)
            paint_result_bar(result_bar, self._screen)
            paint_time_bar(time_bar, self._screen)
            if game_state == GameState.NORMAL:
                for ball in the_balls:
                    paint_ball(ball, self._screen)

                while Gtk.events_pending():
                    Gtk.main_iteration()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == USEREVENT + 1:
                        time_bar.decrease()
                        if time_bar.is_empty():
                            game_state = GameState.LOST
                    elif event.type == MOUSEBUTTONUP:
                        if event.button == self._LEFT_BUTTON:
                            event_pos = event.pos
                            clicked_ball = self.\
                                _get_result_at_pos(event_pos, the_balls)
                            if clicked_ball is not None:
                                if clicked_ball["result"] == target_result:
                                    the_balls[clicked_ball["index"]].hide()
                                    if self.\
                                        _all_target_balls_destroyed(
                                            target_result, the_balls):
                                        game_state = GameState.WON
                                else:
                                    game_state = GameState.LOST
                self._clock.tick(self._FPS)
                for ball in the_balls:
                    ball.move()
                balls_collision.manage_colliding_balls(the_balls)
            else:
                paint_results(balls_area, the_balls, self._screen)
                # Blinks the status text.
                if show_status:
                    if game_state == GameState.WON:
                        end_txt = _("Success ! Click when you finished.")
                    else:
                        end_txt = _("Failure ! Click when you finished.")
                    end_txt_surface = self._end_font.render(end_txt, True,
                                                            self._BLUE,
                                                            self._RED)
                    self._screen.blit(end_txt_surface, self._END_TXT_POS)

                while Gtk.events_pending():
                    Gtk.main_iteration()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == USEREVENT + 2:
                        show_status = not show_status
                    elif event.type == MOUSEBUTTONUP:
                        if event.button == self._LEFT_BUTTON:
                            return

    def show_menu(self):
        """
        Manages the main menu.
        """
        self._lazy_init()
        while True:
            self._screen.fill(self._MENU_BACKGROUND)
            for box_index in range(len(self._levels)):
                box_value = self._levels_rect[box_index]
                pygame.draw.rect(
                    self._screen, self._MENU_LEVELS_RECTS_BG_COLOR,
                    box_value)
                txt = _("Level ") + str(box_index + 1)
                txt_surface = self._menu_font.render(txt, True,
                                                     self._MENU_LEVELS_RECTS_TXT_COLOR)
                self._screen.blit(txt_surface,
                                  (self._levels_rect[box_index][0] +
                                   self._MENU_LEVELS_RECTS_TXT_OFFSET[0],
                                   self._levels_rect[box_index][1] +
                                   self._MENU_LEVELS_RECTS_TXT_OFFSET[1]
                                   ))
            pygame.display.update()
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONUP:
                    if event.button == self._LEFT_BUTTON:
                        selected_level_index = -1
                        for level_index in range(len(self._levels)):
                            if self._point_in_rect(event.pos,
                                                   self._levels_rect[level_index]):
                                selected_level_index = level_index
                                break
                        if selected_level_index >= 0:
                            self._play_game(
                                30,
                                self._levels[selected_level_index])
