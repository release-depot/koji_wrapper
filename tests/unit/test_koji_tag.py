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
    assert kt.tag is 'foo'
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
