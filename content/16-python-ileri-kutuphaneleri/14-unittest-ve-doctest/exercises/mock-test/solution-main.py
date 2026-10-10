import unittest
from unittest.mock import patch

from weather import advice


class TestAdvice(unittest.TestCase):
    @patch("weather.fetch_temp", return_value=5)
    def test_cold(self, fake):
        self.assertEqual(advice("Oslo"), "coat")

    @patch("weather.fetch_temp", return_value=20)
    def test_warm(self, fake):
        self.assertEqual(advice("Izmir"), "t-shirt")

    @patch("weather.fetch_temp", return_value=10)
    def test_boundary(self, fake):
        self.assertEqual(advice("Bern"), "t-shirt")
