"""
Test the utility methods
"""

import pytest  # NOQA
from koji_wrapper.util import convert_to_list, rpmvercmp, labelCompare
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


class TestRpmvercmp(object):

    def test_equal(self):
        assert rpmvercmp('1.2', '1.2') == 0
        assert rpmvercmp('a', 'a') == 0

    def test_basic(self):
        assert rpmvercmp('1.1', '1.2') == -1
        assert rpmvercmp('1.2', '1.1') == 1
        assert rpmvercmp('1.2a', '1.2') == 1
        assert rpmvercmp('1.2', '1.2a') == -1
        assert rpmvercmp('1.2', '1.1abcde') == 1
        assert rpmvercmp('1', '11') == -1
        assert rpmvercmp('11', '1') == 1
        assert rpmvercmp('a', 'b') == -1
        assert rpmvercmp('b', 'a') == 1

    def test_lead_zeroes(self):
        assert rpmvercmp('1.2.2031', '1.2.02031') == 0
        assert rpmvercmp('01.02.0000002031', '1.2.2031') == 0
        assert rpmvercmp('1.2.2031', '1.2.00002030') == 1
        assert rpmvercmp('1.2.2030', '1.2.00002031') == -1

    def test_excessive_version_length(self):
        assert(rpmvercmp('9999999999999999999999999999999999999999999',
                         '9999999999999999999999999999999999999999999') == 0)
        assert(rpmvercmp('9999999999999999999999999999999999999999999',
                         '9999999999999999999999999999999999999999998') == 1)
        assert(rpmvercmp('9999999999999999999999999999999999999999998',
                         '9999999999999999999999999999999999999999999') == -1)

    def test_weird_versions(self):
        a = 'a'
        b = '1'
        assert rpmvercmp(a, b) == -1
        assert rpmvercmp(b, a) == 1

        a = '1.01.001'
        b = '1.1.1'
        assert rpmvercmp(a, b) == 0

        a = '~1'
        assert rpmvercmp(a, b) == -1
        assert rpmvercmp(b, a) == 1

        a = '1~1'
        assert rpmvercmp(a, b) == -1
        assert rpmvercmp(b, a) == 1

        a = '----'
        b = '-'
        assert rpmvercmp(a, b) == 0

        a = '1-'
        b = '1'
        assert rpmvercmp(a, b) == 0

        a = '1-'
        b = '-'
        assert rpmvercmp(a, b) == 1
        assert rpmvercmp(b, a) == -1

    def test_bad_types(self):
        with pytest.raises(ValueError):
            rpmvercmp({}, '1.0')
        with pytest.raises(ValueError):
            rpmvercmp('1.0', {})


class TestLabelCompare(object):

    def test_basic(self):
        a = ('0', '6.0.0', '2.el7ost')
        b = ('0', '6.0.1', '2.el7ost')
        assert labelCompare(a, b) == -1
        assert labelCompare(a, a) == 0
        assert labelCompare(b, a) == 1
        assert labelCompare(b, b) == 0

    def test_vr_only(self):
        # no epoch => epoch = 0
        a = ('6.0.0', '2.el7ost')
        b = ('6.0.1', '2.el7ost')
        assert labelCompare(a, b) == -1
        assert labelCompare(a, a) == 0
        assert labelCompare(b, a) == 1
        assert labelCompare(b, b) == 0

    def test_zero_epoch(self):
        # 0 and no epoch are the same
        a = ('0', '6.0.0', '2.el7ost')
        b = ('6.0.1', '2.el7ost')
        assert labelCompare(a, b) == -1
        assert labelCompare(a, a) == 0
        assert labelCompare(b, a) == 1
        assert labelCompare(b, b) == 0

    def test_eq_epoch(self):
        a = ('1', '6.0.0', '2.el7ost')
        b = ('1', '6.0.1', '2.el7ost')
        assert labelCompare(a, b) == -1
        assert labelCompare(a, a) == 0
        assert labelCompare(b, a) == 1
        assert labelCompare(b, b) == 0

    def test_neq_epoch(self):
        # a always wins.
        a = ('1', '6.0.0', '2.el7ost')
        b = ('0', '6.0.1', '2.el7ost')
        assert labelCompare(a, b) == 1
        assert labelCompare(a, a) == 0
        assert labelCompare(b, a) == -1
        assert labelCompare(b, b) == 0

    def test_bad_types(self):
        a = '1:6.0.0-2.el7ost'
        b = 1
        with pytest.raises(ValueError):
            labelCompare(a, b)
        with pytest.raises(ValueError):
            labelCompare(b, a)

    def test_bad_length(self):
        a = ('1', '6.0.0', '2.el7ost', 1)
        b = ('0', '6.0.1', '2.el7ost')
        with pytest.raises(ValueError):
            labelCompare(a, b)
        with pytest.raises(ValueError):
            labelCompare(b, a)

    def test_bad_epoch(self):
        a = ('abcde', '1.0', '1')
        b = ('1.0', '1')
        with pytest.raises(ValueError):
            labelCompare(a, b)

    def test_weird_versions(self):
        a = ('0', 'a', '1')
        b = ('0', '1', '1')
        assert labelCompare(a, b) == -1
        assert labelCompare(b, a) == 1

        a = ('0', '1.01.001', '1')
        b = ('0', '1.1.1', '1')
        assert labelCompare(a, b) == 0

        a = ('0', '~1', '1')
        b = ('0', '1', '1')
        assert labelCompare(a, b) == -1
        assert labelCompare(b, a) == 1

        a = ('0', '1~1', '1')
        b = ('0', '1', '1')
        assert labelCompare(a, b) == -1
        assert labelCompare(b, a) == 1
