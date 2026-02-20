from models.mileage_log import MileageLog


class MileageController:
    def __init__(self, db):
        self.db = db

    def get_logs(self, vehicle_id: int, limit: int = None) -> list[MileageLog]:
        q = "SELECT * FROM mileage_logs WHERE vehicle_id = ? ORDER BY date DESC, id DESC"
        if limit:
            q += f" LIMIT {int(limit)}"
        rows = self.db.fetchall(q, (vehicle_id,))
        return [MileageLog.from_row(r) for r in rows]

    def get(self, log_id: int) -> MileageLog | None:
        row = self.db.fetchone("SELECT * FROM mileage_logs WHERE id = ?", (log_id,))
        return MileageLog.from_row(row) if row else None

    def add(self, vehicle_id: int, odometer: float, date: str, notes: str = "") -> MileageLog:
        if odometer < 0:
            raise ValueError("Odometer reading cannot be negative.")
        if not date:
            raise ValueError("Date is required.")
        cursor = self.db.execute(
            "INSERT INTO mileage_logs (vehicle_id, odometer_reading, date, notes) VALUES (?,?,?,?)",
            (vehicle_id, odometer, date, notes),
        )
        return self.get(cursor.lastrowid)

    def delete(self, log_id: int):
        self.db.execute("DELETE FROM mileage_logs WHERE id = ?", (log_id,))

    # ── stats ─────────────────────────────────────────────────────────────────

    def latest_odometer(self, vehicle_id: int) -> float | None:
        row = self.db.fetchone(
            "SELECT odometer_reading FROM mileage_logs WHERE vehicle_id = ? ORDER BY date DESC, id DESC LIMIT 1",
            (vehicle_id,),
        )
        return row["odometer_reading"] if row else None

    def total_miles(self, vehicle_id: int) -> float:
        row = self.db.fetchone(
            "SELECT MAX(odometer_reading) - MIN(odometer_reading) AS total FROM mileage_logs WHERE vehicle_id = ?",
            (vehicle_id,),
        )
        return row["total"] if row and row["total"] is not None else 0.0

    def log_count(self, vehicle_id: int) -> int:
        row = self.db.fetchone(
            "SELECT COUNT(*) AS cnt FROM mileage_logs WHERE vehicle_id = ?", (vehicle_id,)
        )
        return row["cnt"] if row else 0
