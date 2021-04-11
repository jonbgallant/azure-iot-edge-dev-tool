## TODO:
## 1) Test create options
## 2) Test environment variables for layered deployments
## 3) Test user-defined module
## 4) Test invalid cases for all current and planned tests

import json
import os

import pytest

from iotedgedev.layered_deploymentmanifest import LayeredDeploymentManifest
from iotedgedev.envvars import EnvVars
from iotedgedev.output import Output
from iotedgedev.utility import Utility

from .utility import assert_list_equal

pytestmark = pytest.mark.unit

tests_dir = os.path.join(os.getcwd(), "tests")
test_assets_dir = os.path.join(tests_dir, "assets")
test_file_1 = os.path.join(test_assets_dir, "layered_deployment.template_1.json")
test_file_2 = os.path.join(test_assets_dir, "layered_deployment.template_2.json")


@pytest.fixture
def layered_deployment_manifest():
    output = Output()
    envvars = EnvVars(output)
    envvars.load()
    utility = Utility(envvars, output)

    def _layered_deployment_manifest(path):
        return LayeredDeploymentManifest(envvars, output, utility, path, True)

    return _layered_deployment_manifest

# test routes are set to default upstream
def test_get_desired_property(deployment_manifest):
    deployment_manifest = layered_deployment_manifest(test_file_1)
    props = deployment_manifest.get_desired_property("$edgeHub", "routes.upstream")
    assert props == "FROM /messages/* INTO $upstream"

# try to get type of nonexistent module
def test_get_desired_property_nonexistent_module(deployment_manifest):
    deployment_manifest = layered_deployment_manifest(test_file_1)
    with pytest.raises(KeyError):
        deployment_manifest.get_desired_property("nonexistentModule", "type")

# try to get nonexistent property of $edgeHub
def test_get_desired_property_nonexistent_prop(deployment_manifest):
    deployment_manifest = layered_deployment_manifest(test_file_1)
    with pytest.raises(KeyError):
        deployment_manifest.get_desired_property("$edgeHub", "nonexistentProp")

# test user-defined modules are present
def test_get_user_modules(deployment_manifest):
    deployment_manifest = layered_deployment_manifest(test_file_1)
    user_modules = list(deployment_manifest.get_user_modules().keys())
    assert_list_equal(user_modules, ["LayeredDeploymentTempSensor", "LayeredDeploymentCSharpModule", "LayeredDeploymentCSharpFunction"])

# test all modules are present
def test_get_all_modules(deployment_manifest):
    deployment_manifest = layered_deployment_manifest(test_file_1)
    system_modules = list(deployment_manifest.get_all_modules().keys())
    assert_list_equal(user_modules, ["LayeredDeploymentTempSensor", "LayeredDeploymentCSharpModule", "LayeredDeploymentCSharpFunction"])

# test adding a new module
def test_add_module_template(deployment_manifest):
    deployment_manifest = layered_deployment_manifest(test_file_1)
    deployment_manifest.add_module_template("LayeredDeploymentCSharpModule2")
    with open(test_file_2, "r") as expected:
        assert deployment_manifest.json == json.load(expected)

# confirm image placeholders expand to proper local CR address
def test_expand_image_placeholders(deployment_manifest):
    deployment_manifest = layered_deployment_manifest(test_file_1)
    deployment_manifest.expand_image_placeholders({"LayeredDeploymentCSharpModule": "localhost:5000/csharpmodule:0.0.1-amd64"})
    assert deployment_manifest.json["modulesContent"]["$edgeAgent"]["properties.desired"]["modules"]["LayeredDeploymentCSharpModule"]["settings"]["image"] == "localhost:5000/csharpmodule:0.0.1-amd64"
