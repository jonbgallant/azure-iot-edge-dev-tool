"""
This module provides interfaces to manipulate IoT Edge deployment manifest (deployment.json)
and deployment manifest template (deployment.template.json)
"""

import json
import sys


class DeploymentManifest:
    def __init__(self, output, path, is_template):
        self.output = output
        try:
            self.path = path
            self.json = json.load(open(path))
            self.is_template = is_template
        except FileNotFoundError:
            if is_template:
                self.output.error('Deployment manifest template file "{0}" not found'.format(path))
            else:
                self.output.error('Deployment manifest file "{0}" not found'.format(path))
            sys.exit()

    def add_module_template(self, module_name):
        """Add a module template to the deployment manifest with amd64 as the default platform"""
        new_module = """{
            "version": "1.0",
            "type": "docker",
            "status": "running",
            "restartPolicy": "always",
            "settings": {
              "image": \"{MODULES.""" + module_name + """.amd64}\",
              "createOptions": ""
            }
        }"""

        self.json["moduleContent"]["$edgeAgent"]["properties.desired"]["modules"][module_name] = json.loads(new_module)

    def save(self):
        """Dump the JSON to the disk"""
        with open(self.path, "w") as deployment_manifest:
            json.dump(self.json, deployment_manifest, indent=2)
