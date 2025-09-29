# tuples will have index , we cannot modify, add, delete the values
# tuples is immutable data types ( unchangeable)
# tuples can have integers, strings, boolean, float, complex numbers
# tuples to do any data validation 

t1 = (1,3,3,4,5,"hello", True, 2.5, 3j) # 0 index, 1 index, 2 index, 3 index, 4 index, 5 index, 6 index, 7 index, 8 index
print(t1[:4])  # index( 0,1,2,3)
print(t1)
print(t1[4])

t2 = list(t1)
t2.append("welcome")
t1 = tuple(t2)
print(t1)

