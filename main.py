from account import Account_Manager
from transactions import deposit, withdraw, transfer,check_balance


def main():
    manager = Account_Manager()

    while True:
        print("\n**************Welcome to our bank**************")
        print("1. Create New Account")
        print("2. Deleter Account")
        print("3. View Account Details")
        print("4. Search Account by Name")
        print("5. Deposit")
        print("6. Withdraw")
        print("7. Transfer")
        print("8. Check Balance")
        print("9. Exit")

        choice = input("Choose an operation (1-9): ").strip()

        if choice == "1":
            manager.create_account_interactive()

        elif choice == "2":
            manager.delete_account_interactive()

        elif choice == "3":
            manager.view_account_details_interactive()

        elif choice == "4":
            manager.search_account_by_name_interactive()

        elif choice == "5":
            account_number = int(input("Enter your account_number: "))
            account = manager.get_account_by_account_number(account_number)
            if account is None:
                print(f"Account {account_number} does not exist.")
            elif manager.verify_pin(account):
                try:
                    deposit(account)
                    manager.save_accounts()
                except ValueError as e:
                    print(f"Error: {e}")


        elif choice == "6":
            account_number = int(input("Enter your account number: "))
            account = manager.get_account_by_account_number(account_number)
            if account is None:
                print(f"Account {account_number} does not exist.")
            elif manager.verify_pin(account):
                try:
                    withdraw(account)
                    manager.save_accounts()
                except ValueError as e:
                    print(f"Error: {e}")


        elif choice == "7":
            sender_number = int(input("Enter your account number: "))
            sender = manager.get_account_by_account_number(sender_number)
            if sender is None:
                print(f"Account {sender_number} does not exist")
            elif manager.verify_pin(sender):
                receiver_number = int(input("Enter recipient's account number: "))
                receiver = manager.get_account_by_account_number(receiver_number)
                if receiver is None:
                    print(f"Account {receiver_number} does not exist.")

                else:
                    try:
                        transfer(sender,receiver)
                        manager.save_accounts()
                    except ValueError as e:
                        print(f"Error: {e}")


        elif choice == "8":
            account_number = int(input("Enter your account number: "))
            account = manager.get_account_by_account_number(account_number)
            if account is None:
                print(f"Account {account_number} does not exist.")
            elif manager.verify_pin(account):
                check_balance(account)

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalide choice. Please choose a number from 1 to 9.")  


if __name__ == "__main__":
    main()          