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
    "bg":      "#0b1220",
    "sidebar": "#0f1a2f",
    "card":    "#15233d",
    "surface": "#111c32",
    "surface_alt": "#1a2a47",
    "border":  "#253554",
    "accent":  "#4f8cff",
    "accent_hover": "#3f79e6",
    "text":    "#e9f1ff",
    "muted":   "#9bb0cf",
    "input":   "#1a2b48",
    "danger":  "#d95b6a",
    "danger_hover": "#c34c5b",
    "success": "#2fbf8f",
    "button_text": "#f8fbff",
}


def apply_global_styles():
    """Configure ttk styles used across all views."""
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("TFrame", background=COLORS["bg"])
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text"])

    style.configure("TCombobox",
              fieldbackground=COLORS["input"],
              background=COLORS["input"],
                    foreground=COLORS["text"],
                    selectbackground=COLORS["accent"],
              selectforeground=COLORS["button_text"],
              bordercolor=COLORS["border"],
              arrowcolor=COLORS["muted"],
              lightcolor=COLORS["input"],
              darkcolor=COLORS["input"])
    style.map("TCombobox",
          fieldbackground=[("readonly", COLORS["input"])],
          foreground=[("readonly", COLORS["text"])],
          selectbackground=[("readonly", COLORS["accent"])])

    style.configure("Treeview",
              background=COLORS["surface"],
                    foreground=COLORS["text"],
              fieldbackground=COLORS["surface"],
                    rowheight=30,
              bordercolor=COLORS["border"],
              lightcolor=COLORS["surface"],
              darkcolor=COLORS["surface"],
                    font=("Segoe UI", 10))
    style.configure("Treeview.Heading",
              background=COLORS["surface_alt"],
              foreground=COLORS["text"],
                    font=("Segoe UI", 10, "bold"),
                    relief="flat")
    style.map("Treeview",
              background=[("selected", COLORS["accent"])],
          foreground=[("selected", COLORS["button_text"])])

    style.configure("Vertical.TScrollbar",
              background=COLORS["surface_alt"],
              troughcolor=COLORS["bg"],
              arrowcolor=COLORS["text"],
              bordercolor=COLORS["bg"],
              lightcolor=COLORS["surface_alt"],
              darkcolor=COLORS["surface_alt"])


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
