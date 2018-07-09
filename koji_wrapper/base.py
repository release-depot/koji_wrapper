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
    convenience methos for interacting with the koji api.
    """

    def __init__(self, url='', topurl='', session=None):
        self.url = url
        self.topurl = topurl
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
    def session(self):
        """
        This property exposes koji.ClientSession used by wrapper

        :param session: makes sure the object has a koji.ClientSession to use.
                Can be passed an existing KojiWrapper object,
                koji.ClientSession object, or None.  In the first two cases,
                the existing session will be reused.
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
            self.__session = koji.ClientSession(self.url)

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
