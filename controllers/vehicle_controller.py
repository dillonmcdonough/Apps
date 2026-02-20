from models.vehicle import Vehicle


class VehicleController:
    def __init__(self, db):
        self.db = db

    def get_all_for_user(self, user_id: int) -> list[Vehicle]:
        rows = self.db.fetchall(
            "SELECT * FROM vehicles WHERE user_id = ? ORDER BY name", (user_id,)
        )
        return [Vehicle.from_row(r) for r in rows]

    def get(self, vehicle_id: int) -> Vehicle | None:
        row = self.db.fetchone("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
        return Vehicle.from_row(row) if row else None

    def create(self, user_id: int, name: str, make="", model="", year=None, license_plate="") -> Vehicle:
        name = name.strip()
        if not name:
            raise ValueError("Vehicle name cannot be empty.")
        cursor = self.db.execute(
            "INSERT INTO vehicles (user_id, name, make, model, year, license_plate) VALUES (?,?,?,?,?,?)",
            (user_id, name, make, model, year, license_plate),
        )
        return self.get(cursor.lastrowid)

    def update(self, vehicle_id: int, name: str, make="", model="", year=None, license_plate="") -> Vehicle:
        name = name.strip()
        if not name:
            raise ValueError("Vehicle name cannot be empty.")
        self.db.execute(
            "UPDATE vehicles SET name=?, make=?, model=?, year=?, license_plate=? WHERE id=?",
            (name, make, model, year, license_plate, vehicle_id),
        )
        return self.get(vehicle_id)

    def delete(self, vehicle_id: int):
        self.db.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
