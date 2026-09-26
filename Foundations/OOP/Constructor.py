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
#     college = "CUTM"

#     def __init__(self , name , section , marks):
#         self.name = name
#         self.section = section
#         self.marks = marks

#     def info(self):
#         print(self.name , self.section)

#     def get_marks(self):
#         return f"{self.name} is in the {self.college} and secured {self.marks}"

# std1 = student("Aditya" , "D" , 88)
# print(f"{std1.name} is in {std1.college} and secured {std1.marks}")
# print(f"{std1.name} is in section {std1.section}")

# std2 = student("Hrithik" , "D" , 89)
# print(f"{std2.name} is in {std2.college} and secured {std2.marks}")
# # print(f"{std2.name} is in section {std2.section}")


# std1.name = "Knaha"
# std1.section = "E"
# std1.info()
# std2.info() 

# print(std1.get_marks())
# print(std2.get_marks())


# PRACTICE QUESTION # # PRACTICE QUESTION #  # PRACTICE QUESTION #   # PRACTICE QUESTION #    # PRACTICE QUESTION #     # PRACTICE QUESTION #

#question = "Create student class that takes names & marks of 3 subjects as arguments in constructor. Then create a method to print the avergate"

# class studnet:
#     college = "CUTM"
#     def __init__(self , name , math_mark , eng_mark , hindi_mark):
#         self.fullname = name
#         self.math = math_mark
#         self.english = eng_mark
#         self.hindi = hindi_mark

#     def average(self):
#         avg = self.math + self.english + self.hindi / 3
#         return f"{avg:.2f}"
    
#     def info(self):
#         print(f"{self.fullname} who is in {self.college} has secured average mark {self.average()}")

# student_1 = studnet("Rudra Prasad Baral" , 88 , 95 , 98)
# # print(f"{student_1.fullname}'s average mark is {student_1.average()}")
# student_1.info() 

