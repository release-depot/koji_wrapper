"""Define Fixtures used throughout the project."""

import pytest


@pytest.fixture()
def sample_build():
    return {'package_name': 'my-project',
            'extra': None,
            'creation_time': '2018-03-01 22:07:52.627945',
            'completion_time': '2018-03-01 22:33:12.648992',
            'package_id': 56043,
            'id': 658835,
            'build_id': 658835,
            'epoch': None,
            'source': None,
            'state': 1,
            'version': '9.0',
            'completion_ts': 1519943592.64899,
            'owner_id': 1527,
            'owner_name': 'someone',
            'nvr': 'my-project-9.0-20190301.1.el7',
            'start_time': '2018-03-01 22:07:52.627945',
            'creation_event_id': 18416869,
            'start_ts': 1519942072.62794,
            'volume_id': 0,
            'creation_ts': 1519942072.62794,
            'name': 'my-project',
            'task_id': 15464337,
            'volume_name': 'DEFAULT',
            'release': '20190301.1.el7'}


@pytest.fixture()
def sample_rpm_list():
    return [
        {
            'build_id': 670920,
            'nvr': 'my-project-9.0-20190301.1.el7',
            'extra': None,
            'buildroot_id': 3837636,
            'buildtime': 1523295721,
            'payloadhash': '42731f7fc0b4db65573cd6615a1200fe',
            'epoch': None,
            'version': '9.0',
            'metadata_only': False,
            'external_repo_id': 0,
            'release': '20190301.1.el7',
            'size': 80084,
            'arch': 'noarch',
            'id': 5531502,
            'external_repo_name': 'INTERNAL',
            'name': 'my-project'
        },
        {
            'build_id': 670920,
            'nvr': 'my-project-9.0-20190301.1.el7',
            'extra': None,
            'buildroot_id': 3837636,
            'buildtime': 1523295718,
            'payloadhash': '7bebd0e2cdee9e07709aa22a7273d10b',
            'epoch': None,
            'version': '9.0',
            'metadata_only': False,
            'external_repo_id': 0,
            'release': '20190301.1.el7',
            'size': 111828,
            'arch': 'src',
            'id': 5531501,
            'external_repo_name': 'INTERNAL',
            'name': 'my-project'
        }
    ]


@pytest.fixture()
def sample_srpm():
    return {
        'build_id': 670920,
        'nvr': 'my-project-9.0-20190301.1.el7',
        'extra': None,
        'buildroot_id': 3837636,
        'buildtime': 1523295718,
        'payloadhash': '7bebd0e2cdee9e07709aa22a7273d10b',
        'epoch': None,
        'version': '9.0',
        'metadata_only': False,
        'external_repo_id': 0,
        'release': '20190301.1.el7',
        'size': 111828,
        'arch': 'src',
        'id': 5531501,
        'external_repo_name': 'INTERNAL',
        'name': 'my-project'
    }


@pytest.fixture()
def sample_archives():
    return [
        {
            'build_id': 666503,
            'type_name': 'xml',
            'type_id': 5,
            'checksum': '5ccff657de1e95f3ec4f6bbaaa807a64',
            'extra': None,
            'filename': 'tdl-x86_64.xml',
            'type_description': 'XML file',
            'metadata_only': False,
            'type_extensions': 'xml',
            'btype': 'image',
            'checksum_type': 0,
            'btype_id': 4,
            'buildroot_id': None,
            'id': 2383603,
            'size': 674
        },
        {
            'build_id': 666503,
            'type_name': 'ks',
            'type_id': 38,
            'checksum': '7b628c55169c29977e2765e22f067816',
            'extra': None,
            'filename': 'input_image.ks',
            'type_description': 'Kickstart',
            'metadata_only': False,
            'type_extensions': 'ks',
            'btype': 'image',
            'checksum_type': 0,
            'btype_id': 4,
            'buildroot_id': None,
            'id': 2383604,
            'size': 444
        },
        {
            'build_id': 666503,
            'type_name': 'rpm',
            'type_id': 38,
            'checksum': 'ecd81413754e88b3907de740e5992275',
            'extra': None,
            'filename': 'koji-myproject.rpm',
            'type_description': 'RPM',
            'metadata_only': False,
            'type_extensions': 'rpm',
            'btype': 'image',
            'checksum_type': 0,
            'btype_id': 4,
            'buildroot_id': None,
            'id': 2383605,
            'size': 2076
        },
        {
            'build_id': 666503,
            'type_name': 'image',
            'type_id': 5,
            'checksum': 'acd4059c1af628de2d4cad777f69d151',
            'extra': None,
            'filename': 'libvirt-qcow2-x86_64.xml',
            'type_description': 'XML file',
            'metadata_only': False,
            'type_extensions': 'xml',
            'btype': 'image',
            'checksum_type': 0,
            'btype_id': 4,
            'buildroot_id': None,
            'id': 2383606,
            'size': 1384
        },
        {
            'build_id': 666503,
            'type_name': 'qcow2',
            'type_id': 28,
            'checksum': '615019a6c1db5a16fe0dee2f577ef06e',
            'extra': None,
            'filename': 'koji-myproject.qcow2',
            'type_description': 'QCOW2 image',
            'metadata_only': False,
            'type_extensions': 'qcow2',
            'btype': 'image',
            'checksum_type': 0,
            'btype_id': 4,
            'buildroot_id': None,
            'id': 2383607,
            'size': 778874368
        }
    ]


@pytest.fixture()
def sample_tagged_builds():
    return [
        {
            'build_id': 711039,
            'owner_name': 'zcaplovi',
            'package_name': 'my-project-selinux',
            'task_id': 16729456,
            'state': 1,
            'nvr': 'my-project-selinux-0.8.14-13.el7ost',
            'start_time': '2018-06-14 15:52:44.261256',
            'creation_event_id': 19964853,
            'creation_time': '2018-06-14 15:52:44.261256',
            'epoch': None,
            'tag_id': 11970,
            'completion_time': '2018-06-14 15:58:09.078495',
            'tag_name': 'rhos-13.0-rhel-7-candidate',
            'version': '0.8.14',
            'volume_id': 0,
            'release': '13.el7ost',
            'package_id': 40498,
            'owner_id': 4340,
            'id': 711039,
            'volume_name': 'DEFAULT',
            'name': 'my-project-selinux'
        },
        {
            'build_id': 710815,
            'owner_name': 'skaplons',
            'package_name': 'cool-project',
            'task_id': 16717562,
            'state': 1,
            'nvr': 'cool-project-12.0.2-0.20180421011362.0ec54fd.el7ost',
            'start_time': '2018-06-13 19:43:51.567191',
            'creation_event_id': 19957612,
            'creation_time': '2018-06-13 19:43:51.567191',
            'epoch': 1,
            'tag_id': 11970,
            'completion_time': '2018-06-13 19:52:31.816179',
            'tag_name': 'rhos-13.0-rhel-7-candidate',
            'version': '12.0.2',
            'volume_id': 0,
            'release': '0.20180421011362.0ec54fd.el7ost',
            'package_id': 43081,
            'owner_id': 4327,
            'id': 710815,
            'volume_name': 'DEFAULT',
            'name': 'cool-project'
        }
    ]
