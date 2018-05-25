"""
Test the utility methods
"""

import pytest
from koji_wrapper.util import convert_to_list


class TestConvertToList(object):
    def test_with_str(self):
        a_field = convert_to_list('foo')
        assert isinstance(a_field, list)

    def test_with_list(self):
        my_list = ['foo', 'bar', 'baz']
        returned = convert_to_list(my_list)
        assert returned == my_list

