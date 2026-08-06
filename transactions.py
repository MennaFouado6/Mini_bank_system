#Deposit money into an account (core logic - no input)
def deposit(account, amount):
    if amount <= 0:
        raise ValueError("Invalid amount. Please try again.")

    account.balance += amount

    transaction = {
        "type": "deposit",
        "amount": amount,
        "balance_after": account.balance
    }
    account.transactions.append(transaction)
    return account.balance


def deposit_interactive(account):
    amount = float(input("Enter amount of money: "))
    new_balance = deposit(account, amount)
    print("Deposit completed successfully!")
    print(f"Balance: {new_balance}")
    return new_balance


#Withdraw money from an account (core logic - no input)
def withdraw(account, amount):
    if amount <= 0:
        raise ValueError("Invalid amount. Please try again.")
    if amount > account.balance:
        raise ValueError("Insufficient funds")

    account.balance -= amount

    transaction = {
        "type": "withdrawal",
        "amount": amount,
        "balance_after": account.balance
    }
    account.transactions.append(transaction)
    return account.balance


def withdraw_interactive(account):
    amount = float(input("Enter amount of money: "))
    new_balance = withdraw(account, amount)
    print("Withdrawal completed successfully!")
    print(f"Balance: {new_balance}")
    return new_balance


#Transfer money between two accounts (core logic - no input)
def transfer(sender_account, receiver_account, amount):
    if amount <= 0:
        raise ValueError("Invalid amount. Please try again")
    if sender_account.account_number == receiver_account.account_number:
        raise ValueError("Cannot transfer to the same account")
    if amount > sender_account.balance:
        raise ValueError("Insufficient funds")

    sender_account.balance -= amount
    receiver_account.balance += amount

    sender_account.transactions.append({
        "type": "transfer",
        "amount": amount,
        "to": receiver_account.account_number,
        "balance_after": sender_account.balance
    })

    receiver_account.transactions.append({
        "type": "received",
        "amount": amount,
        "from": sender_account.account_number,
        "balance_after": receiver_account.balance
    })

    return sender_account.balance, receiver_account.balance


def transfer_interactive(sender_account, receiver_account):
    amount = float(input("Enter amount of money: "))
    sender_balance, receiver_balance = transfer(sender_account, receiver_account, amount)
    print("Transfer completed successfully!")
    print(f"Balance: {sender_balance}")
    return sender_balance, receiver_balance


def check_balance(account):
    print(f"Balance: {account.balance}")
    return account.balance