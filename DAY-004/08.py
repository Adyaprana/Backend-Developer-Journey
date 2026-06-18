# PASS Statement (Used when code is not ready.)

# if True:
#     pass


# ELSE WITH LOOP
for i in range(5):
    print(i)

else:
    print("Loop Finished")


# LOOP COUNTERS
word = "python"
count = 0
for ch in word:
    if ch in "aeiou":
        count += 1
print(count)