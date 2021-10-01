# -*- coding: utf-8 -*-

"""
Wraps a connection to koji, managing the session, and providing convenience
methods for interacting with the koji api.
"""
import os

import koji

from koji_wrapper.base import KojiWrapperBase


class KojiWrapper(KojiWrapperBase):

    def __init__(self, **kwargs):
        self._pathinfo = None
        super().__init__(**kwargs)

    def file_types(self, nvr, types=['image']):
        """
        :param nvr: nvr of the desired build
        :param types: list of koji archive types.  This is currently any of:
            'maven', 'win', or 'image'
        :returns: list of file types of given build
        """
        build = self.build(nvr)
        if not build:
            return None

        file_types = set([])
        for this_type in types:
            archives_list = self.archives(buildID=build['id'], type=this_type)
            if archives_list:
                for archive in archives_list:
                    file_types.add(archive['type_name'])

        if len(file_types):
            return list(file_types)

        # Default
        # TODO: make sure we actually need this default - can't see why we do.
        return ['rpm']

    def srpm_url(self, nvr=None):
        """
        :param nvr: reference to the rpm of the desired package.
            This may be any of:

        - int ID
        - string N-V-R.A
        - string N-V-R.A@location
        - map containing 'name', 'version', 'release', and 'arch' (and
          optionally 'location')

        :returns: srpm url for a given nvr
        """
        try:
            build = self.build(nvr)
            rpm_list = self.rpms(buildID=build.get('build_id'), arches='src')
            src_rpm = None
            for rpm in rpm_list:
                if rpm.get('arch') == 'src':
                    src_rpm = rpm
                    break
            return self._build_srpm_url(rpm=src_rpm, build=build)
        except Exception as inst:
            # TODO: either add logging or decide if we want to do more to
            # handle errors here.
            raise inst

    def _build_srpm_url(self, rpm=None, build=None):

        if self._pathinfo is None and self.topurl is not None:
            self._pathinfo = koji.PathInfo(topdir=self.topurl)

        # TODO: add error handling.
        srpm_path = self._pathinfo.rpm(rpm)
        base_path = self._pathinfo.build(build)
        return os.path.join(base_path, srpm_path)
