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
Manages balls collisions
"""

from math import sqrt
from random import randint


def are_colliding_balls(ball_1, ball_2):
    """
    Says whether two balls collides.
    ball_1 : ball to test => Ball
    ball_2 : ball to test => Ball
    => Boolean
    """
    b1_x, b1_y = ball_1.get_center()
    b2_x, b2_y = ball_2.get_center()
    x_dist = abs(b1_x - b2_x)
    y_dist = abs(b1_y - b2_y)
    b1_radius = ball_1.get_diameter() / 2
    b2_radius = ball_2.get_diameter() / 2
    centers_dist = sqrt(x_dist ** 2 + y_dist ** 2)
    return centers_dist <= (b1_radius + b2_radius)


def manage_colliding_balls(balls_list):
    """
    Detects all colliding balls couples of balls_list,
    and, for each colliding balls couple, alter both ball
    velocity and make a move for both.
    balls_list : list of balls => List of Ball
    """
    for fst_ball_index in range(len(balls_list[:-1])):
        fst_ball = balls_list[fst_ball_index]
        inner_range = range(fst_ball_index + 1, len(balls_list))
        for snd_ball_index in inner_range:
            snd_ball = balls_list[snd_ball_index]
            if (are_colliding_balls(fst_ball, snd_ball)):
                fst_ball.oppose_velocity_and_move()
                snd_ball.oppose_velocity_and_move()


def place_balls(balls_list, balls_area):
    """
    Places all the balls of balls_list, randomly, within balls_area
    but assuring that balls don't collide each other.
    balls_list : list of balls => List of Ball
    balls_area :  space where ball is allowed to be => Tuple of 4 integers (
        left side x, top side y, right side x, bottom side y)
    """
    placed_balls = []
    for ball in balls_list:
        while True:
            ball_x = randint(balls_area[0], balls_area[2] + 1)
            ball_y = randint(balls_area[1], balls_area[3] + 1)
            ball.move_to((ball_x, ball_y))
            collides = False
            for placed_ball in placed_balls:
                curr_collision_state = are_colliding_balls(ball, placed_ball)
                collides = collides or curr_collision_state
            if not collides:
                placed_balls.append(ball)
                break
