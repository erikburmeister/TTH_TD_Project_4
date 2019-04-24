"""Worklog with a Database
create entries and save them to a database. An entry would consist of
an employee name, date of task, title of task, time spent
(rounded minutes), and notes (optional). The user can page through past
entries to edit, or delete them.

Created: 04/08/2019
Author: Erik Burmeister
"""


import datetime
import os


from peewee import *


db = SqliteDatabase("entry_database_2.4.db")


def clear_screen():
    """Clears the screen from any previous output."""

    os.system('cls' if os.name == 'nt' else 'clear')


class Entry(Model):
    """This a class used to create entries for a database.
    The class inherits from the Model class from the PEEWEE library.
    """

    name = CharField(max_length=35)
    date = DateField()
    title = CharField(max_length=35)
    time = IntegerField(default=0)
    notes = TextField()

    class Meta:
        database = db


def initialize():  # pragma: no cover
    """create the database and the table if they don't exist"""

    try:
        db.connect()
        db.create_tables([Entry], safe=True)
        print("A connection to the database has been established.")

    except OperationalError:
        print("A connection to the database is already established.")

    else:
        pass


def main_menu():
    """Displays the main menu of the app."""

    initialize()  # pragma: no cover

    main_menu_options = """
WORK LOG with a Database
------------------------
What Would you like to do?
A) Add New Entry
B) Search in Existing Entries
C) View All Entries
D) Quit Program
"""

    main_menu_answer = ''

    while (not main_menu_answer == 'a' or
           not main_menu_answer == 'b' or
           not main_menu_answer == 'c'):

        print(main_menu_options)

        main_menu_answer = input().lower()

        if main_menu_answer == 'a':
            clear_screen()
            add_to_database()

        elif main_menu_answer == 'b':
            clear_screen()
            search_by_menu()

        elif main_menu_answer == 'c':
            clear_screen()
            display_entries()

        elif main_menu_answer == 'd':
            clear_screen()
            break

        else:
            print("That's not a valid choice.")
            input("Press enter to try again.")
            clear_screen()

    db.close()
    print("The connection to the database has been closed.")
    print("")
    print("Thank you for using Work Log with a Database.")
    print("See you later!")


def add_employee():
    """Creates a name for the class instance"""

    print("Type first, middle (if applicable), and last name")
    name_of_employee = input("Name of employee: ").title().strip()
    clear_screen()

    return name_of_employee


def add_date_obj():
    """Creates a date object and returns it."""

    while True:

        print("Date of task")
        date_of_task = input("Please use MM/DD/YYYY: ")
        time_format = '%m/%d/%Y'

        try:
            validate_date = datetime.datetime.strptime(
                date_of_task, time_format)

        except ValueError:
            print("That's not a valid date or MM/DD/YYYY format.")
            input("Press enter to try again.")
            clear_screen()

        else:
            break

    clear_screen()
    dots = date_of_task.split("/")
    obj_dot = datetime.datetime.strptime(
        "{}/{}/{}".format(dots[2], dots[0], dots[1]), '%Y/%m/%d')

    return obj_dot


def add_title():
    """Creates a title for the class instance"""

    title_of_the_task = input("Title of the task: ")
    clear_screen()

    return title_of_the_task


def add_time():
    """Creates a time for the class instance"""

    while True:

        try:
            time_spent = int(input("Time spent (rounded minutes): "))

        except ValueError:
            print("That's not a number. Try again.")

        else:
            clear_screen()
            break

    return time_spent


def add_notes():
    """Creates notes for the class instance"""

    print("Notes are optional. You can leave this empty")
    task_notes = input("Notes: ")
    clear_screen()

    return task_notes


def add_to_database():
    """Takes all the returned information from all of the
    functions and creates an instance of the class with the
    information provided and adds it to the database.
    """

    Entry.create(name=add_employee(),
                 date=add_date_obj(),
                 title=add_title(),
                 time=add_time(),
                 notes=add_notes())

    print("The entry has been added to the database. ")
    input("Press enter to continue.")


def delete_entry(del_entry):
    """Delete's an entry from the database."""

    clear_screen()
    del_entry.delete_instance()

    print("The entry has been deleted.")
    input("Press enter to return to entries.")


def edit_name(name_of_emp):
    """creates a name that can then substitute an existing one."""

    name_of_emp.name = add_employee()
    name_of_emp.save()

    return name_of_emp.name


def edit_date(date_of_task):
    """creates a date that can then substitute an existing one."""

    date_of_task.date = add_date_obj()
    date_of_task.save()

    return date_of_task.date


def edit_title(title_of_task):
    """creates a title that can then substitute an existing one."""

    title_of_task.title = add_title()
    title_of_task.save()

    return title_of_task.title


def edit_time(time_of_task):
    """creates a time that can then substitute an existing one."""

    time_of_task.time = add_time()
    time_of_task.save()

    return time_of_task.time


def edit_notes(notes_of_task):
    """creates notes that can then substitute an existing set of notes.
    """

    notes_of_task.notes = add_notes()
    notes_of_task.save()

    return notes_of_task.notes


def display_entries(subject=None, subject_2=None,
                    search_query=None, search_query_2=None):
    """Displays entries in a predetermined format."""

    entry = Entry.select().order_by(Entry.date)

    field_mapping = {
        'name': Entry.name,
        'date': Entry.date,
        'title': Entry.title,
        'time': Entry.time,
        'notes': Entry.notes
    }

    selected_field = field_mapping.get(subject)

    if subject and search_query:
        entry = entry.where(selected_field.contains(search_query))

    if subject_2 and search_query and search_query_2:
        entry = entry.where(Entry.date.between(search_query, search_query_2))

    if subject and subject_2 and search_query_2:
        entry = entry.where(
            Entry.title.contains(
                search_query_2) | Entry.notes.contains(search_query_2)
        )

    if subject_2 == 'time' and search_query:
        entry = entry.where(Entry.time == search_query)

    n = 0
    while True:

        if len(entry) >= 1:

            if n == -1:
                n += 1

            print()
            print("Employee name: {}".format(entry[n].name))
            print("-" * len("Employee name: {}".format(entry[n].name)))
            print("Date: {}".format(entry[n].date.strftime("%m/%d/%Y")))
            print("Task: {}".format(entry[n].title))
            print("Time To Complete: {} minutes".format(entry[n].time))
            print("Notes: {}".format(entry[n].notes))
            print("-" * len("Employee name: {}".format(entry[n].name)))
            print("")
            print("Result {} of {}".format(n+1, len(entry)))
            print("")

            choices = ["[N]ext", "[P]revious", "[E]dit",
                       "[D]elete", "[R]eturn to previous menu"]

            if n == 0:
                choices.remove("[P]revious")

            if n == (len(entry)-1):
                choices.remove("[N]ext")

            print("{}".format(', '.join(choices)))
            print("")

            display_entries_selection = input().lower()

            if display_entries_selection == 'p' and n == 0:
                n = n

            elif display_entries_selection == 'p' and n != 0:
                n -= 1

            if display_entries_selection == 'n' and n == len(entry):
                n = n

            elif display_entries_selection == 'n' and n != len(entry) - 1:
                n += 1

            if display_entries_selection == 'e':
                clear_screen()
                entry[n].name = edit_name(entry[n])
                entry[n].date = edit_date(entry[n])
                entry[n].title = edit_title(entry[n])
                entry[n].time = edit_time(entry[n])
                entry[n].notes = edit_notes(entry[n])
                clear_screen()

            if display_entries_selection == 'd':
                if (not subject and not subject_2 and
                    not search_query and not search_query_2):

                    delete_entry(entry[n])
                    entry = Entry.select().order_by(Entry.date)
                    n -= 1

                if subject and search_query:
                    delete_entry(entry[n])
                    entry = entry.where(selected_field.contains(search_query))
                    n -= 1

                if subject_2 and search_query and search_query_2:
                    delete_entry(entry[n])
                    entry = entry.where(Entry.date.between(
                        search_query, search_query_2))
                    n -= 1

                if subject and subject_2 and search_query_2:
                    delete_entry(entry[n])
                    entry = entry.where(
                        Entry.title.contains(
                            search_query_2) | Entry.notes.contains(
                            search_query_2)
                    )
                    n -= 1

                if subject_2 == 'time' and search_query:
                    delete_entry(entry[n])
                    entry = entry.where(Entry.time == search_query)
                    n -= 1

            if display_entries_selection == 'r':
                break

            if len(entry) == 0:
                print("There are no entries left.")
                break

            clear_screen()

        else:
            print("No results found.")
            break

    clear_screen()


def search_by_menu():
    """Displays the search menu of the app."""

    search_by_options = """
Do you want to search by:
A) List of Employees
B) Employee Name
C) List of Dates
D) Search Between Two Dates
E) Exact Time Spent on a Task
F) Term on Task Title and/or Notes
G) Return to Menu
"""

    search_by_answer = ''

    while (not search_by_answer == 'a' or not search_by_answer == 'b' or
           not search_by_answer == 'c' or not search_by_answer == 'd' or
           not search_by_answer == 'e'):

        print(search_by_options)

        search_by_answer = input().lower()

        if search_by_answer == 'a':
            clear_screen()
            list_employees()

        elif search_by_answer == 'b':
            clear_screen()
            search_employee_name()

        elif search_by_answer == 'c':
            clear_screen()
            list_dates()

        elif search_by_answer == 'd':
            clear_screen()
            search_between_dates()

        elif search_by_answer == 'e':
            clear_screen()
            search_times()

        elif search_by_answer == 'f':
            clear_screen()
            search_title_notes()

        elif search_by_answer == 'g':
            clear_screen()
            break

        else:
            print("That's not a valid choice.")
            input("Press enter to try again.")
            clear_screen()


def list_employees():
    """Prints a list of all the employee names who have an entry in
    the database under their name. Then let's the user select the
    employee by inputting the number next to their name. The user input
    is passed into the display_entries() function to display the
    results in a predetermined format.
    """

    employee_list = []
    employee_choice_list = [None]

    entries = Entry.select().order_by(Entry.id)

    for entry in entries:

        if entry.name in employee_list:
            pass

        elif entry not in employee_list:
            employee_list.append(entry.name)
            employee_choice_list.append(entry.name)

    while True:

        print("List of Employee Names")
        print("-" * 36)

        n = 1
        for emp in employee_list:
            print(f"{n})", "Employee name: {}".format(emp))
            n += 1

        print("-" * 36)
        print()
        print("Which employee from the list are you looking for?")
        print("Type the number in front of their name to choose one.")

        try:
            search = employee_choice_list[int(input())]

            if search == employee_choice_list[0]:
                raise IndexError

        except IndexError:
            print("That's not a number on the list. Try again.")
            input("Press enter to try again.")
            clear_screen()

        except ValueError:
            print("That's not a number.")
            input("Press enter to try again.")
            clear_screen()

        else:
            clear_screen()
            break

    display_entries('name', None, search)


def search_employee_name():
    """The user is allowed to input a matching string or part of a
    string that is believed to be in an employee name that has entries
    in the database. The user input is passed into the
    display_entries() function to display the results in a
    predetermined format.
    """

    employee_list = []
    employee_choice_list = [None]

    print("Type part of or the full name of an employee. \n")
    search_1 = input("Search for an employee: ")

    entries = Entry.select().order_by(Entry.id)

    if search_1:
        entries = entries.where(Entry.name.contains(search_1))

        for entry in entries:

            if entry.name in employee_list:
                pass

            elif entry not in employee_list:
                employee_list.append(entry.name)
                employee_choice_list.append(entry.name)

    if len(employee_list) == 0:
            clear_screen()
            print("No employee name contains that search.")
            input("Press enter to return to the last menu.")
            return

    else:
        while True:

            if len(employee_list) >= 1:

                clear_screen()
                print("Search for an employee: {}".format(search_1))
                print("-" * len("Search for an employee: " + search_1))
                n = 1
                for emp in employee_list:
                    print(f"{n})", "Employee name: {}".format(emp))
                    n += 1
                print("-" * len("Search for an employee: " + search_1))

                print("Which employee from the list are you looking for?")
                print("type the number in front of their name.")

                try:
                    search_2 = employee_choice_list[int(input())]
                    if search_2 == employee_choice_list[0]:
                        raise IndexError

                except IndexError:
                    print("That's not a number on the list. Try again.")
                    input("Press enter to try again.")
                    clear_screen()

                except ValueError:
                    print("That's not a number.")
                    input("Press enter to try again.")
                    clear_screen()

                else:
                    clear_screen()
                    break

        return display_entries('name', None, search_2)


def list_dates():
    """Prints a list of all the dates found in an entry in
    the database. Then let's the user select the date by inputting
    the number next to the date. The user input is passed into the
    display_entries() function to display the results in a
    predetermined format.
    """

    date_list = []
    date_choice_list = [None]

    entries = Entry.select().order_by(Entry.id)

    for entry in entries:

            if entry.date.strftime("%m/%d/%Y") in date_list:
                pass

            elif entry not in date_list:
                date_list.append(entry.date.strftime("%m/%d/%Y"))
                date_choice_list.append(entry.date)

    while True:

        print("List of Task Dates")
        print("-" * 24)

        n = 1
        for date in date_list:
            print(f"{n})", "Task date: {}".format(date))
            n += 1

        print("-" * 24)

        print()
        print("Which task date from the list are you looking for?")
        print("Type the number in front of the date to choose one.")

        try:
            search = date_choice_list[int(input())]

            if search == date_choice_list[0]:
                raise IndexError

        except IndexError:
            print("That's not a number on the list. Try again.")
            input("Press enter to try again.")
            clear_screen()

        except ValueError:
            print("That's not a number.")
            input("Press enter to try again.")
            clear_screen()

        else:
            clear_screen()
            break

    display_entries('date', None, search)


def search_between_dates():
    """Allows the user to input 2 dates using the add_date_obj()
    function. The user input is passed into the display_entries()
    function to display the results in a predetermined format.
    """

    print("Enter two dates. The search will find")
    print("all the entries between the first")
    print("and second date.")
    print()

    print("First Date")
    print("----------")
    search = add_date_obj()
    print("Second Date")
    print("-----------")
    search_2 = add_date_obj()

    display_entries(None, 'date', search, search_2)


def search_times():
    """Allows the user to input a number that will find results only
    if they match the exact number that is in an entry. The user input
    is passed into the display_entries() function to display the
    results in a predetermined format.
    """

    while True:

        print("Search for time spent on a task.")
        print("Input the exact number for the")
        print("entry you are looking for.")
        print()

        try:
            search = int(input("Exact time spent (rounded minutes): "))

        except ValueError:
            print("That's not a number. Try again.")
            input("Press enter to try again.")
            clear_screen()

        else:
            clear_screen()
            break

    display_entries(None, 'time', search)


def search_title_notes():
    """Allows the user to input a term that will then be used to
    search all entries in the database and pull matches that have
    the search term in their task title or notes. The user input
    is passed into the display_entries() function to display the
    results in a predetermined format.
    """

    print("Search for any word, or part of a word,")
    print("that might be included in the task name")
    print("or in the notes.")
    print()

    search = input("Search term: ")

    display_entries('title', 'notes', None, search)


if __name__ == '__main__':
    main_menu()
