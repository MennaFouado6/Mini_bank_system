import tkinter as tk
from tkinter import messagebox

from account import Account_Manager

# ---------------- الألوان ----------------
AZURE_WHITE = "#F0FFFF"      # Azureish white
SPACE_CADET = "#1D2951"      # Space cadet
CADET_HOVER = "#2E4272"      # درجة أفتح شوية للـ hover


class BankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NOVA Bank")
        self.root.geometry("560x650")
        self.root.resizable(False, False)
        self.root.configure(bg=AZURE_WHITE)

        self.manager = Account_Manager()
        self.logged_in_account = None

        self.show_home()

    # ---------------- أدوات مساعدة ----------------
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def title_bar(self, text):
        tk.Label(self.root, text=text, bg=SPACE_CADET, fg=AZURE_WHITE,
                 font=("Segoe UI", 18, "bold"), pady=14).pack(fill="x")

    def label(self, text, size=10, bold=False):
        return tk.Label(self.root, text=text, bg=AZURE_WHITE, fg=SPACE_CADET,
                        font=("Segoe UI", size, "bold" if bold else "normal"))

    def button(self, text, command):
        return tk.Button(self.root, text=text, command=command,
                         bg=SPACE_CADET, fg=AZURE_WHITE,
                         activebackground=CADET_HOVER, activeforeground=AZURE_WHITE,
                         font=("Segoe UI", 11, "bold"), bd=0, pady=9, cursor="hand2")

    def entry(self, secret=False):
        return tk.Entry(self.root, show="*" if secret else "",
                        bg=AZURE_WHITE, fg=SPACE_CADET,
                        insertbackground=SPACE_CADET,
                        highlightthickness=1, highlightbackground=SPACE_CADET,
                        font=("Segoe UI", 11), bd=0)

    def text_box(self):
        return tk.Text(self.root, bg=AZURE_WHITE, fg=SPACE_CADET,
                       font=("Consolas", 11), bd=0,
                       highlightthickness=1, highlightbackground=SPACE_CADET)

    # ---------------- القائمة الخارجية ----------------
    def show_home(self):
        self.clear()
        self.logged_in_account = None
        self.title_bar("★ NOVA Bank ★")

        self.label("Welcome! Choose an operation:", 12, True).pack(pady=(25, 12))

        for text, cmd in [("Create New Account", self.show_create_account),
                          ("Login", self.show_login),
                          ("List All Accounts (Admin)", self.show_all_accounts),
                          ("Exit", self.root.destroy)]:
            self.button(text, cmd).pack(fill="x", padx=70, pady=5)

    # ---------------- إنشاء حساب ----------------
    def show_create_account(self):
        self.clear()
        self.title_bar("Create New Account")

        self.label("Name:", 11, True).pack(anchor="w", padx=70, pady=(25, 3))
        name_e = self.entry()
        name_e.pack(fill="x", padx=70, ipady=4)

        self.label("PIN (4 digits):", 11, True).pack(anchor="w", padx=70, pady=(12, 3))
        pin_e = self.entry(secret=True)
        pin_e.pack(fill="x", padx=70, ipady=4)

        self.label("Initial balance:", 11, True).pack(anchor="w", padx=70, pady=(12, 3))
        bal_e = self.entry()
        bal_e.pack(fill="x", padx=70, ipady=4)

        def submit():
            name = name_e.get().strip()
            pin = pin_e.get().strip()

            if not name:
                messagebox.showwarning("Invalid", "Name cannot be empty.")
                return
            if not (pin.isdigit() and len(pin) == 4):
                messagebox.showwarning("Invalid", "PIN must be a 4-digit number.")
                return
            try:
                balance = float(bal_e.get() or 0)
            except ValueError:
                messagebox.showwarning("Invalid", "Balance must be a number.")
                return
            if balance < 0:
                messagebox.showwarning("Invalid", "Balance cannot be negative.")
                return

            account = self.manager.create_account(name, pin, balance)
            messagebox.showinfo("Success", f"Account created successfully!\nAccount number: {account.account_number}")
            self.show_home()

        self.button("Create Account", submit).pack(pady=20)
        self.button("Back", self.show_home).pack()

    # ---------------- تسجيل الدخول (3 محاولات) ----------------
    def show_login(self):
        self.clear()
        self.title_bar("Login")
        attempts = [0]

        self.label("Account number:", 11, True).pack(anchor="w", padx=70, pady=(25, 3))
        acc_e = self.entry()
        acc_e.pack(fill="x", padx=70, ipady=4)

        self.label("PIN:", 11, True).pack(anchor="w", padx=70, pady=(12, 3))
        pin_e = self.entry(secret=True)
        pin_e.pack(fill="x", padx=70, ipady=4)

        def fail(msg):
            attempts[0] += 1
            left = 3 - attempts[0]
            if left <= 0:
                messagebox.showerror("Login failed", "Too many failed attempts. Process failed!")
                self.show_home()
            else:
                messagebox.showwarning("Login failed", f"{msg}\nYou have {left} attempts left.")

        def submit():
            acc_text = acc_e.get().strip()
            pin = pin_e.get().strip()

            if not acc_text.isdigit():
                messagebox.showwarning("Invalid", "Account number must be digits only.")
                return

            account = self.manager.get_account_by_account_number(int(acc_text))
            if account is None:
                fail("This account doesn't exist.")
            elif account.pin != pin:
                fail("Wrong PIN.")
            else:
                self.logged_in_account = account
                messagebox.showinfo("Welcome", f"Welcome back, {account.name}!")
                self.show_dashboard()

        self.button("Login", submit).pack(pady=22)
        self.button("Back", self.show_home).pack()

    # ---------------- القائمة الداخلية ----------------
    def show_dashboard(self):
        self.clear()
        acc = self.logged_in_account
        self.title_bar(f"Welcome, {acc.name}!")

        self.label(f"Account: {acc.account_number}   |   Balance: {acc.balance:.2f}",
                   12, True).pack(pady=(12, 8))

        for text, cmd in [("Deposit", self.do_deposit),
                          ("Withdraw", self.do_withdraw),
                          ("Transfer", self.show_transfer),
                          ("Check Balance", self.do_check_balance),
                          ("View My Details", self.do_view_details),
                          ("Change PIN", self.show_change_pin),
                          ("Transaction History", self.show_history),
                          ("Delete My Account", self.do_delete_account),
                          ("Logout", self.show_home)]:
            self.button(text, cmd).pack(fill="x", padx=70, pady=3)

    # ---------------- شاشة إدخال مبلغ ----------------
    def amount_screen(self, title, on_submit):
        self.clear()
        self.title_bar(title)

        self.label("Enter amount of money:", 12, True).pack(pady=(35, 6))
        amt_e = self.entry()
        amt_e.pack(fill="x", padx=90, ipady=5)

        def submit():
            try:
                amount = float(amt_e.get())
            except ValueError:
                messagebox.showwarning("Invalid", "Please enter a valid number.")
                return
            on_submit(amount)

        self.button("Confirm", submit).pack(pady=22)
        self.button("Back", self.show_dashboard).pack()

    # ---------------- إيداع ----------------
    def do_deposit(self):
        def submit(amount):
            if amount <= 0:
                messagebox.showwarning("Invalid", "Invalid amount. Please try again.")
                return
            acc = self.logged_in_account
            acc.balance += amount
            acc.transactions.append({"type": "deposit", "amount": amount,
                                     "balance_after": acc.balance})
            self.manager.save_accounts()
            messagebox.showinfo("Success", f"Deposit completed successfully!\nBalance: {acc.balance:.2f}")
            self.show_dashboard()
        self.amount_screen("Deposit", submit)

    # ---------------- سحب ----------------
    def do_withdraw(self):
        def submit(amount):
            acc = self.logged_in_account
            if amount <= 0:
                messagebox.showwarning("Invalid", "Invalid amount. Please try again.")
                return
            if amount > acc.balance:
                messagebox.showwarning("Invalid", "Insufficient funds.")
                return
            acc.balance -= amount
            acc.transactions.append({"type": "withdrawal", "amount": amount,
                                     "balance_after": acc.balance})
            self.manager.save_accounts()
            messagebox.showinfo("Success", f"Withdrawal completed successfully!\nBalance: {acc.balance:.2f}")
            self.show_dashboard()
        self.amount_screen("Withdraw", submit)

    # ---------------- تحويل ----------------
    def show_transfer(self):
        self.clear()
        self.title_bar("Transfer")

        self.label("Recipient's account number:", 11, True).pack(anchor="w", padx=70, pady=(25, 3))
        rec_e = self.entry()
        rec_e.pack(fill="x", padx=70, ipady=4)

        self.label("Amount:", 11, True).pack(anchor="w", padx=70, pady=(12, 3))
        amt_e = self.entry()
        amt_e.pack(fill="x", padx=70, ipady=4)

        def submit():
            rec_text = rec_e.get().strip()
            if not rec_text.isdigit():
                messagebox.showwarning("Invalid", "Account number must be digits only.")
                return
            try:
                amount = float(amt_e.get())
            except ValueError:
                messagebox.showwarning("Invalid", "Please enter a valid amount.")
                return

            sender = self.logged_in_account
            receiver_num = int(rec_text)

            if receiver_num == sender.account_number:
                messagebox.showwarning("Invalid", "Cannot transfer to your own account.")
                return
            receiver = self.manager.get_account_by_account_number(receiver_num)
            if receiver is None:
                messagebox.showwarning("Invalid", f"Account {receiver_num} does not exist.")
                return
            if amount <= 0:
                messagebox.showwarning("Invalid", "Invalid amount. Please try again.")
                return
            if amount > sender.balance:
                messagebox.showwarning("Invalid", "Insufficient funds.")
                return

            sender.balance -= amount
            receiver.balance += amount
            sender.transactions.append({"type": "transfer", "amount": amount,
                                        "to": receiver.account_number,
                                        "balance_after": sender.balance})
            receiver.transactions.append({"type": "received", "amount": amount,
                                          "from": sender.account_number,
                                          "balance_after": receiver.balance})
            self.manager.save_accounts()
            messagebox.showinfo("Success", f"Transfer completed successfully!\nBalance: {sender.balance:.2f}")
            self.show_dashboard()

        self.button("Transfer", submit).pack(pady=22)
        self.button("Back", self.show_dashboard).pack()

    # ---------------- باقي العمليات ----------------
    def do_check_balance(self):
        messagebox.showinfo("Balance", f"Balance: {self.logged_in_account.balance:.2f}")

    def do_view_details(self):
        acc = self.logged_in_account
        messagebox.showinfo("Account Details",
                            f"Account Number: {acc.account_number}\n"
                            f"Name: {acc.name}\n"
                            f"Balance: {acc.balance:.2f}")

    def show_change_pin(self):
        self.clear()
        self.title_bar("Change PIN")
        attempts = [0]

        self.label("New 4-digit PIN:", 11, True).pack(anchor="w", padx=70, pady=(25, 3))
        pin_e = self.entry(secret=True)
        pin_e.pack(fill="x", padx=70, ipady=4)

        def submit():
            new_pin = pin_e.get().strip()
            if len(new_pin) == 4 and new_pin.isdigit():
                self.logged_in_account.pin = new_pin
                self.manager.save_accounts()
                messagebox.showinfo("Success", "PIN successfully changed!")
                self.show_dashboard()
                return

            attempts[0] += 1
            left = 3 - attempts[0]
            if left <= 0:
                messagebox.showerror("Failed", "Failed after 3 tries. Operation cancelled.")
                self.show_dashboard()
            else:
                messagebox.showwarning("Invalid",
                                       f"PIN must be 4 digits only!\nYou have {left} attempts left.")

        self.button("Change PIN", submit).pack(pady=22)
        self.button("Back", self.show_dashboard).pack()

    def show_history(self):
        self.clear()
        self.title_bar("Transaction History")
        acc = self.logged_in_account

        t = self.text_box()
        t.pack(fill="both", expand=True, padx=45, pady=15)

        if not acc.transactions:
            t.insert("end", "No transactions found for this account.\n")
        for tr in acc.transactions:
            if tr["type"] == "transfer":
                t.insert("end", f"{tr['amount']} transferred to {tr['to']} | Balance: {tr['balance_after']}\n")
            elif tr["type"] == "received":
                t.insert("end", f"{tr['amount']} received from {tr['from']} | Balance: {tr['balance_after']}\n")
            else:
                t.insert("end", f"{tr['type']} amount: {tr['amount']} | Balance: {tr['balance_after']}\n")
        t.configure(state="disabled")

        self.button("Back", self.show_dashboard).pack(pady=(0, 15))

    def show_all_accounts(self):
        self.clear()
        self.title_bar("All Accounts (Admin)")

        t = self.text_box()
        t.pack(fill="both", expand=True, padx=45, pady=15)

        if not self.manager.accounts:
            t.insert("end", "No accounts found!\n")
        for acc in self.manager.accounts.values():
            t.insert("end", f"{acc}\n")
        t.configure(state="disabled")

        self.button("Back", self.show_home).pack(pady=(0, 15))

    def do_delete_account(self):
        acc = self.logged_in_account
        if messagebox.askyesno("Delete Account", "Are you sure you want to DELETE your account?"):
            self.manager.delete_account(acc.account_number)
            messagebox.showinfo("Deleted", "Account deleted successfully.")
            self.show_home()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()