import sys
import time
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ExtensionFileLoader, FileFinder
from importlib.util import spec_from_loader

from ._logger import logger
from ._version import __version__

_tariff_sheet: dict[str] = {}
_cache = set()


def set_tarrif(name: str, rate: int):
    _tariff_sheet[name] = rate


class TariffFinder(MetaPathFinder):
    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if fullname not in _tariff_sheet:
            return None
        for finder in sys.meta_path:
            if finder is TariffFinder:
                continue
            spec = finder.find_spec(fullname, path, target)
            if spec is not None:
                spec.loader = TariffLoader(spec.loader)
                return spec
        return None


class TariffLoader(Loader):
    def __init__(self, ori_loader):
        self._ori_loader = ori_loader
        self._start_time = time.time()

    def create_module(self, spec):
        return self._ori_loader.create_module(spec)

    def exec_module(self, module):
        self._ori_loader.exec_module(module)
        if module.__name__ not in _tariff_sheet:
            return
        # apply import tariff
        duration = time.time() - self._start_time
        mod_names = module.__name__.split(".")
        current_mod_name = ""
        acc_rate = 0
        for idx, mod_name in enumerate(mod_names):
            current_mod_name += mod_name if idx == 0 else f".{mod_name}"
            acc_rate += _tariff_sheet.get(current_mod_name, 0)
            if current_mod_name in _cache:
                continue
            tex = duration * (1 + acc_rate / 100)
            logger.info(
                "Import tariff for %s is %s%%, sleeping for %0.4fs",
                current_mod_name,
                acc_rate,
                tex,
            )
            time.sleep(tex)
            _cache.add(current_mod_name)


sys.meta_path.insert(0, TariffFinder)
