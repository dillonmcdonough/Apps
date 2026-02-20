"""
Login / user-selection screen shown at app start.
"""
import tkinter as tk
from tkinter import messagebox
from app import COLORS


class LoginView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.pack(fill=tk.BOTH, expand=True)
        self._build()
        self._load_users()

    # ── layout ────────────────────────────────────────────────────────────────

    def _build(self):
        center = tk.Frame(self, bg=COLORS["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(center, text="TORQUE TRACKER",
                 font=("Segoe UI", 32, "bold"),
                 bg=COLORS["bg"], fg=COLORS["accent"]).pack()
        tk.Label(center, text="Vehicle Mileage Management System",
                 font=("Segoe UI", 12),
                 bg=COLORS["bg"], fg=COLORS["muted"]).pack(pady=(0, 30))

        # Card
        card = tk.Frame(center, bg=COLORS["sidebar"], padx=35, pady=30)
        card.pack()

        # ── Select existing user ──────────────────────────────────────────────
        tk.Label(card, text="Select User", font=("Segoe UI", 13, "bold"),
                 bg=COLORS["sidebar"], fg=COLORS["text"]).pack(anchor="w")
        tk.Label(card, text="Double-click or select then press Login",
                 font=("Segoe UI", 9), bg=COLORS["sidebar"], fg=COLORS["muted"]).pack(anchor="w", pady=(0, 8))

        lb_wrap = tk.Frame(card, bg=COLORS["sidebar"])
        lb_wrap.pack(fill=tk.X)

        sb = tk.Scrollbar(lb_wrap, bg=COLORS["card"])
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            lb_wrap, width=34, height=7,
            bg=COLORS["card"], fg=COLORS["text"],
            selectbackground=COLORS["accent"], selectforeground="#fff",
            font=("Segoe UI", 11), relief=tk.FLAT, highlightthickness=0,
            yscrollcommand=sb.set,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sb.config(command=self.listbox.yview)
        self.listbox.bind("<Double-Button-1>", lambda _: self._login())

        tk.Button(card, text="  Login  ", command=self._login,
                  bg=COLORS["accent"], fg="#fff",
                  font=("Segoe UI", 11, "bold"), relief=tk.FLAT,
                  padx=10, pady=7, cursor="hand2",
                  activebackground="#c73652", activeforeground="#fff"
                  ).pack(fill=tk.X, pady=(10, 0))

        # ── Divider ───────────────────────────────────────────────────────────
        tk.Frame(card, bg=COLORS["card"], height=1).pack(fill=tk.X, pady=18)

        # ── Create new user ───────────────────────────────────────────────────
        tk.Label(card, text="New User", font=("Segoe UI", 13, "bold"),
                 bg=COLORS["sidebar"], fg=COLORS["text"]).pack(anchor="w")

        row = tk.Frame(card, bg=COLORS["sidebar"])
        row.pack(fill=tk.X, pady=(8, 0))

        self.new_user_var = tk.StringVar()
        entry = tk.Entry(row, textvariable=self.new_user_var,
                         bg=COLORS["input"], fg=COLORS["text"],
                         insertbackground=COLORS["text"],
                         font=("Segoe UI", 11), relief=tk.FLAT)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, ipadx=6)
        entry.bind("<Return>", lambda _: self._create_user())

        tk.Button(row, text="Create", command=self._create_user,
                  bg=COLORS["card"], fg=COLORS["accent"],
                  font=("Segoe UI", 10, "bold"), relief=tk.FLAT,
                  padx=12, pady=6, cursor="hand2").pack(side=tk.LEFT, padx=(8, 0))

    # ── logic ─────────────────────────────────────────────────────────────────

    def _load_users(self):
        self.listbox.delete(0, tk.END)
        self._users = self.app.users.get_all()
        for u in self._users:
            self.listbox.insert(tk.END, f"  {u.username}")

    def _login(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a user to log in.", parent=self)
            return
        self.app.login(self._users[sel[0]])

    def _create_user(self):
        name = self.new_user_var.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a username.", parent=self)
            return
        try:
            self.app.users.create(name)
            self.new_user_var.set("")
            self._load_users()
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)
