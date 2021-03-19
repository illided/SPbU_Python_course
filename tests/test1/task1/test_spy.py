import unittest
from solutions.test1.task1.spy import Spy, print_usage_statistic


@Spy
def return_itself(x):
    return x


@Spy
def return_something_or_eight(x=None):
    if x is None:
        return 8


class SpyTest(unittest.TestCase):
    def tearDown(self) -> None:
        return_itself.clear()
        return_something_or_eight.clear()

    def test_simple(self):
        return_itself(10)
        statistic = [y for x, y in print_usage_statistic(return_itself)]
        self.assertEqual({"x": 10}, statistic[0])

    def test_with_named(self):
        return_itself(x=7)
        statistic = [y for x, y in print_usage_statistic(return_itself)]
        self.assertEqual({"x": 7}, statistic[0])

    def test_with_default_filled_manually(self):
        return_something_or_eight(x=10)
        statistic = [y for x, y in print_usage_statistic(return_something_or_eight)]
        self.assertEqual({"x": 10}, statistic[0])
