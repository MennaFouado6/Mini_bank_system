from account import Account_Manager #from shahd

class Auth_Reporting:
  def __init__(self, account_management):
    account_management = Account_Manager()
    self.account_management = account_management

  def login(self):
    account_number = int(input("Please Enter your account number: "))
    account = self.account_management.get_account_by_account_number(account_number)
    if account is None:
      print("This account doesn't exist")
      return None
    if not self.account_management.verify_pin(account):
      print("Access not granted!")
      return None
    print("Access granted")
    return account


  def change_pin(self):
      print("-----Change PIN-----")
      print("To proceed to change your pin, First enter your account number or (exit to cancel operation)")
      account_input = input()
      if account_input.lower() == "exit":
        print("Operation cancelled")
        return

      try:
        account_number = int(account_input)
      except ValueError:
        print("Invalid account number!")
        return

      account = self.account_management.get_account_by_account_number(account_number)
      if account is None:
        print(f"Account {account_number} doesn't exist")
        return

      print("Please enter your old pin: ")
      old_pin_auth = self.account_management.verify_pin(account_number)
      if not old_pin_auth:
        return

      new_pin = None
      for attempts in range(3):
        input_pin = int(input("Please enter your new pin: "))
        if len(input_pin) == 4 and input_pin.isdigit():
          new_pin = input_pin
          break
  
        remaining_attempts = 3 - attempts
        print(f"Pin must be in four digits only! You have {remaining_attempts} attempt")
        if remaining_attempts == 0:
          print("You failed to enter a valid PIN after 3 tries. Operation cancelled.")
          return
      try:
        account.pin = new_pin
        print("Pin successfully changed")
        self.account_management.save_accounts()
      except Exception as e:
        print(f"Pin not changed, Error: {e}")
  

  def transaction_history(self, account_number):
    account = self.account_management.get_account_by_account_number(account_number)
    if account is None:
        print(f"Account {account_number} does not exist")
        return

    if not account.transactions:
      print("No transactions found for this account.")
      return

    print(f"-----Transaction History for {account}-----")
    for t in account.transactions:
      if t["type"] == "transfer":
        print(f"{t["amount"]} transfered to {t["to"]}, Sender balance now is: {t["balance_after"]}")
      elif t["type"] == "recieved":
        print(f"{t["amount"]} recieved from {t["from"]}, Receiver balance now is: {t["balance_after"]}")
      else:
        print(f"{t['type']} amount is: {t['amount']}, Balance now is: {t['balance_after']}") #deposit or withdraw
   #end of transaction history
   
  def list_all_accounts(self):
    if not self.account_management.accounts:
      print("No accounts found!")
      return
    print("-----All Accounts-----")
    for account_ in self.account_management.accounts.values():
      print(account_)
    print("-----------------------")
    #end of list all accs