# my_string = " "

# print(f"hello world{my_string}")



# n = int(input("Enter a number: "))

# for i in range(1, n + 1):
#     print(int(i * i))


# n = int(input("Enter a number: "))

# for i in range(1, n + 1):
#     print(str(i), end="")


# Calculator Program # 

print("Welcome to the calculator program! \n")

Menu = ["1. Add", "2. Subtract", "3. Multiply", "4. Divide", "5. Exit"]

print("Please select an operation from the menu below: \n")
for option in Menu:
    print(option)

choice = str(input("Please Select an Operation : \n"))

while choice != "5":

    if choice == "1":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = num1 + num2
        print(f"The result of {num1} + {num2} is: {result}\n")

    elif choice == "2":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = num1 - num2
        print(f"The result of {num1} - {num2} is: {result}\n")

    elif choice == "3":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = num1 * num2
        print(f"The result of {num1} * {num2} is: {result}\n")

    elif choice == "4":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        if num2 != 0:
            result = num1 / num2
            print(f"The result of {num1} / {num2} is: {result}\n")
        else:
            print("Error: Division by zero is not allowed.\n")

    else:
        print("Invalid choice. Please select a valid operation from the menu.\n")

    choice = str(input("Please Select an Operation : \n"))

    

else:
    print("Exiting the calculator program. Goodbye!")  

    