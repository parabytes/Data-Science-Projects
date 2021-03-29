import sqlite3
import pandas as pd
from sqlite3 import Error


def create_table(conn, create_table_sql, table_name):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :param table_name: Table name to be created
    :return:
    """
    try:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS {}".format(table_name))
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def run():
    """ Creates contractors.db database. If tables exist in the database it deletes existing tables and replaces them
    with the new instance.

    :return:
    """
    db = sqlite3.connect('contracts')
    dfs = pd.read_excel('contracts.xls', sheet_name=None)
    for table, df in dfs.items():
        table_name = table.split(' ')[0]
        if table_name == '(GSA)':
            table_name = 'GSA'
        db.execute("DROP TABLE IF EXISTS {}".format(table_name))
        df.to_sql(table_name, db)

    con = sqlite3.connect("contracts")
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    departments = cursor.fetchall()
    departments_list = []
    for i in range(1, len(departments)):
        departments_list.append(departments[i][0])

    federal = departments[0][0]

    cursor.execute('SELECT * FROM federal')

    federal_rows = cursor.fetchall()
    federal_companies = []
    for i in range(len(federal_rows)):
        federal_companies.append(federal_rows[i][1])

    data = []
    for department in departments_list:
        statement = 'SELECT * FROM {}'.format(department)
        cursor.execute(statement)
        for index, row in enumerate(cursor):
            if row[1] in federal_companies:
                row_list = list(row)
                row_list.append(department)
                name = row_list[1]
                actions = row_list[2]
                dollars = row_list[3]
                dept = row_list[6]
                if dept != "Federal":
                    data.append((dept, actions, dollars, name))
    print("Departments")
    print(data)
    print("--------------------")

    contractors_table = """CREATE TABLE "contractors"(
                            "id" INTEGER PRIMARY KEY,
                            "vendor" VARCHAR
                            );"""

    actions_table = """CREATE TABLE "actions"(
                        "id" INTEGER PRIMARY KEY,
                        "department" VARCHAR,
                        "actions" INTEGER,
                        "dollars" INTEGER,
                        "contractor_id" INTEGER NOT NULL,
                        FOREIGN KEY("contractor_id") REFERENCES "contractors"("id")
                        );"""

    create_table(con, contractors_table, "contractors")
    create_table(con, actions_table, "actions")

    for company in federal_companies:
        cursor.execute("INSERT INTO contractors (vendor) VALUES (?)", (company,))
        con.commit()

    cursor.execute('SELECT * FROM contractors')
    contractor_id = cursor.fetchall()
    contractor_id = dict(contractor_id)
    contractor_id = dict([(value, key) for key, value in contractor_id.items()])

    print("Contractor ID")
    print(contractor_id)
    print("--------------------")

    for row in data:
        identifier = contractor_id[row[3]]
        cursor.execute("INSERT INTO actions (department, actions, dollars, contractor_id) VALUES (?, ?, ?, ?)",
                       (row[0], row[1], row[2], identifier))
        con.commit()


if __name__ == "__main__":
    run()
