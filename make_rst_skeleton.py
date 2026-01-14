# stdlib
import pathlib
from typing import List, Optional

# 3rd party
from domdf_python_tools.paths import clean_writer


class Package:

	def __init__(self, name: str, parent_path: pathlib.Path):
		self.name: str = str(name)
		self.submodules: List[Module] = []
		self.subpackages: List[Package] = []
		self.path = parent_path / name

		for filename in self.path.iterdir():
			# print(filename)
			if is_package(filename):
				if not filename.name.startswith('_'):
					self.subpackages.append(Package(filename.name, self.path))
			elif is_module(filename):
				if not filename.stem.startswith('_'):
					self.submodules.append(Module(filename.stem))

		self.submodules.sort(key=lambda m: m.name)

		# print(self.name)
		# print(self.subpackages)
		# print(self.submodules)

	def __repr__(self) -> str:
		return f"{type(self).__name__}({self.name})"

	def __str__(self) -> str:
		return self.__repr__()


class Module:

	def __init__(self, name: str):
		self.name: str = str(name)
		self.submodules: List[Module] = []
		self.subpackages: List[Package] = []

	def __repr__(self) -> str:
		return f"{type(self).__name__}({self.name})"

	def __str__(self) -> str:
		return self.__repr__()

	def make_rst(self, parent_names: List[str], directory: pathlib.Path, extras: Optional[str] = None) -> None:
		dotted_name = '.'.join(parent_names + [self.name])
		print(dotted_name)
		buf = "========="
		buf += '=' * len(dotted_name)
		buf += f"\n:mod:`~{dotted_name}`\n========="
		buf += '=' * len(dotted_name)
		buf += f"\n\n.. automodule:: {dotted_name}\n"
		buf += "\t:undoc-members:\n"
		with (directory / self.name).with_suffix(".rst").open('w', encoding="UTF-8") as fp:
			clean_writer(buf, fp)


def is_package(path: pathlib.Path) -> bool:
	return path.is_dir() and (path / "__init__.py").is_file()


def is_module(path: pathlib.Path) -> bool:
	return path.is_file() and path.suffix == ".py"


package = Package("domdf_wxpython_tools", pathlib.Path('.'))

docs_api_dir = pathlib.Path("doc-source") / "api"
if not docs_api_dir.is_dir():
	docs_api_dir.mkdir(parents=True)

print(package.name)
for subpackage in package.subpackages:
	print(f"{package.name}.{subpackage.name}")

	subpackage_dir = docs_api_dir / subpackage.name
	if not subpackage_dir.is_dir():
		subpackage_dir.mkdir(parents=True)

	with (subpackage_dir / "index.rst").open('w', encoding="UTF-8") as fp:
		dotted_name = '.'.join([package.name, subpackage_dir.name])
		print(dotted_name)
		buf = "========="
		buf += '=' * len(dotted_name)
		buf += f"\n:mod:`~{dotted_name}`\n========="
		buf += '=' * len(dotted_name)
		# buf += f"\n\n.. extras-require:: {subpackage_dir.name}\n"
		# buf += f"	:file: {subpackage_dir.name}/requirements.txt\n"
		# buf += f"	:scope: package"
		buf += f"\n\n.. toctree:: {dotted_name}\n"
		buf += "	:maxdepth: 3\n"
		buf += "	:glob:\n\n"
		buf += "\t./*"
		clean_writer(buf, fp)

	for submodule in subpackage.submodules:
		submodule.make_rst([package.name, subpackage.name], subpackage_dir, extras=subpackage_dir.name)

for submodule in package.submodules:
	submodule.make_rst([package.name], docs_api_dir)
