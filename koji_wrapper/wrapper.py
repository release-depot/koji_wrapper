# -*- coding: utf-8 -*-

"""
Wraps a connection to koji, managing the session, and providing convenience
methods for interacting with the koji api.
"""

from koji_wrapper.base import KojiWrapperBase

class KojiWrapper(KojiWrapperBase):

    def build(self, nvr):
        """
        :param nvr: of the desired build
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

    def file_types(self, nvr, types=['image']):
        """
        :param nvr: of the desired build:
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
        #TODO: make sure we actually need this default - can't see why we do.
        return ['rpm']
