# class person:
#     name = "Aditya"
#     occupation = "Cybersecurity Student"

#     def info(self):
#         print(f"{self.name} is a {self.occupation}")

# a = person()

# a.name = "kanah"
# a.occupation = "Cybersecurity student"

# a.info()

# @Parameterized Constructor

# class person:

#     def __init__(self , name , occupation):
#         self.name = name                                                
#         self.occupation = occupation

#     def info(self):
#         print(f"{self.name} is a {self.occupation}")

# a = person("Aditya" , "Cybersecurity Student")
# print(f"{a.name} is a {a.occupation}")

# b= person("Hrithik" , "Data Science Instructor")
# print(f"{b.name} is a {b.occupation}")

# a.info() 
# b.info()


# @Default Constructor

# class animal:
#     def __init__(self):
#          print("Animals are in the zoo")

# obj = animal()

# class student:
#     def __init__(self , name , section):
#         self.name = name
#         self.section = section

#     def info(self):
#         print(self.name , self.section)

# std1 = student("Aditya" , "D")
# std2 = student("Hrithik" , "D")

# # print(f"{std1.name} is in section {std1.section}")

# std1.name = "Knaha"
# std1.section = "E"
# std1.info()
# std2.info() 