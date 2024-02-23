import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import sqlite3
import os
from tkinter import simpledialog
from auth_token import the_password

class PasswordManager:
    def __init__(self, master, root):
        self.master = master
        self.root = root
        self.root.title(" Rtool")
        
       
        # Initialize the encryption key
        self.key = self.get_key()

        self.create_table()

        self.instructions = '''###To add a password, fill in all the fields and press "Add Password".
        To view a password, enter the Account Name and press "Get Password"###.'''
        self.signature = "Developed by Rafael Garcia"

        self.center_frame = tk.Frame(self.master, bg="#d3d3d3")
        self.center_frame.grid(row=0, column=0, padx=10, pady=10)

        self.instruction_label = tk.Label(self.center_frame, text=self.instructions)
        self.instruction_label.grid(row=0, column=1, padx=10, pady=5)

        self.service_label = tk.Label(self.center_frame, text="Account:")
        self.service_label.grid(row=1, column=0, padx=10, pady=5)
        self.service_entry = tk.Entry(self.center_frame)
        self.service_entry.grid(row=1, column=1, padx=10, pady=5)

        self.username_label = tk.Label(self.center_frame, text="Username:")
        self.username_label.grid(row=2, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self.center_frame)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.center_frame, text="Password:")
        self.password_label.grid(row=3, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.center_frame, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        self.add_button = tk.Button(self.center_frame, text="Add Password", command=self.add_password, height=1, width=10)
        self.add_button.grid(row=5, column=4, padx=10, pady=5)

        self.get_button = tk.Button(self.center_frame, text="Get Password", command=self.get_password, height=1, width=10)
        self.get_button.grid(row=6, column=4, padx=10, pady=5)

        self.signature_label = tk.Label(self.center_frame, text=self.signature)
        self.signature_label.grid(row=7, column=1, padx=5, pady=5)

        # New result_label attribute
        self.result_label = tk.Label(self.center_frame, text="", bg="#d3d3d3")
        self.result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        #Show All
        self.show_all_button = tk.Button(self.center_frame, text="Show All Passwords", command=self.show_all_passwords, height=1, width=15)
        self.show_all_button.grid(row=8, column=1, padx=10, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    def ask_for_master_password(self):
        return simpledialog.askstring("Master Password", "Enter Master Password:", show='*')
    
    def on_close(self):
        self.root.destroy()

    def get_key(self):
        key_path = "encryption_key.key"

        if os.path.exists(key_path):
            with open(key_path, "rb") as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, "wb") as key_file:
                key_file.write(key)

        return key

    def encrypt_password(self, password):
        f = Fernet(self.key)
        return f.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        f = Fernet(self.key)
        return f.decrypt(encrypted_password.encode()).decode()

    def create_table(self):
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                service TEXT PRIMARY KEY,
                username TEXT,
                encrypted_password TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_password(self, service, username, encrypted_password):
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO passwords (service, username, encrypted_password)
            VALUES (?, ?, ?)
        ''', (service, username, encrypted_password))
        conn.commit()
        conn.close()

    def load_password(self, service):
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, encrypted_password FROM passwords WHERE service = ?', (service,))
        result = cursor.fetchone()
        conn.close()
        return result

    def add_password(self):
        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if service and username and password:
            encrypted_password = self.encrypt_password(password)
            self.save_password(service, username, encrypted_password)
            messagebox.showinfo("Success", "Password added successfully!")
        else:
            messagebox.showwarning("Error", "Please fill in all the fields.")

    def get_password(self):
        service = self.service_entry.get()
        result = self.load_password(service)

        if result:
            decrypted_password = self.decrypt_password(result[1])
            messagebox.showinfo("Password", f"Username: {result[0]}\nPassword: {decrypted_password}")
        else:
            messagebox.showwarning("Error", "Password not found.")

    # ... (previous code)

    def show_all_passwords(self):
        # Prompt the user for the master password
        master_password = self.ask_for_master_password()

        if master_password is None:
            # The user canceled the password entry
            return

        # Validate the master password
        if not self.validate_master_password(master_password):
            messagebox.showwarning("Error", "Invalid Master Password")
            return

        # Create a new window for displaying and deleting passwords
        show_all_window = tk.Toplevel(self.root)
        show_all_window.title("All Passwords")

        # Create a Text widget to display passwords
        text_widget = tk.Text(show_all_window, height=20, width=60)
        text_widget.pack(pady=10)

        # Fetch all passwords from the database
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('SELECT service, username, encrypted_password FROM passwords')
        results = cursor.fetchall()
        conn.close()

        if results:
            # Populate the Text widget with passwords
            for row in results:
                decrypted_password = self.decrypt_password(row[2])
                text_widget.insert(tk.END, f"Service: {row[0]}, Username: {row[1]}, Password: {decrypted_password}\n\n")

            # Make the window resizable
            show_all_window.resizable(width=True, height=True)
        else:
            tk.Label(show_all_window, text="No passwords found.").pack(pady=10)

    def validate_master_password(self, entered_password):
        try:
            # Import the master_password from auth_token script
            from auth_token import the_password as stored_master_password
        except ImportError:
            return False

        # Compare entered_password with the stored master password
        return entered_password == stored_master_password


    def delete_selected(self, listbox):
        selected_index = listbox.curselection()

        if selected_index:
            # Extract the selected entry's service and username
            selected_entry = listbox.get(selected_index)
            service = selected_entry.split(",")[0].split(":")[1].strip()
            username = selected_entry.split(",")[1].split(":")[1].strip()

            # Ask for confirmation before deleting
            confirmation = messagebox.askyesno("Delete Confirmation", f"Do you want to delete the entry for {service} - {username}?")

            if confirmation:
                # Delete the entry from the database
                conn = sqlite3.connect('passwords.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM passwords WHERE service = ? AND username = ?', (service, username))
                conn.commit()
                conn.close()

                # Remove the selected entry from the listbox
                listbox.delete(selected_index)

                messagebox.showinfo("Success", f"Entry for {service} - {username} deleted successfully.")
        else:
            messagebox.showwarning("Error", "Please select an entry to delete.")

    