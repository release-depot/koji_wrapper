"""
Test the KojiBase class
"""


import koji
import pytest
# from unittest.mock import MagicMock
from koji_wrapper.base import KojiWrapperBase


def test_parses_config(shared_datadir):
    """
    GIVEN we have a profile defined in a user-specified directory
    WHEN we create a koji.ClientSession object
    THEN we should successfully create a Client using this profile.
    """

    tw = KojiWrapperBase(profile='mykoji',
                         user_config=shared_datadir / 'mykoji.conf')
    assert tw.profile == 'mykoji'
    assert isinstance(tw.session, koji.ClientSession)


def test_config_throws_error_on_no_file():
    """
    GIVEN we do NOT have the expected file defined in the specified
        location
    WHEN we try to create a koji.ClientSession object
    THEN we should get back a koji.ConfigurationError
    """

    with pytest.raises(koji.ConfigurationError):
        KojiWrapperBase(profile='mykoji',
                        user_config='/tmp/not_a_file.conf')


def test_config_throws_error_on_no_profile():
    """
    GIVEN we do NOT have the profile defined in the standard location koji
        looks
    WHEN we try to create a koji.ClientSession object
    THEN we should get back a koji.ConfigurationError
    """

    with pytest.raises(koji.ConfigurationError):
        KojiWrapperBase(profile='not_a_profile')
