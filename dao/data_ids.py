from datetime import datetime


class DataIds:

    def __init__(self, sqlite_con):

        self._db = sqlite_con

        self._data_cursor = self._db.cursor()

        self._current_id = None

        self.update_record_control = [False, False]

    def insert_grain_id(self, id_code_value):

        self._data_cursor.execute(
            """
            INSERT INTO
                grains(code_value, weight, humidity, record_date, update_date)
            VALUES(?, ?, ?, ?, ?)
            """,
            (id_code_value, 0, 0, datetime.now(), datetime.now(),)
        )

        self._db.commit()

        self._current_id = self._data_cursor.lastrowid

    def search_grain_id_code(self, id_code_value):

        self._data_cursor.execute(
            "SELECT code_value FROM grains WHERE code_value LIKE ?",
            (''.join([id_code_value, '%']),)
        )

        grain_id_code_record = self._data_cursor.fetchall()

        return grain_id_code_record

    def search_grain_data(self, id_code_value):

        self._data_cursor.execute(
            "SELECT id, weight, humidity FROM grains WHERE code_value LIKE ?",
            (id_code_value,)
        )

        previous_persisted_values = self._data_cursor.fetchone()

        self._current_id = previous_persisted_values[0]

        return previous_persisted_values[1:]

    def get_current_record_id(self):
        return self._current_id

    def close_con(self):

        self._db.close()
