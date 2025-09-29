for i in range(0,5):
    print(i, end=' ')


sum = 0
for i in range(0,5):
    sum = sum + i 
print("Sum is: ", sum)

s = ["John", "Jane", "Doe"]
for i in s:
    print(i)

list1 = ["John", "Jane", "Doe"]
for i, n in enumerate(list1):
    print(i, n) 

d1 = {"Name":"John", "Age":30, "City":"New York"}
for k,v in d1.items():
    print(v)

s = [1,2,3,4,5]
squr = []
for i in s:
    squr.append(i*i)
print(squr)

sentence = ["I am learning pythong for the 2 weeks"]
words = []
for i in sentence:
    words = i.split()
print(words)

evennumbers = [x for x in range(1,21) if x % 2 == 0]
print(evennumbers)

sentence = ["I am Learning Python for the 2 weeks"]
lowercase = [ word.lower() for word in sentence[0].split()]
print(lowercase)


# zip function 
list1 = ["John", "Jane", "Doe"] 
list2 = [25, 30, 35]    
for name, age in zip(list1, list2):
    print(name, age)

sentences =[ "Error: 404 Not Found", 
            "Error: 500 Internal Server Error", 
            "Warning: Disk Space Low",
            "Success: 200 OK"]

Errors = []
NonErrors = []
for s in sentences:
    if s.startswith("Error"):
        Errors.append(s)
    else:
        NonErrors.append(s)
print("Errors: ", Errors)
print("Non Errors: ", NonErrors)

Errors = []
NonErrors = []
for s in sentences:
    if "Error" in s or "Warning" in s:
        Errors.append(s)
    else:
        NonErrors.append(s)

print("Errors: ", Errors)
print("Non Errors: ", NonErrors)

sentence = ["I am Learning Python for the 2 weeks"]
stop_words = ["is", "the", "for", "am", "i"]

words = []
for word in sentence[0].lower().split():
    if word not in stop_words:
        words.append(word)
        joined = " ".join(words)
        
print(words)
print(joined)


#scheduled activity -- Try and exception block can capture the error and failured in the code on system log


# 




    









