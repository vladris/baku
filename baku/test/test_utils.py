import os
import shutil
import unittest
from datetime import datetime
from baku import utils


class TestUtils(unittest.TestCase):
    def tearDown(self):
        if os.path.exists('testrun'):
            shutil.rmtree('testrun')


    def test_name_from_title_replace_spaces(self):
        self.assertEqual(
            utils.name_from_title('Post title'),
            'post-title')


    def test_ensure_path(self):
        test_path = os.path.join('testrun', 'testdir', '1')
        self.assertFalse(os.path.exists(test_path))

        utils.ensure_path(test_path)

        self.assertTrue(os.path.exists(test_path))


    def test_name_from_title_strip_nonalnum(self):
        self.assertEqual(
            utils.name_from_title('Post & title 123!'),
            'post-title-123')


    def test_parse_date(self):
        date = utils.parse_date('2022/09/01')

        self.assertEqual(date.year, 2022)
        self.assertEqual(date.month, 9)
        self.assertEqual(date.day, 1)


    def test_split_date(self):
        date = datetime(2022, 9, 1)
        year, month, day = utils.split_date(date)

        self.assertEqual(year, '2022')
        self.assertEqual(month, '09')
        self.assertEqual(day, '01')
