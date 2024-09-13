"""
Test the main KojiTag class
"""

import pytest
from unittest.mock import MagicMock
from koji_wrapper.tag import KojiTag

sample_url = 'http://kojihub.com'
sample_topurl = 'http://somerepo.org'


def build_tag(tag, blacklist=None,
              nvr_blacklist=None):
    return KojiTag(url=sample_url,
                   topurl=sample_topurl,
                   tag=tag,
                   blacklist=blacklist,
                   nvr_blacklist=nvr_blacklist)


def test_validates_required_fields():
    """
    GIVEN we do not have a KojiTag object
    WHEN we try to create one without required parameters
    THEN we should get a ValueError
    """
    with pytest.raises(ValueError):
        kt = build_tag(None, None)  # NOQA


def test_sets_tag():
    """
    GIVEN we do not have a KojiTag object
    WHEN we try to create one with a tag specified
    THEN the tag property should be set
    """
    kt = build_tag('foo')
    assert kt.tag == 'foo'
    assert kt.blacklist == []


def test_sets_blacklist_with_str():
    """
    GIVEN we do not have a KojiTag object
    WHEN we try to create one with a blacklist item as a string
    THEN the blacklist property should be set as an array of 1
    """
    kt = build_tag('foo', blacklist='a string')
    assert kt.blacklist == ['a string']


def test_sets_blacklist_with_list():
    """
    GIVEN we do not have a KojiTag object
    WHEN we try to create one with a blacklist item as an array
    THEN the blacklist property should be set as an array of 1
    """
    kt = build_tag('foo', blacklist=['a string'])
    assert kt.blacklist == ['a string']


def test_gets_builds(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object
    WHEN we call the builds() method for the first time
    THEN the tagged builds should be returned
    AND the listTagged method of the session object should be called.
    """
    kt = build_tag('foo')
    kt.session.listTagged = MagicMock(return_value=sample_tagged_builds)
    assert kt.builds() == sample_tagged_builds
    assert kt.session.listTagged.called


def test_passes_builds_extra_args(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object
    WHEN we call the builds() method for the first time with a parameter
    THEN the tagged builds should be returned
    AND the listTagged method of the session object should be called
        with the expected parameter.
    """
    kt = build_tag('foo')
    kt.session.listTagged = MagicMock(return_value=sample_tagged_builds)
    assert kt.builds(inherit=True) == sample_tagged_builds
    kt.session.listTagged.assert_called_with('foo', inherit=True)


def test_caches_builds(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object
    WHEN we call the builds() method for the second time
    THEN the tagged builds should be returned
    AND the listTagged method of the session object should not be called.
    """
    kt = build_tag('foo')
    kt.session.listTagged = MagicMock(return_value=sample_tagged_builds)
    kt.tagged_list = sample_tagged_builds
    assert kt.builds() == sample_tagged_builds
    assert not kt.session.listTagged.called


def test_filters_builds_by_blacklist(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object with a blacklist
    WHEN we call _filter_tagged
    THEN the filtered tagged builds should be returned
    AND it should not include the item in the blacklist
    """
    kt = build_tag('foo', blacklist='my-project-selinux')
    kt.session.listTagged = MagicMock(return_value=sample_tagged_builds)
    filtered = kt._filter_tagged(sample_tagged_builds)
    assert len(filtered) == 1
    assert filtered[0].get('name') == 'cool-project'


def test_filters_builds_by_nvr(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object with an nvr
    WHEN we call _filter_tagged
    THEN the filtered tagged builds should be returned
    AND it should not include the item with the nvr
    """
    _nvr = 'cool-project-12.0.2-0.20180421011362.0ec54fd.el7ost'
    kt = build_tag('foo', nvr_blacklist=_nvr)
    kt.session.listTagged = MagicMock(return_value=sample_tagged_builds)
    filtered = kt._filter_tagged(sample_tagged_builds)
    assert len(filtered) == 1
    assert filtered[0].get('name') == 'my-project-selinux'


def test_filters_builds_by_both(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object with a blacklist and nvr
    WHEN we call _filter_tagged
    THEN the filtered tagged builds should be returned
    AND it should not include the items in the blacklist or nvr
    """
    _nvr = 'cool-project-12.0.2-0.20180421011362.0ec54fd.el7ost'
    _blacklist = 'my-project-selinux'
    kt = build_tag('foo', nvr_blacklist=_nvr, blacklist=_blacklist)
    kt.session.listTagged = MagicMock(return_value=sample_tagged_builds)
    filtered = kt._filter_tagged(sample_tagged_builds)
    assert len(filtered) == 0


def test_selects_latest_build_by_nvr(builds_for_tag):
    """
    GIVEN we have a KojiTag object filtered by tag and package
    WHEN we call latest_by_nvr
    THEN we get the build object with the latest nvr
    """
    kt = build_tag('some_release')
    kt.session.listTagged = MagicMock(return_value=builds_for_tag)
    # In real usage, this is how we would narrow down the build list for the
    # tested use case
    assert kt.builds(package='important-container') == builds_for_tag
    latest = kt.latest_by_nvr()
    assert latest['nvr'] == 'important-container-18.0.0-29'


def test_gets_attribute_for_builds_in_list(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object
    WHEN we call builds_by_attribute with the desired attribute name
    THEN we get back a list of values for that attribute name from the list of
        builds.
    """

    kt = build_tag('foo')
    kt.tagged_list = sample_tagged_builds
    nvrs = kt.builds_by_attribute('nvr')
    assert len(kt.tagged_list) == 2
    assert len(nvrs) == 2
    assert nvrs[0] == 'my-project-selinux-0.8.14-13.el7ost'


def test_invalid_attribute_for_builds_in_list(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object
    WHEN we call builds_by_attribute with an invalid attribute name
    THEN we get a KeyError.
    """

    kt = build_tag('foo')
    kt.tagged_list = sample_tagged_builds
    with pytest.raises(KeyError):
        nvrs = kt.builds_by_attribute('farkle') # NOQA


def test_builds_by_attribute_and_label(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object
    WHEN we call builds_by_attribute_and_label with the desired attribute name
        and label,
    THEN we get back a list of values for that attribute name from the list of
        builds where the label also matches.
    """

    kt = build_tag('foo')
    kt.tagged_list = sample_tagged_builds
    nvrs = kt.builds_by_attribute_and_label('nvr',
                                            'name',
                                            'my-project-selinux')
    assert len(kt.tagged_list) == 2
    assert len(nvrs) == 1
    assert nvrs[0] == 'my-project-selinux-0.8.14-13.el7ost'


def test_invalid_builds_by_attribute_and_label(sample_tagged_builds):
    """
    GIVEN we have a KojiTag object
    WHEN we call builds_by_attribute_and_label with an invalid attribute name
    THEN we get a KeyError.
    """

    kt = build_tag('foo')
    kt.tagged_list = sample_tagged_builds
    with pytest.raises(KeyError):
        kt.builds_by_attribute_and_label('farkle',
                                         'name',
                                         'my-project-selinux')


def test_str_returns_tag():
    """
    GIVEN we have a KojiTag object
    WHEN we call through to the __str__() method
    THEN we get back a string with the tag it was based on
    """
    kt = build_tag('foo')
    assert 'foo' == str(kt)
