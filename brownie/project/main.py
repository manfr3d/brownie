#!/usr/bin/python3

import json
import shutil
import sys
import zipfile
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Iterator, KeysView, List, Optional, Set, Union

import requests

from brownie._config import (
    CONFIG,
    _get_project_config_path,
    _load_project_compiler_config,
    _load_project_config,
)
from brownie.exceptions import ProjectAlreadyLoaded, ProjectNotFound
from brownie.network.contract import ContractContainer
from brownie.project import compiler
from brownie.project.build import BUILD_KEYS, Build
from brownie.project.sources import Sources, get_hash
from brownie.utils import color

FOLDERS = ["contracts", "scripts", "reports", "tests", "build", "build/contracts"]
MIXES_URL = "https://github.com/brownie-mix/{}-mix/archive/master.zip"

_loaded_projects = []


class _ProjectBase:
    def __init__(self, name: str, contract_sources: Dict, project_path: Optional[Path]) -> None:
        self._project_path = project_path
        self._name = name
        self._sources = Sources(contract_sources)
        self._build = Build(self._sources)

    def _compile(self, sources: Dict, compiler_config: Dict, silent: bool) -> None:
        build_json = compiler.compile_and_format(
            sources,
            solc_version=compiler_config["version"],
            optimize=compiler_config["optimize"],
            runs=compiler_config["runs"],
            evm_version=compiler_config["evm_version"],
            minify=compiler_config["minify_source"],
            silent=silent,
        )
        for data in build_json.values():
            self._build._add(data)
            if self._project_path is not None:
                path = self._project_path.joinpath(f"build/contracts/{data['contractName']}.json")
                with path.open("w") as fp:
                    json.dump(data, fp, sort_keys=True, indent=2, default=sorted)

    def _create_containers(self) -> None:
        # create container objects
        self._containers: Dict = {}
        for key, data in self._build.items():
            if data["bytecode"]:
                container = ContractContainer(self, data)
                self._containers[key] = container
                setattr(self, container._name, container)

    def __getitem__(self, key: str) -> ContractContainer:
        return self._containers[key]

    def __iter__(self) -> Iterator[ContractContainer]:
        return iter(self._containers[i] for i in sorted(self._containers))

    def __len__(self) -> int:
        return len(self._containers)

    def __contains__(self, item: ContractContainer) -> bool:
        return item in self._containers

    def dict(self) -> Dict:
        return dict(self._containers)

    def keys(self) -> KeysView[Any]:
        return self._containers.keys()


class Project(_ProjectBase):

    """
    Top level dict-like container that holds data and objects related to
    a brownie project.

    Attributes:
        _project_path: Path object, absolute path to the project
        _name: Name that the project is loaded as
        _sources: project Source object
        _build: project Build object
    """

    def __init__(self, name: str, project_path: Path) -> None:
        contract_sources: Dict = {}
        for path in project_path.glob("contracts/**/*.sol"):
            if "/_" in path.as_posix():
                continue
            with path.open() as fp:
                source = fp.read()
            path_str: str = path.relative_to(project_path).as_posix()
            contract_sources[path_str] = source
        super().__init__(name, contract_sources, project_path)

        for path in list(project_path.glob("build/contracts/*.json")):
            try:
                with path.open() as fp:
                    build_json = json.load(fp)
            except json.JSONDecodeError:
                build_json = {}
            if (
                not set(BUILD_KEYS).issubset(build_json)
                or not project_path.joinpath(build_json["sourcePath"]).exists()
            ):
                path.unlink()
                continue
            self._build._add(build_json)

        self._active = False
        self.load()

    def load(self) -> None:
        """Compiles the project contracts, creates ContractContainer objects and
        populates the namespace."""
        if self._active:
            raise ProjectAlreadyLoaded("Project is already active")

        self._compiler_config = _load_project_compiler_config(self._project_path, "solc")
        solc_version = self._compiler_config["version"]
        if solc_version:
            self._compiler_config["version"] = compiler.set_solc_version(solc_version)

        # compile updated sources, update build
        changed = self._get_changed_contracts()
        self._compiler_config["version"] = solc_version
        self._compile(changed, self._compiler_config, False)
        self._create_containers()

        # add project to namespaces, apply import blackmagic
        name = self._name
        self.__all__ = list(self._containers)
        sys.modules[f"brownie.project.{name}"] = self  # type: ignore
        sys.modules["brownie.project"].__dict__[name] = self
        sys.modules["brownie.project"].__all__.append(name)  # type: ignore
        sys.modules["brownie.project"].__console_dir__.append(name)  # type: ignore
        self._namespaces = [
            sys.modules["__main__"].__dict__,
            sys.modules["brownie.project"].__dict__,
        ]
        self._active = True
        _loaded_projects.append(self)

    def _get_changed_contracts(self) -> Dict:
        changed = [i for i in self._sources.get_contract_list() if self._compare_build_json(i)]
        final = set(changed)
        for contract_name in changed:
            final.update(self._build.get_dependents(contract_name))
        for name in [i for i in final if self._build.contains(i)]:
            self._build._remove(name)
        changed_set: Set = set(self._sources.get_source_path(i) for i in final)
        return dict((i, self._sources.get(i)) for i in changed_set)

    def _compare_build_json(self, contract_name: str) -> bool:
        config = self._compiler_config
        try:
            source = self._sources.get(contract_name)
            build_json = self._build.get(contract_name)
        except KeyError:
            return True
        if build_json["sha1"] != get_hash(source, contract_name, config["minify_source"]):
            return True
        return next(
            (True for k, v in build_json["compiler"].items() if config[k] and v != config[k]), False
        )

    def _update_and_register(self, dict_: Any) -> None:
        dict_.update(self)
        self._namespaces.append(dict_)

    def __repr__(self) -> str:
        return f"<Project object '{color['string']}{self._name}{color}'>"

    def load_config(self) -> None:
        """Loads the project config file settings"""
        if isinstance(self._project_path, Path):
            _load_project_config(self._project_path)

    def close(self, raises: bool = True) -> None:
        """Removes pointers to the project's ContractContainer objects and this object."""
        if not self._active:
            if not raises:
                return
            raise ProjectNotFound("Project is not currently loaded.")

        # remove objects from namespace
        for dict_ in self._namespaces:
            for key in [
                k
                for k, v in dict_.items()
                if v == self or (k in self and v == self[k])  # type: ignore
            ]:
                del dict_[key]

        # undo black-magic
        name = self._name
        del sys.modules[f"brownie.project.{name}"]
        sys.modules["brownie.project"].__all__.remove(name)  # type: ignore
        sys.modules["brownie.project"].__console_dir__.remove(name)  # type: ignore
        self._active = False
        _loaded_projects.remove(self)

        # clear paths
        try:
            sys.path.remove(self._project_path)  # type: ignore
        except ValueError:
            pass


class TempProject(_ProjectBase):

    """Simplified Project class used to hold temporary contracts that are
    compiled via project.compile_source"""

    def __init__(self, name: str, contract_sources: Dict, compiler_config: Dict) -> None:
        super().__init__(name, contract_sources, None)
        self._compile(contract_sources, compiler_config, True)
        self._create_containers()

    def __repr__(self) -> str:
        return f"<TempProject object '{color['string']}{self._name}{color}'>"


def check_for_project(path: Union[Path, str] = ".") -> Optional[Path]:
    """Checks for a Brownie project."""
    path = Path(path).resolve()
    for folder in [path] + list(path.parents):
        if _get_project_config_path(folder):
            return folder
    return None


def get_loaded_projects() -> List:
    """Returns a list of currently loaded Project objects."""
    return _loaded_projects.copy()


def new(project_path_str: str = ".", ignore_subfolder: bool = False) -> str:
    """Initializes a new project.

    Args:
        project_path: Path to initialize the project at. If not exists, it will be created.
        ignore_subfolders: If True, will not raise if initializing in a project subfolder.

    Returns the path to the project as a string.
    """
    project_path = _new_checks(project_path_str, ignore_subfolder)
    project_path.mkdir(exist_ok=True)
    _create_folders(project_path)
    if not _get_project_config_path(project_path):
        shutil.copy(
            CONFIG["brownie_folder"].joinpath("data/config.yaml"),
            project_path.joinpath("brownie-config.yaml"),
        )
    _add_to_sys_path(project_path)
    return str(project_path)


def from_brownie_mix(
    project_name: str, project_path: Union[Path, str] = None, ignore_subfolder: bool = False
) -> str:
    """Initializes a new project via a template. Templates are downloaded from
    https://www.github.com/brownie-mix

    Args:
        project_path: Path to initialize the project at.
        ignore_subfolders: If True, will not raise if initializing in a project subfolder.

    Returns the path to the project as a string.
    """
    project_name = str(project_name).replace("-mix", "")
    url = MIXES_URL.format(project_name)
    if project_path is None:
        project_path = Path(".").joinpath(project_name)
    project_path = _new_checks(project_path, ignore_subfolder)
    if project_path.exists() and list(project_path.glob("*")):
        raise FileExistsError(f"Folder already exists - {project_path}")

    print(f"Downloading from {url}...")
    request = requests.get(url)
    with zipfile.ZipFile(BytesIO(request.content)) as zf:
        zf.extractall(str(project_path.parent))
    project_path.parent.joinpath(project_name + "-mix-master").rename(project_path)
    shutil.copy(
        CONFIG["brownie_folder"].joinpath("data/config.yaml"),
        project_path.joinpath("brownie-config.yaml"),
    )
    _add_to_sys_path(project_path)
    return str(project_path)


def _new_checks(project_path: Union[Path, str], ignore_subfolder: bool) -> Path:
    project_path = Path(project_path).resolve()
    if str(CONFIG["brownie_folder"]) in str(project_path):
        raise SystemError("Cannot make a new project inside the main brownie installation folder.")
    if not ignore_subfolder:
        check = check_for_project(project_path)
        if check and check != project_path:
            raise SystemError("Cannot make a new project in a subfolder of an existing project.")
    return project_path


def compile_source(
    source: str,
    solc_version: Optional[str] = None,
    optimize: Optional[bool] = True,
    runs: Optional[int] = 200,
    evm_version: Optional[int] = None,
) -> "TempProject":
    """Compiles the given source code string and returns a TempProject container with
    the ContractContainer instances."""

    compiler_config = {
        "version": solc_version,
        "optimize": optimize,
        "runs": runs,
        "evm_version": evm_version,
        "minify_source": False,
    }
    return TempProject("TempProject", {"<stdin>": source}, compiler_config)


def load(project_path: Union[Path, str, None] = None, name: Optional[str] = None) -> "Project":
    """Loads a project and instantiates various related objects.

    Args:
        project_path: Path of the project to load. If None, will attempt to
                      locate a project using check_for_project()
        name: Name to assign to the project. If None, the name is generated
              from the name of the project folder

    Returns a Project object.
    """
    # checks
    if project_path is None:
        project_path = check_for_project(".")
    if not project_path or not _get_project_config_path(Path(project_path)):
        raise ProjectNotFound("Could not find Brownie project")

    project_path = Path(project_path).resolve()
    if name is None:
        name = project_path.name
        if not name.lower().endswith("project"):
            name += " project"
        name = "".join(i for i in name.title() if i.isalpha())
    if next((True for i in _loaded_projects if i._name == name), False):
        raise ProjectAlreadyLoaded("There is already a project loaded with this name")

    # paths
    _create_folders(project_path)
    _add_to_sys_path(project_path)

    # load sources and build
    return Project(name, project_path)


def _create_folders(project_path: Path) -> None:
    for path in [i for i in FOLDERS]:
        project_path.joinpath(path).mkdir(exist_ok=True)


def _add_to_sys_path(project_path: Path) -> None:
    project_path_string = str(project_path)
    if project_path_string in sys.path:
        return
    sys.path.insert(0, project_path_string)
