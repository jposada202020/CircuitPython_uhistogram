# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: Unlicense
"""
A more advance example to illustrate how to add text to the histogram
"""

# pylint: disable=protected-access

import displayio
import board
import terminalio
from adafruit_display_text import bitmap_label
from uhistogram import Histogram

display = board.DISPLAY

data = [5, 4, 3, 2, 7, 5, 3, 3, 3, 3, 2, 9, 7, 6]
my_box = Histogram(data, x=50, y=50, width=100, height=100)
my_box.draw()
my_group = displayio.Group()
my_group.append(my_box)

for i in range(my_box._numbins):

    text_area = bitmap_label.Label(terminalio.FONT, text=str(int(my_box.bin_data[i])))
    text_area.x = (
        50 + my_box._xstart + int(i * 1 * my_box._graphx) + my_box._graphx // 2
    )
    text_area.y = 160
    my_group.append(text_area)

display.show(my_group)
while True:
    pass
