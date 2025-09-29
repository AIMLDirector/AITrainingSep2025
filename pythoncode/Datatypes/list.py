# list we can able to add , append, delete, modify the values
# list is mutable data types( changeable) and it main index value 
# list can have  integers, strings, boolean, float, complex numbers
l1 = [1,2,3,3,4,5,7]  # 0 index, 1 index, 2 index, 3 index, 4 index, 5 index, 6 index
l2 = [2, 1.5, 3j, "hello", True]

print(l1[0]) # 1
print(l1[-1])  # 7
print(l1[2:5]) # index( 2,3,4)  value ( 3,3,4)
print(l1)
l1.append(8)
print(l1)
l1.insert(2,"welcome")
print(l1)
l1.remove("welcome")
print(l1)
l1 = set(l1) # no index value 
print(l1)
l1 = list(l1)
print(l1)
l1.sort(reverse=True)
print(l1)
# l1.clear()
print(l1)
l3 = l1 +l2
print(l3)

for i in l2:
    l1.append(i)
print(l1)

l4 =[]
for i in l1:
    if i !=3:
        l4.append(i)
print(l4)
