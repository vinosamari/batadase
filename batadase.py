import sqlite3
from pprint import pprint
from bd_utils import generate_id, create_id


class Batadase:
    """
    Creates database with NAME = db_name
    """

    def __init__(self, db_name: str) -> None:
        self.db_name: str = db_name
        self.table_name: str = ''

    def create_table(self, table_name: str, columns_array: list) -> bool:
        """
        Creates table using columns array as db columns

        columns_array_example = ['column_name column_type column_NULL', id integer PRIMARY KEY', 'name text NOT NULL',
           'dept text NOT NULL', 'salary integer']
        """
        columns_array_str = ', '.join(columns_array)
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name}({columns_array_str});")
        self.setTableName(table_name)
        return True

    def setTableName(self, table_name: str):
        """
        SETS TABLE NAME CLASS VARIABLE TO table_name
        """
        self.table_name = table_name

    def getTableName(self):
        """
        Returns name of the current table in the database
        """
        return self.table_name

    def view_table(self):
        """
        Returns array of all entries in the database
        """
        table = []
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT * FROM {self.table_name}')
            table = cursor.fetchall()
            return table

    def add_row(self, query_titles: list, query_values: list):
        """
        Adds row to database using query as column values. Query should be two arrays. [columnTitles], [columnValues]
        """
        query_values_question_marks = ",".join(list('?' * len(query_values)))
        column_titles = ', '.join(query_titles)
        with sqlite3.connect(self.db_name) as db:
            try:
                cursor = db.cursor()
                _SQL = "INSERT INTO " + self.getTableName() + " (" + column_titles + \
                    ") VALUES(" + query_values_question_marks + ")"
                cursor.execute(_SQL, [val for val in query_values])
                return True
            except sqlite3.IntegrityError as e:
                print('Duplicate Data. A column with that ID already exists.')
                return False

    def delete_row_with_column_details(self, column_query: list):
        """
        Takes in an array of a column's details to delete. ['name', 'itemToDelete'] 
        """
        queryTitle, queryValue = column_query[0], column_query[1]
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            _SQL = 'DELETE FROM ' + self.getTableName() + \
                ' WHERE ' + queryTitle + ' = ?'
            cursor.execute(_SQL, [queryValue])
            return True

    def update_row(self, row_identifier_array: list, update_array: list):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            _SQL = 'UPDATE ' + self.table_name + ' SET ' + \
                update_array[0] + " = " + f"'{update_array[1]}'" + ' WHERE ' + \
                row_identifier_array[0] + ' = ?'
            cursor.execute(_SQL, [str(row_identifier_array[1])])
            # _SQL = 'SELECT * FROM ' + self.getTableName() + ' WHERE ' + \
            # row_identifier_array[0] + ' = ' + row_identifier_array[1]
            # cursor.execute(_SQL)
            result = []
            for x in cursor.fetchall():
                result = x
            return result

    def find_row(self, row_identifier_array: list):
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            QUERY = 'SELECT * FROM ' + self.getTableName() + ' WHERE ' + \
                row_identifier_array[0] + ' = ?'
            cursor.execute(QUERY,  [row_identifier_array[1]])
            result = cursor.fetchall()
            if result == []:
                return f'No matching items found for {row_identifier_array[0]} = {row_identifier_array[1]}'
            else:
                return result

    def row_count(self):
        """
        Returns the number of items in the database
        """
        with sqlite3.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute(f'SELECT * FROM {self.table_name}')
            return f"{len(cursor.fetchall())} items in {self.table_name}"

    def create_dummy_data(self, number: int):
        """
        Creates dummy data for number amount and populates database
        """
        for i in range(1, number+1):
            if i % 2 == 0:
                row_titles = ['id', 'name', 'desc', 'done']
                row_values = [
                    generate_id(10), f"{i}:{i}", f"ITEM {i}", f"{i*i} UNFINISHED"]
                self.add_row(row_titles, row_values)
                continue
            # else:
            row_titles = ['id', 'name', 'desc', 'done']
            row_values = [
                generate_id(10), f"User {i}", f"ITEM {i}", f"{i*i} DONE"]
            self.add_row(row_titles, row_values)
        return True

    def __repr__(self) -> str:
        return self.db_name


# CREATE NEW DB
bd = Batadase('test-1.db')
cols_titles_array = ['id blob PRIMARY KEY',
                     'name text', 'desc text', 'done text']
bd.create_table("TODO_LIST", cols_titles_array)

# # # POPULATE TABLE
bd.create_dummy_data(10)


# # # UPDATE ROW
rowToUpdate = ['name', 'User 1']
udpateDetails = ['name', 'New Name']
# bd.update_row(rowToUpdate, udpateDetails)
pprint(bd.view_table())
