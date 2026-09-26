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

# num1 = int(input("enter first number: "))
# num2 = int(input("enter second number: "))
# print(isgreater(num1 , num2))

# while num1 != 0 or num2 != 0:
    
#     num1 = int(input("enter first number: "))
#     num2 = int(input("enter second number: "))

# def calculate(a , b):
#     print(f"the addition is {a + b}")

# calculate(a = 5 , b = 6)


####################################################### Calculator Using Function ######################################################################



# print("Welcome To The Calculator Program Using Function \n".strip())

# def header(menu):
#     menu = ["1. Add", "2. Subtract", "3. Multiply", "4. Divide", "5. Exit"]
#     return menu

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

# while True:
#     try:
#         print("\nPlease Choose an Operation From Below:")
#         for option in header(menu=None):
#             print(option)
                
#         choice = input("Enter your choice: ").strip()
        
#         if choice == "5":
#             print("Exiting the Calculator Program. Goodbye!")
#             break
                    
#         if choice in ["1", "2", "3", "4"]:
#             num1 = float(input("Enter the first number: "))
#             num2 = float(input("Enter the second number: "))
            
#             if choice == "1":
#                 print(f"Addition of {num1} + {num2} is {addition(num1, num2)}")
#             elif choice == "2":
#                 print(f"Subtraction of {num1} - {num2} is {substraction(num1, num2)}")
#             elif choice == "3":
#                 print(f"Multiplication of {num1} * {num2} is {multiplication(num1, num2)}")
#             elif choice == "4":
#                 print(f"Division of {num1} / {num2} is {divison(num1, num2)}")
#         else:
#             ("Invalid choice! Please choose a valid option from the menu.")
            
#     except ValueError as e:
#         print("Invalid input! Please enter numbers only.", e)


    

   ####################################################### // ######################################################################

# def name(fname , mname , lname):                                          # Throws Error bcz required arugement is needed 
#     print("hello " , fname , mname , lname)
                                                                
# name("kanha" , "Aditya")



# def average(*numbers):
    
#    result = sum(numbers) / len(numbers)

#    print(f"the result is : {result}")

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


# def factorial(num):
    
#     fact = 1
#     for i in range(1 , num+1):
#         fact*=i
#     return (f"the factorial of {num} is {fact}")

# number = int(input("enter a number to check: "))
# print(factorial(number))


# def square(*num):
#     result = []
#     for i in range(len(num)):
#       result.append(num[i] * num[i])
#     return result

# print(square(1 ,2 ,3 , 4))

# def info(name):
#     if name == "Aditya Srichandan":
#         personalinfo1 = {
#             "Dob": "08-01-2005",
#             "Name": "Aditya Srichandan",
#             "Village": "Kanaphasia",
#             "AADHAR NO": "UGXPS5779f",
#             "PAN NO": "75558548448"
#         }
#         return personalinfo1
    
#     elif name == "Kanha Srichandan":  
#         personalinfo2 = {
#             "Dob": "08-01-2005",
#             "Name": "Kanha Srichandan",  
#             "Village": "Kanaphasia",
#             "AADHAR NO": "UGXPS5779f",
#             "PAN NO": "75558548448"
#         }
#         return personalinfo2
#     else:
        
#        print( "Please enter your correct name")

# name = str(input("Enter your name: "))
# print(info(name))