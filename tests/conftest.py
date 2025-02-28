#!/usr/bin/python3

import itertools
import json
import os
import shutil
from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

import brownie
from brownie._config import ARGV

pytest_plugins = "pytester"


# travis cannot call github ethereum/solidity API, so this method is patched
def pytest_sessionstart():
    monkeypatch_session = MonkeyPatch()
    monkeypatch_session.setattr(
        "solcx.get_available_solc_versions",
        lambda: ["v0.5.10", "v0.5.9", "v0.5.8", "v0.5.7", "v0.4.25", "v0.4.24", "v0.4.22"],
    )


def pytest_addoption(parser):
    parser.addoption("--mix-tests", action="store_true", help="Runs brownie mix tests")
    parser.addoption(
        "--evm-tests", action="store_true", help="Runs EVM tests (coverage evaluation)"
    )
    parser.addoption("--skip-regular", action="store_true", help="Skips regular tests")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--evm-tests"):
        evm_skip = pytest.mark.skip(reason="Use --evm-tests to run")
        for i in [i for i in items if "evmtester" in i.fixturenames]:
            i.add_marker(evm_skip)
    if not config.getoption("--mix-tests"):
        mix_skip = pytest.mark.skip(reason="Use --evm-tests to run")
        for i in [i for i in items if "browniemix" in i.fixturenames]:
            i.add_marker(mix_skip)
    if config.getoption("--skip-regular"):
        regular_skip = pytest.mark.skip(reason="--skip-regular")
        for i in [
            i
            for i in items
            if "browniemix" not in i.fixturenames and "evmtester" not in i.fixturenames
        ]:
            i.add_marker(regular_skip)


# auto-parametrize the evmtester fixture
def pytest_generate_tests(metafunc):
    if "evmtester" in metafunc.fixturenames:
        metafunc.parametrize(
            "evmtester",
            itertools.product(
                ["0.4.22", "0.4.25", "0.5.0", "0.5.10"],
                [0, 200, 10000],
                ["byzantium", "constantinople"],
            ),
            indirect=True,
        )


@pytest.fixture(scope="session")
def _project_factory(tmp_path_factory):
    path = tmp_path_factory.mktemp("base")
    path.rmdir()
    shutil.copytree("tests/brownie-test-project", path)
    shutil.copyfile("brownie/data/config.yaml", path.joinpath("brownie-config.yaml"))
    p = brownie.project.load(path, "TestProject")
    p.close()
    return path


def _copy_all(src_folder, dest_folder):
    for path in Path(src_folder).glob("*"):
        dest_path = Path(dest_folder).joinpath(path.name)
        if path.is_dir():
            shutil.copytree(path, dest_path)
        else:
            shutil.copy(path, dest_path)


# project fixtures

# creates a temporary folder and sets it as the working directory
@pytest.fixture
def project(tmp_path):
    original_path = os.getcwd()
    os.chdir(tmp_path)
    yield brownie.project
    os.chdir(original_path)
    for p in brownie.project.get_loaded_projects():
        p.close(False)


# copies the tester project into a temporary folder, loads it, and yields a Project object
@pytest.fixture
def testproject(_project_factory, project, tmp_path):
    _copy_all(_project_factory, tmp_path)
    return project.load(tmp_path, "TestProject")


@pytest.fixture
def otherproject(testproject):
    return brownie.project.load(testproject._project_path, "OtherProject")


# yields a deployed EVMTester contract
# automatically parametrized with multiple compiler versions and settings
@pytest.fixture
def evmtester(_project_factory, project, tmp_path, accounts, request):
    solc_version, runs, evm_version = request.param
    tmp_path.joinpath("contracts").mkdir()
    shutil.copyfile(
        _project_factory.joinpath("contracts/EVMTester.sol"),
        tmp_path.joinpath("contracts/EVMTester.sol"),
    )
    conf_json = brownie._config._load_config(_project_factory.joinpath("brownie-config.yaml"))
    conf_json["compiler"]["solc"].update(
        {"version": solc_version, "optimize": runs > 0, "runs": runs, "evm_version": evm_version}
    )
    with tmp_path.joinpath("brownie-config.yaml").open("w") as fp:
        json.dump(conf_json, fp)
    p = project.load(tmp_path, "EVMProject")
    return p.EVMTester.deploy({"from": accounts[0]})


@pytest.fixture
def plugintesterbase(project, testdir, monkeypatch):
    brownie.test.coverage.clear()
    brownie.network.connect()
    monkeypatch.setattr("brownie.network.connect", lambda k: None)
    testdir.plugins.extend(["pytest-brownie", "pytest-cov"])
    yield testdir
    brownie.network.disconnect()


# setup for pytest-brownie plugin testing
@pytest.fixture
def plugintester(_project_factory, plugintesterbase, request):
    _copy_all(_project_factory, plugintesterbase.tmpdir)
    test_source = getattr(request.module, "test_source", None)
    if test_source:
        plugintesterbase.makepyfile(test_source)
    yield plugintesterbase


# launches and connects to ganache, yields the brownie.network module
@pytest.fixture
def devnetwork(network, rpc):
    if brownie.network.is_connected():
        brownie.network.disconnect(False)
    brownie.network.connect("development")
    yield brownie.network
    if rpc.is_active():
        rpc.reset()


# brownie object fixtures


@pytest.fixture
def accounts(devnetwork):
    return brownie.network.accounts


@pytest.fixture
def history():
    return brownie.network.history


@pytest.fixture
def network():
    yield brownie.network
    if brownie.network.is_connected():
        brownie.network.disconnect(False)


@pytest.fixture
def rpc():
    return brownie.network.rpc


@pytest.fixture
def web3():
    return brownie.network.web3


# configuration fixtures
# changes to config or argv are reverted during teardown


@pytest.fixture
def config():
    initial = brownie.config._copy()
    yield brownie.config
    brownie.config._unlock()
    brownie.config.clear()
    brownie.config.update(initial)
    brownie.config._lock()


@pytest.fixture
def argv():
    initial = {}
    initial.update(ARGV)
    yield ARGV
    ARGV.clear()
    ARGV.update(initial)


# cli mode fixtures


@pytest.fixture
def console_mode(argv):
    argv["cli"] = "console"


@pytest.fixture
def test_mode(argv):
    argv["cli"] = "test"


@pytest.fixture
def coverage_mode(argv, test_mode):
    brownie.test.coverage.clear()
    argv["coverage"] = True
    argv["always_transact"] = True


# contract fixtures


@pytest.fixture
def BrownieTester(testproject, devnetwork):
    return testproject.BrownieTester


@pytest.fixture
def ExternalCallTester(testproject, devnetwork):
    return testproject.ExternalCallTester


@pytest.fixture
def tester(BrownieTester, accounts):
    return BrownieTester.deploy(True, {"from": accounts[0]})


@pytest.fixture
def ext_tester(ExternalCallTester, accounts):
    return ExternalCallTester.deploy({"from": accounts[0]})
