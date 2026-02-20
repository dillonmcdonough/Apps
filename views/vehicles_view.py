"""
Vehicles — add, edit, delete vehicles for the current user.
"""
import tkinter as tk
from tkinter import messagebox
from app import COLORS
from views.widgets import RoundedButton


class VehiclesView(tk.Frame):
    def __init__(self, parent, app, main_view):
        super().__init__(parent, bg=COLORS["bg"])
        self.app        = app
        self.main_view  = main_view
        self._editing   = None  # Vehicle being edited, or None for new
        self.pack(fill=tk.BOTH, expand=True)
        self._build()

    # ── layout ────────────────────────────────────────────────────────────────

    def _build(self):
        # Two-column: list left, form right
        left = tk.Frame(self, bg=COLORS["bg"], width=330)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(22, 10), pady=20)
        left.pack_propagate(False)

        right = tk.Frame(self, bg=COLORS["bg"])
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 22), pady=20)

        self._build_list(left)
        self._build_form(right)

    def _build_list(self, parent):
        tk.Label(parent, text="Your Vehicles",
                 font=("Segoe UI", 14, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 10))

        wrap = tk.Frame(parent, bg=COLORS["card"])
        wrap.pack(fill=tk.BOTH, expand=True)

        sb = tk.Scrollbar(wrap)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self._listbox = tk.Listbox(
            wrap, bg=COLORS["card"], fg=COLORS["text"],
            selectbackground=COLORS["accent"], selectforeground="#fff",
            font=("Segoe UI", 11), relief=tk.FLAT, highlightthickness=0,
            yscrollcommand=sb.set,
        )
        self._listbox.pack(fill=tk.BOTH, expand=True)
        sb.config(command=self._listbox.yview)
        self._listbox.bind("<<ListboxSelect>>", self._on_select)

        btn_row = tk.Frame(parent, bg=COLORS["bg"])
        btn_row.pack(fill=tk.X, pady=(10, 0))

        RoundedButton(
            btn_row,
            text="New Vehicle",
            command=self._clear_form,
            bg=COLORS["card"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["sidebar"],
            active_bg=COLORS["sidebar"],
            font=("Segoe UI", 10),
            radius=10,
            pad_x=12,
            pad_y=7,
        ).pack(side=tk.LEFT)

        RoundedButton(
            btn_row,
            text="Delete",
            command=self._delete,
            bg=COLORS["danger"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["danger_hover"],
            active_bg=COLORS["danger_hover"],
            font=("Segoe UI", 10, "bold"),
            radius=10,
            pad_x=12,
            pad_y=7,
        ).pack(side=tk.RIGHT)

        self._load_list()

    def _build_form(self, parent):
        self._form_title = tk.Label(parent, text="Add New Vehicle",
                                    font=("Segoe UI", 14, "bold"),
                                    bg=COLORS["bg"], fg=COLORS["text"])
        self._form_title.pack(anchor="w", pady=(0, 14))

        card = tk.Frame(parent, bg=COLORS["sidebar"], padx=26, pady=24)
        card.pack(fill=tk.X)

        FIELDS = [
            ("Nickname *",     "name"),
            ("Make",           "make"),
            ("Model",          "model"),
            ("Year",           "year"),
            ("License Plate",  "license_plate"),
        ]

        self._vars = {}
        for i, (label, key) in enumerate(FIELDS):
            tk.Label(card, text=label, font=("Segoe UI", 10),
                     bg=COLORS["sidebar"], fg=COLORS["muted"]).grid(
                row=i, column=0, sticky="w", pady=6)
            var = tk.StringVar()
            tk.Entry(card, textvariable=var,
                     bg=COLORS["input"], fg=COLORS["text"],
                     insertbackground=COLORS["text"],
                     font=("Segoe UI", 11), relief=tk.FLAT, width=26).grid(
                row=i, column=1, sticky="ew", padx=(16, 0), pady=6, ipady=6, ipadx=6)
            self._vars[key] = var
        card.columnconfigure(1, weight=1)

        btn_row = tk.Frame(card, bg=COLORS["sidebar"])
        btn_row.grid(row=len(FIELDS), column=0, columnspan=2, sticky="ew", pady=(18, 0))

        RoundedButton(
            btn_row,
            text="Clear",
            command=self._clear_form,
            bg=COLORS["card"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["input"],
            active_bg=COLORS["input"],
            font=("Segoe UI", 10),
            radius=10,
            pad_x=16,
            pad_y=8,
        ).pack(side=tk.LEFT)

        self._save_btn = RoundedButton(
            btn_row,
            text="Add Vehicle",
            command=self._save,
            bg=COLORS["accent"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["accent_hover"],
            active_bg=COLORS["accent_hover"],
            font=("Segoe UI", 11, "bold"),
            radius=12,
            pad_x=20,
            pad_y=8,
        )
        self._save_btn.pack(side=tk.RIGHT)

    # ── logic ─────────────────────────────────────────────────────────────────

    def _load_list(self):
        self._listbox.delete(0, tk.END)
        self._vehicles = self.app.vehicles.get_all_for_user(self.app.current_user.id)
        for v in self._vehicles:
            self._listbox.insert(tk.END, f"  {v.display_name()}")

    def _on_select(self, _event):
        sel = self._listbox.curselection()
        if not sel:
            return
        v = self._vehicles[sel[0]]
        self._editing = v
        self._vars["name"].set(v.name)
        self._vars["make"].set(v.make)
        self._vars["model"].set(v.model)
        self._vars["year"].set(str(v.year) if v.year else "")
        self._vars["license_plate"].set(v.license_plate)
        self._form_title.configure(text="Edit Vehicle")
        self._save_btn.set_text("Update Vehicle")

    def _clear_form(self):
        self._editing = None
        for var in self._vars.values():
            var.set("")
        self._form_title.configure(text="Add New Vehicle")
        self._save_btn.set_text("Add Vehicle")
        self._listbox.selection_clear(0, tk.END)

    def _save(self):
        name          = self._vars["name"].get().strip()
        make          = self._vars["make"].get().strip()
        model         = self._vars["model"].get().strip()
        year_s        = self._vars["year"].get().strip()
        license_plate = self._vars["license_plate"].get().strip()

        year = None
        if year_s:
            if not year_s.isdigit():
                messagebox.showerror("Input Error", "Year must be a number.", parent=self)
                return
            year = int(year_s)

        try:
            if self._editing:
                self.app.vehicles.update(self._editing.id, name, make, model, year, license_plate)
                messagebox.showinfo("Saved", "Vehicle updated successfully.", parent=self)
            else:
                self.app.vehicles.create(self.app.current_user.id, name, make, model, year, license_plate)
                messagebox.showinfo("Saved", "Vehicle added successfully.", parent=self)

            self._clear_form()
            self._load_list()
            self.main_view.refresh_vehicle_selector()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _delete(self):
        sel = self._listbox.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Select a vehicle to delete.", parent=self)
            return
        v = self._vehicles[sel[0]]
        if not messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{v.display_name()}' and ALL its mileage history?\n\nThis cannot be undone.",
            parent=self,
        ):
            return
        self.app.vehicles.delete(v.id)
        if self.app.current_vehicle and self.app.current_vehicle.id == v.id:
            self.app.current_vehicle = None
        self._clear_form()
        self._load_list()
        self.main_view.refresh_vehicle_selector()
