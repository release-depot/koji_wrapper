# -*- coding: utf-8 -*-

"""
Provides common functionality for classes in this module which
wrap a connection to koji, manage the session, and provide
convenience methods for interacting with the koji api.
"""

import koji
import operator

class KojiWrapperBase(object):

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
        '''
        :param session: makes sure the object has a koji.ClientSession to use
                Can be passed an existing KojiWrapper object, koji.ClientSession
                object, or None.  In the first two cases, the existing session
                will be reused
        '''
        return self.__session

    @session.setter
    def session(self, newsession):
        if isinstance(newsession, koji.ClientSession):
            self.__session = newsession
        elif issubclass(type(newsession), KojiWrapperBase):
            self.__session = newsession.session
        else:
            self.__session = koji.ClientSession(self.url)

    def build(self, nvr):
        """
        :param nvr: nvr of the desired build
        :returns: build object from koji
        """
        return self.session.getBuild(nvr)

    def archives(self, **kwargs):
        """
        :param **kwargs: Any valid named parameter accepted by the koji client's
            listArchives method
        :returns: list of archives from koji
        """
        return self.session.listArchives(**kwargs)
