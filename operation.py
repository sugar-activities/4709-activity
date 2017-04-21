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
Created on Sat Sep 14 11:02:52 2013
"""

OPER_ADD = {'txt': '+', 'operation': lambda op1, op2: op1 + op2}
OPER_SUB = {'txt': '-', 'operation': lambda op1, op2: op1 - op2}
OPER_MUL = {'txt': '*', 'operation': lambda op1, op2: op1 * op2}
OPER_DIV = {'txt': '/', 'operation': lambda op1, op2: op1 / op2}


class Operation(object):

    """
    An abstraction of an operation.
    """

    def __init__(self, op1, op2, operator):
        """
        Constructor
        op1 : numeric value => operand 1
        op2 : numeric value => operand 2
        operator : operator => One of given OPER_* values
                               (for example OPER_ADD)
        """
        self._result = operator['operation'](op1, op2)
        self._txt = str(op1) + operator['txt'] + str(op2)

    def get_result(self):
        """
        Accessor to the result field.
        => numeric value.
        """
        return self._result

    def get_text(self):
        """
        Accessor to the text field
        => string value
        """
        return self._txt
