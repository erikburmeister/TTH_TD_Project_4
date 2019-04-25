import unittest
import datetime
from unittest.mock import patch

from peewee import SqliteDatabase

import app

db = SqliteDatabase(":memory:")
MODELS = [app.Entry]


class WorklogTests(unittest.TestCase):
    def setUp(self):
        db.bind(MODELS)
        db.connect(reuse_if_open=True)
        db.create_tables(MODELS, safe=True)
        self.entry = MODELS[0].create(name="Name",
                                      date=datetime.date(2001, 1, 1),
                                      title="title",
                                      time=0,
                                      notes="notes")

    def test_main_menu(self):
        inputs_to_pass = ['a', 'Name Nameson', '01/01/2000', 'Title', 0, 'Notes', '',  # 6
                          'b', 'z', '', 'a', 1, 'r', 'b', 'eri', 1, 'r', 'c', '1', 'r',  # 19
                          'd', '01-01-2000', '', '01/01/2000', '01-01-2000', '',  # 25
                          '03/03/2003', 'r', 'e', '50', 'r', 'f', 'jan', 'r', 'g', 'c',  # 35
                          'r', 'z', '', 'd', None]  # 40
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.main_menu()

            self.assertEqual(result, inputs_to_pass[40])

    def test_add_employee(self):
        inputs_to_pass = ['Name Nameson', 'Name Nameson ']
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.add_employee()

            self.assertEqual(result, inputs_to_pass[0])
            self.assertNotEqual(result, inputs_to_pass[1])

    def test_add_date_obj(self):
        inputs_to_pass = ['01-01-2000', '', '01/01/2000', datetime.datetime(2000, 1, 1, 0, 0)]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.add_date_obj()

            self.assertEqual(result, inputs_to_pass[3])

    def test_add_title(self):
        inputs_to_pass = ['Task Name']
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.add_employee()
            self.assertEqual(result, inputs_to_pass[0])

    def test_add_time(self):
        inputs_to_pass = ['a', '', 50]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.add_time()
            self.assertEqual(result, inputs_to_pass[2])

    def test_add_notes(self):
        inputs_to_pass = ['Notes']
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.add_notes()
            self.assertEqual(result, inputs_to_pass[0])

    def test_search_by_menu(self):
        inputs_to_pass = ['z', '', 'a', 1, 'r', 'b', 'eri', 1, 'r', 'c', '1', 'r',  # 11
                          'd', '01-01-2000', '', '01/01/2000', '01-01-2000', '',  # 17
                          '03/03/2003', 'r', 'e', 's', '', 50, 'r', 'f', 'jan', 'r',  # 27
                          'g', 'c', 'r', None]  # 31
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.search_by_menu()

            self.assertEqual(result, inputs_to_pass[31])

        inputs_to_pass = ['c', 1, 'r', 'g', None]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.search_by_menu()

            self.assertEqual(result, inputs_to_pass[4])

        inputs_to_pass = ['f', 'no', 'r', 'g', None]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.search_by_menu()

            self.assertEqual(result, inputs_to_pass[4])

    def test_list_employees(self):
        inputs_to_pass = ['0', '', 0, '', 'sad', '', 1, 'r', None]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.list_dates()
            self.assertEqual(result, inputs_to_pass[8])

    def test_search_employee_name(self):
        inputs_to_pass = ['na', 0, '', 's', '', 1, 'r', None]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.search_employee_name()
            self.assertEqual(result, inputs_to_pass[7])

    def test_search_title_notes(self):
        inputs_to_pass = ['mar', None]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.search_title_notes()
            self.assertEqual(result, inputs_to_pass[1])

    def test_delete_entry(self):
        inputs_to_pass = [None]
        result = app.delete_entry(self.entry)
        self.assertEqual(result, inputs_to_pass[0])

    def test_edit_name(self):
        inputs_to_pass = ['New Name']
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.edit_name(self.entry)
            self.assertEqual(result, inputs_to_pass[0])

    def test_edit_date(self):
        inputs_to_pass = ['01/01/2000', datetime.datetime(2000, 1, 1, 0, 0)]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.edit_date(self.entry)
            self.assertEqual(result, inputs_to_pass[1])

    def test_edit_title(self):
        inputs_to_pass = ['Task Title']
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.edit_title(self.entry)
            self.assertEqual(result, inputs_to_pass[0])

    def test_edit_time(self):
        inputs_to_pass = [100]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.edit_time(self.entry)
            self.assertEqual(result, inputs_to_pass[0])

    def test_edit_notes(self):
        inputs_to_pass = ['New Notes']
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.edit_notes(self.entry)
            self.assertEqual(result, inputs_to_pass[0])

    def test_display_entries(self):
        inputs_to_pass = ['e', 'Name Nameson', '01/01/2000',
                          'Title', 0, 'Notes', 'r', None]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.display_entries()
            self.assertEqual(result, inputs_to_pass[7])

        inputs_to_pass = ['d', '', 'r', None]
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = app.display_entries()
            self.assertEqual(result, inputs_to_pass[3])


if __name__ == '__main__':
    unittest.main()