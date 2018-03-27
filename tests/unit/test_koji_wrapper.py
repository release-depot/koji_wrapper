"""
Test the main KojiWrapper class
"""

import pytest
import koji
from koji_wrapper.wrapper import KojiWrapper
from unittest.mock import MagicMock

sample_url = 'http://kojihub.com'
sample_topurl = 'http://somerepo.org'

def build_wrapper(this_session):
    return KojiWrapper( url = sample_url,
                        topurl = sample_topurl,
                        session = this_session)

def test_set_init_values():
    """
    GIVEN KojiWrapper initialized with no session
    WHEN the object is created
    THEN session is set to an instance of koji.ClientSession
    AND we should have properly set url and topurl
    """
    test_wrapper = build_wrapper(None)
    assert test_wrapper.url == sample_url
    assert test_wrapper.topurl == sample_topurl
    assert isinstance(test_wrapper.session,koji.ClientSession)

def test_init_with_koji_client_session():
    """
    GIVEN we have a valid koji.ClientSession object,
    WHEN this object is passed as the session to a new KojiWrapper
    THEN this object's session is set to the session of the passed object
    """
    client_session = MagicMock(spec=koji.ClientSession)
    test_wrapper = build_wrapper(client_session)
    assert isinstance(test_wrapper.session,koji.ClientSession)

def test_init_with_koji_wrapper():
    """
    GIVEN we have a valid KojiWrapper with a session,
    WHEN a KojiWrapper object is passed as the session to a new KojiWrapper
    THEN this object's session is set to the session of the passed object
    """
    my_koji_wrapper = build_wrapper(None)
    test_wrapper = build_wrapper(my_koji_wrapper)
    assert isinstance(test_wrapper.session,koji.ClientSession)
    assert test_wrapper.session is my_koji_wrapper.session

