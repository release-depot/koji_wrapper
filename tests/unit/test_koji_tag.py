"""
Test the main KojiTag class
"""

import pytest
from koji_wrapper.tag import KojiTag

sample_url = 'http://kojihub.com'
sample_topurl = 'http://somerepo.org'

def build_tag(tag, blacklist):
    return KojiTag( url = sample_url,
                    topurl = sample_topurl,
                    tag = tag,
                    blacklist = blacklist,
                    nvr_blacklist = blacklist)

def test_validates_required_fields():
    with pytest.raises(ValueError):
        kt = build_tag(None, None)

def test_sets_tag():
    kt = build_tag('foo', None)
    assert kt.tag is 'foo'
    assert kt.blacklist is None

def test_sets_blacklist_with_str():
    kt = build_tag('foo', 'a string')
    assert kt.blacklist == ['a string']

def test_sets_blacklist_with_list():
    kt = build_tag('foo', ['a string'])
    assert kt.blacklist == ['a string']
