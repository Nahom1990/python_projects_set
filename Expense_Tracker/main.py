from enum import Enum,auto
from datetime import datetime,timezone
class Expense_Categories(Enum):
    FOOD=auto()
    CLOTHS=auto()
    ENTERTAINMENT=auto()
    HEALTH=auto()
    RENT=auto()


class Expense:
    
    def __init__(self,
                 id:int,
                 description:str,
                 amount:float,
                 category:Expense_Categories) -> None:
        self.id=id
        self.description=description,
        self.amount=amount
        self.category=category
        self.create_date=datetime.now(timezone.utc).isoformat()

        if amount<0:
            raise ValueError("zero or negative expense not allowed")

    def update_expense(self,description,amount,category):
        self.description=description
        self.amount=amount
        self.category=category

    def __repr__(self):
        return f"id:{self.id} , description:{self.description} ,amount :{self.amount}, category:{self.category}"

class ExpenseManager:
    def __init__(self) -> None:
        self.expenses:list[Expense]=[]

    def add_expense(self,expense:Expense):
        self.expenses.append(expense)

    def update_expense(self,id,description,amount,category):          
        [expense.update_expense(description,amount,category) for expense in self.expenses if expense.id==id]

    def delete_expense(self,id):
        for expense in self.expenses:
            if expense.id==id:
                self.expenses.remove(expense)
                return

    def view_all_expenses(self):
        for expense in self.expenses:
            print(expense)
            print()

    def summary_of_expenses(self):
        total_expense=0
        for expense in self.expenses:
            total_expense+=expense.amount

        print(f"Total Expense: {total_expense}")

    def summary_expense_by_month(self,month:str):
        total_per_month=0.0
        for expense in self.expenses:
            date_obj = datetime.fromisoformat(expense.create_date)

            month_name = date_obj.strftime("%b").lower()
            if month_name==month.lower():
                total_per_month+=expense.amount
        print()
        print(f"Total Expense at {month}: {total_per_month}")
        print()

expense_1=Expense(0,"gym membership",20,Expense_Categories.HEALTH)
expense_2=Expense(1,"theather",15,category=Expense_Categories.ENTERTAINMENT)
expense_3=Expense(2,"lunch",30,category=Expense_Categories.FOOD)


expense_manager=ExpenseManager()
expense_manager.add_expense(expense_1)
expense_manager.add_expense(expense_2)
expense_manager.add_expense(expense_3)

expense_manager.view_all_expenses()

expense_manager.summary_of_expenses()

expense_manager.summary_expense_by_month(month="sep")