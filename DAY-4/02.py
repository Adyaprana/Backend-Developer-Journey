# LOOPING THROUGH STRING
name = "Adyaprana"
print("Name is:", name)

for ch in name:
    print(ch)
    name = "Python"
print("-----------------------")

# LOOPING THROUGH LIST

skills = ["Python","SQL","Git"]
print("skills are: ",skills)
for skill in skills:
    print(skill)
print("-----------------------")

# enumerate() --> Provides index and value together.
skills = ["Python","SQL","Git"]
print("skills are: ",skills)
for index, skill in enumerate(skills):
    print(index, skill)