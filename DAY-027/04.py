# THEORY 4 — SHALLOW COPY VS DEEP COPY

# Suppose:
import copy
original = [
    [1,2],
    [3,4]
]

# Shallow Copy:
import copy
original = [
    [1,2],
    [3,4]
]
new = copy.copy(original)
new[0][0] = 99
print(original)
# Output: [[99,2],[3,4]] --> Nested list changed.




# Deep Copy:
import copy
original = [
    [1,2],
    [3,4]
]
new = copy.deepcopy(original)
new[0][0] = 99
print(original)
# Output: [[1,2],[3,4]] --> Original stays safe.

# Easy Way:
# Shallow Copy: Photocopy of cover page
# Deep Copy: Complete photocopy of every page