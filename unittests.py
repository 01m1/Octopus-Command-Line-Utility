import unittest
from main import parse_flow, meter_count, total_sum_valid_readings, total_sum_invalid_readings, \
    highest_and_lowest_valid_readings, most_recent_and_oldest_readings


class UnitTest(unittest.TestCase):
    def test_meter_file(self):
        data = parse_flow('meter_readings')
        self.assertEqual(len(data), 3)
        self.assertEqual(data[1300001188124][20200329001234]['READING_STATUS'], "F")
        self.assertEqual(data[1300001188124][2020032904567]['READING_VALUE'], 1144.0)

    def test_file_processing(self):
        data = parse_flow('meter_readings')
        self.assertEqual(meter_count(data), 3)
        self.assertEqual(total_sum_valid_readings(data), 45639.1)
        self.assertEqual(total_sum_invalid_readings(data), 1259.0)
        self.assertEqual(str(highest_and_lowest_valid_readings(data)),
                         "(29310.0, [20200315000000], 4810.1, [20200110000000])")
        self.assertEqual(str(most_recent_and_oldest_readings(data)),
                         "(datetime.date(2021, 4, 2), [20200110000000], datetime.date(2021, 3, 31), [20200329001234])")


if __name__ == "__main__":
    unittest.main()
