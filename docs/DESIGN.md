The Account class manages the account name balance and transaction objects. It also includes the methods to deposit and withdraw money in those accounts.

The ChecckingAccount and SavingsAccount are subclasses of the Account class and manage the method that applies monthly transactions.

The Budget class manages the budget category objects and methods for creating new categories.

The Monthly class manages an expenses object and the methods for creating the monthly expense.

The Transaction class stores all the transactions made by withdrawals and deposits in the account class, and records the date they were made.

The FinanceManager class controls all the Account class logic, account creation and monthly payment processing methods. 

The FinanceApp class manages the main tkinter window where accounts can be created, transactions can be made and account and transaction information will be displayed.

The BudgetWindow class, manages creating budget categories and size of the budget. This window has not been finished yet but when you assign a category to a withdrawal in the main window it will create a new budget category with 0 limit. 

The Monthly budget window is where you can create a monthly recurring object. Every object on their amount can be withdrawn from an account all at the same time here. You can also apply a monthly interest to all savings accounts but the interest amount is currently fixed and cannot be changed.


A factory pattern seperates the GUIs from account creation and operations by calling other classes to run those functions.


Future Improvements:
finish the budget window
create an ability to change the account's monthly interest rate


Developing this program, I learned a lot about different techniques for designing tkinter programs. I learned how to use the tk.frame and pack more effectively.
I also learned I should not make projects too complicated because I definitely made this one more complicated than I orginally thought I was going to.

