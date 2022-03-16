"""

remote pod debugger

"""
import argparse

from remote_pod_debugger.completer import activate_history
from remote_pod_debugger.pod_debugger import PodDebugger
from remote_pod_debugger.utils import info, debug


def main():  # pragma: no cover
    """

    remote pod debugger entrypoint
    """
    _parser = argparse.ArgumentParser("Remote pod debugger")
    _parser.add_argument("--namespace", "-n", help="K8s namespace")
    _parser.add_argument("--host", help="Remote host debugger")
    _parser.add_argument("--port", "-p", type=int, help="Remote port debugger")
    _parser.add_argument(
        "--entrypoint",
        "-e",
        help="Python entrypoint, can be a file or a module (ex: -m http.server)",
    )
    _parser.add_argument("--image-name", "-i", help="Docker image name to replace")
    _parser.add_argument(
        "--pdb-command",
        "-c",
        action="append",
        default=[],
        help="PDB extra command pass to debugger at startup",
    )
    _parser.add_argument(
        "--backup",
        action="store_true",
        default=False,
        help="Backup deployment or daemonset before patch"
    )
    _parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        default=False,
        help="Activate debug",
    )
    _parser.add_argument(
        "--before-script",
        default=None,
        help="Append script before pdb entrypoint"
    )
    _parser.add_argument(
        "--deployment",
        default=None,
        help="Set deployment name to patch"
    )
    _parser.add_argument(
        "--daemonset",
        default=None,
        help="Set daemonset name to patch"
    )
    _parser.add_argument(
        "--container",
        default=None,
        help="Container name to patch"
    )
    _args = _parser.parse_args()

    activate_history()

    info("Welcome to remote pod debugger!")
    _pod_debugger = PodDebugger(before_script=_args.before_script, _debug=_args.debug)
    _namespace = _args.namespace
    if not _namespace:
        _namespace = _pod_debugger.select_namespace()
    _object_name = None
    _object_type = None
    if _args.deployment:
        _object_name = _args.deployment
        _object_type = "deployment"
    elif _args.daemonset:
        _object_name = _args.daemonset
        _object_type = "daemonset"

    if not _object_type:
        _object_type = _pod_debugger.select_object_type()
    if not _object_name and _object_type == "deployment":
        _object_name = _pod_debugger.select_deployment(_namespace)
    elif not _object_name and _object_type == "daemonset":
        _object_name = _pod_debugger.select_daemonset(_namespace)

    if not _object_name:
        raise Exception("Can't find object to patch")

    if _args.backup:
        _backup_filepath = f"/tmp/{_object_name}.yaml"
        with open(_backup_filepath, "w", encoding="utf-8") as _file:
            _pod_debugger.backup(_object_name, _namespace, _file, _object_type)
        info(f"Backup deployment {_object_name} to {_backup_filepath}")

    _container_name = (
        _pod_debugger.select_container(_object_name, _namespace, _object_type)
        if not _args.container
        else _args.container
    )

    _host = input("Host of debugger?\n> ") if not _args.host else _args.host
    _port = input("Port of debugger?\n> ") if not _args.port else _args.port
    _entrypoint = (
        input("Python entrypoint?\n> ") if not _args.entrypoint else _args.entrypoint
    )
    #   _existing_container_args = _pod_debugger.get_container_args(_deployment,
    #                                                              _namespace,
    #                                                              _container_name)
    #   if _existing_container_args:
    #       _entrypoint += " ".join(_existing_container_args)
    _image_name = input("Image name?\n> ") if not _args.image_name else _args.image_name
    _pdb_commands = _args.pdb_command
    if not _pdb_commands:
        end = False
        while not end:
            _pdb_cmd_tmp = input('Add pdb command at startup, else enter "stop"?\n> ')
            if _pdb_cmd_tmp == "stop":
                break
            _pdb_commands.append(_pdb_cmd_tmp)
    _patch_result = _pod_debugger.patch(
        _object_name,
        _namespace,
        _host,
        int(_port),
        _entrypoint,
        _container_name,
        _image_name,
        _args.pdb_command,
        _object_type,
    )
    if _args.debug:
        debug(f"Patch result: {_patch_result}")
    info(f"Success patch {_object_name} {_object_type} on {_namespace} namespace.")


if __name__ == "__main__":
    main()
