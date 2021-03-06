#!/usr/bin/env python3
"""
Day 4: Giant Squid

https://adventofcode.com/2021/day/4
"""
import re
import sys
from typing import Optional

BingoNumbers = list[int]
Board = list[tuple[int, ...]]
Data = tuple[BingoNumbers, list[Board]]

RE_LINE = re.compile(r"^ ?(\d+) {1,2}(\d+) {1,2}(\d+) {1,2}(\d+) {1,2}(\d+)$")

def parse_data(path: Optional[str]) -> Data:
    if not sys.stdin.isatty():
        raw = sys.stdin.readlines()
    else:
        if path:
            with open(path, encoding="utf-8") as f:
                raw = f.readlines()
        else:
            sys.exit("No stdin data was recived.")

    bingo_numbers = list(map(int, raw[0].split(",")))
    boards = [raw[i : i + 5] for i in range(2, len(raw), 6)]
    boards = [
        [tuple(int(match) for match in RE_LINE.findall(line)[0]) for line in board]
        for board in boards
    ]
    return bingo_numbers, boards


def transpose(lst: list) -> list:
    return list(zip(*lst))


def flatten(lst: list) -> list:
    return [item for sublist in lst for item in sublist]


def check_board(winning_nums: BingoNumbers, board: Board) -> bool:
    for line in board + transpose(board):
        if all(num in winning_nums for num in line):
            return True
    return False


def find_bingo_winner(
    bingo_numbers: BingoNumbers, boards: list[Board]
) -> list[tuple[BingoNumbers, Board]]:
    winning_nums = []
    winning_boards = []
    for bingo_number in bingo_numbers:
        winning_nums.append(bingo_number)
        done_boards = list(map(lambda x: x[1], winning_boards))
        for board in [board for board in boards if board not in done_boards]:
            if check_board(winning_nums, board):
                winning_boards.append((list(winning_nums), board))
    return winning_boards


def part_1(bingo_numbers: BingoNumbers, boards: list[Board]):
    """
    To guarantee victory against the giant squid, figure out which
    board will win first. What will your final score be if you choose
    that board?
    """
    winning_boards = find_bingo_winner(bingo_numbers, boards)

    if not winning_boards:
        return -1

    winning_nums, board = winning_boards[0]
    unmarked_nums = sum(filter(lambda x: x not in winning_nums, flatten(board)))
    return unmarked_nums * winning_nums[-1]


def part_2(bingo_numbers: BingoNumbers, boards: list[Board]):
    """
    Figure out which board will win last. Once it wins, what would its
    final score be?
    """
    winning_boards = find_bingo_winner(bingo_numbers, boards)

    if not winning_boards:
        return -1

    loosing_nums, board = winning_boards[-1]
    unmarked_nums = sum(filter(lambda x: x not in loosing_nums, flatten(board)))
    return unmarked_nums * loosing_nums[-1]


def main():
    bingo_nums, boards = parse_data("inputs/example_04.txt")

    print(part_1(bingo_nums, boards))
    print(part_2(bingo_nums, boards))


if __name__ == "__main__":
    main()
