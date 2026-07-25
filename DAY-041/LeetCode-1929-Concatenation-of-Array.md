# LeetCode #1929 — Concatenation of Array

---

# Problem Statement

Given an integer array `nums` of length `n`, create an array `ans` of length `2n` such that:

```text
ans[i] = nums[i]

ans[i + n] = nums[i]
```

for every

```text
0 <= i < n
```

In simple words,

append the original array to itself.

Return the newly created array.

---

# Example 1

```text
Input

nums = [1,2,1]

Output

[1,2,1,1,2,1]
```

Explanation

```text
Original Array

[1,2,1]

↓

Copy Again

[1,2,1]

↓

Concatenate

[1,2,1,1,2,1]
```

---

# Example 2

```text
Input

nums = [1,3,2,1]

Output

[1,3,2,1,1,3,2,1]
```

---

# Constraints

```text
1 <= n <= 1000

1 <= nums[i] <= 1000
```

---

# Understanding the Problem

This problem is very straightforward.

It is **NOT** asking us to:

- Sort the array
- Remove duplicates
- Reverse the array

Instead, it simply asks us to:

> Create a new array that contains the original array **twice**.

Think of it like this:

```text
nums

[1,2,3]

↓

Copy

[1,2,3]

↓

Join Together

[1,2,3,1,2,3]
```

---

# Visual Representation

```text
nums

Index

0   1   2

↓

Value

1   2   3

--------------------------------

ans

Index

0   1   2   3   4   5

↓

Value

1   2   3   1   2   3
```

---

# Approach 1 — Manual Solution (Two Loops)

## Intuition

The simplest way is:

- Traverse the array once.
- Copy every element.
- Traverse the array again.
- Copy every element again.

---

## Algorithm

1. Create an empty answer array.
2. Traverse `nums`.
3. Append every element.
4. Traverse `nums` again.
5. Append every element again.
6. Return the answer.

---

## Code

```python
class Solution(object):

    def getConcatenation(self, nums):

        ans = []

        for i in range(len(nums)):
            ans.append(nums[i])

        for i in range(len(nums)):
            ans.append(nums[i])

        return ans
```

---

## Dry Run

```text
nums

[1,2,1]

Initially

ans = []

-------------------

First Loop

Append 1

ans

[1]

Append 2

[1,2]

Append 1

[1,2,1]

-------------------

Second Loop

Append 1

[1,2,1,1]

Append 2

[1,2,1,1,2]

Append 1

[1,2,1,1,2,1]

Return
```

---

## Time Complexity

```text
O(n)
```

Explanation

```
First Loop

O(n)

+

Second Loop

O(n)

=

O(2n)

↓

O(n)
```

---

## Space Complexity

```text
O(n)
```

The answer array stores `2n` elements.

Ignoring constants,

```
O(2n)

↓

O(n)
```

---

# Approach 2 — One Loop (Index Assignment)

## Intuition

Instead of using two loops,

create the answer array with the required size first.

The problem statement already tells us where every value should go.

```text
ans[i]

↓

First Half

-------------------

ans[i+n]

↓

Second Half
```

Using one traversal,

fill both positions.

---

## Algorithm

1. Create an array of size `2n`.
2. Traverse the original array once.
3. Store the current element at

```text
ans[i]
```

4. Store the same element again at

```text
ans[i+n]
```

5. Return the answer.

---

## Code

```python
class Solution(object):

    def getConcatenation(self, nums):

        ans = [0] * (2 * len(nums))

        for i in range(len(nums)):

            ans[i] = nums[i]

            ans[i + len(nums)] = nums[i]

        return ans
```

---

## Dry Run

```text
nums

[1,2,1]

Length

3

Create

ans

[0,0,0,0,0,0]

-------------------

i = 0

ans[0] = 1

ans[3] = 1

↓

[1,0,0,1,0,0]

-------------------

i = 1

ans[1] = 2

ans[4] = 2

↓

[1,2,0,1,2,0]

-------------------

i = 2

ans[2] = 1

ans[5] = 1

↓

[1,2,1,1,2,1]

Return
```

---

## Why do we create

```python
ans = [0] * (2 * len(nums))
```

?

Because we want to assign values directly using indexes.

Without creating the array first,

this would fail:

```python
ans[i] = nums[i]
```

because the indexes do not exist yet.

---

## Why don't we use append()?

`append()` grows the list.

Example

```python
ans.append(5)
```

adds a new element.

But here,

the answer array already has enough space.

So we simply replace values.

```python
ans[index] = value
```

---

## Time Complexity

```text
O(n)
```

Only one traversal.

---

## Space Complexity

```text
O(n)
```

---

# Approach 3 — Pythonic

Python allows list concatenation directly.

---

## Method 1

```python
class Solution(object):

    def getConcatenation(self, nums):

        return nums + nums
```

---

## Method 2

```python
class Solution(object):

    def getConcatenation(self, nums):

        return nums * 2
```

---

## Why does

```python
nums * 2
```

work?

Example

```python
nums

[1,2,3]
```

Python repeats the list.

```text
[1,2,3]

×

2

↓

[1,2,3,1,2,3]
```

---

## Time Complexity

```text
O(n)
```

---

## Space Complexity

```text
O(n)
```

---

# Comparison of Approaches

| Approach | Time | Space | Interview Friendly |
|----------|------|-------|--------------------|
| Manual Two Loops | O(n) | O(n) | ⭐⭐⭐⭐⭐ |
| One Loop (Index Assignment) | O(n) | O(n) | ⭐⭐⭐⭐⭐ |
| Pythonic (`nums * 2`) | O(n) | O(n) | ⭐⭐☆☆☆ |

---

# Which Approach Should You Use?

### During Interviews

Prefer

```text
Approach 2
```

Why?

Because it demonstrates:

- Array indexing
- Understanding of the problem statement
- Memory allocation
- One-pass traversal

---

### During Coding Contests

You may simply write

```python
return nums * 2
```

because it is shorter and easier to read.

---

# Pattern

```text
Array

↓

Traversal

↓

Array Construction

↓

Index Assignment
```

---

# Key Insight

The problem statement itself provides the solution:

```text
ans[i]

=

nums[i]

----------------

ans[i+n]

=

nums[i]
```

Instead of growing the array twice,

create the required size first,

then fill both positions during a single traversal.

---

# Mistakes I Faced While Solving

## Mistake 1

I first solved it using two loops.

It worked correctly,

but I wanted to reduce it to one loop.

---

## Mistake 2

I tried

```python
ans = []
```

and then

```python
ans[i] = nums[i]
```

This caused an error because the list was empty.

The index did not exist.

---

## Mistake 3

I tried

```python
ans[i+n].append(nums[i])
```

But

```python
ans[i+n]
```

is an integer,

not a list.

`append()` only works on lists.

The correct way is

```python
ans[i+n] = nums[i]
```

---

## What I Learned

There are two ways to build a list:

### Growing the list

```python
append()
```

Used when the list is empty.

---

### Filling existing positions

```python
ans[index] = value
```

Used when the list already has allocated space.

Understanding the difference between these two operations is important for many array problems.

---

# Interview Notes

- Easy array problem.
- Tests understanding of array construction.
- Demonstrates difference between:
  - `append()`
  - Index assignment.
- Good beginner problem for array traversal.
- One-loop solution is cleaner than two loops.

---

# LeetCode Submission

# Intuition

The task is to create a new array by appending the original array to itself. A simple way to achieve this is to traverse the array twice and append each element to a new array during both traversals.

# Approach

- Create an empty array `ans`.
- Traverse the original array once and append each element to `ans`.
- Traverse the array a second time and append each element again.
- Return the resulting array.

# Complexity

- **Time complexity:** `O(n)`

  Two traversals of the array take `O(2n)`, which simplifies to `O(n)`.

- **Space complexity:** `O(n)`

  The answer array stores `2n` elements, which is `O(n)` after ignoring constants.