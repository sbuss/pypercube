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
        self.assertTrue(isinstance(self.min, MetricExpression))
        self.assertTrue(isinstance(self.max, MetricExpression))
        self.assertTrue(isinstance(self.sum + self.sum,
            CompoundMetricExpression))
        self.assertTrue(isinstance(self.sum + self.min,
            CompoundMetricExpression))
        self.assertTrue(isinstance(self.max + self.min,
            CompoundMetricExpression))

        m1 = self.sum
        m2 = self.min
        self.assertTrue(isinstance(m1 + m2, CompoundMetricExpression))
        self.assertTrue(isinstance(m1 - m2, CompoundMetricExpression))
        self.assertTrue(isinstance(m1 * m2, CompoundMetricExpression))
        self.assertTrue(isinstance(m1.__div__(m2), CompoundMetricExpression))
        self.assertTrue(isinstance(
            m1.__truediv__(m2), CompoundMetricExpression))

    def test_filters(self):
        e1 = EventExpression('request', 'elapsed_ms').eq('path', '/')
        e2 = e1.gt('elapsed_ms', 500)
        self.assertEqual("%s" % (Sum(e1) - Min(e2)),
                "(sum(request(elapsed_ms).eq(path, \"/\")) - "\
                "min(request(elapsed_ms).eq(path, \"/\").gt("\
                    "elapsed_ms, 500)))")
