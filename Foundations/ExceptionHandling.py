# localmath/math_tools.py

def options():
    """Prints an interactive menu and lets the user run math programs."""
    while True:
        print("\n==============================")
        print("      === LocalMath Menu ===  ")
        print("==============================")
        print("1. Interactive Calculator")
        print("2. Fibonacci Series Generator")
        print("3. Palindrome Number Checker")
        print("4. Armstrong Number Checker")
        print("5. Factorial Calculator")
        print("6. Even or Odd Checker")
        print("7. Exit")
        print("==============================")
        
        choice = input("Select an option (1-7): ").strip()
        
        if choice == '1':
            _run_calculator()
        elif choice == '2':
            try:
                n = int(input("Enter the number of terms for Fibonacci: "))
                print(f"Fibonacci series up to {n} terms: {fibonacci(n)}")
            except ValueError:
                print("Invalid input! Please enter an integer.")
        elif choice == '3':
            val = input("Enter a number or word to check for Palindrome: ").strip()
            if is_palindrome(val):
                print(f"'{val}' is a Palindrome!")
            else:
                print(f"'{val}' is NOT a Palindrome.")
        elif choice == '4':
            try:
                num = int(input("Enter a number to check for Armstrong: "))
                if is_armstrong(num):
                    print(f"{num} is an Armstrong number!")
                else:
                    print(f"{num} is NOT an Armstrong number.")
            except ValueError:
                print("Invalid input! Please enter an integer.")
        elif choice == '5':
            try:
                num = int(input("Enter a non-negative integer for Factorial: "))
                if num < 0:
                    print("Factorial is not defined for negative numbers.")
                else:
                    print(f"Factorial of {num} is: {factorial(num)}")
            except ValueError:
                print("Invalid input! Please enter an integer.")
        elif choice == '6':
            try:
                num = int(input("Enter an integer to check Even/Odd: "))
                print(f"The number {num} is {is_even_odd(num)}.")
            except ValueError:
                print("Invalid input! Please enter an integer.")
        elif choice == '7':
            print("Exiting LocalMath. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option from 1 to 7.")

def _run_calculator():
    """Internal helper to run an interactive calculator loop."""
    print("\n--- Simple Calculator ---")
    try:
        a = float(input("Enter first number: "))
        op = input("Enter operator (+, -, *, /): ").strip()
        b = float(input("Enter second number: "))
        
        if op == '+':
            print(f"Result: {a} + {b} = {a + b}")
        elif op == '-':
            print(f"Result: {a} - {b} = {a - b}")
        elif op == '*':
            print(f"Result: {a} * {b} = {a * b}")
        elif op == '/':
            if b == 0:
                print("Error: Division by zero is not allowed.")
            else:
                print(f"Result: {a} / {b} = {a / b}")
        else:
            print("Invalid operator selected!")
    except ValueError:
        print("Invalid number input!")

def fibonacci(n):
    """Generates a list containing the Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

def is_palindrome(value):
    """Checks if a string representation of a value reads the same backwards."""
    clean_val = str(value).replace(" ", "").lower()
    return clean_val == clean_val[::-1]

def is_armstrong(number):
    """Checks if a number equals the sum of its own digits raised to the power of the number of digits."""
    num_str = str(number)
    num_digits = len(num_str)
    total_sum = sum(int(digit) ** num_digits for digit in num_str)
    return total_sum == number

def factorial(n):
    """Calculates the factorial of an integer n iteratively."""
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def is_even_odd(number):
    """Returns 'Even' or 'Odd' string based on the integer properties."""
    return "Even" if number % 2 == 0 else "Odd"
