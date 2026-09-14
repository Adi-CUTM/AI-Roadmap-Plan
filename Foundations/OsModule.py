# import os
# import shutil

# print(os.mkdir("TEST"))

# try:
#     print(os.rmdir("TEST"))
# except FileNotFoundError:
#     print("File was not found")
# except OSError:
#     print("The file was not empty")


# try:
#      print(os.mkdir("TEST"))

#      for i in range(1 , 10):
#           os.mkdir(f"TEST/Day {i + 1}")
# except OSError as e:
#      print(f"There was some error {e}")


# try:
#     if os.path.exists("TEST"):
#         print("the file was exist ")
#     else:
#         raise FileExistsError("The file doesnot exist")
# except ValueError as y:
#     print(f"Their was some mistake {y} ")

# try:
#     if not os.path.exists("TEST"):
#         print(os.mkdir("TEST"))
#     else:
#         print("File already exits , Move to the rename concept")

#     for i in range(2, 11):
#         old_path = f"TEST/Day {i}"
#         new_path = f"TEST/NEW {i}"

#         if os.path.exists(old_path):
#             os.rename(old_path, new_path)
#             print(f"file renamed from {old_path} -> {new_path}")
#         else:
#             raise FileNotFoundError(f"Cannot rename {old_path}; file not found")
#         continue

# except OSError as e:
#     print(f" Rename cancelled: {e}")


# folders= os.listdir("TEST")

# for folder in folders:
#     print(os.listdir(f"TEST/{folder}"))


# print(os.getcwd())

# os.chdir("TEST")


# def del_directory():
#     try:
#         if os.path.exists("TEST"):
#             shutil.rmtree("TEST")
#             print("Directory deleted successfully.")

#         elif not os.path.exists("TEST"):
#             raise FileExistsError("Directory is not exists")
        
#     except OSError as e:
#      print(f"Error occurred: {e}")


# del_directory()