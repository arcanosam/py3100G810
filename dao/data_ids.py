from datetime import datetime

from sqlite3 import DatabaseError


class DataIds:

    def __init__(self, sqlite_con):

        self._db = sqlite_con

        self._data_cursor = self._db.cursor()

        self._current_id = None

    def _run_sql(self, statement, parameters=None, db_commit=False):

        try:

            if parameters is None:
                self._data_cursor.execute(statement)
            else:
                self._data_cursor.execute(statement, parameters)

                if db_commit:
                    self._db.commit()

        except DatabaseError as e:
            return False, e

        return True, ''

    def insert_grain_id(self, id_code_value):

        sql_result = self._run_sql(
            """
            INSERT INTO
                grains(code_value, weight, humidity, record_date, update_date)
            VALUES(?, ?, ?, ?, ?)
            """,
            (id_code_value, 0, 0, datetime.now(), datetime.now(),),
            True
        )

        if sql_result[0]:
            self._current_id = self._data_cursor.lastrowid
            return sql_result
        else:
            return sql_result

    def update_weigth_humidity_value(self, grain_attribute_value, grain_weight=True):

        if grain_weight:
            sql_result = self._run_sql(
                """
                UPDATE 
                    grains
                SET
                    weight=?, update_date=?
                WHERE
                    id=?                    
                """,
                (grain_attribute_value, datetime.now(), self._current_id,),
                True
            )

        else:
            sql_result = self._run_sql(
                """
                UPDATE 
                    grains
                SET
                    humidity=?, update_date=?
                WHERE
                    id=?                    
                """,
                (grain_attribute_value, datetime.now(), self._current_id,),
                True
            )

        return sql_result

    def search_grain_id_code(self, id_code_value):

        sql_result = self._run_sql(
            "SELECT code_value FROM grains WHERE code_value LIKE ?",
            (''.join([id_code_value, '%']),)
        )

        if sql_result[0]:

            grain_id_record_found = self._data_cursor.fetchall()

            if len(grain_id_record_found):
                return True, grain_id_record_found
            else:
                return False, None
        else:
            return sql_result

    def search_grain_data(self, id_code_value):

        sql_result = self._run_sql(
            "SELECT id, weight, humidity FROM grains WHERE code_value LIKE ?",
            (id_code_value,)
        )

        if sql_result[0]:

            previous_persisted_values = self._data_cursor.fetchone()

            self._current_id = previous_persisted_values[0]

            return True, previous_persisted_values[1:]
        else:
            return sql_result

    def get_all_grains(self):

        sql_result = self._run_sql(
            """SELECT 
                    code_value, weight, humidity, record_date, update_date
                FROM
                    grains"""
        )

        if sql_result[0]:
            return True, self._data_cursor.fetchall()
        else:
            return sql_result

    def get_current_record_id(self):
        return self._current_id

    def clean_current_record(self):

        self._current_id = None

    def rebuild_db(self):

        try:

            self._data_cursor.executescript(
                """
                BEGIN TRANSACTION;
                DROP TABLE IF EXISTS "grains";
                CREATE TABLE IF NOT EXISTS "grains" (
                    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                    "code_value"	TEXT NOT NULL,
                    "weight"	REAL NOT NULL,
                    "humidity"	REAL NOT NULL,
                    "record_date"	TEXT NOT NULL,
                    "update_date"	TEXT NOT NULL
                );
                DROP INDEX IF EXISTS "grains_barcode_uindex";
                CREATE UNIQUE INDEX IF NOT EXISTS "grains_barcode_uindex" ON "grains" (
                    "code_value"
                );
                COMMIT;"""
            )

        except DatabaseError as e:
            return False, e

        return True, ''

    def close_con(self):

        self._db.close()
