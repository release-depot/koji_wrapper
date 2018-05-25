# -*- coding: utf-8 -*-

""" Collection of utility methods  """

def convert_to_list(value):
    if isinstance(value, (str, int)):
        value = [value]
    return value

