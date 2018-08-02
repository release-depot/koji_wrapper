# -*- coding: utf-8 -*-

""" Collection of validator methods  """


def validate_required(value):
    """
    Method to raise error if a required parameter is not passed in.
    :param value: value to check to make sure it is not None
    :returns: True or ValueError
    """
    if value is None:
        raise ValueError('Missing value for argument')
    return True


def validate_str_or_list(value):
    """
    Method to raise error if a value is not a list.
    :param value: value to check to make sure it is a string, list, or None
    :returns: None or TypeError
    """
    if isinstance(value, (str, list)) or value is None:
        return True
    else:
        raise TypeError('Must be a str or list')
