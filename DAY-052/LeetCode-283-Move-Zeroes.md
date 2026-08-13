# LeetCode #283 — Move Zeroes
---

# Problem Statement

Given an integer array `nums`, move all `0`s to the end of the array while maintaining the relative order of the non-zero elements.

You must perform this operation **in-place** without making a copy of the array.

---

# Examples

## Example 1

```text
Input

nums = [0,1,0,3,12]

Output

[1,3,12,0,0]
```

---

## Example 2

```text
Input

nums = [0]

Output

[0]
```

---

# Constraints

```
1 <= nums.length <= 10⁴

-2³¹ <= nums[i] <= 2³¹-1
```

---

# Understanding the Problem

The question is NOT asking us to sort the array.

It is NOT asking us to remove zeros.

It only asks us to

```
Move every zero

to the end.
```

While doing that,

the order of all non-zero elements must remain exactly the same.

---

# Important Observation

Suppose

```
0 1 0 3 12
```

Expected

```
1 3 12 0 0
```

Notice

```
1

↓

3

↓

12
```

Their order never changes.

This is called

```
Maintaining Relative Order.
```

---

# What Does "In-place" Mean?

"In-place" means

```
Modify

the original array.
```

Do NOT create another array.

Example

❌ Wrong

```python
answer = []
```

✅ Correct

```
Modify nums itself.
```

---

# Brute Force Idea

Whenever we find

```
0
```

Shift every element after it

one position left.

Then place

```
0
```

at the end.

Repeat until all zeros reach the end.

---

# Brute Force Algorithm

1. Traverse the array.
2. Whenever a zero is found,
3. Shift every remaining element left.
4. Put zero at the end.
5. Continue until the array is finished.

---

# Brute Force Dry Run

Input

```
0 1 0 3 12
```

First zero

```
0 1 0 3 12

↓

1 0 3 12 0
```

Second zero

```
1 0 3 12 0

↓

1 3 12 0 0
```

Finished.

---

# Complexity Analysis (Brute Force)

Time Complexity

```
O(n²)
```

because every zero may require shifting many elements.

Space Complexity

```
O(1)
```

---

# Why Is Brute Force Slow?

Suppose

```
0 0 0 0 1 2 3
```

Every zero shifts almost the whole remaining array.

```
Shift

↓

Shift

↓

Shift

↓

Shift
```

Lots of repeated work.

---

# Better Observation

Instead of moving

the zeros,

what if we only move

the non-zero elements?

Ignore every zero.

Copy only

```
1

3

12
```

to the front.

The remaining positions naturally become zeros.

This immediately reduces the complexity to

```
O(n)
```

---

# Pattern Connection

This problem belongs to the

```
In-place Modification
```

pattern.

```
Remove Element (#27)

↓

Move Zeroes (#283)

↓

Remove Duplicates (#26)

↓

Sort Array By Parity (#905)
```

All of them use

```
Reader

+

Writer
```

thinking.

---

# Learning Summary

In this part, I learned:

- The difference between removing and moving elements.
- What "maintaining relative order" means.
- Why brute force is O(n²).
- Why moving only the good elements is a much better idea.
- This problem belongs to the In-place Modification pattern.

---


# Optimal Approach — Reader & Writer

This problem is almost identical to

```
Remove Element (#27)
```

The only difference is

Instead of removing

```
val
```

we move

```
0
```

to the end.

---

# Reader & Writer Analogy

Imagine two people.

## 👀 Reader (`i`)

Reader checks every element.

Reader never writes.

Reader always moves.

---

## ✍️ Writer (`w`)

Writer rebuilds the array.

Writer only writes

non-zero elements.

Writer moves only after writing.

---

# Initial State

Example

```
nums

0 1 0 3 12
```

Initially

```
w = 0

i = 0
```

---

# Step-by-Step Intuition

Reader sees

```
0
```

Bad element.

Skip.

---

Reader sees

```
1
```

Good element.

Copy it

to Writer.

```
nums[w] = nums[i]
```

Now

old position

becomes

```
0
```

Move Writer.

Continue.

Repeat until Reader reaches the end.

---

# Why Do We Need

```python
if i != w
```

This is the most important part.

Suppose

```
nums

1 2 3
```

Initially

```
i = 0

w = 0
```

Reader and Writer

are standing

on the same position.

Copy

```
nums[0]=nums[0]
```

Nothing changes.

If we immediately write

```
nums[0]=0
```

we destroy

```
1
```

Therefore

```
Only replace

the old position

with zero

when

i != w.
```

---

# Understanding Every Line

```python
w = 0
```

Writer starts at the beginning.

---

```python
for i in range(len(nums)):
```

Reader scans every element.

---

```python
if nums[i] != 0:
```

Only non-zero elements are useful.

---

```python
nums[w] = nums[i]
```

Copy the good element

to the Writer position.

---

```python
if i != w:
```

Only erase

the old position

when Reader and Writer

are different.

---

```python
nums[i] = 0
```

Turn the old position

into zero.

---

```python
w += 1
```

Writer moves

to the next free position.

---

# Final Code

```python
class Solution(object):
    def moveZeroes(self, nums):
        w = 0

        for i in range(len(nums)):

            if nums[i] != 0:

                nums[w] = nums[i]

                if i != w:
                    nums[i] = 0

                w += 1
```

---

# Complete Dry Run

Input

```
nums = [0,1,0,3,0,0,12,5,0,8]
```

| Reader (`i`) | Value | Writer (`w`) | Action | Array |
|--------------|-------|--------------|--------|-------|
|0|0|0|Skip|0 1 0 3 0 0 12 5 0 8|
|1|1|0|Copy + Zero old|1 0 0 3 0 0 12 5 0 8|
|2|0|1|Skip|1 0 0 3 0 0 12 5 0 8|
|3|3|1|Copy + Zero old|1 3 0 0 0 0 12 5 0 8|
|4|0|2|Skip|...|
|5|0|2|Skip|...|
|6|12|2|Copy + Zero old|1 3 12 0 0 0 0 5 0 8|
|7|5|3|Copy + Zero old|1 3 12 5 0 0 0 0 0 8|
|8|0|4|Skip|...|
|9|8|4|Copy + Zero old|1 3 12 5 8 0 0 0 0 0|

Final Answer

```
1 3 12 5 8 0 0 0 0 0
```

---

# Complexity Analysis

### Time Complexity

```
O(n)
```

Each element is visited exactly once.

---

### Space Complexity

```
O(1)
```

No extra array is used.

---

# Common Mistakes

### ❌ Creating another array

The problem requires

```
In-place
```

---

### ❌ Moving Writer every iteration

Writer moves

only after writing.

---

### ❌ Forgetting

```python
if i != w
```

This destroys elements

when Reader and Writer

are on the same index.

---

### ❌ Trying to move zeros first

Instead,

move

the non-zero elements.

---

### ❌ Thinking this is a different pattern

It is almost the same as

```
Remove Element (#27)
```

Only one extra line is added.

---

# Pattern Recognition

Whenever a problem says

```
Move

Keep Order

In-place
```

Think

```
Reader

↓

Writer

↓

Copy Good Elements

↓

Clean Old Position

↓

Done
```

---

# Key Takeaways

- Ignore bad elements.
- Copy only the good elements.
- Reader always moves.
- Writer moves only after writing.
- `i != w` prevents destroying valid values.
- This is an extension of the Remove Element pattern.

---
