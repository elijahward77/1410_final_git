# just a comment to test how to change and save changes to a file in a repository
# more changes to the file
import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import messagebox
from datetime import datetime

#2 test, the first commit was committed and uploaded entirly in vs code

class Account(ABC):
    """Account class with account name, account balance, and transaction objects.
    Includes methods to deposit and withdraw money in accounts.
    Has getters to retrieve encapsulated information."""
    def __init__(self, name, initial_balance):
        self._name = name
        self._balance = float(initial_balance)
        self._transactions = []
        if self._balance < 0:
            raise ValueError("Initial balance cannot be negative.")
            
        if self._balance > 0:
            self._transactions.append(Transaction(self._balance, "Initial Deposit", "Income"))


    def deposit(self, amount, description, category):
        """Adds money to the account."""
        amount = abs(float(amount))
        if amount <= 0:
            return False, "Amount must be positive."
        
        self.category = category
        self._balance += amount
        self._transactions.append(Transaction(amount, description, self.category))
        return True, "Deposit successful. (Deposit category will labeled ""Income"")"

    def withdraw(self, amount, description, category):
        """Removes money from the account."""
        amount = abs(float(amount))
        if amount <= 0:
            return False, "Amount must be positive."
        if self._balance < amount:
            return False, "Insufficient funds."
            
        self.category = category
        self._balance -= amount
        self._transactions.append(Transaction(-amount, description, self.category))
        return True, "Withdrawal successful."
    

    # Getters for retrieving encapsulated data.
    def get_balance(self):
        return self._balance

    def get_name(self):
        return self._name

    def get_transactions(self):
        return list(self._transactions)   

class CheckingAccount(Account):
    """Checking account subclass of the Account Class
    from the apply_all_monthly_fees method, it simply doesn't add interest
    """
    def apply_monthly_fee(self):
        print(f"No fees or interest applied to Checking: {self.get_name()}")


class SavingsAccount(Account):
    """savings account subclass of the Account Class
    from the apply_all_monthly_fees method, it applies an interest to all savings accounts
    """
    def __init__(self, name, initial_balance, interest_rate=0.01):
        super().__init__(name, initial_balance)
        self._interest_rate = interest_rate

    def apply_monthly_fee(self):
        """Calculates and deposits monthly interest."""
        interest = self.get_balance() * (self._interest_rate / 12)
        if interest > 0:
            self.deposit(interest, "Monthly Interest", "Income")
        print(f"Interest applied to Savings: {self.get_name()}")

class Budget:
    """Manages budget categories and spending limits.
    **I ran out of time to finish the budget completely**
    """
    def __init__(self):
        self._categories = {}

    def create_new_bug_cat(self, new_category):
        """Create a new category when you withdraw something"""
        
        upper_cat = new_category.upper()
        if upper_cat in self._categories:
            pass
        else:
            self._categories[upper_cat] = 0.0

    def set_category_limit(self, category, limit):
        self._categories[category] = float(limit)

    def get_category_limit(self, category):
        return self._categories.get(category, 0.0)

    def get_all_categories(self):
        return list(self._categories.keys())

    def get_budget_summary(self):
        return self._categories.copy()
    
class Monthly:
    """Create a monthly payment dictionary that tracks Item and Monthly cost"""
    def __init__(self):
        self._expenses = {}

    def set_monthly_expense(self, expense, amount):
        self._expenses[expense] = float(amount)

    def get_monthly_expenses(self):
        return self._expenses

class Transaction():
    """This class will store all the transactions
    It stores the amount, category, and description that is created by every transaction"""
    def __init__(self, amount, category, description):
        self.category = category
        self.amount = amount
        self.description = description
        self.date = datetime.now()

    def __str__(self):
        date_record = self.date.strftime("%Y-%m-%d")
        amount_type = "Deposit" if self.amount > 0 else "Withdrawal"
        return f"[{date_record}] {amount_type}: ${abs(self.amount):.2f} - {self.description} ({self.category})"


class FinanceManager:
    """
    A class to control all the account logic. It controls account creation
    and monthly payment processing.
    """
    def __init__(self):
        self._accounts = {}
        self._budget = Budget()
        self._recurring_expenses = []

    def add_account(self, name, acc_type, initial_balance):
        if name in self._accounts:        # Checks if there is already an account of the same name
            return False, "Account with this name already exists."
        
        if acc_type == "Checking":
            account = CheckingAccount(name, initial_balance)
        elif acc_type == "Savings":
            account = SavingsAccount(name, initial_balance)
        else:
            return False, "Invalid account type."
            
        self._accounts[name] = account
        return True, "Account created."

    def get_account(self, name):
        return self._accounts.get(name)

    def get_all_account_names(self):
        return list(self._accounts.keys())

    def get_budget(self):
        return self._budget    

    def get_recurring_expenses(self):
        return list(self._recurring_expenses)
        
    def process_recurring_expenses(self, default_account_name):
        """
        Checks today's date and processes any recurring expenses.
        """
        account = self.get_account(default_account_name)
        if not account:
            return f"Error: Default account '{default_account_name}' not found."
            
        today = datetime.now().day
        processed_log = ""
        for expense in self._recurring_expenses:
            if expense.day_of_month == today:
                # Checks if it was already paid this month
                today_str = datetime.now().strftime("%Y-%m-%d")
                already_paid = False
                for txn in account.get_transactions():
                    if (txn.date.day == today and
                        txn.date.month == datetime.now().month and
                        txn.description == expense.description):
                        already_paid = True
                        break
                        
                if not already_paid:
                    success, msg = account.withdraw(expense.amount,
                                                    expense.description,
                                                    expense.category)
                    if success:
                        processed_log += f"Processed: {expense.description}\n"
                    else:
                        processed_log += f"Failed to process {expense.description}: {msg}\n"
        return processed_log if processed_log else "No recurring expenses for today."

    # This method loops through all accounts, checking if its
    # a checking or savings account and calls the
    # 'apply_monthly_fee_or_interest' method on each.
    def apply_all_monthly_updates(self):
        """
        Applies fees or interest to each account polymorphically.
        """
        log = "Applying monthly updates...\n"
        for account in self._accounts.values():
            account.apply_monthly_fee()
            log += f"Updated {account.get_name()}.\n"
        return log



    def end_of_month_process(self):
        results = []
        for acc in self.accounts.values():
            # Calls the specific version of the method based on object type
            results.append(acc.apply_monthly_logic())
        return "\n".join(results)

    def apply_monthly_expenses_to_account(self, account_name, monthly_data):
        """Applies a dictionary of monthly expenses as withdrawals to an account"""
        account = self.get_account(account_name)
        if not account:            # Checks if the account actually exists
            return f"Error: Account '{account_name}' not found."

        total_withdrawn = 0
        log = []
        
        # Processes recurring payments
        for expense, amount in monthly_data.items():
            success, message = account.withdraw(amount, f"Monthly: {expense}", "Expense")
            if success:
                total_withdrawn += amount
            else:
                log.append(f"Failed to apply {expense}: {message}")
        
        if total_withdrawn > 0:
            log.insert(0, f"Successfully applied {len(monthly_data)} expenses to {account_name}. Total withdrawn: ${total_withdrawn:.2f}")
        
        return "\n".join(log) if log else "No expenses applied (or no expenses set)."






class FinanceApp():
    """
    The Main GUI class
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Student Finance Manager")
        self.root.geometry("800x650")
        self.manager = FinanceManager()

        # buttons to open the budget window and monthly payment window
        self.budget_button = tk.Button(self.root, text="Open Budget Window", command=self.open_budget)
        self.budget_button.pack(pady=5)
        self.monthly_button = tk.Button(self.root, text="Open Monthly Expenses Window", command=self.open_monthly)
        self.monthly_button.pack(pady=5)

        #account creation frame
        frame_top = tk.Frame(self.root, pady=10)
        frame_top.pack()
        self.create_account_label = tk.Label(frame_top, text="New Account Name:")
        self.create_account_label.pack(side=tk.LEFT)

        # Account name entry
        self.account_name = tk.Entry(frame_top, width=10)
        self.account_name.pack(side=tk.LEFT, padx=5)
        self.acc_type = tk.StringVar(value="Checking")

        # Initial balance entry
        self.create_balance_label = tk.Label(frame_top, text="Enter the Initial Balance:")
        self.create_balance_label.pack(side=tk.LEFT)
        self.initial_balance = tk.Entry(frame_top, width = 10)
        self.initial_balance.pack(side=tk.LEFT, padx=5)

        # option for changing account type and creating the account button
        tk.OptionMenu(frame_top, self.acc_type, "Checking", "Savings").pack(side=tk.LEFT)
        self.add_buddon = tk.Button(frame_top, text="Add", command=self.create_account)
        self.add_buddon.pack(side=tk.LEFT)
        
        #account listbox to display created accounts and select them to apply transactions
        tk.Label(self.root, text="Accounts:", font=10).pack(pady=5)
        self.account_listbox = tk.Listbox(self.root, height=5)
        self.account_listbox.pack(fill=tk.X, padx=20)
        self.account_listbox.bind("<<ListboxSelect>>", self.account_select)
        
        txn_frame = tk.Frame(self.root)
        txn_frame.pack(side="right", fill="both", expand=True, padx=5)
        
        # display account and total balance
        self.txn_label = tk.Label(txn_frame, text="Select an Account", font=( 14))
        self.txn_label.pack(pady=5)
        self.txn_balance_label = tk.Label(txn_frame, text="Balance: $0.00", font=( 12))
        self.txn_balance_label.pack(pady=5)

        # Shows transaction history
        self.txn_listbox = tk.Listbox(txn_frame, height=10)
        self.txn_listbox.pack(fill="x", expand=False, pady=5)
        
        # Transaction frame
        add_txn_frame = tk.LabelFrame(txn_frame, text="Add a Transaction")
        add_txn_frame.pack(fill="x", expand=False, pady=5)
        
        # enter transaction amount
        tk.Label(add_txn_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=3)
        self.txn_amount_entry = tk.Entry(add_txn_frame)
        self.txn_amount_entry.grid(row=0, column=1, padx=5, pady=3)
        
        # enter a transaction description
        tk.Label(add_txn_frame, text="Description:").grid(row=1, column=0, padx=5, pady=3)
        self.txn_desc_entry = tk.Entry(add_txn_frame)
        self.txn_desc_entry.grid(row=1, column=1, padx=5, pady=3)
        
        # enter a transaction category (will default to income if it's a deposit)
        tk.Label(add_txn_frame, text="Category:").grid(row=2, column=0, padx=5, pady=3)
        self.txn_category = tk.Entry(add_txn_frame)
        


        self.txn_category.grid(row=2, column=1, padx=5, pady=3)
        
        txn_btn_frame = tk.Frame(add_txn_frame)
        txn_btn_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        deposit_btn = tk.Button(txn_btn_frame, text="Deposit", command=self.create_deposit)
        deposit_btn.pack(side="left", padx=5)
        withdraw_btn = tk.Button(txn_btn_frame, text="Withdraw", command=self.create_withdraw)
        withdraw_btn.pack(side="left", padx=5)

    # button command to open windows
    def open_budget(self):
        BudgetWindow(self)
    def open_monthly(self):
        MonthlyWindow(self, self.manager)

    # button command to create an account
    def create_account(self):
        name = self.account_name.get()
        balance_str = self.initial_balance.get()
        acc_type = self.acc_type.get()
        
        if not name:
            messagebox.showerror("Error", "Account name cannot be empty.")
            return
           
        try:
            Account._balance = float(balance_str) if balance_str else 0.0
        except ValueError:
            messagebox.showerror("Error", "Initial balance must be a number.")
            return
            
        success, msg = self.manager.add_account(name, acc_type, Account._balance)
        if success:
            messagebox.showinfo("Success", msg)
            self.account_name.delete(0, "end")   
            self.initial_balance.delete(0, "end")
            self.refresh_account_list()          
        else:
            messagebox.showerror("Error", msg)

    def account_select(self, event=None):
        """Updates the transaction view when an account is selected."""
        try:
            selected_index = self.account_listbox.curselection()[0]
            selected_text = self.account_listbox.get(selected_index)
            account_name = selected_text.split(" ($")[0]
            
            account = self.manager.get_account(account_name)
            if not account:
                return
                
            self.txn_label.config(text=f"Account: {account.get_name()}")
            self.txn_balance_label.config(text=f"Balance: ${account.get_balance():.2f}")

            # Refresh transaction list
            self.txn_listbox.delete(0, "end")
            transactions = account.get_transactions()
            for txn in reversed(transactions): 
                self.txn_listbox.insert("end", str(txn))
                
        except IndexError:
            pass

        try:
            selected_index = self.account_listbox.curselection()[0]
            selected_text = self.account_listbox.get(selected_index)
            return selected_text.split(" ($")[0]
        except IndexError:
            return None

    def refresh_account_list(self):
        """Updates the listbox with account names and balances."""
        self.account_listbox.delete(0, "end")
        names = self.manager.get_all_account_names()
        for name in names:
            balance = self.manager.get_account(name).get_balance()
            self.account_listbox.insert("end", f"{name} (${balance:.2f})")


    def get_selected_account(self):
        try:
            index = self.account_listbox.curselection()[0]
            selected_text = self.account_listbox.get(index)
            return selected_text.split(" ($")[0]
        except IndexError:
            return None


    def create_deposit(self):
        """
        Gets all the entered info for the deposit and 
        stores and handles all that info.
        """
        account = self.get_selected_account()
        if not account:
            messagebox.showerror("Error", "Please choose an account.")
            return
        try:
            amount = float(self.txn_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return
        
        description = self.txn_desc_entry.get() or "Deposit"
        category = "Income"

        account = self.manager.get_account(account)
        success, msg = account.deposit(amount, description, category)

        # if it all checks out show a success message and 
        # run the transaction and record it.
        if success:
            messagebox.showinfo("Success", msg)
            self.txn_amount_entry.delete(0, "end")
            self.txn_desc_entry.delete(0, "end")
            self.txn_category.delete(0, "end")
            self.account_select() 
            self.refresh_account_list()  
        else:
            messagebox.showerror("Error", msg)


    # withdrawal button command
    # withdraws money from specified account
    def create_withdraw(self):
        account = self.get_selected_account()
        category = self.txn_category.get()
        description = self.txn_desc_entry.get() or "Withdrawal"
        if not account:
            messagebox.showerror("Error", "Please choose an account.")
            return
        try:
            amount = float(self.txn_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return
        
        if not category:
            messagebox.showerror("Error", "Category cannot be blank.")
            return
        
        # create a new category in the budget with a limit of 0 if you use a new category
        # when you withdraw something.
        manager_budget = self.manager.get_budget()
        manager_budget.create_new_bug_cat(category)
        account_obj = self.manager.get_account(account)

        
        success, msg = account_obj.withdraw(amount, description, category)
        if success:
            messagebox.showinfo("Success", msg)
            self.txn_amount_entry.delete(0, "end")
            self.txn_desc_entry.delete(0, "end")
            self.txn_category.delete(0, "end")
            self.account_select() 
            self.refresh_account_list()  
        else:
            messagebox.showerror("Error", msg)

# the BudgetWindow class with all the tkinter programs
class BudgetWindow(FinanceApp):
    def __init__(self, main_app):
        self.main_app = main_app
        self.manager = main_app.manager 
        self.win = tk.Toplevel(main_app.root) 
        self.win.title("Budget Window")  
        self.win.geometry("500x500")


        create_budget = tk.Frame(self.win)
        create_budget.pack(fill="both", expand=True, padx=5)


        set_budget_frame = tk.LabelFrame(create_budget, text="Set Budget Category")
        set_budget_frame.pack(fill="x", pady=5)

        tk.Label(set_budget_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.budget_category_entry = tk.Entry(set_budget_frame)
        self.budget_category_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(set_budget_frame, text="Limit:").grid(row=0, column=2, padx=5, pady=5)
        self.budget_limit_entry = tk.Entry(set_budget_frame)
        self.budget_limit_entry.grid(row=0, column=3, padx=5, pady=5)
        
        set_budget_btn = tk.Button(set_budget_frame, text="Set/Update", command = self.set_budget) 
        set_budget_btn.grid(row=0, column=4, padx=10, pady=5)

        my_budget_frame = tk.LabelFrame(create_budget, text="My Budget goal:")
        my_budget_frame.pack(fill="x", expand=True, pady=5)

        self.budget_list = tk.Listbox(my_budget_frame, height=8)
        self.budget_list.pack(fill="both", expand=True, padx=5, pady=3)
    

    def set_budget(self):
        category = self.budget_category_entry.get()
        limit_str = self.budget_limit_entry.get()
        
        if not category:
            messagebox.showerror("Error", "Category name cannot be empty.")
            return
            
        try:
            limit = float(limit_str)
        except ValueError:
            messagebox.showerror("Error", "Limit must be a number.")
            return
            
        self.main_app.manager.get_budget().set_category_limit(category, limit)
        messagebox.showinfo("Success", f"Budget for '{category}' set to ${limit:.2f}.")
        
        self.budget_list.insert(tk.END,f"{category} - ${limit_str:.2f}")
        self.budget_category_entry.delete(0, "end")
        self.budget_limit_entry.delete(0, "end")
        
# MonthlyWindow class that handles multiple transactions to multiple accounts at the same time.
class MonthlyWindow():
    def __init__(self, main_app, manager):
        self.month = Monthly()
        self.main_app = main_app
        self.manager = manager
        self.win = tk.Toplevel(main_app.root)
        self.win.title("Monthly Expenses Window")  
        self.win.geometry("550x550")
        
        create_monthly_expense = tk.Frame(self.win)
        create_monthly_expense.pack(fill="both", expand=True, padx=5)


        set_monthly_frame = tk.LabelFrame(create_monthly_expense, text="Set Monthly Expenses")
        set_monthly_frame.pack(fill="x", pady=5)
        
        # name the monthly expense
        tk.Label(set_monthly_frame, text="Payment:").grid(row=0, column=0, padx=5, pady=5)
        self.item_name = tk.Entry(set_monthly_frame)
        self.item_name.grid(row=0, column=1, padx=5, pady=5)
        

        # Set the monthly payment amount
        tk.Label(set_monthly_frame, text="Monthly Amount:").grid(row=0, column=2, padx=5, pady=5)
        self.monthly_amount_entry = tk.Entry(set_monthly_frame)
        self.monthly_amount_entry.grid(row=0, column=3, padx=5, pady=5)

        self.set_monthly_btn = tk.Button(set_monthly_frame, text="ADD", command = self.create_monthly_expense) 
        self.set_monthly_btn.grid(row=0, column=4, padx=10, pady=5)

        show_monthly_expenses = tk.Frame(self.win)
        show_monthly_expenses.pack(fill="x", expand=True, padx=5)

        tk.Label(show_monthly_expenses, text="Monthly Expenses:").pack(pady=5)
        self.expenses_listbox = tk.Listbox(show_monthly_expenses, height=8)
        self.expenses_listbox.pack(fill="x", pady=3)

        # choose which account to apply monthly payments to 
        self.monthly_account_label = tk.Label(show_monthly_expenses, text="Choose account for monthly expenses:")
        self.monthly_account_label.pack(pady=5)
        self.monthly_account = tk.Entry(show_monthly_expenses)
        self.monthly_account.pack(pady=5)
        self.get_account_btn = tk.Button(show_monthly_expenses, text="Apply expenses", command=self.apply_monthly_expense)
        self.get_account_btn.pack(pady=5)

        # button that applies monthly interest rates
        poly_button = tk.Button(show_monthly_expenses, text="Apply All Monthly Interest", command=self.run_monthly_updates)
        poly_button.pack(pady=5)

    # the monthly expense command. creates the created monthly expenses
    def create_monthly_expense(self):
        name = self.item_name.get()
        amount = self.monthly_amount_entry.get().strip()

        if not name or not amount:
            messagebox.showerror("input error", "Please enter both name and amount")
            return
        else:
            try:
                amount = float(amount)
            except ValueError:
                messagebox.showerror("input error", "Amount must be a number.")
                return
            self.month.set_monthly_expense(name, amount)
            messagebox.showinfo("Success", f"Monthly expense '{name}' for ${amount:.2f} set.")

            self.expenses_listbox.insert(tk.END,f"{name} - ${amount:.2f}")
            self.item_name.delete(0,tk.END)
            self.monthly_amount_entry.delete(0,tk.END)


    # applies all the monthly expenses to the selected account
    def apply_monthly_expense(self):
        account_name = self.monthly_account.get()

        if not account_name:
            messagebox.showerror("input error", "Please enter an account name")
            return
        if account_name not in self.manager.get_all_account_names():
            messagebox.showerror("Error", f"Account '{account_name}' has not been created.")
            return
        
        monthly_data = self.month.get_monthly_expenses()

        if not monthly_data:
            messagebox.showwarning("Warning", "No monthly expenses have been set yet.")
            return
        
        log = self.manager.apply_monthly_expenses_to_account(account_name, monthly_data)
        self.monthly_account.delete(0, tk.END)
        messagebox.showinfo("Success", log)


    # applies monthly interest to all savings accounts
    def run_monthly_updates(self):
        apply = self.manager.apply_all_monthly_updates()
        messagebox.showinfo("Monthly Updates", apply)

if __name__ == "__main__":
    root = tk.Tk()
    
    app = FinanceApp(root)
    
    root.mainloop()