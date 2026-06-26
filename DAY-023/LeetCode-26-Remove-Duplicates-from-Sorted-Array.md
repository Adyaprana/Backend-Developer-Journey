# Day 21 - LeetCode #26: Remove Duplicates from Sorted Array

# Overview

Today I solved **LeetCode #26 - Remove Duplicates from Sorted Array**.

This problem introduced me to the **Read Pointer + Write Pointer** pattern, one of the most important Two Pointer techniques used in coding interviews.

The challenge is not just finding duplicates, but removing them **in-place** without creating another array.

---

# Problem Statement

Given an integer array `nums` sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once.

Return the number of unique elements `k`.

The first `k` elements of `nums` should contain the unique elements.

---

# Example 1

Input:

```python
nums = [1,1,2]
```

Output:

```python
2
```

Modified Array:

```python
[1,2,_]
```

Explanation:

Unique values:

```text
1
2
```

Count:

```text
2
```

---

# Example 2

Input:

```python
nums = [0,0,1,1,1,2,2,3,3,4]
```

Output:

```python
5
```

Modified Array:

```python
[0,1,2,3,4,_,_,_,_,_]
```

Explanation:

Unique values:

```text
0
1
2
3
4
```

Count:

```text
5
```

---

# Constraints

```text
1 <= nums.length <= 3 * 10⁴
-100 <= nums[i] <= 100
nums is sorted in non-decreasing order
```

---

# Understanding the Problem

Many beginners misunderstand this problem.

The goal is NOT:

```python
return [0,1,2,3,4]
```

The goal is:

```python
Modify nums itself
```

and return:

```python
5
```

for:

```python
[0,0,1,1,1,2,2,3,3,4]
```

---

# Why Sorted Array Matters

Because duplicates are always adjacent.

Example:

```python
[0,0,1,1,1,2,2,3,3,4]
```

Duplicates:

```text
0 0
1 1 1
2 2
3 3
```

Since duplicates are next to each other, we only need to compare:

```python
nums[i]
```

with:

```python
nums[i-1]
```

---

# Approach 1: Extra Array (Not Accepted)

## Thought Process

My first idea was:

```text
Find unique values
Store them in another array
```

Example:

```python
nums = [0,0,1,1,1,2,2,3,3,4]
```

Result:

```python
[0,1,2,3,4]
```

---

# Code

```python
def removeDuplicates(nums):

    unique = []

    for i in range(len(nums)-1):

        if nums[i] != nums[i+1]:
            unique.append(nums[i])

    unique.append(nums[-1])

    return unique
```

---

# Why This Is Rejected

LeetCode requires:

```text
In-place modification
```

But this approach creates:

```python
unique = []
```

which uses extra memory.

---

# Complexity

Time Complexity:

```text
O(n)
```

Space Complexity:

```text
O(n)
```

---

# Approach 2: Two Pointers (Optimal)

## Key Idea

Use:

```text
Read Pointer
Write Pointer
```

---

### Read Pointer

Searches for new unique values.

---

### Write Pointer

Stores unique values in the correct position.

---

# Visualization

Input:

```python
[0,0,1,1,1,2,2,3,3,4]
```

Initially:

```text
W
R
0 0 1 1 1 2 2 3 3 4
```

---

When Read Pointer finds:

```text
1
```

which is different from:

```text
0
```

Store:

```text
1
```

at Write Pointer position.

---

Array becomes:

```text
0 1 1 1 1 2 2 3 3 4
```

Move Write Pointer.

---

Continue until end.

---

Final:

```text
0 1 2 3 4 ...
```

---

# Optimal Solution

```python
class Solution(object):

    def removeDuplicates(self, nums):

        if not nums:
            return 0

        write = 1

        for read in range(1, len(nums)):

            if nums[read] != nums[read - 1]:

                nums[write] = nums[read]

                write += 1

        return write
```

---

# Dry Run

Input:

```python
nums = [1,1,2]
```

---

Initial:

```python
write = 1
```

Array:

```text
1 1 2
```

---

Read = 1

Compare:

```python
nums[1]
```

with:

```python
nums[0]
```

Result:

```text
1 == 1
```

Duplicate.

Skip.

---

Read = 2

Compare:

```python
nums[2]
```

with:

```python
nums[1]
```

Result:

```text
2 != 1
```

Unique.

Store:

```python
nums[1] = nums[2]
```

Array becomes:

```text
1 2 _
```

Move:

```python
write += 1
```

Now:

```python
write = 2
```

Return:

```python
2
```

---

# Dry Run (Large Example)

Input:

```python
[0,0,1,1,1,2,2,3,3,4]
```

Unique values found:

```text
0
1
2
3
4
```

Stored at:

```text
Index:
0
1
2
3
4
```

Final:

```python
[0,1,2,3,4,2,2,3,3,4]
```

Return:

```python
5
```

Only the first 5 positions matter.

---

# Why It Works

Because the array is sorted.

Whenever:

```python
nums[read] != nums[read - 1]
```

we know:

```text
A new unique value has been found.
```

Store it at:

```python
nums[write]
```

and move:

```python
write += 1
```

---

# Complexity Analysis

## Time Complexity

```text
O(n)
```

Every element is visited once.

---

## Space Complexity

```text
O(1)
```

Only:

```python
read
write
```

variables are used.

No extra array is created.

---

# Comparison of Approaches

| Approach     | Time | Space |
| ------------ | ---- | ----- |
| Extra Array  | O(n) | O(n)  |
| Two Pointers | O(n) | O(1)  |

---

# Interview Pattern Learned

This problem teaches:

```text
Read Pointer + Write Pointer
```

Pattern.

The same pattern appears in:

* LeetCode #27 Remove Element
* LeetCode #283 Move Zeroes
* LeetCode #75 Sort Colors
* LeetCode #88 Merge Sorted Array

---

# Concepts Learned

* Sorted Array Property
* In-place Modification
* Two Pointers
* Read Pointer
* Write Pointer
* Array Overwriting
* Time Complexity Analysis
* Space Complexity Analysis

---

# Results

Problem Solved:

**LeetCode #26 - Remove Duplicates from Sorted Array**

Approaches Learned:

* Extra Array Approach ✅
* Two Pointer Approach ✅

Status:

* Accepted on LeetCode ✅
* Passed All Test Cases ✅

---

# Reflection

The biggest lesson from this problem was:

> Finding unique values is easy. Storing them in the original array without using extra memory is the real challenge.

This was my first Read Pointer + Write Pointer problem and taught me how in-place array modification works.

The Two Pointer technique used here is one of the most important interview patterns and appears in many future LeetCode problems.
