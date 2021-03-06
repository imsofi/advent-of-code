#!/usr/bin/env python3
"""
Day 5: Hydrothermal Venture

https://adventofcode.com/2021/day/5
"""
import sys
from typing import Generator, Optional

import numpy as np

Point = tuple[int, int]
Data = np.ndarray


def coords_to_tuple(bytes_: bytes) -> tuple[int, ...]:
    # bytes given as 'latin1' from numpy.loadtxt
    return tuple(int(i) for i in bytes_.decode("latin1").split(","))

def parse_data(path: Optional[str]) -> Data:
    if not sys.stdin.isatty():
        raw = sys.stdin.readlines()
    else:
        if path:
            with open(path, encoding="utf-8") as f:
                raw = f.readlines()
        else:
            sys.exit("No stdin data was recived.")

    return np.loadtxt(
        raw,
        converters={0: coords_to_tuple, 1: coords_to_tuple},
        dtype=int,
        delimiter=" -> ",
    )


def plot_line_low(
    x_0: int, y_0: int, x_1: int, y_1: int
) -> Generator[Point, None, None]:
    d_x = x_1 - x_0
    d_y = y_1 - y_0
    y_i = 1
    if d_y < 0:
        y_i = -1
        d_y = -d_y
    D = (2 * d_y) - d_x
    y = y_0

    for x in range(x_0, x_1 + 1):
        yield (x, y)

        if D > 0:
            y = y + y_i
            D = D + (2 * (d_y - d_x))
        else:
            D = D + 2 * d_y


def plot_line_high(
    x_0: int, y_0: int, x_1: int, y_1: int
) -> Generator[Point, None, None]:
    d_x = x_1 - x_0
    d_y = y_1 - y_0
    x_i = 1
    if d_x < 0:
        x_i = -1
        d_x = -d_x
    D = (2 * d_x) - d_y
    x = x_0

    for y in range(y_0, y_1 + 1):
        yield (x, y)

        if D > 0:
            x = x + x_i
            D = D + (2 * (d_x - d_y))
        else:
            D = D + 2 * d_x


def plot_line(
    x_0: int, y_0: int, x_1: int, y_1: int
) -> Generator[Point, None, None]:
    """
    Python implementation of the Bresenham's line algorithm.

    https://en.wikipedia.org/wiki/Bresenham's_line_algorithm
    """
    if abs(y_1 - y_0) < abs(x_1 - x_0):
        if x_0 > x_1:
            x_1, y_1, x_0, y_0 = x_0, y_0, x_1, y_1
        return plot_line_low(x_0, y_0, x_1, y_1)
    if y_0 > y_1:
        x_1, y_1, x_0, y_0 = x_0, y_0, x_1, y_1
    return plot_line_high(x_0, y_0, x_1, y_1)


def intercetions(data: Data) -> np.ndarray:
    max_size = int(data.max()) + 1
    diagram = np.zeros((max_size, max_size), dtype=int)

    for ((x_0, y_0), (x_1, y_1)) in data:
        for x, y in plot_line(x_0, y_0, x_1, y_1):
            diagram[y][x] += 1

    return diagram


def part_1(data: Data) -> int:
    """
    Consider only horizontal and vertical lines. At how many points do
    at least two lines overlap?
    """
    # I can probably find a numpy command to do this, but i am still a beginner
    # to numpy as a libary. So im using a list comprehension for filtering.
    filtered_data = np.array(
        [((a, b), (c, d)) for ((a, b), (c, d)) in data if a == c or b == d],
        dtype=int,
    )

    return (intercetions(filtered_data) > 1).sum()


def part_2(data: Data):
    """
    Consider all of the lines. At how many points do at least two lines
    overlap?
    """
    return (intercetions(data) > 1).sum()


def main():
    data = parse_data("inputs/example_05.txt")

    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
