from account import Account_Manager
from transactions import deposit, withdraw, transfer, check_balance
from Auth_Reporting import Auth_Reporting

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter digits only.")

def main():
    manager = Account_Manager()
    auth = Auth_Reporting(manager)
    logged_in_account = None

    while True:
        print("\n************** Welcome to NOVA Bank **************")
        
        # --- PRE-LOGIN MENU ---
        if logged_in_account is None:
            print("1. Create New Account")
            print("2. Login")
            print("3. List All Accounts (Admin)")
            print("4. Exit")
            
            choice = input("Choose an operation (1-4): ").strip()
            
            if choice == "1":
                manager.create_account_interactive()
            elif choice == "2":
                logged_in_account = auth.login()
                if logged_in_account:
                    print(f"\n Welcome back, {logged_in_account.name}!")
                else:
                    print("\n Login failed. Please try again.")
            elif choice == "3":
                auth.list_all_accounts()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please choose 1-4.")

        # after login menu
        else:
            print(f"Logged in as: {logged_in_account.name} (Acc: {logged_in_account.account_number})")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Transfer")
            print("4. Check Balance")
            print("5. View My Details")
            print("6. Change PIN")
            print("7. Transaction History")
            print("8. Delete My Account")
            print("9. Logout")
            
            choice = input("Choose an operation (1-9): ").strip()
            
            if choice == "1":
                try:
                    deposit(logged_in_account)
                    manager.save_accounts()
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == "2":
                try:
                    withdraw(logged_in_account)
                    manager.save_accounts()
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == "3":
                receiver_num = get_int("Enter recipient's account number: ")
                if receiver_num == logged_in_account.account_number:
                    print("Cannot transfer to your own account.")
                else:
                    receiver = manager.get_account_by_account_number(receiver_num)
                    if receiver is None:
                        print(f"Account {receiver_num} does not exist.")
                    else:
                        try:
                            transfer(logged_in_account, receiver)
                            manager.save_accounts()
                        except ValueError as e:
                            print(f"Error: {e}")
                            
            elif choice == "4":
                check_balance(logged_in_account)
                
            elif choice == "5":
                manager.view_account_details(logged_in_account.account_number)
                
            elif choice == "6":
                # Pass logged_in_account so it doesn't ask for PIN again
                auth.change_pin(logged_in_account)
                
            elif choice == "7":
                auth.transaction_history(logged_in_account.account_number)
                
            elif choice == "8":
                confirm = input("Are you sure you want to DELETE your account? (yes/no): ").strip().lower()
                if confirm == "yes":
                    manager.delete_account(logged_in_account.account_number)
                    manager.save_accounts()
                    print("Account deleted successfully.")
                    logged_in_account = None
                else:
                    print("Deletion cancelled.")
                    
            elif choice == "9":
                print(f"Goodbye, {logged_in_account.name}!")
                logged_in_account = None
                
            else:
                print("Invalid choice. Please choose 1-9.")

if __name__ == "__main__":
    main()