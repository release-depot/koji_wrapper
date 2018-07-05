"""
Test the validation decorators
"""

import pytest
from koji_wrapper.validators import validate_required
from koji_wrapper.validators import validate_str_or_list


class TestValidateRequired(object):
    """
    GIVEN we call the validate_required function
    """
    def test_with_data(self):
        """
        WHEN we pass in a value
        THEN we get back True
        """
        a_field = validate_required('foo')
        assert a_field

    def test_with_data_missing(self):
        """
        WHEN we pass in None
        THEN we get a ValueError
        """
        with pytest.raises(ValueError):
            a_field = validate_required(None)  # NOQA


class TestValidateStrOrList(object):
    """
    GIVEN we call the validate_str_or_list function
    """
    def test_valid_type(self):
        """
        WHEN we pass in a string
        THEN we get back True
        """
        a_field = validate_str_or_list('a string')
        assert a_field

    def test_valid_type_none(self):
        """
        WHEN we pass in None
        THEN we get back True
        """
        a_field = validate_str_or_list(None)
        assert a_field

    def test_invalid_type(self):
        """
        WHEN we pass in anything but a string, list, or None
        THEN we get a TypeError
        """
        with pytest.raises(TypeError):
            validate_str_or_list(47)
