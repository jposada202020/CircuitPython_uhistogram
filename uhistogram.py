# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""

`uhistogram`
================================================================================

CircuitPython library to calculate and graph histograms


* Author(s): Jose D. Montoya

Implementation Notes
--------------------

Depends on CircuitPyton version 8.0.0


"""

try:
    from typing import Union, Tuple
except ImportError:
    pass

from ulab import numpy as np
from bitmaptools import draw_line
import displayio

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/jposada202020/CircuitPython_uhistogram.git"


class Histogram(displayio.TileGrid):
    """A Histogram TileGrid. The origin is set using ``x`` and ``y``.

    :param (list, tuple) data: source data to calculate the histogram
    :param int x: x position of the histogram origin
    :param int y: y position of the histogram origin

    :param int width: requested width, in pixels. Defaults to 100 pixels.
    :param int height: requested height, in pixels. Defaults to 100 pixels.

    :param int line_color: background color to use defaults to white (0xFFFFFF)

    **Quickstart: Importing and using uhistogram**

    Here is one way of importing the `uhistogram.Histogram` class so you can use it as
    the name ``uhistogram.Histogram``:

    .. code-block:: python

        from uhistogram import Histogram
        import displayio

    Now you can create a boxplot at pixel position x=50, y=50 using:

    .. code-block:: python

        a=[1, 1, 4, 5, 6, 7, 7, 7, 8, 9, 10, 15, 16, 17, 24, 56, 76, 87, 87]
        my_histogram=Histogram(a, x=50, y=50) # instance the histogram at x=50, y=50
        my_group = displayio.Group()

    Once you set up your display, you can now add ``my_boxplot`` to your display.Group() using:

    .. code-block:: python

        my_group.append(my_histogram)
        display.show(my_group) # add the group to the display


    **Summary: Histogram Features and input variables**

    The `uhistogram` TileGrid has some options for controlling its position, visible appearance,
    through a collection of input variables:

        - **position**: ``x``, ``y``

        - **size**: ``width`` and ``height``

        - **color**: ``line_color``


    .. figure:: histogram.png
       :scale: 100 %
       :figwidth: 50%
       :align: center
       :alt: Diagram of the histogram TileGrid with the pointer in motion.

       This is a diagram of a histogram


    """

    def __init__(
        self,
        data: Union[list, Tuple],
        x: int,
        y: int,
        height: int = 100,
        width: int = 100,
        line_color: int = 0xFFFFFF,
    ) -> None:
        self._data_raw = data
        self.data = np.array(data)
        self._width = width

        self._color_palette = displayio.Palette(4)
        self._color_palette[2] = line_color
        self._color_palette[3] = 0x0000FF
        self._bitmap = displayio.Bitmap(width + 1, height + 1, 3)

        self._yorigin = height
        self._xstart = 0

        self.bin_data = self.get_numberbins(data, rule=0)

        self._numbins = len(self.bin_data)
        self._binmaxqty = int(np.max(self.bin_data))
        self._graphx = self._width // self._numbins
        self._graphy = height // self._binmaxqty

        maximum = self._binmaxqty
        self._new_min = int(self.normalize(0, maximum, maximum, 0, 0))
        self._new_max = int(self.normalize(0, maximum, maximum, 0, maximum))

        super().__init__(self._bitmap, pixel_shader=self._color_palette, x=x, y=y)

    @staticmethod
    def normalize(oldrangemin, oldrangemax, newrangemin, newrangemax, value):
        """
        This function converts the original value into a new defined value in the new range

        :param oldrangemin: minimum of the original range
        :param oldrangemax: maximum of the original range
        :param newrangemin: minimum of the new range
        :param newrangemax: maximum of the new range
        :param value: value to be converted
        :return: converted value

        """
        return (
            ((value - oldrangemin) * (newrangemax - newrangemin))
            / (oldrangemax - oldrangemin)
        ) + newrangemin

    def print_data(self):
        """
        This function prints the bins data

        :return: None
        """

        distribution = {
            i: self._data_raw.count(i) / len(self._data_raw)
            for i in set(self._data_raw)
        }
        distribution2 = {i: self._data_raw.count(i) for i in set(self._data_raw)}

        print("Distribution in % of your data")
        print(distribution)
        print("-" * 40)
        print("Frequency")
        print(distribution2)
        print("-" * 40)
        print("Recommended bins number for your data")
        print(len(self.bin_data))
        print("-" * 40)
        print("Bins distribution")
        print(self.bin_data)

    def draw(self):
        """
        This function draws the histogram

        """

        for i in range(self._numbins):
            self._draw_rectangle(
                self._xstart + (i * self._graphx),
                self._yorigin,
                self._graphx,
                self._graphy * int(self.bin_data[i]),
                3,
            )

    def _draw_rectangle(self, x, y, width, height, color):
        """
        Helper function to draw bins rectangles
        """
        draw_line(self._bitmap, x, y, x + width, y, color)
        draw_line(self._bitmap, x, y, x, y - height, color)
        draw_line(self._bitmap, x + width, y, x + width, y - height, color)
        draw_line(self._bitmap, x + width, y - height, x, y - height, color)

    @staticmethod
    def get_numberbins(data, rule=0):
        """
        Function that calculate the number of bins for the sample. you could use two rules, changing
        the parameter rule.
        rule = 0 applies Sturge's rule
        rule = 1 applies square root choice
        rule = 2 will choose the best criteria to be applied.
        for data size < 30 --> Square Root Choice
        for data size > 30 --> Sturg's Rule

        :param data: data to be analyzed
        :param rule: desired rule. Defaults to 0.
        :return: bin calculated data

        """
        if rule == 2:  # Normal’s rule
            if len(data) > 30:
                rule = 0
            else:
                rule = 1
        if rule == 0:  # Sturge’s rule
            bin_count = int(np.ceil(np.log2(len(data))) + 1)
        if rule == 1:  # Square Root Choice’s rule
            bin_count = int(
                np.ceil(abs(np.max(data) - np.min(data)) / np.sqrt(len(data)))
            )

        start = min(data)
        distance = int(np.ceil(abs(max(data) - min(data)) / bin_count))
        end = min(data) + distance
        bins = np.zeros(bin_count)
        for i in range(bin_count):
            for item in data:
                if start <= item < end:
                    bins[i] = bins[i] + 1
            start = end
            end = end + distance
        return bins
