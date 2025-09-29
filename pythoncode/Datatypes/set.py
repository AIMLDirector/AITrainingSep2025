# set is mutable(changeable) and it main no index value
# set can have  integers, strings, boolean, float, complex numbers
s1 = {1,2,3,3,4,5,7}  # no index value
s2 = {2, 1.5, 3j, "hello", True}
s3 ={"honey", "fruits", "vegetables"}
print(s3)
s3.add("grains")
print(s3)
s3.remove("fruits")
print(s3)
s3.clear()
print(s3)