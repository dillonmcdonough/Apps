# Torque Tracker

Torque Tracker is a desktop app for tracking vehicle odometer entries and viewing mileage stats.

- Create or select a user
- Add and manage vehicles
- Log mileage entries over time
- View dashboard summaries (total miles tracked, number of logs, latest odometer)

---

## 1) Setup (Beginner Friendly)

These steps are written for people new to Python.

### What you need

- A computer with Python 3.10+ installed
- This project folder downloaded/cloned to your computer

### Check if Python is installed

Open a terminal (Command Prompt / PowerShell on Windows, Terminal on macOS/Linux) and run:

```bash
python3 --version
```

If that does not work, try:

```bash
python --version
```

You should see something like `Python 3.10.x` or newer.

If you do **not** have Python:
- Go to https://www.python.org/downloads/
- Install the latest Python 3 version
- On Windows, make sure to check **“Add Python to PATH”** during install

---

## 2) Open the project

In terminal, go to this app folder:

```bash
cd path/to/Apps
```

Example (macOS):

```bash
cd ~/GitHub-Desktop/Apps
```

---

## 3) Run the app

From the project folder, run:

```bash
python3 main.py
```

On some systems, use:

```bash
python main.py
```

A desktop window should open.

---

## 4) First-time use walkthrough

### Login screen

1. If this is your first time, type a username in **New User**.
2. Click **Create** and enter a password in the popup prompt.
3. Select your username from the list.
4. Click **Login** and enter your password in the popup prompt.

For users that existed before passwords were added, the default password is the same as the username.

### Vehicles page

1. Go to **Vehicles** from the left sidebar.
2. Fill in at least **Nickname** (required).
3. Optional: Make, Model, Year, License Plate.
4. Click **Add Vehicle**.
5. Your vehicle appears in the left list.

To edit:
- Click a vehicle in the left list
- Update fields
- Click **Update Vehicle**

To delete:
- Select a vehicle
- Click **Delete**
- Confirm deletion (this also deletes that vehicle’s mileage logs)

### Mileage Log page

1. Select a vehicle from the top-right vehicle dropdown.
2. Go to **Mileage Log**.
3. Enter:
   - Date (`YYYY-MM-DD`)
   - Odometer reading (number)
   - Optional notes
4. Click **Add Log**.

You can remove a log by selecting it in history and clicking **Delete Selected**.

### Dashboard page

The dashboard shows:
- Total miles tracked (max odometer - min odometer)
- Number of mileage entries
- Latest odometer
- Recent log entries
- Quick summary for all vehicles

---

## Data and storage

This app uses a local SQLite database file created automatically in the project folder:

- `torque_tracker.db`

Notes:
- No internet or cloud account required
- Deleting the `.db` file resets all data

---

## Troubleshooting

### “python3: command not found”

- Python is not installed or not on PATH
- Install from https://www.python.org/downloads/
- Reopen terminal and try again

### App does not open window

- Make sure you are in the correct project folder
- Try both commands:
  - `python3 main.py`
  - `python main.py`

### Need a clean reset

1. Close the app
2. Delete `torque_tracker.db`
3. Start app again with `python3 main.py`

---

## Project structure (quick reference)

- `main.py` → app entry point
- `app.py` → main app controller and theme setup
- `database.py` → SQLite setup and queries
- `controllers/` → app logic for users, vehicles, mileage
- `models/` → data models
- `views/` → Tkinter UI screens

---

## Tech stack

- Python
- Tkinter (standard Python GUI library)
- SQLite (local file database)

No extra Python packages are required.