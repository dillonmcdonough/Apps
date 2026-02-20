from dataclasses import dataclass


@dataclass
class Vehicle:
    id: int
    user_id: int
    name: str
    make: str = ""
    model: str = ""
    year: int = None
    license_plate: str = ""
    created_at: str = None

    @classmethod
    def from_row(cls, row) -> "Vehicle":
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            name=row["name"],
            make=row["make"] or "",
            model=row["model"] or "",
            year=row["year"],
            license_plate=row["license_plate"] or "",
            created_at=row["created_at"],
        )

    def display_name(self) -> str:
        """Human-readable name including year/make/model when available."""
        parts = []
        if self.year:
            parts.append(str(self.year))
        if self.make:
            parts.append(self.make)
        if self.model:
            parts.append(self.model)
        if parts:
            return f"{' '.join(parts)} ({self.name})"
        return self.name
