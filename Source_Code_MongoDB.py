import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient



# Ensure High DPI awareness on Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass



# ---------- MongoDB connection ----------

client = MongoClient('mongodb://localhost:27017/')
db = client['bank_database']
accounts_collection = db['accounts']



# ----------- Color scheme -------------

bg_color = "#f0f0f0"
accent_color = "#3498db"
text_color = "#2c3e50"


def create_main_window():
    window = tk.Tk()
    window.title("Bank Details Manager")
    window.geometry("1200x800")
    window.configure(bg=bg_color)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TLabel", background=bg_color, foreground=text_color, font=("Arial", 10))
    style.configure("TEntry", fieldbackground="white", font=("Arial", 10))
    style.configure("TButton", background=accent_color, foreground="white", font=("Arial", 10, "bold"))
    style.map("TButton", background=[('active', '#2980b9')])

    return window



def main():
    main_window = create_main_window()

    input_frame = ttk.Frame(main_window, padding="20")
    input_frame.pack(fill=tk.X, padx=20, pady=20)

    table_frame = ttk.Frame(main_window, padding="20")
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    fields = [
        ("Account Number", 0, 0), ("Name", 0, 2), ("Balance", 0, 4),
        ("Email", 1, 0), ("Phone", 1, 2), ("Address", 1, 4),
        ("Date of Birth", 2, 0), ("Account Type", 2, 2), ("Branch", 2, 4)
    ]

    entries = {}
    for (field, row, col) in fields:
        ttk.Label(input_frame, text=field + ":").grid(row=row, column=col, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(input_frame, width=25)
        entry.grid(row=row, column=col+1, padx=5, pady=5, sticky="w")
        entries[field] = entry

    columns = ('Account Number', 'Name', 'Balance', 'Email', 'Phone', 'Account Type')
    table = ttk.Treeview(table_frame, columns=columns, show='headings')

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=100)

    table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table.yview)
    table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def clear_entries():
        for entry in entries.values():
            entry.delete(0, tk.END)

    def add_account():
        account = {field: entries[field].get() for field, _, _ in fields}
        
        if any(not value for value in account.values()):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            account['Balance'] = float(account['Balance'])
        except ValueError:
            messagebox.showerror("Error", "Balance must be a number")
            return

        accounts_collection.insert_one(account)
        clear_entries()
        update_table()
        messagebox.showinfo("Success", "Account added successfully")

    def update_table():
        for item in table.get_children():
            table.delete(item)

        for account in accounts_collection.find():
            table.insert('', tk.END, values=(account['Account Number'], account['Name'], account['Balance'],
                                             account['Email'], account['Phone'], account['Account Type']))

    button_frame = ttk.Frame(input_frame)
    button_frame.grid(row=3, column=0, columnspan=6, pady=10)

    ttk.Button(button_frame, text="Add Account", command=add_account).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Clear Fields", command=clear_entries).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Refresh Table", command=update_table).pack(side=tk.LEFT, padx=5)

    update_table()

    main_window.mainloop()



if __name__ == "__main__":
    main()
