"""

remote pod debugger

"""
import argparse

from remote_pod_debugger.completer import activate_history
from remote_pod_debugger.pod_debugger import PodDebugger
from remote_pod_debugger.utils import info


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
        "--extra-pip-args",
        default=None,
        help="Append extra pip args to install remote_pdb"
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
    try:
        _pod_debugger.run(_args)
    except KeyboardInterrupt:
        info("Goodbye!")



if __name__ == "__main__":
    main()
