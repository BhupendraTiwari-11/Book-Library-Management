import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, timedelta
import sv_ttk  # For modern theme

class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("400x600")  # Mobile-like aspect ratio

        # Apply modern theme
        sv_ttk.set_theme("light")

        # Create main frame with gradient background
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # Create canvas for gradient background
        self.canvas = tk.Canvas(self.main_frame, width=400, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Create gradient (light blue to white)
        for i in range(600):
            r = int(200 + (255-200) * (i/600))
            g = int(220 + (255-220) * (i/600))
            b = int(240 + (255-240) * (i/600))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, 400, i, fill=color)

        # Create container frame for widgets
        self.container = tk.Frame(self.canvas, bg="#ffffff", bd=10, relief="flat")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Initialize library data
        self.books = {}  # {book_id: {"title": str, "author": str, "status": str, "issued_to": str, "due_date": str}}
        self.load_data()

        # GUI Elements
        self.label_action = tk.Label(self.container, text="Select Action:", bg="#ffffff", font=("Arial", 12))
        self.label_action.pack(pady=10)

        self.action_var = tk.StringVar(value="Add Book")
        actions = ["Add Book", "Remove Book", "Issue Book", "Return Book", "View Books"]
        self.action_menu = ttk.Combobox(self.container, textvariable=self.action_var, values=actions, state="readonly", font=("Arial", 12))
        self.action_menu.pack(pady=10, padx=20, fill="x")

        self.label_book_id = tk.Label(self.container, text="Book ID:", bg="#ffffff", font=("Arial", 12))
        self.label_book_id.pack(pady=5)
        self.entry_book_id = tk.Entry(self.container, font=("Arial", 12), bd=2, relief="groove")
        self.entry_book_id.pack(pady=5, padx=20, fill="x")

        self.label_title = tk.Label(self.container, text="Title:", bg="#ffffff", font=("Arial", 12))
        self.label_title.pack(pady=5)
        self.entry_title = tk.Entry(self.container, font=("Arial", 12), bd=2, relief="groove")
        self.entry_title.pack(pady=5, padx=20, fill="x")

        self.label_author = tk.Label(self.container, text="Author:", bg="#ffffff", font=("Arial", 12))
        self.label_author.pack(pady=5)
        self.entry_author = tk.Entry(self.container, font=("Arial", 12), bd=2, relief="groove")
        self.entry_author.pack(pady=5, padx=20, fill="x")

        self.label_student = tk.Label(self.container, text="Student Name:", bg="#ffffff", font=("Arial", 12))
        self.label_student.pack(pady=5)
        self.entry_student = tk.Entry(self.container, font=("Arial", 12), bd=2, relief="groove")
        self.entry_student.pack(pady=5, padx=20, fill="x")

        self.submit_button = tk.Button(self.container, text="Submit", command=self.perform_action, 
                                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), 
                                     bd=0, relief="flat", padx=20, pady=10)
        self.submit_button.pack(pady=20)

        self.result_label = tk.Label(self.container, text="", bg="#ffffff", font=("Arial", 12), wraplength=300)
        self.result_label.pack(pady=10)

        # Add rounded corners effect to container
        self.container.config(highlightbackground="#cccccc", highlightthickness=2)
        self.canvas.create_window(200, 300, window=self.container)

    def load_data(self):
        try:
            with open("library_data.json", "r") as file:
                self.books = json.load(file)
        except FileNotFoundError:
            self.books = {}

    def save_data(self):
        with open("library_data.json", "w") as file:
            json.dump(self.books, file)

    def perform_action(self):
        action = self.action_var.get()
        book_id = self.entry_book_id.get().strip()
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        student = self.entry_student.get().strip()

        try:
            if action == "Add Book":
                if not book_id or not title or not author:
                    messagebox.showerror("Error", "Book ID, Title, and Author are required.")
                    return
                if book_id in self.books:
                    messagebox.showerror("Error", "Book ID already exists.")
                    return
                self.books[book_id] = {"title": title, "author": author, "status": "Available", "issued_to": "", "due_date": ""}
                self.result_label.config(text=f"Book '{title}' added successfully!")

            elif action == "Remove Book":
                if not book_id:
                    messagebox.showerror("Error", "Book ID is required.")
                    return
                if book_id not in self.books:
                    messagebox.showerror("Error", "Book ID not found.")
                    return
                del self.books[book_id]
                self.result_label.config(text=f"Book ID {book_id} removed successfully!")

            elif action == "Issue Book":
                if not book_id or not student:
                    messagebox.showerror("Error", "Book ID and Student Name are required.")
                    return
                if book_id not in self.books:
                    messagebox.showerror("Error", "Book ID not found.")
                    return
                if self.books[book_id]["status"] == "Issued":
                    messagebox.showerror("Error", "Book is already issued.")
                    return
                self.books[book_id]["status"] = "Issued"
                self.books[book_id]["issued_to"] = student
                due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                self.books[book_id]["due_date"] = due_date
                self.result_label.config(text=f"Book issued to {student}. Due date: {due_date}")

            elif action == "Return Book":
                if not book_id:
                    messagebox.showerror("Error", "Book ID is required.")
                    return
                if book_id not in self.books:
                    messagebox.showerror("Error", "Book ID not found.")
                    return
                if self.books[book_id]["status"] != "Issued":
                    messagebox.showerror("Error", "Book is not issued.")
                    return
                due_date = datetime.strptime(self.books[book_id]["due_date"], "%Y-%m-%d")
                today = datetime.now()
                fine = 0
                if today > due_date:
                    days_late = (today - due_date).days
                    fine = days_late * 1  # $1 per day late
                self.books[book_id]["status"] = "Available"
                self.books[book_id]["issued_to"] = ""
                self.books[book_id]["due_date"] = ""
                self.result_label.config(text=f"Book returned. Fine: ${fine}" if fine > 0 else "Book returned. No fine.")

            elif action == "View Books":
                if not self.books:
                    self.result_label.config(text="No books available.")
                    return
                display_text = "Library Books:\n"
                for book_id, info in self.books.items():
                    display_text += f"ID: {book_id}, Title: {info['title']}, Author: {info['author']}, Status: {info['status']}\n"
                self.result_label.config(text=display_text)

            self.save_data()
            self.clear_entries()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_entries(self):
        self.entry_book_id.delete(0, tk.END)
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_student.delete(0, tk.END)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()
