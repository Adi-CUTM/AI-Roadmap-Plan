# Abstraction #

# class car:
#     def __init__(self):
#         self.acc = False
#         self.brk = False
#         self.clutch = False

#     def start(self):
#         self.acc = True
#         self.clutch = True
#         print("car is started")

# car1 = car()
# car1.start() # Only showing the part that we wants to show to the users but hide the internal development part 


# Encapsulation : - Wrapping data and functions to a single unit (object) #

# PRACTICE QUESTION # # PRACTICE QUESTION #  # PRACTICE QUESTION #   # PRACTICE QUESTION #    # PRACTICE QUESTION #     # PRACTICE QUESTION #

# Question: - Create a Account class with 2 attibutes - balance & account no . Create methods for debit , credit , & printing the balance

# class Account:
#     def __init__(self , balance , accountno , name):
#         self.mybalance = balance
#         self.AcountNumber = accountno
#         self.PersonName = name
#     def greet(self):
#         print(f"Hello, Dear {self.PersonName}")

#     def debit(self , amount):
#         self.mybalance -= amount
#         print(f"Dear {self.PersonName}, Rs.{amount} is debited! ")

#     def credit(self , amount):
#         self.mybalance+=amount
#         print(f"Dear {self.PersonName}, Rs.{amount} is credited! ")

#     def Balance_Info(self):
#         print(f"Dear {self.PersonName}, Your account no is {self.AcountNumber} and your Balance is : {self.mybalance}")


# name_input = input("Enter Account Holder Name: ")
# balance_input = int(input("Enter Initial Balance (Rs.): "))
# acc_no_input = int(input("Enter Account Number: ")) 

# person1 = Account(balance_input, acc_no_input, name_input)
# person1.greet()

# def banking_option():
#         menu = ["1. Deposit" , "2. Withdraw" , "3. Exit"]
#         return menu


# while True:
#     print("\nPlease Choose an Operation From Below:")
#     for option in banking_option():
#          print(option)
#     choice = str(input("Enter your choice You have to perform : "))

#     if choice == "1":
#          credit_amount = int(input("\nEnter amount to credit: "))
#          person1.credit(credit_amount)
#          person1.Balance_Info()
#     elif choice == "2":
         
#          debit_amount = int(input("\nEnter amount to debit: "))
#          person1.debit(debit_amount)
#          person1.Balance_Info()
#     elif choice == "3":
#           print("Exiting the Calculator Program. Goodbye!")
#           break
#     elif choice not in ["1" , "2" , "3"]:
#          raise ValueError("Invalid input! Please enter numbers only.")
    

 
