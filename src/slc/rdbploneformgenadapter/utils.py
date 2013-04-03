"""Useful utilities."""


def cleanString(string):
    """Changes - to _ and removes dots"""
    return string.replace('-', '_').replace('.', '')
