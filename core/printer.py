#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright(C) 2017-2019 :: Catayao56 <Catayao56@gmail.com>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# -*- coding: utf-8 -*-

import sys

from core import simplelib

class Printer:
    """
    Print an object to the screen using number of methods..
    """

    def __init__(self):
        """
        def __init__():
            Initialization method of Printer() class.
        """

        self.cinfo = "{2}[{0}+{2}]{1}".format(
            simplelib.SimpleLib().foreground_colors["green"],
            simplelib.SimpleLib().foreground_colors["default"],
            simplelib.SimpleLib().foreground_colors["grey"]
            )

        self.cwarn = "{2}[{0}!{2}]{1}".format(
            simplelib.SimpleLib().foreground_colors["yellow"],
            simplelib.SimpleLib().foreground_colors["default"],
            simplelib.SimpleLib().foreground_colors["grey"]
        )

        self.cerr = "{2}[{0}E{2}]{1}".format(
            simplelib.SimpleLib().foreground_colors["red"],
            simplelib.SimpleLib().foreground_colors["default"],
            simplelib.SimpleLib().foreground_colors["grey"]
        )

    def print_with_status(self, obj, status=0):
        """
        def print():
            Print <obj> with status number <status>.

            :param obj: Object to print.
            :type object:

            :param status: Status number.
            :type int:
                0 = Normal;
                1 = Warning;
                2 = Error
        """

        if status == 0:
            print(
            self.cinfo,
            simplelib.SimpleLib().foreground_colors["green"],
            obj,
            simplelib.SimpleLib().foreground_colors["default"])
            return None

        elif status == 1:
            print(
            self.cwarn,
            simplelib.SimpleLib().foreground_colors["yellow"],
            obj,
            simplelib.SimpleLib().foreground_colors["default"])
            return None

        elif status == 2:
            print(
            self.cerr,
            simplelib.SimpleLib().foreground_colors["red"],
            obj,
            simplelib.SimpleLib().foreground_colors["default"])
            return None

        else:
            raise ValueError("Unknown status mode!")

    def print_and_flush(self, obj):
        """
        def print_and_flush():
            Print <obj> and then flush.
        """

        sys.stdout.write(obj)
        sys.stdout.flush()
        return None

    def printt(self, obj="", mode=0, temp_objs=[]):
        """
        def print():
            Print <obj> in a number of ways.

            :param obj: Object to print.
            :type str:

            :param mode: How <obj> will be treated.
            :type int:
                0 = Normal print using print function.
                1 = Append <obj> to temporary list.
                2 = Reset the temporary list.
        """

        if mode == 0:
            print(obj)
            return temp_objs

        elif mode == 1:
            temp_objs.append(obj)
            return temp_objs

        elif mode == 2:
            temp_objs = []
            return temp_objs

        else:
            raise ValueError("Mode must be between 0 ~ 2!")
