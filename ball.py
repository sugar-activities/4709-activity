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

from math import sqrt


class Ball(object):

    """
    An abstractation of a ball. Its size is automatically adjusted with
    its given operation text.
    """

    def __init__(self, txt_font, txt_color, bg_color, operation,
                 move_area, velocity=(0, 0)):
        """
        Constructor
        txt_font : text font => olpcgames.pangofont
        txt_color : text color => Tuple of 3 integers in [0,255]
        bg_color : background color => Tuple of 3 integers in [0,255]
        operation : operation => An Operation value
        move_area : space where ball is allowed to be => Tuple of 4 integers (
        left side x, top side y, right side x, bottom side y)
        velocity : current direction of move (so a (0,0) velocity for a fixed
                   ball) => A tuple of 2 floats (x,y)
        """
        self._txt_font = txt_font
        self._txt_color = txt_color
        self._bg_color = bg_color
        self._operation = operation
        self._center = (0, 0)
        self._velocity = velocity
        self._move_area = move_area
        self._visible = True
        txt_size = txt_font.size(operation.get_text())
        if txt_size[0] > txt_size[1]:
            max_txt_size = txt_size[0]
        else:
            max_txt_size = txt_size[1]
        self._diameter = int(max_txt_size * 1.25)

    def get_txt_font(self):
        """
        Accessor to the text font
        => olpcgames.pangofont
        """
        return self._txt_font

    def get_diameter(self):
        """
        Accessor to the diameter.
        => Int value
        """
        return self._diameter

    def get_bg_color(self):
        """
        Accessor to the background color.
        => Tuple of 3 integers
        """
        return self._bg_color

    def get_txt_color(self):
        """
        Accessor to the text (foreground) color.
        => Tuple of 3 integers
        """
        return self._txt_color

    def get_operation(self):
        """
        Accessor to the operation.
        => Operation instance.
        """
        return self._operation

    def get_center(self):
        """
        Accessor to the center position.
        => Tuple of 2 integers.
        """
        return tuple([int(x) for x in self._center])

    def move_to(self, new_center_position):
        """
        Moves the ball to a particular place.
        new_center_position : the new center position => a tuple of 2 integers
        """
        if (new_center_position[0] - self._diameter < self._move_area[0]
           or new_center_position[0] + self._diameter > self._move_area[2]
           or new_center_position[1] - self._diameter < self._move_area[1]
           or new_center_position[1] + self._diameter > self._move_area[3]):
            self._center = (self._move_area[0] + self._diameter,
                            self._move_area[1] + self._diameter)
        else:
            self._center = new_center_position

    def move(self):
        """
        Moves the ball by its current velocity.
        Please notice that this velocity will change whenever the ball hits
        a wall (a screen side).
        """
        expected_new_center = (self._center[0] + self._velocity[0],
                               self._center[1] + self._velocity[1])
        self._center = expected_new_center
        radius = self._diameter / 2
        # Ball must not go across left or right wall.
        if (self._center[0] < self._move_area[0] + radius
           or self._center[0] > self._move_area[2] - radius):
            self._velocity = (-self._velocity[0], self._velocity[1])
            self._center = (self._center[0] + self._velocity[0],
                            self._center[1] + self._velocity[1])
        # Ball must not go across top or bottom wall.
        elif (self._center[1] < self._move_area[1] + radius
              or self._center[1] > self._move_area[3] - radius):
            self._velocity = (self._velocity[0], -self._velocity[1])
            self._center = (self._center[0] + self._velocity[0],
                            self._center[1] + self._velocity[1])

    def oppose_velocity_and_move(self):
        """
        Alters the velocity, by multiplying each of its values
        by -1, then move it from one step (calling move).
        """
        self._velocity = (self._velocity[0] * -1,
                          self._velocity[1] * -1)

    def contains(self, point):
        """
        Tells whether the given point is inside the ball.
        point : the point to test => tuple of 2 integers
        => Boolean
        """
        vector_to_center = (point[0] - self._center[0],
                            point[1] - self._center[1])
        dist_to_center = sqrt(vector_to_center[0] * vector_to_center[0]
                              + vector_to_center[1] * vector_to_center[1])
        return dist_to_center <= self._diameter / 2

    def is_visible(self):
        """
        Tells whether this ball is visible.
        => Boolean
        """
        return self._visible

    def show(self):
        """
        Makes the ball visible.
        """
        self._visible = True

    def hide(self):
        """
        Makes the ball hidden.
        """
        self._visible = False
