import tkinter as tk
from tkinter import ttk, messagebox
import pickle




def load_accounts():
    try:
        with open("accounts.pkl", "rb") as f:
            data = pickle.load(f)
            if isinstance(data, dict):
                return data
            else:
                print("Warning: Loaded data is not a dictionary. Initializing with an empty dictionary.")
                return {}
    except FileNotFoundError:
        print("accounts.pkl not found. Starting with an empty account list.")
        return {}
    except pickle.UnpicklingError:
        print("Error unpickling data. The file might be corrupted. Starting with an empty account list.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Starting with an empty account list.")
        return {}


def save_accounts():
    try:
        with open("accounts.pkl", "wb") as f:
            pickle.dump(accounts, f)
    except Exception as e:
        print(f"Error saving accounts: {e}")
        messagebox.showerror("Error", f"Failed to save accounts: {e}")


def add_account():
    account_number = account_number_entry.get()
    name = name_entry.get()
    balance = balance_entry.get()

    if account_number and name and balance:
        try:
            balance = float(balance)
            accounts[account_number] = {"name": name, "balance": balance}
            save_accounts()
            clear_entries()
            show_accounts()
            messagebox.showinfo("Success", "Account added successfully")
        except ValueError:
            messagebox.showerror("Error", "Invalid balance amount")
    else:
        messagebox.showerror("Error", "Please fill in all fields")


def update_account():
    account_number = account_number_entry.get()
    if account_number in accounts:
        name = name_entry.get()
        balance = balance_entry.get()
        if name and balance:
            try:
                balance = float(balance)
                accounts[account_number]["name"] = name
                accounts[account_number]["balance"] = balance
                save_accounts()
                clear_entries()
                show_accounts()
                messagebox.showinfo("Success", "Account updated successfully")
            except ValueError:
                messagebox.showerror("Error", "Invalid balance amount")
        else:
            messagebox.showerror("Error", "Please fill in all fields")
    else:
        messagebox.showerror("Error", "Account not found")


def delete_account():
    account_number = account_number_entry.get()
    if account_number in accounts:
        del accounts[account_number]
        save_accounts()
        clear_entries()
        show_accounts()
        messagebox.showinfo("Success", "Account deleted successfully")
    else:
        messagebox.showerror("Error", "Account not found")


def show_accounts():
    tree.delete(*tree.get_children())
    for account_number, details in accounts.items():
        tree.insert("", "end", values=(account_number, details["name"], details["balance"]))


def clear_entries():
    account_number_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    balance_entry.delete(0, tk.END)




# ---------------- Window -----------------
root = tk.Tk()
root.title("Simple Bank Management System")
root.geometry("600x400")



# Load existing accounts
accounts = load_accounts()



# ---------------- Widgets -----------------
ttk.Label(root, text="Account Number:").grid(row=0, column=0, padx=5, pady=5)
account_number_entry = ttk.Entry(root)
account_number_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Name:").grid(row=1, column=0, padx=5, pady=5)
name_entry = ttk.Entry(root)
name_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Balance:").grid(row=2, column=0, padx=5, pady=5)
balance_entry = ttk.Entry(root)
balance_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(root, text="Add Account", command=add_account).grid(row=3, column=0, padx=5, pady=5)
ttk.Button(root, text="Update Account", command=update_account).grid(row=3, column=1, padx=5, pady=5)
ttk.Button(root, text="Delete Account", command=delete_account).grid(row=4, column=0, padx=5, pady=5)
ttk.Button(root, text="Show Accounts", command=show_accounts).grid(row=4, column=1, padx=5, pady=5)



# Treeview to display accounts
tree = ttk.Treeview(root, columns=("Account Number", "Name", "Balance"), show="headings")
tree.heading("Account Number", text="Account Number")
tree.heading("Name", text="Name")
tree.heading("Balance", text="Balance")
tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5)




show_accounts()

root.mainloop()
