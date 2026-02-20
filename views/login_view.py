"""
Login / user-selection screen shown at app start.
"""
import tkinter as tk
from tkinter import messagebox
from app import COLORS
from views.widgets import RoundedButton, RoundedPanel


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
        card = RoundedPanel(
            center,
            bg=COLORS["surface"],
            border_color=COLORS["border"],
            radius=18,
            pad_x=35,
            pad_y=30,
        )
        card.pack()
        card_body = card.content

        # ── Select existing user ──────────────────────────────────────────────
        tk.Label(card_body, text="Select User", font=("Segoe UI", 13, "bold"),
                 bg=COLORS["surface"], fg=COLORS["text"]).pack(anchor="w")
        tk.Label(card_body, text="Double-click or select then press Login",
                 font=("Segoe UI", 9), bg=COLORS["surface"], fg=COLORS["muted"]).pack(anchor="w", pady=(0, 8))

        lb_wrap = RoundedPanel(
            card_body,
            bg=COLORS["surface"],
            border_color=COLORS["border"],
            radius=12,
            pad_x=0,
            pad_y=0,
        )
        lb_wrap.pack(fill=tk.X)
        lb_content = lb_wrap.content

        sb = tk.Scrollbar(
            lb_content,
            bg=COLORS["surface_alt"],
            troughcolor=COLORS["bg"],
            activebackground=COLORS["accent"],
            highlightthickness=0,
            bd=0,
        )
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            lb_content, width=34, height=7,
            bg=COLORS["surface"], fg=COLORS["text"],
            selectbackground=COLORS["accent"], selectforeground="#fff",
            font=("Segoe UI", 11), relief=tk.FLAT,
            highlightthickness=0,
            bd=0,
            yscrollcommand=sb.set,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        sb.config(command=self.listbox.yview)
        self.listbox.bind("<Double-Button-1>", lambda _: self._login())

        RoundedButton(
            card_body,
            text="Login",
            command=self._login,
            bg=COLORS["accent"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["accent_hover"],
            active_bg=COLORS["accent_hover"],
            font=("Segoe UI", 11, "bold"),
            radius=12,
            pad_y=8,
        ).pack(fill=tk.X, pady=(10, 0))

        # ── Divider ───────────────────────────────────────────────────────────
        tk.Frame(card_body, bg=COLORS["border"], height=1).pack(fill=tk.X, pady=18)

        # ── Create new user ───────────────────────────────────────────────────
        tk.Label(card_body, text="New User", font=("Segoe UI", 13, "bold"),
                 bg=COLORS["surface"], fg=COLORS["text"]).pack(anchor="w")

        row = tk.Frame(card_body, bg=COLORS["surface"])
        row.pack(fill=tk.X, pady=(8, 0))

        self.new_user_var = tk.StringVar()
        entry = tk.Entry(row, textvariable=self.new_user_var,
                         bg=COLORS["input"], fg=COLORS["text"],
                         insertbackground=COLORS["text"],
                         font=("Segoe UI", 11), relief=tk.FLAT,
                         highlightthickness=1,
                         highlightbackground=COLORS["border"],
                         highlightcolor=COLORS["accent"],
                         bd=0)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, ipadx=6)
        entry.bind("<Return>", lambda _: self._create_user())

        RoundedButton(
            row,
            text="Create",
            command=self._create_user,
            bg=COLORS["surface_alt"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["card"],
            active_bg=COLORS["card"],
            font=("Segoe UI", 10, "bold"),
            radius=10,
            pad_x=14,
            pad_y=7,
        ).pack(side=tk.LEFT, padx=(8, 0))

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
