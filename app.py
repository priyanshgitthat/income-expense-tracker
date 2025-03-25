import customtkinter as ctk
from tkinter import messagebox, filedialog, simpledialog

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Ask for user's name at the start
        self.user_name = simpledialog.askstring("User Name", "Enter your name:")
        if not self.user_name:
            self.user_name = "User"  # Default name if none entered

        self.salary = 0
        self.expenses = {}  # Dictionary to store unique expenses
        self.total_expense = 0

        # UI Elements
        self.title_label = ctk.CTkLabel(root, text=f"Expense Tracker - {self.user_name}", font=("Arial", 20))
        self.title_label.pack(pady=10)

        self.salary_label = ctk.CTkLabel(root, text="Enter Your Salary:")
        self.salary_label.pack()

        self.salary_entry = ctk.CTkEntry(root, width=250)
        self.salary_entry.pack(pady=5)

        self.salary_button = ctk.CTkButton(root, text="Set Salary", command=self.set_salary)
        self.salary_button.pack(pady=5)

        self.expense_label = ctk.CTkLabel(root, text="Add an Expense:")
        self.expense_label.pack()

        self.category_entry = ctk.CTkEntry(root, placeholder_text="Category", width=250)
        self.category_entry.pack(pady=5)

        self.amount_entry = ctk.CTkEntry(root, placeholder_text="Amount", width=250)
        self.amount_entry.pack(pady=5)

        self.add_expense_button = ctk.CTkButton(root, text="Add Expense", command=self.add_expense)
        self.add_expense_button.pack(pady=5)

        self.summary_button = ctk.CTkButton(root, text="View Summary", command=self.view_summary)
        self.summary_button.pack(pady=5)

        self.download_button = ctk.CTkButton(root, text="Download Summary", command=self.download_summary)
        self.download_button.pack(pady=5)

        self.exit_button = ctk.CTkButton(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=20)

        # Sidebar for real-time expenses
        self.expense_frame = ctk.CTkFrame(root, width=250, height=300)
        self.expense_frame.pack(pady=10, padx=10, side="right", fill="y")

        self.expense_list_label = ctk.CTkLabel(self.expense_frame, text="Expenses", font=("Arial", 15))
        self.expense_list_label.pack()

        self.expense_list = ctk.CTkTextbox(self.expense_frame, width=230, height=260)
        self.expense_list.pack(pady=5, padx=5)

    def set_salary(self):
        try:
            self.salary = float(self.salary_entry.get())
            messagebox.showinfo("Success", f"Salary set to Rs. {self.salary}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Enter a valid number.")

    def add_expense(self):
        if self.salary == 0:
            messagebox.showwarning("Warning", "Please set your salary first.")
            return

        category = self.category_entry.get().strip()
        try:
            amount = float(self.amount_entry.get())

            if category in self.expenses:
                self.total_expense -= self.expenses[category]  # Remove old amount
            self.expenses[category] = amount  # Update to new amount
            self.total_expense += amount

            self.update_expense_list()
            messagebox.showinfo("Success", f"Updated {category}: Rs. {amount}")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")

    def update_expense_list(self):
        """Updates the sidebar list of expenses."""
        self.expense_list.delete("1.0", "end")
        for category, amount in self.expenses.items():
            self.expense_list.insert("end", f"{category}: Rs. {amount}\n")

    def view_summary(self):
        if self.salary == 0:
            messagebox.showwarning("Warning", "Please set your salary first.")
            return

        savings = self.salary - self.total_expense
        summary = f"Total Salary: Rs. {self.salary}\nTotal Expenses: Rs. {self.total_expense}\nSavings: Rs. {savings}\n\nExpense Breakdown:\n"
        for category, amount in self.expenses.items():
            summary += f"- {category}: Rs. {amount}\n"

        messagebox.showinfo("Expense Summary", summary)

    def download_summary(self):
        """Generates a text file with the expense summary."""
        if self.salary == 0:
            messagebox.showwarning("Warning", "Please set your salary first.")
            return

        savings = self.salary - self.total_expense
        file_content = f"Expense Summary for {self.user_name}\n"
        file_content += f"Total Salary: Rs. {self.salary}\nTotal Expenses: Rs. {self.total_expense}\nSavings: Rs. {savings}\n\nExpense Breakdown:\n"
        for category, amount in self.expenses.items():
            file_content += f"- {category}: Rs. {amount}\n"

        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 initialfile=f"{self.user_name}_expense_summary.txt",
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(file_content)
            messagebox.showinfo("Success", "Summary downloaded successfully!")

if __name__ == "__main__":
    root = ctk.CTk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
