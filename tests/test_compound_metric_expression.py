import unittest

from pypercube.expression import CompoundMetricExpression
from pypercube.expression import EventExpression
from pypercube.expression import Max
from pypercube.expression import MetricExpression
from pypercube.expression import Min
from pypercube.expression import Sum


class TestCompoundMetricExpressions(unittest.TestCase):
    def setUp(self):
        self.e = EventExpression('test', 'ing')
        self.sum = Sum(self.e)
        self.max = Max(self.e)
        self.min = Min(self.e)

    def test_addition(self):
        self.assertEqual("%s" % (self.sum + self.min),
                "(sum(test(ing)) + min(test(ing)))")
        self.assertEqual("%s" % (self.sum + self.min + self.max),
                "((sum(test(ing)) + min(test(ing))) + max(test(ing)))")
        self.assertEqual("%s" %
                ((self.sum + self.min) + (self.max + self.max)),
                "((sum(test(ing)) + min(test(ing))) + "\
                        "(max(test(ing)) + max(test(ing))))")

    def test_subtraction(self):
        self.assertEqual("%s" % (self.sum - self.min - self.max),
                "((sum(test(ing)) - min(test(ing))) - max(test(ing)))")
        self.assertEqual("%s" %
                ((self.sum - self.min) + (self.max - self.sum)),
                "((sum(test(ing)) - min(test(ing))) + " \
                        "(max(test(ing)) - sum(test(ing))))")

    def test_multiplication(self):
        self.assertEqual("%s" % (self.sum - self.min * self.max),
                "(sum(test(ing)) - (min(test(ing)) * max(test(ing))))")
        self.assertEqual("%s" %
                ((self.max - self.min) * (self.sum + self.min)),
                "((max(test(ing)) - min(test(ing))) * "\
                        "(sum(test(ing)) + min(test(ing))))")
        self.assertEqual("%s" %
                (self.max - self.min * self.sum + self.min),
                "((max(test(ing)) - (min(test(ing)) * "\
                        "sum(test(ing)))) + min(test(ing)))")

    def test_division(self):
        self.assertEqual("%s" % (self.max / self.sum * self.min),
                "((max(test(ing)) / sum(test(ing))) * min(test(ing)))")
        self.assertEqual("%s" %
                ((self.min / self.sum) / (self.min + self.max)),
                "((min(test(ing)) / sum(test(ing))) / "\
                    "(min(test(ing)) + max(test(ing))))")
        self.assertEqual("%s" %
                (self.min / self.sum * self.max + self.min - self.max),
                "((((min(test(ing)) / sum(test(ing))) * max(test(ing))) + "\
                        "min(test(ing))) - max(test(ing)))")

    def test_types(self):
        self.assertTrue(isinstance(self.sum, MetricExpression))
        self.assertTrue(isinstance(self.min, MetricExpression))
        self.assertTrue(isinstance(self.max, MetricExpression))
        self.assertTrue(isinstance(self.sum + self.sum,
            CompoundMetricExpression))
        self.assertTrue(isinstance(self.sum + self.min,
            CompoundMetricExpression))
        self.assertTrue(isinstance(self.max + self.min,
            CompoundMetricExpression))
