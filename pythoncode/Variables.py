# Two types are variables  1. local variable 2 global variable 
x = 10  # global variable
y = "welcome to python" 
a = 1.5  # global variable

def my_function():
    z = 30  # local variable
    print("Inside the function:")
    print("x =", x)  # Accessing global variable
    print("y =", y)  # Accessing global variable
    print("z =", z)  # Accessing local variable

my_function()
   
print(type(x))
print(type(y))
print(type(a))


