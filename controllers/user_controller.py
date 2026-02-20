import hashlib
import hmac
import secrets

from models.user import User


def _hash_password(password: str) -> str:
    """Hash a password using PBKDF2-SHA256 with a random salt."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 260_000)
    return f"pbkdf2$sha256${salt}${dk.hex()}"


def _verify_password(stored: str, provided: str) -> bool:
    """Verify a password. Handles both hashed and legacy plaintext passwords."""
    if stored and stored.startswith("pbkdf2$sha256$"):
        parts = stored.split("$")
        if len(parts) != 4:
            return False
        _, _, salt, expected_hash = parts
        dk = hashlib.pbkdf2_hmac("sha256", provided.encode("utf-8"), salt.encode("utf-8"), 260_000)
        return hmac.compare_digest(dk.hex(), expected_hash)
    # Legacy plaintext comparison
    return stored == provided


class UserController:
    def __init__(self, db):
        self.db = db

    def get_all(self) -> list[User]:
        rows = self.db.fetchall("SELECT * FROM users ORDER BY username")
        return [User.from_row(r) for r in rows]

    def get(self, user_id: int) -> User | None:
        row = self.db.fetchone("SELECT * FROM users WHERE id = ?", (user_id,))
        return User.from_row(row) if row else None

    def create(self, username: str, password: str, is_admin: bool = False) -> User:
        username = username.strip()
        password = password.strip()
        if not username:
            raise ValueError("Username cannot be empty.")
        if not password:
            raise ValueError("Password cannot be empty.")
        if self.db.fetchone("SELECT id FROM users WHERE username = ?", (username,)):
            raise ValueError(f"User '{username}' already exists.")
        hashed = _hash_password(password)
        cursor = self.db.execute(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            (username, hashed, 1 if is_admin else 0),
        )
        return self.get(cursor.lastrowid)

    def authenticate(self, user_id: int, password: str) -> bool:
        row = self.db.fetchone("SELECT password FROM users WHERE id = ?", (user_id,))
        if not row:
            return False
        stored = row["password"]
        if _verify_password(stored, password):
            # Auto-migrate legacy plaintext passwords to hashed on successful login
            if not stored.startswith("pbkdf2$sha256$"):
                self.db.execute(
                    "UPDATE users SET password = ? WHERE id = ?",
                    (_hash_password(password), user_id),
                )
            return True
        return False

    def set_password(self, user_id: int, new_password: str):
        new_password = new_password.strip()
        if not new_password:
            raise ValueError("Password cannot be empty.")
        self.db.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (_hash_password(new_password), user_id),
        )

    def set_admin(self, user_id: int, is_admin: bool):
        self.db.execute(
            "UPDATE users SET is_admin = ? WHERE id = ?",
            (1 if is_admin else 0, user_id),
        )

    def delete(self, user_id: int):
        self.db.execute("DELETE FROM users WHERE id = ?", (user_id,))
