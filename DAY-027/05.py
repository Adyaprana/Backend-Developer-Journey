# THEORY 5 — *args
# Accept unlimited positional arguments.

def total(*numbers):
    print(numbers)
total(10, 20, 30)
# Output: (10,20,30)


# Better Example:
def total(*numbers):
    result = 0
    for num in numbers:
        result += num
    return result
print(total(10, 20, 30))
# Output: 60





# THEORY 6 — **kwargs
# Unlimited keyword arguments.

def student(**info):
    print(info)
student(
    name="Adyaprana",
    age=23
)
# Output
# {
# 'name':'Adyaprana',
# 'age':23
# }