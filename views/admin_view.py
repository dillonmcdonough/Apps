"""
AdminView — admin-only user management panel.
Allows admins to create, delete, promote/demote users, and reset passwords.
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app import COLORS
from views.widgets import RoundedButton, RoundedPanel


class AdminView(tk.Frame):
    def __init__(self, parent, app, main_view):
        super().__init__(parent, bg=COLORS["bg"])
        self.app = app
        self.main_view = main_view
        self._users = []
        self.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        self._build()
        self._load_users()

    # ── layout ────────────────────────────────────────────────────────────────

    def _build(self):
        # Left: user table + action buttons
        left = tk.Frame(self, bg=COLORS["bg"])
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right: create user form
        right = tk.Frame(self, bg=COLORS["bg"], width=268)
        right.pack(side=tk.LEFT, fill=tk.Y, padx=(12, 0))
        right.pack_propagate(False)

        self._build_user_table(left)
        self._build_create_form(right)

    def _build_user_table(self, parent):
        table_panel = RoundedPanel(
            parent,
            bg=COLORS["card"],
            border_color=COLORS["border"],
            radius=14,
            pad_x=16,
            pad_y=16,
        )
        table_panel.pack(fill=tk.BOTH, expand=True)
        body = table_panel.content

        tk.Label(body, text="User Management", font=("Segoe UI", 14, "bold"),
                 bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 12))

        # Treeview
        tree_frame = tk.Frame(body, bg=COLORS["card"])
        tree_frame.pack(fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self._tree = ttk.Treeview(
            tree_frame,
            columns=("username", "role", "created"),
            show="headings",
            yscrollcommand=vsb.set,
        )
        vsb.config(command=self._tree.yview)

        self._tree.heading("username", text="Username")
        self._tree.heading("role", text="Role")
        self._tree.heading("created", text="Created")
        self._tree.column("username", width=200)
        self._tree.column("role", width=110, anchor="center")
        self._tree.column("created", width=150)
        self._tree.pack(fill=tk.BOTH, expand=True)

        # Action buttons
        actions = tk.Frame(body, bg=COLORS["card"])
        actions.pack(fill=tk.X, pady=(12, 0))

        RoundedButton(
            actions,
            text="Reset Password",
            command=self._reset_password,
            bg=COLORS["accent"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["accent_hover"],
            active_bg=COLORS["accent_hover"],
            font=("Segoe UI", 10, "bold"),
            radius=10,
            pad_y=7,
        ).pack(side=tk.LEFT, padx=(0, 8))

        RoundedButton(
            actions,
            text="Toggle Admin",
            command=self._toggle_admin,
            bg=COLORS["surface_alt"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["border"],
            active_bg=COLORS["border"],
            font=("Segoe UI", 10, "bold"),
            radius=10,
            pad_y=7,
        ).pack(side=tk.LEFT, padx=(0, 8))

        RoundedButton(
            actions,
            text="Delete User",
            command=self._delete_user,
            bg=COLORS["danger"],
            fg=COLORS["button_text"],
            hover_bg=COLORS["danger_hover"],
            active_bg=COLORS["danger_hover"],
            font=("Segoe UI", 10, "bold"),
            radius=10,
            pad_y=7,
        ).pack(side=tk.LEFT)

    def _build_create_form(self, parent):
        panel = RoundedPanel(
            parent,
            bg=COLORS["card"],
            border_color=COLORS["border"],
            radius=14,
            pad_x=18,
            pad_y=18,
        )
        panel.pack(fill=tk.X)
        body = panel.content

        tk.Label(body, text="Create User", font=("Segoe UI", 13, "bold"),
                 bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", pady=(0, 14))

        # Username
        tk.Label(body, text="Username", font=("Segoe UI", 9),
                 bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w")
        self._new_username_var = tk.StringVar()
        tk.Entry(
            body,
            textvariable=self._new_username_var,
            bg=COLORS["input"], fg=COLORS["text"],
            insertbackground=COLORS["text"],
            font=("Segoe UI", 10), relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
            bd=0,
        ).pack(fill=tk.X, ipady=6, ipadx=6, pady=(2, 12))

        # Password
        tk.Label(body, text="Password", font=("Segoe UI", 9),
                 bg=COLORS["card"], fg=COLORS["muted"]).pack(anchor="w")
        self._new_password_var = tk.StringVar()
        tk.Entry(
            body,
            textvariable=self._new_password_var,
            bg=COLORS["input"], fg=COLORS["text"],
            insertbackground=COLORS["text"],
            show="*",
            font=("Segoe UI", 10), relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["accent"],
            bd=0,
        ).pack(fill=tk.X, ipady=6, ipadx=6, pady=(2, 12))

        # Admin checkbox
        self._is_admin_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            body,
            text="Grant Admin",
            variable=self._is_admin_var,
            bg=COLORS["card"],
            fg=COLORS["text"],
            selectcolor=COLORS["input"],
            activebackground=COLORS["card"],
            activeforeground=COLORS["text"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 14))

        RoundedButton(
            body,
            text="Create User",
            command=self._create_user,
            bg=COLORS["success"],
            fg=COLORS["button_text"],
            hover_bg="#27a87d",
            active_bg="#27a87d",
            font=("Segoe UI", 10, "bold"),
            radius=10,
            pad_y=8,
        ).pack(fill=tk.X)

    # ── data ──────────────────────────────────────────────────────────────────

    def _load_users(self):
        for item in self._tree.get_children():
            self._tree.delete(item)
        self._users = self.app.users.get_all()
        me = self.app.current_user.id
        for u in self._users:
            role = "Admin" if u.is_admin else "User"
            label = f"{u.username} (you)" if u.id == me else u.username
            created = u.created_at.split(" ")[0] if u.created_at else "—"
            self._tree.insert("", tk.END, iid=str(u.id), values=(label, role, created))

    def _selected_user(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a user first.", parent=self)
            return None
        user_id = int(sel[0])
        return next((u for u in self._users if u.id == user_id), None)

    # ── actions ───────────────────────────────────────────────────────────────

    def _reset_password(self):
        user = self._selected_user()
        if not user:
            return
        new_pw = simpledialog.askstring(
            "Reset Password",
            f"Enter new password for {user.username}:",
            parent=self,
            show="*",
        )
        if not new_pw:
            return
        try:
            self.app.users.set_password(user.id, new_pw)
            messagebox.showinfo(
                "Password Reset",
                f"Password for {user.username} has been reset.",
                parent=self,
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _toggle_admin(self):
        user = self._selected_user()
        if not user:
            return
        if user.id == self.app.current_user.id:
            messagebox.showwarning(
                "Cannot Modify Self",
                "You cannot change your own admin status here.",
                parent=self,
            )
            return
        # Prevent removing the last admin
        if user.is_admin:
            admin_count = sum(1 for u in self._users if u.is_admin)
            if admin_count <= 1:
                messagebox.showwarning(
                    "Cannot Demote",
                    "There must be at least one admin. Create another admin first.",
                    parent=self,
                )
                return
        new_status = not user.is_admin
        action = "promote to Admin" if new_status else "remove Admin rights from"
        if not messagebox.askyesno(
            "Toggle Admin",
            f"Are you sure you want to {action} {user.username}?",
            parent=self,
        ):
            return
        self.app.users.set_admin(user.id, new_status)
        self._load_users()

    def _delete_user(self):
        user = self._selected_user()
        if not user:
            return
        if user.id == self.app.current_user.id:
            messagebox.showwarning(
                "Cannot Delete Self",
                "Use the 'Delete User' button in the sidebar to delete your own account.",
                parent=self,
            )
            return
        if not messagebox.askyesno(
            "Delete User",
            f"Permanently delete '{user.username}' and all their data?",
            parent=self,
        ):
            return
        self.app.users.delete(user.id)
        self._load_users()
        messagebox.showinfo("User Deleted", f"'{user.username}' has been deleted.", parent=self)

    def _create_user(self):
        username = self._new_username_var.get().strip()
        password = self._new_password_var.get().strip()
        is_admin = self._is_admin_var.get()
        if not username:
            messagebox.showwarning("Input Error", "Username cannot be empty.", parent=self)
            return
        if not password:
            messagebox.showwarning("Input Error", "Password cannot be empty.", parent=self)
            return
        try:
            self.app.users.create(username, password, is_admin=is_admin)
            self._new_username_var.set("")
            self._new_password_var.set("")
            self._is_admin_var.set(False)
            self._load_users()
            messagebox.showinfo("User Created", f"User '{username}' has been created.", parent=self)
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self)
