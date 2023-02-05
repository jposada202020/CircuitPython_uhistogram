# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: Unlicense
"""
Simple test to display a histogram based in some data
"""
import displayio
import board
from uhistogram import Histogram

display = board.DISPLAY

data = [5, 4, 3, 2, 7, 5, 3, 3, 3, 3, 2, 9, 7, 6]
my_box = Histogram(data, x=50, y=50, width=100, height=100)
my_box.draw()
my_box.print_data()
my_group = displayio.Group()
my_group.append(my_box)
display.show(my_group)

while True:
    pass
