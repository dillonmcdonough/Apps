from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    username: str
    password: str
    is_admin: bool = False
    created_at: str = None

    @classmethod
    def from_row(cls, row) -> "User":
        try:
            is_admin = bool(row["is_admin"])
        except (IndexError, KeyError):
            is_admin = False
        return cls(
            id=row["id"],
            username=row["username"],
            password=row["password"],
            is_admin=is_admin,
            created_at=row["created_at"],
        )

    def __str__(self):
        return self.username
