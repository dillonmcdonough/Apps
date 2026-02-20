"""
MainView — persistent shell shown after login.
Contains the sidebar navigation, top bar with vehicle selector,
and a content area that swaps child views.

To add a new page:
  1. Add an entry to PAGES.
  2. Add the matching import + elif branch in show_page().
"""
import tkinter as tk
from tkinter import ttk
from app import COLORS


class MainView(tk.Frame):
    # ── Register pages here to extend the app ─────────────────────────────────
    PAGES = [
        ("Dashboard",   "dashboard"),
        ("Vehicles",    "vehicles"),
        ("Mileage Log", "mileage"),
        # ("Service",   "service"),   ← example future page
    ]

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self._active_page = tk.StringVar(value="dashboard")
        self.pack(fill=tk.BOTH, expand=True)
        self._build()
        self.show_page("dashboard")

    # ── construction ──────────────────────────────────────────────────────────

    def _build(self):
        self._build_sidebar()
        self._build_content_area()

    def _build_sidebar(self):
        sb = tk.Frame(self, bg=COLORS["sidebar"], width=210)
        sb.pack(side=tk.LEFT, fill=tk.Y)
        sb.pack_propagate(False)
        self._sidebar = sb

        # Logo
        tk.Label(sb, text="TORQUE", font=("Segoe UI", 20, "bold"),
                 bg=COLORS["sidebar"], fg=COLORS["accent"]).pack(pady=(22, 0))
        tk.Label(sb, text="TRACKER", font=("Segoe UI", 11, "bold"),
                 bg=COLORS["sidebar"], fg=COLORS["text"]).pack()
        tk.Frame(sb, bg=COLORS["card"], height=1).pack(fill=tk.X, padx=15, pady=12)

        # Logged-in user badge
        badge = tk.Frame(sb, bg=COLORS["card"], padx=12, pady=10)
        badge.pack(fill=tk.X, padx=12)
        tk.Label(badge, text="Logged in as", font=("Segoe UI", 8),
                 bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w")
        tk.Label(badge, text=self.app.current_user.username,
                 font=("Segoe UI", 12, "bold"),
                 bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w")

        tk.Frame(sb, bg=COLORS["card"], height=1).pack(fill=tk.X, padx=15, pady=12)

        # Nav buttons
        self._nav_btns = {}
        for label, page_id in self.PAGES:
            btn = tk.Button(sb, text=f"  {label}",
                            command=lambda p=page_id: self.show_page(p),
                            bg=COLORS["sidebar"], fg=COLORS["text"],
                            font=("Segoe UI", 11), relief=tk.FLAT,
                            anchor="w", padx=8, pady=11, cursor="hand2",
                            activebackground=COLORS["card"],
                            activeforeground=COLORS["accent"])
            btn.pack(fill=tk.X)
            self._nav_btns[page_id] = btn

        # Logout at bottom
        tk.Frame(sb, bg=COLORS["card"], height=1).pack(fill=tk.X, padx=15, side=tk.BOTTOM, pady=5)
        tk.Button(sb, text="  Logout", command=self.app.logout,
                  bg=COLORS["sidebar"], fg=COLORS["muted"],
                  font=("Segoe UI", 10), relief=tk.FLAT,
                  anchor="w", padx=8, pady=9, cursor="hand2",
                  activebackground=COLORS["card"]).pack(side=tk.BOTTOM, fill=tk.X)

    def _build_content_area(self):
        content = tk.Frame(self, bg=COLORS["bg"])
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Top bar
        topbar = tk.Frame(content, bg=COLORS["sidebar"], height=58)
        topbar.pack(fill=tk.X)
        topbar.pack_propagate(False)

        self._page_title = tk.Label(topbar, text="",
                                    font=("Segoe UI", 16, "bold"),
                                    bg=COLORS["sidebar"], fg=COLORS["text"])
        self._page_title.pack(side=tk.LEFT, padx=22, pady=14)

        # Vehicle selector (right side of top bar)
        vs = tk.Frame(topbar, bg=COLORS["sidebar"])
        vs.pack(side=tk.RIGHT, padx=18, pady=10)
        tk.Label(vs, text="Vehicle:", font=("Segoe UI", 10),
                 bg=COLORS["sidebar"], fg=COLORS["muted"]).pack(side=tk.LEFT, padx=(0, 6))
        self._vehicle_var = tk.StringVar()
        self._vehicle_combo = ttk.Combobox(vs, textvariable=self._vehicle_var,
                                           width=28, state="readonly")
        self._vehicle_combo.pack(side=tk.LEFT)
        self._vehicle_combo.bind("<<ComboboxSelected>>", self._on_vehicle_changed)

        # Swappable page frame
        self._page_frame = tk.Frame(content, bg=COLORS["bg"])
        self._page_frame.pack(fill=tk.BOTH, expand=True)

        self.refresh_vehicle_selector()

    # ── vehicle selector ──────────────────────────────────────────────────────

    def refresh_vehicle_selector(self):
        """Reload vehicle list from DB and update combobox."""
        self._vehicles = self.app.vehicles.get_all_for_user(self.app.current_user.id)
        if self._vehicles:
            names = [v.display_name() for v in self._vehicles]
            self._vehicle_combo.configure(values=names, state="readonly")

            # Preserve selection if vehicle still exists
            if self.app.current_vehicle:
                ids = [v.id for v in self._vehicles]
                if self.app.current_vehicle.id in ids:
                    idx = ids.index(self.app.current_vehicle.id)
                    self._vehicle_combo.current(idx)
                    return
            self._vehicle_combo.current(0)
            self.app.current_vehicle = self._vehicles[0]
        else:
            self._vehicle_combo.configure(values=["No vehicles — add one!"], state="readonly")
            self._vehicle_combo.current(0)
            self.app.current_vehicle = None

    def _on_vehicle_changed(self, _event):
        idx = self._vehicle_combo.current()
        if self._vehicles and idx >= 0:
            self.app.current_vehicle = self._vehicles[idx]
            self.show_page(self._active_page.get())

    # ── page switching ────────────────────────────────────────────────────────

    def show_page(self, page_id: str):
        self._active_page.set(page_id)

        # Highlight active nav button
        for pid, btn in self._nav_btns.items():
            if pid == page_id:
                btn.configure(bg=COLORS["card"], fg=COLORS["accent"],
                              font=("Segoe UI", 11, "bold"))
            else:
                btn.configure(bg=COLORS["sidebar"], fg=COLORS["text"],
                              font=("Segoe UI", 11))

        titles = {p[1]: p[0] for p in self.PAGES}
        self._page_title.configure(text=titles.get(page_id, page_id.title()))

        for w in self._page_frame.winfo_children():
            w.destroy()

        # ── route ─────────────────────────────────────────────────────────────
        if page_id == "dashboard":
            from views.dashboard_view import DashboardView
            DashboardView(self._page_frame, self.app, self)
        elif page_id == "vehicles":
            from views.vehicles_view import VehiclesView
            VehiclesView(self._page_frame, self.app, self)
        elif page_id == "mileage":
            from views.mileage_view import MileageView
            MileageView(self._page_frame, self.app, self)
        # Add new pages here ↑
