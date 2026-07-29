# LeetCode #303 — Range Sum Query - Immutable

---

# Problem Statement

Given an integer array `nums`, handle multiple queries of the following type:

```text
sumRange(left, right)
```

Return the **sum of the elements** between index `left` and index `right` (inclusive).

The array **never changes** after it is created.

This is why the problem is called **Immutable**.

---

# Example

```text
Input

nums = [-2,0,3,-5,2,-1]

Queries

sumRange(0,2)

sumRange(2,5)

sumRange(0,5)
```

Output

```text
1

-1

-3
```

---

## Explanation

```text
nums

Index

0   1   2   3   4   5

↓

Value

-2  0   3  -5  2  -1
```

### Query 1

```text
sumRange(0,2)

↓

-2 + 0 + 3

↓

1
```

---

### Query 2

```text
sumRange(2,5)

↓

3 + (-5) + 2 + (-1)

↓

-1
```

---

### Query 3

```text
sumRange(0,5)

↓

Sum of entire array

↓

-3
```

---

# Constraints

```text
1 <= nums.length <= 10⁴

-10⁵ <= nums[i] <= 10⁵

0 <= left <= right < nums.length

sumRange() can be called many times.
```

---

# Understanding the Problem

This problem is **NOT** asking us to calculate one range sum.

Instead,

it asks us to calculate **many** range sums.

Think about this.

```text
sumRange(0,5)

sumRange(1,4)

sumRange(2,5)

sumRange(0,3)

sumRange(3,5)

...

Thousands of times
```

If we calculate every query using a loop,

we repeat the same work again and again.

The interviewer wants us to think:

> Can we do some work once and answer every future query quickly?

This idea is called **Preprocessing**.

---

# What is Prefix Sum?

A Prefix Sum array stores the cumulative sum from the beginning of the array.

Example

```text
nums

2   4   6   8
```

Build Prefix Sum

```text
2

2+4 = 6

2+4+6 = 12

2+4+6+8 = 20
```

Store it.

```text
prefix

[2,6,12,20]
```

Notice

```text
prefix[2]

=

2+4+6
```

We already know the sum up to index `2`.

---

# Why Prefix Sum?

Suppose someone asks

```text
sumRange(2,3)
```

Without Prefix Sum

```text
6 + 8

↓

14
```

Need a loop.

With Prefix Sum

```text
prefix

2   6   12   20
```

We already know

```text
20

=

2+4+6+8
```

Remove

```text
2+4

=

6
```

```text
20 - 6

↓

14
```

No loop.

Only one subtraction.

---

# Important Things to Think About

## Observation 1

The array **never changes**.

That means we only need to build the Prefix Sum **once**.

---

## Observation 2

There will be many queries.

Instead of recalculating every range,

store useful information beforehand.

---

## Observation 3

The constructor

```python
__init__()
```

runs only once.

Perfect place to build the Prefix Sum.

---

## Observation 4

Every future query should be answered in

```text
O(1)
```

time.

---

# Prefix Sum Formula

Suppose

```text
prefix

[2,6,12,20]
```

---

## Case 1

```text
left = 0
```

Example

```text
sumRange(0,2)
```

Need

```text
2+4+6
```

Already stored.

```text
Answer

=

prefix[2]
```

---

## Case 2

```text
left > 0
```

Example

```text
sumRange(2,3)
```

Need

```text
6+8
```

Take

```text
prefix[3]

↓

20
```

Remove everything before

index 2.

```text
prefix[1]

↓

6
```

```text
20 - 6

↓

14
```

General Formula

```text
prefix[right]

-

prefix[left-1]
```

---

# Algorithm

## Step 1

Build the Prefix Sum array once inside `__init__()`.

---

## Step 2

Whenever `sumRange()` is called,

check

```text
left == 0 ?
```

If yes

return

```text
prefix[right]
```

Otherwise

return

```text
prefix[right] - prefix[left-1]
```

---

# Code

```python
class NumArray(object):

    def __init__(self, nums):

        self.prefix = []

        running_sum = 0

        for i in range(len(nums)):

            running_sum += nums[i]

            self.prefix.append(running_sum)

    def sumRange(self, left, right):

        if left == 0:

            return self.prefix[right]

        else:

            return self.prefix[right] - self.prefix[left-1]
```

---

# Dry Run

Input

```text
nums

[2,4,6,8]
```

---

## Building Prefix Sum

Initially

```text
running_sum = 0

prefix = []
```

Read

```text
2
```

```text
running_sum

0+2

↓

2
```

```text
prefix

[2]
```

---

Read

```text
4
```

```text
running_sum

2+4

↓

6
```

```text
prefix

[2,6]
```

---

Read

```text
6
```

```text
running_sum

6+6

↓

12
```

```text
prefix

[2,6,12]
```

---

Read

```text
8
```

```text
running_sum

12+8

↓

20
```

```text
prefix

[2,6,12,20]
```

---

# Query 1

```text
sumRange(0,2)
```

Since

```text
left == 0
```

Answer

```text
prefix[2]

↓

12
```

Correct

```text
2+4+6 = 12
```

---

# Query 2

```text
sumRange(1,2)
```

```text
prefix[2]

↓

12
```

Minus

```text
prefix[0]

↓

2
```

```text
12 - 2

↓

10
```

Correct

```text
4+6 = 10
```

---

# Query 3

```text
sumRange(2,3)
```

```text
20

-

6

↓

14
```

Correct

```text
6+8 = 14
```

---

# Time Complexity

## Building Prefix Sum

```text
O(n)
```

Runs only once.

---

## sumRange()

```text
O(1)
```

Only one subtraction.

---

# Space Complexity

```text
O(n)
```

For storing the Prefix Sum array.

---

# Comparison

| Approach | Build | Query | Space |
|----------|------|-------|--------|
| Brute Force | O(1) | O(n) | O(1) |
| Prefix Sum | O(n) | O(1) | O(n) |

---

# Pattern Learned

```text
Array

↓

Prefix Sum

↓

Preprocessing

↓

Range Query

↓

O(1) Answer
```

---

# Key Insight

Instead of solving every query independently,

perform some preprocessing once.

Store cumulative sums.

Then every future range sum becomes a simple subtraction.

---

# What I Learned

- Prefix Sum stores cumulative sums.
- `__init__()` is the perfect place for preprocessing because it runs only once.
- `sumRange()` should not use loops.
- Every query can be answered using one subtraction.
- This pattern is used whenever multiple range queries are asked on an immutable array.

---

# Interview Notes

This is one of the most important Prefix Sum problems.

It teaches:

- Preprocessing
- Prefix Sum
- Range Query
- Time vs Space tradeoff
- Using constructors (`__init__`) effectively

Related Problems

- 1480. Running Sum of 1d Array
- 724. Find Pivot Index
- 560. Subarray Sum Equals K
- 238. Product of Array Except Self
- 304. Range Sum Query 2D - Immutable

---

# LeetCode Submission

## Intuition

Since the array never changes, repeatedly calculating the sum for every query is inefficient. Instead, preprocess the array by building a Prefix Sum array once, allowing each range sum query to be answered in constant time.

## Approach

- Build a Prefix Sum array in the constructor.
- Each position stores the cumulative sum from the beginning of the array.
- For a query:
  - If `left == 0`, return `prefix[right]`.
  - Otherwise, return `prefix[right] - prefix[left - 1]`.

## Complexity

- **Time Complexity**
  - Constructor: `O(n)`
  - `sumRange()`: `O(1)`

- **Space Complexity**
  - `O(n)`