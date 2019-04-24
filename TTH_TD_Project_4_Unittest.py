import unittest

from TTH_TD_Project_4_V7_Unittest import *


db = SqliteDatabase("entry_database_2.4.db")

class WorklogTests(unittest.TestCase):

	def setUp(self):
		self.entry = Entry.select().order_by(Entry.id)

	def test_clear_screen(self):
		self.assertIsNone(clear_screen())

	def test_main_menu(self):
		pass

	def test_add_employee(self):
		self.assertIsNotNone(add_employee)

	def test_add_date_obj(self):
		self.assertIsNotNone(add_date_obj)

	def test_add_title(self):
		self.assertIsNotNone(add_title)

	def test_add_time(self):
		self.assertIsNotNone(add_title)

	def test_add_notes(self):
		self.assertIsNotNone(add_title)

	def test_add_to_database(self):
		self.assertIsNotNone(Entry.create(name="Name",
                 date=datetime.date(2001, 1, 1),
                 title="title",
                 time=0,
                 notes="notes"))

	def test_delete_entry(self):
		self.assertIsNone(delete_entry(self.entry[16]))

	def test_edit_name(self):
		print("Test Edit Name (Write anything)")
		self.assertIsNotNone(edit_name(self.entry[16]))

	def test_edit_date(self):
		print("Test Edit Date (Type a real date)")
		self.assertIsNotNone(edit_date(self.entry[16]))

	def test_edit_title(self):
		print("Test Edit Title (Write anything)")
		self.assertIsNotNone(edit_title(self.entry[16]))

	def test_edit_time(self):
		print("Test Edit Time (Type a number)")
		self.assertIsNotNone(edit_time(self.entry[16]))

	def test_edit_notes(self):
		print("Test Edit Notes (Write anything)")
		self.assertIsNotNone(edit_notes(self.entry[16]))

	def test_display_entries(self):
		self.assertIsNone(display_entries())
		self.assertIsNone(display_entries('name',None, 'Erik'))
		self.assertIsNone(display_entries(None, 'date',
										  datetime.date(2001, 1, 1),
										  datetime.date(2003, 1, 1)))
		self.assertIsNone(display_entries('title', 'notes', None, 'jan'))
		self.assertIsNone(display_entries(None, 'time', 10))

	def test_search_by_menu(self):
		pass

	def test_list_employees(self):
		self.assertIsNone(list_employees())

	def test_search_employee_name(self):
		self.assertIsNone(search_employee_name())

	def test_list_dates(self):
		self.assertIsNone(list_dates())

	def test_search_between_dates(self):
		self.assertIsNone(search_between_dates())

	def test_search_times(self):
		self.assertIsNone(search_times())

	def test_search_title_notes(self):
		self.assertIsNone(search_title_notes())

if __name__ == '__main__':
	unittest.main()