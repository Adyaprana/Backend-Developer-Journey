# FizzBuzz
# Rules:
# Divisible by 3 → Fizz
# Divisible by 5 → Buzz
# Divisible by both → FizzBuzz


num = int(input("Enter a number: "))
print("The number you choose is: ",num)
fizz = num%3 == 0
buzz = num%5 == 0
fizzbuzz = num%3 == 0 and num%5 == 0

if fizzbuzz == True:
    print("The number is fizzbuzz")
elif fizz == True:
    print("The number is fizz")
elif buzz == True:
    print("The number is buzz")
else:
    print("Invalid number")

if num%3 == 0 and num%5 == 0:
    print("The number is fizzbuzz")
elif num%3 == 0:
    print("The number is fizz")
elif num%5 == 0:
    print("The number is buzz")
else:
    print("Invalid number")