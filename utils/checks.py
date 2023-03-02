#!/usr/bin/python3
"""Checks utility functions"""


def check_equals(num: int = 0) -> int:
    """Check if the given number is equal to 1 or 0"""
    if num < 0:
        num = 0
        return num
    elif num > 1:
        num = 1
        return num
