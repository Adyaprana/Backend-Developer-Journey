# THEORY 1 — WHAT IS SYNCHRONOUS CODE?

# Think: You go to a restaurant -> Order food -> Wait -> Food arrives -> Then order dessert -> Wait -> Then pay.
# Everything happens one after another, This is synchronous execution.

# Python:
import time

print("Task 1 Started")
time.sleep(3)
print("Task 1 Finished")

print("Task 2 Started")
time.sleep(3)
print("Task 2 Finished")

# Output:
# Task 1 Started
# (wait 3 sec)
# Task 1 Finished

# Task 2 Started
# (wait 3 sec)
# Task 2 Finished

# Total: 6 seconds