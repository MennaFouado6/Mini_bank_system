import json
import os

#Account
class Account:
  def __init__(self,account_number,name,pin,balance = 0):
    self.account_number = account_number
    self.name = name
    self.pin = pin
    self.balance = balance

  def __repr__(self):
    return f"Account ({self.account_number}, {self.name}, Balance: {self.balance})"
  #nhwel el acc fe dictionary aashan neaarf n7fzo fel malaf
  def to_dict(self):
    return{
        "account_number": self.account_number,
        "name": self.name,
        "pin": self.pin,
        "balance": self.balance
    }
  #nrg3 el hesab mn el dictionary
  @classmethod
  def from_dict(cls,data):
    return cls(
        account_number = int(data["account_number"]),
        name = data["name"],
        pin = data["pin"],
        balance = float(data.get("balance",0)),
    )

#Account Manager
class Account_Manager:
  def __init__(self,filename = "accounts.json"):
    self.filename = filename
    self.accounts = {}
    self.next_account_number = 1001
    self.load_accounts()

  #when it opens and read the accounts in the files
  def load_accounts(self):
    if not os.path.exists(self.filename):
      return
    try:
      with open(self.filename,"r",encoding = "utf-8") as file:
       accounts_data = json.load(file)
      for account_data in accounts_data:
        account = Account.from_dict(account_data)
        self.accounts[account.account_number] = account
      if self.accounts:
        self.next_account_number = max(self.accounts.keys()) + 1

    except Exception as e:
      print(f"Warning: Could not load accounts. Startung with empty accounts. ({e})")
      self.accounts = {}
      self.next_account_number = 1001

  def save_accounts(self):
    try:
      with open(self.filename,"w",encoding="utf-8") as file:
        accounts_as_dicts = [account.to_dict() for account in self.accounts.values()]
        json.dump(accounts_as_dicts,file,indent=2)
    except Exception as e:
      print(f"Warning: Could not save accounts. ({e})")


  #Account input from the user
  def create_account_interactive(self):
    print("-----Create New Account-----")
    while True:
      name = input("Enter your name:").strip()
      if name:
        break
      print("Name cannot be empty. Please try again.")
    pin = None
    for attempt in range(1,4):
      pin_input = input(f"Enter your PIN (4 numbers only) - attempt {attempt}/3: ")
      if pin_input.isdigit() and len(pin_input) == 4:
        pin = pin_input
        break

      remaining = 3 - attempt
      if remaining > 0:
        print(f"Invalid PIN. PIN must be a 4-digit number. You have {remaining} tries left.")

    if pin is None:
      print("You failed to enter a valid PIN after 3 tries. Operation cancelled.")
      return None

    while True:
      balance_input = input("Enter your initial balance (0 or more): ")
      try:
        initial_balance = float(balance_input)
        if initial_balance < 0:
          print("Balance cannot be negative. Please try again.")
          continue
        break
      except ValueError:
        print("Invalid input. Please enter a number.")
    try:
      return self.create_account(name,pin,initial_balance)
    except ValueError as e:
      print(f"Could not create account: {e}")
      return None

  #Making sure everything is correct
  def create_account(self,name,pin,initial_balance = 0):
    if not name or not name.strip():
      raise ValueError("Name cannot be empty")

    if not pin.isdigit() or len(pin) != 4:
      raise ValueError("Invalid PIN. PIN must be a 4-digit number")

    if initial_balance < 0:
      raise ValueError("Initial balance cannot be negative")

    account_number = self.next_account_number
    self.next_account_number += 1

    new_account = Account(account_number,name,pin,initial_balance)
    self.accounts[account_number] = new_account

    self.save_accounts()

    print(f"Account created successfully. Account number: {account_number}")
    return new_account

  def get_account_by_account_number(self,account_number):
    return self.accounts.get(account_number)


  #Delete the account
  def delete_account(self,account_number):
    if account_number not in self.accounts:
      raise ValueError(f"Account {account_number} does not exist")

    del self.accounts[account_number]
    self.save_accounts()
    print(f"Account {account_number} has been deleted successfully")

  #verify pin only 3 times
  def verify_pin(self,account):
    print(f"Enter PIN for account {account.account_number}")

    for attempt in range (1,4):
      entered_pin = input(f"PIN attempt {attempt}/3: ")

      if entered_pin == account.pin:
        return True
      remaining = 3 - attempt
      if remaining > 0:
        print(f"Wrong PIN. You have {remaining} tries left")

    print("Wrong PIN 3 times. Operation cancelled")
    return False

  #When the user put an account that doesn't exist
  def delete_account_interactive(self):
    print("-----Delete Account-----")
    while True:
      account_input = input("Enter the account number to delete (or type 'exit' to cancel): ")

      if account_input.lower() == "exit":
        print("Operation cancelled")
        return
      try:
        account_number = int(account_input)

      except ValueError:
        print("Invalid account number. Please enter digits only.")
        print("----Please try again----")
        continue
      account = self.get_account_by_account_number(account_number)
      if account is None:
        print(f"Account {account_number} does not exist")
        print("----Please try again----")
        continue

      if not self.verify_pin(account):
        return

      try:
        self.delete_account(account_number)
        return

      except ValueError as e:
        print(e)
        print("----Please try again----")


  #enter your account number to know your details
  def view_account_details_interactive(self):
    print("-----Search by Account Number-----")
    while True:
      account_input = input("Enter the account number to view details (or type 'exit' to cancel): ")
      if account_input.lower() == "exit":
        print("Operation is cancelled.")
        return

      try:
        account_number = int(account_input)

      except ValueError:
        print("Invalid account number. Please enter digits only. ")
        print("----Please try again----")
        continue

      account = self.get_account_by_account_number(account_number)

      if account is None:
        print(f"Account {account_number} does not exist")
        print("----Please try again----")
        continue

      if not self.verify_pin(account):
        return

      try:
        self.view_account_details(account_number)
        return
      except ValueError as e:
        print(e)
        print("----Please try again----")

  #View the account details
  def view_account_details(self,account_number):
    account = self.get_account_by_account_number(account_number)
    if account is None:
      raise ValueError(f"Account {account_number} does not exist")

    print("-----Account Details-----")
    print(f"Account Number: {account.account_number}")
    print(f"Name: {account.name}")
    print(f"Balance: {account.balance}")
    print("-------------------------")

  #Search the account by name
  def search_account_by_name(self,name):
    results = []
    for account in self.accounts.values():
      if name.lower() == account.name.lower():
        results.append(account)
    return results

  #SEARCH ACCOUNT INERACTIVE
  def search_account_by_name_interactive(self):
    print("-----Search by Name-----")
    name = input("Enter the name to search (or type 'exit' to cancel): ")
    if name.lower() == "exit":
      print("Operation is cancelled.")
      return
    if not name:
      print("Name cannot be empty")
      return
    results = self.search_account_by_name(name)

    if not results:
      print(f"No accounts found with the name '{name}'.")
      return

    print(f"Found {len(results)} account(s)")
    print("-------------------------")

    for account in results:
      print(f"Account Number: {account.account_number}")
      print(f"Name: {account.name}")
      print(f"Balance: {account.balance}")
      print("-------------------------")

def main():
  manager = Account_Manager()

  while True:
    print("\n**************Welcome to our bank**************")
    print("1. Create New Account")
    print("2. Delete Account")
    print("3. View Account Details")
    print("4. Search Account by Name")
    print("5. Exit")

    choice = input("Choose an operation (1-5): ").strip()

    if choice == "1":
      manager.create_account_interactive()

    elif choice == "2":
      manager.delete_account_interactive()

    elif choice == "3":
      manager.view_account_details_interactive()

    elif choice == "4":
      manager.search_account_by_name_interactive()

    elif choice == "5":
      print("Goodbye!")
      break

    else:
      print("Invalid choice. Please choose a number from 1 to 5.")


if __name__ == "__main__":
  main()