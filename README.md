# Remote pod debugger

Remote python microservice debugger. This app will patch deployment in order to override container entrypoint.

## Install package:

* Clone this repository
* Install python package: `pip install .`

## Usage:


```bash
remote-pod-debugger
```

Available options:

```bash
usage: Remote pod debugger [-h] [--namespace NAMESPACE] [--host HOST] [--port PORT] [--entrypoint ENTRYPOINT] [--image-name IMAGE_NAME] [--pdb-command PDB_COMMAND] [--backup] [--debug]
                           [--before-script BEFORE_SCRIPT] [--deployment DEPLOYMENT] [--daemonset DAEMONSET] [--container CONTAINER]

options:
  -h, --help            show this help message and exit
  --namespace NAMESPACE, -n NAMESPACE
                        K8s namespace
  --host HOST           Remote host debugger
  --port PORT, -p PORT  Remote port debugger
  --entrypoint ENTRYPOINT, -e ENTRYPOINT
                        Python entrypoint, can be a file or a module (ex: -m http.server)
  --image-name IMAGE_NAME, -i IMAGE_NAME
                        Docker image name to replace
  --pdb-command PDB_COMMAND, -c PDB_COMMAND
                        PDB extra command pass to debugger at startup
  --backup              Backup deployment or daemonset before patch
  --debug, -d           Activate debug
  --before-script BEFORE_SCRIPT
                        Append script before pdb entrypoint
  --deployment DEPLOYMENT
                        Set deployment name to patch
  --daemonset DAEMONSET
                        Set daemonset name to patch
  --container CONTAINER
                        Container name to patch
```
