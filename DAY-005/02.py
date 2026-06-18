# LIST METHODS: 
# append, remove, pop, sort, reverse

# append() --> Add item.
skills = ["python"]
skills.append("sql")
skills.append("web-dev")
skills.append("cloud")
print(skills)

# remove() --> Remove by value.
skills.remove("sql")
print(skills)

# pop() --> Remove by index.
skills.pop(0)
print(skills)
print("------------------------------")

# sort() 
numbers = [90, 80,70,60,50]
print(numbers)
numbers.sort()
print("after sort: ",numbers)

# Descending sort
marks = [30, 80, 65, 98]
print(marks)
marks.sort(reverse=True)
print("After Descending sort: ",marks)

# reverse()
numbers = [1,2,3]
numbers.reverse()
print(numbers)

# len()
names = ["A","B","C"]
print(len(names))

# in Operator
skills = ["Python","SQL"]
print("Python" in skills)

