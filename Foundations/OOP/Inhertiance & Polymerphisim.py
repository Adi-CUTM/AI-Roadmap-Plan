# Inheritance

# class car:
#     color = "Black"
    
#     @staticmethod
#     def start():
#        return "Car started"
       
#     @staticmethod
#     def stop():
#         return "car stopped"

# class toyota(car):
#     def info(self):
#         print(f"Toyota car which color is {self.color} is {self.start()} and {self.stop()}")

# class Fortuner(toyota):
#     def __init__(self, car_type):
#         self.type = car_type
        
#     def Spec_info(self, new_color):
#      print(f"Toyota car inherited base color is {self.color}. This specific model is a {self.type} car and its custom color is {new_color}.")

# #  You MUST provide the 'type' string when creating a Fortuner object
# car1 = Fortuner("SUV")

# #  Call the function normally
# car1.Spec_info("White")
# car1.info()


#Multiple Inhertiance


# class A:
#     varA = "HII"
# class B:
#     varB = "Hello"
# class C(A , B):
#     varC = "Contains the properties of both A and B "

# c1 = C()
 
# print(c1.varC)
# print(c1.varA)
# print(c1.varB)

# class Students:
#     def __init__(self , college , name):
#         self.college = college
#         self.name = name

#     def greet(self):
#         return f"hii , {self.name}"

# class Student1(Students):
#     def __init__(self, college, name , section):
#         super().__init__(college, name)
#         self.section = section

#     def Student1_info(self , rollno):
#         print(f"{self.greet()} you took admission in {self.college} college and you are assigned to section {self.section} and your roll number is {rollno}")

# college_input = str(input("Enter your College name: ").strip())
# name = str(input("Enter your name: "))
# section = input("Enter your Section: ")
# Rollno = int(input("Enter your roll Number: "))

# std1 = Student1(college_input , name , section)

# std1.Student1_info(Rollno)
