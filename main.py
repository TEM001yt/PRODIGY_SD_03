import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

FILENAME = "contacts.json"

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("650x400")
        self.root.resizable(False, False)
        
        self.contacts = self.load_contacts()
        self.selected_index = None

        # --- Left Side: Input Form ---
        frame_form = ttk.LabelFrame(root, text=" Contact Details ", padding=15)
        frame_form.place(x=15, y=15, width=280, height=360)

        ttk.Label(frame_form, text="Name:").pack(anchor="w", pady=2)
        self.entry_name = ttk.Entry(frame_form, font=("Arial", 10))
        self.entry_name.pack(fill="x", pady=5)

        ttk.Label(frame_form, text="Phone Number:").pack(anchor="w", pady=2)
        self.entry_phone = ttk.Entry(frame_form, font=("Arial", 10))
        self.entry_phone.pack(fill="x", pady=5)

        ttk.Label(frame_form, text="Email Address:").pack(anchor="w", pady=2)
        self.entry_email = ttk.Entry(frame_form, font=("Arial", 10))
        self.entry_email.pack(fill="x", pady=5)

        # CRUD Action Buttons
        btn_add = ttk.Button(frame_form, text="Add New Contact", command=self.add_contact)
        btn_add.pack(fill="x", pady=10)

        btn_update = ttk.Button(frame_form, text="Update Selected", command=self.update_contact)
        btn_update.pack(fill="x", pady=5)

        btn_clear = ttk.Button(frame_form, text="Clear Fields", command=self.clear_fields)
        btn_clear.pack(fill="x", pady=5)

        # --- Right Side: List View ---
        frame_list = ttk.LabelFrame(root, text=" Contact Directory ", padding=15)
        frame_list.place(x=310, y=15, width=325, height=360)

        # Scrollable Box List Setup
        self.listbox = tk.Listbox(frame_list, font=("Arial", 10), selectmode=tk.SINGLE)
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_contact_select)

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        btn_delete = ttk.Button(root, text="Delete Contact", command=self.delete_contact)
        btn_delete.place(x=310, y=345, width=120)

        self.refresh_listbox()

    # --- Data Core Engine ---
    def load_contacts(self):
        if os.path.exists(FILENAME):
            try:
                with open(FILENAME, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []

    def save_contacts(self):
        with open(FILENAME, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.listbox.insert(tk.END, f"{contact['name']} ({contact['phone']})")

    # --- Operations logic ---
    def add_contact(self):
        name, phone, email = self.entry_name.get().strip(), self.entry_phone.get().strip(), self.entry_email.get().strip()
        if not name or not phone:
            messagebox.showwarning("Missing Info", "Name and Phone Number are required fields.")
            return
        
        self.contacts.append({"name": name, "phone": phone, "email": email})
        self.save_contacts()
        self.refresh_listbox()
        self.clear_fields()
        messagebox.showinfo("Success", "Contact saved successfully!")

    def on_contact_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            self.selected_index = selection[0]
            contact = self.contacts[self.selected_index]
            
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, contact["name"])
            self.entry_phone.delete(0, tk.END)
            self.entry_phone.insert(0, contact["phone"])
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, contact["email"])

    def update_contact(self):
        if self.selected_index is None or self.selected_index >= len(self.contacts):
            messagebox.showwarning("Selection Error", "Please pick a contact from the list directory to update.")
            return
            
        name, phone, email = self.entry_name.get().strip(), self.entry_phone.get().strip(), self.entry_email.get().strip()
        if not name or not phone:
            messagebox.showwarning("Missing Info", "Name and Phone fields cannot be empty.")
            return

        self.contacts[self.selected_index] = {"name": name, "phone": phone, "email": email}
        self.save_contacts()
        self.refresh_listbox()
        self.clear_fields()
        messagebox.showinfo("Updated", "Contact details overwritten.")

    def delete_contact(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Select a contact from the listbox to wipe.")
            return
            
        idx = selection[0]
        if messagebox.askyesno("Confirm Delete", f"Remove '{self.contacts[idx]['name']}' from directory?"):
            self.contacts.pop(idx)
            self.save_contacts()
            self.refresh_listbox()
            self.clear_fields()

    def clear_fields(self):
        self.selected_index = None
        self.listbox.selection_clear(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

if __name__ == "__main__":
    window = tk.Tk()
    app = ContactManager(window)
    window.mainloop()
