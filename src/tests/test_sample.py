"""
Both the test file and the function must include test_. The test function must start with test_. The test file must end with _test.py.
The test file must be in the tests directory.

You can also group multiple tests in a class: https://pytest.org/en/7.4.x/getting-started.html#group-multiple-tests-in-a-class
"""

from unittest import TestCase, main


class SampleTestCase(TestCase):
  def test_sample(self):
    assert 4 == 4


if __name__ == "__name__":
  main()
