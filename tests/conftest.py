"""

conftest
"""
import datetime

from dateutil.tz import tzutc
import pytest


@pytest.fixture()
def deployment():
    """

    deployment fixture
    """
    yield {'api_version': 'apps/v1',
 'kind': 'Deployment',
 'metadata': {'annotations': {'deployment.kubernetes.io/revision': '2'},
              'cluster_name': None,
              'creation_timestamp': datetime.datetime(2022, 3, 13, 22, 35, 30, tzinfo=tzutc()),
              'deletion_grace_period_seconds': None,
              'deletion_timestamp': None,
              'finalizers': None,
              'generate_name': None,
              'generation': 2,
              'labels': {'app': 'debbuger'},
        }
 }


@pytest.fixture()
def daemonset():
    """

    daemonset fixture
    """
    yield {'api_version': 'apps/v1',
 'kind': 'DaemonSet',
 'metadata': {'annotations': {'deployment.kubernetes.io/revision': '2'},
              'cluster_name': None,
              'creation_timestamp': datetime.datetime(2022, 3, 13, 22, 35, 30, tzinfo=tzutc()),
              'deletion_grace_period_seconds': None,
              'deletion_timestamp': None,
              'finalizers': None,
              'generate_name': None,
              'generation': 2,
              'labels': {'app': 'debbuger'},
        }
 }
