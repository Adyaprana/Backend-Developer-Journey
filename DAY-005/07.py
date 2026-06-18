# ✅ Create 5 lists
numbers = [34,56,67,89,99]
car = ["bmw","audi","volvo","ford"]
names = ["adyaprana", "shiv", "krishna" ]
cgpa = [9.2, 9.9, 9.9 ]
data = ["java", 3.14, 56, True ]
print("-----------------6----------")


# ✅ Access elements
fruits = ["Apple", "Banana", "Cherry"]
print(fruits)
print(fruits[0])
print(fruits[-1])
print("---------------------------")


# ✅ Practice slicing
fruits = ["Apple", "Banana", "Cherry", "plums", "oranges", "mango"]
print(fruits)
print(fruits[1:4])
print(fruits[:4])
print(fruits[3:])
print(fruits[1:5:2])
print("---------------------------")


# ✅ Use append()
fruits = ["Apple", "Banana", "Cherry"]
print(fruits)
fruits.append("Mango")
print(fruits)
print("---------------------------")


# ✅ Use remove()
fruits = ["Apple", "Banana", "Cherry"]
print(fruits)
fruits.remove("Apple")
print(fruits)
print("---------------------------")


# ✅ Use pop()
fruits = ["Apple", "Banana", "Cherry", "plums", "oranges", "mango"]
print(fruits)
fruits.pop(0)
print(fruits)
fruits.pop(-1)
print(fruits)
print("---------------------------")


# ✅ Reverse list
fruits = ["Apple", "Banana", "Cherry", "plums" ]
print(fruits)
fruits.reverse()
print(fruits)
print("---------------------------")


# ✅ Sort list
number = [3,7,6,9,4,2]
print(number)
number.sort()
print(number)
number.sort(reverse=True)
print(number)
print("---------------------------")


# ✅ Search element
number = [3, 7, 6, 9, 4, 2] 
print("list:", number) 
search = int(input("Enter digit to search: ")) 
for num in number: 
    if num == search: 
        print(f"number {search} is exist in the list.") 
        break 
else: 
    print(f"number {search} is not exist in the list.") 

print("---------------------------")


# ✅ Count vowels in list
alphabets = ["a", "o", "t", "r", "i", "k", "e" ]
count = 0
vowels = "aeiouAEIOU"
print(alphabets)
for ch in alphabets:
    if ch in vowels:
        count += 1
print(count)
print("---------------------------")

# ✅ Todo List App
tasks = []
while True:
    print("\n")
    print("1.Add")
    print("2.Display")
    print("3.Remove")
    print("4.Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter your task: ")
        tasks.append(task)
    elif choice == "2":
        print(tasks)
    elif choice == "3":
        task = input("Enter what you need to removes: ")
        if task in tasks:
            tasks.remove(task)
    elif choice =="4":
        break
print("---------------------------")

# ✅ Max Finder
numbers = [5,8,21,15,3]
largest = numbers[0]
for num in numbers:
    if num > largest:
        largest = num
print(largest)
print("---------------------------")

# ✅ Min Finder
numbers = [5,8,2,15,3]
smallest = numbers[0]
for num in numbers:
    if num < smallest:
        smallest = num
print(smallest)
print("---------------------------")

# ✅ Average Finder
numbers = [5,8,2,15,3]
sum = 0
n = len(numbers)
for num in numbers:
    sum += num
avg = sum/n
print(avg)
print("---------------------------")


# ✅ Create multiplication table list

num = int(input("Enter the number for the multiplication table: "))
multiplication_list = [num * i for i in range(1, 11)]
print(f"\nFormatted Table for {num}:")
for index, value in enumerate(multiplication_list, start=1):
    print(f"{num} x {index} = {value}")
print("---------------------------")


# ✅ List of squares using comprehension
numbers = [2,5,7,9,3]
squares = [num**2 for num in numbers ]
print(squares)


# ✅ Even number generator using comprehension
evens = [i for i in range(20) if i % 2 == 0]
print(evens)