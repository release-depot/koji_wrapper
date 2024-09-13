# -*- coding: utf-8 -*-

""" KojiTag Module """
from toolchest.rpm.rpmvercmp import rpmvercmp

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

    def __str__(self):
        """return tag as description(str for human)"""
        return self.tag

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

    def builds(self, **kwargs):
        """
        This method wraps the koji client method listTagged:

            https://pagure.io/koji/blob/master/f/hub/kojihub.py

        :param \\*\\*kwargs: Any valid named parameter accepted by the koji
                client method listTagged:
        :returns: list of matching tagged build objects from koji
        """
        if self.tagged_list is None:
            self._filter_tagged(self.session.listTagged(self.tag, **kwargs))
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
        """
        Return the build from the cached builds list (listTagged) that has the
        greatest NVR. This uses the toolchest library to also account for
        timestamps and other things that make the koji '--latest' flag not
        always return the desired result.
        """
        greatest_nvr = None
        for build in self.builds():
            if greatest_nvr:
                # Compare previously found greatest nvr with the next item in
                # the list and only change greatest_nvr if the new item is
                # greater.
                if rpmvercmp(build['nvr'], greatest_nvr['nvr']) == 1:
                    greatest_nvr = build
            else:
                greatest_nvr = build
        return greatest_nvr

    def builds_by_attribute(self, attribute):
        """
        Return a list of the specified attribute, extracted from the list of
        tagged builds.  For instance, you may call with 'nvr' to get back the
        list of NVRs in your build list.  Throws a KeyError if you request an
        attribute that does not exist in the build objects.

        :param attribute: Any attribute (or key) from a build object, such as
                          'nvr', 'name', etc.
        :returns: a list of strings
        :raises KeyError: if attribute passed is invalid

        """

        # covers brewtag.components and brewtag.builds cases
        return [build[attribute] for build in self.tagged_list]

    def builds_by_attribute_and_label(self, attribute, label, match):
        """
        Return a list of the specified attribute, filtered by matching labels,
        extracted from the list of tagged builds.  For instance, you may call
        with 'nvr', 'name', 'foo' to get back the list of NVRs in your build
        list for items with a name of 'foo'.  Throws a KeyError if you request
        an attribute that does not exist in the build objects.

        :param attribute: Any attribute (or key) from a build object, such as
                          'nvr', 'name', etc.
        :param label: Any label (or key) from a build object, which you wish to
                      use to filter your results, such as 'nvr', 'name', etc.
        :param match: Value you are looking to match for the label that was
                      passed in.

        :returns: a list of strings
        :raises KeyError: if attribute passed is invalid

        """

        # covers brewtag.builds_package case
        return [build[attribute] for build in self.tagged_list
                if build[label] == match]
