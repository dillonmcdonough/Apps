"""
Dashboard — overview of the selected vehicle and all user vehicles.
"""
import tkinter as tk
from tkinter import ttk
from app import COLORS
from views.widgets import RoundedPanel


class DashboardView(tk.Frame):
    def __init__(self, parent, app, main_view):
        super().__init__(parent, bg=COLORS["bg"])
        self.app       = app
        self.main_view = main_view
        self.pack(fill=tk.BOTH, expand=True)
        self._build()

    def _build(self):
        # Scrollable canvas wrapper
        canvas = tk.Canvas(self, bg=COLORS["bg"], highlightthickness=0)
        vsb    = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        inner  = tk.Frame(canvas, bg=COLORS["bg"])

        inner.bind("<Configure>",
                   lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Mouse-wheel scrolling
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self._fill(inner)

    def _fill(self, f):
        user    = self.app.current_user
        vehicle = self.app.current_vehicle

        # ── greeting ──────────────────────────────────────────────────────────
        hdr = tk.Frame(f, bg=COLORS["bg"])
        hdr.pack(fill=tk.X, padx=24, pady=20)
        tk.Label(hdr, text=f"Welcome back, {user.username}!",
                 font=("Segoe UI", 20, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w")

        if not vehicle:
            tk.Label(hdr,
                     text="No vehicle selected — head to Vehicles to add one.",
                     font=("Segoe UI", 11), bg=COLORS["bg"],
                     fg=COLORS["accent"]).pack(anchor="w", pady=(4, 0))
            return

        tk.Label(hdr, text=f"Viewing: {vehicle.display_name()}",
                 font=("Segoe UI", 11), bg=COLORS["bg"],
                 fg=COLORS["muted"]).pack(anchor="w", pady=(3, 0))

        # ── stat cards ────────────────────────────────────────────────────────
        total   = self.app.mileage.total_miles(vehicle.id)
        count   = self.app.mileage.log_count(vehicle.id)
        latest  = self.app.mileage.latest_odometer(vehicle.id)

        stats = [
            ("Total Miles Tracked", f"{total:,.1f}"),
            ("Mileage Log Entries", str(count)),
            ("Latest Odometer",     f"{latest:,.1f}" if latest is not None else "—"),
        ]

        row = tk.Frame(f, bg=COLORS["bg"])
        row.pack(fill=tk.X, padx=24, pady=(0, 20))
        for label, value in stats:
            card = RoundedPanel(
                row,
                bg=COLORS["surface"],
                border_color=COLORS["border"],
                radius=16,
                pad_x=22,
                pad_y=16,
            )
            card.pack(side=tk.LEFT, padx=(0, 14))
            card_body = card.content
            tk.Label(card_body, text=value,
                     font=("Segoe UI", 26, "bold"),
                     bg=COLORS["surface"], fg=COLORS["accent"]).pack(anchor="w")
            tk.Label(card_body, text=label,
                     font=("Segoe UI", 9),
                     bg=COLORS["surface"], fg=COLORS["muted"]).pack(anchor="w")

        # ── recent logs ───────────────────────────────────────────────────────
        self._section(f, "Recent Mileage Logs")
        logs = self.app.mileage.get_logs(vehicle.id, limit=6)
        logs_f = tk.Frame(f, bg=COLORS["bg"])
        logs_f.pack(fill=tk.X, padx=24)

        if not logs:
            tk.Label(logs_f, text="No entries yet — add your first log in Mileage Log.",
                     font=("Segoe UI", 11), bg=COLORS["bg"],
                     fg=COLORS["muted"]).pack(anchor="w", pady=6)
        else:
            for log in logs:
                r = RoundedPanel(
                    logs_f,
                    bg=COLORS["surface"],
                    border_color=COLORS["border"],
                    radius=12,
                    pad_x=16,
                    pad_y=10,
                )
                r.pack(fill=tk.X, pady=3)
                row_body = r.content
                tk.Label(row_body, text=log.date, width=13, anchor="w",
                         font=("Segoe UI", 10),
                         bg=COLORS["surface"], fg=COLORS["muted"]).pack(side=tk.LEFT)
                tk.Label(row_body, text=f"{log.odometer_reading:,.1f} mi",
                         font=("Segoe UI", 11, "bold"),
                         bg=COLORS["surface"], fg=COLORS["text"]).pack(side=tk.LEFT, padx=12)
                if log.notes:
                    tk.Label(row_body, text=log.notes,
                             font=("Segoe UI", 10),
                             bg=COLORS["surface"], fg=COLORS["muted"]).pack(side=tk.LEFT)

        # ── all vehicles summary ───────────────────────────────────────────────
        self._section(f, "All Your Vehicles")
        all_vehicles = self.app.vehicles.get_all_for_user(user.id)
        vf = tk.Frame(f, bg=COLORS["bg"])
        vf.pack(fill=tk.X, padx=24, pady=(0, 24))

        if not all_vehicles:
            tk.Label(vf, text="No vehicles added yet.",
                     font=("Segoe UI", 11), bg=COLORS["bg"],
                     fg=COLORS["muted"]).pack(anchor="w")
        else:
            for v in all_vehicles:
                vr = RoundedPanel(
                    vf,
                    bg=COLORS["surface"],
                    border_color=COLORS["border"],
                    radius=12,
                    pad_x=16,
                    pad_y=11,
                )
                vr.pack(fill=tk.X, pady=3)
                vr_body = vr.content

                indicator = "▶ " if (self.app.current_vehicle and v.id == self.app.current_vehicle.id) else "    "
                tk.Label(vr_body, text=f"{indicator}{v.display_name()}",
                         font=("Segoe UI", 11, "bold"),
                         bg=COLORS["surface"], fg=COLORS["text"]).pack(side=tk.LEFT)

                v_miles = self.app.mileage.total_miles(v.id)
                v_count = self.app.mileage.log_count(v.id)
                tk.Label(vr_body, text=f"{v_miles:,.0f} mi tracked  ·  {v_count} logs",
                         font=("Segoe UI", 10),
                         bg=COLORS["surface"], fg=COLORS["muted"]).pack(side=tk.RIGHT)

    def _section(self, parent, title: str):
        tk.Label(parent, text=title,
                 font=("Segoe UI", 14, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", padx=24, pady=(16, 6))
