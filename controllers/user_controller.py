from models.user import User


class UserController:
    def __init__(self, db):
        self.db = db

    def get_all(self) -> list[User]:
        rows = self.db.fetchall("SELECT * FROM users ORDER BY username")
        return [User.from_row(r) for r in rows]

    def get(self, user_id: int) -> User | None:
        row = self.db.fetchone("SELECT * FROM users WHERE id = ?", (user_id,))
        return User.from_row(row) if row else None

    def create(self, username: str, password: str) -> User:
        username = username.strip()
        password = password.strip()
        if not username:
            raise ValueError("Username cannot be empty.")
        if not password:
            raise ValueError("Password cannot be empty.")
        if self.db.fetchone("SELECT id FROM users WHERE username = ?", (username,)):
            raise ValueError(f"User '{username}' already exists.")
        cursor = self.db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password),
        )
        return self.get(cursor.lastrowid)

    def authenticate(self, user_id: int, password: str) -> bool:
        row = self.db.fetchone("SELECT password FROM users WHERE id = ?", (user_id,))
        if not row:
            return False
        return row["password"] == password

    def delete(self, user_id: int):
        self.db.execute("DELETE FROM users WHERE id = ?", (user_id,))
