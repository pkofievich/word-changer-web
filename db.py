import sqlite3

class DataBase:
    def __init__(self, db_name: str, table_name: str) -> None:
        self.table_name = table_name
        self.connection = sqlite3.connect(db_name, timeout=10)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users( id INT, dicts TEXT )")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS dicts( id INT, name TEXT, dict TEXT )")
        self.connection.commit()

    def close(self) -> None:
        self.connection.commit()
        self.connection.close()

    def get(self, page_id: str, name: str = None) -> list:
        if name:
            return self.cursor.execute(f"SELECT {name} FROM {self.table_name} WHERE id = ?", (page_id,)).fetchone()
        else:
            return self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (page_id,)).fetchone()

    def create(self, page_id: str) -> None:
        if not self.get(page_id):
            self.cursor.execute(f"INSERT INTO {self.table_name} (id) VALUES (?)", (page_id,))
            self.connection.commit()

    def remove(self, page_id: str) -> None:
        if self.get(page_id):
            self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (page_id,))
            self.connection.commit()

    def enter(self, page_id: str, name: str, content: str) -> bool:
        rows = self.cursor.execute(f"UPDATE {self.table_name} SET {name} = ? WHERE id = ?", (content, page_id)).rowcount
        self.connection.commit()
        if rows == 0:
            return False
        else:
            return True

    def __del__(self) -> None:
        self.close()