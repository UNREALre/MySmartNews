# -*- coding: utf-8 -*-
"""
Implementation of Object Factory for Parsers and so on.
"""

from smart_parser.parsers.Shazoo import ShazooBuilder
from smart_parser.parsers.Dtf import DtfBuilder
from smart_parser.parsers.Rbc import RbcBuilder


class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key, builder):
        self._builders[key] = builder

    def create(self, key, **kwargs):
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)


factory = ObjectFactory()
factory.register_builder('SHAZ', ShazooBuilder())
factory.register_builder('DTF', DtfBuilder())
factory.register_builder('RBC_POL', RbcBuilder())
factory.register_builder('RBC_ECO', RbcBuilder())
