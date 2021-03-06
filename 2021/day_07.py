#!/usr/bin/env python3
"""
Day 7: Treachery of Whales

https://adventofcode.com/2021/day/7
"""
import math
import sys
from functools import partial
from typing import Callable, Optional, Union

Data = list[int]
Number = Union[int, float]

GR = (math.sqrt(5) + 1) / 2  # The golden ratio


def parse_data(path: Optional[str]) -> Data:
    if not sys.stdin.isatty():
        raw = sys.stdin.readlines()
    else:
        if path:
            with open(path, encoding="utf-8") as f:
                raw = f.readlines()
        else:
            sys.exit("No stdin data was recived.")

    data = sorted(list(map(int, raw[0].split(","))))
    return data


def gss(f: Callable, a: Number, b: Number, lim: Number) -> Number:
    """
    Golden-section search.

    Efficently find an extremum from a given function
    inside of a specified interval, [a, b].

    https://en.wikipedia.org/wiki/Golden-section_search
    """
    c = b - (b - a) / GR
    d = a + (b - a) / GR
    while abs(b - a) > lim:
        if f(c) < f(d):
            b = d
        else:
            a = c

        c = b - (b - a) / GR
        d = a + (b - a) / GR

    return (b + a) / 2


def linear_cost(point: Number, offset: Number) -> Number:
    return abs(point - offset)


def exponential_cost(point: Number, offset: Number) -> Number:
    steps = abs(point - offset)
    return (steps ** 2 + steps) / 2


def calculate_cost(func: Callable, data: Data, pos: Number) -> int:
    """
    Calculate the value of a given position by a defined
    function for cost.
    """
    return round(sum(func(point, pos) for point in data))


def solve(func, data: Data) -> int:
    # Golden ratio search requires a single argument function.
    # So im doing partial application of the function i want the
    # search to happen on.
    crab_cost_func = partial(calculate_cost, func, data)
    # We can set the limit to 1, as we are looking for the closest
    # integer instead of the true minimum.
    pos = gss(crab_cost_func, a=min(data), b=max(data), lim=1)
    # Rounding the position to the nearest integer per the tasks
    # definition of our minimum.
    return calculate_cost(func, data, round(pos))


def part_1(data: Data):
    """
    Determine the horizontal position that the crabs can align to using
    the least fuel possible so they can make you an escape route! How
    much fuel must they spend to align to that position?
    """
    return solve(linear_cost, data)


def part_2(data: Data):
    """
    Determine the horizontal position that the crabs can align to using
    the least fuel possible. How much fuel must they spend to align to
    that position?
    """
    return solve(exponential_cost, data)


def main():
    data = parse_data("inputs/example_07.txt")

    print(part_1(data))
    print(part_2(data))


if __name__ == "__main__":
    main()
