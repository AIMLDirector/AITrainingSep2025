a = 10
print("even number") if a % 2 == 0 else print ("odd number")


if a % 2 == 0:
    print("even number")
else:
    print("odd number")


a = 10
b = 5

if a > b:
    print("A is the greatest number")


if a > b:
    print("A is the greatest number")
else:
    print("B is greater than A")

if a > b:
    print("A is the greatest number")
elif b > a :
    print("B is greater than A")
else:
    print("Both A and B are equal ")

# if condition with case condition in group

Cloud = "AWS"
region = "useast-1"

match Cloud:
    case "AWS":
        print("Amazon Web Services")
        if region.startswith("us"):
            print("Deploy the code in US East 1")
        elif region.startswith("eu"):
            print("Deploy the code in EU West 1")


if cloud == "aws" and region == "us-east-1":
    print("Deploy the code in US East 1")
elif cloud == "aws" and region == "eu-west-1":
    print("Deploy the code in EU West 1")  

 # if condition with logical operator and, or, not
cpu = 6
memory = 32

if cpu > 5 and memory > 16 :
    Print(" This is developer machine")
elif  cpu >  10 and memory > 32:
    print(" This is a server basic configuration")
else: 
    print(" This is a basic machine")

if cpu > 5 or memory > 16 :
    Print(" This is developer machine")
elif  cpu >  10 or memory > 32:
    print(" This is a server basic configuration")
else: 
    print(" This is a basic machine")


env = "prod"
cpu = 10
memory = 40

if env =="prod" and (cpu > 5 or memory >16):
    print("This is a production machine")




 

 