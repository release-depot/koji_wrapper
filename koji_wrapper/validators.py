# -*- coding: utf-8 -*-

""" Collection of validator methods  """

def validate_required(value):
    """
    Decorator method to raise error if a required parameter is not passed in.
    """
    if value is None:
        raise ValueError(f'Missing value for argument')
    return True

def validate_str_or_list(value):
    if isinstance(value, (str, list)) or value is None:
        return True
    else:
        raise TypeError('Must be a str or list')
