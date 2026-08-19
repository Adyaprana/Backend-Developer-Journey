# LeetCode #189 — Rotate Array

---

# Problem Statement

Given an integer array `nums`, rotate the array to the right by `k` steps.

You must modify the array **in-place**.

---

# Examples

## Example 1

```text
Input

nums = [1,2,3,4,5,6,7]

k = 3
```

Output

```text
[5,6,7,1,2,3,4]
```

---

## Example 2

```text
Input

nums = [-1,-100,3,99]

k = 2
```

Output

```text
[3,99,-1,-100]
```

---

# Constraints

```text
1 <= nums.length <= 10⁵

-2³¹ <= nums[i] <= 2³¹-1

0 <= k <= 10⁵
```

---

# Understanding the Problem

The problem asks us to rotate the array to the **right** by `k` positions.

Example

```text
nums

1 2 3 4 5 6 7
```

Rotate once

```text
7 1 2 3 4 5 6
```

Rotate twice

```text
6 7 1 2 3 4 5
```

Rotate three times

```text
5 6 7 1 2 3 4
```

This is the final answer.

---

# What Does Rotation Mean?

Every element moves exactly

```text
k
```

positions to the right.

Example

```text
nums = [1,2,3,4,5,6,7]

k = 3
```

| Number | Old Index | New Index |
|--------|----------:|----------:|
|1|0|3|
|2|1|4|
|3|2|5|
|4|3|6|
|5|4|0|
|6|5|1|
|7|6|2|

Notice that every element moves exactly

```text
+3
```

positions.

---

# Important Observation 1

Some elements move outside the array.

Example

```text
Number 5

Old Index = 4

New Index = 7
```

But the array has only

```text
0 1 2 3 4 5 6
```

indices.

There is no

```text
Index 7
```

So we wrap around to the beginning.

This is why we use

```text
Modulo (%)
```

---

# The New Index Formula

Every element follows one formula.

```text
New Index = (Old Index + k) % Length
```

Example

```text
Old Index = 5

k = 3

Length = 7
```

```text
(5 + 3) % 7

=

8 % 7

=

1
```

So

```text
6
```

moves to

```text
Index 1
```

---

# Important Observation 2

Suppose

```text
nums = [1,2,3]

k = 5
```

Do we really rotate

```
5
```

times?

No.

Because

```text
Rotate 3 times

↓

Original Array
```

So

```text
Rotate 5

=

Rotate 2
```

Therefore

before doing anything

we calculate

```text
k = k % len(nums)
```

Example

```text
5 % 3 = 2
```

Now

```text
Rotate 2
```

gives exactly the same answer.

---

# Brute Force Approach

The simplest idea is

Rotate

```
One Step
```

exactly

```
k
```

times.

Example

```text
1 2 3 4 5
```

Rotate once

```text
5 1 2 3 4
```

Rotate again

```text
4 5 1 2 3
```

Continue until

```
k
```

rotations are completed.

---

# Why Is Brute Force Slow?

Suppose

```text
Length = 100000

k = 99999
```

Almost every element is moved

```
99999
```

times.

This becomes

```text
O(n × k)
```

which is too slow.

---

# Better Approach — Extra Array

Instead of moving elements one by one,

create another array.

```python
arr = [0] * len(nums)
```

For every element

1. Calculate its new position.
2. Put it directly into that position.

Formula

```text
New Index = (Old Index + k) % n
```

Example

```text
nums

1 2 3 4 5 6 7
```

New positions

| Number | Old Index | New Index |
|--------|----------:|----------:|
|1|0|3|
|2|1|4|
|3|2|5|
|4|3|6|
|5|4|0|
|6|5|1|
|7|6|2|

New array becomes

```text
5 6 7 1 2 3 4
```

Finally,

copy the new array back into

```text
nums
```

---
# Full Code
```python
# Approach 1: Using Extra Array
class Solution(object):
    def rotate(self, nums, k):
        arr = [0] * len(nums)
        k = k % len(nums)
        for i in range(len(nums)):
            New_Index = (i + k) % len(nums)
            arr[New_Index] = nums[i]
        nums[:] = arr

```

---

# Complete Dry Run

Input

```text
nums = [1,2,3,4,5,6,7]

k = 3
```

Initially

```text
arr

[0,0,0,0,0,0,0]
```

---

### Step 1

```text
i = 0

Number = 1

New Index = (0+3)%7 = 3
```

```text
arr

0 0 0 1 0 0 0
```

---

### Step 2

```text
i = 1

Number = 2

New Index = 4
```

```text
0 0 0 1 2 0 0
```

---

### Step 3

```text
i = 2

Number = 3

New Index = 5
```

```text
0 0 0 1 2 3 0
```

---

### Step 4

```text
i = 3

Number = 4

New Index = 6
```

```text
0 0 0 1 2 3 4
```

---

### Step 5

```text
i = 4

Number = 5

New Index = 0
```

```text
5 0 0 1 2 3 4
```

---

### Step 6

```text
i = 5

Number = 6

New Index = 1
```

```text
5 6 0 1 2 3 4
```

---

### Step 7

```text
i = 6

Number = 7

New Index = 2
```

```text
5 6 7 1 2 3 4
```

Final Answer

```text
5 6 7 1 2 3 4
```

---

# Complexity Analysis (Extra Array)

### Time Complexity

```text
O(n)
```

Every element is visited exactly once.

---

### Space Complexity

```text
O(n)
```

Because we create another array.

---

# Common Mistakes

## ❌ Forgetting

```python
k = k % len(nums)
```

Example

```text
nums = [1,2,3]

k = 5
```

Without modulo,

we do unnecessary work.

---

## ❌ Using

```python
nums = arr
```

This only changes the local variable.

It does **not** modify the original list.

Correct way

```python
nums[:] = arr
```

---

## ❌ Wrong Formula

Many beginners try

```text
Old Index - k
```

The correct formula for **right rotation** is

```text
(Old Index + k) % n
```

---

## ❌ Forgetting Modulo

Without

```text
%
```

indices become

```text
7

8

9
```

which are outside the array.

---

# Pattern Recognition

This problem introduces a new pattern.

```text
Array Rotation

↓

Index Mapping

↓

New Index Formula

↓

Modulo Arithmetic
```

The formula

```text
New Index = (Old Index + k) % n
```

appears in many problems involving

- Circular Arrays
- Ring Buffers
- Hash Tables
- Cyclic Rotation

---

# Interview Questions

### Q1

Why do we calculate

```python
k = k % len(nums)
```

before rotating?

---

### Q2

Why do we need modulo in the new index formula?

---

### Q3

Why can't we directly write

```python
nums[new_index] = nums[i]
```

inside the original array?

---

### Q4

What is the time complexity of the extra array solution?

---

### Q5

Can this problem be solved without creating another array?

Answer

```
Yes.

Using the Reverse Method.
```

---

# Learning Summary

After solving Part 1, I learned:

- Every element moves exactly `k` positions to the right.
- The new position is calculated using

```text
(Old Index + k) % n
```

- Modulo wraps indices back into the array.
- `k = k % len(nums)` removes unnecessary rotations.
- The extra-array solution is easy to understand and runs in `O(n)` time.
- This problem introduces the **Array Rotation / Index Mapping** pattern.

---

# LeetCode #189 — Rotate Array

---

# Optimal Approach — Reverse Method

The Reverse Method is the most famous and optimal solution for this problem.

Instead of moving every element individually,

we reverse different parts of the array.

This gives an

```text
O(n)
```

solution with

```text
O(1)
```

extra space.

---

# The Big Idea

Suppose

```text
nums = [1,2,3,4,5,6,7]

k = 3
```

Expected Answer

```text
5 6 7 1 2 3 4
```

Notice something.

The last

```text
k
```

elements

```text
5 6 7
```

must come to the front.

The remaining elements

```text
1 2 3 4
```

must move to the back.

Instead of moving numbers one by one,

we move them as groups using reverse operations.

---

# Step 1 — Reverse the Entire Array

Original

```text
1 2 3 4 5 6 7
```

Reverse

```text
7 6 5 4 3 2 1
```

Notice

The last three elements

```text
5 6 7
```

have reached the front,

but they are reversed.

---

# Step 2 — Reverse the First k Elements

Current

```text
7 6 5 4 3 2 1
```

Reverse first

```text
k = 3
```

elements

```text
7 6 5

↓

5 6 7
```

Array becomes

```text
5 6 7 4 3 2 1
```

The first part is now correct.

---

# Step 3 — Reverse the Remaining Elements

Current

```text
5 6 7 4 3 2 1
```

Reverse

```text
4 3 2 1

↓

1 2 3 4
```

Final Answer

```text
5 6 7 1 2 3 4
```

Exactly what we wanted.

---

# Why Does This Work?

Think of the array as two groups.

Original

```text
1 2 3 4 | 5 6 7
```

Goal

```text
5 6 7 | 1 2 3 4
```

The reverse operations simply swap these two groups while restoring the correct order inside each group.

---

# Algorithm

### Step 1

Reduce unnecessary rotations.

```python
k = k % len(nums)
```

---

### Step 2

Reverse the whole array.

---

### Step 3

Reverse the first

```text
k
```

elements.

---

### Step 4

Reverse the remaining elements.

Finished.

---

# Final Code

```python
class Solution(object):
    def rotate(self, nums, k):

        k = k % len(nums)

        nums.reverse()

        nums[:k] = nums[:k][::-1]

        nums[k:] = nums[k:][::-1]
```

---

# Complete Dry Run

Input

```text
nums = [1,2,3,4,5,6,7]

k = 3
```

---

### Step 1

```text
k = 3 % 7

↓

3
```

---

### Step 2

Reverse entire array

```text
1 2 3 4 5 6 7

↓

7 6 5 4 3 2 1
```

---

### Step 3

Reverse first three elements

```text
7 6 5

↓

5 6 7
```

Array becomes

```text
5 6 7 4 3 2 1
```

---

### Step 4

Reverse remaining elements

```text
4 3 2 1

↓

1 2 3 4
```

Final

```text
5 6 7 1 2 3 4
```

---

# Another Dry Run

Input

```text
nums = [1,2,3]

k = 5
```

First

```text
k = 5 % 3

↓

2
```

Original

```text
1 2 3
```

Reverse all

```text
3 2 1
```

Reverse first two

```text
2 3 1
```

Reverse remaining

```text
2 3 1
```

Final Answer

```text
2 3 1
```

Exactly the expected result.

---

# Why k % len(nums)?

Suppose

```text
nums = [1,2,3]

k = 5
```

Rotating

```text
5
```

times is exactly the same as rotating

```text
2
```

times.

Because

```text
5 % 3 = 2
```

Using modulo avoids unnecessary work.

---

# Complexity Analysis

## Time Complexity

```text
O(n)
```

- Reverse entire array → O(n)
- Reverse first k elements → O(k)
- Reverse remaining elements → O(n-k)

Overall

```text
O(n)
```

---

## Space Complexity

```text
O(1)
```

Algorithmically, no additional array is created.

> **Note (Python):** In this learning version, slicing (`nums[:k][::-1]`) creates temporary lists internally. Many interviewers focus on the algorithm itself. Later, when you learn the two-pointer reverse helper, you'll implement the reversals manually to achieve true constant extra space.

---

# Common Mistakes

## ❌ Forgetting

```python
k = k % len(nums)
```

Large values of

```text
k
```

cause unnecessary rotations.

---

## ❌ Reversing in the Wrong Order

Correct order

```text
Reverse Entire Array

↓

Reverse First k

↓

Reverse Remaining
```

Changing the order produces incorrect results.

---

## ❌ Forgetting the Last Reverse

Stopping after two reverses gives

```text
5 6 7 4 3 2 1
```

which is not the final answer.

---

## ❌ Trying to Move Every Element Individually

Doing

```python
nums[new_index] = nums[i]
```

inside the same array overwrites values that have not yet been moved.

---

# Pattern Recognition

Whenever you see

```text
Rotate Array

OR

Move Last k Elements To Front
```

Think immediately

```text
Reverse Whole Array

↓

Reverse First k

↓

Reverse Remaining
```

This is a classic interview pattern.

---

# Interview Questions

### Q1

Why is reversing easier than moving each element individually?

---

### Q2

Why do we reverse the entire array first?

---

### Q3

Why do we reverse the first

```text
k
```

elements?

---

### Q4

Why do we reverse the remaining elements?

---

### Q5

Why do we calculate

```python
k = k % len(nums)
```

before starting?

---

### Q6

Can this solution be implemented without using Python's built-in `reverse()`?

Answer

```
Yes.

Using a helper reverse() function with two pointers.

(We'll learn this later.)
```

---

# Pattern Library Update

```text
Arrays
│
├── Running Sum
│
├── Prefix Sum
│
├── In-place Modification
│
├── Merge from End
│
└── Array Rotation
     │
     ├── Extra Array (Index Mapping)
     └── Reverse Method
```

---

