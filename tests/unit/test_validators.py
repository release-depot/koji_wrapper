"""
Test the validation decorators
"""

import pytest
from koji_wrapper.validators import validate_required
from koji_wrapper.validators import validate_str_or_list


class TestValidateRequired(object):
    def test_with_data(self):
        a_field = validate_required('foo')
        assert a_field

    def test_with_data_missing(self):
        with pytest.raises(ValueError):
            a_field = validate_required(None)

class TestValidateStrOrList(object):
    def test_valid_type(self):
        a_field = validate_str_or_list('a string')
        assert a_field

    def test_valid_type_none(self):
        a_field = validate_str_or_list(None)
        assert a_field

    def test_invalid_type(self):
        with pytest.raises(TypeError):
            validate_str_or_list(47)
