Parking Management System (Python + MySQL)
=========================================

A simple, interactive GUI application to manage vehicle parking in real time.
Built with **Tkinter** for the interface and **MySQL** for persistent storage.

Features
--------
- Vehicle check‑in with slot assignment
- Vehicle check‑out with automatic fee calculation
- Real‑time table of all parking records
- Easy configuration via `db_config.py`

Quick Start
-----------
1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Create the database**

   ```bash
   mysql -u root -p < schema.sql
   ```

3. **Configure MySQL credentials**

   Edit `db_config.py` and update `user`, `password`, and (if needed) `host`.

4. **Run the application**

   ```bash
   python main.py
   ```

Project Layout
--------------
```
parking_management_system/
├── assets/
│   └── logo.png
├── db_config.py
├── main.py
├── requirements.txt
├── schema.sql
└── readme.txt
```

Screenshots
-----------
Add screenshots of the running GUI here after you first run the app.

License
-------
MIT
