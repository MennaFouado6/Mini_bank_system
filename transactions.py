def deposit(account): 
  received_amount = float(input("Enter amount of money: "))
  if received_amount <= 0:
    raise ValueError("Invalid amount. Please try again.")
  else:
    account.balance += received_amount

    transaction = {
        "type": "deposit",
        "amount": received_amount,
        "balance_after": account.balance
    }
    account.transactions.append(transaction)
    print("Deposit completed successfully!")
    print(f"Balance: {account.balance} ")
    return account.balance
    


def withdraw(account): 
  withdrew_amount = float(input("Enter amount of money: "))
  if withdrew_amount <= 0:
    raise ValueError("Invalid amount. Please try again.")
  elif withdrew_amount > account.balance:
    raise ValueError("Insufficient funds")
  else:
    print("Withdrawal completed successfully!")
    account.balance -= withdrew_amount

    transaction = {
        "type": "withdrawal",
        "amount": withdrew_amount,
        "balance_after": account.balance
    }

    account.transactions.append(transaction)

    print(f"Balance: {account.balance}")
    return account.balance
    
def transfer(sender_account, receiver_account):
  transferred_amount = float(input("Enter amount of money: "))
  if transferred_amount <= 0:
    raise ValueError("Invalid amount. Please try again")
  elif transferred_amount > sender_account.balance:
    raise ValueError("Insufficient funds")
  elif sender_account.account_number == receiver_account.account_number:
    raise ValueError("Cannot transfer to the same account")
  else:
    sender_account.balance -= transferred_amount
    receiver_account.balance += transferred_amount

  sender_transaction = {
    "type": "transfer",
    "amount": transferred_amount,
    "to": receiver_account.account_number,
    "balance_after": sender_account.balance
  } 

  sender_account.transactions.append(sender_transaction) 

  receiver_transaction = {
    "type": "received",
    "amount": transferred_amount,
    "from": sender_account.account_number,
    "balance_after": receiver_account.balance
  } 

  receiver_account.transactions.append(receiver_transaction)

  print("Transfer completed successfully!")
  print(f"Balance: {sender_account.balance}")
  return sender_account.balance, receiver_account.balance

def check_balance(account):
  print(f"Balance: {account.balance}")
  return account.balance