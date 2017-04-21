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
Manages the result bar : this bar that tells to the user which result
he must solve.
"""


class ResultBar(object):

    """
    A bar which tells to the player which result he must solve by hitting
    matching balls.
    """

    def __init__(self, txt_font, txt_color, bg_color, header, width,
                 lftp_edge=(0, 0)):
        """
        Constructor:
        Height will be computed internally thanks to the header value and the
        given font.
        txt_font : text font => olpcgames.pangofont
        txt_color : text color => Tuple of 3 integers in [0,255]
        bg_color : background color => Tuple of 3 integers in [0,255]
        header : text start, such as 'Hit balls with result : ' => string
        width : width of the bar => integer
        lftp_edge : coordinates of the left-top edge => tuple of 2 integers.
        """
        self._INSETS = 4
        self._txt_font = txt_font
        self._txt_color = txt_color
        self._bg_color = bg_color
        self._header = header
        self._width = width
        self._lftp_edge = lftp_edge
        self._height = txt_font.size(header)[1] + 2 * self._INSETS

    def get_insets(self):
        """
        Accessor to the component insets.
        => integer
        """
        return self._INSETS

    def get_text_font(self):
        """
        Accesssor to the text font.
        => olpcgames.pangofont
        """
        return self._txt_font

    def get_foreground(self):
        """
        Accessor to the text color.
        => Tuple of 3 integers in [0,255].
        """
        return self._txt_color

    def get_background(self):
        """
        Accessor to the bar background color.
        => Tuple of 3 integers in [0,255].
        """
        return self._bg_color

    def get_header(self):
        """
        Accessor to the header (text start, such as 'Hit balls with result : ')
        => string
        """
        return self._header

    def get_width(self):
        """
        Accessor to the width.
        => integer
        """
        return self._width

    def get_height(self):
        """
        Accesssor to the height.
        => integer
        """
        return self._height

    def get_edge(self):
        """
        Accessor to the coordinates of the left-top edge.
        => Tuple of 2 integers.
        """
        return self._lftp_edge

    def get_result(self):
        """
        Accessor to the result.
        Careful ! This might throw an NameError, as result may not be defined
        yet.
        => integer
        """
        try:
            return self._result
        except AttributeError:
            raise NameError

    def set_result(self, result):
        """
        Sets the result of the bar.
        result : the result to solve => integer
        """
        self._result = result

    def remove_result(self):
        """
        Delete the result value.
        """
        try:
            del self._result
        except AttributeError:
            pass
