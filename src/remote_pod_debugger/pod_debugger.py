"""

Pod debugger
"""
from io import IOBase
import readline
from typing import Union

from kubernetes import client, config
import yaml

from remote_pod_debugger.utils import info, debug, warning
from remote_pod_debugger.completer import Completer


REMOTE_PDB_PACKAGE = "git+https://github.com/manslaughter03/python-remote-pdb"
OBJECT_TYPES = ["deployment", "daemonset"]


class PodDebugger:
    """

    PodDebugger class
    """

    def __init__(
        self,
        remote_pdb_package: str = REMOTE_PDB_PACKAGE,
        before_script: str = None,
        _debug: bool = False,
    ):
        """

        PodDebugger constructor

        Args:
            remote_pdb_package (str): Remote pdb package (default: REMOTE_PDB_PACKAGE)
            before_script (str): script to append in container args (default: None)
            _debug (bool): debug flag (default: False)
        """
        config.load_kube_config()
        self._apps_v1_api = client.AppsV1Api()
        self._core_v1_api = client.CoreV1Api()
        self._debug = _debug
        self._remote_pdb_package = remote_pdb_package
        self._before_script = before_script

    @property
    def remote_pdb_package(self) -> str:
        """

        remote_pdb_package property
        Returns:
            str: remote_pdb_package property
        """
        return self._remote_pdb_package

    @property
    def debug(self) -> bool:
        """

        debug property
        Returns:
            bool: debug property
        """
        return self._debug

    @property
    def before_script(self) -> str:
        """

        before_script property

        Returns:
            str: before_script property
        """
        if self._before_script:
            return self._before_script + f" && pip install {self.remote_pdb_package}"
        return f"pip install {self.remote_pdb_package}"

    @staticmethod
    def _select(msg: str, options: list) -> str:
        """

        Args:
            msg (str): Message before prompt
            options (list): List of option
        Returns:
            str: Option selected
        """
        _selected = False
        readline.set_completer(Completer(options).complete)
        while not _selected:
            _option = input(f"{msg}?\n> ")
            if _option not in options:
                warning(f"{_option} option not found, value available ({options})")
                continue
            break
        return _option

    def select_object_type(self) -> str:
        """

        List object type, and prompt in order to select one
        object type.
        Returns:
            str: object type
        """
        for _item in OBJECT_TYPES:
            print(_item)
        return self._select("Select object type", OBJECT_TYPES)

    def select_namespace(self) -> str:
        """

        List namespace, and prompt in order to select one
        namespace, return namespace name.
        Returns:
            str: namespace name
        """
        _results = self._core_v1_api.list_namespace()
        info("# List of existing namespaces")
        _namespaces = [item.metadata.name for item in _results.items]
        for _item in _namespaces:
            print(_item)
        return self._select("Select one namespace", _namespaces)

    def select_daemonset(self, namespace: str) -> str:
        """

        List daemonset of namespace, and prompt in order to select one
        daemonset, return daemonset name.
        Args:
            namespace (str): namespace name
        Returns:
            str: daemonset name
        """
        _results = self._apps_v1_api.list_namespaced_daemon_set(namespace=namespace)
        _daemonsets = [item.metadata.name for item in _results.items]
        info(f"# List of existing daemonset of namespace {namespace}")
        for _item in _daemonsets:
            print(_item)
        return self._select("Wich daemonset you want to patch", _daemonsets)

    def select_deployment(self, namespace: str) -> str:
        """

        List deployment of namespace, and prompt in order to select one
        deployment, return deployment name.
        Args:
            namespace (str): Namespace name
        Returns:
            str: deployment name
        """
        _results = self._apps_v1_api.list_namespaced_deployment(namespace=namespace)
        _deployments = [item.metadata.name for item in _results.items]
        info(f"# List of existing deployments of namespace {namespace}")
        for _item in _deployments:
            print(_item)
        return self._select("Wich deployment you want to patch", _deployments)

    def get_container_args(
        self, name: str, namespace: str, container_name: str
    ) -> list:
        """

        get container args
        Args:
            name (str): deployment name
            namespace (str): namespace name
            container_name (str): container name
        Return:
            list: list of container args
        """
        _result = self._apps_v1_api.read_namespaced_deployment(name, namespace)
        for _item in _result.spec.template.spec.containers:
            if _item.name == container_name:
                return _item.args

        return []

    def select_container(
        self, name: str, namespace: str, _object: str = "deployment"
    ) -> str:
        """

        List container of deployment and prompt in order to select one of them
        Args:
            namespace (str): namespace name
            name (str): deployment name
        Returns:
            str: container name
        """
        _results = None
        if _object == "deployment":
            _results = self._apps_v1_api.read_namespaced_deployment(
                name=name, namespace=namespace
            )
        elif _object == "daemonset":
            _results = self._apps_v1_api.read_namespaced_daemon_set(
                name=name, namespace=namespace
            )
        if not _results:
            raise Exception("Can't find container")
        _containers = [item.name for item in _results.spec.template.spec.containers]
        info(f"# List of containers of deployment {name} of namespace {namespace}")
        for _item in _containers:
            print(_item)
        return self._select("Wich container you want to patch", _containers)

    def backup(
        self, name: str, namespace: str, file: IOBase, object_type: str = "deployment"
    ):
        """

        backup deployment to file
        Args:
            name (str): deployment name
            namespace (str): namespace name
            filepath (str): filepath
        """
        _data = None
        if object_type == "deployment":
            _data = self._apps_v1_api.read_namespaced_deployment(name, namespace)
        if object_type == "daemonset":
            _data = self._apps_v1_api.read_namespaced_daemon_set(name, namespace)
        if not _data:
            raise Exception(f"Can't find {name} {object_type}")
        yaml.dump(
            client.ApiClient().sanitize_for_serialization(_data),
            file,
            default_flow_style=False,
        )

    def container_args(
        self, host: str, port: int, pdb_extra: str, entrypoint: str
    ) -> str:
        """

        return container args
        Args:
            host (str): Remote host
            port (int): Remote port
            pdb_extra (str): Pdb extra commands
            entrypoint (str): python entrypoint
        Returns:
            str: container args
        """
        return (
            self.before_script + f" && python -m remote_pdb --host {host} --port {port}"
            f" {pdb_extra} --reverse {entrypoint}"
        )

    def patch(
        self,
        name: str,
        namespace: str,
        host: str,
        port: int,
        entrypoint: str,
        container_name: str,
        image_name: str = None,
        pdb_commands: list = None,
        object_name: str = "deployment",
    ) -> Union[client.models.V1Deployment, client.models.V1DaemonSet]:
        """

        Patch container of a deployment, replace cmd and args container,
        you can update image name too.
        Args:
            name (str): deployment name
            namespace (str): namespace name
            host (str): remote host debugger
            port (int): remote port debugger
            entrypoint (str): python file or module entrypoint
            container_name (str): container name
            image_name (str): docker image name
            pdb_commands (list): pdb command list
        Returns:
           Union[client.models.V1Deployment, client.models.V1DaemonSet]: return deployment or daemonset patched
        """
        _pdb_extra = (
            " ".join([f"-c {_item}" for _item in pdb_commands]) if pdb_commands else ""
        )
        _container_args = self.container_args(host, port, _pdb_extra, entrypoint)
        _body = {
            "spec": {
                "template": {
                    "spec": {
                        "containers": [
                            {
                                "name": container_name,
                                "image": image_name,
                                "command": ["sh"],
                                "args": ["-c", _container_args],
                            }
                        ]
                    }
                }
            }
        }
        if self.debug:
            debug(f"Patch deployment {name} of {namespace} with {_body}")
        _result = None
        if object_name == "deployment":
            _result = self._apps_v1_api.patch_namespaced_deployment(
                name, namespace, _body
            )
        elif object_name == "daemonset":
            _result = self._apps_v1_api.patch_namespaced_daemon_set(
                name, namespace, _body
            )

        return _result
