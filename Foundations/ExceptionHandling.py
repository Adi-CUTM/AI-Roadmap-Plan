# try:
#     a = int(input("Enter a number: ").strip())
#     print(f"The multiplication table for {a} is: \n")

#     for i in range(1 , 11):
#         print(f"{a} x {i} = {a*i}")
# except ValueError:
#     print("number you entered is not an integer ")

# try:
#     a = [6 , 4 , 5]

#     print(a.index(1))
# except ValueError as e:
#     print(f"value is not found {e}")

# except ValueError:
#     print("value is not specified")
# except IndexError:
#     print("index Error")

# a = int(input("Enter a number between 5 to 9: ").strip())

# if (a <5 or a > 9):
#     raise ValueError("Value shuold be between 5 and 9 ")

# a = set(input("Write quit here: ").strip().split(","))

# if "quit" in a :
#     print(True)
# else:
#     raise ValueError("Write quit only")