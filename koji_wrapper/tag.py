# -*- coding: utf-8 -*-

""" KojiTag Module """

import koji
from koji_wrapper.wrapper import KojiWrapper
from koji_wrapper.validators import *
from koji_wrapper.util import convert_to_list

class KojiTag(KojiWrapper):
    """Class to work with and gather koji tag information"""

    def __init__(self, tag=None,
                nvr_blacklist=None, blacklist=None,
                **kwargs):
        self.tag = tag
        self.nvr_blacklist = nvr_blacklist
        self.blacklist = blacklist
        super().__init__(**kwargs)


    @property
    def tag(self):
        """:param tag: tag to filter results with."""
        return self.__tag

    @tag.setter
    def tag(self, tag):
        if validate_required(tag):
            self.__tag = tag

    @property
    def nvr_blacklist(self):
        """:param nvr_blacklist: nvr_blacklist to limit results."""
        return self.__nvr_blacklist

    @nvr_blacklist.setter
    def nvr_blacklist(self, nvr_blacklist):
        if validate_str_or_list(nvr_blacklist):
            self.__nvr_blacklist = convert_to_list(nvr_blacklist)

    @property
    def blacklist(self):
        """:param blacklist: blacklist to limit results."""
        return self.__blacklist

    @blacklist.setter
    def blacklist(self, blacklist):
        if validate_str_or_list(blacklist):
            self.__blacklist = convert_to_list(blacklist)
