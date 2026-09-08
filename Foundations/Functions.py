# def addition(num1 , num2):

#     calculate = num1 + num2

#     return calculate

# num1 = int(input("enter first number: "))
# num2 = int(input("enter second number: "))

# print(f"the result of {num1} + {num2} is {addition(num1, num2)}")


# def truecheck(value , num):
#     if value == num:
#         return True
#     else:
#         return False
    
# value = int(input("enter a number: "))
# num = int(input("enter a number to check: "))

# print(f"the result of {value} == {num} is {truecheck(value, num)}")


# def isgreater(a , b):
#     if a > b:
#         return (f"{a} is greater than {b}")
#     elif b > a:
#         return (f"{b} is greater than {a}")
#     else:
#         return (f"{a} and {b} are equal")

# a = int(input("enter first number: "))
# b = int(input("enter second number: "))
# print(isgreater(a, b))

# while a != 0 or b != 0:
    
#     a = int(input("enter first number: "))
#     b = int(input("enter second number: "))

# def calculate(a=8 , b = 8):
#     print(f"the addition is {a + b}")

# calculate()


####################################################### Calculator Using Function ######################################################################



# print("Welcome To The Calculator Program Using Function \n".strip())

# print("Please Choose an Operation From Below\n")

# def header():
#     menu = ["1. Add", "2. Subtract", "3. Multiply", "4. Divide", "5. Exit"]
#     return menu

# for option in header():
#      print(option)


# choice =str(input("Enter you choice:"))

# num1 = int(input("Enter the first number: "))
# num2 = int(input("Enter the second number: "))

# def addition(num1 , num2):
#     return num1 + num2
# def substraction(num1 , num2):
#     return num1 - num2
# def multiplication(num1 , num2):
#     return num1 * num2
# def divison(num1 , num2):
#     if num2 == 0:
#         print("0 is not allowed , Please enter another number")
#     else:
#         return num1 / num2

# while choice !="5":
#     if choice == "1":
#         print(f"addition of {num1} + {num2} is {addition(num1 , num2)}")
#     elif choice == "2":
#         print(f"subtraction of {num1} - {num2} is {substraction(num1 , num2)}")
#     elif choice == "3":
#         print(f"multiplication of {num1} * {num2} is {multiplication(num1 , num2)}")
#     elif choice  == "4":
#         print(f"division of {num1} / {num2} is {divison(num1 , num2)}")
#     else:
#         print("Choose a valid option from menu\n")

#     for option in header():
#      print(option)
#     choice = str(input("Enter you choice: "))

   ####################################################### // ######################################################################

# def name(fname , mname , lname):                                          # Throws Error bcz required arugement is needed 
#     print("hello " , fname , mname , lname)
                                                                
# name("kanha" , "Aditya")



# def average(*numbers):
    
#     for i in numbers:
#      result = sum(numbers) / len(numbers)

#     print(f"the result is : {result}")

# average(5 ,6 ,7 ,8)


# def names(**names):
#     print(type(names))
#     print(f"Hello {names['fname']} {names['mname']} {names['lname']}")

# names(fname = "kanha" , mname = "Aditya" , lname = "Singh")

# def name(fname , mname , lname):                                          
#     return f"hello , {fname} {mname} {lname}"

# print(name("kanha" , "Aditya" , "Singh"))


# def sum_range(*args):                                                     # args are tuple

#     result = sum(args)
#     return result

# print(sum_range(1 , 2 , 3))


# def job_role(**kwargs):                                                   # kwargs are dict

#     for key, value in kwargs.items():
#         print(f"{key}:{value}")

# job_role(name="Alice", age=30, job="Engineer")


# def factorial():
#     num = int(input("enter a number"))
#     fact = 1
#     for i in range( 1 , num + 1):
#         fact = fact * i
#     return fact

# print(factorial())


# def factorial():
#     num = int(input("enter the number: ").strip())
#     fact = 1
#     for i in range(1 , num+1):
#         fact*=i
#     print(f"the factorial of {num} is {fact}")

# factorial()


