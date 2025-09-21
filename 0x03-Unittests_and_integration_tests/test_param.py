# test_param.py

from parameterized import parameterized_class
import unittest

@parameterized_class([
    {"value": 1},
    {"value": 2}
])
class TestDummy(unittest.TestCase):
    def test_value_is_int(self):
        self.assertIsInstance(self.value, int)
