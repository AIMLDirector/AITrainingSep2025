# repeated code or repeated task we can use function in python 

def func():
    pass

func()

def func1(name="kumar"):
    print(name)

func1()



def func2(*args): # n of arguments( variables)
    l1 = list(args)
    count= len(l1)
    print(count)
    print(l1) 
    for i in l1:
        if i == "sample":
            print("found sample")

   

func2("test", "sample", "demo","sample1")

def func3(name: str) -> str:
    return f"Hello  + {name}"

print(func3("kumar"))

print(func3(20))

def func4(name):
    if not isinstance(name, str):
        raise TypeError("Input must be a string")
    return f"Hello  + {name}"

print(func4("kumar"))


