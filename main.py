"""
Torque Tracker - Entry Point
Run this file to start the application.
"""
import tkinter as tk
from app import TorqueTrackerApp

if __name__ == "__main__":
    root = tk.Tk()
    app = TorqueTrackerApp(root)
    root.mainloop()
