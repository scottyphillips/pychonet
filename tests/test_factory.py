import importlib
import inspect
import pkgutil
import unittest
from collections import defaultdict
from types import SimpleNamespace

import pychonet
from pychonet.EchonetInstance import EchonetInstance
from pychonet.lib.eojx import EOJX_CLASS


def device_classes():
    for info in pkgutil.iter_modules(pychonet.__path__):
        if info.ispkg:
            continue
        module = importlib.import_module(f"pychonet.{info.name}")
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if (
                cls.__module__ == module.__name__
                and issubclass(cls, EchonetInstance)
                and cls is not EchonetInstance
            ):
                yield cls


class TestFactory(unittest.TestCase):
    def test_all_device_classes_are_exported_and_registered(self):
        server = SimpleNamespace(
            _state={
                "device": {
                    "instances": defaultdict(
                        lambda: defaultdict(lambda: defaultdict(dict))
                    )
                }
            }
        )
        registered = set()
        for group, codes in EOJX_CLASS.items():
            for code in codes:
                created = pychonet.Factory("device", server, group, code, 0x02)
                registered.add(type(created))
                self.assertEqual((created._eojgc, created._eojcc), (group, code))
                self.assertEqual(created._eojci, 0x02)
        for cls in device_classes():
            with self.subTest(device=cls.__name__):
                self.assertIs(getattr(pychonet, cls.__name__, None), cls)
                self.assertIn(cls, registered)

    def test_unknown_device_uses_generic_instance(self):
        server = SimpleNamespace(
            _state={"device": {"instances": {0x0F: {0xFF: {0x01: {}}}}}}
        )
        device = pychonet.Factory("device", server, 0x0F, 0xFF)
        self.assertIs(type(device), EchonetInstance)
