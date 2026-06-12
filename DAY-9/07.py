# 10 One-Liner Programs
print("-----------One-Liner-Programs-----------")
# 1. Square Numbers:
print(list(map(lambda x:x*x,[1,2,3,4])))

# 2. Cube Numbers:
print(list(map(lambda x:x**3,[1,2,3,4,5])))

# 3. Uppercase:
print(list(map(str.upper,["python", "go", "home"])))

# 4. Lowercase:
print(list(map(str.lower,{"ADYAPRANA", "IS", "A", "GOOD", "BOY"})))

# 5.Even Numbers:
print(list(map(lambda e: e%2==0, [4,7,8])))

# 6. Odd Numbers:
print(list(map(lambda o: o%2!=0, [3,5,6])))

# 7. Long Words:
print(list(map(lambda c: len(c)>4, ["python", "cloud","os"])))

#8. Sort Length:
print(list(sorted([3,5,2,9,7,1,5,])))

print(list(sorted([3,5,2,9,7,1,5,],reverse=True)))

print(list(sorted(["hii", "adyaprana","time","food"],key=len,)))

print(list(sorted(["hii", "adyaprana","time","food"],key=len,)))

print(sorted(["hii", "adyaprana","time","food"],key=lambda x: x[-1]))

# 9. Combine Lists:
print(list(zip(["adyaprana","hari","ram","shiva"], [23, 34, 45, 56])))

# 10. Create Dictionary:
print(dict(zip(["adyaprana","hari","ram","shiva"], [23, 34, 45, 56])))

