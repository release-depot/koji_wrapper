# -*- coding: utf-8 -*-

""" Collection of utility methods  """


def convert_to_list(value):
    """
    :param value: a value to convert into a string.  Currently, this must be one
    of [string, list, None]
    :returns: a flat list version of the value passed in
    """
    if isinstance(value, str):
        value = [value]
    elif value is None:
        value = []
    return value
