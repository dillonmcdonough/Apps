"""
TorqueTrackerApp — top-level orchestrator.
Owns the database, controllers, and current session state (user / vehicle).
Views call back into this object to navigate or mutate state.
"""
import tkinter as tk
from tkinter import ttk

from database import Database
from controllers import UserController, VehicleController, MileageController


# ── shared colour palette ─────────────────────────────────────────────────────
COLORS = {
    "bg":      "#1a1a2e",
    "sidebar": "#16213e",
    "card":    "#0f3460",
    "accent":  "#e94560",
    "accent_hover": "#cf3851",
    "text":    "#e2e8f0",
    "muted":   "#94a3b8",
    "input":   "#0d2137",
    "danger":  "#c0392b",
    "danger_hover": "#a93226",
    "success": "#27ae60",
    "button_text": "#f8fafc",
}


def apply_global_styles():
    """Configure ttk styles used across all views."""
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TCombobox",
                    fieldbackground=COLORS["card"],
                    background=COLORS["card"],
                    foreground=COLORS["text"],
                    selectbackground=COLORS["accent"],
                    selectforeground=COLORS["text"])
    style.map("TCombobox", fieldbackground=[("readonly", COLORS["card"])])

    style.configure("Treeview",
                    background=COLORS["card"],
                    foreground=COLORS["text"],
                    fieldbackground=COLORS["card"],
                    rowheight=30,
                    font=("Segoe UI", 10))
    style.configure("Treeview.Heading",
                    background=COLORS["input"],
                    foreground=COLORS["muted"],
                    font=("Segoe UI", 10, "bold"),
                    relief="flat")
    style.map("Treeview",
              background=[("selected", COLORS["accent"])],
              foreground=[("selected", "#ffffff")])

    style.configure("Vertical.TScrollbar",
                    background=COLORS["card"],
                    troughcolor=COLORS["bg"],
                    arrowcolor=COLORS["muted"])


# ── app ───────────────────────────────────────────────────────────────────────

class TorqueTrackerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Torque Tracker")
        self.root.geometry("1150x720")
        self.root.minsize(950, 620)
        self.root.configure(bg=COLORS["bg"])

        apply_global_styles()

        # Persistence
        self.db = Database()
        self.users  = UserController(self.db)
        self.vehicles = VehicleController(self.db)
        self.mileage  = MileageController(self.db)

        # Session state
        self.current_user: object    = None
        self.current_vehicle: object = None

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.show_login()

    # ── navigation ────────────────────────────────────────────────────────────

    def _clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_login(self):
        self._clear()
        from views.login_view import LoginView
        LoginView(self.root, self)

    def show_main(self):
        self._clear()
        from views.main_view import MainView
        MainView(self.root, self)

    def login(self, user):
        self.current_user    = user
        self.current_vehicle = None
        self.show_main()

    def logout(self):
        self.current_user    = None
        self.current_vehicle = None
        self.show_login()

    def _on_close(self):
        self.db.close()
        self.root.destroy()
