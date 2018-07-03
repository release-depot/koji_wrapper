# -*- coding: utf-8 -*-

""" KojiTag Module """

from koji_wrapper.wrapper import KojiWrapper
from koji_wrapper.validators import validate_required, validate_str_or_list
from koji_wrapper.util import convert_to_list


class KojiTag(KojiWrapper):
    """Class to work with and gather koji tag information"""

    def __init__(self, tag=None,
                 nvr_blacklist=None, blacklist=None,
                 **kwargs):
        self.tag = tag
        self.nvr_blacklist = nvr_blacklist
        self.blacklist = blacklist
        self.tagged_list = None
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

    @property
    def tagged_list(self):
        """:param tagged_list: tagged_list of builds."""
        return self.__tagged_list

    @tagged_list.setter
    def tagged_list(self, tagged_list):
            self.__tagged_list = tagged_list

    def builds(self):
        """
        :returns: list of matching tagged build objects from koji
        """
        if self.tagged_list is None:
            self._filter_tagged(self.session.listTagged(self.tag))
        return self.tagged_list

    def _filter_tagged(self, tagged_builds):
        """
        :param tagged_builds: unflitered list of builds to clean up
        :returns: filtered list of matching tagged build objects from koji
        """
        self.tagged_list = [item for item in tagged_builds if item['name']
                            not in self.blacklist]
        self.tagged_list = [item for item in self.tagged_list if item['nvr']
                            not in self.nvr_blacklist]

        return self.tagged_list

    def latest_by_nvr(self):
        # TODO: implement/port _find_latest logic
        pass
