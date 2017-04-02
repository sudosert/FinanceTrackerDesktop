import sqlite3
from datetime import date

current_month_year = date.today().strftime('%m%Y')  # Returns current month/year in format of 022017

connection = sqlite3.connect("finances.db")
cursor = connection.cursor()


def initial_db_setup():
    command = """
    CREATE TABLE IF NOT EXISTS 'Bills - Master'(
    Name TEXT PRIMARY KEY,
    Amount NUMERIC,
    Notes TEXT,
    Paid INTEGER
    );
    CREATE TABLE IF NOT EXISTS 'Credit - Master'(
    Name TEXT PRIMARY KEY,
    Balance NUMERIC,
    'Limit' NUMERIC,
    Interest NUMERIC,
    Type TEXT
    );
    CREATE TABLE IF NOT EXISTS 'Savings - Master'(
    Name TEXT PRIMARY KEY,
    Balance NUMERIC,
    Interest NUMERIC
    );
    CREATE TABLE IF NOT EXISTS 'Bills - {}'
    AS SELECT * FROM 'Bills - Master'
    """.format(current_month_year)

    command_list = command.split(";")
    [cursor.execute(command) for command in command_list]  # Cycles through each SQL statement separated by ;


# Getter Functions
def get_list_of_bills():
    command = """
    SELECT * FROM 'Bills - {}'
    """.format(current_month_year)
    cursor.execute(command)
    return cursor.fetchall()


def get_selected_bill_info(bill_name):
    command = """
    SELECT Amount, Paid FROM 'Bills - {}'
    WHERE Name = ?
    """.format(current_month_year)
    cursor.execute(command, (bill_name,))
    return cursor.fetchone()


# Setter Functions
def add_new_bill(name, amount, notes, recurring):
    command = """
    INSERT INTO 'Bills - {}' (Name, Amount, Notes, Paid)
    VALUES (?, ?, ?, 0)
    """.format(current_month_year)
    if recurring:
        command += ";"
        command += """
        INSERT INTO 'Bills - Master' (Name, Amount, Notes, Paid)
        VALUES (?, ?, ?, 0)
        """

    command_list = command.split(";")
    [cursor.execute(command, (name, amount, notes)) for command in command_list]  # Cycles through each SQL statement
    connection.commit()


def update_selected_bill(bill_name, bill_amount, bill_paid):
    command = """
    UPDATE 'Bills - {}'
    SET Amount = ?, Paid = ?
    WHERE Name = ?
    """.format(current_month_year)
    cursor.execute(command, (bill_amount, bill_paid, bill_name))
    connection.commit()




