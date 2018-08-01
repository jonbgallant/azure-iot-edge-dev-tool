from .dockercls import Docker
from .modules import Modules


class iotedgehubdev:
    def __init__(self, envvars, output, utility):
        self.envvars = envvars
        self.output = output
        self.utility = utility

    def setup(self):
        self.output.header("Setting Up Edge Simulator")
        self.envvars.verify_envvar_has_val("DEVICE_CONNECTION_STRING", self.envvars.DEVICE_CONNECTION_STRING)
        self.utility.exe_proc("iotedgehubdev setup -c {0}".format(self.envvars.DEVICE_CONNECTION_STRING).split())

    def start_single(self, inputs):
        self.output.header("Starting Edge Simulator in Single Mode")
        self.utility.call_proc("iotedgehubdev start -i {0}".format(inputs).split())

    def start_solution(self, verbose=True, no_build=False):
        if not no_build:
            dock = Docker(self.envvars, self.utility, self.output)
            mod = Modules(self.envvars, self.utility, self.output, dock)
            mod.build()

        self.output.header("Starting Edge Simulator in Solution Mode")
        self.utility.call_proc("iotedgehubdev start -d {0} {1}".format(self.envvars.DEPLOYMENT_CONFIG_FILE_PATH, "-v" if verbose else "").split())

    def stop(self):
        self.output.header("Stopping Edge Simulator")
        self.utility.exe_proc("iotedgehubdev stop".split())
