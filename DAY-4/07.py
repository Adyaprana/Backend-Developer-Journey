# Prime Number Checker 
# Only divisible by 1 or itself. ||exp-> 2,3,5,7,11,13

num = int(input("Enter number to check: "))

is_prime = True

for i in range(2, num):

    if num % i == 0:
        is_prime = False
        break
if is_prime:
        print("it's a prime number")
else:
        print("not a prime number")
print("------------------------------------------")

# Print All Primes 1–100

for num in range(2, 101):
    is_prime = True
    for i in range(2, num):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num)
