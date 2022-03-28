"""

test PodDebugger
"""
from unittest.mock import patch, MagicMock
import io

import pytest

from remote_pod_debugger.pod_debugger import PodDebugger


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("remote_pod_debugger.pod_debugger.client.AppsV1Api.patch_namespaced_deployment")
def test_pod_debugger_patch_deployment(patch_namespaced_deployment, load_kube_config):
    """

    test patch deployment
    """
    _deployment_name = "debugger-deployment"
    _namespace = "debugger"
    _host = "127.0.0.1"
    _port = 5999
    _entrypoint = "main.py"
    _container_name = "debugger"
    _image_name = "localhost:5001/b4nks/debugger-app"
    _pdb_commands = []
    _pod_debugger = PodDebugger(_debug=True)
    _patch_results = _pod_debugger.patch(_deployment_name,
                                         _namespace,
                                         _host,
                                         _port,
                                         _entrypoint,
                                         _container_name,
                                         _image_name,
                                         _pdb_commands)
    assert patch_namespaced_deployment.called


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("remote_pod_debugger.pod_debugger.client.AppsV1Api.patch_namespaced_daemon_set")
def test_pod_debugger_patch_daemonset(patch_namespaced_daemon_set, load_kube_config):
    """

    test patch daemonset
    """
    _deployment_name = "debugger-deployment"
    _namespace = "debugger"
    _host = "127.0.0.1"
    _port = 5999
    _entrypoint = "main.py"
    _container_name = "debugger"
    _image_name = "localhost:5001/b4nks/debugger-app"
    _pdb_commands = []
    _pod_debugger = PodDebugger(_debug=True)
    _patch_results = _pod_debugger.patch(_deployment_name,
                                         _namespace,
                                         _host,
                                         _port,
                                         _entrypoint,
                                         _container_name,
                                         _image_name,
                                         _pdb_commands,
                                         "daemonset")
    assert patch_namespaced_daemon_set.called


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("remote_pod_debugger.pod_debugger.client.AppsV1Api.read_namespaced_deployment")
def test_pod_debugger_backup_deployment(read_namespaced_deployment, load_kube_config, deployment):
    """

    test backup deployment
    """
    _deployment_name = "debugger-deployment"
    _namespace = "debugger"
    _pod_debugger = PodDebugger()
    _file = io.StringIO()
    read_namespaced_deployment.return_value = deployment
    _pod_debugger.backup(_deployment_name, _namespace, _file)
    assert read_namespaced_deployment.called
    assert _file.getvalue() == "api_version: apps/v1\nkind: Deployment\nmetadata:\n  annotations:\n    deployment.kubernetes.io/revision: '2'\n  cluster_name: null\n  creation_timestamp: '2022-03-13T22:35:30+00:00'\n  deletion_grace_period_seconds: null\n  deletion_timestamp: null\n  finalizers: null\n  generate_name: null\n  generation: 2\n  labels:\n    app: debbuger\n"


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("remote_pod_debugger.pod_debugger.client.AppsV1Api.read_namespaced_daemon_set")
def test_pod_debugger_backup_daemonset(read_namespaced_daemon_set, load_kube_config, daemonset):
    """

    test backup daemonset
    """
    _daemon_name = "debugger-deployment"
    _namespace = "debugger"
    _pod_debugger = PodDebugger()
    _file = io.StringIO()
    read_namespaced_daemon_set.return_value = daemonset
    _pod_debugger.backup(_daemon_name, _namespace, _file, "daemonset")
    assert read_namespaced_daemon_set.called
    assert _file.getvalue() == "api_version: apps/v1\nkind: DaemonSet\nmetadata:\n  annotations:\n    deployment.kubernetes.io/revision: '2'\n  cluster_name: null\n  creation_timestamp: '2022-03-13T22:35:30+00:00'\n  deletion_grace_period_seconds: null\n  deletion_timestamp: null\n  finalizers: null\n  generate_name: null\n  generation: 2\n  labels:\n    app: debbuger\n"


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("remote_pod_debugger.pod_debugger.client.CoreV1Api.list_namespace")
@patch("builtins.input", lambda *args: 'test1')
def test_pod_debugger_select_namespace(list_namespace, load_kube_config):
    """

    test select_namespace
    """
    class fakeMetadata:
        def __init__(self, value):
            self.name = value
    class fakeNamespace:
        def __init__(self, value):
            self.metadata = fakeMetadata(value)
    class fakeListNamespace:
        def __init__(self, value):
            self.items = [fakeNamespace(item) for item in value]
    namespace_selected = "test1"
    list_namespace.return_value = fakeListNamespace(["test1", "test2"])
    _pod_debugger = PodDebugger(_debug=True)
    result = _pod_debugger.select_namespace()
    assert result == namespace_selected


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("remote_pod_debugger.pod_debugger.client.AppsV1Api.list_namespaced_deployment")
@patch("builtins.input", lambda *args: 'test1')
def test_pod_debugger_select_deployment(list_namespace, load_kube_config):
    """

    test select_deployment
    """
    class fakeMetadata:
        def __init__(self, value):
            self.name = value
    class fakeDeployment:
        def __init__(self, value):
            self.metadata = fakeMetadata(value)
    class fakeListDeployment:
        def __init__(self, value):
            self.items = [fakeDeployment(item) for item in value]
    namespace_selected = "test1"
    list_namespace.return_value = fakeListDeployment(["test1", "test2"])
    _pod_debugger = PodDebugger(_debug=True)
    result = _pod_debugger.select_deployment("waa")
    assert result == namespace_selected


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("remote_pod_debugger.pod_debugger.client.AppsV1Api.list_namespaced_daemon_set")
@patch("builtins.input", lambda *args: 'test1')
def test_pod_debugger_select_daemon_set(list_namespace, load_kube_config):
    """

    test select_daemonset
    """
    class fakeMetadata:
        def __init__(self, value):
            self.name = value
    class fakeDeployment:
        def __init__(self, value):
            self.metadata = fakeMetadata(value)
    class fakeListDeployment:
        def __init__(self, value):
            self.items = [fakeDeployment(item) for item in value]
    namespace_selected = "test1"
    list_namespace.return_value = fakeListDeployment(["test1", "test2"])
    _pod_debugger = PodDebugger(_debug=True)
    result = _pod_debugger.select_daemonset("waa")
    assert result == namespace_selected


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
def test_pod_debugger_before_script(load_kube_config):
    """

    test before_script property
    """
    _pod_debugger = PodDebugger(_debug=True, before_script="apk add git --update")
    assert _pod_debugger.before_script == 'apk add git --update && pip install  git+https://github.com/manslaughter03/python-remote-pdb'


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("builtins.input", lambda *args: 'test1')
@patch("remote_pod_debugger.pod_debugger.client.AppsV1Api.read_namespaced_deployment")
def test_pod_debugger_select_container_for_deployment(read_namespaced_deployment, load_kube_config):
    """

    test select_container for deployment
    """
    _container_name = "test1"
    _pod_debugger = PodDebugger(_debug=True)
    class container:
        def __init__(self, name: str):
            self.name = name

    returner = MagicMock()
    returner.spec.template.spec.containers = [container("test1"), container("test2")]
    read_namespaced_deployment.return_value = returner

    result = _pod_debugger.select_container("waa", "waa")
    assert result == _container_name


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("builtins.input", lambda *args: 'test1')
@patch("remote_pod_debugger.pod_debugger.client.AppsV1Api.read_namespaced_daemon_set")
def test_pod_debugger_select_container_for_daemon_set(read_namespaced_daemon_set, load_kube_config):
    """

    test select_container for daemonset
    """
    _container_name = "test1"
    _pod_debugger = PodDebugger(_debug=True)
    class container:
        def __init__(self, name: str):
            self.name = name

    returner = MagicMock()
    returner.spec.template.spec.containers = [container("test1"), container("test2")]
    read_namespaced_daemon_set.return_value = returner

    result = _pod_debugger.select_container("waa", "waa", "daemonset")
    assert result == _container_name


@pytest.mark.parametrize("object_type", [
    (
        "daemonset"
    ),
    (
        "deployment"
    ),
])
@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("builtins.input")
def test_pod_debugger_select_object_type(input, load_kube_config, object_type):
    input.return_value = object_type
    _pod_debugger = PodDebugger(_debug=True)
    result = _pod_debugger.select_object_type()
    assert result == object_type


@patch("remote_pod_debugger.pod_debugger.config.load_kube_config")
@patch("remote_pod_debugger.pod_debugger.client.AppsV1Api.read_namespaced_deployment")
def test_pod_debugger_get_container_args(read_namespaced_deployment, load_kube_config):
    """

    test select_container for deployment
    """
    _container_name = "test1"
    _args = ["--test"]
    _pod_debugger = PodDebugger(_debug=True)
    class container:
        def __init__(self, name: str, args: list):
            self.name = name
            self.args = args

    returner = MagicMock()
    returner.spec.template.spec.containers = [container("test1", _args),
                                              container("test2", _args)]
    read_namespaced_deployment.return_value = returner
    _args = _pod_debugger.get_container_args("test", "waa", _container_name)
    assert _args == _args
