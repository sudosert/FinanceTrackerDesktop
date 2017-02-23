import sqlite3

connection = sqlite3.connect("finances.db")
cursor = connection.cursor()

def initial_db_setup():
    command = """
    CREATE TABLE IF NOT EXISTS 'Bills - Master'(
    Name TEXT PRIMARY KEY,
    Amount NUMERIC,
    Notes TEXT
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
    )
    """
    cursor.execute(command)


def get_list_of_bills():
    command = """
    SELECT * FROM 'Bills - Master'
    """
    cursor.execute(command)
    return cursor.fetchall()


def add_new_bill(name, amount, notes):
    command = """
    INSERT INTO 'Bills - Master' (Name, Amount, Notes) 
    VALUES (?, ?, ?) 
    """
    cursor.execute(command, (name, amount, notes))
    connection.commit()






