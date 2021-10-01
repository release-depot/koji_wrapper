# -*- coding: utf-8 -*-

""" Collection of utility methods  """

from koji_wrapper.exceptions import UnsupportedTypeException


def convert_to_list(value):
    """
    :param value: a value to convert into a list.  Currently, this must be one
        of \\[[string, list, None\\[]
    :returns: a flat list version of the value passed in
    """

    supported = (str, list)
    if isinstance(value, supported) is False and value is not None:
        raise UnsupportedTypeException

    if isinstance(value, str):
        value = [value]
    elif value is None:
        value = []
    return value
