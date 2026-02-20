"""
Mileage Log — add entries and view full history for the selected vehicle.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from app import COLORS
from views.widgets import RoundedButton


class MileageView(tk.Frame):
    def __init__(self, parent, app, main_view):
        super().__init__(parent, bg=COLORS["bg"])
        self.app       = app
        self.main_view = main_view
        self.pack(fill=tk.BOTH, expand=True)
        self._build()

    # ── layout ────────────────────────────────────────────────────────────────

    def _build(self):
        if not self.app.current_vehicle:
            tk.Label(self,
                     text="No vehicle selected.\nGo to Vehicles to add or select one.",
                     font=("Segoe UI", 13), bg=COLORS["bg"], fg=COLORS["muted"],
                     justify=tk.CENTER).place(relx=0.5, rely=0.5, anchor="center")
            return

        self._build_entry_form()
        self._build_history()

    def _build_entry_form(self):
        veh = self.app.current_vehicle
        top = tk.Frame(self, bg=COLORS["bg"])
        top.pack(fill=tk.X, padx=22, pady=18)

        tk.Label(top, text=f"Vehicle: {veh.display_name()}",
                 font=("Segoe UI", 11), bg=COLORS["bg"],
                 fg=COLORS["muted"]).pack(anchor="w", pady=(0, 8))

        card = tk.Frame(top, bg=COLORS["sidebar"], padx=22, pady=16)
        card.pack(fill=tk.X)

        tk.Label(card, text="New Mileage Entry",
                 font=("Segoe UI", 12, "bold"),
                 bg=COLORS["sidebar"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 10))

        fields_row = tk.Frame(card, bg=COLORS["sidebar"])
        fields_row.pack(fill=tk.X)

        # Date
        df = tk.Frame(fields_row, bg=COLORS["sidebar"])
        df.pack(side=tk.LEFT, padx=(0, 18))
        tk.Label(df, text="Date (YYYY-MM-DD)",
                 font=("Segoe UI", 9),
                 bg=COLORS["sidebar"], fg=COLORS["muted"]).pack(anchor="w")
        self._date_var = tk.StringVar(value=str(date.today()))
        tk.Entry(df, textvariable=self._date_var,
                 bg=COLORS["input"], fg=COLORS["text"],
                 insertbackground=COLORS["text"],
                 font=("Segoe UI", 11), relief=tk.FLAT, width=15).pack(ipady=6, ipadx=6)

        # Odometer
        of = tk.Frame(fields_row, bg=COLORS["sidebar"])
        of.pack(side=tk.LEFT, padx=(0, 18))
        tk.Label(of, text="Odometer (miles)",
                 font=("Segoe UI", 9),
                 bg=COLORS["sidebar"], fg=COLORS["muted"]).pack(anchor="w")
        self._odo_var = tk.StringVar()

        # Pre-fill with latest + 1 as a hint
        latest = self.app.mileage.latest_odometer(self.app.current_vehicle.id)
        if latest is not None:
            self._odo_var.set(f"{latest:.0f}")

        tk.Entry(of, textvariable=self._odo_var,
                 bg=COLORS["input"], fg=COLORS["text"],
                 insertbackground=COLORS["text"],
                 font=("Segoe UI", 11), relief=tk.FLAT, width=16).pack(ipady=6, ipadx=6)

        # Notes
        nf = tk.Frame(fields_row, bg=COLORS["sidebar"])
        nf.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 18))
        tk.Label(nf, text="Notes (optional)",
                 font=("Segoe UI", 9),
                 bg=COLORS["sidebar"], fg=COLORS["muted"]).pack(anchor="w")
        self._notes_var = tk.StringVar()
        tk.Entry(nf, textvariable=self._notes_var,
                 bg=COLORS["input"], fg=COLORS["text"],
                 insertbackground=COLORS["text"],
                 font=("Segoe UI", 11), relief=tk.FLAT).pack(fill=tk.X, ipady=6, ipadx=6)

        # Add button
        RoundedButton(
            fields_row,
            text="Add Log",
            command=self._add_log,
            bg=COLORS["accent"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["accent_hover"],
            active_bg=COLORS["accent_hover"],
            font=("Segoe UI", 11, "bold"),
            radius=12,
            pad_x=18,
            pad_y=8,
        ).pack(side=tk.LEFT, anchor="s")

    def _build_history(self):
        bottom = tk.Frame(self, bg=COLORS["bg"])
        bottom.pack(fill=tk.BOTH, expand=True, padx=22, pady=(0, 18))

        hdr = tk.Frame(bottom, bg=COLORS["bg"])
        hdr.pack(fill=tk.X, pady=(0, 8))
        tk.Label(hdr, text="Mileage History",
                 font=("Segoe UI", 13, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(side=tk.LEFT)
        RoundedButton(
            hdr,
            text="Delete Selected",
            command=self._delete_log,
            bg=COLORS["danger"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["danger_hover"],
            active_bg=COLORS["danger_hover"],
            font=("Segoe UI", 10),
            radius=10,
            pad_x=12,
            pad_y=6,
        ).pack(side=tk.RIGHT)

        tree_wrap = tk.Frame(bottom, bg=COLORS["card"])
        tree_wrap.pack(fill=tk.BOTH, expand=True)

        cols = ("date", "odometer", "notes")
        self._tree = ttk.Treeview(tree_wrap, columns=cols,
                                  show="headings", selectmode="browse")

        self._tree.heading("date",     text="Date",              anchor="center")
        self._tree.heading("odometer", text="Odometer (mi)",     anchor="center")
        self._tree.heading("notes",    text="Notes",             anchor="w")

        self._tree.column("date",     width=130, anchor="center", stretch=False)
        self._tree.column("odometer", width=160, anchor="center", stretch=False)
        self._tree.column("notes",    width=500, anchor="w")

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)

        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self._load_history()

    # ── logic ─────────────────────────────────────────────────────────────────

    def _load_history(self):
        self._tree.delete(*self._tree.get_children())
        self._logs = self.app.mileage.get_logs(self.app.current_vehicle.id)
        for log in self._logs:
            self._tree.insert("", "end", iid=str(log.id),
                              values=(log.date,
                                      f"{log.odometer_reading:,.1f}",
                                      log.notes))

    def _add_log(self):
        date_s  = self._date_var.get().strip()
        odo_s   = self._odo_var.get().strip().replace(",", "")
        notes   = self._notes_var.get().strip()

        if not date_s:
            messagebox.showerror("Input Error", "Date is required.", parent=self)
            return
        if not odo_s:
            messagebox.showerror("Input Error", "Odometer reading is required.", parent=self)
            return
        try:
            odometer = float(odo_s)
        except ValueError:
            messagebox.showerror("Input Error", "Odometer must be a number.", parent=self)
            return

        try:
            self.app.mileage.add(self.app.current_vehicle.id, odometer, date_s, notes)
            self._odo_var.set("")
            self._notes_var.set("")
            self._load_history()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _delete_log(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Select a log entry to delete.", parent=self)
            return
        if not messagebox.askyesno("Confirm", "Delete this mileage entry?", parent=self):
            return
        self.app.mileage.delete(int(sel[0]))
        self._load_history()
