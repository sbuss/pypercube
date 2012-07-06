import unittest

from pypercube.filters import Filter
from pypercube.filters import EQ
from pypercube.filters import LT
from pypercube.filters import LE
from pypercube.filters import GT
from pypercube.filters import GE
from pypercube.filters import NE
from pypercube.filters import RE
from pypercube.filters import IN
from pypercube.filters import StartsWith
from pypercube.filters import EndsWith


class TestFilter(unittest.TestCase):
    def test_equality(self):
        f1 = Filter('eq', 'name', 'test')
        f2 = EQ('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('lt', 'name', 'test')
        self.assertNotEqual(f1, f2)
        f2 = LT('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('le', 'name', 'test')
        f2 = LE('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('gt', 'name', 'test')
        f2 = GT('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('ge', 'name', 'test')
        f2 = GE('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('ne', 'name', 'test')
        f2 = NE('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('re', 'name', 'test')
        f2 = RE('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('in', 'name', ['t', 'e', 's', 't'])
        f2 = IN('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('in', 'name', ['test'])
        f2 = IN('name', ['test'])
        self.assertEqual(f1, f2)
        f1 = Filter('re', 'name', '^test')
        f2 = StartsWith('name', 'test')
        self.assertEqual(f1, f2)
        f1 = Filter('re', 'name', '.*test$')
        f2 = EndsWith('name', 'test')
        self.assertEqual(f1, f2)

    def test_starts_with(self):
        f = StartsWith('name', 'test')
        self.assertEqual("%s" % f, '.re(name, "^test")')

    def test_ends_with(self):
        f = EndsWith('name', 'test')
        self.assertEqual("%s" % f, '.re(name, ".*test$")')

    def test_re(self):
        # FIXME: Regular expressions are broken
        f = RE('name', r"\s+([A-Za-z0-9]+)")
        self.assertEqual("%s" % f, r'.re(name, "\s+([A-Za-z0-9]+)")')

    def test_in(self):
        f = IN('name', ['a', 'b', 'c'])
        self.assertEqual("%s" % f, '.in(name, ["a", "b", "c"])')
