import math
import unittest


def time_to_cyclic(hour):
    """Convert hour into cyclic features (sine and cosine)"""
    # Normalize hour (0-24) to (0-2π) for trigonometric functions
    radians = (hour % 24) * (2 * math.pi / 24)  # Ensure hour is within 0-24 range
    return math.sin(radians), math.cos(radians)


def cyclic_time_difference(hour1, hour2):
    """Calculate cyclic time difference between two hours"""
    sin1, cos1 = time_to_cyclic(hour1)
    sin2, cos2 = time_to_cyclic(hour2)

    # Calculate the Euclidean distance between (sin1, cos1) and (sin2, cos2)
    dot_product = sin1 * sin2 + cos1 * cos2

    # Ensure dot_product is clamped to [-1, 1] to avoid math domain errors in acos
    dot_product = max(-1.0, min(1.0, dot_product))

    diff = math.acos(dot_product) * (24 / (2 * math.pi))  # Convert angle back to hours
    return diff


# Unit Tests and Functional Tests
class TestCyclicTime(unittest.TestCase):

    def test_time_to_cyclic_midnight(self):
        """Test cyclic conversion for midnight (0 hours)"""
        sin, cos = time_to_cyclic(0)
        self.assertAlmostEqual(sin, 0, places=5)
        self.assertAlmostEqual(cos, 1, places=5)

    def test_time_to_cyclic_noon(self):
        """Test cyclic conversion for noon (12 hours)"""
        sin, cos = time_to_cyclic(12)
        self.assertAlmostEqual(sin, 0, places=5)
        self.assertAlmostEqual(cos, -1, places=5)

    def test_time_to_cyclic_edge_case(self):
        """Test cyclic conversion for edge cases (24 hours)"""
        sin, cos = time_to_cyclic(24)
        self.assertAlmostEqual(sin, 0, places=5)
        self.assertAlmostEqual(cos, 1, places=5)

    def test_cyclic_time_difference_same_hour(self):
        """Difference between same hours should be zero"""
        self.assertAlmostEqual(cyclic_time_difference(10, 10), 0, places=5)

    def test_cyclic_time_difference_across_midnight(self):
        """Test time difference across midnight"""
        diff = cyclic_time_difference(23, 1)
        self.assertAlmostEqual(diff, 2, places=5)

    def test_cyclic_time_difference_within_day(self):
        """Test time difference within same day"""
        diff = cyclic_time_difference(10, 14)
        self.assertAlmostEqual(diff, 4, places=5)

    def test_cyclic_time_difference_half_day(self):
        """Test time difference between opposite hours (e.g., 0 and 12)"""
        diff = cyclic_time_difference(0, 12)
        self.assertAlmostEqual(diff, 12, places=5)

    def test_cyclic_time_difference_negative_hour(self):
        """Test time difference with negative hours"""
        diff = cyclic_time_difference(-1, 1)
        self.assertAlmostEqual(diff, 2, places=5)


if __name__ == '__main__':
    unittest.main()
