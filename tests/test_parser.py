# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test signature parsing.
"""

# isort: STDLIB
import unittest
from os import environ, sys

# isort: THIRDPARTY
import pyparsing
from hypothesis import given, settings

# isort: FIRSTPARTY
from hs_dbus_signature import dbus_signatures

# isort: LOCAL
from dbus_signature_pyparsing import Parser

settings.register_profile("tracing", deadline=None)
if sys.gettrace() is not None or environ.get("TRAVIS") is not None:
    settings.load_profile("tracing")


class ParseTestCase(unittest.TestCase):
    """
    Test parsing various signatures.
    """

    _PARSER = Parser()

    @given(dbus_signatures())
    @settings(max_examples=100)
    def test_parsing(self, signature):
        """
        Test that parsing is always succesful on valid strings.
        """
        self.assertIsNotNone(self._PARSER.PARSER.parseString(signature, parseAll=True))

    def test_exception(self):
        """
        Test failure on some invalid strings.
        """
        parser = self._PARSER.PARSER
        with self.assertRaises(pyparsing.ParseException):
            parser.parseString("a", parseAll=True)
        with self.assertRaises(pyparsing.ParseException):
            parser.parseString("()", parseAll=True)
        with self.assertRaises(pyparsing.ParseException):
            parser.parseString("{}", parseAll=True)
        with self.assertRaises(pyparsing.ParseException):
            parser.parseString("{b}", parseAll=True)
        with self.assertRaises(pyparsing.ParseException):
            parser.parseString("a{b}", parseAll=True)
        with self.assertRaises(pyparsing.ParseException):
            parser.parseString("a{}", parseAll=True)
        with self.assertRaises(pyparsing.ParseException):
            parser.parseString("a{byy}", parseAll=True)
        with self.assertRaises(pyparsing.ParseException):
            parser.parseString("a{ayy}", parseAll=True)
