"""
Test the utility methods
"""

import pytest  # NOQA
from koji_wrapper.util import convert_to_list
from koji_wrapper.exceptions import UnsupportedTypeException


class TestConvertToList(object):
    """
    GIVEN we call the convert_to_list function
    """
    def test_with_str(self):
        """
        WHEN we pass in a single string
        THEN we get back a list of 1 item
        """
        returned = convert_to_list('foo')
        assert isinstance(returned, list)
        assert len(returned) == 1

    def test_with_list(self):
        """
        WHEN we pass in a list
        THEN we get back the same list
        """
        my_list = ['foo', 'bar', 'baz']
        returned = convert_to_list(my_list)
        assert isinstance(returned, list)
        assert len(returned) == 3
        assert returned == my_list

    def test_with_none(self):
        """
        WHEN we pass in None
        THEN we get back an empty list
        """
        returned = convert_to_list(None)
        assert isinstance(returned, list)
        assert len(returned) == 0
        assert returned == []

    def test_with_unsupported(self):
        """
        WHEN we pass in an unsupported type
        THEN we get back an UnsupportedTypeException
        """
        with pytest.raises(UnsupportedTypeException):
            convert_to_list({})
