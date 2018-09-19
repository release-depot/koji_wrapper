# -*- coding: utf-8 -*-

"""
Provides common functionality for classes in this module which
wrap a connection to koji, manage the session, and provide
convenience methods for interacting with the koji api.
"""

import koji


class KojiWrapperBase(object):
    """
    Base Koji Wrapper object

    This class provides the common functionality to wrap
    a connection to koji, manage the session and simple
    convenience methods for interacting with the koji api.
    """

    def __init__(self, url='', topurl='',
                 profile='', user_config='', session=None):
        self.url = url
        self.topurl = topurl
        self.profile = profile
        self.user_config = user_config
        self.session = session

    @property
    def url(self):
        """:param url: Url of the koji-compliant hub to use"""
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def topurl(self):
        """:param topurl: Url of the package repository to use"""
        return self.__topurl

    @topurl.setter
    def topurl(self, topurl):
        self.__topurl = topurl

    @property
    def profile(self):
        """
        This is the profile koji should use to configure a client.

        This is a specific server, and there should be a config file specified
        in one of the standard locations koji looks:
          - /etc/koji.conf
          - /etc/koji.conf.d
          - ~/.koji/config.d
        :param profile: profile name of the koji-compliant hub to use
        """
        return self.__profile

    @profile.setter
    def profile(self, profile):
        self.__profile = profile

    @property
    def user_config(self):
        """
        This would be used in the case where you have custom user config.

        The file can be in any readable location specified by the user, and can
        point to a directory or a specific file.

        :param user_config: user_config file/path to be merged with profile
                or used in place of the profile if not installed in the system
                location.
        """

        return self.__user_config

    @user_config.setter
    def user_config(self, user_config):
        self.__user_config = user_config

    @property
    def session(self):
        """
        This property exposes koji.ClientSession used by wrapper

        Makes sure the object has a koji.ClientSession to use. It can be passed
        an existing KojiWrapper object, koji.ClientSession object, or None.  In
        the first two cases, the existing session will be reused. In the case
        of None, a new ClientSession will be created using the url param, if
        present.  When not present, if a profile and/or config are specified,
        those will be used to configure the ClientSession object.

        :param newsession: koji.ClientSession object to use

        :raises koji.ConfigurationError: In the case of a bad configuration,
            the client is not created, and this error is returned.
        """
        return self.__session

    @session.setter
    def session(self, newsession):
        if isinstance(newsession, koji.ClientSession):
            self.__session = newsession
        elif issubclass(type(newsession), KojiWrapperBase):
            self.__session = newsession.session
            if self.url is None or self.url == '':
                self.url = newsession.url

            if self.topurl is None or self.topurl == '':
                self.topurl = newsession.topurl
        else:
            self.__session = self._build_client()

    def _build_client(self):
        """
        Method to set up the KojiClient object used in this instance of
        KojiWrapperBase.  It will call all needed methods to get the config set
        up for the user.
        """
        if self.url:
            return koji.ClientSession(self.url)
        else:
            _profile = koji.read_config(self.profile,
                                        user_config=self.user_config)
            """
            NOTE: This check is here because if the user does not have and koji
            config files, read_config will 'helpfully' return you a useless
            default config.  The required baseurl ('server' in _profile) has a
            default, so we cannot check that.  However, topurl defaults to
            None, so we currently use this to devine if the returned config
            is the useless default.
            """
            if not _profile.get('topurl'):
                raise koji.ConfigurationError("no configuration for profile \
                        name: {0}".format(self.profile))
            return koji.ClientSession(_profile.get('server'), opts=_profile)

    def archives(self, **kwargs):
        """
        This method wraps koji client method listArchives

            https://pagure.io/koji/blob/master/f/hub/kojihub.py

        :param **kwargs: Any valid named parameter accepted by the koji
                client method listArchives:

        :returns: list of archives from koji
        """
        return self.session.listArchives(**kwargs)

    def build(self, nvr):
        """
        This method wraps the koji client method getBuild:

            https://pagure.io/koji/blob/master/f/hub/kojihub.py

        :param nvr: nvr of the desired build
        :returns: build object from koji
        """
        return self.session.getBuild(nvr)

    def rpms(self, **kwargs):
        """
        This method wraps the koji client method listRPMs

            https://pagure.io/koji/blob/master/f/hub/kojihub.py

        :param **kwargs: Any valid named parameter accepted by the koji
                client method listRPMs:

        :returns: list of matching rpms from koji
        """
        return self.session.listRPMs(**kwargs)

    def _handle_exception():
        pass
