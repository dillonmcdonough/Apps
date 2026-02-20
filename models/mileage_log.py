from dataclasses import dataclass


@dataclass
class MileageLog:
    id: int
    vehicle_id: int
    odometer_reading: float
    date: str
    notes: str = ""
    created_at: str = None

    @classmethod
    def from_row(cls, row) -> "MileageLog":
        return cls(
            id=row["id"],
            vehicle_id=row["vehicle_id"],
            odometer_reading=row["odometer_reading"],
            date=row["date"],
            notes=row["notes"] or "",
            created_at=row["created_at"],
        )
