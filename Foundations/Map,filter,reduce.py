# def cube(x):
#     return x*x*x

# l = [5 , 2 , 3 , 4]

# newl = list(map(cube , l))
# print(newl)

# newl = list(map(lambda x : x*x*x , l))
# print(newl)

# def filter_function(a):
#     return a > 4

# newl = list(map(filter_function , l))
# print(newl)

# newl = list(filter(filter_function , l))
# print(newl)

# from functools import reduce

# num_list = [1 , 2 , 3 , 4 , 5]

# def my_sum(x , y):
#     return x + y

# sum = reduce(my_sum , num_list)
# print(sum)