import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db_config import get_connection

FEE_PER_HOUR = 20  # Adjust as needed

class ParkingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Management System")
        self.create_widgets()
        self.refresh_tree()

    def create_widgets(self):
        # Vehicle Entry Frame
        entry_frame = ttk.LabelFrame(self.root, text="Vehicle Entry")
        entry_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(entry_frame, text="Vehicle No:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_vehicle = ttk.Entry(entry_frame, width=20)
        self.entry_vehicle.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Slot No:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_slot = ttk.Entry(entry_frame, width=10)
        self.entry_slot.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(entry_frame, text="Park", command=self.park_vehicle).grid(row=0, column=4, padx=10, pady=5)

        # Vehicle Exit Frame
        exit_frame = ttk.LabelFrame(self.root, text="Vehicle Exit")
        exit_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(exit_frame, text="Vehicle No:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.exit_vehicle = ttk.Entry(exit_frame, width=20)
        self.exit_vehicle.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(exit_frame, text="Checkout", command=self.checkout_vehicle).grid(row=0, column=2, padx=10, pady=5)

        # Treeview Frame
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "vehicle_no", "slot_no", "entry_time", "exit_time", "fee")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor="center", width=100)
        self.tree.pack(fill="both", expand=True)

        ttk.Button(self.root, text="Refresh", command=self.refresh_tree).pack(pady=5)

    # ----------------- DB Methods ----------------- #
    def park_vehicle(self):
        vehicle_no = self.entry_vehicle.get().strip().upper()
        slot_no = self.entry_slot.get().strip()

        if not vehicle_no or not slot_no:
            messagebox.showerror("Missing Data", "Please enter both vehicle number and slot number.")
            return

        conn = get_connection()
        cur = conn.cursor()

        # Check if vehicle already parked
        cur.execute("SELECT id FROM parkings WHERE vehicle_no=%s AND exit_time IS NULL", (vehicle_no,))
        if cur.fetchone():
            messagebox.showwarning("Duplicate", "This vehicle is already parked.")
            conn.close()
            return

        cur.execute(
            "INSERT INTO parkings (vehicle_no, slot_no, entry_time) VALUES (%s, %s, %s)",
            (vehicle_no, slot_no, datetime.now())
        )
        conn.commit()
        conn.close()

        self.entry_vehicle.delete(0, "end")
        self.entry_slot.delete(0, "end")
        self.refresh_tree()
        messagebox.showinfo("Success", "Vehicle parked successfully.")

    def checkout_vehicle(self):
        vehicle_no = self.exit_vehicle.get().strip().upper()

        if not vehicle_no:
            messagebox.showerror("Missing Data", "Please enter the vehicle number.")
            return

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, entry_time FROM parkings WHERE vehicle_no=%s AND exit_time IS NULL", (vehicle_no,))
        record = cur.fetchone()

        if not record:
            messagebox.showerror("Not Found", "Vehicle not found or already checked out.")
            conn.close()
            return

        entry_time = record["entry_time"]
        hours = max(1, int((datetime.now() - entry_time).total_seconds() // 3600))
        fee = hours * FEE_PER_HOUR

        cur.execute(
            "UPDATE parkings SET exit_time=%s, fee=%s WHERE id=%s",
            (datetime.now(), fee, record["id"])
        )
        conn.commit()
        conn.close()

        self.exit_vehicle.delete(0, "end")
        self.refresh_tree()
        messagebox.showinfo("Checkout Complete", f"Parking fee: ₹{fee}")

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, vehicle_no, slot_no, entry_time, COALESCE(exit_time, '-') AS exit_time, COALESCE(fee, 0) FROM parkings")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingApp(root)
    root.mainloop()
