def deposit(account, balance): 
  received_amount = int(input("Enter amount of money: "))
  if received_amount <= 0:
    raise ValueError("Invalid amount. Please try again.")
  else:
    print("Operation is successful!")
    balance += received_amount
    print(f"Balance: {balance} ")
    return balance
    


def withdraw(account, balance): 
  withdrew_amount = int(input("Enter amount of money: "))
  if withdrew_amount <= 0:
    raise ValueError("Invalid amount. Please try again.")
  elif withdrew_amount > balance:
    raise ValueError("Insufficient funds")
  else:
    print("Operation is successful!")
    balance -= withdrew_amount
    print(f"Balance: {balance}")
    return balance
    
#transfer()

def check_balance(account, balance):
  print(f"Balance: {balance}")

#exceptions:
# invalid amount
# insufficient funds