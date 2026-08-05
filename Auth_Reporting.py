from account import Account_Manager

class Auth_Reporting:
    def __init__(self, account_management: Account_Manager):
        self.account_management = account_management

    def login(self):
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            try:
                account_number = int(input("Please Enter your account number: "))
            except ValueError:
                print(f"Invalid input. {max_attempts - (attempts + 1)} attempts left.")
                attempts += 1
                continue
            
            account = self.account_management.get_account_by_account_number(account_number)

            if account is None:
                print(f"This account doesn't exist, you have {max_attempts - (attempts + 1)} attempts left!")
                attempts += 1
                continue
            
            if self.account_management.verify_pin(account):
                print("Access granted!")
                return account
            
            print(f"Wrong PIN. {max_attempts - (attempts + 1)} attempts left")
            attempts += 1
            
        print("Too many failed attempts. Process failed!")
        return None

    def change_pin(self, logged_in_account=None):
        print("-----Change PIN-----")
        
        # If user is already logged in, skip account/PIN verification
        if logged_in_account:
            account = logged_in_account
            print(f"Changing PIN for account {account.account_number}")
        else:
            # Fallback for admin/unauthenticated use
            print("Enter account number or 'exit' to cancel:")
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

            print("Please enter your old PIN: ")
            if not self.account_management.verify_pin(account):
                print("Old PIN verification failed.")
                return

        #
        new_pin = None
        for attempt in range(1, 4):
            input_pin = input("Please enter your new 4-digit PIN: ")
            if len(input_pin) == 4 and input_pin.isdigit():
                new_pin = input_pin
                break
            
            remaining = 3 - attempt
            print(f"PIN must be 4 digits only! You have {remaining} attempts left.")
            if remaining == 0:
                print("Failed after 3 tries. Operation cancelled.")
                return

        try:
            account.pin = new_pin
            print("PIN successfully changed!")
            self.account_management.save_accounts()
        except Exception as e:
            print(f"PIN not changed. Error: {e}")

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
                print(f"{t['amount']} transferred to {t['to']}, Balance: {t['balance_after']}")
            elif t["type"] == "received":
                print(f"{t['amount']} received from {t['from']}, Balance: {t['balance_after']}")
            else:
                print(f"{t['type']} amount: {t['amount']}, Balance: {t['balance_after']}")

    def list_all_accounts(self):
        if not self.account_management.accounts:
            print("No accounts found!")
            return
        print("-----All Accounts-----")
        for acc in self.account_management.accounts.values():
            print(acc)
        print("-----------------------")