"""
Test the KojiBase class
"""


import koji
import pytest
from unittest.mock import MagicMock
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


def test_logs_in_w_kerberos(shared_datadir):
    """
    GIVEN we have a profile that has an authtype of 'kerberos'
    WHEN we try to log in with a koji client that is kinit'ed
    THEN we should get back True and successfully log in.
    """

    tw = KojiWrapperBase(profile='mykoji',
                         user_config=shared_datadir / 'mykoji.conf')
    tw.session.gssapi_login = MagicMock(return_value=True)
    logged_in = tw.login()
    assert tw.profile == 'mykoji'
    assert logged_in is True
    assert tw.session.gssapi_login.called


def test_fails_gssapi_login_wo_ticket(shared_datadir):
    """
    GIVEN we have a profile that has an authtype of 'kerberos'
    WHEN we try to log in with a koji client that is not kinit'ed
    THEN we should get back an AuthError and not be logged in.
    """

    tw = KojiWrapperBase(profile='mykoji',
                         user_config=shared_datadir / 'mykoji.conf')
    logged_in = tw.login()
    assert tw.profile == 'mykoji'
    assert logged_in is False


def test_logs_in_w_ssl(shared_datadir):
    """
    GIVEN we have a profile that connects via ssl
    WHEN we try to log in with a koji client that has the correct credentials
    THEN we should get back True and successfully log in.
    """

    tw = KojiWrapperBase(profile='ssl_koji',
                         user_config=shared_datadir / 'ssl_koji.conf')
    tw.session.ssl_login = MagicMock(return_value=True)
    logged_in = tw.login()
    assert tw.profile == 'ssl_koji'
    assert logged_in is True
    assert tw.session.ssl_login.called


def test_fails_login_w_bad_ssl(shared_datadir):
    """
    GIVEN we have a profile that connects via ssl
    WHEN we try to log in with a koji client that does not have the correct
    credentials
    THEN we should get back an AuthError and not be logged in.
    """

    tw = KojiWrapperBase(profile='ssl_koji',
                         user_config=shared_datadir / 'ssl_koji.conf')
    logged_in = tw.login()
    assert tw.profile == 'ssl_koji'
    assert logged_in is False
