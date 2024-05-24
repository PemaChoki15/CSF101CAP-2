####################################################
# Pema Choki
# 1 Electrical
# 02230068
####################################################
# REFERENCES
# https://github.com/shawkyebrahim2514/Banking-System-Application
# https://www.geeksforgeeks.org/python-program-to-create-bankaccount-class-with-deposit-withdraw-function/

import random # Importing the random momdule

ACCOUNTS_FILE = 'accounts.txt' # Create a file name accounts.txt


class Account:     # Define a class named solution
    def __init__(self, account_number, password, account_type, balance=0.0):
        self.account_number = account_number # Initialize an account number
        self.password = password             # Initialize a default password for the account
        self.account_type = account_type     # Initialize the account type
        self.balance = balance               # Initialize the balance of the account

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount           # Add the deposited amount and the initial balance
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Unable to Deposit.")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:        # Withdraw can be possible only if the withdrwa amount is less than the initial balance
                self.balance -= amount        # Subtract the initial balance by the withdrawn amount
                print(f"Withdrew {amount}. New balance: {self.balance}")
            else:
                print("Insufficient funds.")   # Cancel the withdraw if the account has insufficient balance
        else:
            print("Unable to Withdraw.")

    def __str__(self):
        return f"{self.account_number},{self.password},{self.account_type},{self.balance}"


class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, 'business', balance)    # Create a business type account


class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, 'personal', balance)     # Create a personal type account


class Bank:
    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = {}           # Initialize an empty dictionary
        with open(ACCOUNTS_FILE, 'r') as f:
            for line in f:
                account_number, password, account_type, balance = line.strip().split(',')
                balance = float(balance)
                if account_type == 'business':
                    account = BusinessAccount(account_number, password, balance)
                else:
                    account = PersonalAccount(account_number, password, balance)        # Store the account informations in the file
                accounts[account_number] = account
        return accounts

    def save_accounts(self):
        with open(ACCOUNTS_FILE, 'w') as f:
            for account in self.accounts.values():
                f.write(str(account) + '\n')           # Save the account created

    def create_account(self, account_type):
        account_number = str(random.randint(100000000, 999999999))    # Create an account 
        password = account_number[-4:]  # Default password
        if account_type == 'business':
            account = BusinessAccount(account_number, password)        
        else:
            account = PersonalAccount(account_number, password)
        self.accounts[account_number] = account
        self.save_accounts()
        print(f"Account created. Account number: {account_number}, Password: {password}")         # Create a personal or business account

    def login(self, account_number, password):
        account = self.accounts.get(account_number)          # Login into the account
        if account and account.password == password:
            return account
        else:
            print("Invalid account number or password.")      # Message printed for invalid account number or password
            return None                                       # If the Acoount type is unknown then return none

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]              # Account is removed from the dictionary
            self.save_accounts()
            print(f"Account {account_number} deleted.")    # Acount is deleted sucessfully
        else:
            print("Account not found.")                    # Else print it if the account does not exits

    def transfer_money(self, from_account, to_account_number, amount):
        to_account = self.accounts.get(to_account_number)                # Send money to other account number
        if not to_account:
            print("Receiving account not found.")                        # Print it if the receiving account is not found
            return
        if from_account.balance >= amount:                               # Sending money is only possible if the amount is less the balance                              
            from_account.balance -= amount                               # Subract the amount send and the balance
            to_account.balance += amount
            self.save_accounts()
            print(f"Transferred {amount} to account {to_account_number}. New balance: {from_account.balance}")
        else:
            print("Insufficient funds.")                                  # Print it if the account has is insufficient fund

def main():
    bank = Bank()         # Initialize an bank object
    while True:
        print("\nWelcome To the Bank!")
        print("\n1. Open Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")       # Choose your choice

        if choice == '1':
            account_type = input("Enter account type (Personal/Business): ")
            if account_type in ['Personal', 'Business']:            # Create an account
                bank.create_account(account_type)
            else:
                print("Invalid account type.")
        elif choice == '2':
            account_number = input("Enter account your number: ")       # Log into your account
            password = input("Enter password: ")
            account = bank.login(account_number, password)
            if account:
                while True:
                    print("\n1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transfer Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    choice = input("Enter your choice: ")

                    if choice == '1':
                        print(f"Balance: {account.balance}")      # Check the balance of your account
                    elif choice == '2':
                        amount = float(input("Enter amount to deposit: "))     # Deposit money to your account
                        account.deposit(amount)
                        bank.save_accounts()
                    elif choice == '3':
                        amount = float(input("Enter amount to withdraw: "))     # Withdraw money from your account
                        account.withdraw(amount)
                        bank.save_accounts()
                    elif choice == '4':
                        to_account_number = input("Enter account number to transfer to: ")         # Send money to other account from your account
                        amount = float(input("Enter amount to transfer: "))
                        bank.transfer_money(account, to_account_number, amount)
                    elif choice == '5':
                        confirm = input("Are you sure you want to delete your account? (yes/no): ")    # Delete your account if not required
                        if confirm == 'yes':
                            bank.delete_account(account.account_number)
                            break
                    elif choice == '6':             # Log out sucessfully
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            print("Exiting...")                 # Exit after finishing everything
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()