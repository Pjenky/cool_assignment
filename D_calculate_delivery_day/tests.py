from datetime import datetime, timezone
import unittest
from main import get_delivery_date, next_working_day, is_closed, calculate_easter_day

class TestDeliveryFunctions(unittest.TestCase):
    def test_calculate_easter_day(self):
        # Test the function for a range of years with known Easter dates
        test_cases = {
            2021: datetime(2021, 4, 4),
            2022: datetime(2022, 4, 17),
            2023: datetime(2023, 4, 9),
            2024: datetime(2024, 3, 31),
        }

        for year, expected_date in test_cases.items():
            with self.subTest(year=year):
                calculated_date = calculate_easter_day(year)
                self.assertEqual(calculated_date, expected_date)

    def test_is_closed(self):
        # Test for a date that should be closed
        closed_date = datetime(2024, 1, 1)
        self.assertTrue(is_closed(closed_date))

        # Test for a date that should not be closed
        open_date = datetime(2024, 1, 5)
        self.assertFalse(is_closed(open_date))

    def test_next_working_day(self):
        # Test for a weekend, expecting the next Monday
        weekend_date = datetime(2024, 1, 13)
        next_working = next_working_day(weekend_date)
        self.assertEqual(next_working.weekday(), 0)

        # Test for a holiday, expecting the next working day after the holiday
        holiday_date = datetime(2024, 1, 1)
        next_working = next_working_day(holiday_date)
        self.assertNotEqual(next_working.day, 1)

        # Test for a regular weekday, expecting the same day
        weekday_date = datetime(2024, 1, 15)
        next_working = next_working_day(weekday_date)
        self.assertEqual(next_working.day, 15)
    
    def test_get_delivery_date(self):
        # Test cases
        test_orders = [
            (datetime(2021, 5, 20, 12, 51, 32, 199883, timezone.utc), datetime(2021, 5, 21).date()),
            (datetime(2021, 5, 20, 13, 3, 31, 245381, timezone.utc), datetime(2021, 5, 25).date()),
            (datetime(2020, 12, 29, 12, 15, 12, 0, timezone.utc), datetime(2020, 12, 30).date()),
            (datetime(2020, 12, 29, 14, 15, 12, 0, timezone.utc), datetime(2021, 1, 4).date()),
        ]

        for order_datetime, expected_delivery_date in test_orders:
            with self.subTest(order_datetime=order_datetime):
                delivery_date = get_delivery_date(order_datetime)
                self.assertEqual(delivery_date.date(), expected_delivery_date)

if __name__ == '__main__':
    unittest.main()