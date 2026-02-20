from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password: str
    created_at: str = None

    @classmethod
    def from_row(cls, row) -> "User":
        return cls(
            id=row["id"],
            username=row["username"],
            password=row["password"],
            created_at=row["created_at"],
        )

    def __str__(self):
        return self.username
